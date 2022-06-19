"""
插入一个数

求最小值

删除最小值

合并两棵树

整棵树维护一个值 val 和到其最近的空节点的距离 dis
"""

'''
维护一个小根堆的集合，支持
1. 在集合中插入一个新堆，堆中只包含一个数a
2. 将第 x 个插入的数和第 y 个插入的数所在的小根堆合并
3. 输出第 x 个插入的数所在小根堆的最小值
4. 删除第 x 个插入的数所在小根堆的最小值（若最小值不唯一，则优先删除先插入的数）
'''

# 节点数
N = 200100
# 左指针
LeftPoint = [0] * N
# 右指针
RightPoint = [0] * N
# 节点距离
distance = [0] * N
# 树中的值
val = [0] * N
# 并查集
disjoint = [0] * N
# 缓存，并查集操作使用
buffer = [0] * N
# 当前对象池的末尾
pool_pos = 1

T = int

class LeftistHeapForest:
    def __get_union_root(self, node: int) -> int:
        """
        获取并查集中的root id
        :param node: 节点
        :return: 节点所在的数的根节点的id
        """
        pos = 0
        p = node
        while p != disjoint[p]:
            buffer[pos] = p
            pos += 1
            p = disjoint[p]
        for i in range(0, pos):
            disjoint[buffer[i]] = p
        return p

    def __in_same_union(self, id1: int, id2: int) -> bool:
        """
        查询两个节点是否在同一个并查集中
        :param id1:节点1
        :param id2:节点2
        :return:是否在同一个并查集中
        """
        return self.__get_union_root(id1) == self.__get_union_root(id2)

    def __merge_union(self, id1: int, id2: int):
        """
        合并两个并查集
        :param id1:
        :param id2:
        """
        disjoint[self.__get_union_root(id1)] = self.__get_union_root(id2)

    def __change_union_root_id(self, id: int):
        """
        并查集修改根id
        :param id: 要修改的id
        """
        disjoint[self.__get_union_root(id)] = id
        disjoint[id] = id

    def __merge(self, id1: int, id2: int) -> int:
        """
        合并两个堆
        :param id1: 堆根id
        :param id2: 堆根id
        :return: 合并后的新堆的根id
        """
        if id1 == 0 or id2 == 0:
            return id1 + id2

        val1, val2 = val[id1], val[id2]
        if val2 < val1 or (val1 == val2 and id2 < id1):
            id1 = id1 ^ id2
            id2 = id1 ^ id2
            id1 = id1 ^ id2

        new_root_id = self.__merge(RightPoint[id1], id2)
        RightPoint[id1] = new_root_id
        distance[id1] = distance[new_root_id] + 1

        l_id, r_id = LeftPoint[id1], RightPoint[id1]
        if distance[r_id] > distance[l_id]:
            LeftPoint[id1], RightPoint[id1] = r_id, l_id
        return id1

    def make_new_heap(self, v: T) -> int:
        """
        用数值v创建新堆
        :param v:
        :return: 创建的节点的id
        """
        global pool_pos
        id = pool_pos
        pool_pos += 1
        LeftPoint[id], RightPoint[id], distance[id] = 0, 0, 0
        val[id] = v
        disjoint[id] = id
        return id

    def merge(self, id1: int, id2: int) -> int:
        """
        合并两个堆
        :param id1: 堆根id
        :param id2: 堆根id
        :return: 合并后的新堆的根id
        """
        if id1 == 0 or id2 == 0:
            return self.__get_union_root(id1 + id2)

        if self.__in_same_union(id1, id2):
            return self.__get_union_root(id1)

        new_root_id = self.__merge(self.__get_union_root(id1), self.__get_union_root(id2))
        self.__merge_union(id1, id2)
        self.__change_union_root_id(new_root_id)

        return new_root_id

    def put(self, id: int, val: T) -> int:
        """
        入堆
        :param id:堆顶编号
        :param val: 要放入的值
        :return: 新节点id
        """
        new_id = self.make_new_heap(val)
        self.merge(new_id, id)
        return new_id

    def get_top_val(self, id: int) -> list:
        """
        获取id所在堆的堆顶元素
        :param id:
        :return: [堆顶id,堆顶元素值]
        """
        top_id = self.__get_union_root(id)
        return [top_id, val[top_id]]

    def pop_top_val(self, id: int) -> list:
        """
        将id所在的堆的堆顶元素出堆
        :param id:
        :return: [堆顶id,堆顶值]
        """
        top_id = self.__get_union_root(id)
        new_root_id = self.__merge(LeftPoint[top_id], RightPoint[top_id])
        self.__change_union_root_id(new_root_id)
        return [top_id, val[top_id]]

if __name__ == '__main__':
    algo = LeftistHeapForest()
    n = int(input())
    for i in range(0, n):
        rd = input().split(' ')
        if rd[0] == '1':
            a = int(rd[1])
            algo.make_new_heap(a)
        elif rd[0] == '2':
            x, y = int(rd[1]), int(rd[2])
            algo.merge(x, y)
        elif rd[0] == '3':
            x = int(rd[1])
            print(algo.get_top_val(x)[1])
        elif rd[0] == '4':
            x = int(rd[1])
            algo.pop_top_val(x)
