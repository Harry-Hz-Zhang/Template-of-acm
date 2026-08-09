def directed_eulerian_path(n, edges):
    """Return a vertex path using every directed edge once, or []."""
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    outdegree = [0] * n
    for edge_id, (u, v) in enumerate(edges):
        graph[u].append((v, edge_id))
        outdegree[u] += 1
        indegree[v] += 1
    starts = [u for u in range(n) if outdegree[u] == indegree[u] + 1]
    ends = [u for u in range(n) if indegree[u] == outdegree[u] + 1]
    if len(starts) > 1 or len(ends) > 1:
        return []
    if any(abs(indegree[u] - outdegree[u]) > 1 for u in range(n)):
        return []
    start = starts[0] if starts else next((u for u in range(n) if outdegree[u]), 0)
    index = [0] * n
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        if index[u] < len(graph[u]):
            v, _ = graph[u][index[u]]
            index[u] += 1
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    return path if len(path) == len(edges) + 1 else []


def undirected_eulerian_path(n, edges):
    """Return a vertex path using every undirected edge once, or []."""
    graph = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        graph[u].append((v, edge_id))
        graph[v].append((u, edge_id))
    odd = [u for u in range(n) if len(graph[u]) % 2]
    if len(odd) not in (0, 2):
        return []
    start = odd[0] if odd else next((u for u in range(n) if graph[u]), 0)
    used = [False] * len(edges)
    index = [0] * n
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        while index[u] < len(graph[u]) and used[graph[u][index[u]][1]]:
            index[u] += 1
        if index[u] == len(graph[u]):
            path.append(stack.pop())
        else:
            v, edge_id = graph[u][index[u]]
            used[edge_id] = True
            stack.append(v)
    path.reverse()
    return path if len(path) == len(edges) + 1 else []
