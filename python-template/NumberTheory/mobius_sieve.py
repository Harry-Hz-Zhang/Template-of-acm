def mobius_sieve(limit):
    """Run the mobius sieve operation."""
    mu = [1] * (limit + 1)
    is_prime = [True] * (limit + 1)
    for prime in range(2, limit + 1):
        if not is_prime[prime]:
            continue
        for multiple in range(prime, limit + 1, prime):
            is_prime[multiple] = False
            mu[multiple] *= -1
        square = prime * prime
        for multiple in range(square, limit + 1, square):
            mu[multiple] = 0
    if limit >= 0:
        mu[0] = 0
    return mu
