def divisor_sieve(limit):
    """Run the divisor sieve operation."""
    divisors = [[] for _ in range(limit + 1)]
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            divisors[multiple].append(divisor)
    return divisors
