def tree_diameter(graph):
    """Weighted tree with nonnegative weights. Return (distance, vertex_path)."""
    if not graph:
        return 0, []

    def farthest(start):
        """Run the farthest operation."""
        distance = [-1] * len(graph)
        parent = [-1] * len(graph)
        distance[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v, weight in graph[u]:
                if v != parent[u]:
                    parent[v] = u
                    distance[v] = distance[u] + weight
                    stack.append(v)
        end = max(range(len(graph)), key=distance.__getitem__)
        return end, distance, parent

    start, _, _ = farthest(0)
    end, distance, parent = farthest(start)
    path = []
    u = end
    while u != -1:
        path.append(u)
        if u == start:
            break
        u = parent[u]
    path.reverse()
    return distance[end], path
