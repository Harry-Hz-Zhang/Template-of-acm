import heapq
from collections import Counter


class TopKSum(object):
    """Maintain the sum and threshold of the k largest values."""

    def __init__(self, k):
        """Create an empty multiset that tracks its k largest values."""
        if k < 0:
            raise ValueError('k must be nonnegative')
        self.k = k
        self.large = []
        self.small = []
        self.large_count = Counter()
        self.small_count = Counter()
        self.delayed_large = Counter()
        self.delayed_small = Counter()
        self.large_size = self.small_size = self.total = 0

    @staticmethod
    def _prune(heap, delayed, sign):
        """Run the internal prune step."""
        while heap and delayed[sign * heap[0]]:
            delayed[sign * heapq.heappop(heap)] -= 1

    def _move_to_large(self):
        """Run the internal move to large step."""
        self._prune(self.small, self.delayed_small, -1)
        value = -heapq.heappop(self.small)
        self.small_count[value] -= 1
        self.small_size -= 1
        heapq.heappush(self.large, value)
        self.large_count[value] += 1
        self.large_size += 1
        self.total += value

    def _move_to_small(self):
        """Run the internal move to small step."""
        self._prune(self.large, self.delayed_large, 1)
        value = heapq.heappop(self.large)
        self.large_count[value] -= 1
        self.large_size -= 1
        self.total -= value
        heapq.heappush(self.small, -value)
        self.small_count[value] += 1
        self.small_size += 1

    def _balance(self):
        """Restore the requested partition size after an update."""
        while self.large_size < self.k and self.small_size:
            self._move_to_large()
        while self.large_size > self.k:
            self._move_to_small()
        self._prune(self.large, self.delayed_large, 1)
        self._prune(self.small, self.delayed_small, -1)

    def add(self, value):
        """Insert one value into the multiset."""
        if self.large_size < self.k:
            heapq.heappush(self.large, value)
            self.large_count[value] += 1
            self.large_size += 1
            self.total += value
        elif self.k and value > self.large[0]:
            self._move_to_small()
            heapq.heappush(self.large, value)
            self.large_count[value] += 1
            self.large_size += 1
            self.total += value
        else:
            heapq.heappush(self.small, -value)
            self.small_count[value] += 1
            self.small_size += 1
        self._balance()

    def discard(self, value):
        """Remove one matching value and report whether it existed."""
        if self.large_count[value]:
            self.large_count[value] -= 1
            self.delayed_large[value] += 1
            self.large_size -= 1
            self.total -= value
        elif self.small_count[value]:
            self.small_count[value] -= 1
            self.delayed_small[value] += 1
            self.small_size -= 1
        else:
            return False
        self._balance()
        return True

    def sum_largest(self):
        """Return the sum of the current k largest values."""
        return self.total

    def kth_largest(self):
        """Return the current k-th largest value."""
        if self.large_size < self.k or self.k == 0:
            raise ValueError('fewer than k values')
        self._prune(self.large, self.delayed_large, 1)
        return self.large[0]

    def change_k(self, k):
        """Change k while preserving all stored values."""
        if k < 0:
            raise ValueError('k must be nonnegative')
        self.k = k
        self._balance()
