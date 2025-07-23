from typing import List

class MagicService:
    # 初始化函数，接受两个参数：channels 和 charge
    # channels：一个列表，表示不同视频类型可以使用的通道数
    # charge：一个列表，表示不同视频类型的费用
    def __init__(self, channels: List[int], charge: List[int]):
        self.channels = channels  # 记录每种视频类型的通道数
        self.charge = charge      # 记录每种视频类型的收费标准
        # 初始化一个长度为3的列表，每个元素都是一个集合，用于记录不同视频类型已经被预定的通道
        self.booked = [set() for _ in range(3)]

    # 分配通道，time表示当前时间，userId表示用户ID，videoType表示视频类型
    def allocateChannel(self, time: int, userId: int, videoType: int) -> bool:
        # 从视频类型开始尝试分配，优先分配更高视频类型的通道
        for p in range(videoType, 3):
            # 检查当前视频类型的通道是否有空闲
            if len(self.booked[p]) < self.channels[p]:
                # 如果有空闲，预定一个通道，并记录用户的预定信息（时间、用户ID、视频类型）
                self.booked[p].add((time, userId, videoType))
                return True  # 分配成功，返回True
        return False  # 如果没有空闲通道，返回False

    # 释放通道，time表示当前时间，userId表示用户ID
    def freeChannel(self, time: int, userId: int) -> int:
        level = ans = -1  # level记录视频类型，ans记录费用
        # 遍历所有视频类型，查找该用户的预定信息
        for p in range(3):
            for info in self.booked[p]:
                if info[1] == userId:  # 找到对应用户的预定信息
                    # 取消用户在该视频类型上的预定
                    self.booked[p].discard(info)
                    level = p  # 记录该用户的通道级别
                    # 计算费用：（结束时间 - 开始时间）* 视频类型的费用
                    ans = (time - info[0]) * self.charge[info[2]]
                    break
            if level != -1:  # 找到并取消了该用户的预定
                break
        if level == -1:  # 如果没有找到该用户的预定
            return -1
        # 调整用户的预定通道级别，确保更低的视频类型（更高的优先级）能占用空闲的通道
        while level < 2:
            now_info = None
            # 遍历更高级别的视频类型，尝试将这些用户调整到低级别的视频类型通道
            for p in range(2, level, -1):
                for info in self.booked[p]:
                    if info[2] <= level and (now_info is None or info[1] < now_info[1]):
                        now_info = info
                if now_info:
                    # 找到一个可以调整到低级别的视频类型的用户，并执行调整
                    self.booked[p].discard(now_info)
                    self.booked[level].add(now_info)
                    level = p  # 更新当前级别
                    break
        return ans  # 返回该用户的费用

    # 查询用户当前使用的通道级别，返回-1表示没有使用任何通道
    def queryChannel(self, userId: int) -> int:
        for p in range(3):
            # 检查用户是否在当前级别的视频类型中有预定
            if any(info[1] == userId for info in self.booked[p]):
                return p  # 如果有，返回该通道级别
        return -1  # 如果没有，返回-1

# 以下是程序的主逻辑
obj = None
Q = int(input())  # 输入总共的操作次数
for i in range(Q):
    cmd = input()  # 读取命令
    if i == 0 and cmd == 'MagicService':
        # 初始化MagicService对象
        channels = list(map(int, input().split()))  # 输入每种视频类型的通道数
        charge = list(map(int, input().split()))    # 输入每种视频类型的费用
        obj = MagicService(channels, charge)  # 创建对象
        print("null")  # 对于构造函数返回null
    elif i > 0 and cmd == 'allocateChannel':
        # 分配通道的操作
        time = int(input())  # 输入当前时间
        userId = int(input())  # 输入用户ID
        videoType = int(input())  # 输入视频类型
        print(obj.allocateChannel(time, userId, videoType))  # 调用分配通道函数
    elif i > 0 and cmd == 'freeChannel':
        # 释放通道的操作
        time = int(input())  # 输入当前时间
        userId = int(input())  # 输入用户ID
        print(obj.freeChannel(time, userId))  # 调用释放通道函数
    elif i > 0 and cmd == 'queryChannel':
        # 查询通道的操作
        userId = int(input())  # 输入用户ID
        print(obj.queryChannel(userId))  # 调用查询通道函数
    else:
        assert False  # 如果命令不合法，抛出异常
