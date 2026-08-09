def _extended_gcd(a, b):
    """Run the internal extended gcd step."""
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    gcd, x, y = _extended_gcd(b, a % b)
    return gcd, y, x - (a // b) * y


def solve_linear_diophantine(a, b, c):
    """Return (x0, y0, dx, dy): x=x0+dx*t, y=y0+dy*t; None if impossible."""
    if a == 0 and b == 0:
        return (0, 0, 1, 0) if c == 0 else None
    gcd, x, y = _extended_gcd(a, b)
    if c % gcd:
        return None
    scale = c // gcd
    return x * scale, y * scale, b // gcd, -a // gcd
