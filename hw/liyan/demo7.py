# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多进程测试请求拦截功能 + 结果处理消费者 (优化版)
优化点：
1. 实现每20次请求自动更换代理
2. 添加滑块验证自动处理逻辑
3. 增强代理获取稳定性和异常处理
4. 优化资源管理和进程安全
"""
import json
import pandas as pd
import requests
from multiprocessing import Process, Manager, cpu_count, Lock
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from queue import Empty
import time
import random
import json
import requests
import time
import random
from playwright.sync_api import sync_playwright, ProxySettings

# 全局配置
REQUESTS_PER_PROXY = 20  # 每20次请求更换一次代理
SLIDER_DISTANCES = [250, 280]  # 滑块可能的拖动距离
PROXY_RETRY_LIMIT = 5  # 代理获取重试次数
PAGE_LOAD_TIMEOUT = 30000  # 页面加载超时时间(毫秒)
# 代理配置常量
PROXY_TEST_URL = "https://www.baidu.com/"  # 用于测试代理连通性的URL
PROXY_CONNECT_TIMEOUT = 10  # 代理连接超时时间(秒)
PROXY_RETRY_DELAY = 3  # 代理重试延迟(秒)
MAX_PROXY_RETRIES = 3  # 代理最大重试次数

def test_proxy_connectivity(proxy):
    """测试代理是否可以正常连接"""
    try:
        # 使用requests测试代理连通性
        proxies = {
            "http": proxy["full_url"],
            "https": proxy["full_url"]
        }

        # 测试连接目标网站
        response = requests.get(
            PROXY_TEST_URL,
            proxies=proxies,
            timeout=PROXY_CONNECT_TIMEOUT
        )

        if response.status_code == 200:
            return True

        print(f"代理测试失败，状态码: {response.status_code}")
        return False

    except Exception as e:
        print(f"代理连接测试失败: {str(e)}")
        return False

def get_proxy():
    """获取代理IP，增加详细错误处理和格式验证"""
    for attempt in range(PROXY_RETRY_LIMIT):
        try:
            res = requests.get(
                "https://service.ipzan.com/core-extract?num=1&no=20240512326767842864&minute=1&format=json&pool=quality&mode=auth&secret=4tes3co25ogs3o",
                timeout=10
            )
            res.raise_for_status()  # 检查HTTP错误状态码
            json_data = json.loads(res.text)

            if json_data["code"] == 0 and json_data["data"]["list"]:
                proxy_info = json_data["data"]["list"][0]

                # 验证代理信息完整性
                required_fields = ["ip", "port", "account", "password"]
                if not all(field in proxy_info for field in required_fields):
                    print(f"代理信息不完整: {proxy_info}")
                    continue

                # 构建标准代理格式
                proxy = {
                    "server": f"http://{proxy_info['ip']}:{proxy_info['port']}",
                    "username": proxy_info["account"],
                    "password": proxy_info["password"],
                    "full_url": f"http://{proxy_info['account']}:{proxy_info['password']}@{proxy_info['ip']}:{proxy_info['port']}"
                }

                # 测试代理连通性
                if test_proxy_connectivity(proxy):
                    print(f"成功获取并验证代理: {proxy_info['ip']}:{proxy_info['port']}")
                    return proxy
                else:
                    print(f"代理不可用: {proxy_info['ip']}:{proxy_info['port']}")

            print(f"获取代理失败，响应: {json_data}")

        except requests.exceptions.RequestException as e:
            print(f"代理API请求异常(尝试{attempt + 1}/{PROXY_RETRY_LIMIT}): {str(e)}")
        except json.JSONDecodeError:
            print(f"代理API响应格式错误(尝试{attempt + 1}/{PROXY_RETRY_LIMIT})")
        except Exception as e:
            print(f"获取代理时发生未知错误(尝试{attempt + 1}/{PROXY_RETRY_LIMIT}): {str(e)}")

        if attempt < PROXY_RETRY_LIMIT - 1:
            time.sleep(PROXY_RETRY_DELAY)

    raise Exception("达到最大代理获取重试次数")

def create_browser_context(p, proxy):
    """创建带有正确代理配置的浏览器上下文"""
    try:
        # 构建Playwright代理配置
        proxy_settings = ProxySettings(
            server=proxy["server"],
            username=proxy["username"],
            password=proxy["password"]
        )
        print("proxy_settings: ", proxy_settings)
        # 启动浏览器并配置代理
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--ignore-certificate-errors',  # 忽略证书错误
                '--disable-blink-features=AutomationControlled'  # 隐藏自动化特征
            ],
        )

        # 创建上下文时应用代理
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            proxy=proxy_settings,
            ignore_https_errors=True  # 忽略HTTPS错误
        )
        page = context.new_page()
        return browser, context, page
        # # 验证浏览器代理是否生效
        # page = context.new_page()
        # try:
        #     page.goto(PROXY_TEST_URL, timeout=15000)
        #     page_content = page.content()
        #     proxy_ip = proxy["server"].split("//")[-1].split(":")[0]
        #
        #     if proxy_ip in page_content:
        #         print(f"浏览器代理配置成功: {proxy_ip}")
        #         return browser, context, page
        #     else:
        #         print(f"浏览器代理未生效，页面内容: {page_content[:200]}")
        #         browser.close()
        #         raise Exception("浏览器代理配置失败")

        # except Exception as e:
        #     print(f"浏览器代理测试失败: {str(e)}")
        #     browser.close()
        #     raise

    except Exception as e:
        print(f"创建浏览器上下文失败: {str(e)}")
        raise

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
        slider_container = page.locator('.nc_container')
        slider_button = page.locator('.nc_iconfont.btn_slide')
        success_indicator = page.locator('.nc-lang-cnt[data-nc-lang="success"]')
        refresh_button = page.locator('.nc_refresh')

        # 等待滑块容器加载完成
        slider_container.wait_for(timeout=15000)
        print("检测到滑块容器，准备处理验证")

        # 获取滑块位置和大小（处理可能的iframe嵌套）
        frame = None
        if page.frames:
            # 检查是否在iframe中
            for f in page.frames:
                if f.locator('.nc_container').count() > 0:
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
        if success_indicator.count() > 0:
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


def test_interception_for_phone(page, worker_id, test_phone, results_lock, results):
    """更新测试函数，添加滑块触发控制"""
    print(f"\nWorker {worker_id} 测试手机号: {test_phone}")
    intercepted_data = None
    interception_success = False
    request_attempts = 0
    MAX_ATTEMPTS = 5  # 最多尝试次数，确保触发滑块

    def handle_request(route):
        nonlocal intercepted_data, interception_success
        # [保持原有请求拦截逻辑不变]

    try:
        page.unroute("**/*")
        page.route("**/*", handle_request)

        while request_attempts < MAX_ATTEMPTS:
            request_attempts += 1
            print(f"尝试第 {request_attempts}/{MAX_ATTEMPTS} 次请求...")

            page.goto(
                "https://login.dingtalk.com/oauth2/challenge.htm?redirect_uri=https%3A%2F%2Foa.dingtalk.com%2Fomp%2Flogin%2Fdingtalk_sso_call_back%3Fcontinue%3Dhttps%253A%252F%252Foa.dingtalk.com%252Findex.htm&response_type=code&client_id=dingoaltcsv4vlgoefhpec&scope=openid+corpid&org_type=management#/login",
                wait_until="domcontentloaded",
                timeout=PAGE_LOAD_TIMEOUT
            )

            # 检测并处理滑块（根据用户反馈，频繁请求后出现）
            if request_attempts >= 3:  # 前2次可能不出现滑块，第3次开始检测
                print(f"第 {request_attempts} 次请求，检查滑块验证...")
                if page.locator('.nc_container').count() > 0:
                    print("检测到滑块验证，开始自动处理...")
                    if not solve_slider(page):
                        print("滑块验证失败，准备重试...")
                        continue  # 滑块失败，重试当前手机号

            # [保持原有输入手机号和点击按钮逻辑不变]

            # 检查是否成功拦截请求
            if interception_success:
                break

            # 未触发滑块时，主动刷新页面增加请求次数
            if request_attempts < MAX_ATTEMPTS:
                print("未触发滑块验证，刷新页面继续尝试...")
                page.reload(wait_until="domcontentloaded")
                time.sleep(random.uniform(2, 3))

        return intercepted_data if interception_success else None

    except Exception as e:
        print(f"测试异常: {e}")
        return None


def browser_consumer(worker_id, phone_queue, results, results_lock):
    """优化后的浏览器消费者，增强代理管理"""
    print(f"🛠️ Worker {worker_id} started")
    request_count = 0  # 请求计数器
    browser = None
    context = None
    page = None
    current_proxy = None
    proxy_retries = 0

    try:
        with sync_playwright() as p:
            while True:
                # 检查是否需要更换代理或初始化浏览器
                if (request_count % REQUESTS_PER_PROXY == 0) or not browser or proxy_retries >= MAX_PROXY_RETRIES:
                    # 关闭旧浏览器
                    if context:
                        try:
                            context.close()
                        except Exception:
                            pass
                    if browser:
                        try:
                            browser.close()
                        except Exception:
                            pass

                    # 获取新代理并创建浏览器上下文
                    try:
                        current_proxy = get_proxy()
                        browser, context, page = create_browser_context(p, current_proxy)
                        request_count = 0  # 重置计数器
                        proxy_retries = 0  # 重置代理重试计数
                        print(f"Worker {worker_id} 成功初始化新代理连接")

                    except Exception as e:
                        print(f"Worker {worker_id} 初始化代理失败: {str(e)}")
                        proxy_retries += 1
                        if proxy_retries >= MAX_PROXY_RETRIES:
                            print(f"Worker {worker_id} 达到最大代理重试次数，暂停任务")
                            time.sleep(60)  # 暂停60秒后再试
                        else:
                            time.sleep(PROXY_RETRY_DELAY * (proxy_retries + 1))  # 指数退避
                        continue

                try:
                    phone = phone_queue.get_nowait()
                    print(
                        f"🔧 Worker {worker_id} processing: {phone} (请求次数: {request_count + 1}/{REQUESTS_PER_PROXY})")

                    # 执行测试
                    result = test_interception_for_phone(page, worker_id, phone, results_lock, results)
                    if result:
                        with results_lock:
                            results.append(result)
                        print(f"📥 Worker {worker_id} added result to queue")

                    phone_queue.task_done()
                    request_count += 1
                    proxy_retries = 0  # 重置代理错误计数

                except Empty:
                    break
                except Exception as e:
                    print(f"Worker {worker_id} 处理任务异常: {str(e)}")
                    proxy_retries += 1
                    with results_lock:
                        results.append({"phone": phone, "error": str(e), "proxy_error": True})
                    phone_queue.task_done()

                    # 如果连续代理错误，触发代理更换
                    if proxy_retries >= MAX_PROXY_RETRIES:
                        print(f"Worker {worker_id} 检测到连续代理错误，准备更换代理")
                        request_count = REQUESTS_PER_PROXY  # 强制更换代理

    finally:
        # 确保资源释放
        if context:
            try:
                context.close()
            except Exception:
                pass
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        print(f"🏁 Worker {worker_id} finished")


def request_consumer(results, results_lock, processed_data, final_data):
    """请求消费者进程：处理results中的数据"""
    print("📡 Request consumer started")
    while True:
        with results_lock:
            if not results:
                time.sleep(4)
                continue
            data = results.pop(0)

        try:
            # 检查是否有错误信息
            if "error" in data:
                print(f"📤 处理错误数据 {data['phone']}: {data['error']}")
                with results_lock:
                    processed_data.append({"phone": data["phone"], "status": "error", "message": data["error"]})
                continue

            print(f"📤 Processing result for phone: {data['phone']}")
            res = requests.post(data["url"], data=data["post_data"], headers=data["headers"], timeout=15)
            time.sleep(random.uniform(1, 2))  # 随机延迟，模拟人类行为

            if res.status_code == 200:
                res_json = json.loads(res.text)
                if "result" in res_json:
                    with results_lock:
                        final_data.append({"phone": data["phone"], "result": True})
                        processed_data.append({"phone": data["phone"], "status": "success"})
                else:
                    # 检测到滑块，添加回队列重试
                    print(f"检测到滑块验证，将 {data['phone']} 重新加入队列")
                    with results_lock:
                        results.append(data)
            else:
                print(f"请求失败，状态码: {res.status_code}")
                with results_lock:
                    results.append(data)  # 重试

        except Exception as e:
            print(f"❌ Error processing data: {str(e)}")
            with results_lock:
                results.append(data)  # 异常时重试


def producer(phone_queue, test_numbers):
    """生产者进程：填充待测试的手机号队列"""
    print(f"🚀 Producer started, loading {len(test_numbers)} phone numbers")
    for num in test_numbers:
        phone_queue.put(num)
    print("✅ Producer finished loading all numbers")


def main():
    # 读取测试数据
    try:
        with open("phone_numbers.txt", "r", encoding="utf-8") as f:
            test_numbers = [line.strip() for line in f if line.strip()]
        if not test_numbers:
            print("错误：未找到测试手机号")
            return
    except Exception as e:
        print(f"读取手机号文件失败: {str(e)}")
        return

    # 创建共享数据结构
    manager = Manager()
    phone_queue = manager.Queue()
    results = manager.list()
    processed_data = manager.list()
    final_data = manager.list()
    lock = manager.Lock()

    # 启动生产者
    producer_proc = Process(target=producer, args=(phone_queue, test_numbers))
    producer_proc.start()

    # 启动浏览器消费者 (根据CPU核心数和任务数确定进程数)
    worker_count = min(cpu_count(), len(test_numbers), 4)  # 限制最大4个浏览器进程
    browser_workers = []
    for i in range(worker_count):
        p = Process(target=browser_consumer, args=(i + 1, phone_queue, results, lock))
        p.start()
        browser_workers.append(p)
        time.sleep(2)  # 错开启动时间，避免同时请求代理

    # 启动请求消费者
    request_worker = Process(target=request_consumer, args=(results, lock, processed_data, final_data))
    request_worker.start()

    # 等待生产者完成
    producer_proc.join()

    # 等待浏览器消费者完成
    for p in browser_workers:
        p.join()

    # 等待请求消费者处理剩余数据
    print("等待请求消费者处理剩余数据...")
    while len(results) > 0:
        time.sleep(1)

    # 终止请求消费者
    request_worker.terminate()

    # 保存结果
    try:
        with open("test_res_demo4.json", "w", encoding="utf-8") as f:
            json.dump(list(results), f, ensure_ascii=False, indent=2)

        with open("processed_data.json", "w", encoding="utf-8") as f:
            json.dump(list(processed_data), f, ensure_ascii=False, indent=2)

        # 生成Excel结果
        phones = []
        status = []
        for item in final_data:
            phones.append(item['phone'])
            status.append(item['result'])

        df = pd.DataFrame({"phone": phones, "status": status})
        with pd.ExcelWriter("final_result.xlsx") as writer:
            df.to_excel(writer, sheet_name='钉钉-电话号码检测结果', index=False)

        print(f"\n🎉 All done! Processed {len(processed_data)} items")

    except Exception as e:
        print(f"保存结果失败: {str(e)}")


if __name__ == "__main__":
    main()
