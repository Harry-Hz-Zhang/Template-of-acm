"""Standalone bit-string helpers."""


class Bitset:
    """Integer-backed bit string with 0-based bit offsets."""

    def __init__(self, size=0, value=0):
        """Initialize the data structure."""
        if size < 0:
            raise ValueError("size must be nonnegative")
        self.n = size
        self.value = value & ((1 << size) - 1 if size else 0)

    @staticmethod
    def mask(left, right):
        """Run the mask operation."""
        if left > right:
            return 0
        return ((1 << (right - left + 1)) - 1) << left

    def add(self, length, value):
        """Append length low-order bits."""
        if length < 0:
            raise ValueError("length must be nonnegative")
        self.value |= (value & ((1 << length) - 1)) << self.n
        self.n += length

    @staticmethod
    def extract(current, left, right):
        """Run the extract operation."""
        if left < 0 or right < left or right >= current.n:
            raise IndexError("bit range is out of range")
        length = right - left + 1
        return Bitset(length, current.value >> left)

    def equal(self, other):
        """Run the equal operation."""
        length = min(self.n, other.n)
        self.value = (~(self.value ^ other.value)) & ((1 << length) - 1 if length else 0)

    def calc(self):
        """Return the number of all-one substrings."""
        result = run = 0
        for index in range(self.n):
            if (self.value >> index) & 1:
                run += 1
                result += run
            else:
                run = 0
        return result

    def __str__(self):
        """Implement the str operator."""
        return ''.join('1' if (self.value >> i) & 1 else '0' for i in range(self.n))
