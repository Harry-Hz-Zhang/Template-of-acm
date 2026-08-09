class SparseTable(object):
    """Static idempotent operation on 1-based nonempty closed intervals."""

    def __init__(self, data, operation=min):
        """Initialize the data structure."""
        data = list(data)
        self.n = len(data)
        self.operation = operation
        self.table = [data]
        length = 2
        while length <= len(data):
            half = length // 2
            previous = self.table[-1]
            self.table.append([
                operation(previous[i], previous[i + half])
                for i in range(len(data) - length + 1)
            ])
            length <<= 1

    def query(self, left, right):
        """Run the query operation."""
        if not 1 <= left <= right <= self.n:
            raise IndexError('range is out of bounds')
        left, right = left - 1, right
        length = right - left
        if length <= 0:
            raise ValueError('query interval must be nonempty')
        level = length.bit_length() - 1
        return self.operation(self.table[level][left], self.table[level][right - (1 << level)])
