from collections import deque
import sys


INF = 10 ** 30


class Dinic(object):
    def __init__(self, n):
        """Create a residual network with n zero-based vertices."""
        self.n = n
        self.graph = [[] for _ in range(n)]
        self._edges = []
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 2 * n + 100))

    def add_edge(self, u, v, capacity):
        """Add a directed edge and return its stable edge index."""
        if not 0 <= u < self.n or not 0 <= v < self.n:
            raise IndexError('vertex is out of range')
        if capacity < 0:
            raise ValueError('capacity must be nonnegative')
        forward = [v, capacity, None]
        backward = [u, 0, forward]
        forward[2] = backward
        self.graph[u].append(forward)
        self.graph[v].append(backward)
        self._edges.append((u, forward, capacity))
        return len(self._edges) - 1

    def get_edge(self, edge_id):
        """Return (from, to, capacity, flow) for one original edge."""
        u, edge, capacity = self._edges[edge_id]
        return u, edge[0], capacity, edge[2][1]

    def edges(self):
        """Return current flow information for every original edge."""
        return [self.get_edge(edge_id) for edge_id in range(len(self._edges))]

    def min_cut(self, source):
        """Return residual vertices reachable from source after a flow run."""
        if not 0 <= source < self.n:
            raise IndexError('source is out of range')
        reachable = [False] * self.n
        reachable[source] = True
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if edge[1] > 0 and not reachable[edge[0]]:
                    reachable[edge[0]] = True
                    queue.append(edge[0])
        return reachable

    def max_flow(self, source, sink, flow_limit=INF):
        """Send up to flow_limit units and return the additional flow."""
        total = 0
        while total < flow_limit:
            level = [-1] * self.n
            level[source] = 0
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for edge in self.graph[u]:
                    if edge[1] > 0 and level[edge[0]] == -1:
                        level[edge[0]] = level[u] + 1
                        queue.append(edge[0])
            if level[sink] == -1:
                break
            current = [0] * self.n

            def dfs(u, pushed):
                """Push one blocking-flow path through the level graph."""
                if u == sink:
                    return pushed
                while current[u] < len(self.graph[u]):
                    edge = self.graph[u][current[u]]
                    if edge[1] > 0 and level[edge[0]] == level[u] + 1:
                        sent = dfs(edge[0], min(pushed, edge[1]))
                        if sent:
                            edge[1] -= sent
                            edge[2][1] += sent
                            return sent
                    current[u] += 1
                return 0

            while total < flow_limit:
                pushed = dfs(source, flow_limit - total)
                if not pushed:
                    break
                total += pushed
        return total
