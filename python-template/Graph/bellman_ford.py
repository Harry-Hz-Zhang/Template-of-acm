INF = float('inf')


def bellman_ford(n, edges, source):
    """edges contains (u, v, weight). Return (distance, parent, has_negative_cycle)."""
    distance = [INF] * n
    parent = [-1] * n
    distance[source] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, weight in edges:
            if distance[u] != INF and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                parent[v] = u
                changed = True
        if not changed:
            break
    has_negative_cycle = any(
        distance[u] != INF and distance[u] + weight < distance[v]
        for u, v, weight in edges
    )
    return distance, parent, has_negative_cycle
