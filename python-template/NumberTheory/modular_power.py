def modular_power(base, exponent, modulus):
    """Run the modular power operation."""
    if exponent < 0 or modulus <= 0:
        raise ValueError('exponent must be nonnegative and modulus positive')
    return pow(base, exponent, modulus)
