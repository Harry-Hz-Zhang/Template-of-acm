class BinomialModPrime(object):
    def __init__(self, limit, modulus):
        """Precompute factorial helpers modulo a prime."""
        if modulus <= 1 or limit < 0 or limit >= modulus:
            raise ValueError('require 0 <= limit < prime modulus')
        self.modulus = modulus
        self.factorial = [1]
        self.inverse_factorial = [1]
        self.power_two = [1]
        self.ensure(limit)

    def ensure(self, limit):
        """Extend all precomputed tables through limit."""
        if limit < len(self.factorial):
            return
        if limit >= self.modulus:
            raise ValueError('factorial table must stay below the modulus')
        old = len(self.factorial) - 1
        self.factorial.extend([1] * (limit - old))
        self.power_two.extend([1] * (limit - old))
        for value in range(old + 1, limit + 1):
            self.factorial[value] = self.factorial[value - 1] * value % self.modulus
            self.power_two[value] = self.power_two[value - 1] * 2 % self.modulus
        self.inverse_factorial.extend([1] * (limit - old))
        self.inverse_factorial[limit] = pow(self.factorial[limit], self.modulus - 2, self.modulus)
        for value in range(limit, old, -1):
            self.inverse_factorial[value - 1] = self.inverse_factorial[value] * value % self.modulus

    def combination(self, n, k):
        """Return C(n, k) modulo the configured prime."""
        if k < 0 or k > n:
            return 0
        self.ensure(n)
        return (self.factorial[n] * self.inverse_factorial[k]
                % self.modulus * self.inverse_factorial[n - k] % self.modulus)

    def permutation(self, n, k):
        """Return A(n, k) modulo the configured prime."""
        if k < 0 or k > n:
            return 0
        self.ensure(n)
        return self.factorial[n] * self.inverse_factorial[n - k] % self.modulus

    def F(self, n):
        """Return n! modulo the configured prime."""
        if n < 0:
            raise ValueError('n must be nonnegative')
        self.ensure(n)
        return self.factorial[n]

    def iF(self, n):
        """Return the modular inverse of n!."""
        if n < 0:
            raise ValueError('n must be nonnegative')
        self.ensure(n)
        return self.inverse_factorial[n]

    def P2(self, n):
        """Return 2 raised to n modulo the configured prime."""
        if n < 0:
            raise ValueError('n must be nonnegative')
        if n < self.modulus:
            self.ensure(n)
            return self.power_two[n]
        return pow(2, n, self.modulus)

    A = permutation
    C = combination


Comb = BinomialModPrime
