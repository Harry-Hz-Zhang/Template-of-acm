import math
import random


def is_prime(value):
    """Deterministic Miller-Rabin for 0 <= value < 2**64."""
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if value % prime == 0:
            return value == prime
    d = value - 1
    exponent = 0
    while d % 2 == 0:
        exponent += 1
        d //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        x = pow(base, d, value)
        if x in (1, value - 1):
            continue
        for _ in range(exponent - 1):
            x = x * x % value
            if x == value - 1:
                break
        else:
            return False
    return True


def pollard_rho(value):
    """Run the pollard rho operation."""
    if value % 2 == 0:
        return 2
    if value % 3 == 0:
        return 3
    while True:
        constant = random.randrange(1, value)
        x = random.randrange(0, value)
        y = x
        divisor = 1
        while divisor == 1:
            x = (x * x + constant) % value
            y = (y * y + constant) % value
            y = (y * y + constant) % value
            divisor = math.gcd(abs(x - y), value)
        if divisor != value:
            return divisor


def factorize(value):
    """Return sorted prime factors with repetition."""
    if value <= 0:
        raise ValueError('value must be positive')
    factors = []

    def split(current):
        """Run the split operation."""
        if current == 1:
            return
        if is_prime(current):
            factors.append(current)
            return
        divisor = pollard_rho(current)
        split(divisor)
        split(current // divisor)

    split(value)
    return sorted(factors)
