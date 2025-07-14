'''
题目描述
在魔法世界的网络中，存在着一些特别的魔法IP地址。每个IP地址由四段数字组成，每一段数字有三种特殊的表现形式。
第一种表现形式：正常整数形式
例如，9.18.27.36，表示这是一个正常的整数。
第二种表现形式：区间形式，用 [] 括起
例如，9.18.27.[34,36]，表示这一段IP地址可以展开为多个IP地址，从 34 到 36，即：9.18.27.34、9.18.27.35、9.18.27.36。
第三种表现形式：集合形式，用 {} 括起
例如，9.18.27.{36,45}，表示这一段IP地址可以是 36 或 45，即：9.18.27.36 和 9.18.27.45。
你需要将这些特殊的IP地址字符串转换成标准的IP地址形式，并按字典序升序排列输出。每个分量的字典序应按照数字的大小进行排序。例如：
- 19.255.0.0 大于 19.6.0.0，因为 255 大于 6。
注意：输出结果的数量不会超过10000个。
输入格式
- 输入一个IP地址字符串，包含四段，每段可能包含上述三种表现形式之一。
输出格式
- 输出所有合法的IP地址字符串，按字典序升序排列，每行输出一个IP地址。
样例
样例1
样例输入：
9.18.27.36
样例输出：
9.18.27.36
样例2
样例输入：
9.18.27.[34,36]
样例输出：
9.18.27.34
9.18.27.35
9.18.27.36
样例3
样例输入：
9.18.27.{36,45}
样例输出：
9.18.27.36
9.18.27.45
'''
class Solution:
    def generate_ip_addresses(self, ip_str: str):
        # 将输入的IP地址字符串按点号'.'进行分割，得到四段IP分量
        segments = ip_str.split('.')

        # 创建一个二维列表，每个元素是当前段所有可能的整数值
        possibilities = []

        # 遍历每一段分量，解析其具体的形式
        for segment in segments:
            if '[' in segment:  # 如果包含 '['，说明是区间形式 [a,b]
                start = segment.index('[')          # 找到 '[' 的索引位置
                end = segment.index(']')            # 找到 ']' 的索引位置
                range_str = segment[start + 1:end]  # 提取中括号内的字符串，例如 "34,36"
                range_vals = list(map(int, range_str.split(',')))  # 将字符串转换为整数列表 [34, 36]
                # 生成闭区间 [34, 36] 对应的所有整数 [34, 35, 36]
                possibilities.append(list(range(range_vals[0], range_vals[1] + 1)))
            elif '{' in segment:  # 如果包含 '{'，说明是集合形式 {x,y,z}
                start = segment.index('{')          # 找到 '{' 的索引
                end = segment.index('}')            # 找到 '}' 的索引
                set_str = segment[start + 1:end]    # 提取大括号内的字符串，例如 "36,45"
                # 将字符串切分并转换为整数，并按数值升序排序
                set_vals = sorted(map(int, set_str.split(',')))
                possibilities.append(set_vals)      # 加入集合形式的所有取值
            else:  # 普通整数形式
                possibilities.append([int(segment)])  # 单个数字也转成一个列表，例如 [9]

        # 用于存储最终生成的所有合法IP地址字符串
        result = []

        # 定义回溯函数，用于递归地生成所有可能的IP地址
        def backtrack(index, current_ip):
            if index == 4:
                # 当四段都处理完毕时，将当前IP拼接成字符串形式并加入结果中
                result.append(".".join(str(x) for x in current_ip))
                return

            # 遍历当前段的所有可能取值，递归生成下一段
            for value in possibilities[index]:
                current_ip.append(value)        # 选择当前值
                backtrack(index + 1, current_ip)  # 递归处理下一段
                current_ip.pop()                # 回溯，撤销选择

        # 从第0段开始回溯生成
        backtrack(0, [])

        # 最终返回生成的IP地址结果（已保证每段排序，因此整体排序可省略）
        return result


if __name__ == "__main__":
    # 从标准输入读取一行IP地址字符串，并去除首尾空白字符
    ip_str = input().strip()

    # 创建 Solution 实例，并调用方法生成IP地址结果
    solution = Solution()
    result = solution.generate_ip_addresses(ip_str)

    # 按行打印所有生成的合法IP地址
    for ip in result:
        print(ip)

