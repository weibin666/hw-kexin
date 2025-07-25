'''
题目描述
在魔法大陆的一片神秘区域，有一个由 魔法塔 守护的二维地图。地图上的每个位置可能是以下之一：
- A：魔法塔的位置，负责守护该区域。
- B：魔法屏障，阻挡魔法塔的视线。
- C：旅人，需要魔法塔的保护。
- .：空地，没有任何目标或阻挡。
魔法塔的监控规则：
1. 魔法塔的视线可以穿过 旅人 (C)，继续观察到其后方的目标。
2. 魔法屏障 (B) 会完全阻挡魔法塔的视线，其后的目标无法被监控。
3. 魔法塔可以同时监控其所在行和列的目标。
你的任务是找到能够监控到最多旅人的魔法塔，并计算该魔法塔能监控到的旅人数。
输入格式
前两行分别输入两个整数 m 和 n，表示地图的行数和列数，满足 1 ≤ m, n ≤ 100。
接下来输入 m 行，每行包含一个长度为 n 的字符串，表示地图 magicMap 的布局：
- 每个字符为以下之一：A、B、C 或 .，且字符间无空格。
输出格式
输出一个整数，表示能够监控到最多旅人的魔法塔的旅人数。如果地图上没有魔法塔 A，输出 0。
样例
样例1
样例输入：
5
5
ACC.B
.C..C
A.BCA
....B
CCA..
样例输出：
3
样例说明：
- 第一行的魔法塔 A 可以监控到 3 个旅人。
- 第三行的左侧魔法塔 A 可以监控到 1 个旅人。
- 第三行的右侧魔法塔 A 可以监控到 2 个旅人。
样例2
样例输入：
5
5
A....
.B.C.
AC.BA
.....
CCA..
样例输出：
2
样例3
样例输入：
4
4
.B..
BCBC
CB.A
....
样例输出：
1

'''
from typing import List

class Solution:
    def max_prorect(self, mat: List[str]) -> int:
        # 获取地图的行数 n 和列数 m
        n, m = len(mat), len(mat[0])

        # 初始化两个辅助数组，分别用于记录每个位置在行方向和列方向可以监控到的旅人数
        sx = [[0 for _ in range(m)] for _ in range(n)]  # 行方向
        sy = [[0 for _ in range(m)] for _ in range(n)]  # 列方向

        # 遍历每一行，预处理每个位置在该行中能监控到的旅人数
        for i in range(n):
            j = 0
            while j < m:
                if mat[i][j] == 'B':
                    # 遇到屏障则跳过，屏障后续部分将重新计数
                    j += 1
                else:
                    # 从当前 j 开始向右遍历直到遇到屏障或行尾，统计中间出现的旅人数
                    k = j
                    cnt = 0
                    while k < m and mat[i][k] != 'B':
                        cnt += (mat[i][k] == 'C')  # 是旅人则计数加一
                        k += 1
                    # 将该段区间 [j, k) 内的所有位置都赋值为统计到的旅人数
                    for p in range(j, k):
                        sx[i][p] = cnt
                    j = k  # 跳过该段

        # 遍历每一列，预处理每个位置在该列中能监控到的旅人数
        for j in range(m):
            i = 0
            while i < n:
                if mat[i][j] == 'B':
                    # 遇到屏障则跳过，屏障下方部分将重新计数
                    i += 1
                else:
                    # 从当前 i 开始向下遍历直到遇到屏障或列底，统计中间出现的旅人数
                    k = i
                    cnt = 0
                    while k < n and mat[k][j] != 'B':
                        cnt += (mat[k][j] == 'C')  # 是旅人则计数加一
                        k += 1
                    # 将该段区间 [i, k) 内的所有位置都赋值为统计到的旅人数
                    for p in range(i, k):
                        sy[p][j] = cnt
                    i = k  # 跳过该段

        # 遍历地图，查找所有魔法塔 'A' 所在位置，计算其可监控的旅人数（行+列方向）
        ans = 0
        for i in range(n):
            for j in range(m):
                if mat[i][j] == 'A':
                    # 对于每个魔法塔，取其行方向和列方向的总监控旅人数
                    ans = max(ans, sx[i][j] + sy[i][j])  # 更新最大值

        return ans  # 返回所有魔法塔中能监控最多旅人的值

# 主程序入口
if __name__ == '__main__':
    sol = Solution()
    # 读入地图行数和列数
    n = int(input())
    m = int(input())
    # 读入地图每一行，组成二维字符地图
    mat = [input() for _ in range(n)]
    # 输出结果：能够监控最多旅人的魔法塔能监控的旅人数
    print(sol.max_prorect(mat))
