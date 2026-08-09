from collections import Counter


class SafeModProduct(object):
    """Multiplicative multiset product modulo a prime, including zero factors."""

    def __init__(self, modulus):
        """Initialize the data structure."""
        if modulus <= 1:
            raise ValueError('modulus must be greater than one')
        self.modulus = modulus
        self.nonzero_product = 1
        self.zero_count = 0
        self.count = Counter()

    def multiply(self, value):
        """Run the multiply operation."""
        value %= self.modulus
        self.count[value] += 1
        if value == 0:
            self.zero_count += 1
        else:
            self.nonzero_product = self.nonzero_product * value % self.modulus

    def divide(self, value):
        """Run the divide operation."""
        value %= self.modulus
        if not self.count[value]:
            raise ValueError('factor is absent')
        self.count[value] -= 1
        if value == 0:
            self.zero_count -= 1
        else:
            self.nonzero_product = self.nonzero_product * pow(value, self.modulus - 2, self.modulus) % self.modulus

    def value(self):
        """Run the value operation."""
        return 0 if self.zero_count else self.nonzero_product
