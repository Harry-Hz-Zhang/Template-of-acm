def find_directed_cycle(graph):
    """Return one closed vertex cycle, or []."""
    state = [0] * len(graph)
    parent = [-1] * len(graph)
    for start in range(len(graph)):
        if state[start]:
            continue
        state[start] = 1
        stack = [(start, 0)]
        while stack:
            u, index = stack[-1]
            if index == len(graph[u]):
                state[u] = 2
                stack.pop()
                continue
            v = graph[u][index]
            stack[-1] = (u, index + 1)
            if state[v] == 0:
                state[v] = 1
                parent[v] = u
                stack.append((v, 0))
            elif state[v] == 1:
                cycle = [v]
                x = u
                while x != v:
                    cycle.append(x)
                    x = parent[x]
                return [v] + list(reversed(cycle[1:])) + [v]
    return []


def find_undirected_cycle(n, edges):
    """edges contains (u, v); return one closed vertex cycle, or []."""
    graph = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        graph[u].append((v, edge_id))
        graph[v].append((u, edge_id))
    state = [0] * n
    parent = [-1] * n
    parent_edge = [-1] * n
    for start in range(n):
        if state[start]:
            continue
        state[start] = 1
        stack = [(start, 0)]
        while stack:
            u, index = stack[-1]
            if index == len(graph[u]):
                state[u] = 2
                stack.pop()
                continue
            v, edge_id = graph[u][index]
            stack[-1] = (u, index + 1)
            if edge_id == parent_edge[u]:
                continue
            if state[v] == 0:
                state[v] = 1
                parent[v] = u
                parent_edge[v] = edge_id
                stack.append((v, 0))
            elif state[v] == 1:
                path = [u]
                while path[-1] != v:
                    path.append(parent[path[-1]])
                return [v] + list(reversed(path[:-1])) + [v]
    return []
