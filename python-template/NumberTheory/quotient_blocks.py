def quotient_blocks(n):
    """Yield maximal inclusive [left, right] with constant n // index."""
    left = 1
    while left <= n:
        quotient = n // left
        right = n // quotient
        yield left, right, quotient
        left = right + 1
