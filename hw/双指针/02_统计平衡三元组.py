'''
题目描述
小慕最近在研究三元组的平衡性问题。给定一个整数数组 arr，以及三个整数 numA、numB、numC，请你帮助小慕统计满足以下条件的三元组个数 (arr[i], arr[j], arr[k])，其中 0 <= i < j < k < len(arr)：
三元组需同时满足以下三个条件：
- |arr[i] - arr[j]| <= numA
- |arr[j] - arr[k]| <= numB
- |arr[i] - arr[k]| <= numC
请你返回所有满足条件的三元组的数量。
输入格式
输入包含四行：
- 第一行一个整数 n，表示数组 arr 的长度。（3 <= n <= 1000）
- 第二行包含 n 个整数，表示数组 arr 中的元素，元素值范围为 -100000 <= arr[i] <= 100000
- 第三行一个整数 numA
- 第四行一个整数 numB
- 第五行一个整数 numC
输出格式
输出一个整数，表示满足条件的三元组的数量。
样例
样例1
样例输入：
8
4 9 9 8 9 5 3 7
1
3
0
样例输出：
3
样例说明：
符合要求的三元组为：
- (9, 9, 9)
- (9, 8, 9)
- (9, 8, 9)
'''

class Solution:
    def countBalancedTriplets(self, arr, numA, numB, numC):
        n = len(arr)  # 获取数组长度
        count = 0     # 初始化满足条件的三元组计数器

        # 遍历数组的中间位置 j，确保 i < j < k
        for j in range(1, n - 1):
            mid = arr[j]  # 当前中间值

            # 构造左侧所有满足 |arr[i] - arr[j]| <= numA 的 i 值集合
            valid_i = sorted(x for x in arr[:j] if abs(x - mid) <= numA)

            # 构造右侧所有满足 |arr[j] - arr[k]| <= numB 的 k 值集合
            valid_k = sorted(x for x in arr[j+1:] if abs(x - mid) <= numB)

            # 双指针初始化，准备查找满足 |arr[i] - arr[k]| <= numC 的配对数
            l = r = 0

            # 对于每一个合法的 i 值，统计有多少个合法的 k 值满足最终条件
            for i_val in valid_i:
                # 移动左指针 l，使得 valid_k[l] >= i_val - numC
                while l < len(valid_k) and valid_k[l] < i_val - numC:
                    l += 1
                # 移动右指针 r，使得 valid_k[r] <= i_val + numC
                while r < len(valid_k) and valid_k[r] <= i_val + numC:
                    r += 1
                # 统计所有在 [i_val - numC, i_val + numC] 范围内的 k 值个数
                count += r - l

        return count  # 返回最终满足条件的三元组数量


# 主程序，读取输入并调用函数
if __name__ == "__main__":
    n = int(input())  # 输入数组长度
    arr = list(map(int, input().split()))  # 输入数组元素
    numA = int(input())  # 输入 numA 条件值
    numB = int(input())  # 输入 numB 条件值
    numC = int(input())  # 输入 numC 条件值

    sol = Solution()
    print(sol.countBalancedTriplets(arr, numA, numB, numC))  # 输出最终答案
