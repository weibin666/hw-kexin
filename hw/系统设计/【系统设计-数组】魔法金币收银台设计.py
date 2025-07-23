class MagicCashRegister:
    def __init__(self, initGolds: list):
        # 面额列表，从小到大：1、5、10、50、100卢比
        self.denomination = [1, 5, 10, 50, 100]
        # 初始化收银台的金币数量
        self.golds = initGolds

    def processTransaction(self, price: int, paidGolds: list) -> list:
        m = len(paidGolds)  # 面额种类数量，等于5
        # 计算顾客支付的总金额
        paid = sum(self.denomination[i] * paidGolds[i] for i in range(m))

        # 如果顾客支付的金额小于商品价格，交易失败，返回 -1
        if paid < price:
            return [-1]

        # 计算找零金额
        rest = paid - price

        # 计算交易后收银台拥有的金币数（包含顾客支付的金币）
        now = [self.golds[i] + paidGolds[i] for i in range(m)]

        # 初始化找零的金币列表，记录每种面额找出的数量
        result = [0 for _ in range(m)]

        # 从大面额开始优先找零（面值大的金币优先使用）
        for i in range(m - 1, -1, -1):
            # 当前面额最多能用多少枚来找零
            mn = min(now[i], rest // self.denomination[i])
            # 从找零金额中减去这些面额总值
            rest -= mn * self.denomination[i]
            # 记录找零中该面额金币的数量
            result[i] = mn
            # 更新收银台中该面额金币数量
            now[i] -= mn

        # 如果还有剩余找不开，返回 -2，表示无法找零
        if rest > 0:
            return [-2]

        # 找零成功，更新收银台金币数量
        self.golds = now
        return result


system = None  # 初始化收银台系统对象
Q = int(input())  # 读取交易次数

for i in range(Q):
    cmd = input()  # 读取当前操作指令

    # 初始化收银台系统
    if i == 0 and cmd == "MagicCashRegister":
        initGolds = list(map(int, input().split()))  # 读取初始金币数量
        system = MagicCashRegister(initGolds)  # 创建系统对象
        print("null")  # 初始化不输出任何金币找零信息

    # 处理一笔交易
    elif cmd == 'processTransaction':
        price = int(input())  # 读取商品价格
        paidGolds = list(map(int, input().split()))  # 读取顾客支付的金币数量
        result = system.processTransaction(price, paidGolds)  # 执行交易
        print(*result)  # 输出找零结果或失败信息

    else:
        # 如果出现未知命令，断言异常（此处用于调试）
        assert False
