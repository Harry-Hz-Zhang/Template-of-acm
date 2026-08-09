from collections import deque


def maximum_matching(graph):
    """Edmonds blossom: return mate[v], where -1 means unmatched."""
    n = len(graph)
    match = [-1] * n
    parent = [-1] * n
    base = list(range(n))

    def lca(a, b):
        """Run the lca operation."""
        used = [False] * n
        while True:
            a = base[a]
            used[a] = True
            if match[a] == -1:
                break
            a = parent[match[a]]
        while True:
            b = base[b]
            if used[b]:
                return b
            b = parent[match[b]]

    def mark_path(vertex, root, child, blossom):
        """Run the mark path operation."""
        while base[vertex] != root:
            blossom[base[vertex]] = blossom[base[match[vertex]]] = True
            parent[vertex] = child
            child = match[vertex]
            vertex = parent[match[vertex]]

    def augment(start):
        """Run the augment operation."""
        nonlocal parent, base
        used = [False] * n
        parent = [-1] * n
        base = list(range(n))
        queue = deque([start])
        used[start] = True
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if base[u] == base[v] or match[u] == v:
                    continue
                if v == start or (match[v] != -1 and parent[match[v]] != -1):
                    root = lca(u, v)
                    blossom = [False] * n
                    mark_path(u, root, v, blossom)
                    mark_path(v, root, u, blossom)
                    for x in range(n):
                        if blossom[base[x]]:
                            base[x] = root
                            if not used[x]:
                                used[x] = True
                                queue.append(x)
                elif parent[v] == -1:
                    parent[v] = u
                    if match[v] == -1:
                        x = v
                        while x != -1:
                            p = parent[x]
                            next_x = match[p] if p != -1 else -1
                            match[x] = p
                            if p != -1:
                                match[p] = x
                            x = next_x
                        return True
                    v = match[v]
                    used[v] = True
                    queue.append(v)
        return False

    for vertex in range(n):
        if match[vertex] == -1:
            augment(vertex)
    return match
