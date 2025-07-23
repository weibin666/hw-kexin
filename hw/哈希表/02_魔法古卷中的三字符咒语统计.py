'''
题目描述
在魔法王国中，发现了一本记录着一长串字符的古老魔法卷轴。卷轴中的每连续 三个字符 组成的子字符串被称为 魔法咒语。为了研究咒语的力量，巫师们需要你解决以下问题：
1. 找到 出现次数最多 的三字符咒语。
2. 输出该咒语的出现次数。
如果有多个咒语的出现次数相同，则选择 字典序最小 的咒语。
输入格式
输入一个字符串 s，表示魔法卷轴中的字符序列，满足以下条件：
- 字符串仅包含小写字母。
- 3 ≤ len(s) ≤ 10^5。
输出格式
输出两行：
1. 第一行输出出现次数最多的三字符咒语。
2. 第二行输出该咒语的出现次数。
样例
样例1
样例输入：
abcabcabc
样例输出：
abc
3
样例说明：
所有可能的三字符咒语及其出现次数为：
- "abc" 出现 3 次。
- "bca" 出现 2 次。
- "cab" 出现 2 次。
因此，出现次数最多的咒语是 "abc"，出现了 3 次。
样例2
样例输入：
aabbaabb
样例输出：
aab
2
样例说明：
所有可能的三字符咒语及其出现次数为：
- "aab" 出现 2 次。
- "abb" 出现 2 次。
- "baa" 出现 2 次。
由于 "aab" 在字典序上最小，因此选择 "aab"。

'''
from typing import List  # 引入 List 类型，用于函数返回值类型声明


# 定义一个 Solution 类，里面包含一个最大频率子串查找的方法
class Solution:

    # max_3_substring 方法用于查找给定字符串中出现频率最高的 3 个字符组成的子串
    # 参数 s: 输入的字符串
    # 返回值是一个列表，包含出现次数最多的子串和它的出现次数
    def max_3_substring(self, s: str) -> List[str]:
        from collections import Counter  # 从 collections 模块中引入 Counter，用于计算各子串出现的频率

        # 使用 Counter 统计所有长度为 3 的子串的出现次数
        # s[i:i + 3] 为从索引 i 开始的长度为 3 的子串，i 的范围是 [0, len(s) - 3]
        '''
        关键代码如下：
        c = Counter(s[i:i + 3] for i in range(len(s) - 2))
        mx = max(c.values())
        '''
        c = Counter(s[i:i + 3] for i in range(len(s) - 2))

        # 计算出出现次数的最大值（即最大频率）
        mx = max(c.values())

        # 查找所有出现次数等于最大频率的子串，并取出其中字典序最小的一个
        s = min(k for k, v in c.items() if v == mx)

        # 返回一个包含最频繁的子串和它的出现次数的列表，注意次数需要转换成字符串形式
        return [s, str(mx)]


# 主程序部分
if __name__ == '__main__':
    # 创建 Solution 类的实例
    sol = Solution()

    # 接收用户输入的字符串
    s = input()

    # 调用 max_3_substring 方法，获取结果
    res = sol.max_3_substring(s)

    # 输出结果：首先输出子串，然后输出它的出现次数
    for val in res:
        print(val)
