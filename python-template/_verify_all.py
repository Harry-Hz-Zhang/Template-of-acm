from __future__ import print_function

import bisect
import importlib.util
import itertools
import math
import os
import random
from collections import Counter, deque
from fractions import Fraction


ROOT = os.path.dirname(os.path.abspath(__file__))
VERIFIED = set()


def load(category, filename):
    """Run the load operation."""
    relative = os.path.join(category, filename + '.py')
    path = os.path.join(ROOT, relative)
    name = 'template_' + category + '_' + filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    VERIFIED.add(relative)
    return module


def choose(n, k):
    """Run the choose operation."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for value in range(1, k + 1):
        result = result * (n - value + 1) // value
    return result


def all_pairs_unweighted(graph):
    """Run the all pairs unweighted operation."""
    result = []
    for source in range(len(graph)):
        distance = [-1] * len(graph)
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if distance[v] == -1:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        result.append(distance)
    return result


def test_graph():
    """Run the test graph operation."""
    bfs = load('Graph', 'bfs')
    zero_one = load('Graph', 'zero_one_bfs')
    dijkstra = load('Graph', 'dijkstra')
    bellman = load('Graph', 'bellman_ford')
    floyd = load('Graph', 'floyd_warshall')
    topological = load('Graph', 'topological_sort')
    kruskal = load('Graph', 'kruskal')
    prim = load('Graph', 'prim')
    scc = load('Graph', 'strongly_connected_components')
    cuts = load('Graph', 'bridges_articulation')
    matching = load('Graph', 'bipartite_matching')
    dinic = load('Graph', 'dinic')
    min_cost = load('Graph', 'min_cost_max_flow')
    lca_module = load('Graph', 'lca')
    reconstruction_module = load('Graph', 'tree_reconstruction')
    color_coding_module = load('Graph', 'color_coding')
    hld_module = load('Graph', 'heavy_light_decomposition')
    euler = load('Graph', 'eulerian_path')
    diameter = load('Graph', 'tree_diameter')
    two_sat = load('Graph', 'two_sat')
    de_bruijn = load('Graph', 'de_bruijn')
    centroid_module = load('Graph', 'centroid_decomposition')
    min_cut_module = load('Graph', 'stoer_wagner_min_cut')

    for _ in range(80):
        n = random.randint(1, 8)
        graph = [[] for _ in range(n)]
        weighted = [[] for _ in range(n)]
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.25:
                    weight = random.randint(0, 9)
                    graph[u].append(v)
                    weighted[u].append((v, weight))
                    matrix[u][v] = min(matrix[u][v], weight)
        source = random.randrange(n)
        assert bfs.bfs_shortest_paths(graph, source)[0] == all_pairs_unweighted(graph)[source]
        expected = floyd.floyd_warshall(matrix)[source]
        assert dijkstra.dijkstra(weighted, source)[0] == expected
        graph01 = [[(v, weight & 1) for v, weight in edges] for edges in weighted]
        matrix01 = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix01[i][i] = 0
            for v, weight in graph01[i]:
                matrix01[i][v] = min(matrix01[i][v], weight)
        assert zero_one.zero_one_bfs(graph01, source) == floyd.floyd_warshall(matrix01)[source]

    for _ in range(50):
        n = random.randint(1, 8)
        edges = []
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.35:
                    weight = random.randint(-5, 8)
                    edges.append((u, v, weight))
                    matrix[u][v] = min(matrix[u][v], weight)
        expected = floyd.floyd_warshall(matrix)[0]
        actual, _, negative = bellman.bellman_ford(n, edges, 0)
        assert not negative and actual == expected
    assert bellman.bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)], 0)[2]

    for _ in range(50):
        n = random.randint(1, 12)
        order = list(range(n))
        random.shuffle(order)
        position = {value: i for i, value in enumerate(order)}
        graph = [[] for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if position[u] < position[v] and random.random() < 0.15:
                    graph[u].append(v)
        result = topological.topological_sort(graph)
        result_position = {value: i for i, value in enumerate(result)}
        assert len(result) == n
        assert all(result_position[u] < result_position[v] for u in range(n) for v in graph[u])
    assert topological.topological_sort([[1], [0]]) == []

    for _ in range(50):
        n = random.randint(1, 7)
        edges = []
        graph = [[] for _ in range(n)]
        for v in range(1, n):
            u = random.randrange(v)
            weight = random.randint(0, 20)
            edges.append((weight, u, v))
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.2:
                    weight = random.randint(0, 20)
                    edges.append((weight, u, v))
                    graph[u].append((v, weight))
                    graph[v].append((u, weight))
        k_weight, _ = kruskal.kruskal(n, edges)
        p_weight, _ = prim.prim(graph)
        brute = float('inf')
        if n == 1:
            brute = 0
        else:
            for selected in itertools.combinations(edges, n - 1):
                dsu = kruskal.DisjointSetUnion(n)
                if all(dsu.union(u, v) for _, u, v in selected) and dsu.size[dsu.find(0)] == n:
                    brute = min(brute, sum(edge[0] for edge in selected))
        assert k_weight == p_weight == brute

    for _ in range(50):
        n = random.randint(1, 9)
        graph = [[] for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.22:
                    graph[u].append(v)
        ids, _ = scc.strongly_connected_components(graph)
        reach = all_pairs_unweighted(graph)
        assert all((ids[u] == ids[v]) == (reach[u][v] >= 0 and reach[v][u] >= 0)
                   for u in range(n) for v in range(n))

    for _ in range(40):
        n = random.randint(2, 9)
        edge_set = set()
        for v in range(1, n):
            edge_set.add((random.randrange(v), v))
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.2:
                    edge_set.add((u, v))
        edges = sorted(edge_set)
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        actual_bridges, actual_points = cuts.bridges_and_articulation_points(graph)

        def component_count(banned_vertex=-1, banned_edge=None):
            """Run the component count operation."""
            visited = [banned_vertex == i for i in range(n)]
            count = 0
            for start in range(n):
                if visited[start]:
                    continue
                count += 1
                visited[start] = True
                stack = [start]
                while stack:
                    u = stack.pop()
                    for v in graph[u]:
                        if banned_edge == (min(u, v), max(u, v)) or visited[v]:
                            continue
                        visited[v] = True
                        stack.append(v)
            return count

        expected_bridges = [edge for edge in edges if component_count(banned_edge=edge) > 1]
        expected_points = [u for u in range(n) if component_count(banned_vertex=u) > 1]
        assert actual_bridges == expected_bridges and actual_points == expected_points

    for _ in range(50):
        left = random.randint(0, 6)
        right = random.randint(0, 6)
        graph = [[v for v in range(right) if random.random() < 0.45] for _ in range(left)]
        actual = matching.hopcroft_karp(graph, right)[0]

        def brute_match(index, used):
            """Run the brute match operation."""
            if index == left:
                return 0
            return max([brute_match(index + 1, used)] + [
                1 + brute_match(index + 1, used | {v}) for v in graph[index] if v not in used
            ])

        assert actual == brute_match(0, set())

    for _ in range(35):
        n = random.randint(2, 7)
        source, sink = 0, n - 1
        capacities = [[0] * n for _ in range(n)]
        flow = dinic.Dinic(n)
        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.2:
                    capacity = random.randint(0, 6)
                    capacities[u][v] += capacity
                    flow.add_edge(u, v, capacity)
        actual = flow.max_flow(source, sink)
        brute = min(
            sum(capacities[u][v] for u in range(n) for v in range(n)
                if (mask >> u) & 1 and not (mask >> v) & 1)
            for mask in range(1 << n)
            if (mask & 1) and not ((mask >> sink) & 1)
        )
        assert actual == brute

    long_flow = dinic.Dinic(1501)
    for u in range(1500):
        long_flow.add_edge(u, u + 1, 1)
    assert long_flow.max_flow(0, 1500) == 1

    for _ in range(30):
        size = random.randint(1, 4)
        costs = [[random.randint(-5, 10) for _ in range(size)] for _ in range(size)]
        network = min_cost.MinCostMaxFlow(2 * size + 2)
        source, sink = 2 * size, 2 * size + 1
        for i in range(size):
            network.add_edge(source, i, 1, 0)
            network.add_edge(size + i, sink, 1, 0)
            for j in range(size):
                network.add_edge(i, size + j, 1, costs[i][j])
        actual_flow, actual_cost = network.flow(source, sink)
        expected_cost = min(sum(costs[i][p[i]] for i in range(size))
                            for p in itertools.permutations(range(size)))
        assert (actual_flow, actual_cost) == (size, expected_cost)

    for _ in range(60):
        n = random.randint(1, 30)
        graph = [[] for _ in range(n)]
        parent = [0] * n
        depth = [0] * n
        for v in range(1, n):
            parent[v] = random.randrange(v)
            depth[v] = depth[parent[v]] + 1
            graph[v].append(parent[v])
            graph[parent[v]].append(v)
        lca = lca_module.LowestCommonAncestor(graph)
        hld = hld_module.HeavyLightDecomposition(graph)
        for _ in range(20):
            u, v = random.randrange(n), random.randrange(n)
            a, b = u, v
            path_a, path_b = [], []
            while depth[a] > depth[b]:
                path_a.append(a)
                a = parent[a]
            while depth[b] > depth[a]:
                path_b.append(b)
                b = parent[b]
            while a != b:
                path_a.append(a)
                path_b.append(b)
                a, b = parent[a], parent[b]
            expected_path = path_a + [a] + list(reversed(path_b))
            assert lca.lca(u, v) == a
            positions = set()
            for left, right in hld.path_segments(u, v):
                positions.update(range(left, right + 1))
            assert {hld.vertex_at[position] for position in positions} == set(expected_path)

    directed_edges = [(0, 1), (1, 2), (2, 0), (0, 3)]
    directed_path = euler.directed_eulerian_path(4, directed_edges)
    assert Counter(zip(directed_path, directed_path[1:])) == Counter(directed_edges)
    undirected_edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 2)]
    undirected_path = euler.undirected_eulerian_path(4, undirected_edges)
    assert Counter(tuple(sorted(edge)) for edge in zip(undirected_path, undirected_path[1:])) == Counter(
        tuple(sorted(edge)) for edge in undirected_edges)

    for _ in range(50):
        n = random.randint(1, 15)
        graph = [[] for _ in range(n)]
        for v in range(1, n):
            u = random.randrange(v)
            weight = random.randint(0, 10)
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        actual, path = diameter.tree_diameter(graph)
        brute = 0
        for source in range(n):
            distances = [-1] * n
            distances[source] = 0
            stack = [source]
            while stack:
                u = stack.pop()
                for v, weight in graph[u]:
                    if distances[v] == -1:
                        distances[v] = distances[u] + weight
                        stack.append(v)
            brute = max(brute, max(distances))
        assert actual == brute and path

    for _ in range(100):
        n = random.randint(1, 6)
        clauses = []
        solver = two_sat.TwoSat(n)
        for _ in range(random.randint(0, 12)):
            a, b = random.randrange(n), random.randrange(n)
            a_value, b_value = bool(random.getrandbits(1)), bool(random.getrandbits(1))
            clauses.append((a, a_value, b, b_value))
            solver.add_or(a, a_value, b, b_value)
        expected = next((assignment for assignment in itertools.product((False, True), repeat=n)
                         if all(assignment[a] == av or assignment[b] == bv for a, av, b, bv in clauses)), None)
        actual = solver.solve()
        assert (actual is None) == (expected is None)
        assert actual is None or all(actual[a] == av or actual[b] == bv for a, av, b, bv in clauses)

    for order in range(1, 5):
        for alphabet in range(1, 4):
            sequence = de_bruijn.de_bruijn_sequence(order, alphabet)
            windows = [tuple(sequence[i:i + order]) for i in range(alphabet ** order)]
            assert len(sequence) == alphabet ** order + order - 1
            assert len(set(windows)) == alphabet ** order

    for _ in range(30):
        n = random.randint(1, 30)
        graph = [[] for _ in range(n)]
        for v in range(1, n):
            u = random.randrange(v)
            graph[u].append(v)
            graph[v].append(u)
        parent, root = centroid_module.centroid_decomposition(graph)
        children = [[] for _ in range(n)]
        for u in range(n):
            if parent[u] != -1:
                children[parent[u]].append(u)

        def validate(vertices, centroid):
            """Run the validate operation."""
            allowed = set(vertices)
            parts = []
            seen = {centroid}
            for start in graph[centroid]:
                if start not in allowed or start in seen:
                    continue
                part = []
                stack = [start]
                seen.add(start)
                while stack:
                    u = stack.pop()
                    part.append(u)
                    for v in graph[u]:
                        if v in allowed and v not in seen:
                            seen.add(v)
                            stack.append(v)
                parts.append(part)
            assert max([0] + [len(part) for part in parts]) * 2 <= len(vertices)
            assert len(parts) == len(children[centroid])
            for part in parts:
                child = next(value for value in children[centroid] if value in set(part))
                validate(part, child)

        validate(list(range(n)), root)

    for _ in range(45):
        n = random.randint(2, 8)
        matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                matrix[u][v] = matrix[v][u] = random.randint(0, 9)
        actual_weight, side = min_cut_module.stoer_wagner_min_cut(matrix)
        brute = min(sum(matrix[u][v] for u in range(n) for v in range(u + 1, n)
                        if ((mask >> u) & 1) != ((mask >> v) & 1))
                    for mask in range(1, (1 << n) - 1))
        side = set(side)
        side_weight = sum(matrix[u][v] for u in side for v in range(n) if v not in side)
        assert actual_weight == brute == side_weight


def test_data_structures():
    """Run the test data structures operation."""
    trie_module = load('DataStructures', 'trie')
    xor_module = load('DataStructures', 'xor_trie')
    dsu_module = load('DataStructures', 'disjoint_set_union')
    weighted_module = load('DataStructures', 'weighted_dsu')
    rollback_module = load('DataStructures', 'rollback_dsu')
    fenwick_module = load('DataStructures', 'fenwick_tree')
    range_module = load('DataStructures', 'range_fenwick')
    segment_module = load('DataStructures', 'segment_tree')
    lazy_module = load('DataStructures', 'lazy_segment_tree')
    sparse_module = load('DataStructures', 'sparse_table')
    prefix_module = load('DataStructures', 'prefix_2d')
    monotonic_module = load('DataStructures', 'monotonic_stack')
    sliding_module = load('DataStructures', 'sliding_window')
    basis_module = load('DataStructures', 'linear_basis')
    persistent_module = load('DataStructures', 'persistent_segment_tree')
    li_chao_module = load('DataStructures', 'li_chao_tree')
    treap_module = load('DataStructures', 'randomized_treap')

    trie = trie_module.Trie()
    words = Counter()
    alphabet = 'abc'
    for _ in range(300):
        word = ''.join(random.choice(alphabet) for _ in range(random.randint(0, 5)))
        if random.random() < 0.65:
            amount = random.randint(1, 3)
            trie.insert(word, amount)
            words[word] += amount
        else:
            amount = random.randint(1, 3)
            erased = trie.erase(word, amount)
            expected = min(words[word], amount)
            words[word] -= expected
            assert erased == expected
        prefix = word[:random.randint(0, len(word))]
        assert trie.search(word) == words[word]
        assert trie.count_prefix(prefix) == sum(count for item, count in words.items() if item.startswith(prefix))
        assert Counter(trie.get_all_with_prefix(prefix)) == Counter(
            {item: count for item, count in words.items() if item.startswith(prefix) and count})

    xor_trie = xor_module.XorTrie(7)
    values = []
    for _ in range(250):
        if not values or random.random() < 0.7:
            value = random.randrange(256)
            xor_trie.insert(value)
            values.append(value)
        else:
            value = random.choice(values)
            assert xor_trie.erase(value) == 1
            values.remove(value)
        if values:
            query = random.randrange(256)
            limit = random.randrange(256)
            assert xor_trie.max_xor(query) == max(query ^ value for value in values)
            assert xor_trie.count_xor_less(query, limit) == sum((query ^ value) < limit for value in values)

    for _ in range(40):
        n = random.randint(1, 20)
        dsu = dsu_module.DisjointSetUnion(n)
        labels = list(range(n + 1))
        for _ in range(100):
            a, b = random.randint(1, n), random.randint(1, n)
            merged = labels[a] != labels[b]
            old = labels[b]
            new = labels[a]
            labels = [new if label == old else label for label in labels]
            assert dsu.union(a, b) == merged
            x, y = random.randint(1, n), random.randint(1, n)
            assert dsu.same(x, y) == (labels[x] == labels[y])
            assert dsu.component_size(x) == labels[1:].count(labels[x])

    for _ in range(40):
        n = random.randint(1, 20)
        weights = [0] + [random.randint(-100, 100) for _ in range(n)]
        dsu = weighted_module.WeightedDisjointSetUnion(n)
        for v in range(2, n + 1):
            u = random.randint(1, v - 1)
            assert dsu.union(u, v, weights[v] - weights[u])
        for _ in range(30):
            x, y = random.randint(1, n), random.randint(1, n)
            assert dsu.difference(x, y) == weights[y] - weights[x]
        assert not dsu.union(1, n, weights[n] - weights[1] + 1)

    rollback = rollback_module.RollbackDisjointSetUnion(6)
    start = rollback.snapshot()
    rollback.union(1, 2)
    middle = rollback.snapshot()
    rollback.union(2, 3)
    rollback.union(4, 5)
    assert rollback.components == 3
    rollback.rollback(middle)
    assert rollback.components == 5 and rollback.find(1) == rollback.find(2) != rollback.find(3)
    rollback.rollback(start)
    assert rollback.components == 6
    assert rollback.rollback() is False

    for _ in range(50):
        n = random.randint(1, 40)
        values = [random.randint(-20, 20) for _ in range(n)]
        fenwick = fenwick_module.FenwickTree(values)
        range_fenwick = range_module.RangeFenwick(n)
        for index, value in enumerate(values, 1):
            range_fenwick.add_range(index, index, value)
        segment = segment_module.SegmentTree(values)
        lazy = lazy_module.LazySegmentTree(values)
        sparse = sparse_module.SparseTable(values)
        original = values[:]
        for left in range(n):
            right = random.randint(left + 1, n)
            assert sparse.query(left + 1, right) == min(original[left:right])
        for _ in range(100):
            if random.random() < 0.5:
                index = random.randrange(n)
                delta = random.randint(-10, 10)
                values[index] += delta
                fenwick.add(index + 1, delta)
                segment.modify(index + 1, values[index])
                lazy.add(index + 1, index + 1, delta)
                range_fenwick.add_range(index + 1, index + 1, delta)
            else:
                left = random.randrange(n)
                right = random.randint(left + 1, n)
                expected = sum(values[left:right])
                assert fenwick.range_sum(left + 1, right) == expected
                assert segment.range_query(left + 1, right) == expected
                assert lazy.query(left + 1, right) == expected
                assert range_fenwick.range_sum(left + 1, right) == expected

    for _ in range(40):
        rows, columns = random.randint(1, 8), random.randint(1, 8)
        matrix = [[random.randint(-5, 5) for _ in range(columns)] for _ in range(rows)]
        matrix_1based = [[0] * (columns + 1)] + [[0] + row for row in matrix]
        prefix = prefix_module.Prefix2D(matrix_1based)
        difference = prefix_module.Diff2D(rows, columns)
        expected_diff = [[0] * (columns + 1) for _ in range(rows + 1)]
        for _ in range(30):
            top = random.randint(1, rows)
            bottom = random.randint(top, rows)
            left = random.randint(1, columns)
            right = random.randint(left, columns)
            assert prefix.query(top, left, bottom, right) == sum(
                matrix[i - 1][j - 1] for i in range(top, bottom + 1) for j in range(left, right + 1))
            delta = random.randint(-5, 5)
            difference.insert(top, bottom, left, right, delta)
            for i in range(top, bottom + 1):
                for j in range(left, right + 1):
                    expected_diff[i][j] += delta
        assert difference.to_array() == expected_diff

    for _ in range(100):
        values = [random.randint(-5, 5) for _ in range(random.randint(0, 30))]
        previous, following = monotonic_module.nearest_strictly_smaller(values)
        for i in range(1, len(values) + 1):
            expected_previous = next((j for j in range(i - 1, 0, -1) if values[j - 1] < values[i - 1]), 0)
            expected_following = next((j for j in range(i + 1, len(values) + 1) if values[j - 1] < values[i - 1]), len(values) + 1)
            assert (previous[i], following[i]) == (expected_previous, expected_following)
        if values:
            window = random.randint(1, len(values) + 2)
            expected_min = [min(values[i:i + window]) for i in range(len(values) - window + 1)]
            expected_max = [max(values[i:i + window]) for i in range(len(values) - window + 1)]
            assert sliding_module.sliding_window_minimum(values, window) == expected_min
            assert sliding_module.sliding_window_maximum(values, window) == expected_max

    for _ in range(80):
        values = [random.randrange(64) for _ in range(random.randint(0, 8))]
        basis = basis_module.XorLinearBasis(5)
        for value in values:
            basis.insert(value)
        possible = {0}
        for value in values:
            possible |= {current ^ value for current in list(possible)}
        assert basis.rank == (len(possible).bit_length() - 1)
        assert basis.max_xor() == max(possible)
        assert all(basis.can_represent(value) == (value in possible) for value in range(64))

    for _ in range(40):
        size = random.randint(1, 20)
        tree = persistent_module.PersistentSegmentTree(size)
        roots = [tree.empty_root]
        values = []
        for _ in range(random.randint(1, 30)):
            value = random.randrange(size) + 1
            values.append(value)
            roots.append(tree.add(roots[-1], value))
        for _ in range(30):
            left = random.randrange(len(values) + 1)
            right = random.randint(left, len(values))
            query_left = random.randrange(1, size + 1)
            query_right = random.randint(query_left, size)
            actual = tree.query(roots[right], query_left, query_right) - tree.query(roots[left], query_left, query_right)
            assert actual == sum(query_left <= value <= query_right for value in values[left:right])
            if left < right:
                k = random.randint(1, right - left)
                assert tree.kth_between(roots[left], roots[right], k) == sorted(values[left:right])[k - 1]
    try:
        persistent_module.PersistentSegmentTree(0)
        assert False
    except ValueError:
        pass

    for _ in range(40):
        tree = li_chao_module.LiChaoTree(-20, 20)
        lines = []
        for _ in range(20):
            line = random.randint(-10, 10), random.randint(-20, 20)
            lines.append(line)
            tree.add_line(*line)
            for x in range(-20, 21):
                assert tree.query(x) == min(slope * x + intercept for slope, intercept in lines)

    treap = treap_module.TreapMultiset()
    values = []
    for _ in range(500):
        if not values or random.random() < 0.65:
            value = random.randint(-20, 20)
            treap.insert(value)
            bisect.insort(values, value)
        else:
            value = random.randint(-20, 20)
            expected = value in values
            assert treap.erase(value) == expected
            if expected:
                values.remove(value)
        query = random.randint(-20, 20)
        assert treap.count_less(query) == bisect.bisect_left(values, query)
        if values:
            k = random.randrange(1, len(values) + 1)
            assert treap.kth(k) == values[k - 1]


def test_geometry():
    """Run the test geometry operation."""
    geometry = load('Geometry', 'geometry_2d')
    geometry3 = load('Geometry', 'geometry_3d')

    for _ in range(100):
        a = geometry.Point(random.uniform(-10, 10), random.uniform(-10, 10))
        b = geometry.Point(random.uniform(-10, 10), random.uniform(-10, 10))
        if geometry.dist(a, b) < 1e-7:
            continue
        p = geometry.Point(random.uniform(-10, 10), random.uniform(-10, 10))
        foot = geometry.project(p, geometry.Line(a, b))
        assert abs((foot - p) * (b - a)) < 1e-6
        reflected = geometry.reflection(p, geometry.Line(a, b))
        assert geometry.dist((p + reflected) / 2.0, foot) < 1e-7

    assert geometry.segments_intersect((0, 0), (2, 2), (0, 2), (2, 0))
    assert geometry.segments_intersect((0, 0), (2, 0), (1, 0), (3, 0))
    assert not geometry.segments_intersect((0, 0), (1, 0), (2, 0), (3, 0))
    intersection = geometry.line_intersection(geometry.Line((0, 0), (2, 2)), geometry.Line((0, 2), (2, 0)))
    assert abs(intersection.x - 1) < 1e-9 and abs(intersection.y - 1) < 1e-9
    assert geometry.line_intersection(geometry.Line((0, 0), (1, 0)), geometry.Line((0, 1), (1, 1))) is None

    for _ in range(80):
        points = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(random.randint(1, 30))]
        hull = geometry.convex_hull(points)
        assert all(geometry.point_in_polygon(point, hull) >= 0 for point in points) if len(hull) >= 3 else True
        if len(hull) >= 3:
            assert all(((hull[i - 1] - hull[i - 2]) ^ (hull[i] - hull[i - 1])) > 0 for i in range(len(hull)))
            actual, _ = geometry.convex_polygon_diameter(hull)
            expected = max(geometry.dist_2(a, b) for a in hull for b in hull)
            assert actual == expected
        actual, _ = geometry.closest_pair(points)
        if len(points) >= 2:
            expected = min((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2
                           for i in range(len(points)) for j in range(i + 1, len(points)))
            assert actual == expected

    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert geometry.point_in_polygon((1, 1), square) == 1
    assert geometry.point_in_polygon((2, 1), square) == 0
    assert geometry.point_in_polygon((3, 1), square) == -1
    assert geometry.polygon_area(square) == 4
    center = geometry.polygon_centroid(square)
    assert abs(center.x - 1) < 1e-9 and abs(center.y - 1) < 1e-9

    half_planes = [
        ((0, 0), (1, 0)),
        ((1, 0), (0, 1)),
        ((1, 1), (-1, 0)),
        ((0, 1), (0, -1)),
    ]
    clipped = geometry.half_plane_intersection(half_planes)
    assert len(clipped) == 4 and abs(geometry.polygon_area(clipped) - 1) < 1e-8

    circum = geometry.circum_circle((0, 0), (2, 0), (0, 2))
    assert abs(circum.O.x - 1) < 1e-9 and abs(circum.O.y - 1) < 1e-9
    assert len(geometry.circle_line_intersections(geometry.Circle((0, 0), 1), (-2, 0), (2, 0))) == 2
    assert len(geometry.circle_circle_intersections((0, 0), 1, (2, 0), 1)) == 1
    assert geometry.Point(1, 2) * geometry.Point(3, 4) == 11
    assert geometry.Point(1, 2) ^ geometry.Point(3, 4) == -2
    assert geometry.circle_relationship(geometry.Circle((0, 0), 1), geometry.Circle((3, 0), 1)) == 4
    assert len(geometry.circle_tangent_points(geometry.Circle((0, 0), 1), (1, 0))) == 1
    assert geometry.distance_point_to_segment((1, 1), (0, 0), (2, 0)) == 1
    assert geometry.distance_segment_to_segment(geometry.Line((0, 0), (1, 0)),
                                               geometry.Line((0, 2), (1, 2))) == 2
    square_polygon = geometry.Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    assert square_polygon.is_ccw() and square_polygon.is_convex()
    assert square_polygon.in_polygon((1, 1)) == 2
    assert geometry.segment_in_polygon(((0.5, 0.5), (1.5, 1.5)), square_polygon)
    assert not geometry.segment_in_polygon(((-1, 1), (1, 1)), square_polygon)
    assert geometry.minimum_area_three_rectangles([(1, 2), (2, 3), (4, 1)]) == 16

    for _ in range(50):
        points = [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(random.randint(1, 8))]
        actual = geometry.minimum_circle(points)
        assert all(math.hypot(point[0] - actual.O.x, point[1] - actual.O.y) <= actual.r + 1e-7
                   for point in points)
        candidates = [(geometry.Point(point[0], point[1]), 0.0) for point in points]
        candidates.extend((geometry.Point((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0),
                           math.hypot(a[0] - b[0], a[1] - b[1]) / 2.0)
                          for a, b in itertools.combinations(points, 2))
        for a, b, c in itertools.combinations(points, 3):
            candidate = geometry.circum_circle(a, b, c)
            if candidate is not None:
                candidates.append((candidate.O, candidate.r))
        expected = min(candidate[1] for candidate in candidates
                       if all(math.hypot(point[0] - candidate[0].x, point[1] - candidate[0].y)
                              <= candidate[1] + 1e-7 for point in points))
        assert abs(actual.r - expected) < 1e-7

    assert abs(geometry.adaptive_simpson(lambda x: x * x, 0, 1) - 1.0 / 3.0) < 1e-9
    assert abs(geometry.adaptive_simpson(math.sin, 0, math.pi) - 2.0) < 1e-9
    assert geometry3.Point(1, 0, 0) ^ geometry3.Point(0, 1, 0) == geometry3.Point(0, 0, 1)
    assert geometry3.signed_tetrahedron_volume_six((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)) == 1
    assert abs(geometry3.central_angle((1, 0, 0), (0, 1, 0)) - math.pi / 2) < 1e-9
    assert abs(geometry3.distance_point_to_plane((0, 0, 2), (0, 0, 0), (0, 0, 1)) - 2) < 1e-9
    assert abs(geometry3.spherical_cap_area(math.pi / 2, 2) - 8 * math.pi) < 1e-9
    assert geometry3.Plane((0, 0, 0), (1, 0, 0), (0, 1, 0)).normal() == geometry3.Point(0, 0, 1)
    for _ in range(50):
        points = [tuple(random.randint(-5, 5) for _ in range(random.randint(1, 5))) for _ in range(8)]
        dimension = len(points[0])
        points = [point[:dimension] if len(point) >= dimension else point + (0,) * (dimension - len(point)) for point in points]
        expected = max(sum(abs(a[i] - b[i]) for i in range(dimension)) for a in points for b in points)
        assert geometry.maximum_manhattan_distance(points) == expected


def test_number_theory_and_combinatorics():
    """Run the test number theory and combinatorics operation."""
    power = load('NumberTheory', 'modular_power')
    gray = load('NumberTheory', 'gray_code')
    division = load('NumberTheory', 'ceil_div')
    crt = load('NumberTheory', 'extended_gcd_crt')
    floor = load('NumberTheory', 'floor_sum')
    sieve = load('NumberTheory', 'linear_sieve')
    factor = load('NumberTheory', 'factorization')
    phi_module = load('NumberTheory', 'euler_phi')
    mobius = load('NumberTheory', 'mobius_sieve')
    blocks = load('NumberTheory', 'quotient_blocks')
    pollard = load('NumberTheory', 'miller_rabin_pollard_rho')
    binomial = load('Combinatorics', 'binomial_mod_prime')
    pascal = load('Combinatorics', 'pascal_triangle')
    lucas = load('Combinatorics', 'lucas_theorem')
    composite = load('Combinatorics', 'binomial_composite_mod')
    stirling = load('Combinatorics', 'stirling_numbers')

    for _ in range(100):
        base, exponent, modulus = random.randint(-100, 100), random.randint(0, 100), random.randint(1, 100)
        assert power.modular_power(base, exponent, modulus) == pow(base, exponent, modulus)
        value = random.randint(0, 10000)
        assert gray.gray_code(value) == value ^ (value >> 1)
        numerator = random.randint(-1000, 1000)
        denominator = random.choice([value for value in range(-20, 21) if value])
        assert division.ceil_div(numerator, denominator) == int(math.ceil(float(numerator) / denominator))
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        gcd, x, y = crt.extended_gcd(a, b)
        assert gcd == math.gcd(a, b) and a * x + b * y == gcd
        n, m = random.randint(0, 30), random.randint(1, 20)
        multiplier, offset = random.randint(-30, 30), random.randint(-30, 30)
        assert floor.floor_sum(n, m, multiplier, offset) == sum(
            (multiplier * i + offset) // m for i in range(n))

    for _ in range(100):
        congruences = [(random.randrange(modulus), modulus)
                       for modulus in [random.randint(1, 10) for _ in range(random.randint(0, 4))]]
        actual = crt.chinese_remainder(congruences)
        limit = 1
        for _, modulus in congruences:
            limit *= modulus
        solutions = [value for value in range(max(1, limit))
                     if all(value % modulus == remainder for remainder, modulus in congruences)]
        assert (actual is None) == (not solutions)
        assert actual is None or all(actual[0] % modulus == remainder for remainder, modulus in congruences)

    primes, minimum_prime, phi_values, mu_values = sieve.linear_sieve(500)
    expected_primes = [value for value in range(2, 501)
                       if all(value % divisor for divisor in range(2, int(value ** 0.5) + 1))]
    assert primes == expected_primes
    assert all(minimum_prime[value] == next(prime for prime in primes if value % prime == 0)
               for value in range(2, 501))
    for value in range(1, 501):
        expected_phi = sum(math.gcd(value, other) == 1 for other in range(1, value + 1))
        assert phi_values[value] == phi_module.euler_phi(value) == expected_phi
        factors = factor.prime_factorization(value)
        rebuilt = 1
        for prime, exponent in factors:
            rebuilt *= prime ** exponent
        assert rebuilt == value
        assert factor.divisors(value) == [divisor for divisor in range(1, value + 1) if value % divisor == 0]
    assert mobius.mobius_sieve(500) == mu_values

    for n in range(1, 200):
        covered = []
        for left, right, quotient in blocks.quotient_blocks(n):
            covered.extend(range(left, right + 1))
            assert all(n // index == quotient for index in range(left, right + 1))
        assert covered == list(range(1, n + 1))

    for value in range(1, 2000):
        expected_prime = value >= 2 and all(value % divisor for divisor in range(2, int(value ** 0.5) + 1))
        assert pollard.is_prime(value) == expected_prime
    for value in [1, 2, 97, 2 ** 20, 99991 * 100003, 1000000007 * 1000000009]:
        factors = pollard.factorize(value)
        product = 1
        for prime in factors:
            assert pollard.is_prime(prime)
            product *= prime
        assert product == value

    comb = binomial.BinomialModPrime(100, 1000000007)
    try:
        binomial.BinomialModPrime(7, 7)
        assert False
    except ValueError:
        pass
    triangle = pascal.pascal_triangle(30)
    for n in range(31):
        for k in range(n + 1):
            expected = choose(n, k)
            assert comb.combination(n, k) == expected % 1000000007
            assert triangle[n][k] == expected
    for prime in (2, 3, 5, 7, 11):
        for n in range(80):
            for k in range(n + 1):
                assert lucas.lucas(n, k, prime) == choose(n, k) % prime
    for modulus in range(1, 50):
        for n in range(25):
            for k in range(n + 1):
                assert composite.binomial_mod(n, k, modulus) == choose(n, k) % modulus

    second = [[0] * 9 for _ in range(9)]
    first = [[0] * 9 for _ in range(9)]
    second[0][0] = first[0][0] = 1
    for n in range(1, 9):
        for k in range(1, n + 1):
            second[n][k] = second[n - 1][k - 1] + k * second[n - 1][k]
            first[n][k] = first[n - 1][k - 1] + (n - 1) * first[n - 1][k]
            assert stirling.stirling_second_kind(n, k) == second[n][k]
            assert stirling.stirling_first_kind_unsigned(n, k) == first[n][k]


def test_strings():
    """Run the test strings operation."""
    z_module = load('Strings', 'z_function')
    manacher_module = load('Strings', 'manacher')
    kmp_module = load('Strings', 'kmp')
    suffix_array_module = load('Strings', 'suffix_array')
    automaton_module = load('Strings', 'suffix_automaton')
    aho_module = load('Strings', 'aho_corasick')
    hash_module = load('Strings', 'rolling_hash')

    for _ in range(200):
        text = ''.join(random.choice('abc') for _ in range(random.randint(0, 30)))
        z = z_module.z_function(text)
        expected_z = []
        for i in range(len(text)):
            length = 0
            while i + length < len(text) and text[length] == text[i + length]:
                length += 1
            expected_z.append(length)
        assert z == expected_z

        odd, even = manacher_module.manacher(text)
        for i in range(len(text)):
            expected_odd = 1
            while i - expected_odd >= 0 and i + expected_odd < len(text) \
                    and text[i - expected_odd] == text[i + expected_odd]:
                expected_odd += 1
            expected_even = 0
            while i - expected_even - 1 >= 0 and i + expected_even < len(text) \
                    and text[i - expected_even - 1] == text[i + expected_even]:
                expected_even += 1
            assert (odd[i], even[i]) == (expected_odd, expected_even)

        pattern = ''.join(random.choice('abc') for _ in range(random.randint(0, 7)))
        expected_positions = [] if not pattern else [
            i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern
        ]
        assert kmp_module.kmp_search(text, pattern) == expected_positions

        order, rank, lcp = suffix_array_module.suffix_array(text)
        assert order == sorted(range(len(text)), key=lambda i: text[i:])
        assert all(rank[suffix] == position for position, suffix in enumerate(order))
        for position in range(1, len(text)):
            a, b = text[order[position - 1]:], text[order[position]:]
            expected_lcp = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
            assert lcp[position] == expected_lcp

        automaton = automaton_module.SuffixAutomaton.from_sequence(text)
        substrings = {text[left:right] for left in range(len(text)) for right in range(left + 1, len(text) + 1)}
        assert automaton.count_distinct_substrings() == len(substrings)
        assert all(automaton.contains(value) for value in substrings)

        rolling_hash = hash_module.RollingHash(text)
        for _ in range(20):
            left = random.randint(0, len(text))
            right = random.randint(left, len(text))
            length = right - left
            other = random.randint(0, len(text) - length) if length <= len(text) else 0
            if text[left:right] == text[other:other + length]:
                assert rolling_hash.hash(left, right) == rolling_hash.hash(other, other + length)

    for _ in range(80):
        patterns = [''.join(random.choice('abc') for _ in range(random.randint(1, 5)))
                    for _ in range(random.randint(0, 8))]
        text = ''.join(random.choice('abc') for _ in range(random.randint(0, 30)))
        aho = aho_module.AhoCorasick()
        for pattern_id, pattern in enumerate(patterns):
            aho.add(pattern, pattern_id)
        actual = sorted(aho.find_all(text))
        expected = sorted((end, pattern_id) for pattern_id, pattern in enumerate(patterns)
                          for end in range(len(pattern) - 1, len(text))
                          if text[end - len(pattern) + 1:end + 1] == pattern)
        assert actual == expected


def test_supplemental_graph():
    """Run the test supplemental graph operation."""
    boruvka_module = load('Graph', 'boruvka')
    reconstruction = load('Graph', 'kruskal_reconstruction_tree')
    ebcc = load('Graph', 'edge_biconnected_components')
    hungarian_module = load('Graph', 'hungarian')
    blossom = load('Graph', 'blossom_matching')
    lower_flow = load('Graph', 'lower_bound_flow')
    sack_module = load('Graph', 'dsu_on_tree')
    tour_module = load('Graph', 'tree_euler_tour')
    centroid_module = load('Graph', 'tree_centroids')
    bipartite = load('Graph', 'bipartite_check')
    cycle = load('Graph', 'cycle_detection')
    closure = load('Graph', 'transitive_closure')
    spfa_module = load('Graph', 'spfa')
    dense_module = load('Graph', 'dense_prim')
    kruskal_module = load('Graph', 'kruskal')

    for _ in range(50):
        n = random.randint(1, 8)
        edges = [(random.randint(-5, 15), u, v) for u in range(n) for v in range(u + 1, n)
                 if random.random() < 0.4]
        assert boruvka_module.boruvka(n, edges)[0] == kruskal_module.kruskal(n, edges)[0]
    assert boruvka_module.boruvka(3, [(1, 0, 1)])[0] is None

    for _ in range(40):
        n = random.randint(1, 8)
        edges = [(random.randint(-5, 12), u, v) for u in range(n) for v in range(u + 1, n)
                 if random.random() < 0.45]
        children, weights, roots = reconstruction.kruskal_reconstruction_tree(n, edges)
        parent = [-1] * len(children)
        for u, pair in enumerate(children):
            for v in pair:
                assert parent[v] == -1
                parent[v] = u
                assert weights[v] is None or weights[v] <= weights[u]
        assert roots == [u for u in range(len(children)) if parent[u] == -1]
        best = [[float('inf')] * n for _ in range(n)]
        for u in range(n):
            best[u][u] = float('-inf')
        for weight, u, v in edges:
            best[u][v] = best[v][u] = min(best[u][v], weight)
        for middle in range(n):
            for u in range(n):
                for v in range(n):
                    best[u][v] = min(best[u][v], max(best[u][middle], best[middle][v]))
        for u in range(n):
            ancestors = set()
            x = u
            while x != -1:
                ancestors.add(x)
                x = parent[x]
            for v in range(u + 1, n):
                x = v
                while x != -1 and x not in ancestors:
                    x = parent[x]
                assert (x == -1) == (best[u][v] == float('inf'))
                if x != -1:
                    assert weights[x] == best[u][v]

    def component_count(n, edges, skipped=-1, forbidden=None):
        """Run the component count operation."""
        graph = [[] for _ in range(n)]
        for edge_id, (u, v) in enumerate(edges):
            if edge_id != skipped and (forbidden is None or edge_id not in forbidden):
                graph[u].append(v)
                graph[v].append(u)
        count = 0
        labels = [-1] * n
        for start in range(n):
            if labels[start] != -1:
                continue
            stack = [start]
            labels[start] = count
            while stack:
                u = stack.pop()
                for v in graph[u]:
                    if labels[v] == -1:
                        labels[v] = count
                        stack.append(v)
            count += 1
        return count, labels

    for _ in range(50):
        n = random.randint(1, 8)
        edges = []
        for u in range(n):
            for v in range(u + 1, n):
                edges.extend([(u, v)] * random.randint(0, 2))
        ids, components, bridges, tree = ebcc.edge_biconnected_components(n, edges)
        base = component_count(n, edges)[0]
        expected = [i for i in range(len(edges)) if component_count(n, edges, i)[0] > base]
        assert bridges == expected
        _, labels = component_count(n, edges, forbidden=set(bridges))
        assert all((ids[u] == ids[v]) == (labels[u] == labels[v]) for u in range(n) for v in range(n))
        assert sum(map(len, components)) == n and sum(map(len, tree)) == 2 * len(bridges)

    for _ in range(60):
        rows = random.randint(0, 5)
        columns = random.randint(rows, 6)
        cost = [[random.randint(-10, 15) for _ in range(columns)] for _ in range(rows)]
        actual, assignment = hungarian_module.hungarian(cost)
        expected = min((sum(cost[i][p[i]] for i in range(rows))
                        for p in itertools.permutations(range(columns), rows)), default=0)
        assert actual == expected == sum(cost[i][assignment[i]] for i in range(rows))
        assert len(set(assignment)) == rows

    def brute_matching(graph):
        """Run the brute matching operation."""
        memo = {}

        def solve(mask):
            """Run the solve operation."""
            if not mask:
                return 0
            if mask in memo:
                return memo[mask]
            u = (mask & -mask).bit_length() - 1
            answer = solve(mask ^ (1 << u))
            for v in graph[u]:
                if mask >> v & 1:
                    answer = max(answer, 1 + solve(mask ^ (1 << u) ^ (1 << v)))
            memo[mask] = answer
            return answer

        return solve((1 << len(graph)) - 1)

    for _ in range(100):
        n = random.randint(0, 9)
        graph = [[] for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.4:
                    graph[u].append(v)
                    graph[v].append(u)
        mate = blossom.maximum_matching(graph)
        assert all(v == -1 or mate[v] == u and v in graph[u] for u, v in enumerate(mate))
        assert sum(v != -1 for v in mate) // 2 == brute_matching(graph)

    def brute_flows(n, edges, source=None, sink=None):
        """Run the brute flows operation."""
        for flows in itertools.product(*(range(lower, upper + 1) for _, _, lower, upper in edges)):
            balance = [0] * n
            for flow, (u, v, _, _) in zip(flows, edges):
                balance[u] -= flow
                balance[v] += flow
            if source is None:
                if all(value == 0 for value in balance):
                    return flows, 0
            elif all(balance[u] == 0 for u in range(n) if u not in (source, sink)) \
                    and balance[source] <= 0 and balance[sink] == -balance[source]:
                return flows, -balance[source]
        return None

    for with_terminals in (False, True):
        for _ in range(80):
            n = random.randint(2, 4)
            edges = []
            for _ in range(random.randint(0, 5)):
                u, v = random.sample(range(n), 2)
                lower = random.randint(0, 2)
                edges.append((u, v, lower, lower + random.randint(0, 2)))
            network = lower_flow.LowerBoundFlow(n)
            for edge in edges:
                network.add_edge(*edge)
            source, sink = (0, n - 1) if with_terminals else (None, None)
            actual = network.feasible(source, sink)
            expected = brute_flows(n, edges, source, sink)
            assert (actual is None) == (expected is None)
            if actual is not None:
                flows, value = actual
                assert all(lower <= flow <= upper for flow, (_, _, lower, upper) in zip(flows, edges))
                balance = [0] * n
                for flow, (u, v, _, _) in zip(flows, edges):
                    balance[u] -= flow
                    balance[v] += flow
                if source is None:
                    assert all(item == 0 for item in balance) and value == 0
                else:
                    assert all(balance[u] == 0 for u in range(n) if u not in (source, sink))
                    assert balance[source] == -value and balance[sink] == value and value >= 0
    for source, sink in ((0, None), (None, 1), (0, 0), (-1, 1), (0, 2)):
        try:
            lower_flow.LowerBoundFlow(2).feasible(source, sink)
            assert False
        except ValueError:
            pass

    for _ in range(40):
        n = random.randint(1, 30)
        graph = [[] for _ in range(n)]
        for v in range(1, n):
            u = random.randrange(v)
            graph[u].append(v)
            graph[v].append(u)
        tin, tout, preorder, parent, depth = tour_module.tree_euler_tour(graph)
        assert sorted(preorder) == list(range(n))
        assert all(preorder[tin[u]] == u and tout[u] - tin[u] >= 1 for u in range(n))
        assert all(parent[v] == -1 or depth[v] == depth[parent[v]] + 1 for v in range(n))
        subtree = [set(preorder[tin[u]:tout[u]]) for u in range(n)]
        active = set()
        sack_module.dsu_on_tree(graph, active.add, active.remove,
                                lambda u: (_ for _ in ()).throw(AssertionError()) if active != subtree[u] else None)
        expected_centroids = []
        for banned in range(n):
            seen = {banned}
            largest = 0
            for start in range(n):
                if start in seen:
                    continue
                size = 0
                stack = [start]
                seen.add(start)
                while stack:
                    u = stack.pop()
                    size += 1
                    for v in graph[u]:
                        if v not in seen:
                            seen.add(v)
                            stack.append(v)
                largest = max(largest, size)
            if 2 * largest <= n:
                expected_centroids.append(banned)
        assert centroid_module.tree_centroids(graph) == expected_centroids

    for _ in range(80):
        n = random.randint(0, 7)
        graph = [[] for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.35:
                    graph[u].append(v)
                    graph[v].append(u)
        possible = any(all(colors[u] != colors[v] for u in range(n) for v in graph[u])
                       for colors in itertools.product((0, 1), repeat=n))
        valid, colors = bipartite.bipartite_coloring(graph)
        assert valid == possible
        assert not valid or all(colors[u] != colors[v] for u in range(n) for v in graph[u])

    for _ in range(80):
        n = random.randint(1, 8)
        directed = [[v for v in range(n) if random.random() < 0.2] for _ in range(n)]
        found = cycle.find_directed_cycle(directed)
        indegree = [0] * n
        for u in range(n):
            for v in directed[u]:
                indegree[v] += 1
        queue = deque(u for u in range(n) if indegree[u] == 0)
        removed = 0
        while queue:
            u = queue.popleft()
            removed += 1
            for v in directed[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.append(v)
        assert bool(found) == (removed < n)
        assert not found or found[0] == found[-1] and all(v in directed[u] for u, v in zip(found, found[1:]))

        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.25]
        found = cycle.find_undirected_cycle(n, edges)
        components = component_count(n, edges)[0]
        assert bool(found) == (len(edges) > n - components)
        edge_set = {tuple(sorted(edge)) for edge in edges}
        assert not found or found[0] == found[-1] and all(tuple(sorted(edge)) in edge_set
                                                             for edge in zip(found, found[1:]))

    for _ in range(80):
        n = random.randint(1, 10)
        graph = [[] for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if random.random() < 0.2:
                    graph[u].extend([v] * random.randint(1, 3))
        masks = closure.transitive_closure(graph)
        distances = all_pairs_unweighted(graph)
        assert all(bool(masks[u] >> v & 1) == (distances[u][v] >= 0) for u in range(n) for v in range(n))

    for _ in range(60):
        n = random.randint(1, 10)
        graph = [[] for _ in range(n)]
        expected = [float('inf')] * n
        expected[0] = 0
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.25:
                    weight = random.randint(-8, 12)
                    graph[u].append((v, weight))
                    expected[v] = min(expected[v], expected[u] + weight)
        actual, _, negative = spfa_module.spfa(graph, 0)
        assert not negative and actual == expected
    assert spfa_module.spfa([[(1, 0)], [(2, -1)], [(1, 0)]], 0)[2]

    for _ in range(60):
        n = random.randint(0, 9)
        matrix = [[float('inf')] * n for _ in range(n)]
        edges = []
        for u in range(n):
            matrix[u][u] = 0
            for v in range(u + 1, n):
                if random.random() < 0.4:
                    weight = random.randint(-8, 15)
                    matrix[u][v] = matrix[v][u] = weight
                    edges.append((weight, u, v))
        assert dense_module.dense_prim(matrix)[0] == kruskal_module.kruskal(n, edges)[0]


def test_supplemental_data_structures():
    """Run the test supplemental data structures operation."""
    dual_module = load('DataStructures', 'dual_heap')
    top_k_module = load('DataStructures', 'top_k')
    zobrist_module = load('DataStructures', 'zobrist_hash')
    trace_module = load('DataStructures', 'linear_basis_trace')
    timestamp_module = load('DataStructures', 'timestamp_linear_basis')
    mo_module = load('DataStructures', 'mo_distinct')
    cartesian_module = load('DataStructures', 'cartesian_tree')
    connectivity_module = load('DataStructures', 'offline_dynamic_connectivity')
    sqrt_module = load('DataStructures', 'sqrt_decomposition')
    bitset_module = load('DataStructures', 'bitset')
    venice_module = load('DataStructures', 'venice_set')
    bit_tree_module = load('DataStructures', 'bit_segment_tree')
    splay_module = load('DataStructures', 'splay_multiset')

    for _ in range(30):
        heap = dual_module.DualHeap()
        values = []
        for _ in range(150):
            value = random.randint(-15, 15)
            if not values or random.random() < 0.6:
                heap.add(value)
                bisect.insort(values, value)
            else:
                expected = value in values
                assert heap.discard(value) == expected
                if expected:
                    values.remove(value)
            assert len(heap) == len(values)
            if values:
                median = values[(len(values) - 1) // 2]
                assert heap.median() == median
                assert heap.deviation_sum() == sum(abs(value - median) for value in values)
        while values:
            value = random.choice(values)
            assert heap.discard(value)
            values.remove(value)
        assert not heap.discard(0)

    for _ in range(40):
        k = random.randint(0, 8)
        top_k = top_k_module.TopKSum(k)
        values = []
        for _ in range(150):
            value = random.randint(-20, 20)
            if not values or random.random() < 0.6:
                top_k.add(value)
                values.append(value)
            else:
                expected = value in values
                assert top_k.discard(value) == expected
                if expected:
                    values.remove(value)
            if random.random() < 0.15:
                k = random.randint(0, 10)
                top_k.change_k(k)
            ordered = sorted(values)
            take = min(k, len(values))
            assert top_k.sum_largest() == (sum(ordered[-take:]) if take else 0)
            if k and len(values) >= k:
                assert top_k.kth_largest() == ordered[-k]

    first = zobrist_module.ZobristHash(12345)
    second = zobrist_module.ZobristHash(12345)
    parity = set()
    for _ in range(200):
        item = (random.randint(0, 10), random.choice('abc'))
        assert first.toggle(item) == second.toggle(item)
        parity.symmetric_difference_update([item])
        expected = 0
        for value in parity:
            expected ^= first.codes[value]
        assert first.digest() == expected

    for _ in range(80):
        values = [random.randrange(64) for _ in range(random.randint(0, 9))]
        basis = trace_module.TraceableXorBasis(5)
        for item_id, value in enumerate(values):
            basis.insert(value, item_id)
        possible = {0}
        for value in values:
            possible |= {current ^ value for current in list(possible)}
        for target in range(64):
            trace = basis.represent(target)
            assert (trace is not None) == (target in possible)
            assert trace is None or target == __import__('functools').reduce(
                lambda result, item_id: result ^ values[item_id], trace, 0)

    for _ in range(80):
        entries = [(random.randrange(64), random.randint(0, 12)) for _ in range(random.randint(0, 10))]
        basis = timestamp_module.TimestampXorBasis(5)
        for value, timestamp in entries:
            basis.insert(value, timestamp)
        for minimum in range(14):
            possible = {0}
            for value, timestamp in entries:
                if timestamp >= minimum:
                    possible |= {current ^ value for current in list(possible)}
            assert all(basis.can_represent(value, minimum) == (value in possible) for value in range(64))

    for _ in range(100):
        n = random.randint(0, 30)
        values = [random.randint(-5, 5) for _ in range(n)]
        queries = []
        for _ in range(random.randint(0, 40)):
            if n:
                left = random.randint(1, n)
                right = random.randint(left, n)
                queries.append((left, right))
        assert mo_module.mo_distinct_counts(values, queries) == [len(set(values[left - 1:right]))
                                                                  for left, right in queries]

    for minimum in (False, True):
        for _ in range(80):
            values = [random.randint(-10, 10) for _ in range(random.randint(0, 30))]
            root, parent, left, right = cartesian_module.cartesian_tree(values, minimum)
            if not values:
                assert root == 0
                continue
            order = []
            stack = []
            node = root
            while stack or node:
                while node:
                    stack.append(node)
                    node = left[node]
                node = stack.pop()
                order.append(node)
                node = right[node]
            assert order == list(range(1, len(values) + 1))
            assert parent[root] == 0 and parent[1:].count(0) == 1
            for child in range(1, len(values) + 1):
                if parent[child] != 0:
                    assert child in (left[parent[child]], right[parent[child]])
                    assert (values[parent[child] - 1] <= values[child - 1]) if minimum \
                        else (values[parent[child] - 1] >= values[child - 1])

    for _ in range(80):
        n = random.randint(2, 8)
        operations = []
        active = Counter()
        expected = []
        pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
        for _ in range(random.randint(0, 80)):
            choice = random.random()
            if choice < 0.4:
                edge = random.choice(pairs)
                active[edge] += 1
                operations.append(('add',) + edge)
            elif choice < 0.65 and any(active.values()):
                edge = random.choice([edge for edge, count in active.items() if count])
                active[edge] -= 1
                operations.append(('remove',) + edge)
            else:
                query = random.choice(pairs)
                graph = [[] for _ in range(n + 1)]
                for (u, v), count in active.items():
                    if count:
                        graph[u].append(v)
                        graph[v].append(u)
                seen = {query[0]}
                stack = [query[0]]
                while stack:
                    u = stack.pop()
                    for v in graph[u]:
                        if v not in seen:
                            seen.add(v)
                            stack.append(v)
                expected.append(query[1] in seen)
                operations.append(('query',) + query)
        assert connectivity_module.offline_dynamic_connectivity(n, operations) == expected

    for _ in range(50):
        values = [random.randint(-10, 10) for _ in range(random.randint(1, 40))]
        structure = sqrt_module.RangeAddPointQuery(values)
        for _ in range(100):
            if random.random() < 0.7:
                left = random.randint(1, len(values))
                right = random.randint(left, len(values))
                delta = random.randint(-10, 10)
                structure.add(left, right, delta)
                values[left - 1:right] = [value + delta for value in values[left - 1:right]]
            else:
                index = random.randint(1, len(values))
                assert structure.get(index) == values[index - 1]

    bits = bitset_module.Bitset(4, 0b1011)
    assert str(bits) == '1101'
    assert bits.calc() == 4
    assert str(bitset_module.Bitset.extract(bits, 1, 2)) == '10'

    for _ in range(40):
        structure = venice_module.VeniceSet()
        values = []
        for _ in range(150):
            choice = random.random()
            if not values or choice < 0.45:
                value = random.randint(-20, 20)
                structure.add(value)
                values.append(value)
            elif choice < 0.7:
                delta = random.randint(-10, 10)
                structure.add_all(delta)
                values = [value + delta for value in values]
            else:
                value = random.randint(-20, 20)
                expected = value in values
                assert structure.discard(value) == expected
                if expected:
                    values.remove(value)
            assert len(structure) == len(values)
            if values:
                assert structure.minimum() == min(values)

    empty = bit_tree_module.BitSegmentTree([])
    assert empty.count(1, 0) == 0
    try:
        empty.kth_one(1)
        assert False
    except IndexError:
        pass
    for _ in range(60):
        bits = [random.randrange(2) for _ in range(random.randint(1, 40))]
        tree = bit_tree_module.BitSegmentTree(bits)
        for _ in range(120):
            left = random.randint(1, len(bits))
            right = random.randint(left, len(bits))
            choice = random.randrange(3)
            if choice == 0:
                value = random.randrange(2)
                tree.assign(left, right, value)
                bits[left - 1:right] = [value] * (right - left + 1)
            elif choice == 1:
                tree.flip(left, right)
                bits[left - 1:right] = [value ^ 1 for value in bits[left - 1:right]]
            else:
                assert tree.count(left, right) == sum(bits[left - 1:right])
            positions = [i + 1 for i, value in enumerate(bits) if value]
            if positions:
                k = random.randint(1, len(positions))
                assert tree.kth_one(k) == positions[k - 1]

    for _ in range(40):
        tree = splay_module.SplayMultiset()
        values = []
        for _ in range(200):
            value = random.randint(-30, 30)
            if not values or random.random() < 0.65:
                tree.insert(value)
                bisect.insort(values, value)
            else:
                expected = value in values
                assert tree.discard(value) == expected
                if expected:
                    values.remove(value)
            assert len(tree) == len(values)
            if values:
                query = random.randint(-35, 35)
                assert tree.rank(query) == bisect.bisect_left(values, query) + 1
                assert tree.predecessor(query) == (values[bisect.bisect_left(values, query) - 1]
                                                   if bisect.bisect_left(values, query) else None)
                position = bisect.bisect_right(values, query)
                assert tree.successor(query) == (values[position] if position < len(values) else None)
                index = random.randint(1, len(values))
                assert tree.kth(index) == values[index - 1]

    # C++-compatible closed intervals, Info/Tag, search, and persistence.
    segment_module = load('DataStructures', 'segment_tree')
    lazy_module = load('DataStructures', 'lazy_segment_tree')
    li_chao_module = load('DataStructures', 'li_chao_tree')
    persistent_module = load('DataStructures', 'persistent_segment_tree')
    trie_module = load('DataStructures', 'trie')
    fenwick_module = load('DataStructures', 'fenwick_tree')
    dsu_module = load('DataStructures', 'disjoint_set_union')
    sparse_module = load('DataStructures', 'sparse_table')

    segment = segment_module.SegmentTree([1, 2, 3, 4])
    assert segment.range_query(2, 3) == 5
    segment.modify(2, 8)
    assert segment.find_first(1, 4, lambda value: value > 7) == 2
    assert segment.find_last(1, 4, lambda value: value > 7) == 2
    zkw = segment_module.ZKWSegmentTree([None, 'a', 'b', 'c'], identity='')
    assert zkw.range_query(1, 3) == 'abc'

    lazy = lazy_module.LazySegmentTree([1, 2, 3, 4])
    lazy.range_apply(2, 3, 5)
    assert lazy.range_query(1, 4) == 20
    assert lazy.find_first(1, 4, lambda value: value >= 15) == -1
    custom = lazy_module.LazySegmentTree(
        [lazy_module.SumInfo(1), lazy_module.SumInfo(2), lazy_module.SumInfo(3)],
        info_type=lazy_module.SumInfo,
        tag_type=lazy_module.AffineTag,
    )
    custom.range_apply(1, 2, lazy_module.AffineTag(2, 1))
    assert custom.range_query(1, 2).sum == 8

    minimum = li_chao_module.LiChaoTree(-5, 5, 'min')
    maximum = li_chao_module.LiChaoTree(-5, 5, 'max')
    minimum.add_segment(1, 0, -5, 5)
    minimum.add_segment(-1, 0, -2, 2)
    maximum.add_line(1, 0)
    maximum.add_line(-1, 0)
    assert minimum.query(-2) == -2 and minimum.query(4) == 4
    assert maximum.query(-3) == 3 and maximum.query(3) == 3

    tree = persistent_module.PersistentSegmentTree(8)
    root = tree.empty_root
    for value in (1, 3, 3, 7):
        root = tree.add(root, value)
    assert tree.count_leq(tree.empty_root, root, 3) == 3
    assert tree.max_less(tree.empty_root, root, 7) == 3
    assert tree.max_value(root) == 7
    assert tree.kth(tree.empty_root, root, 3) == 3
    max_tree = persistent_module.PersistentMaxIndexTree([None, 5, 2, 7])
    max_root = max_tree.update(max_tree.empty_root, 2, 9)
    assert max_tree.query(max_root, 1, 3) == (9, 7)

    automaton = trie_module.AhoCorasick()
    automaton.insert('he', 0)
    automaton.insert('she', 1)
    automaton.insert('hers', 2)
    automaton.insert('his', 3)
    assert set(automaton.search('ushers')) == {(4, 1), (4, 0), (6, 2)}

    zero_based_calls = [
        lambda: fenwick_module.FenwickTree(3).add(0, 1),
        lambda: bit_tree_module.BitSegmentTree([0]).flip(0, 1),
        lambda: dsu_module.DisjointSetUnion(3).find(0),
        lambda: sparse_module.SparseTable([1]).query(0, 1),
        lambda: sqrt_module.RangeAddPointQuery([1]).get(0),
    ]
    for call in zero_based_calls:
        try:
            call()
            assert False
        except IndexError:
            pass


def test_supplemental_geometry():
    """Run the test supplemental geometry operation."""
    polar = intersections = tangents = triangles = convex_contains = load('Geometry', 'geometry_2d')
    chebyshev = segment_union = minkowski = pick = hull_module = point_polygon = polar
    hull3 = load('Geometry', 'geometry_3d')

    for _ in range(100):
        origin = random.randint(-3, 3), random.randint(-3, 3)
        points = [(random.randint(-8, 8), random.randint(-8, 8)) for _ in range(30)]

        def angle_key(point):
            """Run the angle key operation."""
            x, y = point[0] - origin[0], point[1] - origin[1]
            angle = math.atan2(y, x)
            return (angle + 2 * math.pi if angle < 0 else angle, x * x + y * y)

        assert polar.polar_sort(points, origin) == sorted(points, key=angle_key)

    def cross(a, b, c):
        """Run the cross operation."""
        return ((b[0] - a[0]) * (c[1] - a[1])
                - (b[1] - a[1]) * (c[0] - a[0]))

    def on_segment(point, a, b):
        """Run the on segment operation."""
        return cross(a, b, point) == 0 and all(min(x, y) <= value <= max(x, y)
                                                for x, y, value in zip(a, b, point))

    def exact_intersections(a, b, c, d):
        """Run the exact intersections operation."""
        denominator = cross((0, 0), (b[0] - a[0], b[1] - a[1]),
                            (d[0] - c[0], d[1] - c[1]))
        if denominator:
            numerator = cross((0, 0), (c[0] - a[0], c[1] - a[1]),
                              (d[0] - c[0], d[1] - c[1]))
            ratio = Fraction(numerator, denominator)
            point = (Fraction(a[0]) + ratio * (b[0] - a[0]),
                     Fraction(a[1]) + ratio * (b[1] - a[1]))
            return [point] if on_segment(point, a, b) and on_segment(point, c, d) else []
        if cross(a, b, c):
            return []
        common = sorted(set(point for point in (a, b, c, d)
                            if on_segment(point, a, b) and on_segment(point, c, d)))
        return common[:1] if len(common) == 1 else [common[0], common[-1]] if common else []

    for _ in range(400):
        a, b, c, d = [tuple(random.randint(-4, 4) for _ in range(2)) for _ in range(4)]
        actual = intersections.segment_intersection_points(a, b, c, d)
        expected = exact_intersections(a, b, c, d)
        assert len(actual) == len(expected)
        assert all(abs(float(x) - point[0]) < 1e-8 and abs(float(y) - point[1]) < 1e-8
                   for point, (x, y) in zip(actual, expected))

    for _ in range(100):
        center_a = random.randint(-8, 8), random.randint(-8, 8)
        center_b = random.randint(-8, 8), random.randint(-8, 8)
        if center_a == center_b:
            center_b = center_b[0] + 1, center_b[1]
        radius_a, radius_b = random.randint(1, 5), random.randint(1, 5)
        result = tangents.common_tangents(center_a, radius_a, center_b, radius_b)
        distance = math.hypot(center_a[0] - center_b[0], center_a[1] - center_b[1])

        def tangent_count(threshold):
            """Run the tangent count operation."""
            return 0 if distance < threshold - 1e-9 else 1 if abs(distance - threshold) <= 1e-9 else 2

        assert len(result) == tangent_count(abs(radius_a - radius_b)) + tangent_count(radius_a + radius_b)
        assert len({tuple(round(value, 8) for point in pair for value in point) for pair in result}) == len(result)
        for point_a, point_b in result:
            assert abs(math.hypot(point_a[0] - center_a[0], point_a[1] - center_a[1]) - radius_a) < 1e-7
            assert abs(math.hypot(point_b[0] - center_b[0], point_b[1] - center_b[1]) - radius_b) < 1e-7
            direction = point_b[0] - point_a[0], point_b[1] - point_a[1]
            if math.hypot(*direction) > 1e-8:
                assert abs(direction[0] * (point_a[0] - center_a[0])
                           + direction[1] * (point_a[1] - center_a[1])) < 1e-7
                assert abs(direction[0] * (point_b[0] - center_b[0])
                           + direction[1] * (point_b[1] - center_b[1])) < 1e-7

    for _ in range(80):
        while True:
            a, b, c = [tuple(random.randint(-8, 8) for _ in range(2)) for _ in range(3)]
            if cross(a, b, c):
                break
        incenter, inradius = triangles.triangle_incircle(a, b, c)
        side_distances = [abs(cross(x, y, incenter)) / math.hypot(x[0] - y[0], x[1] - y[1])
                          for x, y in ((a, b), (b, c), (c, a))]
        assert all(abs(value - inradius) < 1e-7 for value in side_distances)
        circumcenter, circumradius = triangles.triangle_circumcircle(a, b, c)
        assert all(abs(math.hypot(point[0] - circumcenter[0], point[1] - circumcenter[1]) - circumradius) < 1e-7
                   for point in (a, b, c))

    assert convex_contains.convex_polygon_contains([], (0, 0)) == -1
    assert convex_contains.convex_polygon_contains([(1, 2)], (1, 2)) == 0
    assert convex_contains.convex_polygon_contains([(0, 0), (2, 0)], (3, 0)) == -1
    for _ in range(100):
        points = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(30)]
        polygon = hull_module.convex_hull(points)
        if len(polygon) < 3:
            continue
        for _ in range(30):
            point = random.randint(-12, 12), random.randint(-12, 12)
            assert convex_contains.convex_polygon_contains(polygon, point) == point_polygon.point_in_polygon(point, polygon)

    for _ in range(100):
        points = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(random.randint(0, 30))]
        structure = chebyshev.ChebyshevDistanceSum(points)
        for _ in range(20):
            x, y = random.randint(-20, 20), random.randint(-20, 20)
            assert structure.query(x, y) == sum(max(abs(x - a), abs(y - b)) for a, b in points)
    floating_points = [(0.1, 0.2), (2.5, -1.25)]
    floating_sum = chebyshev.ChebyshevDistanceSum(floating_points)
    assert abs(floating_sum.query(0.3, -0.4)
               - sum(max(abs(0.3 - x), abs(-0.4 - y)) for x, y in floating_points)) < 1e-12

    for _ in range(200):
        segments = [(random.randint(-15, 15), random.randint(-15, 15)) for _ in range(random.randint(0, 20))]
        covered = set()
        for left, right in segments:
            left, right = sorted((left, right))
            covered.update(range(left, right))
        assert segment_union.segment_union_length(segments) == len(covered)

    for _ in range(100):
        polygon_a = hull_module.convex_hull([(random.randint(-8, 8), random.randint(-8, 8)) for _ in range(15)])
        polygon_b = hull_module.convex_hull([(random.randint(-8, 8), random.randint(-8, 8)) for _ in range(15)])
        if len(polygon_a) < 3 or len(polygon_b) < 3:
            continue
        actual = hull_module.convex_hull(minkowski.minkowski_sum(polygon_a, polygon_b))
        expected = hull_module.convex_hull([(a[0] + b[0], a[1] + b[1]) for a in polygon_a for b in polygon_b])
        assert actual == expected
    assert minkowski.minkowski_sum([(1, 2)], [(3, 4)]) == [(4, 6)]

    for _ in range(100):
        polygon = hull_module.convex_hull([(random.randint(-6, 6), random.randint(-6, 6)) for _ in range(20)])
        if len(polygon) < 3:
            continue
        interior, boundary = pick.lattice_polygon_points(polygon)
        minimum_x, maximum_x = min(x for x, _ in polygon), max(x for x, _ in polygon)
        minimum_y, maximum_y = min(y for _, y in polygon), max(y for _, y in polygon)
        counts = Counter(point_polygon.point_in_polygon((x, y), polygon)
                         for x in range(minimum_x, maximum_x + 1)
                         for y in range(minimum_y, maximum_y + 1))
        assert (interior, boundary) == (counts[1], counts[0])

    def volume(a, b, c, d):
        """Run the volume operation."""
        normal = ((b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1]),
                  (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2]),
                  (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
        return sum(normal[i] * (d[i] - a[i]) for i in range(3))

    for _ in range(50):
        parameters = random.sample(range(-10, 11), random.randint(4, 9))
        points = [(value, value * value, value * value * value) for value in parameters]
        random.shuffle(points)
        faces = hull3.convex_hull_faces(points)
        actual = {frozenset(face) for face in faces}
        expected = set()
        for face in itertools.combinations(range(len(points)), 3):
            signs = [volume(points[face[0]], points[face[1]], points[face[2]], points[u])
                     for u in range(len(points)) if u not in face]
            if all(value > 0 for value in signs) or all(value < 0 for value in signs):
                expected.add(frozenset(face))
        assert actual == expected and len(actual) == len(faces)
        for a, b, c in faces:
            assert all(volume(points[a], points[b], points[c], point) <= 1e-7 for point in points)


def test_supplemental_math_strings():
    """Run the test supplemental math strings operation."""
    bits = load('NumberTheory', 'bit_tricks')
    omega_module = load('NumberTheory', 'omega_sieve')
    divisor_module = load('NumberTheory', 'divisor_sieve')
    diophantine = load('NumberTheory', 'linear_diophantine')
    inversions = load('Combinatorics', 'inversion_count')
    partitions = load('Combinatorics', 'integer_partitions')
    catalan = load('Combinatorics', 'catalan')
    product_module = load('Combinatorics', 'safe_mod_product')
    palindromes = load('Strings', 'palindromic_tree')
    ntt_module = load('Polynomial', 'ntt')
    matrix_module = load('LinearAlgebra', 'matrix')
    gaussian = load('LinearAlgebra', 'gaussian_elimination')

    for value in range(1024):
        assert bits.lowbit(value) == (value & -value)
        assert bits.floor_log2(value) == value.bit_length() - 1
        assert bits.count_trailing_zeros(value) == ((value & -value).bit_length() - 1)
        expected = [mask for mask in range(value + 1) if mask & ~value == 0]
        assert sorted(bits.submasks(value, True)) == expected

    omega = omega_module.omega_sieve(500)
    divisors = divisor_module.divisor_sieve(500)
    for value in range(1, 501):
        assert divisors[value] == [item for item in range(1, value + 1) if value % item == 0]
        prime_factors = {item for item in range(2, value + 1)
                         if value % item == 0 and all(item % divisor for divisor in range(2, int(item ** 0.5) + 1))}
        assert omega[value] == len(prime_factors)

    for a in range(-8, 9):
        for b in range(-8, 9):
            for c in range(-12, 13):
                result = diophantine.solve_linear_diophantine(a, b, c)
                possible = c == 0 if a == b == 0 else c % math.gcd(a, b) == 0
                assert (result is not None) == possible
                if result is not None:
                    x, y, dx, dy = result
                    assert a * x + b * y == c
                    assert all(a * (x + dx * t) + b * (y + dy * t) == c for t in range(-3, 4))

    for _ in range(200):
        values = [random.randint(-8, 8) for _ in range(random.randint(0, 30))]
        assert inversions.inversion_count(values) == sum(values[i] > values[j]
                                                          for i in range(len(values))
                                                          for j in range(i + 1, len(values)))

    partition_values = partitions.partition_numbers(30)
    exact = [[0] * 31 for _ in range(31)]
    exact[0][0] = 1
    for total in range(1, 31):
        for parts in range(1, total + 1):
            exact[total][parts] = exact[total - 1][parts - 1]
            if total >= parts:
                exact[total][parts] += exact[total - parts][parts]
    for total in range(31):
        assert partition_values[total] == sum(exact[total])
        assert all(partitions.partitions_exact_parts(total, parts) == exact[total][parts]
                   for parts in range(total + 1))
    assert catalan.catalan_numbers(12) == [choose(2 * n, n) // (n + 1) for n in range(13)]

    for _ in range(60):
        product = product_module.SafeModProduct(101)
        values = []
        for _ in range(150):
            value = random.randint(-250, 250)
            residue = value % 101
            if not values or random.random() < 0.6:
                product.multiply(value)
                values.append(residue)
            else:
                expected = residue in values
                try:
                    product.divide(value)
                    actual = True
                except ValueError:
                    actual = False
                assert actual == expected
                if expected:
                    values.remove(residue)
            expected_product = 1
            for item in values:
                expected_product = expected_product * item % 101
            assert product.value() == expected_product
    try:
        product_module.SafeModProduct(1)
        assert False
    except ValueError:
        pass

    for _ in range(150):
        text = ''.join(random.choice('abc') for _ in range(random.randint(0, 25)))
        tree = palindromes.PalindromicTree()
        names = {}
        for index, symbol in enumerate(text):
            node = tree.add(symbol)
            names.setdefault(node, text[index - tree.length[node] + 1:index + 1])
        expected = {text[left:right] for left in range(len(text)) for right in range(left + 1, len(text) + 1)
                    if text[left:right] == text[left:right][::-1]}
        assert tree.distinct_count() == len(expected)
        occurrences = tree.propagate_occurrences()
        assert set(names.values()) == expected
        assert all(occurrences[node] == sum(text[i:i + len(value)] == value
                                            for i in range(len(text) - len(value) + 1))
                   for node, value in names.items())

    for length in [1, 2, 4, 8, 16, 32]:
        for _ in range(30):
            values = [random.randint(-1000, 1000) for _ in range(length)]
            transformed = ntt_module.ntt(values[:])
            forward = transformed[:]
            assert ntt_module.ntt(transformed, True) == [value % ntt_module.MODULUS for value in values]
            if length <= 8:
                root = pow(ntt_module.PRIMITIVE_ROOT, (ntt_module.MODULUS - 1) // length,
                           ntt_module.MODULUS)
                expected = [sum(values[j] * pow(root, i * j, ntt_module.MODULUS)
                                for j in range(length)) % ntt_module.MODULUS for i in range(length)]
                assert forward == expected
    for _ in range(150):
        a = [random.randint(-100, 100) for _ in range(random.randint(0, 25))]
        b = [random.randint(-100, 100) for _ in range(random.randint(0, 25))]
        expected = [] if not a or not b else [sum(a[i] * b[k - i] for i in range(len(a))
                                                  if 0 <= k - i < len(b)) % ntt_module.MODULUS
                                               for k in range(len(a) + len(b) - 1)]
        assert ntt_module.convolution(a, b) == expected

    for _ in range(100):
        rows, shared, columns = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
        a = [[random.randint(-5, 5) for _ in range(shared)] for _ in range(rows)]
        b = [[random.randint(-5, 5) for _ in range(columns)] for _ in range(shared)]
        expected = [[sum(a[i][k] * b[k][j] for k in range(shared)) for j in range(columns)]
                    for i in range(rows)]
        assert matrix_module.matrix_multiply(a, b) == expected
        modulus = random.randint(2, 20)
        assert matrix_module.matrix_multiply(a, b, modulus) == [[value % modulus for value in row]
                                                                 for row in expected]
    for _ in range(80):
        n = random.randint(1, 4)
        matrix = [[random.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        exponent = random.randint(0, 8)
        expected = [[int(i == j) for j in range(n)] for i in range(n)]
        for _ in range(exponent):
            expected = matrix_module.matrix_multiply(expected, matrix)
        assert matrix_module.matrix_power(matrix, exponent) == expected

    def fraction_rank(matrix):
        """Run the fraction rank operation."""
        values = [[Fraction(value) for value in row] for row in matrix]
        rows = len(values)
        columns = len(values[0]) if rows else 0
        rank = 0
        for column in range(columns):
            pivot = next((row for row in range(rank, rows) if values[row][column]), None)
            if pivot is None:
                continue
            values[rank], values[pivot] = values[pivot], values[rank]
            divisor = values[rank][column]
            values[rank] = [value / divisor for value in values[rank]]
            for row in range(rows):
                if row != rank and values[row][column]:
                    factor = values[row][column]
                    values[row] = [values[row][j] - factor * values[rank][j] for j in range(columns)]
            rank += 1
            if rank == rows:
                break
        return rank

    for _ in range(250):
        rows, columns = random.randint(1, 5), random.randint(1, 5)
        matrix = [[random.randint(-5, 5) for _ in range(columns)] for _ in range(rows)]
        vector = [random.randint(-5, 5) for _ in range(rows)]
        rank = fraction_rank(matrix)
        augmented_rank = fraction_rank([row + [value] for row, value in zip(matrix, vector)])
        expected_status = 0 if rank != augmented_rank else 1 if rank == columns else 2
        status, solution, actual_rank = gaussian.solve_linear_system(matrix, vector)
        assert status == expected_status and actual_rank == rank
        assert solution is None or all(abs(sum(matrix[i][j] * solution[j] for j in range(columns)) - vector[i]) < 1e-7
                                       for i in range(rows))
    for _ in range(100):
        n = random.randint(0, 5)
        matrix = [[random.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        expected = 0
        for permutation in itertools.permutations(range(n)):
            inversions_count = sum(permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n))
            term = (-1 if inversions_count % 2 else 1)
            for i in range(n):
                term *= matrix[i][permutation[i]]
            expected += term
        assert abs(gaussian.determinant(matrix) - expected) < 1e-7


def test_added_templates():
    """Differentially verify newly added themes and algebra operations."""
    basic = load('BasicAlgorithms', 'search_and_mapping')
    classic = load('DynamicProgramming', 'classic_dp')
    state_dp = load('DynamicProgramming', 'state_dp')
    optimized = load('DynamicProgramming', 'optimized_dp')
    games = load('GameTheory', 'game_theory')
    groups = load('GroupTheory', 'permutations')
    probability = load('Probability', 'probability')
    number = load('NumberTheory', 'extended_gcd_crt')
    factorization = load('NumberTheory', 'factorization')
    combination = load('Combinatorics', 'binomial_mod_prime')
    partitions = load('Combinatorics', 'integer_partitions')
    matrix = load('LinearAlgebra', 'matrix')
    gaussian = load('LinearAlgebra', 'gaussian_elimination')
    polynomial = load('Polynomial', 'ntt')
    automata = load('Strings', 'aho_corasick')
    timeline_module = load('DataStructures', 'offline_dynamic_connectivity')
    cost_flow = load('Graph', 'min_cost_max_flow')

    assert basic.first_true(0, 20, lambda value: value * value >= 70) == 9
    assert basic.last_true(0, 20, lambda value: value * value <= 70) == 8
    assert abs(basic.first_true_real(0, 2, lambda value: value * value >= 2) - math.sqrt(2)) < 1e-12
    point, value = basic.ternary_search(-5, 5, lambda x: -(x - 2) ** 2 + 7, True)
    assert abs(point - 2) < 1e-7 and abs(value - 7) < 1e-9
    mapping = basic.BidirectionalMap(4)
    mapping.swap_actual(1, 3)
    assert mapping.to_internal(1) == 3 and mapping.to_actual(3) == 1
    assert basic.coordinate_compress([8, 3, 8, 5]) == ([3, 5, 8], [2, 0, 2, 1])

    for _ in range(80):
        capacity = random.randint(0, 15)
        items = [(random.randint(1, 8), random.randint(-3, 15)) for _ in range(random.randint(0, 8))]
        expected = max((sum(items[i][1] for i in range(len(items)) if mask >> i & 1)
                        for mask in range(1 << len(items))
                        if sum(items[i][0] for i in range(len(items)) if mask >> i & 1) <= capacity), default=0)
        assert classic.zero_one_knapsack(capacity, items) == expected
        actual, selected = classic.zero_one_knapsack_solution(capacity, items)
        assert actual == expected
        assert sum(items[i][0] for i in selected) <= capacity
        assert sum(items[i][1] for i in selected) == actual

        values = [random.randint(-10, 10) for _ in range(random.randint(0, 10))]
        subsequence = classic.longest_increasing_subsequence(values)
        brute_lis = max((len(candidate) for length in range(len(values) + 1)
                         for candidate in itertools.combinations(values, length)
                         if all(candidate[i] < candidate[i + 1] for i in range(len(candidate) - 1))), default=0)
        assert len(subsequence) == classic.lis_length(values) == brute_lis
        if values:
            expected_subarray = max((sum(values[left:right]), left, right)
                                    for left in range(len(values)) for right in range(left + 1, len(values) + 1))[0]
            assert classic.maximum_subarray(values)[0] == expected_subarray

    assert classic.complete_knapsack(7, [(2, 3), (3, 5)]) == 11
    assert classic.bounded_knapsack(7, [(2, 3, 2), (3, 5, 1)]) == 11
    assert classic.longest_common_subsequence('abcbdab', 'bdcaba') in ('bcba', 'bdab')
    for limit in range(100):
        for target in range(12):
            assert state_dp.count_numbers_with_digit_sum(limit, target) == sum(
                sum(map(int, str(value))) == target for value in range(limit + 1))
    assert state_dp.count_accepted_strings(3, [[0, 1], [0]], 0, {1}) == 2
    sos_values = [random.randint(-5, 5) for _ in range(16)]
    sub = state_dp.subset_sums(sos_values)
    sup = state_dp.superset_sums(sos_values)
    assert all(sub[mask] == sum(sos_values[value] for value in range(16) if value & ~mask == 0)
               for mask in range(16))
    assert all(sup[mask] == sum(sos_values[value] for value in range(16) if mask & ~value == 0)
               for mask in range(16))
    assert optimized.minimum_interval_increments([1, 3, 2, 5]) == 6
    values = [3, -2, 4, -1]
    assert optimized.maximum_subarray_ceiling_penalty(values, 2, 3) == max(
        [0] + [sum(values[left:right]) - 3 * ((right - left + 1) // 2)
               for left in range(len(values)) for right in range(left + 1, len(values) + 1)])
    assert optimized.sliding_window_min_dp([3, 1, 4, 2], 2) == [0, 3, 1, 5, 3]
    assert optimized.rooted_subtree_choice_counts([[1], [0, 2], [1]]) == [3, 2, 1]
    for _ in range(100):
        values = [random.randint(-8, 10) for _ in range(random.randint(0, 10))]
        block_size = random.randint(1, 5)
        penalty = random.randint(0, 8)
        expected = max([0] + [sum(values[left:right]) - penalty *
                              ((right - left + block_size - 1) // block_size)
                              for left in range(len(values))
                              for right in range(left + 1, len(values) + 1)])
        assert optimized.maximum_subarray_ceiling_penalty(values, block_size, penalty) == expected

    assert games.bash_winning(7, 3) and not games.bash_winning(8, 3)
    assert games.nim_winning([1, 2, 4]) and not games.nim_winning([1, 2, 3])
    assert not games.anti_nim_winning([1]) and games.anti_nim_winning([1, 1])
    assert not games.wythoff_winning(3, 5) and games.wythoff_winning(2, 2)
    assert not games.fibonacci_game_winning(13) and games.fibonacci_game_winning(14)
    assert games.subtraction_game_sg(5, [1, 2]) == [0, 1, 2, 0, 1, 2]
    assert games.tree_grundy([[1, 2], [0], [0]]) == 0

    permutation = [2, 0, 1]
    inverse = groups.inverse_permutation(permutation)
    assert groups.compose_permutations(permutation, inverse) == [0, 1, 2]
    sortable = [3, 1, 2, 1]
    for left, right in groups.sorting_swaps(sortable):
        sortable[left], sortable[right] = sortable[right], sortable[left]
    assert sortable == sorted(sortable)
    assert probability.expected_value([(0.25, 2), (0.75, 6)]) == 5
    assert probability.geometric_expected_trials(0.25) == 4
    assert probability.geometric_expected_failures(0.25) == 3
    assert abs(sum(probability.geometric_probability(i, 0.5) for i in range(1, 50)) - 1) < 1e-12

    assert number.lcm(-12, 18) == 36
    assert factorization.divisor_count(360) == 24
    comb = combination.BinomialModPrime(0, 1000000007)
    assert comb.F(6) == 720 and comb.iF(6) * comb.F(6) % comb.modulus == 1
    assert comb.P2(20) == 1 << 20 and comb.A(6, 2) == 30 and comb.C(6, 2) == 15
    assert partitions.identical_balls_distinct_boxes(5, 3) == 21
    assert partitions.distinct_balls_distinct_boxes(4, 2, False) == 14
    assert partitions.distinct_balls_identical_boxes(5, 2) == 15
    assert partitions.identical_balls_identical_boxes(5, 2, False) == 2

    modulus = 1000000007
    assert matrix.matrix_add([[1, 2]], [[3, 4]]) == [[4, 6]]
    assert matrix.matrix_subtract([[1, 2]], [[3, 4]], 5) == [[3, 3]]
    status, solution, rank = gaussian.solve_linear_system_mod([[1, 1], [1, -1]], [5, 1], modulus)
    assert (status, rank) == (1, 2) and solution == [3, 2]
    inverse = gaussian.matrix_inverse_mod([[1, 2], [3, 5]], modulus)
    assert matrix.matrix_multiply([[1, 2], [3, 5]], inverse, modulus) == [[1, 0], [0, 1]]
    assert gaussian.determinant_mod([[1, 2], [3, 5]], modulus) == modulus - 1
    assert gaussian.solve_xor_system([[1, 1], [0, 1]], [1, 0]) == (1, [1, 0], 2)
    assert gaussian.spanning_tree_count(4, list(itertools.combinations(range(4), 2)), modulus) == 16

    for _ in range(40):
        left = [random.randrange(polynomial.MODULUS) for _ in range(random.randint(1, 12))]
        right = [random.randrange(polynomial.MODULUS) for _ in range(random.randint(1, 7))]
        right[-1] = right[-1] or 1
        product = polynomial.poly_multiply(left, right)
        quotient, remainder = polynomial.poly_divmod(product, right)
        assert polynomial.poly_trim(quotient) == polynomial.poly_trim(left) and not remainder
        size = random.randint(1, 12)
        formal = [1] + [random.randrange(polynomial.MODULUS) for _ in range(size - 1)]
        inverse = polynomial.poly_inverse(formal, size)
        assert polynomial.convolution(formal, inverse)[:size] == [1] + [0] * (size - 1)
        assert polynomial.poly_exp(polynomial.poly_log(formal, size), size) == formal
        square = polynomial.poly_multiply(formal, formal)[:size]
        root = polynomial.poly_sqrt(square, size)
        assert polynomial.convolution(root, root)[:size] == square
        points = random.sample(range(1, 50), random.randint(1, 7))
        expected = [polynomial.poly_evaluate(left, point) for point in points]
        assert polynomial.multipoint_evaluate(left, points) == expected
        interpolation = polynomial.lagrange_interpolate(points, expected)
        assert [polynomial.poly_evaluate(interpolation, point) for point in points] == expected
    assert polynomial.poly_power([1, 1], 4) == [1, 4, 6, 4, 1]
    assert polynomial.poly_mul_transpose([1, 2, 3], [4, 5]) == [14, 23, 12]
    counts = polynomial.subset_sum_residue_counts(5, 3)
    brute_counts = [0] * 3
    for mask in range(1 << 5):
        brute_counts[sum(index + 1 for index in range(5) if mask >> index & 1) % 3] += 1
    assert counts == brute_counts

    next_positions = automata.NextPositionAutomaton('abac')
    assert next_positions.next_after(0, 'a') == 1
    assert next_positions.next_after(1, 'a') == 3
    assert next_positions.next_after(3, 'z') == 5
    assert next_positions.is_subsequence('aac')
    timeline = timeline_module.TimeSegmentTree(3)
    timeline.add_interval(0, 2, 4)
    timeline.add_interval(1, 3, 7)
    active = []

    def apply(value):
        """Append one active timeline value."""
        active.append(value)

    def rollback(size):
        """Restore the active timeline list to a snapshot."""
        del active[size:]

    assert timeline.traverse(apply, lambda: len(active), rollback, lambda time: sum(active)) == [4, 11, 7]
    network = cost_flow.MinCostMaxFlow(3)
    network.add_edge(0, 1, 1, 5)
    network.add_edge(1, 2, 1, 0)
    network.add_edge(0, 2, 1, 1)
    assert network.max_cost_flow(0, 2, 1) == (1, 5)


def test_plan_regressions():
    """Cover the cross-language API and boundary regressions from the audit."""
    prefix_module = load('DataStructures', 'prefix_2d')
    top_k_module = load('DataStructures', 'top_k')
    mo_module = load('DataStructures', 'mo_distinct')
    dinic_module = load('Graph', 'dinic')
    topological_module = load('Graph', 'topological_sort')
    lca_module = load('Graph', 'lca')
    reconstruction_module = load('Graph', 'tree_reconstruction')
    color_coding_module = load('Graph', 'color_coding')
    kmp_module = load('Strings', 'kmp')
    manacher_module = load('Strings', 'manacher')
    geometry = load('Geometry', 'geometry_2d')
    geometry3 = load('Geometry', 'geometry_3d')

    difference = prefix_module.Diff2D(3, 4)
    difference.insert(1, 2, 2, 4, 3)
    difference.insert(10, 11, 1, 2, 9)
    expected = [[0] * 5 for _ in range(4)]
    for row in range(1, 3):
        for column in range(2, 5):
            expected[row][column] = 3
    assert difference.to_array() == expected

    top_k = top_k_module.TopKSum(1)
    for value in (4, 1, 7, 3):
        top_k.add(value)
    top_k.change_k(3)
    assert top_k.sum_largest() == 14 and top_k.kth_largest() == 3
    top_k.change_k(0)
    assert top_k.sum_largest() == 0

    values = [1, 2, 1, 3, 1, 2]
    assert mo_module.mo_frequent_values(values, [(1, 6, 2), (2, 4, 1)]) == [[1], []]
    frequencies = Counter()

    def add(index):
        """Add one 1-based array position to the active Mo range."""
        frequencies[values[index - 1]] += 1

    def remove(index):
        """Remove one 1-based array position from the active Mo range."""
        frequencies[values[index - 1]] -= 1

    assert mo_module.mo_process(len(values), [(1, 3), (2, 6)], add, remove,
                                lambda: sum(count > 0 for count in frequencies.values())) == [2, 3]
    for _ in range(60):
        current = [random.randint(-3, 3) for _ in range(random.randint(1, 20))]
        queries = []
        for _ in range(random.randint(1, 15)):
            left = random.randint(1, len(current))
            right = random.randint(left, len(current))
            queries.append((left, right, random.randint(0, right - left + 1)))
        expected = [sorted(value for value, count in Counter(current[left - 1:right]).items()
                           if count > threshold) for left, right, threshold in queries]
        assert mo_module.mo_frequent_values(current, queries) == expected

    network = dinic_module.Dinic(4)
    first = network.add_edge(0, 1, 3)
    network.add_edge(1, 3, 2)
    network.add_edge(0, 2, 2)
    network.add_edge(2, 3, 2)
    assert first == 0 and network.max_flow(0, 3) == 4
    assert network.edges()[0] == (0, 1, 3, 2)
    assert network.min_cut(0) == [True, True, False, False]

    graph = [[2], [2], []]
    assert topological_module.topological_sort(graph, lexicographical=True) == [0, 1, 2]
    tree = [[1], [0, 2, 3], [1], [1]]
    lca = lca_module.LowestCommonAncestor(tree)
    assert lca.is_on_path(1, 2, 3) and not lca.is_on_path(0, 2, 3)
    preorder = [1, 2, 4, 5, 3]
    inorder = [4, 2, 5, 1, 3]
    postorder = [4, 5, 2, 3, 1]
    expected_tree = (1, {2: 4, 1: 2}, {2: 5, 1: 3})
    assert reconstruction_module.build_from_preorder_inorder(preorder, inorder) == expected_tree
    assert reconstruction_module.build_from_postorder_inorder(postorder, inorder) == expected_tree
    weighted_path = [[(1, 2)], [(0, 2), (2, 5)], [(1, 5)]]
    assert color_coding_module.color_coding_max_path(weighted_path, 3, 100, 7) == 7

    assert kmp_module.kmp_search('abc', '') == []
    assert manacher_module.longest_palindromic_suffix('abac') == 'c'
    assert manacher_module.longest_palindromic_suffix('abacaba') == 'abacaba'

    circle = geometry.Circle((0, 0), 2)
    assert geometry.circle_relationship(circle, geometry.Circle((0, 0), 2)) == -1
    clockwise = [(0, 0), (0, 2), (2, 2), (2, 0)]
    assert geometry.convex_polygon_contains(clockwise, (1, 1)) == 1
    assert abs(geometry.adaptive_simpson_2d(lambda x, y: x + y, 0, 1, 0, 1) - 1) < 1e-8
    tetrahedron = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    assert abs(geometry3.convex_hull_area(tetrahedron) - (1.5 + math.sqrt(3) / 2.0)) < 1e-8


def main():
    """Run the main operation."""
    random.seed(int(os.environ.get('TEMPLATE_TEST_SEED', '20260809')))
    test_graph()
    test_data_structures()
    test_geometry()
    test_number_theory_and_combinatorics()
    test_strings()
    test_supplemental_graph()
    test_supplemental_data_structures()
    test_supplemental_geometry()
    test_supplemental_math_strings()
    test_added_templates()
    test_plan_regressions()
    expected = set()
    for category in os.listdir(ROOT):
        category_path = os.path.join(ROOT, category)
        if not os.path.isdir(category_path):
            continue
        for filename in os.listdir(category_path):
            if filename.endswith('.py'):
                expected.add(os.path.join(category, filename))
    missing = expected - VERIFIED
    extra = VERIFIED - expected
    assert not missing and not extra, 'verification registry mismatch: missing=%r extra=%r' % (missing, extra)
    print('All %d algorithm templates passed differential/property tests.' % len(VERIFIED))


if __name__ == '__main__':
    main()
