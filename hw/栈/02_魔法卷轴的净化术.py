'''
题目描述
在奇幻大陆的古老图书馆中，小慕发现了一批被黑暗魔法污染的魔法卷轴。污染的表现形式是：若两个相邻的符文是相同字母但大小写不同（例如 "Aa" 或 "bB"），它们会互相抵消，释放魔力并从卷轴中消失。
为了恢复卷轴原貌，小慕需要你编写一个净化法术，反复移除所有符合条件的相邻字符对，直到无法再继续为止。请你输出最终净化后的卷轴内容。
特别说明：如果卷轴被完全净化为空，请输出 -1。
输入格式
第一行输入一个字符串 inputStr，代表魔法卷轴的原始内容。
- 1 <= inputStr.length <= 10000
- inputStr 仅包含大小写英文字母。
输出格式
输出一个字符串，表示净化后剩余的内容。若最终为空字符串，请输出 -1。
样例
样例1
样例输入：
commMmon
样例输出：
common
样例2
样例输入：
DfFdmM
样例输出：
-1
样例3
样例输入：
i
样例输出：
i

'''


class Solution:
    def purifyScroll(self, inputStr: str) -> str:
        # 初始化一个栈，用于存储尚未被抵消的字符
        stack = []

        # 遍历输入字符串中的每一个字符
        for ch in inputStr:
            # 判断当前字符是否可以与栈顶字符抵消
            # 抵消条件是：两个字符是相同字母但大小写不同（ASCII码差值为32）
            if stack and abs(ord(stack[-1]) - ord(ch)) == 32:
                stack.pop()  # 抵消：将栈顶字符弹出
            else:
                stack.append(ch)  # 无法抵消：将当前字符压入栈中

        # 若栈为空，表示所有字符都被抵消，返回 -1
        # 否则返回栈中剩余的字符组成的字符串，即净化后的结果
        return ''.join(stack) if stack else "-1"


if __name__ == "__main__":
    # 从标准输入读取卷轴字符串，去除前后空格
    inputStr = input().strip()

    # 创建解决方案对象
    sol = Solution()

    # 执行净化法术，获取净化后的卷轴内容
    result = sol.purifyScroll(inputStr)

    # 输出净化结果
    print(result)

