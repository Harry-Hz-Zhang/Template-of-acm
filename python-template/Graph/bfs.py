from collections import deque


def bfs_shortest_paths(graph, source):
    """Unweighted graph: return (distance, parent), unreachable distance is -1."""
    n = len(graph)
    distance = [-1] * n
    parent = [-1] * n
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
    return distance, parent
