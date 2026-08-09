from collections import deque


INF = 10 ** 30


class MinCostMaxFlow(object):
    def __init__(self, n):
        """Create a residual cost network with n vertices."""
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, capacity, cost):
        """Add a directed edge with capacity and per-unit cost."""
        forward = [v, capacity, cost, None]
        backward = [u, 0, -cost, forward]
        forward[3] = backward
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def flow(self, source, sink, flow_limit=INF, maximize=False):
        """Return (flow, cost), optionally maximizing cost instead."""
        total_flow = 0
        total_cost = 0
        while total_flow < flow_limit:
            distance = [INF] * self.n
            parent = [None] * self.n
            in_queue = [False] * self.n
            distance[source] = 0
            queue = deque([source])
            in_queue[source] = True
            while queue:
                u = queue.popleft()
                in_queue[u] = False
                for edge in self.graph[u]:
                    v, capacity, cost = edge[:3]
                    cost = -cost if maximize else cost
                    if capacity > 0 and distance[u] + cost < distance[v]:
                        distance[v] = distance[u] + cost
                        parent[v] = (u, edge)
                        if not in_queue[v]:
                            in_queue[v] = True
                            queue.append(v)
            if parent[sink] is None:
                break
            pushed = flow_limit - total_flow
            v = sink
            while v != source:
                u, edge = parent[v]
                pushed = min(pushed, edge[1])
                v = u
            v = sink
            while v != source:
                u, edge = parent[v]
                edge[1] -= pushed
                edge[3][1] += pushed
                v = u
            total_flow += pushed
            total_cost += pushed * distance[sink] * (-1 if maximize else 1)
        return total_flow, total_cost

    def max_cost_flow(self, source, sink, flow_limit=INF):
        """Return a maximum-cost flow up to the requested limit."""
        return self.flow(source, sink, flow_limit, True)
