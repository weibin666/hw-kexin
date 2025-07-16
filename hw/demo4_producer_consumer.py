#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多进程测试请求拦截功能 + 结果处理消费者
"""
import json
from typing import final
import pandas as pd
import requests
from multiprocessing import Process, Manager, cpu_count, Lock
from playwright.sync_api import sync_playwright
from queue import Empty
import time
import random


def proxy_fetcher():
    for _ in range(100):
        res = requests.get(
            "https://service.ipzan.com/core-extract?num=1&no=20240512326767842864&minute=1&format=json&pool=quality&mode=auth&secret=4tes3co25ogs3o")
        json_data = json.loads(res.text)
        if json_data["code"] == 0:
            ip = json_data["data"]["list"][0]["ip"]
            port = json_data["data"]["list"][0]["port"]
            account = json_data["data"]["list"][0]["account"]
            password = json_data["data"]["list"][0]["password"]
            proxies = {
                "server": f"http://{ip}:{port}",
                "username": account,
                "password": password
            }
            return proxies
        else:
            continue


class DynamicProxyManager:
    def __init__(self, lock, proxy_fetcher, rotate_interval=20):
        self.proxy_fetcher = proxy_fetcher  # 代理获取函数
        self.current_proxy = None
        self.rotate_interval = rotate_interval
        self.lock = lock

    def get_proxy(self, counter):
        print("counter: ",counter)
        counter.value += 1
        if counter.value % self.rotate_interval == 0 or self.current_proxy is None:
            self.current_proxy = self.proxy_fetcher()
            print(f"Using new proxy: {self.current_proxy}")
        return self.current_proxy


def producer(phone_queue, test_numbers):
    """生产者进程：填充待测试的手机号队列"""
    print(f"🚀 Producer started, loading {len(test_numbers)} phone numbers")
    for num in test_numbers:
        phone_queue.put(num)
    print("✅ Producer finished loading all numbers")


def browser_consumer(worker_id, phone_queue, results, results_lock, final_data, counter):
    """浏览器消费者进程：处理手机号测试任务"""
    print(f"🛠️ Worker {worker_id} started")
    with results_lock:
        proxy=DynamicProxyManager(results_lock, proxy_fetcher).get_proxy(counter)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox'],
            # proxy=proxy,
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            # proxy=proxy,
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
                        print(f"📥 Worker {worker_id} added result to queue")
                phone_queue.task_done()

            except Empty:
                break
        browser.close()
    print(f"🏁 Worker {worker_id} finished")


def send_request(page, data, results_lock, results, final_data):
    """请求消费者进程：处理results中的数据"""
    try:
        # 模拟发送请求处理数据
        print(f"📤 Processing result for phone: {data['phone']}")
        res = requests.post(data["url"], data=data["post_data"], headers=data["headers"])
        time.sleep(1.5)
        print(f"{data['phone']} send_request状态码： ", res.status_code)
        print(f"请求数据 {data}")
        print(f"{data['phone']} send_request结果： ", res.text)
        if res.status_code == 200:
            if "result" in json.loads(res.text).keys():
                with results_lock:
                    final_data.append({"phone": data["phone"], "result": json.loads(res.text)["result"]})
                    print(f"✅ Processed result for phone: {data['phone']}")
            else:
                # 有滑块出现，处理滑块，经过页面分析，滑块需要拖动280px
                with results_lock:
                    results.append(data)
    except Exception as e:
        print(f"❌ Error processing data: {str(e)}")
        with results_lock:
            results.append(data)  # 重新放回队列


def test_interception_for_phone(page, worker_id, test_phone, results_lock, results, final_data):
    """针对单个电话号码的测试函数"""
    print(f"\nWorker {worker_id} 测试手机号: {test_phone}")
    intercepted_data = None
    interception_success = False

    def handle_request(route):
        nonlocal intercepted_data, interception_success
        request = route.request
        print(f"Worker {worker_id} 拦截到请求: {request.url}")

        if "need_register" in request.url:
            print(f"Worker {worker_id} 找到目标请求: {request.url}")
            try:
                post_data = request.post_data
                if post_data:
                    print(f"Worker {worker_id} POST数据: {post_data[:200]}...")
                    intercepted_data = {
                        'worker_id': worker_id,
                        'phone': test_phone,
                        'url': request.url,
                        'headers': dict(request.headers),
                        'post_data': post_data
                    }
                    interception_success = True
                    # weibin 20250713 15:29新增
                    # send_request(page, intercepted_data, results_lock, results, final_data)
                    route.abort()
                    print(f"Worker {worker_id} 请求已中断")
                else:
                    print(f"Worker {worker_id} 请求无POST数据")
                    route.continue_()
            except Exception as e:
                print(f"Worker {worker_id} 拦截异常: {e}")
                route.continue_()
        else:
            route.continue_()

    page.route("**/*", handle_request)
    try:
        print(f"Worker {worker_id} 开始加载页面...")
        page.goto(
            "https://login.dingtalk.com/oauth2/challenge.htm?redirect_uri=https%3A%2F%2Foa.dingtalk.com%2Fomp%2Flogin%2Fdingtalk_sso_call_back%3Fcontinue%3Dhttps%253A%252F%252Foa.dingtalk.com%252Findex.htm&response_type=code&client_id=dingoaltcsv4vlgoefhpec&scope=openid+corpid&org_type=management#/login",
            wait_until="domcontentloaded", timeout=15000)

        print(f"Worker {worker_id} 页面初始加载完成")
        time.sleep(3)

        # 尝试点击账号登录tab
        try:
            account_tab = page.locator('div.flex-box-tab-item', has_text='账号登录')
            if account_tab.count() > 0:
                account_tab.first.click()
                print(f"Worker {worker_id} 点击账号登录tab")
                time.sleep(2)
        except Exception as e:
            print(f"Worker {worker_id} 点击账号登录tab失败: {e}")

        # 检查并切换到手机输入模式
        try:
            mobile_tab = page.locator('.module-pass-login-type-tab-item', has_text='手机')
            if mobile_tab.count() > 0:
                mobile_tab_active = page.locator(
                    '.module-pass-login-type-tab-item.module-pass-login-type-tab-item-active', has_text='手机')
                if mobile_tab_active.count() == 0:
                    mobile_tab.first.click()
                    print(f"Worker {worker_id} 切换到手机输入模式")
                    time.sleep(1)
                else:
                    print(f"Worker {worker_id} 已在手机输入模式")
            else:
                print(f"Worker {worker_id} 未找到手机标签")
        except Exception as e:
            print(f"Worker {worker_id} 切换手机模式失败: {e}")

        # 输入手机号
        try:
            input_success = page.evaluate(f"""
                (function() {{
                    function setAndGetPhone(phone) {{
                        var input = document.querySelector('.module-pass-login-form-area-mobile input[type="tel"]');
                        if (!input) {{
                            input = document.querySelector('input[type="tel"]');
                        }}
                        if (!input) return {{ success: false, error: '未找到输入框' }};

                        try {{
                            var reactProps = Object.keys(input).find(k => k.startsWith('__reactProps'));
                            var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;

                            setter.call(input, phone);

                            if (reactProps && input[reactProps].onChange) {{
                                input[reactProps].onChange({{ target: input }});
                            }} else {{
                                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            }}

                            if (input.value === phone) {{
                                return {{ success: true, value: input.value }};
                            }} else {{
                                return {{ success: false, error: '值设置失败', actual: input.value }};
                            }}
                        }} catch (e) {{
                            return {{ success: false, error: e.message }};
                        }}
                    }}

                    return setAndGetPhone('{test_phone}');
                }})();
            """)

            if input_success.get('success'):
                print(f"Worker {worker_id} ✅ 手机号输入成功: {test_phone}")
            else:
                print(f"Worker {worker_id} ❌ 手机号输入失败: {input_success.get('error', '未知错误')}")
                try:
                    mobile_input = page.locator('input[type="tel"]')
                    if mobile_input.count() > 0:
                        mobile_input.first.fill(test_phone)
                        print(f"Worker {worker_id} 备用方案输入手机号: {test_phone}")
                except Exception as backup_error:
                    print(f"Worker {worker_id} 备用方案输入失败: {backup_error}")

            time.sleep(2)
        except Exception as e:
            print(f"Worker {worker_id} 输入手机号失败: {e}")

        # 点击下一步按钮
        try:
            click_result = page.evaluate("""
                (function() {
                    var btn = document.querySelector('.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)');
                    if (!btn || btn.disabled) return {clicked: false, reason: '按钮不存在或已禁用'};
                    btn.click();
                    return {clicked: true, text: btn.innerText};
                })();
            """)
            solve_slider(page)
            if click_result.get('clicked'):
                print(f"Worker {worker_id} ✅ JS点击下一步按钮成功")
            else:
                print(f"Worker {worker_id} ❌ JS点击下一步按钮失败，原因: {click_result.get('reason')}")
                try:
                    next_btn = page.locator(
                        '.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)')
                    if next_btn.count() > 0:
                        page.evaluate("""
                            Array.from(document.querySelectorAll('.app-page.app-page-curr, .app-page-bg-pc')).forEach(el => {
                                el.style.pointerEvents = 'none';
                                el.style.zIndex = '0';
                            });
                        """)
                        next_btn.first.click()
                        # weibin add at 20250713 21:34
                        solve_slider(page)
                        print(f"Worker {worker_id} 备用方案点击按钮成功")
                except Exception as backup_error:
                    print(f"Worker {worker_id} 备用方案点击失败: {backup_error}")

            time.sleep(3)

            btn_disabled = page.evaluate("""
                (function() {
                    var btn = document.querySelector('.module-pass-login-form-area-active .base-comp-button-type-primary');
                    return btn && btn.classList.contains('base-comp-button-disabled');
                })();
            """)

            if btn_disabled:
                print(f"Worker {worker_id} 按钮已变为禁用，提交成功！")
            else:
                print(f"Worker {worker_id} 按钮未变为禁用，可能未提交或页面无响应。")

        except Exception as e:
            print(f"Worker {worker_id} 点击按钮异常: {e}")

        # 保存结果
        if interception_success:
            with results_lock:
                results.append(intercepted_data)
            print(f"Worker {worker_id} ✅ 拦截成功！")
        else:
            print(f"Worker {worker_id} ❌ 拦截失败")
    except Exception as e:
        print(f"Worker {worker_id} 测试异常: {e}")
    if intercepted_data:
        send_request(page, intercepted_data, results_lock, results, final_data)


# 生成更接近人类的滑动轨迹（贝塞尔曲线）
def generate_bezier_curve(start_x, start_y, end_x, end_y):
    """生成贝塞尔曲线路径"""
    control_point1 = (start_x + random.randint(50, 100), start_y + random.randint(-20, 20))
    control_point2 = (end_x - random.randint(50, 100), end_y + random.randint(-20, 20))

    points = []
    for t in range(0, 101):
        t /= 100.0
        x = (1 - t) ** 3 * start_x + 3 * (1 - t) ** 2 * t * control_point1[0] + 3 * (1 - t) * t ** 2 * \
            control_point2[0] + t ** 3 * end_x
        y = (1 - t) ** 3 * start_y + 3 * (1 - t) ** 2 * t * control_point1[1] + 3 * (1 - t) * t ** 2 * \
            control_point2[1] + t ** 3 * end_y
        points.append((x, y))
    return points


def solve_slider(page):
    """优化版滑块验证处理，基于实际页面元素结构"""
    try:
        # 根据HTML分析的实际滑块元素选择器
        slider_container = page.locator('.nocaptcha')
        slider_button = page.locator('.nc_iconfont.btn_slide')  # nc_iconfont btn_slide
        success_indicator = page.locator('.nc-lang-cnt')
        refresh_button = page.locator('.nc_refresh')
        # 等待滑块容器加载完成
        slider_container.wait_for(timeout=15000)
        print("检测到滑块容器，准备处理验证")

        # 获取滑块位置和大小（处理可能的iframe嵌套）
        frame = None
        if page.frames:
            # 检查是否在iframe中
            for f in page.frames:
                if f.locator('.nocaptcha').count() > 0:
                    frame = f
                    break

        # 使用正确的上下文（主页面或iframe）
        context = frame if frame else page
        slider = context.locator('.nc_iconfont.btn_slide')
        bounding_box = slider.bounding_box()

        if not bounding_box:
            print("无法获取滑块位置，尝试刷新滑块")
            refresh_button.click()
            time.sleep(1)
            return solve_slider(page)  # 递归重试

        # 计算滑动路径（基于实际HTML中的滑块宽度调整）
        start_x, start_y = bounding_box['x'] + bounding_box['width'] / 2, bounding_box['y'] + bounding_box['height'] / 2

        # 分析HTML发现滑块轨道长度在280px左右，增加随机偏移
        track_length = 280 + random.randint(-5, 5)
        # 生成轨迹点
        end_x = start_x + track_length
        end_y = start_y + random.randint(-5, 5)  # 微小的垂直偏移
        path = generate_bezier_curve(start_x, start_y, end_x, end_y)

        # 执行滑动操作
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        time.sleep(random.uniform(0.1, 0.3))  # 按下后短暂停顿

        # 按轨迹移动鼠标
        for i, (x, y) in enumerate(path):
            # 模拟人类速度变化：先加速后减速
            speed = int(100 + 200 * (abs(50 - i) / 50))  # 中间快两端慢
            page.mouse.move(x, y, delay=speed)

            # 随机添加微小停顿
            if random.random() < 0.1:
                time.sleep(random.uniform(0.01, 0.03))

        page.mouse.up()
        time.sleep(1.5)  # 等待验证结果

        # 检查验证状态（根据HTML中的成功提示元素）
        if success_indicator.count() == 0:
            print("滑块验证成功")
            return True

        # 验证失败处理
        print("滑块验证失败，尝试刷新并重试")
        refresh_button.click()
        time.sleep(random.uniform(1, 2))
        return solve_slider(page)  # 递归重试

    except Exception as e:
        print(f"滑块处理异常: {str(e)}")
        # 尝试刷新滑块并重试
        try:
            refresh_button.click()
            time.sleep(2)
            return solve_slider(page)
        except:
            return False


def main():
    # 读取测试数据
    with open("phone_numbers.txt", "r", encoding="utf-8") as f:
        test_numbers = [line.strip() for line in f if line.strip()]
    # 创建共享数据结构
    manager = Manager()
    phone_queue = manager.Queue()
    results = manager.list()
    # processed_data = manager.list()
    final_data = manager.list()
    counter = manager.Value('i', 0)  # 'i' 表示整数类型，初始值为0
    lock = manager.Lock()

    # 启动生产者
    producer_proc = Process(target=producer, args=(phone_queue, test_numbers))
    producer_proc.start()

    # 启动浏览器消费者
    browser_workers = []
    for i in range(min(cpu_count(), len(test_numbers))):
        p = Process(target=browser_consumer, args=(i + 1, phone_queue, results, lock,
                                                   final_data,
                                                   counter))  # worker_id, phone_queue, results, results_lock
        p.start()
        browser_workers.append(p)
    # 等待生产者完成
    producer_proc.join()
    # 等待浏览器消费者完成
    for p in browser_workers:
        p.join()
    # 等待请求消费者处理剩余数据
    while len(results) > 0:
        time.sleep(1)
    phones = []
    status = []
    for item in final_data:
        phones.append(item['phone'])
        status.append(item['result'])
    df = pd.DataFrame({"phone": phones, "status": status})
    with pd.ExcelWriter("final_result.xlsx") as writer:
        df.to_excel(writer, sheet_name='钉钉-电话号码检测结果', index=False)
    print(f"\n🎉 All done! Processed {len(phones)} items")


if __name__ == "__main__":
    main()
