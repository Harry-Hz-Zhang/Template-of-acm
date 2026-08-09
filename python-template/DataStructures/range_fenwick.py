class _Fenwick(object):
    def __init__(self, n):
        """Initialize the data structure."""
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, index, delta):
        """Run the add operation."""
        while index <= self.n:
            self.tree[index] += delta
            index += index & -index

    def sum(self, end):
        """Run the sum operation."""
        result = 0
        while end > 0:
            result += self.tree[end]
            end -= end & -end
        return result


class RangeFenwick(object):
    """Range add and range sum on 1-based closed intervals."""

    def __init__(self, n):
        """Initialize the data structure."""
        if n < 0:
            raise ValueError('size must be nonnegative')
        self.n = n
        self.bit1 = _Fenwick(n)
        self.bit2 = _Fenwick(n)

    def _add_boundary(self, index, delta):
        """Run the internal add boundary step."""
        if 1 <= index <= self.n:
            self.bit1.add(index, delta)
            self.bit2.add(index, delta * (index - 1))

    def add_range(self, left, right, delta):
        """Add delta to the closed interval ``[left, right]``."""
        if left > right:
            return
        if not 1 <= left <= right <= self.n:
            raise IndexError('range is out of bounds')
        self._add_boundary(left, delta)
        self._add_boundary(right + 1, -delta)

    def prefix_sum(self, end):
        """Return the sum on ``[1, end]``."""
        end = min(self.n, end)
        return self.bit1.sum(end) * end - self.bit2.sum(end)

    def range_sum(self, left, right):
        """Return the sum on the closed interval ``[left, right]``."""
        if left > right:
            return 0
        if not 1 <= left <= right <= self.n:
            raise IndexError('range is out of bounds')
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
