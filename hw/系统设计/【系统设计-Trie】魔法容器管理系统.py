# 定义字典树（Trie）中的每个节点结构
class TrieNode:
    def __init__(self):
        self.children = {}  # 存储子节点，键为字符，值为对应的 TrieNode
        self.is_end_of_word = False  # 标记该节点是否是某个完整单词的结尾
        self.cnt = 0  # 表示以该节点为路径前缀的单词数量（用于删除时判断是否可清除）

# 定义魔法容器类
class MagicContainer:
    def __init__(self):
        self.root = TrieNode()  # 初始化 Trie 的根节点
        self.size = 0  # 当前容器中咒语的数量

    def add(self, keyword: str) -> int:
        """
        向容器中添加一个魔法咒语 keyword。
        如果该咒语已存在，返回当前咒语数量；
        如果是新咒语，则插入并返回添加后的数量。
        """
        node = self.root
        # 遍历 keyword 的每个字符，构建 Trie 路径
        for ch in keyword:
            if ch not in node.children:
                node.children[ch] = TrieNode()  # 如果当前字符不存在，则创建新节点
            node = node.children[ch]

        # 如果当前单词已经存在（已是某个单词的结尾）
        if node.is_end_of_word:
            return self.size  # 不再插入，直接返回当前数量

        # 重新从根节点走一遍路径，增加路径上每个节点的计数 cnt
        node = self.root
        for ch in keyword:
            node = node.children[ch]
            node.cnt += 1  # 当前节点的前缀引用数加1

        node.is_end_of_word = True  # 将最后一个节点标记为单词结尾
        self.size += 1  # 容器中咒语数量加1
        return self.size

    def remove(self, keyword: str) -> int:
        """
        从容器中删除指定魔法咒语 keyword。
        若删除成功，返回删除后的容器大小；
        若咒语不存在，返回 -1。
        """
        node = self.root
        stack = []  # 用于记录路径，方便回溯删除

        # 遍历 keyword，查找路径是否存在
        for ch in keyword:
            if ch not in node.children:
                return -1  # 若路径不存在，说明该咒语未插入过
            stack.append((node, ch))  # 记录路径
            node = node.children[ch]

        # 如果最后一个节点不是单词结尾，说明该词不存在
        if not node.is_end_of_word:
            return -1

        node.is_end_of_word = False  # 取消单词结束标记
        self.size -= 1  # 容器数量减少

        # 从路径回溯，更新 cnt 并删除无用节点
        for parent, ch in reversed(stack):
            node.cnt -= 1  # 当前节点的前缀引用数减1
            if node.cnt == 0:  # 若 cnt 为 0，说明无其他路径使用
                del parent.children[ch]  # 删除该子节点
            node = parent  # 回溯上一层节点

        return self.size  # 返回更新后的容器大小

    def filter(self, sentence: str) -> str:
        """
        进行前缀匹配操作，找到所有咒语中能匹配 sentence 前缀的项，
        删除其中字典序最小的匹配项并返回其字符串。
        若无匹配，则返回 -1。
        """
        node = self.root
        stack = []  # 用于记录前缀路径

        # 逐个字符匹配 sentence，如果中断则说明无匹配项
        for ch in sentence:
            if ch not in node.children:
                return "-1"  # 没有任何匹配的前缀
            stack.append((node, ch))  # 记录路径
            node = node.children[ch]

        ls = list(sentence)  # 当前已匹配的前缀字符列表

        # 如果当前前缀不是完整单词，继续深入找字典序最小的补全
        while not node.is_end_of_word:
            ch = min(node.children.keys())  # 选择字典序最小的子节点字符
            ls.append(ch)  # 补全到匹配的完整咒语
            stack.append((node, ch))  # 记录路径
            node = node.children[ch]

        node.is_end_of_word = False  # 删除该单词
        self.size -= 1  # 数量减少

        # 回溯路径，更新引用计数并删除无用节点
        for parent, ch in reversed(stack):
            node.cnt -= 1
            if node.cnt == 0:
                del parent.children[ch]
            node = parent

        return "".join(ls)  # 返回被删除的咒语

# 主程序入口
system = None  # 初始化全局变量，表示魔法容器未建立
Q = int(input())  # 输入操作次数

# 逐行处理每条指令
for i in range(Q):
    cmd = input()  # 读取当前指令
    if i == 0 and cmd == "MagicContainer":
        print("null")  # 初始化输出 null
        system = MagicContainer()  # 初始化魔法容器
    elif cmd == 'add':
        keyword = input()  # 读取咒语
        print(system.add(keyword))  # 输出添加后容器中咒语数量
    elif cmd == 'remove':
        keyword = input()  # 读取要删除的咒语
        print(system.remove(keyword))  # 输出删除结果
    elif cmd == "filter":
        sentence = input()  # 读取要匹配的前缀
        print(system.filter(sentence))  # 输出删除的匹配咒语或 -1
    else:
        assert False  # 若出现未定义指令，触发断言错误
