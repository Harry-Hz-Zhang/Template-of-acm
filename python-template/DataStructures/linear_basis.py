class XorLinearBasis(object):
    def __init__(self, max_bit=60):
        """Initialize the data structure."""
        self.max_bit = max_bit
        self.basis = [0] * (max_bit + 1)
        self.rank = 0

    def insert(self, value):
        """Run the insert operation."""
        for bit in range(self.max_bit, -1, -1):
            if not (value >> bit) & 1:
                continue
            if self.basis[bit]:
                value ^= self.basis[bit]
            else:
                self.basis[bit] = value
                self.rank += 1
                return True
        return False

    def can_represent(self, value):
        """Run the can represent operation."""
        for bit in range(self.max_bit, -1, -1):
            if (value >> bit) & 1:
                value ^= self.basis[bit]
        return value == 0

    def max_xor(self, initial=0):
        """Run the max xor operation."""
        result = initial
        for bit in range(self.max_bit, -1, -1):
            result = max(result, result ^ self.basis[bit])
        return result

    def min_xor(self, initial=0):
        """Return the minimum xor value reachable from initial."""
        result = initial
        for bit in range(self.max_bit, -1, -1):
            if self.basis[bit] and (result ^ self.basis[bit]) < result:
                result ^= self.basis[bit]
        return result

    def merge(self, other):
        """Run the merge operation."""
        for value in other.basis:
            if value:
                self.insert(value)
