'''
题目练习网址：https://www.algomooc.com/problem/K0000
视频讲解回放：
题目描述
在遥远的魔法大陆，每位魔导师都拥有一颗具有固定魔力值的魔法水晶。每逢月圆之夜，魔法议会会发放一批魔法卷轴。每张卷轴都需要足够的魔力值才能成功激活。
为了公平分配魔力资源，每颗水晶在一轮仪式中只能使用一次。
激活仪式中，每张卷轴将依次寻找一颗尚未被使用且满足条件的水晶来启动：
- 只能选择一颗魔力值大于等于卷轴所需魔力值的水晶（即 水晶 >= 卷轴）；
- 若有多颗水晶满足条件，优先选择魔力值最小的水晶；
- 若魔力值相同，选择编号最小的水晶（编号从 0 开始）；
- 若没有任何水晶满足条件，则此次激活失败，返回 -1；
- 每颗水晶只能匹配成功一次，成功匹配后将无法再次用于其他卷轴。
输入格式
第一行输入一个整数 n，表示魔法水晶的数量。
第二行输入 n 个整数，表示每颗水晶的魔力值（单位：魔力点），中间用空格隔开。
第三行输入一个整数 m，表示待激活的魔法卷轴数量。
第四行输入 m 个整数，表示每张卷轴所需的魔力值（单位：魔力点），中间用空格隔开。
- 1 <= n, m <= 200000
- 1 <= 魔力值 <= 10^9
输出格式
输出一行 m 个整数，依次表示每张卷轴所匹配的水晶编号，若无法匹配则输出 -1。编号之间用空格分隔。
样例
样例1
样例输入：
4
128 256 64 196
4
128 64 64 512
样例输出：
0 2 3 -1
样例说明：
- 第 1 张卷轴需 128 魔力，水晶 0（128）刚好满足，选编号最小的 0；
- 第 2 张卷轴需 64 魔力，水晶 2（64）满足，选 2；
- 第 3 张卷轴需 64 魔力，水晶 2 已用，水晶 3（196）满足，选 3；
- 第 4 张卷轴需 512 魔力，所有剩余水晶都不足，输出 -1。


'''
from bisect import bisect_left
from sortedcontainers import SortedList  # 引入支持自动排序且支持二分的容器


class Solution:
    def assign_crystals(self, crystals, scrolls):
        """
        crystals: List[int] - 魔法水晶的魔力值
        scrolls: List[int] - 魔法卷轴所需的魔力值
        return: List[int] - 每张卷轴匹配到的水晶编号，无法匹配返回 -1
        """
        n = len(crystals)

        # 使用 SortedList 维护可用水晶，元素为元组 (魔力值, 编号)
        # 因为需要按魔力值升序、相同魔力值按编号升序查找最小满足项
        available = SortedList((val, idx) for idx, val in enumerate(crystals))

        result = []  # 存储每张卷轴匹配的水晶编号（或 -1）

        for need in scrolls:
            # 使用 bisect_left 查找满足 (魔力值 >= 需求值) 的最左位置
            # 因为元素是 (魔力值, 编号)，我们构造 (need, -1)，以便找到编号最小的满足项
            i = available.bisect_left((need, -1))

            if i == len(available):
                # 没有任何水晶满足要求，返回 -1
                result.append(-1)
            else:
                # 找到了满足需求的水晶，取其编号
                val, idx = available[i]
                result.append(idx)
                # 将该水晶从可用集合中移除，表示已经被使用
                available.pop(i)

        return result


# 以下为输入输出逻辑
n = int(input())  # 读取水晶数量
crystals = list(map(int, input().split()))  # 读取每个水晶的魔力值

m = int(input())  # 读取卷轴数量
scrolls = list(map(int, input().split()))  # 读取每张卷轴的魔力值需求

sol = Solution()
res = sol.assign_crystals(crystals, scrolls)  # 调用方法获取匹配结果

print(*res)  # 输出匹配结果，用空格分隔
