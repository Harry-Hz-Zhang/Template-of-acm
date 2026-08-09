def partition_numbers(limit, modulus=None):
    """Return p(0)..p(limit) using Euler's pentagonal recurrence."""
    partitions = [0] * (limit + 1)
    partitions[0] = 1
    for n in range(1, limit + 1):
        k = 1
        while k * (3 * k - 1) // 2 <= n:
            sign = 1 if k % 2 else -1
            first = k * (3 * k - 1) // 2
            second = k * (3 * k + 1) // 2
            partitions[n] += sign * partitions[n - first]
            if second <= n:
                partitions[n] += sign * partitions[n - second]
            k += 1
        if modulus is not None:
            partitions[n] %= modulus
    return partitions


def partitions_exact_parts(total, parts, modulus=None):
    """Count partitions of total into exactly parts positive integers."""
    dp = [[0] * (parts + 1) for _ in range(total + 1)]
    dp[0][0] = 1
    for value in range(1, total + 1):
        for current in range(value, total + 1):
            for count in range(1, parts + 1):
                dp[current][count] += dp[current - value][count - 1]
                if modulus is not None:
                    dp[current][count] %= modulus
    return dp[total][parts]


def _combination(n, k):
    """Return an exact binomial coefficient without newer math APIs."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for value in range(1, k + 1):
        result = result * (n - value + 1) // value
    return result


def identical_balls_distinct_boxes(total, boxes, allow_empty=True):
    """Count distributions of identical balls into labeled boxes."""
    if total < 0 or boxes < 0:
        raise ValueError('counts must be nonnegative')
    if boxes == 0:
        return int(total == 0)
    if allow_empty:
        return _combination(total + boxes - 1, boxes - 1)
    return _combination(total - 1, boxes - 1) if total else 0


def distinct_balls_distinct_boxes(total, boxes, allow_empty=True):
    """Count distributions of labeled balls into labeled boxes."""
    if total < 0 or boxes < 0:
        raise ValueError('counts must be nonnegative')
    if allow_empty:
        return boxes ** total if boxes else int(total == 0)
    return sum((-1) ** missing * _combination(boxes, missing) * (boxes - missing) ** total
               for missing in range(boxes + 1))


def distinct_balls_identical_boxes(total, boxes):
    """Count partitions of labeled balls into nonempty unlabeled boxes."""
    if total < 0 or boxes < 0:
        raise ValueError('counts must be nonnegative')
    dp = [0] * (boxes + 1)
    dp[0] = 1
    for _ in range(total):
        for count in range(boxes, 0, -1):
            dp[count] = dp[count - 1] + count * dp[count]
        dp[0] = 0
    return dp[boxes]


def identical_balls_identical_boxes(total, boxes, allow_empty=True, modulus=None):
    """Count partitions of identical balls into unlabeled boxes."""
    if total < 0 or boxes < 0:
        raise ValueError('counts must be nonnegative')
    if not allow_empty:
        return partitions_exact_parts(total, boxes, modulus)
    result = sum(partitions_exact_parts(total, count, modulus)
                 for count in range(min(total, boxes) + 1))
    return result if modulus is None else result % modulus
