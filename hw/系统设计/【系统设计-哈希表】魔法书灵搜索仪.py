from typing import List

class SearchEngine:
    def __init__(self):
        # 用于维护书籍ID和其对应绑定的关键词集合
        self.book_keywords = {}  # 字典：书籍ID -> 关键词集合（set）

    def addWord(self, book_id: int, words: List[str]) -> int:
        # 如果当前书籍ID尚未被登记，则创建一个新的关键词集合
        if book_id not in self.book_keywords:
            self.book_keywords[book_id] = set()
        # 将新关键词加入该书籍的关键词集合（自动去重）
        self.book_keywords[book_id].update(words)
        # 返回该书籍当前绑定的关键词总数
        return len(self.book_keywords[book_id])

    def delWord(self, book_id: int, words: List[str]) -> int:
        # 如果该书籍ID未登记，直接返回0
        if book_id not in self.book_keywords:
            return 0
        # 从该书籍的关键词集合中移除指定的关键词（若不存在自动忽略）
        self.book_keywords[book_id].difference_update(words)
        # 如果删除后该书籍没有任何关键词了，则将该书籍从系统中移除
        if not self.book_keywords[book_id]:
            del self.book_keywords[book_id]
        # 返回该书籍当前绑定的关键词数量，若已删除返回0
        return len(self.book_keywords.get(book_id, set()))

    def query(self, words: List[str]) -> List[int]:
        # 结果列表用于收集满足条件的书籍ID
        result = []
        # 遍历所有登记的书籍ID，按升序排列
        for book_id in sorted(self.book_keywords.keys()):
            # 如果该书籍的关键词集合包含所有查询关键词，则加入结果
            if all(word in self.book_keywords[book_id] for word in words):
                result.append(book_id)
        # 若无满足条件的书籍，则返回 [-1]；否则返回结果列表
        return result if result else [-1]
    
    def query2(self, words: List[str]) -> List[int]:
        words = set(words)
        result = []
        for book_id in sorted(self.book_keywords.keys()):
            if self.book_keywords[book_id] & words == words:
                result.append(book_id)
        return result
        
# 主逻辑入口
system = None  # 初始化搜索系统对象
Q = int(input())  # 输入操作的总次数
for i in range(Q):
    cmd = input().strip()  # 读取当前操作指令
    if i == 0 and cmd == "SearchEngine":
        # 第一个命令必须是 SearchEngine，用于系统初始化
        system = SearchEngine()
        print("null")  # 输出 "null" 表示系统已初始化
    elif i > 0 and cmd == "addWord":
        # 添加关键词操作
        book_id = int(input().strip())  # 读取书籍ID
        word_count = int(input().strip())  # 读取关键词个数（可忽略）
        words = input().strip().split()  # 读取所有关键词
        print(system.addWord(book_id, words))  # 执行添加操作并输出当前关键词总数
    elif i > 0 and cmd == "delWord":
        # 删除关键词操作
        book_id = int(input().strip())  # 读取书籍ID
        word_count = int(input().strip())  # 读取待删除关键词个数（可忽略）
        words = input().strip().split()  # 读取所有待删除关键词
        print(system.delWord(book_id, words))  # 执行删除操作并输出当前关键词总数
    elif i > 0 and cmd == "query":
        # 查询操作
        word_count = int(input().strip())  # 读取查询关键词个数（可忽略）
        words = input().strip().split()  # 读取所有查询关键词
        ans = system.query(words)  # 执行查询操作
        print(*ans)  # 输出满足条件的书籍ID，空格分隔；若无结果输出 -1
    else:
        # 若指令格式错误，则触发断言错误
        assert False
