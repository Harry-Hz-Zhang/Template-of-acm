def tree_centroids(graph):
    """Return the one or two centroids of a tree."""
    n = len(graph)
    if n == 0:
        return []
    parent = [-1] * n
    order = [0]
    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    size = [1] * n
    for u in reversed(order):
        for v in graph[u]:
            if parent[v] == u:
                size[u] += size[v]
    return [u for u in range(n) if max([n - size[u]] + [size[v] for v in graph[u] if parent[v] == u]) * 2 <= n]
