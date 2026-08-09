class _DSU(object):
    def __init__(self, n):
        """Initialize the data structure."""
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        """Run the find operation."""
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        """Run the union operation."""
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def boruvka(n, edges):
    """edges contains (weight, u, v); return (MST weight, chosen edges), or (None, [])."""
    dsu = _DSU(n)
    components = n
    chosen = []
    total = 0
    while components > 1:
        cheapest = [None] * n
        for edge in edges:
            weight, u, v = edge
            a, b = dsu.find(u), dsu.find(v)
            if a == b:
                continue
            if cheapest[a] is None or edge < cheapest[a]:
                cheapest[a] = edge
            if cheapest[b] is None or edge < cheapest[b]:
                cheapest[b] = edge
        changed = False
        for edge in cheapest:
            if edge is not None and dsu.union(edge[1], edge[2]):
                total += edge[0]
                chosen.append(edge)
                components -= 1
                changed = True
        if not changed:
            return None, []
    return total, chosen
