'''
题目描述
在魔法世界的辉煌之都，魔导士协会颁发了一系列魔法学徒编号。但由于魔法干扰，这些编号变得杂乱无章，亟需整理。
请你帮助协会判断哪些编号是合法的，并对合法的编号进行格式化。
合法魔法学徒编号规则：
- 去除所有空格后，编号长度不超过9。
- 首字符必须是字母，其余字符均为数字（至少包含一个数字）。
格式化要求（格式化后示例：a00012345）：
- 编号首字母统一规整成小写字符。
- 去除所有空格。
- 若编号长度不足9位，在数字前面补零，使编号长度恰好为9。
请对格式化后的合法编号去重后，按照字典序升序输出。
输入格式
第一行包含一个整数 N，表示待整理的编号个数，取值范围：1 <= N < 100。
接下来 N 行，每行包含一个字符串，表示待整理的魔法学徒编号（长度不超过 20）。
输出格式
按照字典序升序输出规整后的合法编号，每个编号占一行。
样例
样例1
样例输入：
8
ss789
12n00
s00123
k2 3490
S123
s234
x235
m990
样例输出：
k00023490
m00000990
s00000123
s00000234
x00000235
样例说明：
- 12n00 非法，丢弃。
- S00123 和 S123 经过格式化后相同，去重。
- 字典序排序即按照首字母排序，若首字母相同则比较后续字符，类似于字典查找顺序。

'''
class Solution:
    def regular_id(self, card_ids):
        # 使用集合来存储合法且格式化后的学徒编号，自动去重
        valid_ids = set()

        # 遍历每一个待整理的编号
        for card_id in card_ids:
            # 去除编号中的所有空格
            card_id = card_id.replace(" ", "")

            # 检查编号是否合法：
            # - 长度不超过9
            # - 首字符必须是字母
            # - 首字符后至少包含一个数字
            # - 且首字符之后的所有字符必须是数字
            if len(card_id) > 9 or not card_id[0].isalpha() or not any(c.isdigit() for c in card_id[1:]) or not all(
                    c.isdigit() for c in card_id[1:]):
                continue  # 如果不合法，则跳过当前编号

            # 将首字母统一转换为小写，符合格式化要求
            card_id = card_id[0].lower() + card_id[1:]

            # 提取首字母后的数字部分，并在左侧补零，使其总长度为8位
            num_part = card_id[1:].zfill(8)

            # 将格式化后的编号拼接起来（1个小写字母 + 8位数字），总长度为9位
            formatted_id = card_id[0] + num_part

            # 将合法格式化后的编号加入集合，自动去重
            valid_ids.add(formatted_id)

        # 将所有合法编号按字典序排序后返回
        return sorted(valid_ids)


if __name__ == "__main__":
    # 读取输入的编号数量
    count = int(input().strip())

    # 读取每一行编号输入，构成一个列表
    card_ids = [input().strip() for _ in range(count)]

    # 创建类对象并调用处理函数
    function = Solution()
    result = function.regular_id(card_ids)

    # 按行输出处理结果
    print('\n'.join(result))

