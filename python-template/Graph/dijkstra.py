import heapq


INF = float('inf')


def dijkstra(graph, source):
    """graph[u] contains (v, nonnegative_weight)."""
    n = len(graph)
    distance = [INF] * n
    parent = [-1] * n
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        dist_u, u = heapq.heappop(heap)
        if dist_u != distance[u]:
            continue
        for v, weight in graph[u]:
            new_distance = dist_u + weight
            if new_distance < distance[v]:
                distance[v] = new_distance
                parent[v] = u
                heapq.heappush(heap, (new_distance, v))
    return distance, parent
