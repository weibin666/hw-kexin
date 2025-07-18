'''
题目描述
在魔法城堡的中心，有一座古老的神秘房间，房间里隐藏着一件珍贵的宝物。为了获得这份宝藏，你需要帮助勇士们完成一项任务：他们必须从一个特定的起点开始，寻找通往宝藏的道路，穿越整个房间，并在路径上每一块可以通行的空地都要经过一次，最终找到宝藏。
房间的布局由一个二维网格 grid 表示，每个格子上可能是以下几种内容：
- 数字 1 表示起点。
- 数字 2 表示宝藏所在的终点。
- 数字 0 表示可以通行的空地。
- 数字 -1 表示障碍物，无法通过。
在这次任务中，勇士们只能朝四个方向移动（上、下、左、右），且不能重复经过任何一块空地。你的任务是计算从起点到宝藏的所有有效路径数目，其中每一条路径必须经过每一块可以通行的空地。
输入格式
输入的第一行包含两个整数 m 和 n，表示网格的行数和列数 (1 <= m * n <= 20)。
接下来的 m 行中，每行包含 n 个整数，表示房间的布局。每个整数的值可以是以下之一：
- 1：表示起点。
- 2：表示终点。
- 0：表示可以通行的空地。
- -1：表示障碍物。
输出格式
输出一个整数，表示从起点到终点的所有不同路径数目。如果不存在路径，输出 0。
样例
样例1
样例输入：
3 4
1 0 0 0
0 0 0 0
0 0 2 -1
样例输出：
2
样例说明：
有以下两条路径：
1. (0,0) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (1,2) -> (1,1) -> (1,0) -> (2,0) -> (2,1) -> (2,2)
2. (0,0) -> (1,0) -> (2,0) -> (2,1) -> (1,1) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (1,2) -> (2,2)
样例2
样例输入：
3 4
1 0 0 0
0 0 0 0
0 0 0 2
样例输出：
4
样例说明：
有以下四条路径：
1. (0,0) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (1,2) -> (1,1) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (2,3)
2. (0,0) -> (0,1) -> (1,1) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (1,2) -> (0,2) -> (0,3) -> (1,3) -> (2,3)
3. (0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (1,2) -> (1,1) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (2,3)
4. (0,0) -> (1,0) -> (2,0) -> (2,1) -> (1,1) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (1,2) -> (2,2) -> (2,3)
样例3
样例输入：
2 2
0 1
2 0
样例输出：
0
样例说明：
没有一条路径能完全穿过每一个空的方格一次。

'''

class Solution:
    def findPaths(self, grid: list) -> int:
        # 获取网格的行数和列数
        n, m = len(grid), len(grid[0])
        ans = 0  # 记录最终的合法路径数量
        foods = 0  # 记录需要遍历的可通行空地数量（值为 0 的格子）
        mp = grid  # 将输入网格赋值给 mp，后续操作中对 mp 修改即可
        vis = [[False for _ in range(m)] for _ in range(n)]  # 标记每个格子是否已访问
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # 定义四个移动方向：上、下、左、右
        sx = sy = ex = ey = -1  # 起点和终点坐标初始化为 -1（未找到）

        # 遍历整个网格，找出起点、终点，并统计可通行空地的总数
        for i in range(n):
            for j in range(m):
                if mp[i][j] == 1:
                    sx, sy = i, j  # 记录起点坐标
                elif mp[i][j] == 2:
                    ex, ey = i, j  # 记录终点坐标
                elif mp[i][j] == 0:
                    foods += 1  # 统计所有空地数量

        # 定义深度优先搜索函数，参数为当前坐标 (x, y) 和已走过的空地数量 collected
        def dfs(x: int, y: int, collected: int):
            nonlocal ans  # 引用外部变量 ans

            # 如果当前格子是终点
            if mp[x][y] == 2:
                # 判断是否已遍历所有空地，是则说明找到一条合法路径
                if collected == foods:
                    ans += 1
                return

            val = mp[x][y]  # 记录当前格子的原始值
            if val == 0:
                collected += 1  # 如果当前格子是空地，则增加已遍历数量
                mp[x][y] = -2  # 临时将空地标记为 -2，避免重复走

            vis[x][y] = True  # 标记当前格子为已访问

            # 尝试向四个方向移动
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy  # 计算新位置
                # 如果新位置合法、未访问且不是障碍物（-1），则继续搜索
                if 0 <= nx < n and 0 <= ny < m and not vis[nx][ny] and mp[nx][ny] != -1:
                    dfs(nx, ny, collected)

            vis[x][y] = False  # 回溯时取消当前格子的访问标记
            mp[x][y] = val  # 恢复当前格子的原始值，确保其他路径能访问到

        # 从起点开始深度优先搜索
        dfs(sx, sy, 0)

        # 返回最终合法路径数量
        return ans


if __name__ == "__main__":
    # 读取输入的行数和列数
    n, m = map(int, input().split())
    # 构建二维网格，表示房间布局
    grid = [list(map(int, input().split())) for _ in range(n)]

    # 创建 Solution 类对象
    solution = Solution()
    # 调用 findPaths 方法计算路径数目
    result = solution.findPaths(grid)

    # 输出结果
    print(result)
