class WeightedDisjointSetUnion(object):
    """Maintain equations weight[y] - weight[x] on nodes ``1..n``."""

    def __init__(self, n):
        """Initialize the data structure."""
        self.n = n
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.size[0] = 0
        self.weight_to_parent = [0] * (n + 1)

    def find(self, x):
        """Run the find operation."""
        if not 1 <= x <= self.n:
            raise IndexError('node is out of range')
        if self.parent[x] != x:
            parent = self.parent[x]
            self.parent[x] = self.find(parent)
            self.weight_to_parent[x] += self.weight_to_parent[parent]
        return self.parent[x]

    def weight(self, x):
        """Run the weight operation."""
        self.find(x)
        return self.weight_to_parent[x]

    def union(self, x, y, difference):
        """Run the union operation."""
        root_x = self.find(x)
        root_y = self.find(y)
        adjusted = difference + self.weight(x) - self.weight(y)
        if root_x == root_y:
            return adjusted == 0
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
            adjusted = -adjusted
        self.parent[root_y] = root_x
        self.weight_to_parent[root_y] = adjusted
        self.size[root_x] += self.size[root_y]
        return True

    def difference(self, x, y):
        """Run the difference operation."""
        if self.find(x) != self.find(y):
            return None
        return self.weight(y) - self.weight(x)
