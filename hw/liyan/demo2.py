#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多线程测试请求拦截功能
"""
import json
import sys
import os
import time
import threading
from queue import Queue
from playwright.sync_api import sync_playwright

# 共享电话号码列表和结果列表
phone_numbers = Queue()
results = []
# 线程锁保护共享结果
results_lock = threading.Lock()


def worker(worker_id):
    """工作线程函数，每个线程运行一个独立的浏览器实例"""
    print(f"Worker {worker_id} 启动")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        while not phone_numbers.empty():
            try:
                phone = phone_numbers.get_nowait()
                test_interception_for_phone(page, worker_id, phone)
                phone_numbers.task_done()
            except:
                break

        browser.close()
    print(f"Worker {worker_id} 结束")


def test_interception_for_phone(page, worker_id, test_phone):
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


def main():
    # 初始化测试手机号
    fw = open("test_res.json", "w", encoding="utf-8")
    test_numbers = [i.strip() for i in open("phone_numbers.txt", "r", encoding="utf-8").readlines()]  # 示例号码
    for num in test_numbers:
        phone_numbers.put(num)

    # 创建并启动工作线程
    threads = []
    num_workers = 5  # 根据实际情况调整线程数

    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i + 1,))
        t.start()
        threads.append(t)

    # 等待所有任务完成
    phone_numbers.join()

    # 等待所有线程结束
    for t in threads:
        t.join()

    # 打印汇总结果
    print("\n测试完成，汇总结果:")
    for result in results:
        print(f"\nWorker {result['worker_id']} 拦截结果:")
        print(f"手机号: {result['phone']}")
        print(f"URL: {result['url']}")
        print(f"POST数据(前200字符): {result['post_data'][:200]}...")
        fw.write(json.dumps(result, ensure_ascii=False).strip() + "\n")
        fw.flush()


if __name__ == "__main__":
    main()
