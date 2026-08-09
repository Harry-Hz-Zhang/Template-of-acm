class RollingHash(object):
    def __init__(self, sequence, base=911382323, modulus=972663749):
        """Initialize the data structure."""
        self.modulus = modulus
        self.power = [1] * (len(sequence) + 1)
        self.prefix = [0] * (len(sequence) + 1)
        for i, value in enumerate(sequence):
            number = value if isinstance(value, int) else ord(value)
            self.power[i + 1] = self.power[i] * base % modulus
            self.prefix[i + 1] = (self.prefix[i] * base + number + 1) % modulus

    def hash(self, left, right):
        """Run the hash operation."""
        return (self.prefix[right] - self.prefix[left] * self.power[right - left]) % self.modulus
