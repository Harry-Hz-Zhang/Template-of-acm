def kruskal_reconstruction_tree(n, edges):
    """Return (children, merge_weight, roots); leaves 0..n-1 are original vertices."""
    parent = list(range(2 * n))
    children = [[] for _ in range(2 * n)]
    merge_weight = [None] * (2 * n)

    def find(x):
        """Run the find operation."""
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    next_node = n
    for weight, u, v in sorted(edges):
        u, v = find(u), find(v)
        if u == v:
            continue
        children[next_node] = [u, v]
        merge_weight[next_node] = weight
        parent[u] = parent[v] = next_node
        parent[next_node] = next_node
        next_node += 1
    roots = sorted({find(u) for u in range(n)})
    return children[:next_node], merge_weight[:next_node], roots
