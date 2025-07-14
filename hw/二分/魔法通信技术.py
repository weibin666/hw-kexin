'''
题目描述
在奇幻大陆「阿斯卡隆」，魔法通信技术已经高度发达，魔法师们可以通过「魔法信标」相互联系。然而，由于部分区域受魔法禁制影响，某些信标无法接入主网络，这些区域被称为 「禁区」。如果一位魔法师的信标编号前缀属于某个禁区范围，他将无法使用通信服务。
现在，给定若干个禁区编号范围，以及一批魔法信标编号，请你判断哪些信标可以正常使用通信服务，并按照字典序降序输出；如果所有信标都在禁区范围内，则输出 "empty"。
输入格式
第一行包含两个整数 m 和 n，表示禁区的数量和信标编号的数量（1 <= m, n <= 1000）。
接下来的 m 行，每行包含两个字符串 start 和 end（start <= end），表示一个禁区编号范围，所有以 [start, end] 之间的前缀开头的信标都无法使用。
- start 和 end 具有相同的长度，长度范围为 [1,6]。
然后的 n 行，每行包含一个字符串 area，表示一个魔法信标编号。
- 信标编号的长度范围为 [6,15]。
输出格式
按照字典序降序输出所有可用的魔法信标编号，每行一个。如果所有信标都无法使用，则输出 "empty"。
样例
样例1
样例输入：
2 4
755 769
398 399
3970001
756000000000002
600032
755100
样例输出：
600032
3970001
样例说明：
- 信标 755100 和 756000000000002 的前缀落在 [755,769] 之间，无法使用。
- 信标 3970001 和 600032 不在任何禁区范围，可以正常使用，按字典序降序排列后输出。
样例2
样例输入：
1 2
4 4
4000000
495555
样例输出：
empty

'''
from typing import List
from bisect import bisect_right

class Solution:
    def get_roaming_area(self, restricts: List[List[str]], areas: List[str]) -> List[str]:
        merged = [[] for _ in range(7)]  # merged[i] 表示前缀长度为 i 的禁区

        # 将禁区根据前缀长度进行分类
        for start, end in restricts:
            length = len(start)
            merged[length].append([int(start), int(end)])

        left = [[] for _ in range(7)]   # 每种长度的左端点列表
        right = [[] for _ in range(7)]  # 每种长度的右端点列表

        # 合并每种长度的区间
        for i in range(1, 7):
            bucket = sorted(merged[i])
            res = []
            for l, r in bucket:
                if not res or res[-1][1] < l - 1:
                    res.append([l, r])
                else:
                    res[-1][1] = max(res[-1][1], r)
            left[i] = [v[0] for v in res]
            right[i] = [v[1] for v in res]

        # 判断某个信标是否被禁用
        def is_restricted(area: str) -> bool:
            for length in range(1, 7):
                if length > len(area):
                    break
                prefix = int(area[:length])
                idx = bisect_right(left[length], prefix) - 1
                if 0 <= idx and left[length][idx] <= prefix <= right[length][idx]:
                    return True
            return False

        # 过滤合法信标并按字典序降序排序
        res = sorted([area for area in areas if not is_restricted(area)], reverse=True)
        return res if res else ["empty"]

# 处理输入输出
if __name__ == "__main__":
    m, n = map(int, input().strip().split())
    restricts = [input().strip().split() for _ in range(m)]
    areas = [input().strip() for _ in range(n)]

    solution = Solution()
    results = solution.get_roaming_area(restricts, areas)
    print("\n".join(results))
