"""Mo's algorithm helpers for 1-based closed ranges."""


def mo_order(n, queries, block_size=None):
    """Return odd-even Mo query order for 1-based closed ranges."""
    if block_size is None:
        block_size = max(1, int(n ** 0.5))
    return sorted(
        range(len(queries)),
        key=lambda index: (
            queries[index][0] // block_size,
            queries[index][1] if ((queries[index][0] // block_size) & 1) == 0
            else -queries[index][1],
        ),
    )


def mo_distinct_counts(values, queries):
    """Return distinct counts for 1-based closed ranges."""
    n = len(values)
    for left, right in queries:
        if not 1 <= left <= right <= n:
            raise IndexError('range is out of bounds')
    order = mo_order(n, queries)
    frequency = {}
    answer = [0] * len(queries)
    left, right, distinct = 1, 0, 0
    for query_id in order:
        query_left, query_right = queries[query_id]
        while left > query_left:
            left -= 1
            value = values[left - 1]
            frequency[value] = frequency.get(value, 0) + 1
            distinct += frequency[value] == 1
        while right < query_right:
            right += 1
            value = values[right - 1]
            frequency[value] = frequency.get(value, 0) + 1
            distinct += frequency[value] == 1
        while left < query_left:
            value = values[left - 1]
            frequency[value] -= 1
            distinct -= frequency[value] == 0
            left += 1
        while right > query_right:
            value = values[right - 1]
            frequency[value] -= 1
            distinct -= frequency[value] == 0
            right -= 1
        answer[query_id] = distinct
    return answer


def mo_even_distinct(values, queries):
    """Return whether each closed range has an even distinct count."""
    return [count % 2 == 0 for count in mo_distinct_counts(values, queries)]


def mo_process(n, queries, add, remove, get_answer):
    """Run generic Mo callbacks on 1-based closed ranges."""
    for left, right in queries:
        if not 1 <= left <= right <= n:
            raise IndexError('range is out of bounds')
    answers = [None] * len(queries)
    left, right = 1, 0
    for query_id in mo_order(n, queries):
        query_left, query_right = queries[query_id]
        while left > query_left:
            left -= 1
            add(left)
        while right < query_right:
            right += 1
            add(right)
        while left < query_left:
            remove(left)
            left += 1
        while right > query_right:
            remove(right)
            right -= 1
        answers[query_id] = get_answer()
    return answers


def mo_frequent_values(values, queries):
    """Return sorted values whose range frequency exceeds each threshold."""
    ranges = [(left, right) for left, right, _ in queries]
    n = len(values)
    for left, right, threshold in queries:
        if not 1 <= left <= right <= n:
            raise IndexError('range is out of bounds')
        if threshold < 0:
            raise ValueError('threshold must be nonnegative')
    unique = sorted(set(values))
    index = {value: i for i, value in enumerate(unique)}
    size = 1
    while size < len(unique):
        size <<= 1
    tree = [0] * (2 * size)
    frequency = [0] * len(unique)

    def update(position, delta):
        """Update one compressed frequency in the max tree."""
        frequency[position] += delta
        node = size + position
        tree[node] = frequency[position]
        node //= 2
        while node:
            tree[node] = max(tree[node * 2], tree[node * 2 + 1])
            node //= 2

    def collect(node, left, right, threshold, result):
        """Collect leaves whose frequency exceeds the threshold."""
        if tree[node] <= threshold:
            return
        if right - left == 1:
            if left < len(unique):
                result.append(unique[left])
            return
        middle = (left + right) // 2
        collect(node * 2, left, middle, threshold, result)
        collect(node * 2 + 1, middle, right, threshold, result)

    answers = [None] * len(queries)
    left, right = 1, 0
    for query_id in mo_order(n, ranges):
        query_left, query_right, threshold = queries[query_id]
        while left > query_left:
            left -= 1
            update(index[values[left - 1]], 1)
        while right < query_right:
            right += 1
            update(index[values[right - 1]], 1)
        while left < query_left:
            update(index[values[left - 1]], -1)
            left += 1
        while right > query_right:
            update(index[values[right - 1]], -1)
            right -= 1
        result = []
        collect(1, 0, size, threshold, result)
        answers[query_id] = result
    return answers
