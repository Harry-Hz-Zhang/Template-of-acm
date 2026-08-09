from collections import deque


INF = float('inf')


def spfa(graph, source):
    """Return (distance, parent, reachable_negative_cycle)."""
    n = len(graph)
    distance = [INF] * n
    parent = [-1] * n
    relax_count = [0] * n
    in_queue = [False] * n
    distance[source] = 0
    queue = deque([source])
    in_queue[source] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for v, weight in graph[u]:
            if distance[u] + weight >= distance[v]:
                continue
            distance[v] = distance[u] + weight
            parent[v] = u
            relax_count[v] = relax_count[u] + 1
            if relax_count[v] >= n:
                return distance, parent, True
            if not in_queue[v]:
                in_queue[v] = True
                queue.append(v)
    return distance, parent, False
