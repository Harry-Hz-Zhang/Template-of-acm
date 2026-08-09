def euler_phi(value):
    """Run the euler phi operation."""
    if value <= 0:
        raise ValueError('value must be positive')
    result = value
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        if remaining % prime == 0:
            while remaining % prime == 0:
                remaining //= prime
            result -= result // prime
        prime = 3 if prime == 2 else prime + 2
    if remaining > 1:
        result -= result // remaining
    return result
