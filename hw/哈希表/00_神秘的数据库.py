'''
题目描述
在一个神秘的魔法世界中，存在着一个巨大的数据库，维护着当前的网元信息表（curTable）。每个网元都有一个独特的标识符（neId）、名称（neName）以及一个标记值（neFlag）。为了保证网元信息的一致性，系统还备份了一份网元信息表（bakTable），它仅包含每个网元的标识符（neId）和名称（neName）。我们的任务是将备份表中的信息同步到当前表中，确保两个表的一致性。
同步规则：
- 对于 curTable 中不存在的 neId，在 curTable 中增加该条记录，并将 neFlag 初始设置为 0。
- 对于 curTable 中已存在的 neId，更新 neName 的值为 bakTable 中对应的值，neFlag 不需要更新。
输入格式
- 第一行输入一个整数 curTableSize，表示当前网元信息表 curTable 的记录条数。
- 接下来 curTableSize 行，每行包含 neId、neName 和 neFlag，分别表示网元的标识符、名称和标记值。
- 接下来输入一个整数 bakTableSize，表示备份网元信息表 bakTable 的记录条数。
- 接下来 bakTableSize 行，每行包含 neId 和 neName，分别表示备份表中的网元标识符和名称。
- neId 值仅由数字组成，且在 1 到 100000 范围内。
- neName 由字母和数字组成，长度为 1 到 20。
- neFlag 为一个数字，范围为 0 到 9。
- 0 <= curTableSize, bakTableSize <= 50000，且 curTableSize 和 bakTableSize 不同时为 0。
输出格式
- 按照 neId 升序输出同步后的当前网元信息表内容，每行输出 neId、neName 和 neFlag，用空格分隔。
样例
样例1
样例输入：
4
256 NE256 1
290 NE290 0
268 26800000 1
257 NE257 1
3
273 NE273
268 NE268
257 NE257
样例输出：
256 NE256 1
257 NE257 1
268 NE268 1
273 NE273 0
290 NE290 0
样例说明：
- 当前网元信息表 curTable 中有 4 条记录：256、290、268 和 257。根据备份表 bakTable 中的记录进行同步。
- 在同步过程中，268 的 neName 更新为 NE268，而其他记录保持不变。273 在 curTable 中不存在，因此会新增一条记录，neFlag 设置为 0。

'''
class Solution:
    def syncTables(self, curTable, bakTable):
        # 使用字典来存储当前网元信息表 curTable 的数据
        # key 为 neId，value 是一个列表，包含 [neName, neFlag]
        cur_dict = {ne[0]: [ne[1], ne[2]] for ne in curTable}

        # 遍历备份表中的每一条记录
        for neId, neName in bakTable:
            if neId in cur_dict:
                # 如果该 neId 已存在于当前表中，则更新其 neName 为备份表中的值
                cur_dict[neId][0] = neName
            else:
                # 如果该 neId 不存在于当前表中，则新增记录，并设置 neFlag 初始为 0
                cur_dict[neId] = [neName, 0]

        # 将当前网元信息表按 neId 升序排序
        result = sorted(cur_dict.items(), key=lambda x: x[0])

        # 将排序结果转换为指定的输出格式：[[neId, neName, neFlag], ...]
        return [f"{k} {v[0]} {v[1]}" for k, v in result]


if __name__ == "__main__":
    # 读取当前网元信息表的记录数
    curTableSize = int(input())

    # 初始化当前表列表
    curTable = []
    for _ in range(curTableSize):
        # 每行输入：neId、neName、neFlag（用空格分隔）
        neId, neName, neFlag = input().split()
        # 将字符串 neId 和 neFlag 转换为整数，加入 curTable 列表
        curTable.append([int(neId), neName, int(neFlag)])

    # 读取备份网元信息表的记录数
    bakTableSize = int(input())

    # 初始化备份表列表
    bakTable = []
    for _ in range(bakTableSize):
        # 每行输入：neId 和 neName（用空格分隔）
        neId, neName = input().split()
        # 将字符串 neId 转换为整数，加入 bakTable 列表
        bakTable.append([int(neId), neName])

    # 创建 Solution 类实例并调用同步方法
    sol = Solution()
    result = sol.syncTables(curTable, bakTable)

    # 按升序输出同步后的当前网元信息表，每行输出 neId、neName、neFlag
    for s in result:
        print(s)