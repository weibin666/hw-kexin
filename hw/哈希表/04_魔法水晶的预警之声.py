'''
题目描述
在奥术帝国的魔法网络中，水晶塔对外开放了多个 Test 魔法接口，供其他法师塔调用。每一次调用都会被记录在一份水晶日志中。每条记录为两个整数 time 和 interfaceId，表示某魔法接口 interfaceId 在时间 time 被调用了一次。
作为魔法网络监察官，你需要调查哪些魔法接口存在异常高频使用现象。给定一个时间窗口长度 timeSegment，如果某个魔法接口存在一个时间窗口 [t, t+timeSegment) 内被调用次数不少于 minLimits 次，我们称该接口为高频接口，很可能被用于非法魔法实验。
请你找出所有满足条件的高频接口编号，并按升序输出。若没有高频接口，请输出一个 -1。
输入格式
- 第一行一个整数 n，表示调用记录的数量。
- 接下来 n 行，每行两个整数 time 和 interfaceId，表示一次接口调用。
- 接下来一行一个整数 timeSegment，表示时间窗口长度。
- 最后一行一个整数 minLimits，表示窗口内最小调用次数。
满足：
- 1 <= n <= 10^5
- 0 <= time <= 10^6
- 0 <= interfaceId <= 10^5
- 所有 time 保证非递减
- 1 <= timeSegment <= 10^5
- 1 <= minLimits <= n
输出格式
- 若存在高频接口，输出一行若干个升序排列的接口编号，以空格分隔。
- 若不存在，输出-1。
样例
样例1
样例输入：
8
0 1
0 10
9 1
10 10
20 3
25 3
100 3
100 3
10
2
样例输出：
1 3
样例说明：
- 接口 1：在时间窗口 [0, 10) 中被调用两次（时间为 0 和 9），满足条件；
- 接口 3：在时间窗口 [100, 110) 被调用两次（时间为 100, 100），也满足条件；
- 接口 10：两次调用时间为 0 和 10，不在同一个窗口，不满足条件。

'''
from collections import defaultdict  # 导入默认字典，用于自动初始化列表
from typing import List

# 定义解决方案类
class Solution:
    # 定义获取高频接口的方法
    def get_interfaces(self, invokes: List[List[int]], time_segment: int, min_limits: int) -> List[int]:
        mp = defaultdict(list)  # 创建一个默认字典，key 是 interfaceId，value 是所有被调用的时间列表

        # 将每条调用记录按接口编号分类，存入字典
        for t, id in invokes:
            '''
            # 学会判断哪些字段作为键
            '''
            mp[id].append(t)  # 把调用时间加入对应接口的调用时间列表

        ans = []  # 存储最终结果：所有满足条件的接口编号

        # 遍历每一个接口编号及其调用时间列表
        for k, v in mp.items():
            # 为了判断某段时间窗口内是否有不少于 min_limits 次调用，我们滑动窗口
            for i in range(min_limits - 1, len(v)):
                # 检查从第 i - min_limits + 1 到 i 这段时间内是否满足调用次数
                if v[i] < v[i - min_limits + 1] + time_segment:
                    # 满足条件：接口 k 在某个 timeSegment 内被调用了不少于 min_limits 次
                    ans.append(k)  # 加入答案
                    break  # 已满足条件，跳出当前接口的进一步判断

        ans.sort()  # 对所有满足条件的接口编号升序排列

        if len(ans) == 0:
            ans = [-1]  # 若没有找到任何高频接口，返回 -1

        return ans  # 返回结果列表

# 主程序入口
n = int(input())  # 输入调用记录数量
invokes = [list(map(int, input().split())) for _ in range(n)]  # 读取 n 条调用记录，每条包含 time 和 interfaceId
time_segment = int(input())  # 输入时间窗口长度
min_limits = int(input())  # 输入最小调用次数

# 创建 Solution 对象并调用方法计算答案
ans = Solution().get_interfaces(invokes, time_segment, min_limits)

# 输出所有高频接口编号（或 -1）
print(*ans)
