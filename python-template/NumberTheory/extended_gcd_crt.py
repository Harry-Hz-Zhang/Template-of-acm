def extended_gcd(a, b):
    """Return (gcd, x, y), with gcd >= 0 and a*x + b*y = gcd."""
    old_r, r = abs(a), abs(b)
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return old_r, old_x if a >= 0 else -old_x, old_y if b >= 0 else -old_y


def modular_inverse(value, modulus):
    """Return a modular inverse, or None when it does not exist."""
    gcd, inverse, _ = extended_gcd(value, modulus)
    if gcd != 1:
        return None
    return inverse % modulus


def lcm(a, b):
    """Return the nonnegative least common multiple of two integers."""
    if not a or not b:
        return 0
    gcd, _, _ = extended_gcd(a, b)
    return abs(a // gcd * b)


def merge_congruences(remainder_a, modulus_a, remainder_b, modulus_b):
    """Merge two possibly non-coprime congruences; return (remainder, modulus) or None."""
    gcd, x, _ = extended_gcd(modulus_a, modulus_b)
    difference = remainder_b - remainder_a
    if difference % gcd:
        return None
    reduced_b = modulus_b // gcd
    multiplier = (difference // gcd * x) % reduced_b
    lcm = modulus_a // gcd * modulus_b
    return (remainder_a + modulus_a * multiplier) % lcm, lcm


def chinese_remainder(congruences):
    """Merge many congruences, including non-coprime moduli."""
    remainder, modulus = 0, 1
    for next_remainder, next_modulus in congruences:
        if next_modulus <= 0:
            raise ValueError('moduli must be positive')
        merged = merge_congruences(remainder, modulus, next_remainder, next_modulus)
        if merged is None:
            return None
        remainder, modulus = merged
    return remainder, modulus
