def transitive_closure(graph):
    """Return bit masks: bit v of reach[u] is set iff u can reach v."""
    reach = []
    for u, adjacent in enumerate(graph):
        mask = 1 << u
        for v in adjacent:
            mask |= 1 << v
        reach.append(mask)
    for middle in range(len(graph)):
        bit = 1 << middle
        for u in range(len(graph)):
            if reach[u] & bit:
                reach[u] |= reach[middle]
    return reach
