class RangeAddPointQuery(object):
    """Range add and point query on 1-based closed intervals."""

    def __init__(self, values):
        """Initialize the data structure."""
        self.values = list(values)
        self.block_size = max(1, int(len(self.values) ** 0.5))
        self.lazy = [0] * ((len(self.values) + self.block_size - 1) // self.block_size)

    def add(self, left, right, delta):
        """Run the add operation."""
        if not 1 <= left <= right <= len(self.values):
            if left > right:
                return
            raise IndexError("range is out of bounds")
        left -= 1
        while left < right and left % self.block_size:
            self.values[left] += delta
            left += 1
        while left + self.block_size <= right:
            self.lazy[left // self.block_size] += delta
            left += self.block_size
        while left < right:
            self.values[left] += delta
            left += 1

    def get(self, index):
        """Run the get operation."""
        if not 1 <= index <= len(self.values):
            raise IndexError("index is out of range")
        index -= 1
        return self.values[index] + self.lazy[index // self.block_size]
