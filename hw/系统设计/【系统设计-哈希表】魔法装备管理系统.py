from typing import List, Tuple

class MagicDeviceMgtSystem:
    def __init__(self, proc_num: int, max_mem_size: int):
        # 初始化魔法设备管理系统
        # proc_num: 处理器数量
        # max_mem_size: 每个处理器的最大内存容量
        # rest: 记录每种处理器剩余的内存情况，初始为每个处理器都具有最大内存
        self.rest = [[max_mem_size for _ in range(proc_num)] for _ in range(3)]
        # device_info: 用于存储设备的状态信息，key是设备ID，value是[proc_id, mem_size, device_type]
        self.device_info = dict()

    def create_device(self, device_id: int, device_type: int, mem_size: int) -> int:
        # 创建一个新的设备，分配内存并选择一个处理器
        # device_id: 设备的唯一标识符
        # device_type: 设备类型（1、2、3），会被减去1变为索引 0、1、2
        # mem_size: 设备需要的内存大小
        
        device_type -= 1  # 设备类型从1开始，减1转换为索引0、1、2
        rest = self.rest[device_type]  # 获取对应类型设备的剩余内存列表
        proc_id = 0  # 假设设备最初会分配给第一个处理器
        for i in range(len(rest)):
            # 寻找剩余内存最多的处理器
            if rest[i] > rest[proc_id]:
                proc_id = i
        # 如果选择的处理器的剩余内存小于设备需要的内存，则无法分配
        if rest[proc_id] < mem_size:
            return -1  # 返回-1表示内存不足，无法创建设备
        
        # 将设备分配到处理器
        rest[proc_id] -= mem_size
        # 将设备的状态信息记录在device_info字典中
        self.device_info[device_id] = [proc_id, mem_size, device_type]
        return proc_id  # 返回分配的处理器ID

    def delete_device(self, device_id: int) -> bool:
        # 删除设备并释放内存
        # device_id: 需要删除的设备的唯一标识符
        if device_id not in self.device_info.keys():
            # 如果设备不存在，返回False
            return False
        else:
            # 获取设备的状态信息
            proc_id, mem_size, device_type = self.device_info[device_id]
            # 删除设备信息
            self.device_info.pop(device_id)
            # 释放设备占用的内存
            self.rest[device_type][proc_id] += mem_size
            return True  # 返回True表示删除成功

    def query_device(self, device_type: int) -> List[Tuple[int, int, int]]:
        # 查询设备信息，按照特定规则排序
        # device_type: 查询的设备类型（1、2、3），会被减去1变为索引 0、1、2
        device_type -= 1  # 设备类型从1开始，减1转换为索引0、1、2
        # 筛选出所有该类型的设备信息，按照设备ID、内存大小和处理器ID排序
        info = [
            (device_id, mem_size, proc_id) for (device_id, (proc_id, mem_size, tmp_device_type)) in
            self.device_info.items() if tmp_device_type == device_type
        ]
        # 按照内存大小（降序），处理器ID（升序），设备ID（升序）排序
        info.sort(key=lambda v: (-v[1], v[2], v[0]))
        return info  # 返回查询结果，包含设备ID、内存大小和处理器ID

# 系统初始化和命令输入处理
system = None
Q = int(input())
for i in range(Q):
    cmd = input()
    if i == 0 and cmd == "MagicDeviceMgtSystem":
        proc_num = int(input())
        max_mem_size = int(input())
        system = MagicDeviceMgtSystem(proc_num, max_mem_size)
        print("null")
    elif i > 0 and cmd == 'create_device':
        device_id = int(input())
        device_type = int(input())
        mem_size = int(input())
        print(system.create_device(device_id, device_type, mem_size))
    elif i > 0 and cmd == "delete_device":
        device_id = int(input())
        print(system.delete_device(device_id))
    elif i > 0 and cmd == "query_device":
        device_type = int(input())
        ans = system.query_device(device_type)
        for u in ans:
            print(*u)
    else:
        assert False