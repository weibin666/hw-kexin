class AlarmSystem:
    def __init__(self):
        """
        初始化闹钟系统，使用一个字典 self.alarms 存储所有闹钟。
        字典的键是闹钟的 id，值是一个元组 (weekdays, hour, minute, typeId)
        """
        self.alarms = {}

    def addAlarm(self, id: int, weekdays: list, hour: int, minute: int, typeId: int) -> bool:
        """
        添加新的闹钟

        参数：
        - id：闹钟的唯一编号
        - weekdays：一个整数列表，包含该闹钟在一周中会响铃的星期几（1~7）
        - hour：闹钟响铃的小时（0~23）
        - minute：闹钟响铃的分钟（0~59）
        - typeId：闹钟的类型（0 普通, 1 紧急, 2 重要）

        返回值：
        - 如果该 id 的闹钟不存在，则添加成功，返回 True；
        - 否则已存在同 id，添加失败，返回 False。
        """
        if id in self.alarms:
            return False  # 已存在相同 id，添加失败

        # 记录该闹钟的详细信息
        self.alarms[id] = (weekdays, hour, minute, typeId)
        return True

    def deleteAlarm(self, id: int) -> bool:
        """
        删除指定 id 的闹钟

        参数：
        - id：闹钟的唯一编号

        返回值：
        - 如果该闹钟存在并删除成功，返回 True；
        - 否则返回 False。
        """
        if id not in self.alarms:
            return False  # 不存在该闹钟，删除失败

        # 删除闹钟
        del self.alarms[id]
        return True

    def queryAlarm(self, weekday: int, hour: int, startMinute: int, endMinute: int) -> list:
        """
        查询指定时间范围内会响铃的所有闹钟

        参数：
        - weekday：星期几（1~7）
        - hour：查询的小时（0~23）
        - startMinute：起始分钟（0~59）
        - endMinute：结束分钟（startMinute ≤ endMinute < 60）

        返回值：
        - 满足条件的闹钟 id 列表，排序规则如下：
            1. 先按 (hour, minute) 升序
            2. 再按 typeId 升序
            3. 最后按 id 升序
        - 如果没有匹配的闹钟，则返回 [-1]
        """
        result = []

        # 遍历所有闹钟，逐个检查是否符合条件
        for alarm_id, (weekdays, alarm_hour, alarm_minute, typeId) in self.alarms.items():
            if weekday in weekdays:  # 闹钟设置在指定星期几响铃
                if alarm_hour == hour and startMinute <= alarm_minute <= endMinute:
                    # 满足时间范围，将候选项加入结果
                    result.append((alarm_hour, alarm_minute, typeId, alarm_id))

        # 根据题目指定顺序排序
        result.sort(key=lambda x: (x[0], x[1], x[2], x[3]))

        if result:
            # 提取排序后的闹钟 id
            return [alarm[3] for alarm in result]
        else:
            return [-1]  # 没有找到符合条件的闹钟

# 主程序入口
system = None  # 用于存放系统实例
Q = int(input())  # 操作次数

for i in range(Q):
    cmd = input()  # 读取操作命令

    # 操作1：初始化闹钟系统
    if i == 0 and cmd == "AlarmSystem":
        system = AlarmSystem()  # 创建新系统实例
        print("null")  # 按题目要求输出 null

    # 操作2：添加闹钟
    elif i > 0 and cmd == "addAlarm":
        id = int(input())  # 读取闹钟 id
        weekdays_len = int(input())  # 读取 weekdays 数组长度（不使用，仅为配合输入）
        weekdays = list(map(int, input().split()))  # 读取 weekdays 数组
        hour = int(input())  # 小时
        minute = int(input())  # 分钟
        typeId = int(input())  # 闹钟类型
        print(system.addAlarm(id, weekdays, hour, minute, typeId))  # 输出添加结果（True/False）

    # 操作3：删除闹钟
    elif i > 0 and cmd == "deleteAlarm":
        id = int(input())  # 读取要删除的闹钟 id
        print(system.deleteAlarm(id))  # 输出删除结果（True/False）

    # 操作4：查询闹钟
    elif i > 0 and cmd == "queryAlarm":
        weekday = int(input())  # 查询的星期几
        hour = int(input())  # 查询的小时
        startMinute = int(input())  # 查询的起始分钟
        endMinute = int(input())  # 查询的结束分钟
        result = system.queryAlarm(weekday, hour, startMinute, endMinute)  # 获取查询结果
        print(*result)  # 按空格输出所有 id 或 -1

    else:
        # 非法命令触发断言（测试阶段防止漏判）
        assert False
