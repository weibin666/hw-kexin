'''
题目描述
在魔法大陆上，魔导服务器维持着整个王国的魔法网络。然而，由于魔力流动的波动，不同服务器之间的魔法延迟（latency）可能会影响王国的信息传输。
为了优化魔法网络，魔法工程师们需要选择一台服务器作为主服务器，使得整个集群的魔法延迟之和最小。
每台服务器的位置由一个唯一的魔法机位编号表示。服务器之间的魔法延迟可以简单地用它们机位编号之差的绝对值来计算，而服务器到自身的延迟为0。
请帮助魔法工程师们找到最佳的主服务器，并计算出最小的集群网络延迟。
输入格式
第一行包含一个整数 n，表示服务器的数量，满足 1 <= n <= 500。
第二行包含 n 个整数，表示服务器的机位编号，每个数值范围在 1 <= x <= 10000，相邻数值以空格分隔。
输出格式
输出一个整数，表示最小的集群网络延迟。
样例
样例1
样例输入：
3
2 6 4
样例输出：
4
样例说明：
服务器的机位编号为 [2, 6, 4]，如果选择编号为 4 的服务器作为主服务器，则计算的总延迟为：
|2-4| + |4-6| = 2 + 2 = 4
这是所有可能方案中最小的延迟。
样例2
样例输入：
4
2 4 3 1
样例输出：
4
样例说明：
服务器的机位编号为 [2, 4, 3, 1]，可以选择机位 2 或 3 作为主服务器，计算延迟如下：
选择 2: |2-2| + |4-2| + |3-2| + |1-2| = 0 + 2 + 1 + 1 = 4
选择 3: |2-3| + |4-3| + |3-3| + |1-3| = 1 + 1 + 0 + 2 = 4
两种方案的总延迟都是 4，为最小值。
题目解析
理解题目
本题描述了一个有关“服务器主机选择优化”的问题。魔法王国中有若干台魔导服务器，每台服务器都具有一个唯一的编号，可以看作是一维坐标轴上的点。我们需要从这些服务器中选择一个主服务器，使得所有其他服务器到主服务器之间的延迟总和最小。
根据题意，服务器之间的延迟定义为两者编号差的绝对值，即：
latency(a, b) = |a - b|
因此，问题本质上可以转化为：在一个整数数组中，选定一个数作为中心，使所有数到它的绝对差之和最小。
这实际上是一个经典的中位数优化问题。
使用算法
本题使用的是前缀和优化的贪心算法，在排序后的数组上对每个位置尝试作为主服务器，并计算总延迟，同时维护当前最小值。虽然最终选择的是中位数对应的位置，但该算法在实现上通过前缀和公式进行了高效的遍历与数学优化。
关键思想：
- 在排序后的数组中，某个位置的服务器作为主服务器时，延迟由两部分组成：
  - 左边所有服务器的延迟；
  - 右边所有服务器的延迟。
- 使用前缀和来快速计算这两部分延迟总和，避免暴力枚举带来的重复计算。
具体延迟计算公式为：
总延迟 = x * i - sl + (s - sl) - x * (n - i)
其中：
- x 为当前服务器编号；
- i 为当前位置（从 1 开始）；
- sl 表示前 i 个服务器编号的前缀和；
- s 表示所有服务器编号的总和；
- n 为服务器总数。
实现
解决本题可分为以下几个步骤：
1. 排序服务器编号数组。由于延迟与编号位置有关，将数组升序排列，可以使得左边与右边的贡献具有单调性，从而便于使用前缀和处理。
2. 预处理总和。提前计算出所有编号的总和 s，后续可用于快速计算右半部分的延迟。
3. 遍历每一个服务器编号，尝试以它作为主服务器：
  - 用变量 sl 记录当前前缀和；
  - 对每一个位置 i，基于上面提到的公式，计算以 arr[i] 为主服务器时的总延迟；
  - 维护当前的最小延迟值。
4. 输出最小延迟值。最终得到的即是最佳主服务器对应的最小网络延迟。

'''
class Solution:
    def cluster_latency(self, arr):
        # 首先对服务器机位编号排序，从小到大排列
        arr.sort()
        n = len(arr)         # 服务器数量
        s = sum(arr)         # 所有服务器编号的总和
        sl = 0               # 前缀和初始化（用于计算当前位置左侧编号之和）
        ans = float('inf')   # 初始化最小总延迟为无穷大，便于后续取最小值

        # 枚举每一个位置的服务器编号 x，尝试将它作为主服务器
        for i, x in enumerate(arr, 1):  # 注意 enumerate 从 1 开始
            sl += x  # 更新前缀和：当前编号之前（含当前）的编号之和

            # 当前 x 作为主服务器，总延迟计算公式如下：
            # 左侧部分（包括当前）：x * i - sl
            #   表示左侧所有点到 x 的距离之和，即 ∑(x - arr[j]) for j in 0..i-1
            # 右侧部分： (s - sl) - x * (n - i)
            #   表示右侧所有点到 x 的距离之和，即 ∑(arr[j] - x) for j in i..n-1
            # 总和就是左侧距离之和 + 右侧距离之和
            total_delay = x * i - sl + (s - sl) - x * (n - i)

            # 更新最小值
            ans = min(ans, total_delay)

        return ans


# 读取输入
num = input().strip()                      # 第一行：服务器数量，虽然未用，但为了格式统一仍保留
arr = list(map(int, input().split()))     # 第二行：服务器的机位编号数组
print(Solution().cluster_latency(arr))    # 输出最小的集群延迟

