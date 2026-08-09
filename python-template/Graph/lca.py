class LowestCommonAncestor(object):
    def __init__(self, graph, root=0):
        """Precompute binary lifting tables for a rooted tree."""
        n = len(graph)
        self.depth = [-1] * n
        self.depth[root] = 0
        parent = [root] * n
        order = [root]
        for u in order:
            for v in graph[u]:
                if self.depth[v] == -1:
                    self.depth[v] = self.depth[u] + 1
                    parent[v] = u
                    order.append(v)
        levels = max(1, n.bit_length())
        self.up = [parent]
        for _ in range(1, levels):
            previous = self.up[-1]
            self.up.append([previous[previous[v]] for v in range(n)])

    def kth_ancestor(self, u, k):
        """Return the k-th ancestor of a node."""
        bit = 0
        while k:
            if k & 1:
                u = self.up[bit][u]
            k >>= 1
            bit += 1
        return u

    def lca(self, u, v):
        """Return the lowest common ancestor of two nodes."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        for level in range(len(self.up) - 1, -1, -1):
            if self.up[level][u] != self.up[level][v]:
                u = self.up[level][u]
                v = self.up[level][v]
        return self.up[0][u]

    def distance(self, u, v):
        """Return the number of edges on the unique tree path."""
        ancestor = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[ancestor]

    def is_on_path(self, x, u, v):
        """Return whether x lies on the unique path from u to v."""
        return self.distance(u, x) + self.distance(x, v) == self.distance(u, v)
