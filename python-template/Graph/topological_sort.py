from collections import deque
import heapq


def topological_sort(graph, lexicographical=False):
    """Return a topological order, or [] when the directed graph has a cycle."""
    indegree = [0] * len(graph)
    for edges in graph:
        for v in edges:
            indegree[v] += 1
    queue = [i for i, degree in enumerate(indegree) if degree == 0]
    if lexicographical:
        heapq.heapify(queue)
        pop = lambda: heapq.heappop(queue)
        push = lambda value: heapq.heappush(queue, value)
    else:
        queue = deque(queue)
        pop = queue.popleft
        push = queue.append
    order = []
    while queue:
        u = pop()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                push(v)
    return order if len(order) == len(graph) else []
