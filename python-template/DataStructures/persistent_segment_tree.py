class PersistentSegmentTree:
    """Persistent point-add/range-sum tree over 1-based indices."""

    def __init__(self, size):
        """Initialize the data structure."""
        if size <= 0:
            raise ValueError('size must be positive')
        self.size = size
        self.left = [0]
        self.right = [0]
        self.total = [0]
        self.empty_root = 0

    def _clone(self, node):
        """Run the internal clone step."""
        self.left.append(self.left[node])
        self.right.append(self.right[node])
        self.total.append(self.total[node])
        return len(self.total) - 1

    def add(self, previous_root, index, delta=1):
        """Run the add operation."""
        if not 1 <= index <= self.size:
            raise IndexError('index is out of range')
        index -= 1

        def update(node, left, right):
            """Run the update operation."""
            new_node = self._clone(node)
            self.total[new_node] += delta
            if right - left > 1:
                middle = (left + right) // 2
                if index < middle:
                    self.left[new_node] = update(self.left[new_node], left, middle)
                else:
                    self.right[new_node] = update(self.right[new_node], middle, right)
            return new_node

        return update(previous_root, 0, self.size)

    def query(self, root, query_left, query_right):
        """Run the query operation."""
        query_left = max(1, query_left)
        query_right = min(self.size, query_right)
        if query_left > query_right:
            return 0
        query_left -= 1

        def get(node, left, right):
            """Run the get operation."""
            if not node or query_right <= left or right <= query_left:
                return 0
            if query_left <= left and right <= query_right:
                return self.total[node]
            middle = (left + right) // 2
            return get(self.left[node], left, middle) + get(self.right[node], middle, right)

        return get(root, 0, self.size)

    def count_leq(self, left_root, right_root, value):
        """Count entries with index <= value in a version difference."""
        return self.query(right_root, 1, value) - self.query(left_root, 1, value)

    def max_less(self, left_root, right_root, value):
        """Return the largest index < value in a version difference."""
        value = min(value, self.size + 1)
        if value <= 1:
            return -1
        value -= 1

        def visit(left_root, right_root, left, right):
            """Run the visit operation."""
            if left >= value or self.total[right_root] - self.total[left_root] == 0:
                return -1
            if right - left == 1:
                return left
            middle = (left + right) // 2
            result = visit(self.right[left_root], self.right[right_root], middle, right)
            return result if result != -1 else visit(self.left[left_root], self.left[right_root], left, middle)

        result = visit(left_root, right_root, 0, self.size)
        return result + 1 if result != -1 else -1

    def max_value(self, root):
        """Return the largest index present in one version."""
        if not self.total[root]:
            return -1
        node, left, right = root, 0, self.size
        while right - left > 1:
            middle = (left + right) // 2
            if self.total[self.right[node]]:
                node, left = self.right[node], middle
            else:
                node, right = self.left[node], middle
        return left + 1

    def kth_between(self, left_root, right_root, k):
        """1-based kth index in multiset(right_root - left_root)."""
        count = self.total[right_root] - self.total[left_root]
        if k < 1 or k > count:
            raise IndexError('k is out of range')
        left = 0
        right = self.size
        while right - left > 1:
            middle = (left + right) // 2
            left_count = (self.total[self.left[right_root]]
                          - self.total[self.left[left_root]])
            if k <= left_count:
                left_root = self.left[left_root]
                right_root = self.left[right_root]
                right = middle
            else:
                k -= left_count
                left_root = self.right[left_root]
                right_root = self.right[right_root]
                left = middle
        return left + 1

    kth = kth_between


class PersistentMaxIndexTree:
    """Persistent index tree storing two maximum values per range.

    Values are 1-based; updates return new roots and preserve old versions.
    """

    def __init__(self, values, neg_inf=float("-inf")):
        """Initialize the data structure."""
        values = list(values)
        values = values[1:] if values else []
        self.n = len(values)
        self.neg_inf = neg_inf
        self.left = [0]
        self.right = [0]
        self.max_a = [neg_inf]
        self.max_b = [neg_inf]
        self._values = values
        self.empty_root = self._build(1, self.n) if self.n else 0

    def _build(self, left, right):
        """Run the internal build step."""
        node = len(self.max_a)
        self.left.append(0)
        self.right.append(0)
        self.max_a.append(self.neg_inf)
        self.max_b.append(self._values[left - 1] if left == right else self.neg_inf)
        if left != right:
            middle = (left + right) // 2
            self.left[node] = self._build(left, middle)
            self.right[node] = self._build(middle + 1, right)
            self._pull(node)
        return node

    def _pull(self, node):
        """Run the internal pull step."""
        self.max_a[node] = max(self.max_a[self.left[node]], self.max_a[self.right[node]])
        self.max_b[node] = max(self.max_b[self.left[node]], self.max_b[self.right[node]])

    def update(self, root, index, value):
        """Run the update operation."""
        if not 1 <= index <= self.n:
            raise IndexError("index is out of range")

        def change(node, left, right):
            """Run the change operation."""
            new_node = len(self.max_a)
            self.left.append(self.left[node])
            self.right.append(self.right[node])
            self.max_a.append(self.max_a[node])
            self.max_b.append(self.max_b[node])
            if left == right:
                self.max_a[new_node] = value
                self.max_b[new_node] = self.neg_inf
                return new_node
            middle = (left + right) // 2
            if index <= middle:
                self.left[new_node] = change(self.left[node], left, middle)
            else:
                self.right[new_node] = change(self.right[node], middle + 1, right)
            self._pull(new_node)
            return new_node

        return change(root, 1, self.n)

    def query(self, root, left, right):
        """Run the query operation."""
        left, right = max(1, left), min(self.n, right)
        if left > right or not root:
            return self.neg_inf, self.neg_inf

        def visit(node, node_left, node_right):
            """Run the visit operation."""
            if node == 0 or right < node_left or node_right < left:
                return self.neg_inf, self.neg_inf
            if left <= node_left and node_right <= right:
                return self.max_a[node], self.max_b[node]
            middle = (node_left + node_right) // 2
            a1, b1 = visit(self.left[node], node_left, middle)
            a2, b2 = visit(self.right[node], middle + 1, node_right)
            return max(a1, a2), max(b1, b2)

        return visit(root, 1, self.n)
