#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能分析脚本
用于分析钉钉检测工具的运行日志，生成性能报告
"""

import re
import json
from datetime import datetime
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import pandas as pd

class PerformanceAnalyzer:
    def __init__(self):
        self.performance_data = defaultdict(list)
        self.retry_data = defaultdict(int)
        self.error_data = defaultdict(int)
        self.timing_data = defaultdict(list)
        self.phone_results = {}
        
    def parse_log_file(self, log_file_path):
        """解析日志文件"""
        print(f"正在解析日志文件: {log_file_path}")
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 解析时间戳
            timestamp_match = re.match(r'\[(\d{2}:\d{2}:\d{2}\.\d{3})\]', line)
            if not timestamp_match:
                continue
                
            timestamp = timestamp_match.group(1)
            
            # 解析性能监控数据
            perf_match = re.search(r'性能监控 - (.+): ([\d.]+)秒', line)
            if perf_match:
                operation = perf_match.group(1)
                duration = float(perf_match.group(2))
                self.performance_data[operation].append(duration)
                continue
            
            # 解析重试数据
            retry_match = re.search(r'重试 - (.+): 第(\d+)/(\d+)次重试，原因: (.+)', line)
            if retry_match:
                phone = retry_match.group(1)
                retry_count = int(retry_match.group(2))
                max_retries = int(retry_match.group(3))
                reason = retry_match.group(4)
                self.retry_data[f"{reason}_{phone}"] += 1
                continue
            
            # 解析错误数据
            error_match = re.search(r'(检测失败|检测异常|请求超时|代理错误|请求异常)', line)
            if error_match:
                error_type = error_match.group(1)
                self.error_data[error_type] += 1
                continue
            
            # 解析手机号结果
            result_match = re.search(r'检测完成: (.+) - (.+)', line)
            if result_match:
                phone = result_match.group(1)
                status = result_match.group(2)
                self.phone_results[phone] = status
                continue
    
    def generate_report(self):
        """生成性能报告"""
        print("\n" + "="*60)
        print("钉钉检测工具性能分析报告")
        print("="*60)
        
        # 1. 总体统计
        print("\n1. 总体统计")
        print("-" * 30)
        total_operations = sum(len(times) for times in self.performance_data.values())
        print(f"总操作次数: {total_operations}")
        print(f"检测的手机号数量: {len(self.phone_results)}")
        
        # 2. 性能分析
        print("\n2. 性能分析")
        print("-" * 30)
        
        performance_summary = []
        for operation, times in self.performance_data.items():
            if times:
                avg_time = sum(times) / len(times)
                total_time = sum(times)
                max_time = max(times)
                min_time = min(times)
                
                performance_summary.append({
                    'operation': operation,
                    'count': len(times),
                    'avg_time': avg_time,
                    'total_time': total_time,
                    'max_time': max_time,
                    'min_time': min_time
                })
        
        # 按平均耗时排序
        performance_summary.sort(key=lambda x: x['avg_time'], reverse=True)
        
        for item in performance_summary:
            print(f"操作: {item['operation']}")
            print(f"  执行次数: {item['count']}")
            print(f"  平均耗时: {item['avg_time']:.3f}秒")
            print(f"  总耗时: {item['total_time']:.3f}秒")
            print(f"  最大耗时: {item['max_time']:.3f}秒")
            print(f"  最小耗时: {item['min_time']:.3f}秒")
            
            # 性能建议
            if item['avg_time'] > 5.0:
                print(f"  ⚠️ 警告: 平均耗时过长，建议优化")
            elif item['avg_time'] > 2.0:
                print(f"  ⚡ 注意: 平均耗时较长，建议关注")
            print()
        
        # 3. 重试分析
        print("\n3. 重试分析")
        print("-" * 30)
        
        if self.retry_data:
            retry_summary = defaultdict(int)
            for key, count in self.retry_data.items():
                reason = key.split('_')[0]
                retry_summary[reason] += count
            
            for reason, count in sorted(retry_summary.items(), key=lambda x: x[1], reverse=True):
                print(f"重试原因: {reason}")
                print(f"  重试次数: {count}")
                if count > 10:
                    print(f"  ⚠️ 警告: 重试次数过多，建议检查网络或配置")
                print()
        else:
            print("无重试记录")
        
        # 4. 错误分析
        print("\n4. 错误分析")
        print("-" * 30)
        
        if self.error_data:
            total_errors = sum(self.error_data.values())
            for error_type, count in sorted(self.error_data.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_errors) * 100
                print(f"错误类型: {error_type}")
                print(f"  错误次数: {count} ({percentage:.1f}%)")
                if percentage > 50:
                    print(f"  ⚠️ 警告: 该错误占比过高，需要重点关注")
                print()
        else:
            print("无错误记录")
        
        # 5. 结果统计
        print("\n5. 检测结果统计")
        print("-" * 30)
        
        if self.phone_results:
            result_counter = Counter(self.phone_results.values())
            total_phones = len(self.phone_results)
            
            for status, count in result_counter.most_common():
                percentage = (count / total_phones) * 100
                print(f"状态: {status}")
                print(f"  数量: {count} ({percentage:.1f}%)")
            print()
        
        # 6. 优化建议
        print("\n6. 优化建议")
        print("-" * 30)
        
        # 分析最耗时的操作
        if performance_summary:
            slowest_operation = performance_summary[0]
            if slowest_operation['avg_time'] > 5.0:
                print(f"⚠️ 最耗时操作: {slowest_operation['operation']} (平均{slowest_operation['avg_time']:.3f}秒)")
                print("   建议: 考虑优化该操作的实现或增加并发")
        
        # 分析重试情况
        if self.retry_data:
            total_retries = sum(self.retry_data.values())
            if total_retries > 20:
                print(f"⚠️ 总重试次数过多: {total_retries}")
                print("   建议: 检查网络稳定性或调整重试策略")
        
        # 分析错误率
        if self.error_data and self.phone_results:
            total_errors = sum(self.error_data.values())
            total_phones = len(self.phone_results)
            error_rate = (total_errors / total_phones) * 100
            if error_rate > 20:
                print(f"⚠️ 错误率过高: {error_rate:.1f}%")
                print("   建议: 检查代理配置或网络连接")
        
        print("\n" + "="*60)
        print("分析完成")
        print("="*60)
    
    def save_report(self, output_file):
        """保存报告到文件"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'performance_data': dict(self.performance_data),
            'retry_data': dict(self.retry_data),
            'error_data': dict(self.error_data),
            'phone_results': self.phone_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"报告已保存到: {output_file}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python performance_analyzer.py <日志文件路径> [输出文件路径]")
        print("示例: python performance_analyzer.py log.txt report.json")
        return
    
    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "performance_report.json"
    
    analyzer = PerformanceAnalyzer()
    
    try:
        analyzer.parse_log_file(log_file)
        analyzer.generate_report()
        analyzer.save_report(output_file)
    except FileNotFoundError:
        print(f"错误: 找不到日志文件 {log_file}")
    except Exception as e:
        print(f"分析过程中出现错误: {e}")

if __name__ == "__main__":
    main() 