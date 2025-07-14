#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import threading
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# 模拟全局状态
global_state = {
    'results_cache': {},
    'processing_requests': set(),
    'completed_requests': 0,
    'failed_requests': 0
}
global_state_lock = threading.Lock()

def cache_result(phone_number, result):
    """缓存结果"""
    with global_state_lock:
        global_state['results_cache'][phone_number] = result

def update_global_state(key, value, operation='set'):
    """更新全局状态"""
    with global_state_lock:
        if operation == 'increment':
            global_state[key] = global_state.get(key, 0) + value
        else:
            global_state[key] = value

# 模拟检测函数
def mock_check_phone(phone_number, log_func=None):
    """模拟检测手机号"""
    if log_func:
        log_func(f"开始检测: {phone_number}")
    
    # 检查是否已经处理过
    results_cache = global_state.get('results_cache', {})
    if phone_number in results_cache:
        if log_func:
            log_func(f"跳过重复请求: {phone_number} - 已存在结果: {results_cache[phone_number].get('status', '未知')}")
        return results_cache[phone_number]
    
    # 检查是否正在处理中
    with global_state_lock:
        if phone_number in global_state.get('processing_requests', set()):
            if log_func:
                log_func(f"跳过正在处理中的请求: {phone_number}")
            return None
        else:
            if 'processing_requests' not in global_state:
                global_state['processing_requests'] = set()
            global_state['processing_requests'].add(phone_number)
    
    try:
        # 模拟检测时间
        time.sleep(random.uniform(1, 3))
        
        # 模拟不同的检测结果
        results = ["已注册", "未注册", "滑块验证", "请求频繁"]
        status = random.choice(results)
        
        result = {
            'phone': phone_number,
            'status': status,
            'response': {'mock': True}
        }
        
        # 缓存结果
        cache_result(phone_number, result)
        update_global_state('completed_requests', 1, 'increment')
        
        if log_func:
            log_func(f"检测完成: {phone_number} - {status}")
        
        return result
        
    finally:
        # 从处理中集合移除
        with global_state_lock:
            if 'processing_requests' in global_state:
                global_state['processing_requests'].discard(phone_number)

class MockWorker(QThread):
    result_signal = pyqtSignal(int, str)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, phone_list):
        super().__init__()
        self.phone_list = phone_list
        self.running = True
    
    def stop(self):
        self.running = False
    
    def run(self):
        try:
            self.log_signal.emit("开始模拟检测...")
            
            # 记录已发送到表格的结果，避免重复发送
            sent_results = set()
            
            def check_and_update_results():
                """检查缓存结果并更新表格"""
                results_cache = global_state.get('results_cache', {})
                for i, mobile in enumerate(self.phone_list):
                    if mobile in results_cache and (mobile, i) not in sent_results:
                        cached_result = results_cache[mobile]
                        status = cached_result.get('status', '未知')
                        self.result_signal.emit(i, status)
                        sent_results.add((mobile, i))
                        self.log_signal.emit(f"实时更新: {mobile} - {status}")
            
            # 模拟并发检测
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for i, mobile in enumerate(self.phone_list):
                    # 立即发送"检测中"状态到表格
                    self.result_signal.emit(i, '检测中')
                    self.log_signal.emit(f"开始检测: {mobile}")
                    
                    future = executor.submit(mock_check_phone, mobile, self.log_signal.emit)
                    futures.append((future, mobile, i))
                
                # 等待所有任务完成，同时定期检查结果
                for future, mobile, idx in futures:
                    try:
                        result = future.result()
                        
                        # 检查任务的结果
                        if result:
                            if result.get('status') == '检测失败':
                                # 任务失败，更新表格状态
                                self.result_signal.emit(idx, '检测失败')
                                sent_results.add((mobile, idx))
                                self.log_signal.emit(f"检测失败: {mobile}")
                            elif result.get('status') == '检测中':
                                # 请求已发送到异步线程，保持"检测中"状态
                                self.log_signal.emit(f"请求已发送到异步线程: {mobile}")
                            else:
                                # 其他状态，直接更新
                                status = result.get('status', '检测中')
                                self.result_signal.emit(idx, status)
                                sent_results.add((mobile, idx))
                                self.log_signal.emit(f"检测结果: {mobile} - {status}")
                        
                        # 检查是否有新的缓存结果
                        check_and_update_results()
                            
                    except Exception as e:
                        self.log_signal.emit(f"任务执行异常: {e}")
                        self.result_signal.emit(idx, '检测异常')
                        sent_results.add((mobile, idx))
            
            # 处理仍未完成的项目
            for i, mobile in enumerate(self.phone_list):
                if (mobile, i) not in sent_results:
                    # 如果还没有结果，说明检测失败
                    status = '检测失败'
                    self.result_signal.emit(i, status)
                    self.log_signal.emit(f"未找到结果: {mobile} - {status}")
            
            # 显示最终统计
            completed = global_state.get('completed_requests', 0)
            failed = global_state.get('failed_requests', 0)
            self.log_signal.emit(f"检测完成 - 成功: {completed}, 失败: {failed}")
            self.log_signal.emit("所有检测完成！")
            self.finished_signal.emit()
            
        except Exception as e:
            self.log_signal.emit(f"工作线程异常: {e}")
            self.finished_signal.emit()

class TestTableUpdate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("表格更新测试")
        self.setGeometry(200, 100, 800, 600)
        self.phone_numbers = []
        self.worker = None
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 配置区
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("测试手机号:"))
        self.phone_input = QLineEdit("13800138000,13800138001,13800138002,13800138003,13800138004")
        config_layout.addWidget(self.phone_input)
        
        btn_start = QPushButton("开始测试")
        btn_start.clicked.connect(self.start_test)
        config_layout.addWidget(btn_start)
        layout.addLayout(config_layout)

        # 手机号表格
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["序号", "手机号", "状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # 日志区
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        layout.addWidget(self.log_text)

    def start_test(self):
        try:
            if self.worker and self.worker.isRunning():
                QMessageBox.warning(self, "警告", "有任务正在执行，请等待完成！")
                return
            
            # 解析手机号
            phone_text = self.phone_input.text().strip()
            if not phone_text:
                QMessageBox.warning(self, "警告", "请输入测试手机号！")
                return
            
            self.phone_numbers = [phone.strip() for phone in phone_text.split(',') if phone.strip()]
            if not self.phone_numbers:
                QMessageBox.warning(self, "警告", "没有有效的手机号！")
                return
            
            # 重置全局状态
            global global_state
            global_state = {
                'results_cache': {},
                'processing_requests': set(),
                'completed_requests': 0,
                'failed_requests': 0
            }
            
            # 初始化表格
            self.table.setRowCount(0)
            for i, phone in enumerate(self.phone_numbers, 1):
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(i)))
                self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(phone))
                self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(""))
            
            self.log_text.append("开始测试表格更新功能...")
            
            # 启动工作线程
            self.worker = MockWorker(self.phone_numbers)
            self.worker.result_signal.connect(self.update_status)
            self.worker.finished_signal.connect(self.check_finished)
            self.worker.log_signal.connect(self.log_text.append)
            self.worker.start()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动测试失败: {str(e)}")
            self.log_text.append(f"启动测试异常: {e}")

    def update_status(self, idx, status):
        try:
            # 确保在主线程中更新UI
            if hasattr(self, 'table') and idx < self.table.rowCount():
                try:
                    self.table.setItem(idx, 2, QTableWidgetItem(status))
                    self.log_text.append(f"表格更新: 第{idx+1}行 - {status}")
                except Exception as e:
                    self.log_text.append(f"UI更新异常: {e}")
        except Exception as e:
            self.log_text.append(f"update_status异常: {e}")

    def check_finished(self):
        self.log_text.append("测试完成！")
        QMessageBox.information(self, "完成", "表格更新测试完成！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestTableUpdate()
    win.show()
    sys.exit(app.exec_()) 