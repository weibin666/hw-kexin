from typing import List, Tuple

# 定义“魔法租房系统”类
class RentingSystem:
    def __init__(self):
        """
        初始化租房系统，使用一个字典存储所有房源信息，key 是房源 id，value 是房源元组。
        """
        self.rooms = {}

    def addRoom(self, id: int, area: int, price: int, rooms: int, address: List[int]) -> bool:
        """
        添加房源信息，如果房源 id 不存在，则添加并返回 True；否则更新信息并返回 False。

        :param id: 房源编号
        :param area: 房源面积
        :param price: 月租金
        :param rooms: 卧室数量
        :param address: 房源地址坐标 [x, y]
        :return: 是否为新添加（True）或更新（False）
        """
        if id in self.rooms:
            # 若房源已存在，则更新其信息
            self.rooms[id] = (area, price, rooms, address)
            return False
        else:
            # 房源不存在则添加新房源
            self.rooms[id] = (area, price, rooms, address)
            return True

    def deleteRoom(self, id: int) -> bool:
        """
        删除指定编号的房源。

        :param id: 要删除的房源编号
        :return: 删除成功返回 True，否则返回 False
        """
        if id in self.rooms:
            # 若房源存在，删除之
            del self.rooms[id]
            return True
        else:
            # 房源不存在
            return False

    def queryRoom(self, area: int, price: int, rooms: int, address: List[int], orderBy: List[List[int]]) -> List[int]:
        """
        查询满足条件的房源，并按照给定的排序方式返回结果。

        :param area: 最小面积
        :param price: 最大价格
        :param rooms: 精确的卧室数量
        :param address: 查询位置坐标，用于计算曼哈顿距离
        :param orderBy: 排序条件，每个元素为 [字段编号, 顺序]，字段编号：1=面积，2=价格，3=距离；顺序：1=升序，-1=降序
        :return: 符合条件房源的 ID 列表，按排序顺序返回，若无符合条件房源则返回 [-1]
        """
        filtered_rooms = []  # 存储筛选出的房源信息
        for room_id, (room_area, room_price, room_rooms, room_address) in self.rooms.items():
            # 筛选条件：面积不小于给定值，价格不大于给定值，卧室数完全相同
            if room_area >= area and room_price <= price and room_rooms == rooms:
                # 计算房源与目标地址的曼哈顿距离
                manhattan_distance = abs(room_address[0] - address[0]) + abs(room_address[1] - address[1])
                # 保存筛选通过的房源信息
                filtered_rooms.append((room_id, room_area, room_price, manhattan_distance, room_address))

        # 构造排序 key 函数
        def room_sort_key(room):
            # 提取排序字段值
            sorting_params = {
                1: room[1],  # 面积
                2: room[2],  # 价格
                3: room[3],  # 曼哈顿距离
            }

            sort_key = []
            for param, order in orderBy:
                key = sorting_params[param]
                if order == -1:
                    key = -key  # 若降序，则将 key 取反实现逆序排列
                sort_key.append(key)

            # 添加 room_id 作为最终排序的 tie-breaker（确保稳定性）
            sort_key.append(room[0])

            return sort_key

        # 对房源信息进行排序
        filtered_rooms.sort(key=room_sort_key)

        # 提取排序后的房源 id
        sorted_room_ids = [room[0] for room in filtered_rooms]
        if len(sorted_room_ids) == 0:
            return [-1]  # 无符合条件房源，返回 [-1]
        return sorted_room_ids

# 主流程：按题目要求进行命令解析与执行
system = None  # 系统对象初始为 None
Q = int(input())  # 读取操作总数 Q

for i in range(Q):
    cmd = input()  # 读取当前操作命令

    if i == 0 and cmd == "RentingSystem":
        # 第一个命令必须为初始化操作
        print("null")
        system = RentingSystem()

    elif cmd == "addRoom":
        # 添加房源：读取各项参数
        id = int(input())  # 房源 id
        area = int(input())  # 面积
        price = int(input())  # 价格
        rooms = int(input())  # 卧室数
        address = list(map(int, input().split()))  # 地址 [x, y]
        print(system.addRoom(id, area, price, rooms, address))  # 输出添加结果

    elif cmd == "deleteRoom":
        # 删除房源：读取 id 并尝试删除
        id = int(input())
        print(system.deleteRoom(id))

    elif cmd == "queryRoom":
        # 查询房源：读取筛选条件和排序条件
        area = int(input())  # 最小面积
        price = int(input())  # 最大价格
        rooms = int(input())  # 卧室数
        address = list(map(int, input().split()))  # 地址坐标
        orderBy_len = int(input())  # 排序规则数量
        orderBy = []
        for _ in range(orderBy_len):
            parameter, order = map(int, input().split())  # 每个排序字段及顺序
            orderBy.append([parameter, order])
        ans = system.queryRoom(area, price, rooms, address, orderBy)
        print(*ans)  # 输出排序结果（空格分隔）

    else:
        # 其他非法命令（防御性编程）
        assert False
