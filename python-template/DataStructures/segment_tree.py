"""Generic segment trees with 1-based closed intervals."""

from copy import deepcopy


_MISSING = object()


class SegmentTree:
    """Static tree with custom node values and an associative merge operation."""

    def __init__(self, data=0, operation=None, identity=_MISSING):
        """Initialize the data structure."""
        if isinstance(data, int):
            if identity is _MISSING:
                identity = 0
            values = [deepcopy(identity) for _ in range(max(0, data))]
        else:
            values = list(data)

        if identity is _MISSING:
            identity = type(values[0])() if values and not isinstance(values[0], (int, float, complex)) else 0
        self.n = len(values)
        self.operation = operation or (lambda left, right: left + right)
        self.identity = identity
        self.info = [self._new_identity() for _ in range(4 * self.n + 5)]
        self.tree = self.info
        if self.n:
            self._build(1, 1, self.n, values)

    def _new_identity(self):
        """Run the internal new identity step."""
        return deepcopy(self.identity)

    def _combine(self, left, right):
        """Run the internal combine step."""
        return self.operation(left, right)

    def _build(self, node, left, right, values):
        """Run the internal build step."""
        if left == right:
            self.info[node] = values[left - 1]
            return
        middle = (left + right) // 2
        self._build(node * 2, left, middle, values)
        self._build(node * 2 + 1, middle + 1, right, values)
        self._pull(node)

    def _pull(self, node):
        """Run the internal pull step."""
        self.info[node] = self._combine(self.info[node * 2], self.info[node * 2 + 1])

    def _clip(self, left, right):
        """Run the internal clip step."""
        left = max(1, left)
        right = min(self.n, right)
        return left, right

    def modify(self, index, value):
        """Set a 1-based position."""
        if not 1 <= index <= self.n:
            raise IndexError("index is out of range")

        def update(node, left, right):
            """Run the update operation."""
            if left == right:
                self.info[node] = value
                return
            middle = (left + right) // 2
            if index <= middle:
                update(node * 2, left, middle)
            else:
                update(node * 2 + 1, middle + 1, right)
            self._pull(node)

        update(1, 1, self.n)

    def range_query(self, left, right):
        """Merge a 1-based closed interval."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return self._new_identity()

        def query(node, node_left, node_right):
            """Run the query operation."""
            if right < node_left or node_right < left:
                return self._new_identity()
            if left <= node_left and node_right <= right:
                return self.info[node]
            middle = (node_left + node_right) // 2
            return self._combine(
                query(node * 2, node_left, middle),
                query(node * 2 + 1, middle + 1, node_right),
            )

        return query(1, 1, self.n)

    def find_first(self, left, right, predicate):
        """Return the first matching position in a closed interval."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return -1

        def search(node, node_left, node_right):
            """Run the search operation."""
            if right < node_left or node_right < left or not predicate(self.info[node]):
                return -1
            if node_left == node_right:
                return node_left
            middle = (node_left + node_right) // 2
            result = search(node * 2, node_left, middle)
            return result if result != -1 else search(node * 2 + 1, middle + 1, node_right)

        return search(1, 1, self.n)

    def find_last(self, left, right, predicate):
        """Return the last matching position in a closed interval."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return -1

        def search(node, node_left, node_right):
            """Run the search operation."""
            if right < node_left or node_right < left or not predicate(self.info[node]):
                return -1
            if node_left == node_right:
                return node_left
            middle = (node_left + node_right) // 2
            result = search(node * 2 + 1, middle + 1, node_right)
            return result if result != -1 else search(node * 2, node_left, middle)

        return search(1, 1, self.n)

    @staticmethod
    def _score(value):
        """Run the internal score step."""
        return getattr(value, "sum", value)

    def search(self, target):
        """Find the first position whose nonnegative prefix aggregate reaches target."""
        if self.n == 0 or target <= 0 or self._score(self.info[1]) < target:
            return -1
        node, left, right = 1, 1, self.n
        while left != right:
            middle = (left + right) // 2
            if self._score(self.info[node * 2]) >= target:
                node, right = node * 2, middle
            else:
                target -= self._score(self.info[node * 2])
                node, left = node * 2 + 1, middle + 1
        return left

class ZKWSegmentTree:
    """Generic iterative (ZKW-style) tree with 1-based closed intervals."""

    def __init__(self, values, operation=None, identity=_MISSING):
        """Initialize the data structure."""
        values = list(values)
        values = values[1:]
        if identity is _MISSING:
            identity = type(values[0])() if values and not isinstance(values[0], (int, float, complex)) else 0
        self.n = len(values)
        self.operation = operation or (lambda left, right: left + right)
        self.identity = identity
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.info = [deepcopy(identity) for _ in range(2 * self.size)]
        self.info[self.size:self.size + self.n] = values
        for node in range(self.size - 1, 0, -1):
            self.info[node] = self.operation(self.info[node * 2], self.info[node * 2 + 1])

    def modify(self, index, value):
        """Run the modify operation."""
        if not 1 <= index <= self.n:
            raise IndexError("index is out of range")
        node = self.size + index - 1
        self.info[node] = value
        node //= 2
        while node:
            self.info[node] = self.operation(self.info[node * 2], self.info[node * 2 + 1])
            node //= 2

    def range_query(self, left, right):
        """Run the range query operation."""
        left, right = max(1, left), min(self.n, right)
        if left > right:
            return deepcopy(self.identity)
        left += self.size - 1
        right += self.size - 1
        result_left = deepcopy(self.identity)
        result_right = deepcopy(self.identity)
        while left <= right:
            if left & 1:
                result_left = self.operation(result_left, self.info[left])
                left += 1
            if not right & 1:
                result_right = self.operation(self.info[right], result_right)
                right -= 1
            left //= 2
            right //= 2
        return self.operation(result_left, result_right)

    def find_first(self, left, right, predicate):
        """Run the find first operation."""
        left, right = max(1, left), min(self.n, right)
        if left > right:
            return -1

        def walk(node, node_left, node_right):
            """Run the walk operation."""
            if (right < node_left or node_right < left or node_left > self.n
                    or not predicate(self.info[node])):
                return -1
            if node_left == node_right:
                return node_left
            middle = (node_left + node_right) // 2
            result = walk(node * 2, node_left, middle)
            return result if result != -1 else walk(node * 2 + 1, middle + 1, node_right)

        return walk(1, 1, self.size)


# C++ naming alias.
ZKW_segment_tree = ZKWSegmentTree
