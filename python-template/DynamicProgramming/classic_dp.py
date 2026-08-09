import bisect


def zero_one_knapsack(capacity, items):
    """Return the maximum value of a 0/1 knapsack."""
    if capacity < 0 or any(weight < 0 for weight, _ in items):
        raise ValueError('weights and capacity must be nonnegative')
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for current in range(capacity, weight - 1, -1):
            dp[current] = max(dp[current], dp[current - weight] + value)
    return dp[capacity]


def zero_one_knapsack_solution(capacity, items):
    """Return the best value and one list of selected item indices."""
    if capacity < 0 or any(weight < 0 for weight, _ in items):
        raise ValueError('weights and capacity must be nonnegative')
    dp = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for index, (weight, value) in enumerate(items, 1):
        for current in range(capacity + 1):
            dp[index][current] = dp[index - 1][current]
            if weight <= current:
                dp[index][current] = max(dp[index][current], dp[index - 1][current - weight] + value)
    selected = []
    current = capacity
    for index in range(len(items), 0, -1):
        weight, value = items[index - 1]
        if weight <= current and dp[index][current] == dp[index - 1][current - weight] + value \
                and dp[index][current] != dp[index - 1][current]:
            selected.append(index - 1)
            current -= weight
    selected.reverse()
    return dp[-1][capacity], selected


def complete_knapsack(capacity, items):
    """Return the maximum value when every item may be reused."""
    if capacity < 0 or any(weight <= 0 for weight, _ in items):
        raise ValueError('capacity must be nonnegative and weights positive')
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for current in range(weight, capacity + 1):
            dp[current] = max(dp[current], dp[current - weight] + value)
    return dp[capacity]


def bounded_knapsack(capacity, items):
    """Return the maximum value for (weight, value, count) items."""
    expanded = []
    for weight, value, count in items:
        if weight <= 0 or count < 0:
            raise ValueError('weights must be positive and counts nonnegative')
        block = 1
        while count:
            take = min(block, count)
            expanded.append((weight * take, value * take))
            count -= take
            block <<= 1
    return zero_one_knapsack(capacity, expanded)


def longest_increasing_subsequence(values):
    """Return one strictly increasing longest subsequence."""
    if not values:
        return []
    tails, tail_indices = [], []
    previous = [-1] * len(values)
    for index, value in enumerate(values):
        position = bisect.bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
            tail_indices.append(index)
        else:
            tails[position] = value
            tail_indices[position] = index
        if position:
            previous[index] = tail_indices[position - 1]
    result = []
    index = tail_indices[-1]
    while index != -1:
        result.append(values[index])
        index = previous[index]
    return result[::-1]


def lis_length(values):
    """Return the length of a strictly increasing subsequence."""
    tails = []
    for value in values:
        position = bisect.bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)


def longest_common_subsequence(first, second):
    """Return one longest common subsequence."""
    dp = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i, left in enumerate(first, 1):
        for j, right in enumerate(second, 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if left == right else max(dp[i - 1][j], dp[i][j - 1])
    result = []
    i, j = len(first), len(second)
    while i and j:
        if first[i - 1] == second[j - 1]:
            result.append(first[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    result.reverse()
    return ''.join(result) if isinstance(first, str) and isinstance(second, str) else result


def maximum_subarray(values, allow_empty=False):
    """Return (sum, left, right) for a maximum half-open subarray."""
    if not values:
        if allow_empty:
            return 0, 0, 0
        raise ValueError('values must be nonempty')
    best_sum = 0 if allow_empty else values[0]
    best_left = best_right = 0
    current_sum = 0
    current_left = 0
    for index, value in enumerate(values):
        if current_sum < 0:
            current_sum, current_left = 0, index
        current_sum += value
        if current_sum > best_sum or not allow_empty and best_right == 0:
            best_sum, best_left, best_right = current_sum, current_left, index + 1
    return best_sum, best_left, best_right
