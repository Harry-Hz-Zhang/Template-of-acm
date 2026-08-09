def linear_sieve(limit):
    """Return (primes, minimum_prime, phi, mu) for 0..limit."""
    minimum_prime = [0] * (limit + 1)
    phi = [0] * (limit + 1)
    mu = [0] * (limit + 1)
    if limit >= 1:
        phi[1] = 1
        mu[1] = 1
    primes = []
    for value in range(2, limit + 1):
        if minimum_prime[value] == 0:
            minimum_prime[value] = value
            phi[value] = value - 1
            mu[value] = -1
            primes.append(value)
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            minimum_prime[product] = prime
            if value % prime == 0:
                phi[product] = phi[value] * prime
                mu[product] = 0
                break
            phi[product] = phi[value] * (prime - 1)
            mu[product] = -mu[value]
    return primes, minimum_prime, phi, mu
