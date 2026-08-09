from collections import deque


INF = float('inf')


def zero_one_bfs(graph, source):
    """graph[u] contains (v, weight), where weight is 0 or 1."""
    distance = [INF] * len(graph)
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, weight in graph[u]:
            new_distance = distance[u] + weight
            if new_distance < distance[v]:
                distance[v] = new_distance
                if weight == 0:
                    queue.appendleft(v)
                else:
                    queue.append(v)
    return distance
