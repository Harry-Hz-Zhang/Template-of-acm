import random


NEG_INF = -(10 ** 30)


def color_coding_max_path(graph, k, iterations=300, seed=None):
    """Estimate the maximum weight simple k-vertex path by color coding."""
    n = len(graph)
    if k <= 0 or k > n or iterations <= 0:
        raise ValueError('require 1 <= k <= n and positive iterations')
    generator = random.Random(seed)
    full_mask = (1 << k) - 1
    answer = NEG_INF
    for _ in range(iterations):
        colors = [generator.randrange(k) for _ in range(n)]
        dp = [[NEG_INF] * n for _ in range(1 << k)]
        for vertex, color in enumerate(colors):
            dp[1 << color][vertex] = 0
        for mask in range(1, 1 << k):
            for u in range(n):
                current = dp[mask][u]
                if current == NEG_INF:
                    continue
                for v, weight in graph[u]:
                    bit = 1 << colors[v]
                    if not mask & bit:
                        next_mask = mask | bit
                        dp[next_mask][v] = max(dp[next_mask][v], current + weight)
        answer = max(answer, max(dp[full_mask]))
    return answer
