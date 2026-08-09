class DisjointSetUnion(object):
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
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def kruskal(n, edges):
    """edges contains (weight, u, v). Return (weight, chosen_edges), or (None, [])."""
    dsu = DisjointSetUnion(n)
    total = 0
    chosen = []
    for weight, u, v in sorted(edges):
        if dsu.union(u, v):
            total += weight
            chosen.append((weight, u, v))
    if n and len(chosen) != n - 1:
        return None, []
    return total, chosen
