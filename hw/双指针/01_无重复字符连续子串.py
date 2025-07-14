'''
题目描述
在一片神秘的魔法森林中，勇士小慕收到了一项艰难的任务：他必须在森林的深处找到所有不含重复字符的魔法符号。每个符号都是由字母组成的，符号越长，它所能承载的魔法力量越强。小慕必须计算出，给定一个符号，森林中所有不含重复字符的符号组合有多少个。为了完成这个任务，小慕必须根据符号的结构和魔法规则，计算出无重复字符的连续子串的个数。
输入格式
输入一个由小写字母组成的字符串str，表示魔法符号。字符串的长度不超过20000。
输出格式
输出一个整数，表示无重复字符的连续子串的个数。
样例
样例1
样例输入：
abac
样例输出：
8
样例说明：
所有子串是 a, ab, aba, abac, b, ba, bac, a, ac, c。其中无重复字符的子串为：a, ab, b, ba, bac, a, ac, c，总个数为8。
样例2
样例输入：
xbmxbnh
样例输出：
21
样例说明：
所有子串是 x, xb, xbm, b, bm, bmx, m, mx, mxb, mxbn, mxbnh, x, xb, xbn, xbnh, b, bn, bnh, n, nh, h。其中无重复字符的子串为：x, xb, xbm, b, bm, bmx, m, mx, mxb, mxbn, mxbnh, x, xb, xbn, xbnh, b, bn, bnh, n, nh, h，总个数为21。
'''
class Solution:
    def countUniqueSubstrings(self, s: str) -> int:
        # 使用滑动窗口方法来计算所有不含重复字符的子串数量

        n = len(s)  # 获取字符串的长度
        left = 0  # 滑动窗口的左边界，初始为0
        unique_substrings_count = 0  # 初始化无重复字符子串的总数
        char_map = {}  # 用于记录每个字符上一次出现的位置

        # 遍历字符串的每一个字符，作为滑动窗口的右边界
        for right in range(n):
            # 如果当前字符已经出现在窗口中，且位置在左边界之后
            if s[right] in char_map and char_map[s[right]] >= left:
                # 更新左边界为重复字符的下一个位置，避免重复
                left = char_map[s[right]] + 1

            # 更新当前字符在字符串中的最新位置
            char_map[s[right]] = right

            # 当前以 right 结尾的不含重复字符的子串数量为 (right - left + 1)
            # 累加到总数量中
            unique_substrings_count += (right - left + 1)

        # 返回无重复字符子串的总个数
        return unique_substrings_count


if __name__ == "__main__":
    # 从标准输入读取字符串并去除首尾空白字符
    s = input().strip()

    # 创建 Solution 类的实例
    solution = Solution()

    # 调用 countUniqueSubstrings 方法计算结果
    result = solution.countUniqueSubstrings(s)

    # 输出最终结果
    print(result)
