from dataclasses import dataclass
from typing import List
from collections import Counter


# 定义一个 ProductRepos 数据类，用于存储每个产品和它所关联的仓库
@dataclass
class ProductRepos:
    product_id: int  # 产品ID
    repo_ids: List[int]  # 仓库ID列表

# CodeStatsSystem 类，负责统计每个产品的代码行数和语言使用情况
class CodeStatsSystem:
    def __init__(self, products: List[ProductRepos]):
        # 初始化时，我们根据传入的产品列表构建一个仓库到产品的映射
        self.repo_2_product = {}
        # 遍历所有产品及其仓库，将仓库ID映射到产品ID
        for p in products:
            for x in p.repo_ids:
                self.repo_2_product[x] = p.product_id
        # 存储每个产品每种语言的代码行数
        self.cnt = {}

    # 更新某个仓库的代码行数
    def change_code_lines(self, repo_id: int, language_id: int, code_lines: int) -> int:
        # 查找仓库对应的产品ID
        product_id = self.repo_2_product[repo_id]
        # 如果该产品还没有记录，初始化它的计数器
        if product_id not in self.cnt.keys():
            self.cnt[product_id] = Counter()
        # 更新指定语言的代码行数
        self.cnt[product_id][language_id] = self.cnt[product_id][language_id] + code_lines
        # 返回该语言的代码行数
        return self.cnt[product_id][language_id]

    # 获取某个产品的语言统计信息
    def stat_language(self, product_id: int) -> List[int]:
        if product_id == 0:
            # 如果 product_id 为0，表示我们需要统计所有产品的代码行数
            cnt = Counter()
            for c in self.cnt.values():
                cnt.update(c)
        else:
            # 如果指定了具体的产品ID，获取该产品的代码行数
            if product_id not in self.cnt.keys():
                self.cnt[product_id] = Counter()
            cnt = self.cnt[product_id]
            # cnt[key: 语言id,value: 产品下的代码行数]
        # 对统计结果按代码行数降序排列，如果行数相同则按语言ID升序排列
        vec = sorted(cnt.items(), key=lambda t: (-t[1], t[0]))
        # 返回排序后的语言ID列表（只包含行数大于0的语言）
        return [t[0] for t in vec if t[1] > 0]

# 输入处理
Q = int(input())  # 输入查询次数
sol = None  # 用于存储 CodeStatsSystem 的实例
for i in range(Q):
    cmd = input()  # 读取命令
    if i == 0 and cmd == 'CodeStatsSystem':
        # 第一个命令是初始化 CodeStatsSystem
        m = int(input())  # 产品的数量
        products = []
        for _ in range(m):
            product_id = int(input())  # 产品ID
            reop_ids_size = int(input())  # 仓库ID的数量
            repo_ids = list(map(int, input().split()))  # 仓库ID列表
            products.append(ProductRepos(product_id, repo_ids))  # 创建 ProductRepos 对象并添加到列表中
        sol = CodeStatsSystem(products)  # 初始化 CodeStatsSystem 实例
        print("null")  # 对应的输出
    elif i > 0 and cmd == 'change_code_lines':
        # 命令为修改代码行数
        repo_id = int(input())  # 仓库ID
        language_id = int(input())  # 语言ID
        code_lines = int(input())  # 代码行数
        # 调用 change_code_lines 方法并输出结果
        print(sol.change_code_lines(repo_id, language_id, code_lines))
    elif i > 0 and cmd == 'stat_language':
        # 命令为统计语言
        product_id = int(input())  # 产品ID
        # 调用 stat_language 方法并输出结果
        print(*sol.stat_language(product_id))
    else:
        # 如果输入的命令不符合预期，则报错
        assert False

