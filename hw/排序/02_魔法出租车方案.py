'''
题目描述
在魔法公司的一次团建出游中，公司有多个部门，每个部门的人数各不相同。为了满足团建活动的需求，公司联系了多个魔法出租车公司，每个出租车公司提供了不同的车型，车型的载客量不尽相同，每种车都有无数辆。
每个部门的人数必须被安排到同一辆车上，并且每辆车只能搭载一个部门的人。现在，我们需要根据每个出租车公司的方案，选择一个使得所有的出租车尽量空座最少的方案（从0开始）。如果有多个方案具有相同的空座数，选择序号最小的公司。如果没有公司能满足需求，返回 -1。
输入格式
- 第一行输入一个整数 n，表示公司的部门数量。
- 第二行输入一个长度为 n 的数组 depts，其中每个元素表示一个部门的人数。
- 接下来输入 k（租车公司数量），然后对于每个租车公司：
  - 第一行输入该公司提供的车型数量 m。
  - 第二行输入该公司提供的所有车型的载客量（一个整数列表）。
- 1 <= m, k <= 300
- 1 <= n <= 5000
- 1 <= depts[i] <= 10^5
输出格式
- 输出一个整数，表示能使空座位最少的租车公司序号。如果没有公司能满足需求，输出 -1。
样例
样例1
样例输入：
3
10 8 15
2
3
8 15 12
4
20 4 15 4
样例输出：
0
样例2
样例输入：
2
5 9
3
1
4
2
6 10
2
5 11
样例输出：
1
样例3
样例输入：
2
10 10
2
4
2 9 8 3
1
7
样例输出：
-1
'''
class Solution:
    def minSeatCompany(self, depts, plans):
        # 外部排序一次，避免多次排序开销
        depts.sort()
        def calculate_empty_seats(plan):
            total_empty = 0
            plan.sort()  # 对车型进行排序（每个公司都不同，必须排序）
            print("plan", plan)

            plan_idx = 0
            m = len(plan)

            for dept in depts:
                # 跳过不能满足该部门人数的车型
                while plan_idx < m and plan[plan_idx] < dept:
                    plan_idx += 1
                if plan_idx == m:
                    return -1  # 没有车型可以承载当前部门
                total_empty += plan[plan_idx] - dept  # 空座 = 当前车型 - 部门人数

            return total_empty

        min_empty = float('inf')
        best_idx = -1

        for i, plan in enumerate(plans):
            empty = calculate_empty_seats(plan)
            if empty != -1 and empty < min_empty:
                min_empty = empty
                best_idx = i

        return best_idx

# 暴力解法
# class Solution2:
#     def minSeatCompany(self, depts, plans):
#         min_empty = float('inf')  # 初始化最小空座数为无穷大
#         best_idx = -1  # 初始化最优公司编号为-1（表示没有找到）

#         for idx, plan in enumerate(plans):  # 遍历每个租车公司
#             total_empty = 0  # 记录当前公司的总空座数
#             for dept in depts:  # 遍历每个部门
#                 min_seat = float('inf')  # 初始化当前部门的最小空座数为无穷大
#                 for seat in plan:  # 遍历当前公司的每种车型
#                     if seat >= dept:  # 如果车型能容纳该部门
#                         min_seat = min(min_seat, seat - dept)  # 更新最小空座数
#                 if min_seat == float('inf'):  # 如果没有车型能容纳该部门
#                     total_empty = -1  # 标记为不可行
#                     break  # 退出部门循环
#                 total_empty += min_seat  # 累加空座数
#             if total_empty != -1 and total_empty < min_empty:  # 如果当前公司可行且空座更少
#                 min_empty = total_empty  # 更新最小空座数
#                 best_idx = idx  # 更新最优公司编号
#         return best_idx  # 返回最优公司编号


if __name__ == "__main__":
    # 输入公司部门数和部门人数
    n = int(input())
    depts = list(map(int, input().split()))

    # 输入租车公司数
    k = int(input())
    plans = []

    # 输入每个租车公司提供的车型
    for _ in range(k):
        m = int(input())  # 车型数量
        plan = list(map(int, input().split()))  # 车型载客量
        plans.append(plan)
    print("plans", plans)
    print("depts", depts)
    # 创建解题对象并调用方法
    solution = Solution()
    result = solution.minSeatCompany(depts, plans)

    print(result)

