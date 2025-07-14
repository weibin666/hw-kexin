'''
题目描述
在魔法大陆「艾瑞迪亚」，元素使者小慕正在为战斗准备符文晶石。她手中有两串符文石数组 array1 和 array2，分别代表她和敌方的元素能量波动值。
每块符文晶石都有一个“抗性判定”标准。小慕希望找到她手中哪些晶石是完全安全的——也就是说，它们在释放时不会受到敌方任意一块晶石的干扰。
具体来说，若小慕的某一枚晶石的能量值 array1[i] 与敌方任意一块晶石 array2[j] 的能量差 |array1[i] - array2[j]| 都严格大于某个预设的魔法干扰距离 distance，那么该晶石就被视为“安全的”。
你的任务是帮助小慕统计她的晶石中，有多少枚是安全的。
输入格式
第一行输入三个整数 n、m 和 distance，分别表示小慕的晶石数量、敌方晶石数量，以及魔法干扰的距离范围。
第二行输入 n 个整数，表示小慕的符文晶石能量值数组 array1。
第三行输入 m 个整数，表示敌方的符文晶石能量值数组 array2。
1 <= n, m <= 10000
-1000000 <= array1[i], array2[j] <= 1000000
0 <= distance <= 1000000
输出格式
输出一个整数，表示小慕的符文晶石中，符合安全标准的晶石数量。
样例
样例1
样例输入：
3 4 3
3 6 15
9 11 6 7
样例输出：
1
样例说明：
- 对于 array1[0] = 3，有 |3 - 6| = 3 == distance，不满足“严格大于”条件，因此不安全；
- 对于 array1[1] = 6，有 |6 - 6| = 0 <= distance，不安全；
- 对于 array1[2] = 15，与所有 array2[j] 的差均大于 distance，因此安全。
最终仅有一个元素满足条件，返回 1。

'''
from bisect import bisect_left
from typing import List



class Solution:
    def countSafeRunes(self, array1: List[int], array2: List[int], distance: int) -> int:
        """
        使用排序 + 二分查找优化判断过程。
        """
        # 先对 array2 排序，便于后续使用二分查找
        array2.sort()
        count = 0

        for a in array1:
            # 使用 bisect 在 array2 中找第一个 >= a - distance 的位置
            left = bisect_left(array2, a - distance)

            # 判断该位置及其之后的元素是否在干扰范围内
            # 只要有一个元素在 [a - distance, a + distance] 区间内，说明不安全
            is_safe = True
            if left < len(array2) and abs(array2[left] - a) <= distance:
                is_safe = False

            if is_safe:
                count += 1

        return count

sol = Solution()
n,m,d=map(int,input().split())
arr1=list(map(int,input().split()))
arr2=list(map(int,input().split()))
print(sol.countSafeRunes(arr1,arr2,d))