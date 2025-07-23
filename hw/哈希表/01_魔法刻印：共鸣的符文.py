'''
题目描述
在远古的符文大陆上，魔导师小慕正在研究一种神秘的共鸣魔法。该魔法能在多个魔法卷轴中寻找出所有共同出现的符文字符，并从中提炼出可刻印在魔法器物上的“共鸣刻印”。
每个魔法卷轴上的内容由一串仅包含小写字母的符文组成。若某个字符在所有魔法卷轴中都至少出现一次，则该字符具备“共鸣特性”。更神奇的是，如果某个字符在每个卷轴中都重复出现了若干次，那么该字符就应被重复记录同样多次。
小慕需要你帮助他，从所有魔法卷轴中找出这些具有共鸣的符文字符，并输出最终的“共鸣刻印”。
输入格式
第一行输入一个整数 n，表示魔法卷轴的数量，满足 1 <= n <= 200。
接下来的 n 行中，每行是一个长度不超过 1000 的字符串 s_i，表示第 i 个魔法卷轴的内容。字符串仅包含小写字母 'a' 到 'z'。
输出格式
输出一个字符串，表示共鸣刻印中的所有字符，需满足以下条件：
- 每个字符必须在所有魔法卷轴中都至少出现一次；
- 若某字符在所有卷轴中都出现了 k 次，则输出中应包含 k 个该字符；
- 若某字符在某些卷轴中出现次数不足 k 次，则只取所有卷轴中的最小出现次数；
- 所有字符应按字典序升序输出；
- 若无任何字符在所有卷轴中共鸣，则输出字符串 "null"（不带引号）。
样例
样例1
样例输入：
3
smooth
common
moorings
样例输出：
moo

'''

'''
2. &= 运算符
这是 Python 的位与赋值运算符，相当于 min_freq = min_freq & Counter(word)。但对于 Counter 对象，& 运算符有特殊含义。

3. Counter 之间的 & 运算
当两个 Counter 对象进行 & 运算时，结果是一个新的 Counter，其中包含两个 Counter 中都存在的键，且每个键的值为两者中较小的那个（即取交集并取最小值）。
'''
from collections import Counter  # 引入Counter类，用于统计字符频率
from typing import List  # 引入List类型注解

# 定义一个解决方案类
class Solution:
    # 定义一个方法，用于找出所有字符串中共通的字符
    def commonChars(self, words: List[str]) -> str:
        # 如果输入列表为空，直接返回 "null"
        if not words:
            return "null"

        # 使用 Counter 统计第一个字符串中每个字符出现的次数
        # Counter 是一个字典子类，专门用于计数
        min_freq = Counter(words[0])
        print(min_freq)

        # 遍历其余的字符串
        for word in words[1:]:
            # 对每个字符串使用 Counter 统计频率
            # 使用“&”操作符取交集，即取每个字符在所有字符串中出现的最小次数
            min_freq &= Counter(word) # 这种方法正好能将不是共同出现的键值对去掉
            '''
            c1 = Counter({'a': 2, 'b': 1})
            c2 = Counter({'a': 1, 'b': 2, 'c': 3})
            print(c1 & c2)
            # 输出: Counter({'a': 1, 'b': 1}) 这种方法正好能将不是共同出现的键值对去掉，比如'c': 3
            '''

        # 初始化结果列表
        result = []
        # 遍历所有在交集中出现的字符，按字典序排序
        for char in sorted(min_freq.keys()):
            # 将该字符重复 min_freq[char] 次加入结果中
            result.extend([char] * min_freq[char])

        # 如果结果为空，说明没有任何共鸣字符，返回 "null"
        # 否则将字符列表拼接成字符串返回
        return ''.join(result) if result else "null"

# 创建 Solution 类的实例
sol = Solution()

# 读取魔法卷轴数量
n = int(input())

# 读取所有魔法卷轴内容，去除前后空白符，存入列表中
words = [input().strip() for _ in range(n)]
print(words)
# 调用类方法获取共鸣刻印结果并输出
print(sol.commonChars(words))
