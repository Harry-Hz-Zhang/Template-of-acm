import heapq
from collections import Counter


class DualHeap:
    """Dynamic lower median and sum of absolute deviations."""

    def __init__(self):
        """Initialize the data structure."""
        self.low = []
        self.high = []
        self.delayed_low = Counter()
        self.delayed_high = Counter()
        self.count = Counter()
        self.low_size = self.high_size = 0
        self.low_sum = self.high_sum = 0

    @staticmethod
    def _prune(heap, delayed, sign):
        """Run the internal prune step."""
        while heap and delayed[sign * heap[0]]:
            value = sign * heapq.heappop(heap)
            delayed[value] -= 1

    def _balance(self):
        """Run the internal balance step."""
        self._prune(self.low, self.delayed_low, -1)
        self._prune(self.high, self.delayed_high, 1)
        if self.low_size > self.high_size + 1:
            value = -heapq.heappop(self.low)
            self.low_size -= 1
            self.low_sum -= value
            heapq.heappush(self.high, value)
            self.high_size += 1
            self.high_sum += value
        elif self.low_size < self.high_size:
            value = heapq.heappop(self.high)
            self.high_size -= 1
            self.high_sum -= value
            heapq.heappush(self.low, -value)
            self.low_size += 1
            self.low_sum += value
        self._prune(self.low, self.delayed_low, -1)
        self._prune(self.high, self.delayed_high, 1)

    def add(self, value):
        """Run the add operation."""
        self.count[value] += 1
        if not self.low or value <= -self.low[0]:
            heapq.heappush(self.low, -value)
            self.low_size += 1
            self.low_sum += value
        else:
            heapq.heappush(self.high, value)
            self.high_size += 1
            self.high_sum += value
        self._balance()

    def discard(self, value):
        """Run the discard operation."""
        if not self.count[value]:
            return False
        self.count[value] -= 1
        if value <= -self.low[0]:
            self.delayed_low[value] += 1
            self.low_size -= 1
            self.low_sum -= value
            if value == -self.low[0]:
                self._prune(self.low, self.delayed_low, -1)
        else:
            self.delayed_high[value] += 1
            self.high_size -= 1
            self.high_sum -= value
            if self.high and value == self.high[0]:
                self._prune(self.high, self.delayed_high, 1)
        self._balance()
        return True

    def median(self):
        """Run the median operation."""
        if not self.low_size:
            raise ValueError('heap is empty')
        return -self.low[0]

    def deviation_sum(self):
        """Run the deviation sum operation."""
        median = self.median()
        return median * self.low_size - self.low_sum + self.high_sum - median * self.high_size

    def __len__(self):
        """Implement the len operator."""
        return self.low_size + self.high_size
