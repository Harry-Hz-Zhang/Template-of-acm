def catalan_numbers(limit, modulus=None):
    """Run the catalan numbers operation."""
    catalan = [0] * (limit + 1)
    catalan[0] = 1
    for n in range(1, limit + 1):
        catalan[n] = sum(catalan[left] * catalan[n - 1 - left] for left in range(n))
        if modulus is not None:
            catalan[n] %= modulus
    return catalan
