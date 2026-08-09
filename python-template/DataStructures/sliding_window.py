from collections import deque


def sliding_window_minimum(values, window_size):
    """Run the sliding window minimum operation."""
    if window_size <= 0:
        raise ValueError('window_size must be positive')
    queue = deque()
    result = []
    for i, value in enumerate(values):
        while queue and values[queue[-1]] >= value:
            queue.pop()
        queue.append(i)
        if queue[0] <= i - window_size:
            queue.popleft()
        if i + 1 >= window_size:
            result.append(values[queue[0]])
    return result


def sliding_window_maximum(values, window_size):
    """Run the sliding window maximum operation."""
    return [-x for x in sliding_window_minimum([-x for x in values], window_size)]
