import bisect


def first_true(left, right, predicate):
    """Return the first true integer in [left, right), or right."""
    while left < right:
        middle = (left + right) // 2
        if predicate(middle):
            right = middle
        else:
            left = middle + 1
    return left


def last_true(left, right, predicate):
    """Return the last true integer in [left, right], or left - 1."""
    answer = left - 1
    while left <= right:
        middle = (left + right) // 2
        if predicate(middle):
            answer, left = middle, middle + 1
        else:
            right = middle - 1
    return answer


def first_true_real(left, right, predicate, iterations=80):
    """Approximate a false-to-true boundary on a real interval."""
    if iterations < 0:
        raise ValueError('iterations must be nonnegative')
    for _ in range(iterations):
        middle = (left + right) / 2.0
        if predicate(middle):
            right = middle
        else:
            left = middle
    return right


def ternary_search(left, right, function, maximize=False, iterations=120):
    """Return an approximate extremum point and value of a unimodal function."""
    if iterations < 0:
        raise ValueError('iterations must be nonnegative')
    for _ in range(iterations):
        first = left + (right - left) / 3.0
        second = right - (right - left) / 3.0
        move_left = function(first) < function(second)
        if move_left == maximize:
            left = first
        else:
            right = second
    point = (left + right) / 2.0
    return point, function(point)


class BidirectionalMap(object):
    """Maintain a 1-based permutation and its inverse under swaps."""

    def __init__(self, size):
        """Create the identity mapping on 1 through size."""
        if size < 0:
            raise ValueError('size must be nonnegative')
        self.actual = list(range(size + 1))
        self.internal = list(range(size + 1))

    def swap_actual(self, first, second):
        """Swap two actual labels while updating the inverse map."""
        if not 1 <= first < len(self.actual) or not 1 <= second < len(self.actual):
            raise IndexError('label is out of range')
        left, right = self.actual[first], self.actual[second]
        self.actual[first], self.actual[second] = right, left
        self.internal[left], self.internal[right] = second, first

    def to_internal(self, actual):
        """Map an actual label to its current internal label."""
        return self.actual[actual]

    def to_actual(self, internal):
        """Map an internal label back to its current actual label."""
        return self.internal[internal]


def coordinate_compress(values, start=0):
    """Return sorted unique values and each value's compressed rank."""
    unique = sorted(set(values))
    return unique, [bisect.bisect_left(unique, value) + start for value in values]
