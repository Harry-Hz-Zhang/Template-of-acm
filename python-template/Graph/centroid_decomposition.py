def centroid_decomposition(graph):
    """Return (centroid_parent, centroid_root) for a tree."""
    n = len(graph)
    if n == 0:
        return [], -1
    removed = [False] * n
    centroid_parent = [-1] * n
    traversal_parent = [-1] * n
    size = [0] * n
    tasks = [(0, -1)]
    root = -1
    while tasks:
        start, decomposition_parent = tasks.pop()
        if removed[start]:
            continue
        component = []
        traversal_parent[start] = -1
        stack = [start]
        while stack:
            u = stack.pop()
            component.append(u)
            for v in graph[u]:
                if not removed[v] and v != traversal_parent[u]:
                    traversal_parent[v] = u
                    stack.append(v)
        for u in reversed(component):
            size[u] = 1 + sum(size[v] for v in graph[u]
                              if not removed[v] and traversal_parent[v] == u)
        total = len(component)
        centroid = next(
            u for u in component
            if max([total - size[u]] + [size[v] for v in graph[u]
                    if not removed[v] and traversal_parent[v] == u]) * 2 <= total
        )
        centroid_parent[centroid] = decomposition_parent
        if decomposition_parent == -1:
            root = centroid
        removed[centroid] = True
        tasks.extend((v, centroid) for v in graph[centroid] if not removed[v])
    return centroid_parent, root
