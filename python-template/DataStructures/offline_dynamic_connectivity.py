class TimeSegmentTree(object):
    """Store items on half-open time intervals for rollback traversal."""

    def __init__(self, size):
        """Create a timeline with positions 0 through size - 1."""
        if size < 0:
            raise ValueError('size must be nonnegative')
        self.size = size
        self.nodes = [[] for _ in range(max(1, 4 * size))]

    def add_interval(self, left, right, item):
        """Attach an item to every time in the half-open interval."""
        if not 0 <= left <= right <= self.size:
            raise IndexError('time interval is out of bounds')

        def add(node, node_left, node_right):
            """Insert an interval into canonical segment nodes."""
            if right <= node_left or node_right <= left:
                return
            if left <= node_left and node_right <= right:
                self.nodes[node].append(item)
                return
            middle = (node_left + node_right) // 2
            add(node * 2, node_left, middle)
            add(node * 2 + 1, middle, node_right)

        if left < right:
            add(1, 0, self.size)

    def traverse(self, apply, snapshot, rollback, visit):
        """Apply interval items with rollback and return one value per time."""
        results = [None] * self.size

        def solve(node, left, right):
            """Traverse one time segment under a rollback snapshot."""
            marker = snapshot()
            for item in self.nodes[node]:
                apply(item)
            if right - left == 1:
                results[left] = visit(left)
            else:
                middle = (left + right) // 2
                solve(node * 2, left, middle)
                solve(node * 2 + 1, middle, right)
            rollback(marker)

        if self.size:
            solve(1, 0, self.size)
        return results


class _RollbackDSU(object):
    def __init__(self, n):
        """Create a 1-based rollback disjoint-set structure."""
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.size[0] = 0
        self.history = []

    def find(self, x):
        """Return a representative without path compression."""
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, a, b):
        """Merge two components and record a rollback entry."""
        a, b = self.find(a), self.find(b)
        if a == b:
            self.history.append(None)
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, a, self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]

    def rollback(self, snapshot):
        """Undo changes until the requested history size."""
        while len(self.history) > snapshot:
            change = self.history.pop()
            if change is not None:
                child, parent, old_size = change
                self.parent[child] = child
                self.size[parent] = old_size


def offline_dynamic_connectivity(n, operations):
    """Process edge operations over nodes ``1..n`` and return query answers."""
    for _, u, v in operations:
        if not 1 <= u <= n or not 1 <= v <= n:
            raise IndexError('node is out of range')
    time_count = len(operations)
    active = {}
    intervals = []
    for time, (kind, u, v) in enumerate(operations):
        edge = (min(u, v), max(u, v))
        if kind == 'add':
            active.setdefault(edge, []).append(time)
        elif kind == 'remove':
            if not active.get(edge):
                raise ValueError('removing an inactive edge')
            intervals.append((active[edge].pop(), time, edge))
        elif kind != 'query':
            raise ValueError('unknown operation kind')
    for edge, starts in active.items():
        intervals.extend((start, time_count, edge) for start in starts)
    timeline = TimeSegmentTree(time_count)
    for left, right, edge in intervals:
        timeline.add_interval(left, right, edge)
    dsu = _RollbackDSU(n)

    def apply(edge):
        """Apply one active edge to the rollback DSU."""
        dsu.union(edge[0], edge[1])

    def visit(time):
        """Answer a connectivity query at one timeline position."""
        kind, u, v = operations[time]
        return dsu.find(u) == dsu.find(v) if kind == 'query' else None

    results = timeline.traverse(apply, lambda: len(dsu.history), dsu.rollback, visit)
    return [results[time] for time, operation in enumerate(operations) if operation[0] == 'query']
