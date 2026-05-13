import math
import time
import random
import json


class Node:
    __slots__ = ['key', 'degree', 'parent', 'child', 'left', 'right', 'mark']

    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0
        self.ops = 0

    def insert(self, key):
        self.ops += 1
        node = Node(key)
        if self.min_node is None:
            self.min_node = node
        else:
            self._add_to_root(node)
            if node.key < self.min_node.key:
                self.min_node = node
        self.total_nodes += 1
        return node

    def _add_to_root(self, node):
        node.parent = None
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node

    def find_node(self, key):
        if not self.min_node: return None
        stack = [self.min_node]
        visited = set()
        while stack:
            start = stack.pop()
            if start in visited: continue
            curr = start
            while True:
                self.ops += 1
                if curr.key == key: return curr
                if curr.child: stack.append(curr.child)
                visited.add(curr)
                curr = curr.right
                if curr == start: break
        return None

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                curr = z.child
                first = curr
                while True:
                    self.ops += 1
                    next_node = curr.right
                    self._add_to_root(curr)
                    curr = next_node
                    if curr == first: break

            z.left.right = z.right
            z.right.left = z.left

            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()
            self.total_nodes -= 1
        return z

    def _consolidate(self):
        max_deg = int(math.log2(max(1, self.total_nodes))) + 2
        A = [None] * max_deg

        roots = []
        curr = self.min_node
        if curr:
            start = curr
            while True:
                roots.append(curr)
                curr = curr.right
                if curr == start: break

        for w in roots:
            x = w
            d = x.degree
            while d < max_deg and A[d] is not None:
                self.ops += 1
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            if d < max_deg:
                A[d] = x

        self.min_node = None
        for node in A:
            if node:
                if self.min_node is None:
                    self.min_node = node
                    node.left = node.right = node
                else:
                    self._add_to_root(node)
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link(self, y, x):
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    def decrease_key(self, x, k):
        self.ops += 1
        if k > x.key: return
        x.key = k
        y = x.parent
        if y and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def _cut(self, x, y):
        self.ops += 1
        if x == x.right:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x: y.child = x.right
        y.degree -= 1
        self._add_to_root(x)
        x.mark = False

    def _cascading_cut(self, y):
        z = y.parent
        if z:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()


data_size = 10000

with open('Data.json') as f:
        data = json.load(f)

heap = FibonacciHeap()
nodes_map = {}


def print_stats(title, count, total_time, total_ops):
    avg_time = total_time / count
    avg_ops = total_ops / count
    print(f"--- {title} ---")
    print(f"Всего действий: {count}")
    print(f"Общее время:   {total_time:.6f} сек")
    print(f"Общее операции: {total_ops}")
    print(f"Среднее время:  {avg_time:.8f} сек/действие")
    print(f"Среднее опер.:  {avg_ops:.2f} опер/действие")
    print("-" * 30)


heap.ops = 0
start = time.perf_counter()
for x in data:
    node = heap.insert(x)
    if x not in nodes_map: nodes_map[x] = node
end = time.perf_counter()
print_stats("Добавление (Insert)", len(data), end - start, heap.ops)


search_keys = random.sample(data, 100)
heap.ops = 0
start = time.perf_counter()
for k in search_keys:
    heap.find_node(k)
end = time.perf_counter()
print_stats("Поиск (Find)", len(search_keys), end - start, heap.ops)


delete_keys = random.sample(list(nodes_map.keys()), 1000)
delete_nodes = [nodes_map[k] for k in delete_keys]

heap.ops = 0
start = time.perf_counter()
for n in delete_nodes:
    heap.delete(n)
end = time.perf_counter()
print_stats("Удаление (Delete)", len(delete_nodes), end - start, heap.ops)