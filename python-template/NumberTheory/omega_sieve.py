def omega_sieve(limit):
    """Return omega[n]: number of distinct prime factors of n."""
    omega = [0] * (limit + 1)
    for prime in range(2, limit + 1):
        if omega[prime] == 0:
            for multiple in range(prime, limit + 1, prime):
                omega[multiple] += 1
    return omega
