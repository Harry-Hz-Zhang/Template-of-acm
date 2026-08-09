import heapq
from collections import Counter


class VeniceSet(object):
    """Multiset supporting add-all and minimum."""

    def __init__(self):
        """Initialize the data structure."""
        self.heap = []
        self.count = Counter()
        self.offset = 0
        self.size = 0

    def add(self, value):
        """Run the add operation."""
        stored = value - self.offset
        heapq.heappush(self.heap, stored)
        self.count[stored] += 1
        self.size += 1

    def discard(self, value):
        """Run the discard operation."""
        stored = value - self.offset
        if not self.count[stored]:
            return False
        self.count[stored] -= 1
        self.size -= 1
        return True

    def add_all(self, delta):
        """Run the add all operation."""
        self.offset += delta

    def minimum(self):
        """Run the minimum operation."""
        while self.heap and not self.count[self.heap[0]]:
            heapq.heappop(self.heap)
        if not self.heap:
            raise ValueError('set is empty')
        return self.heap[0] + self.offset

    def __len__(self):
        """Implement the len operator."""
        return self.size
