import sys
import os
import traceback
import threading
import queue
import random
import requests
import json
import time
import urllib.parse
from typing import List, Optional, Callable
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import re
import multiprocessing
from datetime import datetime
import pickle

# Redis缓存支持（可选）
try:
    import redis
    REDIS_AVAILABLE = True
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("Redis连接成功，将使用Redis缓存")
except ImportError:
    REDIS_AVAILABLE = False
    print("Redis模块未安装，将使用内存缓存")
except Exception as e:
    REDIS_AVAILABLE = False
    print(f"Redis连接失败: {e}，将使用内存缓存")

# 全局进程池 - 专门处理重发请求
request_process_pool = None
request_process_pool_lock = threading.Lock()

# 全局状态管理
global_state = {
    'active_requests': 0,
    'completed_requests': 0,
    'failed_requests': 0,
    'proxy_usage': {},
    'proxy_assignments': {},
    'request_queue': queue.Queue(),
    'results_cache': {},
    'browser_initialized': False,
    'initialization_lock': threading.Lock(),
    'browser_setup_completed': False,
    'browser_setup_lock': threading.Lock()
}
global_state_lock = threading.Lock()

# 进程间通信的结果队列
result_queue = multiprocessing.Queue()

def get_request_process_pool():
    """获取全局请求进程池"""
    global request_process_pool
    with request_process_pool_lock:
        if request_process_pool is None:
            max_workers = min(multiprocessing.cpu_count() * 2, 100)
            request_process_pool = ProcessPoolExecutor(max_workers=max_workers)
        return request_process_pool

def shutdown_request_process_pool():
    """关闭全局请求进程池"""
    global request_process_pool
    with request_process_pool_lock:
        if request_process_pool:
            request_process_pool.shutdown(wait=True)
            request_process_pool = None

def update_global_state(key, value, operation='set'):
    """更新全局状态"""
    with global_state_lock:
        if operation == 'increment':
            global_state[key] = global_state.get(key, 0) + value
        elif operation == 'dict_increment':
            if key not in global_state:
                global_state[key] = {}
            if value not in global_state[key]:
                global_state[key][value] = 0
            global_state[key][value] += 1
        else:
            global_state[key] = value

def get_global_state(key, default=None):
    """获取全局状态"""
    with global_state_lock:
        return global_state.get(key, default)

def cache_result(phone_number, result):
    """缓存结果"""
    with global_state_lock:
        global_state['results_cache'][phone_number] = result
    
    # 同时缓存到Redis
    if REDIS_AVAILABLE:
        try:
            key = f"dingtalk_check:{phone_number}"
            redis_client.setex(key, 3600, json.dumps(result))
        except Exception as e:
            print(f"Redis缓存失败: {e}")

def get_cached_result_from_redis(phone_number):
    """从Redis获取缓存结果"""
    if REDIS_AVAILABLE:
        try:
            key = f"dingtalk_check:{phone_number}"
            cached_data = redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis获取缓存失败: {e}")
    return None

# 性能监控工具
class PerformanceMonitor:
    def __init__(self):
        self.start_times = {}
        self.total_times = {}
        self.counts = {}
        self.lock = threading.Lock()
    
    def start_timer(self, name):
        with self.lock:
            self.start_times[name] = time.time()
    
    def end_timer(self, name):
        with self.lock:
            if name in self.start_times:
                elapsed = time.time() - self.start_times[name]
                if name not in self.total_times:
                    self.total_times[name] = 0
                    self.counts[name] = 0
                self.total_times[name] += elapsed
                self.counts[name] += 1
                del self.start_times[name]
                return elapsed
        return 0

# 全局性能监控器
perf_monitor = PerformanceMonitor()

def log_with_time(message, log_func=None):
    """带时间戳的日志"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    full_message = f"[{timestamp}] {message}"
    if log_func:
        log_func(full_message)
    else:
        print(full_message)

# 清除所有系统代理设置
requests.utils.default_proxies = {}
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("https_proxy", None)
os.environ.pop("NO_PROXY", None)
os.environ.pop("no_proxy", None) 