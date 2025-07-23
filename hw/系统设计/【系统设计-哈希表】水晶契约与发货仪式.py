from typing import List

class MagicOrderSystem:
    def __init__(self):
        # 初始化魔法订单系统
        # orders 字典用于存储每个wizard_id的订单，键是wizard_id，值是一个包含已下订单的物品集合
        self.orders = {}

    def place_order(self, wizard_id: int, items: List[int]) -> int:
        # 创建一个新的订单或更新已有订单
        # wizard_id: 法师的唯一标识符
        # items: 该法师下单的物品列表
        
        # 如果该法师的订单还不存在，则为其创建一个空集合
        if wizard_id not in self.orders:
            self.orders[wizard_id] = set()
        
        # 更新该法师的订单，添加新的物品（集合会自动去重）
        self.orders[wizard_id].update(items)
        
        # 返回该法师当前拥有的物品数量
        return len(self.orders[wizard_id])

    def deliver_item(self, item_type: int) -> int:
        # 交付一个特定类型的物品给所有下过订单的法师
        # item_type: 需要交付的物品类型
        
        cnt = 0  # 记录交付成功的法师数量
        # 遍历所有法师的订单，检查是否有该物品
        for wizard_id in self.orders.keys():
            # 如果法师下单了该物品
            if item_type in self.orders[wizard_id]:
                # 从该法师的订单中移除该物品
                self.orders[wizard_id].remove(item_type)
                # 增加交付成功的法师数量
                cnt += 1
        
        # 返回交付成功的法师数量
        return cnt

    def query_status(self) -> List[int]:
        # 查询所有法师的订单状态
        # 返回一个排序后的法师ID列表，按照法师订单中物品数量的降序排列，
        # 如果物品数量相同，则按照法师ID升序排列
        
        result = []  # 存储法师订单状态的列表
        for wizard_id, items in self.orders.items():
            # 将每个法师的ID和物品数量（len(items)）作为一个元组添加到结果列表
            result.append((wizard_id, len(items)))
        
        # 按照物品数量降序排列，如果数量相同则按照法师ID升序排列
        result.sort(key=lambda x: (-x[1], x[0]))
        
        # 返回排序后的法师ID列表
        return [v[0] for v in result]


# 系统初始化和命令输入处理
system = None  # 用于存储MagicOrderSystem的实例
Q = int(input())  # 读取输入的命令数量
for i in range(Q):
    cmd = input()  # 读取命令
    if i == 0 and cmd == "MagicOrderSystem":
        # 如果是第一次命令，创建一个新的MagicOrderSystem对象
        system = MagicOrderSystem()
        print("null")  # 初始化时输出 "null"
    elif i > 0 and cmd == 'place_order':
        # 如果命令是下单
        wizard_id = int(input())  # 读取法师ID
        items_size = int(input())  # 读取物品数量（实际上不需要用到，直接读取物品列表即可）
        items = list(map(int, input().split()))  # 读取物品列表
        print(system.place_order(wizard_id, items))  # 输出下单后该法师拥有的物品数量
    elif i > 0 and cmd.startswith("deliver_item"):
        # 如果命令是交付物品
        item_type = int(input())  # 读取物品类型
        print(system.deliver_item(item_type))  # 输出交付物品的法师数量
    elif i > 0 and cmd == "query_status":
        # 如果命令是查询法师状态
        print(*system.query_status())  # 输出查询后的法师ID列表
    else:
        # 如果命令无效，抛出异常
        assert False
