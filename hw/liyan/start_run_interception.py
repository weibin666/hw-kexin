#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试请求拦截功能
"""

import sys
import os
import time
import threading
from playwright.sync_api import sync_playwright

def test_interception():
    """测试请求拦截功能"""
    print("开始测试请求拦截功能...")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # 设置为False以便观察
        context = browser.new_context()
        page = context.new_page()
        
        # 设置请求拦截
        intercepted_data = None
        interception_success = False
        
        def handle_request(route):
            nonlocal intercepted_data, interception_success
            request = route.request
            print(f"拦截到请求: {request.url}")
            
            if "need_register" in request.url:
                print(f"找到目标请求: {request.url}")
                try:
                    post_data = request.post_data
                    if post_data:
                        print(f"POST数据: {post_data[:200]}...")
                        intercepted_data = {
                            'url': request.url,
                            'headers': dict(request.headers),
                            'post_data': post_data
                        }
                        interception_success = True
                        route.abort()
                        print("请求已中断")
                    else:
                        print("请求无POST数据")
                        route.continue_()
                except Exception as e:
                    print(f"拦截异常: {e}")
                    route.continue_()
            else:
                route.continue_()
        
        page.route("**/*", handle_request)
        
        try:
            # 导航到登录页面
            print("开始加载页面...")
            
            # 使用更短的超时时间，因为拦截到login_with_qr就表示页面已加载
            page.goto("https://login.dingtalk.com/oauth2/challenge.htm?redirect_uri=https%3A%2F%2Foa.dingtalk.com%2Fomp%2Flogin%2Fdingtalk_sso_call_back%3Fcontinue%3Dhttps%253A%252F%252Foa.dingtalk.com%252Findex.htm&response_type=code&client_id=dingoaltcsv4vlgoefhpec&scope=openid+corpid&org_type=management#/login", 
                     wait_until="domcontentloaded", timeout=15000)
            
            print("页面初始加载完成")
            
            # 等待login_with_qr请求完成（页面真正加载完成）
            print("等待页面完全加载...")
            time.sleep(3)  # 等待login_with_qr请求发送
            
            # 先尝试点击账号登录tab（如果存在）
            try:
                account_tab = page.locator('div.flex-box-tab-item', has_text='账号登录')
                if account_tab.count() > 0:
                    account_tab.first.click()
                    print("点击账号登录tab")
                    time.sleep(2)  # 等待页面切换
            except Exception as e:
                print(f"点击账号登录tab失败: {e}")
            
            # 检查并切换到手机输入模式
            try:
                # 检查当前是否在邮箱模式，如果是则切换到手机模式
                mobile_tab = page.locator('.module-pass-login-type-tab-item', has_text='手机')
                if mobile_tab.count() > 0:
                    # 检查手机标签是否已经是激活状态
                    mobile_tab_active = page.locator('.module-pass-login-type-tab-item.module-pass-login-type-tab-item-active', has_text='手机')
                    if mobile_tab_active.count() == 0:
                        # 手机标签不是激活状态，需要点击切换到手机模式
                        mobile_tab.first.click()
                        print("切换到手机输入模式")
                        time.sleep(1)
                    else:
                        print("已在手机输入模式")
                else:
                    print("未找到手机标签，可能页面结构不同")
            except Exception as e:
                print(f"切换手机模式失败: {e}")
            
            # 输入测试手机号
            test_phone = "13800138000"
            try:
                # 使用专业的JavaScript方法输入手机号
                input_success = page.evaluate(f"""
                    (function() {{
                        function setAndGetPhone(phone) {{
                            var input = document.querySelector('.module-pass-login-form-area-mobile input[type="tel"]');
                            if (!input) {{
                                input = document.querySelector('input[type="tel"]');
                            }}
                            if (!input) {{
                                return {{ success: false, error: '未找到输入框' }};
                            }}
                            
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
                    print(f"✅ 手机号输入成功: {test_phone}")
                    print(f"   实际值: {input_success.get('value')}")
                else:
                    print(f"❌ 手机号输入失败: {input_success.get('error', '未知错误')}")
                    if 'actual' in input_success:
                        print(f"   实际值: {input_success.get('actual')}")
                    
                    # 备用方案
                    try:
                        mobile_input = page.locator('input[type="tel"]')
                        if mobile_input.count() > 0:
                            mobile_input.first.fill(test_phone)
                            print(f"备用方案输入手机号: {test_phone}")
                        else:
                            print("备用方案也找不到输入框")
                    except Exception as backup_error:
                        print(f"备用方案输入失败: {backup_error}")
                
                time.sleep(2)
            except Exception as e:
                print(f"输入手机号失败: {e}")
            
            # 用JS点击"下一步"按钮，并检测是否点击成功
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
                    print(f"✅ JS点击下一步按钮成功，按钮文本: {click_result.get('text')}")
                else:
                    print(f"❌ JS点击下一步按钮失败，原因: {click_result.get('reason')}")
                    
                    # 备用方案：尝试其他选择器
                    try:
                        next_btn = page.locator('.module-pass-login-form-area-active .base-comp-button-type-primary:not(.base-comp-button-disabled)')
                        if next_btn.count() > 0:
                            # 移除阻挡元素
                            page.evaluate("""
                                Array.from(document.querySelectorAll('.app-page.app-page-curr, .app-page-bg-pc')).forEach(el => {
                                    el.style.pointerEvents = 'none';
                                    el.style.zIndex = '0';
                                });
                            """)
                            next_btn.first.click()
                            print("备用方案点击按钮成功")
                        else:
                            print("备用方案也找不到可用按钮")
                    except Exception as backup_error:
                        print(f"备用方案点击失败: {backup_error}")
                
                # 等待页面响应
                time.sleep(3)
                
                # 检查按钮是否变为禁用（表示已提交）
                btn_disabled = page.evaluate("""
                    (function() {
                        var btn = document.querySelector('.module-pass-login-form-area-active .base-comp-button-type-primary');
                        return btn && btn.classList.contains('base-comp-button-disabled');
                    })();
                """)
                
                if btn_disabled:
                    print("按钮已变为禁用，提交成功！")
                else:
                    print("按钮未变为禁用，可能未提交或页面无响应。")
                
            except Exception as e:
                print(f"点击按钮异常: {e}")
            
            # 检查结果
            if interception_success:
                print("✅ 拦截成功！")
                print(f"URL: {intercepted_data['url']}")
                print(f"POST数据: {intercepted_data['post_data'][:200]}...")
            else:
                print("❌ 拦截失败")
            
        except Exception as e:
            print(f"测试异常: {e}")
        
        finally:
            # 等待用户观察
            input("按回车键关闭浏览器...")
            browser.close()

if __name__ == "__main__":
    test_interception()