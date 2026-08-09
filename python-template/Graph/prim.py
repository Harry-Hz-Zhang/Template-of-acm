import heapq


def prim(graph, start=0):
    """graph[u] contains (v, weight). Return (MST weight, parent), or (None, parent)."""
    n = len(graph)
    if n == 0:
        return 0, []
    parent = [-1] * n
    used = [False] * n
    heap = [(0, start, -1)]
    total = 0
    count = 0
    while heap:
        weight, u, p = heapq.heappop(heap)
        if used[u]:
            continue
        used[u] = True
        parent[u] = p
        total += weight
        count += 1
        for v, edge_weight in graph[u]:
            if not used[v]:
                heapq.heappush(heap, (edge_weight, v, u))
    return (total, parent) if count == n else (None, parent)
