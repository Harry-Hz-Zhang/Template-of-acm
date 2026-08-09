from collections import deque


def hopcroft_karp(graph, right_size):
    """graph[u] lists right-side vertices. Return (matching_size, left_match, right_match)."""
    left_size = len(graph)
    left_match = [-1] * left_size
    right_match = [-1] * right_size
    distance = [0] * left_size

    def bfs():
        """Run the bfs operation."""
        queue = deque()
        found = False
        for u in range(left_size):
            if left_match[u] == -1:
                distance[u] = 0
                queue.append(u)
            else:
                distance[u] = -1
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                other = right_match[v]
                if other == -1:
                    found = True
                elif distance[other] == -1:
                    distance[other] = distance[u] + 1
                    queue.append(other)
        return found

    def dfs(u):
        """Run the dfs operation."""
        for v in graph[u]:
            other = right_match[v]
            if other == -1 or (distance[other] == distance[u] + 1 and dfs(other)):
                left_match[u] = v
                right_match[v] = u
                return True
        distance[u] = -1
        return False

    matching = 0
    while bfs():
        for u in range(left_size):
            if left_match[u] == -1 and dfs(u):
                matching += 1
    return matching, left_match, right_match
