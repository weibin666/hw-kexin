#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多进程测试请求拦截功能
"""
import json
import os
import time
from multiprocessing import Process, Queue, Manager, cpu_count, Lock
from playwright.sync_api import sync_playwright


def producer(phone_queue, test_numbers):
    """生产者进程：填充待测试的手机号队列"""
    print(f"Producer started, loading {len(test_numbers)} phone numbers")
    for num in test_numbers:
        phone_queue.put(num)
    print("Producer finished loading all numbers")


def consumer(worker_id, phone_queue, results, results_lock):
    """消费者进程：处理手机号测试任务"""
    print(f"Worker {worker_id} started")

    with sync_playwright() as p:
        # 优化浏览器配置
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        while True:
            try:
                phone = phone_queue.get_nowait()
                print(f"Worker {worker_id} processing: {phone}")

                # 执行测试
                result = test_interception_for_phone(page, worker_id, phone)

                # 保存结果
                if result:
                    with results_lock:
                        results.append(result)

                # 任务完成标记
                phone_queue.task_done()

            except:
                break

        browser.close()
    print(f"Worker {worker_id} finished")


def test_interception_for_phone(page, worker_id, test_phone):
    """优化后的测试函数"""
    intercepted_data = None
    interception_success = False

    def handle_request(route):
        nonlocal intercepted_data, interception_success
        request = route.request

        if "need_register" in request.url:
            try:
                post_data = request.post_data
                if post_data:
                    intercepted_data = {
                        'worker_id': worker_id,
                        'phone': test_phone,
                        'url': request.url,
                        'headers': dict(request.headers),
                        'post_data': post_data
                    }
                    interception_success = True
                    route.abort()
                else:
                    route.continue_()
            except Exception as e:
                print(f"Worker {worker_id} 拦截异常: {e}")
                route.continue_()
        else:
            route.continue_()

    page.route("**/*", handle_request)

    try:
        # 加载页面
        page.goto(
            "https://login.dingtalk.com/oauth2/challenge.htm?redirect_uri=https%3A%2F%2Foa.dingtalk.com%2Fomp%2Flogin%2Fdingtalk_sso_call_back%3Fcontinue%3Dhttps%253A%252F%252Foa.dingtalk.com%252Findex.htm&response_type=code&client_id=dingoaltcsv4vlgoefhpec&scope=openid+corpid&org_type=management#/login",
            wait_until="domcontentloaded",
            timeout=15000
        )

        # 切换到账号登录
        try:
            account_tab = page.locator('div.flex-box-tab-item', has_text='账号登录')
            if account_tab.count() > 0:
                account_tab.first.click()
                time.sleep(2)
        except:
            pass

        # 切换到手机输入模式
        try:
            mobile_tab = page.locator('.module-pass-login-type-tab-item', has_text='手机')
            if mobile_tab.count() > 0:
                mobile_tab_active = page.locator(
                    '.module-pass-login-type-tab-item.module-pass-login-type-tab-item-active', has_text='手机')
                if mobile_tab_active.count() == 0:
                    mobile_tab.first.click()
                    time.sleep(1)
        except:
            pass

        # 输入手机号
        try:
            page.fill('input[type="tel"]', test_phone)
            page.dispatch_event('input[type="tel"]', 'change')
            time.sleep(2)
        except Exception as e:
            print(f"Worker {worker_id} 输入手机号失败: {e}")

        # 点击下一步
        try:
            next_btn = page.locator(
                '.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)')
            if next_btn.count() > 0:
                next_btn.first.click()
                time.sleep(3)
        except Exception as e:
            print(f"Worker {worker_id} 点击按钮异常: {e}")

        if interception_success:
            print(f"Worker {worker_id} ✅ 拦截成功！")
            return intercepted_data
        else:
            print(f"Worker {worker_id} ❌ 拦截失败")
            return None

    except Exception as e:
        print(f"Worker {worker_id} 测试异常: {e}")
        return None


def main():
    # 读取测试数据
    with open("phone_numbers.txt", "r", encoding="utf-8") as f:
        test_numbers = [line.strip() for line in f if line.strip()]

    # 创建共享数据结构
    manager = Manager()
    phone_queue = manager.Queue()  # 任务队列
    results = manager.list()  # 结果列表
    results_lock = manager.Lock()  # 结果锁

    # 启动生产者进程
    producer_process = Process(target=producer, args=(phone_queue, test_numbers))
    producer_process.start()

    # 根据CPU核心数创建消费者进程
    num_workers = min(cpu_count(), len(test_numbers))  # 优化进程数
    consumers = []

    for i in range(num_workers):
        p = Process(target=consumer, args=(i + 1, phone_queue, results, results_lock))
        p.start()
        consumers.append(p)

    # 等待所有进程完成
    producer_process.join()

    # 等待队列处理完成
    while not phone_queue.empty():
        time.sleep(1)

    # 终止消费者进程
    for p in consumers:
        p.terminate()

    # 保存结果
    with open("test_res.json", "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"\n测试完成，共处理 {len(results)} 条有效数据")


if __name__ == "__main__":
    main()