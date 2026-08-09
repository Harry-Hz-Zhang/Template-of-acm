def strongly_connected_components(graph):
    """Kosaraju: return (component_id, components) for a directed graph."""
    n = len(graph)
    reverse_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            reverse_graph[v].append(u)

    visited = [False] * n
    order = []
    for start in range(n):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            u, index = stack[-1]
            if index < len(graph[u]):
                v = graph[u][index]
                stack[-1] = (u, index + 1)
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

    component_id = [-1] * n
    components = []
    for start in reversed(order):
        if component_id[start] != -1:
            continue
        cid = len(components)
        component = []
        stack = [start]
        component_id[start] = cid
        while stack:
            u = stack.pop()
            component.append(u)
            for v in reverse_graph[u]:
                if component_id[v] == -1:
                    component_id[v] = cid
                    stack.append(v)
        components.append(component)
    return component_id, components
