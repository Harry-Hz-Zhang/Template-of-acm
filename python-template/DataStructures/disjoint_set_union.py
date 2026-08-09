class DisjointSetUnion:
    """Disjoint-set union over nodes ``1..n``."""

    def __init__(self, n):
        """Initialize the data structure."""
        self.n = n
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.size[0] = 0
        self.components = n

    def find(self, x):
        """Run the find operation."""
        if not 1 <= x <= self.n:
            raise IndexError('node is out of range')
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
        self.components -= 1
        return True

    def same(self, a, b):
        """Run the same operation."""
        return self.find(a) == self.find(b)

    def component_size(self, x):
        """Run the component size operation."""
        return self.size[self.find(x)]
