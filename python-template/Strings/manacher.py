def manacher(sequence):
    """Return (odd, even): palindrome radii centered at each position/gap."""
    n = len(sequence)
    odd = [0] * n
    left, right = 0, -1
    for i in range(n):
        radius = 1 if i > right else min(odd[left + right - i], right - i + 1)
        while i - radius >= 0 and i + radius < n and sequence[i - radius] == sequence[i + radius]:
            radius += 1
        odd[i] = radius
        if i + radius - 1 > right:
            left, right = i - radius + 1, i + radius - 1
    even = [0] * n
    left, right = 0, -1
    for i in range(n):
        radius = 0 if i > right else min(even[left + right - i + 1], right - i + 1)
        while i - radius - 1 >= 0 and i + radius < n and sequence[i - radius - 1] == sequence[i + radius]:
            radius += 1
        even[i] = radius
        if i + radius - 1 > right:
            left, right = i - radius, i + radius - 1
    return odd, even


def transformed_radii(sequence):
    """Return radii on the separator-expanded Manacher sequence."""
    transformed = [None]
    for value in sequence:
        transformed.extend((value, None))
    radii = [0] * len(transformed)
    center = right = 0
    for index in range(len(transformed)):
        if index < right:
            radii[index] = min(right - index, radii[2 * center - index])
        while index - radii[index] - 1 >= 0 and index + radii[index] + 1 < len(transformed) \
                and transformed[index - radii[index] - 1] == transformed[index + radii[index] + 1]:
            radii[index] += 1
        if index + radii[index] > right:
            center, right = index, index + radii[index]
    return radii


def longest_palindromic_suffix(sequence):
    """Return the longest suffix that is a palindrome."""
    odd, even = manacher(sequence)
    best = 0
    n = len(sequence)
    for index in range(n):
        if index + odd[index] == n:
            best = max(best, 2 * odd[index] - 1)
        if index + even[index] == n:
            best = max(best, 2 * even[index])
    return sequence[n - best:]
