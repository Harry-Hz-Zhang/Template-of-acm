lowbit = lambda value: value & -value
floor_log2 = lambda value: value.bit_length() - 1
count_trailing_zeros = lambda value: (value & -value).bit_length() - 1


def submasks(mask, include_zero=False):
    """Run the submasks operation."""
    current = mask
    while current:
        yield current
        current = (current - 1) & mask
    if include_zero:
        yield 0
