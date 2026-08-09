import math


def bash_winning(stones, maximum_take):
    """Return whether the first player wins the normal Bash game."""
    if stones < 0 or maximum_take <= 0:
        raise ValueError('require nonnegative stones and a positive move limit')
    return stones % (maximum_take + 1) != 0


def nim_winning(heaps):
    """Return whether a normal Nim position is winning."""
    value = 0
    for heap in heaps:
        if heap < 0:
            raise ValueError('heap sizes must be nonnegative')
        value ^= heap
    return value != 0


def anti_nim_winning(heaps):
    """Return whether a misere Nim position is winning."""
    heaps = [heap for heap in heaps if heap]
    if any(heap < 0 for heap in heaps):
        raise ValueError('heap sizes must be nonnegative')
    if not heaps:
        return False
    if all(heap == 1 for heap in heaps):
        return len(heaps) % 2 == 0
    return nim_winning(heaps)


def wythoff_winning(first, second):
    """Return whether a Wythoff Nim position is winning."""
    if first < 0 or second < 0:
        raise ValueError('heap sizes must be nonnegative')
    first, second = sorted((first, second))
    difference = second - first
    return first != int(difference * (1.0 + math.sqrt(5.0)) / 2.0)


def fibonacci_game_winning(stones):
    """Return whether the first player wins the Fibonacci take-away game."""
    if stones <= 0:
        raise ValueError('stones must be positive')
    first, second = 1, 2
    while first < stones:
        first, second = second, first + second
    return first != stones


def subtraction_game_sg(limit, moves):
    """Return SG values for removing any amount in moves."""
    if limit < 0 or any(move <= 0 for move in moves):
        raise ValueError('require nonnegative limit and positive moves')
    moves = sorted(set(moves))
    sg = [0] * (limit + 1)
    for state in range(1, limit + 1):
        reachable = {sg[state - move] for move in moves if move <= state}
        value = 0
        while value in reachable:
            value += 1
        sg[state] = value
    return sg


def tree_grundy(tree, root=0):
    """Return the rooted Green Hackenbush Grundy value."""
    parent = [-1] * len(tree)
    order = [root]
    for u in order:
        for v in tree[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    values = [0] * len(tree)
    for u in reversed(order):
        for v in tree[u]:
            if parent[v] == u:
                values[u] ^= values[v] + 1
    return values[root]
