'''
题目描述
在魔法大陆上，小慕举办了一场盛大的弹珠对决。每颗弹珠都蕴含了强大的魔法能量，沿着同一条魔力轨道前进。弹珠们的能量大小由一个整数数组 marbles 表示：
- marbles[i] 的绝对值代表第 i 颗弹珠的能量大小；
- 正号表示该弹珠向右移动，负号表示向左移动。
所有弹珠以相同的速度飞驰。
当弹珠们迎面而来发生魔法碰撞时，遵循如下规则：
- 如果两颗弹珠发生碰撞，能量较小的那颗会被击碎消失；
- 如果两颗弹珠的能量大小相同，则两颗弹珠都会湮灭；
- 移动方向相同的弹珠永远不会碰撞。
请你施展魔法，找出所有经过激烈碰撞后仍然存在的弹珠，并按照原有顺序排列返回。
输入格式
- 第一行输入一个整数 n (1 <= n <= 10^4)，表示弹珠的数量。
- 第二行输入 n 个整数，表示数组 marbles，其中每个整数的范围为 -1000 <= marbles[i] <= 1000，且 marbles[i] != 0。
输出格式
- 如果有弹珠剩下，输出一行剩余弹珠的能量值，以空格分隔。
- 如果所有弹珠都湮灭了，则输出一行 -1。
样例
样例1
样例输入：
6
5 10 -5 -10 7 8
样例输出：
5 7 8
样例2
样例输入：
4
8 -8 5 -5
样例输出：
-1
样例3
样例输入：
5
10 2 -5 -7 8
样例输出：
10 8
'''


class Solution:
    def marbleCollision(self, marbles):
        # 使用一个栈来模拟弹珠的碰撞过程
        stack = []

        # 遍历每一颗弹珠
        for marble in marbles:
            if marble > 0:
                # 如果当前弹珠向右移动，直接加入栈中
                stack.append(marble)
            else:
                # 当前弹珠向左移动，需要判断是否会与栈中的弹珠碰撞
                while stack and stack[-1] > 0:
                    # 如果栈顶弹珠向右且能量更小，被当前左向弹珠击碎，弹出栈顶继续比较
                    if stack[-1] < -marble:
                        stack.pop()
                        continue
                    # 如果栈顶弹珠能量与当前弹珠相等，双方湮灭，弹出栈顶并终止当前弹珠处理
                    elif stack[-1] == -marble:
                        stack.pop()
                    # 栈顶弹珠能量更大，当前弹珠被击碎，不加入栈，直接退出循环
                    break
                else:
                    # 如果没有发生碰撞或右向弹珠都处理完了，当前左向弹珠加入栈
                    stack.append(marble)

        # 如果栈中还有剩余弹珠，返回它们
        if stack:
            return stack
        else:
            # 所有弹珠都湮灭了，返回 [-1]
            return [-1]


if __name__ == "__main__":
    # 读取弹珠数量
    n = int(input())
    # 读取弹珠能量数组
    marbles = list(map(int, input().split()))
    # 创建 Solution 类的实例
    sol = Solution()
    # 调用 marbleCollision 方法处理弹珠碰撞
    ans = sol.marbleCollision(marbles)
    # 将结果按空格输出
    print(*ans)

