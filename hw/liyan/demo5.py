#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多线程测试请求拦截功能（支持每20次请求更换代理）
"""

import threading
from queue import Queue
from playwright.sync_api import sync_playwright

# 代理池配置
PROXY_POOL = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
    "socks5://proxy4.example.com:1080"
]

# 共享数据结构
phone_numbers = Queue()
results = []
results_lock = threading.Lock()
proxy_lock = threading.Lock()  # 代理选择锁


class ProxyRotator:
    """代理轮换管理器"""

    def __init__(self, proxy_pool):
        self.proxy_pool = proxy_pool
        self.current_index = 0
        self.request_count = 0

    def get_proxy(self):
        """获取当前代理"""
        with proxy_lock:
            return self.proxy_pool[self.current_index]

    def mark_request(self):
        """记录请求并判断是否需要切换代理"""
        with proxy_lock:
            self.request_count += 1
            if self.request_count >= 20:
                self.request_count = 0
                self.current_index = (self.current_index + 1) % len(self.proxy_pool)
                print(f"\n代理切换至: {self.proxy_pool[self.current_index]}")
                return True
        return False


# 全局代理轮换器
proxy_rotator = ProxyRotator(PROXY_POOL)


def worker(worker_id):
    """工作线程函数"""
    print(f"Worker {worker_id} 启动")

    # 初始化浏览器实例（首次使用第一个代理）
    browser, context, page = init_browser(worker_id)

    while not phone_numbers.empty():
        try:
            phone = phone_numbers.get_nowait()

            # 执行请求前检查是否需要更换代理
            if proxy_rotator.mark_request():
                # 关闭旧浏览器实例
                browser.close()
                # 使用新代理创建浏览器实例
                browser, context, page = init_browser(worker_id)

            # 执行测试
            test_interception_for_phone(page, worker_id, phone)
            phone_numbers.task_done()

        except Exception as e:
            print(f"Worker {worker_id} 发生异常: {e}")
            break

    # 关闭浏览器
    browser.close()
    print(f"Worker {worker_id} 结束")


def init_browser(worker_id):
    """初始化带代理的浏览器实例"""
    current_proxy = proxy_rotator.get_proxy()
    print(f"Worker {worker_id} 使用代理: {current_proxy}")

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False,
        proxy={
            "server": current_proxy,
            # 如果需要认证可以添加以下内容
            # "username": "your_username",
            # "password": "your_password"
        }
    )
    context = browser.new_context()
    page = context.new_page()
    return browser, context, page


def test_interception_for_phone(page, worker_id, test_phone):
    """测试逻辑（保持原有实现）"""
    # 这里保持您原来的测试逻辑不变
    print(f"Worker {worker_id} 测试手机号: {test_phone}")
    # ... 原有测试代码 ...


def main():
    # 初始化测试手机号
    test_numbers = [f"1380013800{i}" for i in range(100)]  # 测试100个号码
    for num in test_numbers:
        phone_numbers.put(num)

    # 创建并启动工作线程
    threads = []
    num_workers = 3  # 线程数

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
        print(f"使用的代理: {result['proxy']}")
        print(f"URL: {result['url']}")
        print(f"POST数据(前200字符): {result['post_data'][:200]}...")


if __name__ == "__main__":
    main()