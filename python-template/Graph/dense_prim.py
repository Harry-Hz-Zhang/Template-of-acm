INF = float('inf')


def dense_prim(matrix):
    """O(n^2) MST from an adjacency matrix; missing edges are INF."""
    n = len(matrix)
    if n == 0:
        return 0, []
    distance = [INF] * n
    parent = [-1] * n
    used = [False] * n
    distance[0] = 0
    total = 0
    for _ in range(n):
        u = min((v for v in range(n) if not used[v]), key=distance.__getitem__)
        if distance[u] == INF:
            return None, parent
        used[u] = True
        total += distance[u]
        for v in range(n):
            if not used[v] and matrix[u][v] < distance[v]:
                distance[v] = matrix[u][v]
                parent[v] = u
    return total, parent
