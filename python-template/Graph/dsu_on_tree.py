import sys


def dsu_on_tree(graph, add, remove, answer, root=0):
    """Run sack/DSU-on-tree callbacks add(vertex), remove(vertex), answer(vertex)."""
    n = len(graph)
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 100))
    parent = [-1] * n
    size = [1] * n
    heavy = [-1] * n
    tin = [0] * n
    tout = [0] * n
    order = []
    stack = [(root, -1, 0)]
    while stack:
        u, p, state = stack.pop()
        if state == 0:
            parent[u] = p
            tin[u] = len(order)
            order.append(u)
            stack.append((u, p, 1))
            for v in reversed(graph[u]):
                if v != p:
                    stack.append((v, u, 0))
        else:
            for v in graph[u]:
                if parent[v] == u:
                    size[u] += size[v]
                    if heavy[u] == -1 or size[v] > size[heavy[u]]:
                        heavy[u] = v
            tout[u] = len(order)

    def solve(u, keep):
        """Run the solve operation."""
        for v in graph[u]:
            if parent[v] == u and v != heavy[u]:
                solve(v, False)
        if heavy[u] != -1:
            solve(heavy[u], True)
        for v in graph[u]:
            if parent[v] == u and v != heavy[u]:
                for index in range(tin[v], tout[v]):
                    add(order[index])
        add(u)
        answer(u)
        if not keep:
            for index in range(tin[u], tout[u]):
                remove(order[index])

    solve(root, True)
