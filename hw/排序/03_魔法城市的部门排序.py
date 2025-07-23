'''
题目描述
在魔法王国的一个大城市中，每个城市都有若干个魔法部门，每个部门有一个名称和一个部门人数。你作为王国的部门排序师，需要帮助城市的管理者根据部门的大小和名称对部门进行排序，以便分配资源和制定计划。
你需要根据以下规则，输出每个城市的部门信息：
1. 先按照部门人数从高到低排列；
2. 如果部门人数相同，则按照部门名称的字典序排列；
3. 如果某个城市的部门数量不足 5 个，则输出该城市的所有部门信息。
所有的部门信息按城市名称的字典序进行排序，若城市名称相同，则按部门名称的字典序排列。
输入格式
- 第一行输入一个整数 num，表示数据的行数。
- 接下来 num 行，每行包含三个元素，依次表示 city、departmentName 和 personNum。
  - city：城市名称，字符串，不超过 100 个字符。
  - departmentName：部门名称，字符串，不超过 100 个字符。
  - personNum：部门人数，整数，1 <= personNum <= 100000。
- 1 <= num <= 10000
- 同城市下的部门必定不同名字。
输出格式
输出格式与输入格式一致，每个城市的部门信息按以下规则排序：
- 每个城市的部门信息按部门人数从高到低排序，人数相同则按部门名称字典序排序；
- 如果城市的部门不足 5 个，则全部输出；
- 所有城市按字典序排列，如果城市名称相同，则按部门名称字典序排序。
样例
样例1
样例输入：
11
Beastland FireDepartment 100
Beastland WaterDepartment 50
Beastland EarthDepartment 50
Beastland AirDepartment 100
Beastland MagicDepartment 75
Beastland LandDepartment 75
Crestdale ArtDepartment 30
Crestdale HealthDepartment 60
Crestdale EconomyDepartment 50
Crestdale PoliceDepartment 40
Crestdale FireDepartment 90
样例输出：
Beastland AirDepartment 100
Beastland FireDepartment 100
Beastland LandDepartment 75
Beastland MagicDepartment 75
Beastland EarthDepartment 50
Crestdale FireDepartment 90
Crestdale HealthDepartment 60
Crestdale EconomyDepartment 50
Crestdale PoliceDepartment 40
Crestdale ArtDepartment 30
'''

class Solution:
    def sort_departments(self, data):
        # 创建一个字典，用于存储每个城市对应的所有部门信息
        # 键是城市名，值是该城市中所有部门的列表，每个部门是一个元组 (department_name, person_num)
        city_departments = {}

        # 遍历所有输入数据行
        for line in data:
            # 将每行按空格拆分为城市名、部门名和人数
            city, department_name, person_num = line.split()
            # 如果城市不在字典中，则初始化一个空列表
            if city not in city_departments:
                city_departments[city] = []
            # 将部门信息添加到对应城市的列表中，人数转换为整数
            city_departments[city].append((department_name, int(person_num)))

        # 遍历每个城市，对其部门列表进行排序
        for city in city_departments:
            # 排序规则：
            '''
            学习这种写法：
            city_departments[city].sort(key=lambda x: (-x[1], x[0]))
            '''
            # 1. 先按人数降序排列（-x[1] 表示降序）
            # 2. 若人数相同，则按部门名称字典序升序排列（x[0]）
            city_departments[city].sort(key=lambda x: (-x[1], x[0]))

            # 如果该城市的部门数超过 5 个，只保留前 5 个部门
            # 若不足 5 个，则保留全部（即列表切片不会出错）
            city_departments[city] = city_departments[city][:5]

        # 准备结果列表用于最终输出
        result = []

        # 按照城市名称字典序遍历所有城市
        for city in sorted(city_departments.keys()):
            # 获取排序后的该城市的部门列表
            departments = city_departments[city]
            # 将部门信息按格式拼接为字符串并加入结果列表
            for department_name, person_num in departments:
                result.append(f"{city} {department_name} {person_num}")

        # 返回所有排序好的部门信息（每行一个字符串）
        return result


if __name__ == "__main__":
    # 读取输入的行数
    num = int(input())
    # 逐行读取输入内容，去除每行首尾空白字符
    data = [input().strip() for _ in range(num)]

    # 创建解决方案类的实例
    sol = Solution()
    # 调用排序函数获取结果
    result = sol.sort_departments(data)

    # 遍历结果并逐行打印输出
    for line in result:
        print(line)
