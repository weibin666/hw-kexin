'''
题目描述
在魔法大陆「车灵界」中，魔法骑士们骑着各种具有魔力铭文的飞车在大陆间穿梭。在每个魔法年内，所有的停车记录都会被记录在魔法档案中，用以评估每位骑士的活跃度和停留轨迹。魔法议会为了选出“停留之星”，发起了一场关于特定月份内停留行为的评选试炼。
每条魔法停车记录由以下三部分组成：
- 车牌号（由魔法铭文唯一标识，例如 YB0001）
- 停车日期（格式为 yyyy-mm-dd）
- 停留时间（单位为分钟）
议会希望你统计指定月份内，哪位骑士在魔法停车塔停留时间最长。若存在多位骑士的总停留时间相同，则比较他们的停留次数，次数多者为先；若仍相同，则按车牌字典序升序排序。
输入格式
第一行包含一个整数 n（1 <= n <= 10^4），表示接下来的 n 行是魔法停车记录。
接下来 n 行，每行包含一条记录，格式如下：
<车牌号> <日期> <停留时间>
- 车牌号 为仅包含大写字母与数字的字符串，长度不超过 10。
- 日期 为 yyyy-mm-dd 格式的合法日期。
- 停留时间 为正整数，不超过 10^4。
最后一行输入一个整数 m（1 <= m <= 12），表示需要统计的魔法月份。
输出格式
输出一个字符串，表示在指定月份内停留时间最长的骑士的车牌号。
如果没有任何记录属于该月份，则输出NULL。
样例
样例1
样例输入：
5
YB0001 2019-01-03 50
YB0002 2019-01-05 200
YB0001 2019-01-04 100
YB0001 2019-02-04 100
AB0001 2019-02-05 300
1

样例输出：
YB0002

样例说明：
YB0001 停留时间50+100，停留2次
YB0002 停留时间200，停留1次
输出YB0002
样例2
样例输入：
7
YB0002 2019-01-03 100
YB0001 2019-01-05 50
YB0001 2019-01-05 50
YB0001 2019-01-05 50
YB0002 2019-01-04 100
AB0002 2019-01-04 50
AB0002 2019-01-05 150
1
样例输出：
AB0002

样例说明：
在指定的 1 月份中：
- AB0002 停留总时间 200，次数 2
- YB0002 停留总时间 200，次数 2
- YB0001 停留总时间 150，次数 3
由于 AB0002 与 YB0002 停留时间相同，次数也相同，但 AB0002 的车牌字典序靠前，因此被选为“停留之星”。
'''
from typing import List
from collections import defaultdict

class Solution:
    def findTopVehicle(self, records: List[str], month: int) -> str:
        # 创建默认字典，值为 [总停留时间, 停留次数]
        '''
        defaultdict(lambda: [0, 0]) 定义方法学着点
        '''
        stats = defaultdict(lambda: [0, 0])

        # 用于记录当前最优的车牌号和对应的 [总时间, 次数]
        best_plate = None
        best_time = -1
        best_count = -1

        for record in records:
            parts = record.strip().split()
            if len(parts) != 3:
                continue  # 跳过格式非法记录

            plate, date, duration_str = parts
            try:
                cur_month = int(date.split('-')[1])  # 提取月份
                if cur_month != month:
                    continue  # 非目标月份，跳过

                duration = int(duration_str)
                stats[plate][0] += duration     # 累加停留时间
                stats[plate][1] += 1            # 累加停留次数

                total_time, count = stats[plate]

                # 判断当前记录是否为更优的车牌：
                # 优先级：时间 > 次数 > 车牌号字典序
                if (total_time > best_time or
                    (total_time == best_time and count > best_count) or
                    (total_time == best_time and count == best_count and (best_plate is None or plate < best_plate))):
                    best_plate = plate
                    best_time = total_time
                    best_count = count

            except:
                continue  # 忽略无法转换或非法格式

        # 若未找到符合条件的记录，则输出 NULL
        return best_plate if best_plate is not None else "NULL"

def sovle_v2():
    from collections import defaultdict

    n = int(input())
    records = []
    for _ in range(n):
        parts = input().split()
        plate = parts[0]
        date = parts[1]
        duration = int(parts[2])
        records.append((plate, date, duration))

    m = int(input())

    # 筛选目标月份的记录
    target_records = []
    for record in records:
        date_parts = record[1].split('-')
        month = int(date_parts[1])
        if month == m:
            target_records.append(record)

    if not target_records:
        print("NULL")
    else:
        # 统计每个车牌的总停留时间和次数
        stats = defaultdict(lambda: {'total_duration': 0, 'count': 0})
        for plate, date, duration in target_records:
            stats[plate]['total_duration'] += duration
            stats[plate]['count'] += 1

        # 转换为列表并排序
        '''
        这个写法牛逼呀！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        sorted_stats = sorted(stats.items(), key=lambda x: (-x[1]['total_duration'], -x[1]['count'], x[0]))
        '''
        print(stats)
        sorted_stats = sorted(stats.items(), key=lambda x: (-x[1]['total_duration'], -x[1]['count'], x[0]))
        print(sorted_stats)
        print(sorted_stats[0][0])

if __name__ == "__main__":
    # n = int(input())  # 读取记录条数
    # records = [input().strip() for _ in range(n)]  # 读取所有记录
    # month = int(input().strip())  # 读取目标月份
    #
    # solution = Solution()
    # result = solution.findTopVehicle(records, month)
    # print(result)
    sovle_v2()
