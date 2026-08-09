INF = float('inf')


def floyd_warshall(matrix):
    """Return all-pairs shortest distances from a weighted adjacency matrix."""
    distance = [row[:] for row in matrix]
    n = len(distance)
    for k in range(n):
        for i in range(n):
            if distance[i][k] == INF:
                continue
            for j in range(n):
                candidate = distance[i][k] + distance[k][j]
                if candidate < distance[i][j]:
                    distance[i][j] = candidate
    return distance
