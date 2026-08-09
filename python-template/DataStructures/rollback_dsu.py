class RollbackDisjointSetUnion(object):
    """Rollback DSU over nodes ``1..n``."""

    def __init__(self, n):
        """Initialize the data structure."""
        self.n = n
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.size[0] = 0
        self.history = []
        self.components = n

    def find(self, x):
        """Run the find operation."""
        if not 1 <= x <= self.n:
            raise IndexError('node is out of range')
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, a, b):
        """Run the union operation."""
        a = self.find(a)
        b = self.find(b)
        if a == b:
            self.history.append(None)
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, a, self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True

    def snapshot(self):
        """Run the snapshot operation."""
        return len(self.history)

    def rollback(self, snapshot=None):
        """Run the rollback operation."""
        if snapshot is None:
            if not self.history:
                return False
            snapshot = len(self.history) - 1
        if snapshot < 0 or snapshot > len(self.history):
            raise ValueError('invalid snapshot')
        target = snapshot
        while len(self.history) > target:
            change = self.history.pop()
            if change is None:
                continue
            child, parent, old_size = change
            self.parent[child] = child
            self.size[parent] = old_size
            self.components += 1
        return True
