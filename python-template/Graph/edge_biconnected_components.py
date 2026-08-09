import sys


def edge_biconnected_components(n, edges):
    """Return (component_id, components, bridge_edge_ids, bridge_tree)."""
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 100))
    graph = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        graph[u].append((v, edge_id))
        graph[v].append((u, edge_id))
    tin = [-1] * n
    low = [0] * n
    bridges = set()
    timer = [0]

    def dfs(u, parent_edge=-1):
        """Run the dfs operation."""
        tin[u] = low[u] = timer[0]
        timer[0] += 1
        for v, edge_id in graph[u]:
            if edge_id == parent_edge:
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, edge_id)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.add(edge_id)

    for u in range(n):
        if tin[u] == -1:
            dfs(u)
    component_id = [-1] * n
    components = []
    for start in range(n):
        if component_id[start] != -1:
            continue
        cid = len(components)
        component_id[start] = cid
        component = []
        stack = [start]
        while stack:
            u = stack.pop()
            component.append(u)
            for v, edge_id in graph[u]:
                if edge_id not in bridges and component_id[v] == -1:
                    component_id[v] = cid
                    stack.append(v)
        components.append(component)
    tree = [[] for _ in components]
    for edge_id in bridges:
        u, v = edges[edge_id]
        a, b = component_id[u], component_id[v]
        tree[a].append(b)
        tree[b].append(a)
    return component_id, components, sorted(bridges), tree
