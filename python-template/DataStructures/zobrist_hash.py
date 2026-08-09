import random


class ZobristHash(object):
    def __init__(self, seed=0, bits=64):
        """Initialize the data structure."""
        self.random = random.Random(seed)
        self.bits = bits
        self.codes = {}
        self.value = 0

    def toggle(self, item):
        """Run the toggle operation."""
        if item not in self.codes:
            self.codes[item] = self.random.getrandbits(self.bits)
        self.value ^= self.codes[item]
        return self.value

    def digest(self):
        """Run the digest operation."""
        return self.value
