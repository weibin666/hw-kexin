'''
题目描述
在魔法王国的数据塔中，有一段由 二进制魔法流 组成的字符串，每个字符要么是 0，要么是 1。你的目标是通过一个 反转操作 让某种 目标魔法值 target (0 或 1) 在魔法流中形成尽可能长的连续区域。
反转操作 定义为：将魔法流中的一个 0 改为 1 或将一个 1 改为 0。
请你计算在最多执行一次反转操作后，目标值的最大连续长度。
输入格式
输入共两行：
1. 第一行输入一个整数 target，表示目标魔法值，取值为 0 或 1。
2. 第二行输入一个长度为 length 的二进制字符串 bits，每个字符为 0 或 1，满足 1≤length≤10,000。
输出格式
输出一个整数，表示通过最多一次反转操作后，目标值的最大连续长度。
样例
样例1
样例输入：
1
1011010111
样例输出：
5
样例说明：
- 将第 7 位的 0 反转为 1，使得字符串变为 1011011111。
- 目标值 1 的最长连续区域为 11111，长度为 5。
样例2
样例输入：
0
10101
样例输出：
3
样例说明：
- 将第 3 位的 1 反转为 0，使得字符串变为 10001。
- 目标值 0 的最长连续区域为 000，长度为 3。
'''
from typing import List

class Solution:
    def max_continuous_length(self, target: str, bits: str) -> int:
        n = len(bits)        # 获取字符串的长度
        left = 0             # 初始化左指针，表示窗口的左边界
        max_len = 0          # 用于记录最大连续目标值长度
        flip_used = 0        # 用于记录当前窗口内是否已经使用了一次反转（最多只能反转一次）

        # 使用滑动窗口遍历字符串，每次尝试扩展右边界
        for right in range(n):
            # 如果当前字符不是目标字符 target，表示我们要使用一次反转
            if bits[right] != target:
                flip_used += 1

            # 如果反转次数超过1次，不合法，需要移动左边界
            while flip_used > 1:
                # 如果左边界是一个非目标字符，我们移出它相当于“收回”一次反转
                if bits[left] != target:
                    flip_used -= 1
                left += 1  # 收缩窗口，向右移动左边界

            # 更新最大连续长度
            max_len = max(max_len, right - left + 1)

        return max_len  # 返回最终的最大连续目标字符长度

if __name__ == '__main__':
    sol = Solution()
    target = input().strip()      # 读取目标字符（'0' 或 '1'）
    bits = input().strip()        # 读取二进制字符串
    print(sol.max_continuous_length(target, bits))  # 输出结果

