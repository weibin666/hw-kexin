from collections import defaultdict, deque
from typing import List

# 定义魔法系统的主类
class ServiceWgSys:
    def __init__(self):
        # 构建依赖图 g，g[A] 表示 A 依赖的所有服务集合
        self.g = defaultdict(set)
        # id2name 记录每个服务器上正在运行的服务名集合
        self.id2name = defaultdict(set)
        # name_cnt 记录每个服务当前总共运行的分身数量（在所有服务器上的总数）
        self.name_cnt = defaultdict(int)

    # 在指定服务器上启动指定服务
    def startService(self, serverId: int, serviceName: str) -> bool:
        # 如果该服务已在该服务器上运行，则不能重复启动，返回 False
        if serviceName in self.id2name[serverId]:
            return False
        # 否则将服务名加入该服务器的运行服务集合
        self.id2name[serverId].add(serviceName)
        # 同时该服务的总运行实例数加一
        self.name_cnt[serviceName] += 1
        return True

    # 添加服务依赖关系：fromService 依赖 toService
    def addDependency(self, fromService: str, toService: str) -> bool:
        # 如果依赖关系已存在，返回 False
        if toService in self.g[fromService]:
            return False
        # 否则添加依赖边 fromService -> toService
        self.g[fromService].add(toService)
        return True

    # 查询某个服务当前是否可释放魔力（即是否“可用”）
    def isServiceAvailable(self, serviceName: str) -> bool:
        # 使用队列进行 BFS 遍历依赖图
        q = deque([serviceName])
        # vis 记录访问过的服务，避免重复遍历
        vis = {serviceName}
        while q:
            u = q.popleft()  # 当前服务
            # 若当前服务没有任何实例在运行，则无法释放魔力
            if self.name_cnt[u] == 0:
                return False
            # 遍历所有被依赖的服务
            for v in self.g[u]:
                if v not in vis:
                    vis.add(v)
                    q.append(v)
        # 所有依赖的服务都可用，且当前服务有实例运行，返回 True
        return True

    # 重启服务器列表，服务器上的所有服务实例都会熄灭
    def rebootServers(self, serverIds: List[int]):
        for id in serverIds:
            # 遍历该服务器上所有运行的服务，将对应服务总运行数量减一
            for name in self.id2name[id]:
                self.name_cnt[name] -= 1
            # 清空该服务器上的所有服务记录
            self.id2name.pop(id, None)


# 处理输入命令
system = None  # 初始化魔法系统实例
Q = int(input())  # 输入命令总数
for i in range(Q):
    cmd = input().strip()  # 读取当前命令

    # 第一条命令只能是初始化系统
    if i == 0 and cmd == "ServiceWgSys":
        system = ServiceWgSys()
        print("null")
    elif cmd == "startService":
        # 启动服务命令：读取服务器编号和服务名
        serverId = int(input())
        serviceName = input().strip()
        print(system.startService(serverId, serviceName))  # 输出 True/False
    elif cmd == "addDependency":
        # 添加依赖命令：读取两个服务名
        fromService = input().strip()
        toService = input().strip()
        print(system.addDependency(fromService, toService))  # 输出 True/False
    elif cmd == "isServiceAvailable":
        # 查询服务是否可用
        serviceName = input().strip()
        print(system.isServiceAvailable(serviceName))  # 输出 True/False
    elif cmd == "rebootServers":
        # 重启服务器命令：读取重启服务器的数量和对应编号
        n = int(input())
        serverIds = list(map(int, input().split()))
        system.rebootServers(serverIds)  # 执行重启
        print("null")
    else:
        # 如果输入命令不合法，抛出异常
        raise ValueError(f"Unknown command: {cmd}")
