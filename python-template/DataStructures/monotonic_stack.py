def nearest_strictly_smaller(values):
    """Return 1-based previous/next indices; use 0 and n + 1 when absent."""
    values = [None] + list(values)
    n = len(values) - 1
    previous = [0] * (n + 1)
    stack = []
    for index in range(1, n + 1):
        while stack and values[stack[-1]] >= values[index]:
            stack.pop()
        if stack:
            previous[index] = stack[-1]
        stack.append(index)
    following = [n + 1] * (n + 1)
    following[0] = 0
    stack = []
    for index in range(n, 0, -1):
        while stack and values[stack[-1]] >= values[index]:
            stack.pop()
        if stack:
            following[index] = stack[-1]
        stack.append(index)
    return previous, following
