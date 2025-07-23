from typing import List

class MagicContainerSystem:
    M = 30  # 每个容器有 30 个端口

    def __init__(self, container_ids: List[int]):
        """
        初始化魔法容器系统。
        每个容器用一个列表表示端口使用情况，-1 表示端口空闲。
        同时维护一个业务到容器及端口信息的映射。
        """
        self.mp = {}  # 容器ID -> 对应端口状态数组（长度为30，初始为全-1）
        self.task2container = {}  # 业务ID -> [容器ID, 起始端口下标, 占用长度]
        for cid in container_ids:
            self.mp[cid] = [-1 for _ in range(self.M)]  # 初始化每个容器的端口列表为全空闲

    def add(self, cid: int, bid: int, startport: int, level: int) -> int:
        """
        向容器 cid 中添加业务 bid，从 startport 开始占用 level 个连续端口。
        若 startport 为 0 表示自动分配。
        返回：成功绑定的起始端口（从1开始），失败返回 -1。
        """
        if cid not in self.mp.keys() or bid in self.task2container.keys():
            return -1  # 容器不存在 或 任务已存在

        v = self.mp[cid]  # 获取该容器的端口状态列表
        startport -= 1    # 转换为0-based索引

        if startport != -1:
            # 若提供了具体起始端口，检查合法性和是否空闲
            if startport % level == 0 and all(v[startport + j] == -1 for j in range(level)):
                for j in range(level):
                    v[startport + j] = bid  # 标记该业务占用这些端口
                self.task2container[bid] = [cid, startport, level]  # 记录业务信息
                return startport + 1  # 返回从1开始的端口编号
        else:
            # 自动分配起始端口（仅适用于 level=1）
            for st in range(0, self.M, level):  # 每 level 个端口检查一次
                if all(v[st + j] == -1 for j in range(level)):
                    for j in range(level):
                        v[st + j] = bid  # 标记业务占用
                    self.task2container[bid] = [cid, st, level]  # 记录业务信息
                    return st + 1  # 返回实际起始端口
        return -1  # 无法绑定

    def remove(self, bids: List[int]) -> int:
        """
        删除一组业务编号所对应的业务。
        返回成功删除的业务数量。
        """
        ans = 0
        for bid in bids:
            if bid in self.task2container:
                cid, st, level = self.task2container[bid]  # 获取该业务绑定信息
                for j in range(level):
                    self.mp[cid][st + j] = -1  # 清除容器中对应端口的业务标记
                ans += 1
                self.task2container.pop(bid)  # 删除业务记录
        return ans

    def query(self, cid: int) -> List[int]:
        """
        查询容器 cid 中的所有业务。
        返回业务 ID 列表，按以下顺序排序：
        - level 降序
        - startport 升序
        - bid 升序
        若该容器没有业务，返回 [-1]
        """
        bid_set = {x for x in self.mp[cid] if x != -1}  # 提取所有业务ID（去重）
        if len(bid_set) == 0:
            return [-1]  # 无业务
        # 按规则排序
        bids = sorted(
            bid_set,
            key=lambda bid: (-self.task2container[bid][2], self.task2container[bid][1], bid)
        )
        return bids

    def free(self, cid: int) -> int:
        """
        清除容器 cid 中的所有业务，释放所有端口。
        返回被释放的业务数量。
        """
        bid_set = {x for x in self.mp[cid] if x != -1}  # 获取当前容器绑定的业务
        for bid in bid_set:
            self.task2container.pop(bid)  # 删除业务记录
        self.mp[cid] = [-1 for _ in range(self.M)]  # 清空容器端口状态
        return len(bid_set)


# 主程序部分，处理交互式输入
system = None
Q = int(input())  # 操作总数
for i in range(Q):
    cmd = input()
    if i == 0 and cmd == "MagicContainerSystem":
        # 初始化系统
        n = int(input())  # 容器数量
        container_ids = list(map(int, input().split()))  # 容器ID列表
        system = MagicContainerSystem(container_ids)
        print("null")
    elif i > 0 and cmd == 'add':
        # 添加业务
        cid = int(input())
        bid = int(input())
        startport = int(input())
        level = int(input())
        print(system.add(cid, bid, startport, level))
    elif i > 0 and cmd == "remove":
        # 删除业务
        m = int(input())
        bids = list(map(int, input().split()))
        print(system.remove(bids))
    elif i > 0 and cmd == "query":
        # 查询容器业务
        cid = int(input())
        res = system.query(cid)
        print(*res)
    elif i > 0 and cmd == "free":
        # 清空容器
        cid = int(input())
        print(system.free(cid))
    else:
        # 非法指令
        assert False
