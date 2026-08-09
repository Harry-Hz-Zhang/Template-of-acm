def tree_euler_tour(graph, root=0):
    """Return (tin, tout, preorder, parent, depth); subtree(u) is preorder[tin[u]:tout[u]]."""
    n = len(graph)
    tin = [0] * n
    tout = [0] * n
    parent = [-1] * n
    depth = [0] * n
    preorder = []
    stack = [(root, -1, 0)]
    while stack:
        u, p, state = stack.pop()
        if state == 0:
            parent[u] = p
            tin[u] = len(preorder)
            preorder.append(u)
            stack.append((u, p, 1))
            for v in reversed(graph[u]):
                if v != p:
                    depth[v] = depth[u] + 1
                    stack.append((v, u, 0))
        else:
            tout[u] = len(preorder)
    return tin, tout, preorder, parent, depth
