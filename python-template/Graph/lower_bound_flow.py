from collections import deque
import sys


class LowerBoundFlow(object):
    """Feasible circulation, optionally with source/sink, for lower <= flow <= upper."""

    def __init__(self, n):
        """Initialize the data structure."""
        self.n = n
        self.edges = []

    def add_edge(self, u, v, lower, upper):
        """Run the add edge operation."""
        if lower < 0 or lower > upper:
            raise ValueError('require 0 <= lower <= upper')
        self.edges.append((u, v, lower, upper))

    def feasible(self, source=None, sink=None):
        """Run the feasible operation."""
        if (source is None) != (sink is None):
            raise ValueError('source and sink must be given together')
        if source is not None and (not 0 <= source < self.n or not 0 <= sink < self.n or source == sink):
            raise ValueError('source and sink must be distinct valid vertices')
        n = self.n + 2
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 10))
        super_source, super_sink = self.n, self.n + 1
        graph = [[] for _ in range(n)]

        def add(u, v, capacity):
            """Run the add operation."""
            forward = [v, capacity, None, capacity]
            backward = [u, 0, forward, 0]
            forward[2] = backward
            graph[u].append(forward)
            graph[v].append(backward)
            return forward

        balance = [0] * self.n
        original = []
        for u, v, lower, upper in self.edges:
            original.append((add(u, v, upper - lower), lower))
            balance[u] -= lower
            balance[v] += lower
        artificial = add(sink, source, 10 ** 30) if source is not None and sink is not None else None
        demand = 0
        for u, value in enumerate(balance):
            if value > 0:
                add(super_source, u, value)
                demand += value
            elif value < 0:
                add(u, super_sink, -value)

        def max_flow(s, t):
            """Run the max flow operation."""
            total = 0
            while True:
                level = [-1] * n
                level[s] = 0
                queue = deque([s])
                while queue:
                    u = queue.popleft()
                    for edge in graph[u]:
                        if edge[1] and level[edge[0]] == -1:
                            level[edge[0]] = level[u] + 1
                            queue.append(edge[0])
                if level[t] == -1:
                    return total
                current = [0] * n

                def dfs(u, pushed):
                    """Run the dfs operation."""
                    if u == t:
                        return pushed
                    while current[u] < len(graph[u]):
                        edge = graph[u][current[u]]
                        if edge[1] and level[edge[0]] == level[u] + 1:
                            sent = dfs(edge[0], min(pushed, edge[1]))
                            if sent:
                                edge[1] -= sent
                                edge[2][1] += sent
                                return sent
                        current[u] += 1
                    return 0

                while True:
                    pushed = dfs(s, 10 ** 30)
                    if not pushed:
                        break
                    total += pushed

        if max_flow(super_source, super_sink) != demand:
            return None
        flows = [lower + edge[3] - edge[1] for edge, lower in original]
        value = artificial[3] - artificial[1] if artificial is not None else 0
        return flows, value
