def prefix_function(pattern):
    """Return KMP prefix lengths for a pattern sequence."""
    prefix = [0] * len(pattern)
    for i in range(1, len(pattern)):
        matched = prefix[i - 1]
        while matched and pattern[i] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[i] == pattern[matched]:
            matched += 1
        prefix[i] = matched
    return prefix


def kmp_search(text, pattern):
    """Return all zero-based matches; an empty pattern has no matches."""
    if not pattern:
        return []
    prefix = prefix_function(pattern)
    positions = []
    matched = 0
    for i, value in enumerate(text):
        while matched and value != pattern[matched]:
            matched = prefix[matched - 1]
        if value == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            positions.append(i - len(pattern) + 1)
            matched = prefix[matched - 1]
    return positions
