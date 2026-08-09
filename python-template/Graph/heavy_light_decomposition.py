class HeavyLightDecomposition(object):
    def __init__(self, graph, root=0):
        """Initialize the data structure."""
        n = len(graph)
        self.parent = [-1] * n
        self.depth = [0] * n
        order = [root]
        for u in order:
            for v in graph[u]:
                if v != self.parent[u]:
                    self.parent[v] = u
                    self.depth[v] = self.depth[u] + 1
                    order.append(v)

        size = [1] * n
        heavy = [-1] * n
        for u in reversed(order):
            best_size = 0
            for v in graph[u]:
                if self.parent[v] == u:
                    size[u] += size[v]
                    if size[v] > best_size:
                        best_size = size[v]
                        heavy[u] = v

        self.head = [0] * n
        self.position = [0] * n
        self.vertex_at = [0] * n
        timer = 0
        stack = [(root, root)]
        while stack:
            start, chain_head = stack.pop()
            u = start
            while u != -1:
                self.head[u] = chain_head
                self.position[u] = timer
                self.vertex_at[timer] = u
                timer += 1
                for v in graph[u]:
                    if self.parent[v] == u and v != heavy[u]:
                        stack.append((v, v))
                u = heavy[u]
        self.size = size

    def path_segments(self, u, v, edge_values=False):
        """Return inclusive position intervals whose union is path u-v."""
        segments = []
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            segments.append((self.position[self.head[u]], self.position[u]))
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        left = self.position[u] + (1 if edge_values else 0)
        if left <= self.position[v]:
            segments.append((left, self.position[v]))
        return segments

    def subtree_segment(self, u):
        """Run the subtree segment operation."""
        return self.position[u], self.position[u] + self.size[u] - 1
