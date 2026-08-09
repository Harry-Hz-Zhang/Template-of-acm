import sys


def bridges_and_articulation_points(graph):
    """Undirected graph adjacency list; parallel edges must appear separately."""
    sys.setrecursionlimit(max(1000, 2 * len(graph) + 10))
    n = len(graph)
    timer = [0]
    tin = [-1] * n
    low = [0] * n
    articulation = [False] * n
    bridges = []

    def dfs(u, parent, skipped_parent_edge):
        """Run the dfs operation."""
        tin[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in graph[u]:
            if v == parent and not skipped_parent_edge[0]:
                skipped_parent_edge[0] = True
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u, [False])
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.append((min(u, v), max(u, v)))
                if parent != -1 and low[v] >= tin[u]:
                    articulation[u] = True
                children += 1
        if parent == -1 and children > 1:
            articulation[u] = True

    for u in range(n):
        if tin[u] == -1:
            dfs(u, -1, [False])
    return sorted(bridges), [u for u in range(n) if articulation[u]]
