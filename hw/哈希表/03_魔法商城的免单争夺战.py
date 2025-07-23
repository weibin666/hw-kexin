'''
题目描述
在一个神秘的魔法商城，每天都会有一个魔法免单时刻。每到这个时刻，那些下单最快的魔法师（精确到毫秒）就能免费获取魔法道具！
你的任务是，作为魔法商城的管理员，需要帮助记录并统计出有多少订单可以抢到免单。
输入格式
1. 第一行：一个整数 size，代表魔法订单的数量（1 ≤ size < 50000）。
2. 接下来的 size 行：每行是一个订单的下单时间，格式如下：
YYYY-MM-DD hh:mm:ss.fff
  - YYYY-MM-DD 是下单的日期。
  - hh:mm:ss 是下单的具体时刻（小时、分钟、秒）。
  - fff 是下单时间的毫秒值。
输出格式
一个整数，表示可以抢到兔单的订单数量。
样例
样例1
样例输入：
3
2019-01-01 00:00:00.001
2019-01-01 00:00:00.002
2019-01-01 00:00:00.003
样例输出：
1
样例说明：
在这个场景中，魔法商城同一秒内有三个订单，最早的订单（毫秒值为 001）能够抢到免单，其余订单无缘免单。
样例2
样例输入：
6
2019-01-01 00:00:00.001
2019-01-01 00:00:00.002
2019-01-01 00:00:00.003
2019-01-01 08:59:00.123
2019-01-01 08:59:00.123
2018-12-28 13:08:00.999
样例输出：
4
样例3
样例输入：
5
2019-01-01 00:00:00.004
2019-01-01 00:00:00.004
2019-01-01 00:00:01.006
2019-01-01 00:00:01.006
2019-01-01 00:00:01.005
样例输出：
3
'''
from collections import defaultdict


class Solution:
    def free_order(self, order_time):
        # 创建一个字典，用来记录每秒的最早订单时间（毫秒）
        '''
        要熟练使用下面这个方法：
        time_map = defaultdict(list)
        '''
        time_map = defaultdict(list)
        '''
        要熟练使用上面这个方法：
        time_map = defaultdict(list)
        '''
        # 遍历订单，按照秒分组
        for order in order_time:
            main_time, ms = order.rsplit(".", 1)
            print(main_time, ms)
            ms = int(ms)
            time_map[main_time].append(ms)

        # 统计抢到兔单的订单数量
        free_count = 0

        for main_time, ms_list in time_map.items():
            # 找到当前秒的最小毫秒值
            min_ms = min(ms_list)
            # 统计所有等于最小毫秒值的订单数量
            free_count += ms_list.count(min_ms)

        return free_count


# 魔法代码入口
if __name__ == "__main__":
    size = int(input().strip())
    order_time = [input().strip() for _ in range(size)]
    mall = Solution()
    result = mall.free_order(order_time)
    print(result)
