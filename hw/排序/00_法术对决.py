'''
题目描述
在神秘的魔法王国，巫师们参加了一场名为「法术对决」的竞技比赛，每位巫师都会获得一个法术评分。请计算所有巫师法术评分的中位数，并返回法术评分等于中位数的巫师姓名列表。如果有多人符合要求，则按照输入顺序的逆序输出。
中位数的定义如下：
- 如果数据的个数是奇数，则中位数是排序后居中位置的那个数。
- 如果数据的个数是偶数，则中位数是排序后中间两个数中较小的那个数。
输入格式
第一行包含一个整数 num，表示巫师的人数，满足 1 <= num <= 100。
接下来的 num 行，每行包含两个部分：
- name（字符串），表示巫师的名字，仅由英文字母和数字组成，长度在 [1,15] 之间，且不重复。
- score（整数），表示巫师的法术评分，范围为 [0,100]。
输出格式
输出分数等于中位数的巫师姓名列表，巫师之间以单个空格分隔，按照输入顺序的逆序排列。
样例
样例1
样例输入：
5
Mage02 34
Sorcerer01 32
Wizard03 34
Enchanter04 56
Warlock05 79
样例输出：
Wizard03 Mage02
样例说明：
巫师的法术评分排序后为 [32, 34, 34, 56, 79]，中位数是 34。 评分等于 34 的巫师有两人：Mage02 和 Wizard03，按照输入顺序的逆序排列，输出 Wizard03 Mage02。
样例2
样例输入：
4
Apprentice01 10
Invoker1b 10
Conjurer2a 9
Summoner02 9
样例输出：
Summoner02 Conjurer2a
样例说明：
巫师的法术评分排序后为 [9, 9, 10, 10]，中位数是 9。 评分等于 9 的巫师有两人：Conjurer2a 和 Summoner02，按照输入顺序的逆序排列，输出 Summoner02 Conjurer2a。

'''

from typing import List, Tuple


class Solution:
    def get_medium_name_list(self, employee_list: List[Tuple[str, int]]) -> List[str]:
        """
        计算巫师法术评分的中位数，并返回法术评分等于中位数的巫师姓名列表，按照输入顺序的逆序排列。
        :param employee_list: 包含巫师姓名和法术评分的列表。
        :return: 符合中位数条件的巫师姓名列表。
        """
        # 提取所有巫师的法术评分，并按升序排序
        sorted_scores = sorted(x[1] for x in employee_list)

        # 计算中位数的位置
        num = len(sorted_scores)  # 巫师总数
        median_index = (num - 1) // 2  # 计算中位数索引（适用于奇偶情况）
        median_score = sorted_scores[median_index]  # 获取中位数分数

        # 逆序遍历原输入列表，筛选出法术评分等于中位数的巫师姓名
        result = [name for name, score in reversed(employee_list) if score == median_score]

        return result  # 返回符合条件的巫师姓名列表


if __name__ == "__main__":
    # 读取输入的巫师人数
    num = int(input().strip())
    employee_list = []  # 存储巫师的姓名和法术评分

    # 读取每个巫师的姓名和法术评分，并存入列表
    for _ in range(num):
        employee = input().strip().split()  # 按空格拆分输入
        employee_list.append((employee[0], int(employee[1])))  # 将姓名和分数存入列表，分数转换为整数

    # 创建 Solution 类的实例
    function = Solution()
    # 获取符合中位数条件的巫师姓名列表
    results = function.get_medium_name_list(employee_list)
    # 按照题目要求，以空格分隔输出符合条件的巫师姓名
    print(" ".join(results))
