def prime_factorization(value):
    """Return sorted (prime, exponent) pairs by trial division."""
    if value == 0:
        raise ValueError('zero has no prime factorization')
    value = abs(value)
    factors = []
    prime = 2
    while prime * prime <= value:
        if value % prime == 0:
            exponent = 0
            while value % prime == 0:
                value //= prime
                exponent += 1
            factors.append((prime, exponent))
        prime = 3 if prime == 2 else prime + 2
    if value > 1:
        factors.append((value, 1))
    return factors


def divisors(value):
    """Return all positive divisors in sorted order."""
    if value <= 0:
        raise ValueError('value must be positive')
    result = [1]
    for prime, exponent in prime_factorization(value):
        previous = result[:]
        power = 1
        for _ in range(exponent):
            power *= prime
            result.extend(divisor * power for divisor in previous)
    return sorted(result)


def divisor_count(value):
    """Return the number of positive divisors of a positive integer."""
    if value <= 0:
        raise ValueError('value must be positive')
    result = 1
    for _, exponent in prime_factorization(value):
        result *= exponent + 1
    return result
