class BitSegmentTree:
    """Binary lazy tree with 1-based closed intervals."""

    def __init__(self, bits):
        """Initialize the data structure."""
        bits = list(bits)
        self.n = len(bits)
        self.ones = [0] * (4 * self.n if self.n else 1)
        self.lazy = [-1] * len(self.ones)  # -1 none, 0/1 assign, 2 flip
        if self.n:
            self._build(1, 0, self.n, bits)

    def _build(self, node, left, right, bits):
        """Run the internal build step."""
        if right - left == 1:
            self.ones[node] = int(bool(bits[left]))
            return
        middle = (left + right) // 2
        self._build(2 * node, left, middle, bits)
        self._build(2 * node + 1, middle, right, bits)
        self.ones[node] = self.ones[2 * node] + self.ones[2 * node + 1]

    def _apply(self, node, left, right, tag):
        """Run the internal apply step."""
        if tag == 2:
            self.ones[node] = right - left - self.ones[node]
            self.lazy[node] = {-1: 2, 2: -1, 0: 1, 1: 0}[self.lazy[node]]
        else:
            self.ones[node] = (right - left) * tag
            self.lazy[node] = tag

    def _push(self, node, left, right):
        """Run the internal push step."""
        if self.lazy[node] != -1 and right - left > 1:
            middle = (left + right) // 2
            self._apply(2 * node, left, middle, self.lazy[node])
            self._apply(2 * node + 1, middle, right, self.lazy[node])
            self.lazy[node] = -1

    def _update(self, query_left, query_right, tag):
        """Run the internal update step."""
        def update(node, left, right):
            """Run the update operation."""
            if query_right <= left or right <= query_left:
                return
            if query_left <= left and right <= query_right:
                self._apply(node, left, right, tag)
                return
            self._push(node, left, right)
            middle = (left + right) // 2
            update(2 * node, left, middle)
            update(2 * node + 1, middle, right)
            self.ones[node] = self.ones[2 * node] + self.ones[2 * node + 1]

        if query_left < query_right:
            update(1, 0, self.n)

    def assign(self, left, right, value):
        """Run the assign operation."""
        if left > right:
            return
        if not 1 <= left <= right <= self.n:
            raise IndexError('range is out of bounds')
        self._update(left - 1, right, int(bool(value)))

    def flip(self, left, right):
        """Run the flip operation."""
        if left > right:
            return
        if not 1 <= left <= right <= self.n:
            raise IndexError('range is out of bounds')
        self._update(left - 1, right, 2)

    def count(self, query_left, query_right):
        """Run the count operation."""
        if query_left > query_right:
            return 0
        if not 1 <= query_left <= query_right <= self.n:
            raise IndexError('range is out of bounds')
        query_left, query_right = query_left - 1, query_right
        def query(node, left, right):
            """Run the query operation."""
            if query_right <= left or right <= query_left:
                return 0
            if query_left <= left and right <= query_right:
                return self.ones[node]
            self._push(node, left, right)
            middle = (left + right) // 2
            return query(2 * node, left, middle) + query(2 * node + 1, middle, right)

        return query(1, 0, self.n) if query_left < query_right else 0

    def kth_one(self, k):
        """Return the 1-based position of the k-th one (k starts at 1)."""
        if not self.n or k < 1 or k > self.ones[1]:
            raise IndexError('k is out of range')
        k -= 1
        node, left, right = 1, 0, self.n
        while right - left > 1:
            self._push(node, left, right)
            middle = (left + right) // 2
            if k < self.ones[2 * node]:
                node, right = 2 * node, middle
            else:
                k -= self.ones[2 * node]
                node, left = 2 * node + 1, middle
        return left + 1

    def find_first(self, left, right, bit=1):
        """Return the first 1-based position equal to bit."""
        left, right = max(1, left), min(self.n, right)
        if left > right:
            return -1

        def search(node, node_left, node_right):
            """Run the search operation."""
            if right < node_left or node_right < left:
                return -1
            if bit and self.ones[node] == 0:
                return -1
            if not bit and self.ones[node] == node_right - node_left + 1:
                return -1
            if node_left == node_right:
                return node_left
            self._push(node, node_left - 1, node_right)
            middle = (node_left + node_right) // 2
            result = search(node * 2, node_left, middle)
            return result if result != -1 else search(node * 2 + 1, middle + 1, node_right)

        return search(1, 1, self.n)
