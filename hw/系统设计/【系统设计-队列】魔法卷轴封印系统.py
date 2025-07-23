from collections import deque
from typing import List

class ZipSystem:
    def __init__(self, timeWindow: int, maxFiles: int, maxSize: int):
        self.q = deque()
        self.timeWindow = timeWindow
        self.maxFiles = maxFiles
        self.maxSize = maxSize

    def insertFile(self, timestamp: int, fileId: int, fileSize: int) -> int:
        self.q.append([timestamp, fileId, fileSize])
        return len(self.q)

    def zip(self) -> List[int]:
        if len(self.q) == 0:
            return []
        p = 0
        sz = 0
        while p < len(self.q) and p < self.maxFiles and self.q[p][0] - self.q[0][0] <= self.timeWindow and sz + self.q[p][2] <= self.maxSize:
            sz += self.q[p][2]
            p += 1
        ans = []
        for _ in range(p):
            ans.append(self.q.popleft()[1])
        return sorted(ans)


system = None
Q = int(input())
for i in range(Q):
    cmd = input()
    if i == 0 and cmd == "ZipSystem":
        timeWindow = int(input())
        maxFiles = int(input())
        maxSize = int(input())
        system = ZipSystem(timeWindow, maxFiles, maxSize)
        print("null")
    elif i > 0 and cmd == 'insertFile':
        timestamp = int(input())
        fileId = int(input())
        fileSize = int(input())
        print(system.insertFile(timestamp, fileId, fileSize))
    elif i > 0 and cmd == "zip":
        ans = system.zip()
        print(" ".join(map(str, ans)))
    else:
        assert False