def _validate(permutation):
    """Validate a zero-based permutation."""
    if sorted(permutation) != list(range(len(permutation))):
        raise ValueError('values must form a zero-based permutation')


def inverse_permutation(permutation):
    """Return the inverse of a zero-based permutation."""
    permutation = list(permutation)
    _validate(permutation)
    inverse = [0] * len(permutation)
    for index, value in enumerate(permutation):
        inverse[value] = index
    return inverse


def compose_permutations(first, second):
    """Return second[first[i]] for two zero-based permutations."""
    first, second = list(first), list(second)
    _validate(first)
    _validate(second)
    if len(first) != len(second):
        raise ValueError('permutation sizes must match')
    return [second[first[index]] for index in range(len(first))]


def sorting_swaps(values):
    """Return stable zero-based swaps that sort a value sequence."""
    target = sorted(range(len(values)), key=lambda index: (values[index], index))
    permutation = inverse_permutation(target)
    swaps = []
    for index in range(len(values)):
        while permutation[index] != index:
            other = permutation[index]
            swaps.append((index, other))
            permutation[index], permutation[other] = permutation[other], permutation[index]
    return swaps
