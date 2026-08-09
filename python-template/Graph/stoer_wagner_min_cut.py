def stoer_wagner_min_cut(matrix):
    """Undirected nonnegative adjacency matrix: return (cut_weight, one_side_vertices)."""
    n = len(matrix)
    if n < 2:
        return 0, list(range(n))
    weights_matrix = [row[:] for row in matrix]
    vertices = list(range(n))
    groups = [[u] for u in range(n)]
    best_weight = float('inf')
    best_cut = []
    while len(vertices) > 1:
        added = [False] * n
        connection = [0] * n
        previous = -1
        for phase_index in range(len(vertices)):
            selected = max((u for u in vertices if not added[u]), key=connection.__getitem__)
            if phase_index == len(vertices) - 1:
                if connection[selected] < best_weight:
                    best_weight = connection[selected]
                    best_cut = groups[selected][:]
                groups[previous].extend(groups[selected])
                for u in vertices:
                    if u not in (previous, selected):
                        weights_matrix[previous][u] += weights_matrix[selected][u]
                        weights_matrix[u][previous] = weights_matrix[previous][u]
                vertices.remove(selected)
            else:
                added[selected] = True
                previous = selected
                for u in vertices:
                    if not added[u]:
                        connection[u] += weights_matrix[selected][u]
    return best_weight, best_cut
