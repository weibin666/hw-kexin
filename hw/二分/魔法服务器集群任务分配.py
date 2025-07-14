'''
题目描述
在一个神秘的魔法世界里，魔法师们掌控着一个强大的魔法服务器集群。为了应对一波前所未有的任务压力，魔法师们将任务按照不同类型进行分类，每种任务有不同的数量。这些任务将被分配到服务器集群中，而每台服务器只能处理一种类型的任务。每台服务器可以处理多个任务，但不同类型的任务不能同时分配给同一台服务器。
为了保证魔法服务器集群的正常运行，魔法师们设定了负载和最高负载的概念：
- 负载定义为每台服务器所分配的任务个数，如果某台服务器没有任务，那么其负载为0。
- 最高负载则是所有服务器中负载的最大值。
在任务分配中，魔法师们需要制定一个方案，使得最高负载的值最小。你的任务是设计一个算法，计算并返回这个最小的最高负载。
输入格式
- 第一行一个整数serverNum，表示集群中服务器的数量 (1 <= serverNum <= 10^9)。
- 第二行一个整数taskTypeNum，表示这批任务的类型数 (1 <= taskTypeNum <= 100000，且 taskTypeNum <= serverNum)。
- 第三行输入taskTypeNum个整数，表示任务数组task，其中task[i]表示该类型任务的数量 (1 <= task[i] <= 10^9)。
输出格式
输出一个整数，表示所有服务器分配任务后最高负载的最小值。
样例
样例1
样例输入：
7 4
10 20 15 5
样例输出：
10
样例说明：
在这个样例中，魔法集群包含7台服务器，任务有4种类型，分别是10个、20个、15个和5个。通过合理的分配，每台服务器的负载可以做到最小的最高负载为10。
此时分配的服务器台数分别是[1, 2, 2, 1]。

'''

class Solution:
    def minMaxLoad(self, serverNum: int, task: list) -> int:
        # 使用二分查找来确定最小的最大负载值

        # 初始的负载区间是从 1 到所有任务中数量最多的那类任务数量
        left, right = 1, max(task)
        result = right  # 最终结果初始化为最大值

        # 二分查找开始
        while left <= right:
            mid = (left + right) // 2  # 尝试的中间负载值

            # 检查是否可以在最大负载为 mid 的前提下完成任务分配
            if self.isPossible(task, serverNum, mid):
                # 如果可以，则更新答案，并尝试更小的负载
                result = mid
                right = mid - 1
            else:
                # 如果不可以，则增大负载再试
                left = mid + 1

        # 返回找到的最小的最大负载值
        return result

    def isPossible(self, task: list, serverNum: int, maxLoad: int) -> bool:
        # 检查是否可以在给定最大负载 maxLoad 下使用不超过 serverNum 台服务器完成所有任务

        required_servers = 0  # 所需的服务器总数初始化为 0

        for t in task:
            # 每种任务类型需要分配多少台服务器：
            # 如果该任务类型有 t 个任务，每台服务器最多 maxLoad 个任务
            # 向上取整计算所需服务器数：(t + maxLoad - 1) // maxLoad
            required_servers += (t + maxLoad - 1) // maxLoad

        # 返回所需服务器数是否不超过给定服务器总数
        return required_servers <= serverNum


if __name__ == "__main__":
    # 输入处理：读取服务器数量 serverNum 和任务类型数量 taskTypeNum
    serverNum, taskTypeNum = map(int, input().split())

    # 读取每种任务类型的任务数量数组
    task = list(map(int, input().split()))

    # 创建解决方案实例
    sol = Solution()

    # 调用方法计算最小最大负载
    result = sol.minMaxLoad(serverNum, task)

    # 输出结果
    print(result)
