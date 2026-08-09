def hungarian(cost):
    """Minimum-cost assignment for rows <= columns; return (cost, assigned_column_per_row)."""
    rows = len(cost)
    columns = len(cost[0]) if rows else 0
    if rows > columns or any(len(row) != columns for row in cost):
        raise ValueError('cost must be rectangular with rows <= columns')
    u = [0] * (rows + 1)
    v = [0] * (columns + 1)
    match = [0] * (columns + 1)
    path = [0] * (columns + 1)
    for row in range(1, rows + 1):
        match[0] = row
        column = 0
        minimum = [float('inf')] * (columns + 1)
        used = [False] * (columns + 1)
        while True:
            used[column] = True
            current_row = match[column]
            delta = float('inf')
            next_column = 0
            for candidate in range(1, columns + 1):
                if used[candidate]:
                    continue
                reduced = cost[current_row - 1][candidate - 1] - u[current_row] - v[candidate]
                if reduced < minimum[candidate]:
                    minimum[candidate] = reduced
                    path[candidate] = column
                if minimum[candidate] < delta:
                    delta = minimum[candidate]
                    next_column = candidate
            for candidate in range(columns + 1):
                if used[candidate]:
                    u[match[candidate]] += delta
                    v[candidate] -= delta
                else:
                    minimum[candidate] -= delta
            column = next_column
            if match[column] == 0:
                break
        while column:
            previous = path[column]
            match[column] = match[previous]
            column = previous
    assignment = [-1] * rows
    for column in range(1, columns + 1):
        if match[column]:
            assignment[match[column] - 1] = column - 1
    return -v[0], assignment
