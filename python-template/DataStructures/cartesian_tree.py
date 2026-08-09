def cartesian_tree(values, minimum=True):
    """Return 1-based root, parent, left child, and right child arrays."""
    values = [None] + list(values)
    n = len(values) - 1
    parent = [0] * (n + 1)
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    stack = []
    better = (lambda a, b: a < b) if minimum else (lambda a, b: a > b)
    for index in range(1, n + 1):
        last = 0
        while stack and better(values[index], values[stack[-1]]):
            last = stack.pop()
        if stack:
            parent[index] = stack[-1]
            right[stack[-1]] = index
        if last:
            parent[last] = index
            left[index] = last
        stack.append(index)
    return (stack[0] if stack else 0), parent, left, right
