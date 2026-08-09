def suffix_array(sequence):
    """Return (suffix_array, rank, lcp), where lcp[i]=LCP(sa[i-1], sa[i])."""
    n = len(sequence)
    if n == 0:
        return [], [], []
    values = {value: index for index, value in enumerate(sorted(set(sequence)))}
    rank = [values[value] for value in sequence]
    order = list(range(n))
    length = 1
    while length < n:
        order.sort(key=lambda i: (rank[i], rank[i + length] if i + length < n else -1))
        new_rank = [0] * n
        for i in range(1, n):
            previous = order[i - 1]
            current = order[i]
            previous_key = (rank[previous], rank[previous + length] if previous + length < n else -1)
            current_key = (rank[current], rank[current + length] if current + length < n else -1)
            new_rank[current] = new_rank[previous] + (current_key != previous_key)
        rank = new_rank
        if rank[order[-1]] == n - 1:
            break
        length <<= 1
    inverse = [0] * n
    for position, suffix in enumerate(order):
        inverse[suffix] = position
    lcp = [0] * n
    matched = 0
    for i in range(n):
        position = inverse[i]
        if position == 0:
            continue
        j = order[position - 1]
        while i + matched < n and j + matched < n and sequence[i + matched] == sequence[j + matched]:
            matched += 1
        lcp[position] = matched
        if matched:
            matched -= 1
    return order, inverse, lcp
