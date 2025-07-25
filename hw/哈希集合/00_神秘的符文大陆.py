'''
题目描述
在神秘的符文大陆上，存在着一种古老的魔法符文，这些符文由英文字母和数字组成，蕴含着强大的魔力。传说中，只有当某个符文在所有符文卷轴中都出现至少 n 次时，才能解锁其真正的力量。现在，你作为一位符文大师，需要从 m 个符文卷轴中找出这些强大的符文。
输入格式
- 首行是整数 n，表示符文需要出现的最小次数，取值范围 [1, 100]。
- 第二行是整数 m，表示符文卷轴的数量，取值范围 [1, 100]。
- 接下来 m 行，每行一个符文卷轴，由英文字母和数字组成，长度范围 [1, 2000)。
输出格式
按 ASCII 码升序输出所有符合条件的符文。如果没有符合条件的符文，则输出字符串"null"。
样例
样例1
样例输入：
2
3
aabbccFFFFx2x2
aaccddFFFFx2x2
aabcdFFFFx2x2
样例输出：
2Fax
样例说明：
符文 a 在三个卷轴中都出现 2 次，符合要求；符文 b 在第二、三个卷轴中分别出现 0 次、1 次，不符合要求；符文 c 在第三个卷轴中出现 1 次，不符合要求；符文 d 在第三个卷轴中出现 1 次，不符合要求；符文 F 在三个卷轴中都出现了 4 次，符合要求；符文 x 在三个卷轴中都出现了 2 次，符合要求；符文 2 在三个卷轴中都出现了 2 次，符合要求。因此符文 a、F、x、2 符合要求，按 ASCII 码升序输出为 2Fax。
样例2
样例输入：
2
3
aa
bb
cc
样例输出：
null
样例说明：
没有任何符文在所有卷轴中都出现 2 次及以上，因此输出空字符串。
题目解析
理解题目
这道题目涉及字符串处理与字符统计，需要在多个符文卷轴中筛选出符合条件的符文。具体来说：
- 符文卷轴 是由字母和数字组成的字符串。
- 符合条件的符文 需要在 所有 符文卷轴中至少出现 n 次。
- 按 ASCII 码顺序 输出符合条件的符文，若无符合条件的符文，则返回 "null"。
从样例来看，核心任务是统计每个符文在各个卷轴中出现的次数，然后筛选出所有卷轴都满足至少 n 次出现的符文，并进行排序输出。
使用算法
本题使用了集合运算 和 哈希表统计 进行高效筛选，算法流程如下：
- 遍历每个符文卷轴，统计字符出现次数：
  - 使用 Counter 统计当前卷轴中各符文的出现次数。
  - 选取出现次数至少为 n 的字符，存入集合。
- 求多个集合的交集：
  - 初始时，将第一个卷轴的符合条件符文作为结果集合。
  - 依次取后续卷轴的符合条件字符集合的交集，确保筛选出的符文在所有卷轴中都符合要求。
- 排序并输出：
  - 按照 ASCII 码升序排序。
  - 若结果集合为空，则输出 "null"，否则输出拼接后的字符串。
实现
步骤 1：读取输入
首先，读取 n（最小出现次数）和 m（符文卷轴数量），然后读取 m 行字符串，存入列表 strings。
步骤 2：遍历所有卷轴，统计字符出现次数
使用 Counter 统计每个卷轴的字符出现次数，筛选出 至少出现 n 次的字符，存入一个集合。
步骤 3：排序并输出
对结果集合 res 进行 ASCII 码排序，并转换为字符串输出。
如果 res 非空，则按 ASCII 排序并拼接成字符串返回。
如果 res 为空，返回 "null"。

'''
from collections import Counter  # 引入Counter类用于统计字符出现次数


class Solution:
    def get_n_times_character(self, n, strings):
        """
        获取在所有字符串中至少出现 n 次的字符，并按 ASCII 码升序排序返回

        :param n: 符文需要出现的最小次数
        :param strings: 包含多个符文卷轴的字符串列表
        :return: 结果字符串，包含符合条件的字符，按 ASCII 码排序；若无符合条件的字符，返回 "null"
        """
        res = set()  # 初始化结果集合

        for i, s in enumerate(strings):
            c = Counter(s)  # 统计当前符文卷轴中每个字符的出现次数
            '''
            学习！
            '''
            st = {k for k, v in c.items() if v >= n}  # 筛选出在当前卷轴中出现至少 n 次的字符

            if i == 0:
                res = st  # 如果是第一个卷轴，直接初始化结果集合
            else:
                '''
                学习！
                '''
                res &= st  # 取交集，确保符文在所有卷轴中都至少出现 n 次

        # 如果结果集合非空，则按 ASCII 码升序排序并拼接成字符串返回，否则返回 "null"
        return "".join(ch for ch in sorted(res)) if res else "null"


# 读取输入
n = int(input())  # 符文需要出现的最小次数
m = int(input())  # 符文卷轴的数量
strings = [input() for _ in range(m)]  # 读取 m 行符文卷轴字符串

# 输出符合条件的符文字符
print(Solution().get_n_times_character(n, strings))
