'''
题目描述
在魔法大陆 阿瓦隆，流传着一份古老的 占星秘术。据说，秘术需要通过一串神秘数字计算出“星辰之力”才能解开命运的奥秘。
大魔导师 奥卫 受困于一场混沌风暴，他唯一的希望就是通过秘术计算“星辰之力”的总和，以此施放大封印术来平息风暴。你作为他的 占星助手，需要帮助他完成这一计算。
秘术的核心在于 子列表的中位数之和。具体而言，给定一个长度为 n 的整数序列，要求计算它的所有 连续子列表 的 中位数 之和。
中位数的定义：
- 如果子列表长度为奇数，则中位数是排序后的中间元素。
- 如果子列表长度为偶数，则取排序后靠左的那个中间元素（即 floor((k+1)/2) 位置的元素，基于 1 索引）。
输入格式
输入包含两部分：
- 第一行包含一个整数 n (1 <= n <= 100)，表示数列的长度。
- 第二行包含 n 个整数 a_1, a_2, ..., a_n (-10^3 <= a_i <= 10^3)，表示魔法数列。
输出格式
输出一个整数，表示所有 连续子列表的中位数之和。
样例
样例1
样例输入：
4
1 7 5 4
样例输出：
41
样例说明：
长度为 1 的子列表：[1], [7], [5], [4] -> 中位数之和 = 1 + 7 + 5 + 4 = 17
长度为 2 的子列表：[1,7], [7,5], [5,4] -> 排序后中位数分别为 1, 5, 4 -> 1 + 5 + 4 = 10
长度为 3 的子列表：[1,7,5], [7,5,4] -> 排序后中位数分别为 5, 5 -> 5 + 5 = 10
长度为 4 的子列表：[1,7,5,4] -> 排序后中位数为 4
最终和 = 17 + 10 + 10 + 4 = 41
样例2
样例输入：
4
1 2 3 10
样例输出：
29


'''

from heapq import heappush, heappop


# 用于动态维护中位数的数据结构
class MedianFinder:
    def __init__(self):
        # 最大堆，用于存储较小的一半数据（取负数实现最大堆）
        self.que_min = []
        # 最小堆，用于存储较大的一半数据
        self.que_max = []

    def addNum(self, num: int) -> None:
        # 如果最大堆为空或当前数字小于最大堆堆顶（即较小一半的最大值），加入最大堆
        if not self.que_min or num <= -self.que_min[0]:
            heappush(self.que_min, -num)
            # 如果最大堆的大小比最小堆多超过1，平衡一下
            if len(self.que_max) + 1 < len(self.que_min):
                heappush(self.que_max, -heappop(self.que_min))
        else:
            # 否则加入最小堆
            heappush(self.que_max, num)
            # 如果最小堆的数量多于最大堆，移动堆顶元素到最大堆保持平衡
            if len(self.que_max) > len(self.que_min):
                heappush(self.que_min, -heappop(self.que_max))

    def findMedian(self) -> int:
        # 返回当前数据流的中位数（根据题目规则：偶数个数时返回靠左的中间值）
        return -self.que_min[0]  # 最大堆堆顶元素即为中位数


class Solution:
    def sum_of_medians(self, nums):
        n = len(nums)  # 数列长度
        total_sum = 0  # 用于记录所有子列表中位数的总和

        # 枚举每个子列表的起点
        for i in range(n):
            median_finder = MedianFinder()  # 每次新建一个 MedianFinder 对象

            # 枚举终点，生成从 i 到 j 的连续子列表
            for j in range(i, n):
                median_finder.addNum(nums[j])  # 向中位数维护结构中添加元素
                total_sum += median_finder.findMedian()  # 累加当前子列表的中位数

        return total_sum  # 返回所有子列表中位数的和


# 读取输入部分
n = int(input())  # 读取数列长度
nums = list(map(int, input().split()))  # 读取数列

# 输出所有子列表的中位数之和
print(Solution().sum_of_medians(nums))
