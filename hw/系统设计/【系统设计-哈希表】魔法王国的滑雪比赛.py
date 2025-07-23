from collections import defaultdict
from heapq import heappop, heappush
from typing import List

class SkiRankingSystem:
    def __init__(self):
        """
        初始化滑雪排名系统。
        使用 defaultdict(list) 存储每个用户的最好 3 次成绩。
        使用小顶堆 self.heap 存储所有添加的成绩记录，用于快速获取成绩最好的运动员。
        使用 self.stamp 来表示成绩的时间戳，用于处理成绩相同时的排序优先级。
        """
        self.stamp = 0  # 时间戳，用于区分同样成绩的先后顺序
        self.mp = defaultdict(list)  # 存储每个用户的前 3 次最好成绩
        self.heap = []  # 最小堆，用于获取最优成绩的运动员（按成绩+时间戳排序）

    def addRecord(self, userId: int, duration: int) -> None:
        """
        添加一条滑雪成绩记录。

        参数：
        - userId: 运动员的 ID
        - duration: 滑雪用时（成绩）

        操作：
        - 把新成绩加入用户成绩列表中，并只保留最好的 3 个成绩（升序排列）
        - 把本次成绩和时间戳加入全局最小堆中（供 getTopAthletes 使用）
        """
        # 更新用户成绩列表，插入新成绩后排序，保留前 3 个最小值
        self.mp[userId] = sorted(self.mp[userId] + [duration])[:3]
        # 将新成绩及时间戳压入堆中
        heappush(self.heap, [duration, self.stamp, userId])
        self.stamp += 1  # 时间戳自增

    def getTopAthletes(self, num: int) -> List[int]:
        """
        获取当前成绩最好的 num 个运动员的 ID。

        参数：
        - num: 需要查询的前 N 名运动员

        返回：
        - List[int]：运动员 ID 列表，按成绩升序排序
        """
        vis = set()  # 用于去重，确保每个运动员只出现一次
        res = []  # 存储当前选择的前 N 名成绩信息
        # 不断弹出堆顶元素，直到找到 num 个不同运动员
        while len(res) < num and self.heap:
            info = heappop(self.heap)
            if info[2] not in vis:
                vis.add(info[2])
                res.append(info)
        # 将提取出的元素重新压入堆中，保持堆不变
        for info in res:
            heappush(self.heap, info)
        # 返回按成绩排序的运动员 ID
        return [info[2] for info in res]

    def queryTop3Record(self, userId: int) -> List[int]:
        """
        查询某个运动员的前 3 次最好成绩。

        参数：
        - userId: 运动员 ID

        返回：
        - List[int]：升序排列的前 3 次成绩，若无成绩则返回 [-1]
        """
        v = self.mp[userId]
        if len(v) == 0:
            return [-1]  # 没有成绩记录
        return v  # 返回已排序的前 3 个最好成绩


# 主函数部分，模拟交互流程
system = None  # 系统对象
Q = int(input())  # 总操作数
for i in range(Q):
    cmd = input()  # 读取当前命令
    if i == 0 and cmd == "SkiRankingSystem":
        # 初始化命令：创建系统对象
        system = SkiRankingSystem()
        print("null")
    elif i > 0 and cmd == "addRecord":
        # 添加成绩命令：读取参数并添加成绩
        userId = int(input())
        duration = int(input())
        system.addRecord(userId, duration)
        print("null")
    elif i > 0 and cmd == "getTopAthletes":
        # 查询前 N 名运动员命令
        num = int(input())
        ans = system.getTopAthletes(num)
        print(*ans)  # 输出运动员 ID 列表
    elif i > 0 and cmd == "queryTop3Record":
        # 查询指定运动员的前 3 次最好成绩
        userId = int(input())
        ans = system.queryTop3Record(userId)
        print(*ans)  # 输出成绩列表
    else:
        assert False  # 防止非法输入
