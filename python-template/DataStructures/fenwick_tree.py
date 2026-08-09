"""Fenwick tree with 1-based closed intervals."""


class FenwickTree(object):
    def __init__(self, size_or_data):
        """Initialize the data structure."""
        if isinstance(size_or_data, int):
            if size_or_data < 0:
                raise ValueError('size must be nonnegative')
            self.n = size_or_data
            self.tree = [0] * (self.n + 1)
        else:
            data = list(size_or_data)
            self.n = len(data)
            self.tree = [0] + data
            for index in range(1, self.n + 1):
                parent = index + (index & -index)
                if parent <= self.n:
                    self.tree[parent] += self.tree[index]

    def add(self, index, delta):
        """Run the add operation."""
        if not 1 <= index <= self.n:
            raise IndexError('index is out of range')
        while index <= self.n:
            self.tree[index] += delta
            index += index & -index

    def sum(self, end):
        """Return the clamped prefix sum on ``[1, end]``."""
        end = min(self.n, end)
        result = 0
        while end > 0:
            result += self.tree[end]
            end -= end & -end
        return result

    def range_sum(self, left, right):
        """Return the sum on the 1-based closed interval ``[left, right]``."""
        if left > right:
            return 0
        return self.sum(right) - self.sum(left - 1)

    def lower_bound(self, target):
        """Return the first 1-based position with prefix sum at least target."""
        if target <= 0:
            return 1 if self.n else -1
        index = 0
        bit = 1 << (self.n.bit_length() - 1) if self.n else 0
        while bit:
            next_index = index + bit
            if next_index <= self.n and self.tree[next_index] < target:
                index = next_index
                target -= self.tree[next_index]
            bit >>= 1
        return index + 1 if index < self.n else -1

    def select(self, target):
        """Return the largest x with prefix sum on [1, x] at most target."""
        index = 0
        current = 0
        bit = 1 << (self.n.bit_length() - 1) if self.n else 0
        while bit:
            next_index = index + bit
            if next_index <= self.n and current + self.tree[next_index] <= target:
                index = next_index
                current += self.tree[next_index]
            bit >>= 1
        return index
