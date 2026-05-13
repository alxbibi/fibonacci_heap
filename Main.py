import math
import json


class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

    def __repr__(self):
        return f'Node{self.key}'


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def find_min(self):
        return self.min_node.key if self.min_node else None

    def insert(self, key):
        new_node = Node(key)
        if self.min_node is None:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.total_nodes += 1
        return new_node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = self._get_nodes_in_list(z.child)
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None

            z.left.right = z.right
            z.right.left = z.left

            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()

            self.total_nodes -= 1
        return z.key if z else None

    def find_node(self, key):
        """Итеративный поиск узла по ключу (O(n))."""
        if not self.min_node:
            return None

        stack = [self.min_node]
        visited = set()

        while stack:
            start_node = stack.pop()
            if start_node in visited:
                continue

            curr = start_node
            while True:
                if curr in visited:
                    break
                visited.add(curr)

                if curr.key == key:
                    return curr

                if curr.child:
                    stack.append(curr.child)

                curr = curr.right
                if curr == start_node:
                    break
        return None

    def delete(self, node):
        """Удаляет узел, уменьшая его ключ до -бесконечности."""
        self.decrease_key(node, float('-inf'))
        self.extract_min()

    def _add_to_root_list(self, node):
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node

    def _get_nodes_in_list(self, start_node):
        nodes = []
        curr = start_node
        while True:
            nodes.append(curr)
            curr = curr.right
            if curr == start_node:
                break
        return nodes

    def _consolidate(self):
        max_degree = int(math.log2(self.total_nodes)) + 1
        A = [None] * (max_degree + 1)

        root_nodes = self._get_nodes_in_list(self.min_node)

        for w in root_nodes:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        self.min_node = None
        for node in A:
            if node is not None:
                if self.min_node is None:
                    self.min_node = node
                    node.left = node.right = node
                else:
                    self._add_to_root_list(node)
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
        if k > x.key:
            return
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def _cut(self, x, y):
        if x == x.right:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                y.child = x.right
        y.degree -= 1
        self._add_to_root_list(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def _search_recursive(self, curr, key, visited):
        if not curr or curr in visited:
            return None
        visited.add(curr)
        if curr.key == key:
            return curr

        res = None
        if curr.right not in visited:
            res = self._search_recursive(curr.right, key, visited)

        if not res and curr.child:
            res = self._search_recursive(curr.child, key, visited)
        return res

test_heap = FibonacciHeap()

with open('Data.json') as f:
    data = json.load(f)

for x in data:
    test_heap.insert(x)

print(test_heap.find_node(190))