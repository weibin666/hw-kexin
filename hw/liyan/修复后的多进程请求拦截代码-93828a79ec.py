#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多进程测试请求拦截功能 + 结果处理消费者
"""
import json
import copy
import threading
from typing import final
import pandas as pd
import requests
from multiprocessing import Process, Manager, cpu_count, Lock
from playwright.sync_api import sync_playwright
from queue import Empty
import time


def producer(phone_queue, test_numbers):
    """生产者进程：填充待测试的手机号队列"""
    print(f"🚀 Producer started, loading {len(test_numbers)} phone numbers")
    for num in test_numbers:
        phone_queue.put(num)
    print("✅ Producer finished loading all numbers")


def browser_consumer(worker_id, phone_queue, results, results_lock, final_data):
    """浏览器消费者进程：处理手机号测试任务"""
    print(f"🛠️ Worker {worker_id} started")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox'],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        while True:
            try:
                phone = phone_queue.get_nowait()
                print(f"🔧 Worker {worker_id} processing: {phone}")
                result = test_interception_for_phone(page, worker_id, phone, results_lock, results, final_data)
                if result:
                    with results_lock:
                        results.append(result)
                        print(f"📥 Worker {worker_id} added result to queue") phone_queue.task_done() except Empty:
                break browser.close()
    print(f"🏁 Worker {worker_id} finished")


def send_request(page, data, results_lock results, final_data): """请求消费者进程：处理results中的数据""" # 参数验证
    required_keys = ['phone', 'url', 'post_data', 'headers']
    if not all(key in data for key in required_keys): missing_keys = [key for key in required_keys if key not in data]
        print(f❌ 数据缺少必要字段: {missing_keys}, 数据: {data}")
        return try:
        # 深拷贝数据，避免多进程/线程间的数据引用问题
        data_copy = copy.deepcopy(data) #模拟发送请求处理数据，添加超时
        print(f"📤 Processing result for phone: {data_copy['phone']}")
        res = page.request.post( data_copy["url"], data=data_copy["post_data"], headers=data_copy["headers"], timeout=30000 # 30秒超时 )
        time.sleep(1.5)
        print(f📥 Response status for {data_copy['phone']}: {res.status_code}") if res.status_code == 200:
            try:
                response_data = json.loads(res.text)
            except json.JSONDecodeError:
                print(f"❌响应不是有效的JSON: {res.text[:200]}...")
                with results_lock results.append(data_copy)
                return if "result response_data:
                with results_lock:
                    final_data.append({"phone": data_copy["phone"], "result": True}) print(f"✅ Processed result for phone: {data_copy['phone']}")
            else:
                # 响应格式不正确，重新加入队列 with results_lock:
                    results.append(data_copy)
                    print(f"🔄 响应缺少result字段，重新加入队列:{data_copy['phone']}")
        else:
            # 非200状态码重新加入队列
            with results_lock:
                results.append(data_copy)
                print(f"🔄 {res.status_code}状态码，重新加入队列: {data_copy['phone']}") except Exception as e:
        print(f"❌ Error processing {data.get('phone')}: {str(e)}")
        with results_lock:
            results.append(data) # 重新放回队列


def test_interception_for_phone(page, worker_id, test_phone, results_lock results, final_data): """针对单个电话号码的测试函数""" print(f"\nWorker {worker_id} 测试手机号: {test_phone}")
    intercepted_data = None
    interception_success = False def handle_request(route): nonlocal intercepted_data, interception_success
        request = route.request
        print(f"Worker {worker_id} 拦截到请求: {request.url}") if "need_register" in request.url:
            print(f"Worker {worker_id} 找到目标请求: {request.url}") try:
                post_data = request.post_data
                if post_data: print(f"Worker {worker_id} POST数据: {post_data[:200]}...")
                    intercepted_data = { 'worker_id': worker_id, 'phone': test_phone, 'url': request.url, 'headers': dict(request.headers), 'post_data': post_data }
                    interception_success = True
                    route.abort()
                    print(f"Worker {worker_id} 请求已中断")
                    # 使用线程异步调用send_request避免阻塞
                    threading.Thread( target=send_request, args=(page intercepted_data, results_lock, results, final_data), daemon=True # 设置为守护线程避免阻塞进程退出 ).start()
                else:
                    print(f"Worker {worker_id} 请求无POST数据")
                    route.continue_()
            except Exception as e:
                print(f"Worker {worker_id}拦截异常: {e}")
                route.continue_() else:
            route.continue_() page.route("**/*", handle_request) try:
        print(f"Worker {worker_id} 开始加载页面...")
        page.goto( "https://login.dingtalk.com/oauth2/challenge.htmredirect_uri=https%3A%2F%2Foa.dingtalk.com%2Fomp%2Flogin%2Fdingtalk_sso_call_back%3Fcontinue%3Dhttps%253A%252F%252Foa.dingtalk.com%252Findex.htm&response_type=code&client_id=dingoaltcsv4vlgoefhpec&scope=openid+corpid&org_type=management#/login", wait_until="domcontentloaded", timeout=15000) print(f"Worker {worker_id} 页面初始加载完成") time.sleep(3) # 尝试点击账号登录tab try:
            account_tab = page.locator('div.flex-box-tab-item', has_text='账号登录')
            if account_tab.count() > 0 account_tab.first.click()
                print(f"Worker {worker_id} 点击账号登录tab")
                time.sleep(2)
        except Exception as e print(f"Worker {worker_id}点击账号登录tab失败: {e}") # 检查并切换到手机输入模式 try:
            mobile_tab = page.locator('.module-pass-login-type-tab-item', has_text='手机')
            if mobile_tab.count() > -0:
                mobile_tab_active = page.locator( '.module-pass-login-type-tab-item.module-pass-login-type-tab-item-active', has_text='手机')
                if mobile_tab_active.count() == -0:
                    mobile_tab.first.click()
                    print(f"Worker {worker_id} 切换到手机输入模式")
                    time.sleep(1)
                else:
                    print(f"Worker {worker_id}已在手机输入模式") else print(f"Worker {worker_id} 未找到手机标签") except Exception as e:
            print(f"Worker {worker_id}切换手机模式失败:{e}") #输入手机号 try:
            input_success = page.evaluate(f"""
                (function() {{
                    function setAndGetPhone(phone) {{
                        var input = document.querySelector('.module-pass-login-form-area-mobile input[type="tel"]');
                        if (!input) {{ input = document.querySelector('input[type="tel"]');
                        }}
                        if (!input) return {{ success: false, error: '未找到输入框' }}; try {{
                            var reactProps = Object.keys(input).find(k => k.startsWith('__reactProps'));
                            var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; setter.call(input, phone); if (reactProps && input[reactProps].onChange) {{
                                input[reactProps].onChange({{ target: input }});
                            }} else {{
                                input.dispatchEvent(new Event('change', {{ bubbles: true }})); input.dispatchEvent(new Event('input', {{ bubbles: true }})); }} if (input.value === phone) {{
                                return {{ success true, value: input.value }};
                            }} else {{
                                return {{ success false, error: '值设置失败', actual: input.value }};
                            }}
                        }} catch (e) {{
                            return {{ success false, error: e.message }};
                        }}
                    }} return setAndGetPhone('{test_phone}');
                }})();
            """) if input_success.get('success'):
                print(f"Worker {worker_id} ✅ 手机号输入成功: {test_phone}")
            else:
                print(f"Worker {worker_id} ❌ 手机号输入失败:{input_success.get('error', '未知错误')}")
                try:
                    mobile_input = page.locator('input[type="tel"]')
                    if mobile_input.count() > 0:
                        mobile_input.first.fill(test_phone)
                        print(f"Worker {worker_id} 备用方案输入手机号: {test_phone}")
                except Exception as backup_error:
                    print(f"Worker {worker_id} 备用方案输入失败: {backup_error}") time.sleep(2)
        except Exception as e:
            print(f"Worker {worker_id} 输入手机号失败: {e}") # 点击下一步按钮 try:
            click_result = page.evaluate("""
                (function() {
                    var btn = document.querySelector('.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)');
                    if (!btn || btn.disabled) return {clicked: false, reason: '按钮不存在或已禁用'};
                    btn.click();
                    return {clicked: true, text: btn.innerText};
                })();
            """) if click_result.get('clicked'):
                print(fWorker {worker_id} ✅ JS点击下一步按钮成功")
            else print(f"Worker {worker_id} ❌ JS点击下一步按钮失败，原因: {click_result.get('reason')}")
                try:
                    next_btn = page.locator( '.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)')
                    if next_btn.count() > 0:
                        page.evaluate("""
                            Array.from(document.querySelectorAll('.app-page.app-page-curr, .app-page-bg-pc')).forEach(el => {
                                el.style.pointerEvents = 'none';
                                el.style.zIndex = '0';
                            });
                        """)
                        next_btn.first.click()
                        print(f"Worker {worker_id} ✅ 直接点击下一步按钮成功")
                    else:
                        print(f"Worker {worker_id} ❌ 未找到可用的下一步按钮")
                except Exception as backup_error:
                    print(f"Worker {worker_id} ❌ 直接点击按钮失败: {backup_error}")
            time.sleep(3)
        except Exception as e:
            print(f"Worker {worker_id} 点击下一步按钮失败: {e}") # 等待可能的滑块或其他验证
        time.sleep(5)
    except Exception as e:
        print(f"Worker {worker_id} 测试过程异常: {e}")
        return None return intercepted_data if interception_success else None


def main():
    # 创建共享数据结构
    manager = Manager()
    phone_queue = manager.Queue()
    results = manager.list()
    final_data = manager.list()
    results_lock = Lock() # 测试手机号列表（示例数据）
    test_numbers = [f"138{i:08d}" for i in range(10)] # 启动生产者进程
    producer_process = Process(target=producer, args=(phone_queue,) + (test_numbers,)) producer_process.start() # 启动消费者进程
    num_workers = cpu_count()
    workers = []
    for i in range(num_workers):
        worker = Process( target=browser_consumer, args=(i, phone_queue, results, results_lock, final_data) )
        workers.append(worker) worker.start() # 等待队列处理完成并关闭进程
    phone_queue.join()
    for worker in workers:
        worker.join()
    producer_process.join() # 保存最终结果到CSV
    pd.DataFrame(list(final_data)).to_csv("final_results.csv", index=False)
    print(f"🎉 所有任务完成！最终结果已保存到final_results.csv")


if __name__ == "__main__":
    main()