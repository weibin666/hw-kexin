# 双向链表的节点类，用于维护窗口层级顺序
class Node:
    def __init__(self, id):
        self.id = id       # 窗口ID
        self.prev = None   # 前一个节点
        self.next = None   # 后一个节点

# 多窗口系统类，包含窗口创建、销毁、移动、点击处理
class MultiWindowSys:
    def __init__(self):
        # 哈希表：窗口ID -> [row, col, width, height, node]
        # 用于快速访问窗口信息
        self.windows = {}

        # 创建一个双向链表头尾（虚拟节点），用于维护窗口的层级
        # 链表尾部是最上层窗口，头部是最底层窗口
        self.head = Node(-1)  # 哨兵头结点
        self.tail = Node(-1)  # 哨兵尾结点
        self.head.next = self.tail
        self.tail.prev = self.head

    def create_window(self, id: int, row: int, col: int, width: int, height: int) -> bool:
        # 创建一个新的窗口
        if id in self.windows:
            return False  # 若ID已存在，创建失败
        node = Node(id)  # 创建对应链表节点
        self._add_to_tail(node)  # 加入链表尾部，表示置于最上层
        # 存储窗口信息及对应节点
        self.windows[id] = [row, col, width, height, node]
        return True

    def destroy_window(self, id: int) -> bool:
        # 销毁指定ID的窗口
        if id not in self.windows:
            return False  # 若不存在该ID，销毁失败
        _, _, _, _, node = self.windows[id]
        self._remove_node(node)  # 从链表中移除
        del self.windows[id]     # 从哈希表中删除
        return True

    def move_window(self, id: int, row: int, col: int) -> bool:
        # 移动窗口到新的左上角坐标
        if id not in self.windows:
            return False
        self.windows[id][0] = row  # 更新row
        self.windows[id][1] = col  # 更新col
        return True

    def click(self, row: int, col: int) -> int:
        # 处理点击事件，从最上层窗口往下查找
        cur = self.tail.prev  # 从链表尾部（最上层）开始
        while cur != self.head:
            id = cur.id
            w_row, w_col, width, height, _ = self.windows[id]
            # 判断点击是否命中该窗口范围
            if (w_row <= row < w_row + height) and (w_col <= col < w_col + width):
                # 命中后，将该窗口提到最上层
                self._remove_node(cur)
                self._add_to_tail(cur)
                return id  # 返回命中的窗口ID
            cur = cur.prev  # 继续往下层查找
        return -1  # 没有窗口命中，返回-1

    # 将节点插入链表尾部（表示最上层）
    def _add_to_tail(self, node: Node):
        last = self.tail.prev
        last.next = node
        node.prev = last
        node.next = self.tail
        self.tail.prev = node

    # 从链表中移除指定节点
    def _remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev


# 主程序部分，读取输入并根据指令调用系统方法
system = None
Q = int(input())  # 操作总数
for i in range(Q):
    cmd = input()  # 操作指令
    if i == 0 and cmd == "MultiWindowSys":
        # 初始化系统
        system = MultiWindowSys()
        print("null")
    elif i > 0 and cmd == "create_window":
        # 创建窗口
        id = int(input())
        row = int(input())
        col = int(input())
        width = int(input())
        height = int(input())
        print(system.create_window(id, row, col, width, height))
    elif i > 0 and cmd == "destroy_window":
        # 销毁窗口
        id = int(input())
        print(system.destroy_window(id))
    elif i > 0 and cmd == "move_window":
        # 移动窗口
        id = int(input())
        row = int(input())
        col = int(input())
        print(system.move_window(id, row, col))
    elif i > 0 and cmd == "click":
        # 处理点击事件
        row = int(input())
        col = int(input())
        print(system.click(row, col))
    else:
        # 不支持的命令
        assert False
