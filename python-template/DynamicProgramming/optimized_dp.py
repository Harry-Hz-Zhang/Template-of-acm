from collections import deque


def waterline_sequence_count(values, modulus=None):
    """Run the global-offset waterline recurrence from the C++ template."""
    offset, total = 0, 1
    states = {0: 1}
    for value in values:
        offset -= value
        key = value + offset
        old = states.get(key, 0)
        added = total - old
        states[key] = total
        total += added
        if modulus is not None:
            states[key] %= modulus
            total %= modulus
    return total


def minimum_interval_increments(target):
    """Return the minimum +1 interval operations needed from an all-zero array."""
    if any(value < 0 for value in target):
        raise ValueError('target values must be nonnegative')
    previous = 0
    result = 0
    for value in target:
        result += max(0, value - previous)
        previous = value
    return result


def maximum_subarray_ceiling_penalty(values, block_size, penalty):
    """Maximize subarray sum minus penalty times its ceiling block count."""
    if block_size <= 0:
        raise ValueError('block size must be positive')
    answer = 0
    for offset in range(block_size):
        current = 0
        for start in range(offset, len(values), block_size):
            block_sum = 0
            for index in range(start, min(len(values), start + block_size)):
                block_sum += values[index]
                answer = max(answer, current + block_sum - penalty)
            current = max(0, current + block_sum - penalty)
    return answer


def sliding_window_min_dp(costs, window, lower_bounds=None):
    """Solve dp[i] = cost[i] + min(dp[j]) over a bounded predecessor window."""
    if window <= 0:
        raise ValueError('window must be positive')
    lower_bounds = [0] * len(costs) if lower_bounds is None else list(lower_bounds)
    if len(lower_bounds) != len(costs):
        raise ValueError('lower bound count must match costs')
    dp = [0] + [float('inf')] * len(costs)
    queue = deque([0])
    for position, cost in enumerate(costs, 1):
        minimum = max(0, position - window, lower_bounds[position - 1])
        while queue and queue[0] < minimum:
            queue.popleft()
        if not queue:
            raise ValueError('no valid predecessor')
        dp[position] = dp[queue[0]] + cost
        while queue and dp[position] <= dp[queue[-1]]:
            queue.pop()
        queue.append(position)
    return dp


def rooted_subtree_choice_counts(tree, root=0, modulus=None):
    """Return product(child_count + 1) for every rooted subtree."""
    parent = [-1] * len(tree)
    order = [root]
    for u in order:
        for v in tree[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    result = [1] * len(tree)
    for u in reversed(order):
        for v in tree[u]:
            if parent[v] == u:
                result[u] *= result[v] + 1
                if modulus is not None:
                    result[u] %= modulus
    return result
