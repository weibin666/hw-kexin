'''
题目描述
在魔法王国的中心矗立着一座巨大的流量水晶，负责记录经过的魔法流流量。水晶每秒记录一次流量数据，并将其存储在数组 magicFlows 中。然而，当某些时间窗口内的魔法流量总和超过设定阈值时，流量水晶将会发生 魔法超载事件。
魔法超载事件 定义如下：
在一个连续的时间窗口（窗口长度范围为 [minWindow, maxWindow]），如果该窗口内的魔法流量之和大于设定的阈值 magicThreshold，则视为一次 魔法超载事件。
注意：
1. 两个时间窗口只要起点或终点不同，就视为不同的时间窗口。
2. 确保魔法超载事件总次数不超过 100,000 次。
求发生魔法超载事件的次数。
输入格式
第一行输入一个整数 n，表示数组 magicFlows 的长度，满足 1 <= n <= 100,000。
第二行输入 n 个整数，表示数组 magicFlows，其中 0 <= magicFlows[i] <= 10,000。
第三行、第四行分别输入两个整数，分别表示时间窗口的最小长度 minWindow 和最大长度 maxWindow，满足 1 <= minWindow <= maxWindow <= n。
第五行输入一个整数 magicThreshold，表示魔法超载的阈值，满足 1 <= magicThreshold <= 10^9。
输出格式
输出一个整数，表示发生魔法超载事件的次数。
样例
样例1
样例输入：
5
5 2 3 6 4
2
3
10
样例输出：
2
样例说明：
总计 2 次魔法超载事件：[2, 3, 6], [3, 6, 4]
样例2
样例输入：
5
1 1 1 1 1
1
5
10
样例输出：
0
样例3
样例输入：
10
10 9 8 7 6 5 4 3 2 1
2
5
15
样例输出：
16
'''
from typing import List


class Solution:
    def get_event_count(self, magic_flows: List[int], min_windows: int, max_windows: int, magic_threshold: int) -> int:
        """
        计算魔法超载事件的次数。

        参数:
        - magic_flows (List[int]): 魔法流量数组，每秒记录一次流量。
        - min_windows (int): 时间窗口的最小长度。
        - max_windows (int): 时间窗口的最大长度。
        - magic_threshold (int): 魔法超载的流量阈值。

        返回:
        - int: 发生魔法超载事件的次数。
        """
        traffics_size = len(magic_flows)

        # 计算前缀和数组，用于快速求任意窗口的总和
        prefix_sum = [0] * (traffics_size + 1)
        for r in range(traffics_size):
            prefix_sum[r + 1] = prefix_sum[r] + magic_flows[r]
            # prefix_sum[i] 表示数组 magic_flows 前 i 个元素的累积和

        ans = 0  # 用于记录魔法超载事件的次数
        l = 0  # 滑动窗口的左边界

        # 遍历滑动窗口的右边界
        for r in range(1, traffics_size + 1):
            # 动态调整窗口左边界，确保窗口和不超过阈值
            while prefix_sum[r] - prefix_sum[l] > magic_threshold:
                l += 1

            # 确保窗口长度在 min_windows 和 max_windows 范围内
            if l > 0:
                l -= 1  # 回退一步，尝试扩大窗口范围
                pl = max(min(l, r - min_windows), 0)  # 有效左边界
                pr = max(0, r - max_windows)  # 窗口不能超过 max_windows
                ans += pl - pr + 1  # 累计符合条件的窗口数量

        return ans


if __name__ == '__main__':
    sol = Solution()
    # 输入数组长度
    n = int(input())

    # 输入魔法流量数组
    magic_flows = list(map(int, input().split()))

    # 输入窗口的最小长度
    min_windows = int(input())

    # 输入窗口的最大长度
    max_windows = int(input())

    # 输入魔法超载阈值
    magic_threshold = int(input())

    # 计算并输出魔法超载事件的次数
    print(sol.get_event_count(magic_flows, min_windows, max_windows, magic_threshold))

