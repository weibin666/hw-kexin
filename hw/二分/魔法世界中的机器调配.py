'''
在一个充满魔法和神秘力量的世界里，数百种任务需要在固定的时间段内完成。每个任务都有一个明确的开始时间、结束时间（左开右闭），以及它所需要完成的工作量。为了完成这些任务，您将召唤出各种强大的机器（类似魔法机器人的存在），它们拥有单位时间内完成工作量的能力。
您的目标是通过合理调配这些魔法机器，在给定的时间内高效地完成所有任务。每个任务可能会在不同的时间段内与其他任务重叠，因此我们需要计算最少需要多少台机器才能按时完成这些任务。
输入格式
- 第一行：整数 n，表示任务的数量。
- 接下来的 n 行，每行包含三个整数 starttime、endtime 和 tasknum，分别表示一个任务的开始时间、结束时间和所需完成的工作量。
- 第 n+2 行：整数 ability，表示每台机器每单位时间内能够完成的工作量。
- 1 <= n, tasknum <= 10^4
- 1 <= starttime < endtime <= 10^5

case1:
3
1 4 10
2 5 5
3 6 15
5
输出：
2
'''
from heapq import heappush, heappop

class Solution:
    def solve(self, tasks: list, ability: int):
        # `ok`函数判断是否能够用`cnt`台机器完成所有任务
        def ok(cnt):
            size = cnt * ability  # 每台机器的处理能力是 `ability`，`cnt`台机器总能力为 `cnt * ability`
            p = 0  # 指示任务数组的位置
            now = 0  # 当前时间
            q = []  # 优先队列，用来处理任务的时间和剩余工作量
            while p < len(tasks) or len(q) > 0:
                # 添加所有在当前时间点开始的任务到队列
                while p < len(tasks) and now >= tasks[p][0]:
                    heappush(q, [tasks[p][1], tasks[p][2]])  # [结束时间, 工作量]
                    p += 1
                rest = size  # 当前机器的处理能力
                # 处理当前时间点的任务
                while len(q) > 0 and rest > 0:
                    # 如果最早结束的任务已经结束，返回 False
                    if q[0][0] <= now:
                        return False
                    tm, sz = heappop(q)
                    x = min(rest, sz)  # 在剩余的处理能力内，分配给当前任务的工作量
                    rest -= x  # 更新剩余的处理能力
                    sz -= x  # 更新任务剩余工作量
                    if sz > 0:
                        heappush(q, [tm, sz])  # 如果任务还有剩余，继续放回队列
                now += 1  # 增加时间
            return True  # 所有任务能够在给定机器数下完成

        tasks.sort()  # 先按照任务的开始时间进行排序

        l = 1  # 最小机器数量
        r = sum(t[2] for t in tasks)  # 最大机器数量，任务总工作量
        while l < r:
            mid = (l + r) // 2
            if ok(mid):  # 判断mid台机器能否完成所有任务
                r = mid  # 可以完成任务，缩小右边界
            else:
                l = mid + 1  # 不能完成任务，增加机器数量

        return l  # 最小机器数量

# 使用例子
sol = Solution()
n = int(input())  # 任务数量
tasks = [list(map(int, input().split())) for _ in range(n)]  # 任务数据
ability = int(input())  # 每台机器的能力
print(sol.solve(tasks, ability))  # 输出最少机器数量
