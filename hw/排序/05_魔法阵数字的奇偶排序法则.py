'''
题目描述
在魔法王国的数字魔法阵中，数字分为 奇数 和 偶数。巫师们需要对魔法阵中的数字进行特定的排序，遵循以下规则：
1. 奇数法则：奇数按 升序 排列。
2. 偶数法则：偶数按 降序 排列。
3. 位置不变：数字的奇偶位置必须与原数组一致。
你的任务是对给定的数字魔法阵进行重新排序，满足上述规则。
输入格式
第一行输入一个整数 n，表示数组的长度，满足 1 ≤ n ≤ 10^5。
第二行输入一个长度为 n 的整数数组 magicArray，表示魔法阵的初始排列，每个数字为不超过10^5的非负整数。
输出格式
输出一个长度为 n 的整数数组，表示重新排序后的魔法阵。
样例
样例1
样例输入：
6
5 2 3 8 1 4
样例输出：
1 8 3 4 5 2
样例说明：
- 奇数部分：[5, 3, 1] 按升序变为 [1, 3, 5]。
- 偶数部分：[2, 8, 4] 按降序变为 [8, 4, 2]。
- 原位置顺序保持不变，最终结果为 [1, 8, 3, 4, 5, 2]。
样例2
样例输入：
4
2 4 6 8
样例输出：
8 6 4 2
样例3
样例输入：
4
1 3 5 7
样例输出：
1 3 5 7
'''
from typing import List  # 导入 List 类型，用于类型提示


class Solution:
    # 定义方法 reorder_magic_array，接受一个整数列表 nums，返回处理后的列表
    def reorder_magic_array(self, nums: List[int]) -> List[int]:
        # 先过滤出奇数，并进行升序排序
        odds = sorted([num for num in nums if num % 2 != 0])
        # 过滤出偶数，并进行降序排序
        evens = sorted([num for num in nums if num % 2 == 0], reverse=True)

        # 创建一个空列表，用来存放最终排序后的结果
        result = []
        # 初始化奇数和偶数的索引
        odd_index, even_index = 0, 0

        # 遍历原始列表 nums，根据当前元素的奇偶性，将相应的元素从 sorted 的列表中取出
        for num in nums:
            if num % 2 != 0:  # 如果是奇数
                result.append(odds[odd_index])  # 从升序的奇数列表中取出元素
                odd_index += 1  # 奇数列表索引加一，指向下一个未取出的元素
            else:  # 如果是偶数
                result.append(evens[even_index])  # 从降序的偶数列表中取出元素
                even_index += 1  # 偶数列表索引加一，指向下一个未取出的元素

        # 返回排序后的结果列表
        return result


if __name__ == '__main__':
    sol = Solution()  # 创建 Solution 类的实例
    n = int(input())  # 输入一个整数，表示列表 nums 的长度
    nums = list(map(int, input().split()))  # 输入一个由空格分隔的整数列表，并将其转换为列表
    print(*sol.reorder_magic_array(nums))  # 调用 reorder_magic_array 方法处理列表，并打印结果

