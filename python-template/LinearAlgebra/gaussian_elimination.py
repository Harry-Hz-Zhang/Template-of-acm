def solve_linear_system(matrix, vector, eps=1e-10):
    """Return (status, one_solution, rank): status is 0 none, 1 unique, 2 infinite."""
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    augmented = [list(matrix[i]) + [vector[i]] for i in range(rows)]
    pivot_columns = []
    row = 0
    for column in range(columns):
        pivot = max(range(row, rows), key=lambda i: abs(augmented[i][column]), default=row)
        if row >= rows or abs(augmented[pivot][column]) <= eps:
            continue
        augmented[row], augmented[pivot] = augmented[pivot], augmented[row]
        divisor = augmented[row][column]
        augmented[row] = [value / divisor for value in augmented[row]]
        for i in range(rows):
            if i != row and abs(augmented[i][column]) > eps:
                factor = augmented[i][column]
                augmented[i] = [augmented[i][j] - factor * augmented[row][j] for j in range(columns + 1)]
        pivot_columns.append(column)
        row += 1
        if row == rows:
            break
    for i in range(row, rows):
        if all(abs(augmented[i][j]) <= eps for j in range(columns)) and abs(augmented[i][columns]) > eps:
            return 0, None, row
    solution = [0.0] * columns
    for i, column in enumerate(pivot_columns):
        solution[column] = augmented[i][columns]
    return (1 if row == columns else 2), solution, row


def determinant(matrix, eps=1e-10):
    """Return the floating-point determinant of a square matrix."""
    values = [list(row) for row in matrix]
    n = len(values)
    if any(len(row) != n for row in values):
        raise ValueError('matrix must be square')
    result = 1.0
    for column in range(n):
        pivot = max(range(column, n), key=lambda i: abs(values[i][column]))
        if abs(values[pivot][column]) <= eps:
            return 0.0
        if pivot != column:
            values[column], values[pivot] = values[pivot], values[column]
            result = -result
        result *= values[column][column]
        for row in range(column + 1, n):
            factor = values[row][column] / values[column][column]
            for j in range(column + 1, n):
                values[row][j] -= factor * values[column][j]
    return result


def solve_linear_system_mod(matrix, vector, modulus):
    """Solve a linear system over a prime field and return status, solution, rank."""
    if modulus <= 1 or len(matrix) != len(vector):
        raise ValueError('require a valid modulus and one value per row')
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    if any(len(values) != columns for values in matrix):
        raise ValueError('matrix must be rectangular')
    augmented = [[value % modulus for value in matrix[i]] + [vector[i] % modulus]
                 for i in range(rows)]
    pivot_columns = []
    row = 0
    for column in range(columns):
        pivot = next((index for index in range(row, rows) if augmented[index][column]), None)
        if pivot is None:
            continue
        augmented[row], augmented[pivot] = augmented[pivot], augmented[row]
        inverse = pow(augmented[row][column], modulus - 2, modulus)
        augmented[row] = [value * inverse % modulus for value in augmented[row]]
        for index in range(rows):
            if index != row and augmented[index][column]:
                factor = augmented[index][column]
                augmented[index] = [(augmented[index][j] - factor * augmented[row][j]) % modulus
                                    for j in range(columns + 1)]
        pivot_columns.append(column)
        row += 1
        if row == rows:
            break
    if any(not any(augmented[index][:columns]) and augmented[index][columns]
           for index in range(row, rows)):
        return 0, None, row
    solution = [0] * columns
    for index, column in enumerate(pivot_columns):
        solution[column] = augmented[index][columns]
    return (1 if row == columns else 2), solution, row


def determinant_mod(matrix, modulus):
    """Return a square matrix determinant modulo a prime."""
    values = [[value % modulus for value in row] for row in matrix]
    n = len(values)
    if modulus <= 1 or any(len(row) != n for row in values):
        raise ValueError('require a square matrix and valid modulus')
    result = 1
    for column in range(n):
        pivot = next((row for row in range(column, n) if values[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            values[column], values[pivot] = values[pivot], values[column]
            result = -result
        pivot_value = values[column][column]
        result = result * pivot_value % modulus
        inverse = pow(pivot_value, modulus - 2, modulus)
        for row in range(column + 1, n):
            factor = values[row][column] * inverse % modulus
            for index in range(column + 1, n):
                values[row][index] = (values[row][index] - factor * values[column][index]) % modulus
    return result % modulus


def matrix_inverse_mod(matrix, modulus):
    """Return a square matrix inverse over a prime field."""
    n = len(matrix)
    if modulus <= 1 or any(len(row) != n for row in matrix):
        raise ValueError('require a square matrix and valid modulus')
    augmented = [[value % modulus for value in row] + [int(i == j) for j in range(n)]
                 for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next((row for row in range(column, n) if augmented[row][column]), None)
        if pivot is None:
            raise ValueError('matrix is singular')
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column], modulus - 2, modulus)
        augmented[column] = [value * inverse % modulus for value in augmented[column]]
        for row in range(n):
            if row != column and augmented[row][column]:
                factor = augmented[row][column]
                augmented[row] = [(augmented[row][j] - factor * augmented[column][j]) % modulus
                                  for j in range(2 * n)]
    return [row[n:] for row in augmented]


def solve_xor_system(matrix, vector):
    """Solve a GF(2) linear system and return status, solution, rank."""
    if len(matrix) != len(vector):
        raise ValueError('require one value per matrix row')
    columns = len(matrix[0]) if matrix else 0
    if any(len(row) != columns for row in matrix):
        raise ValueError('matrix must be rectangular')
    rows = [sum((value & 1) << column for column, value in enumerate(values)) |
            ((vector[index] & 1) << columns) for index, values in enumerate(matrix)]
    pivot_columns = []
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(rows)) if rows[index] >> column & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index] >> column & 1:
                rows[index] ^= rows[rank]
        pivot_columns.append(column)
        rank += 1
    coefficient_mask = (1 << columns) - 1
    if any(not row & coefficient_mask and row >> columns & 1 for row in rows):
        return 0, None, rank
    solution = [0] * columns
    for index, column in enumerate(pivot_columns):
        solution[column] = rows[index] >> columns & 1
    return (1 if rank == columns else 2), solution, rank


def spanning_tree_count(n, edges, modulus):
    """Count spanning trees of an undirected multigraph modulo a prime."""
    if n < 0:
        raise ValueError('vertex count must be nonnegative')
    if n <= 1:
        return 1
    laplacian = [[0] * n for _ in range(n)]
    for u, v in edges:
        if not 0 <= u < n or not 0 <= v < n:
            raise IndexError('vertex is out of range')
        if u == v:
            continue
        laplacian[u][u] += 1
        laplacian[v][v] += 1
        laplacian[u][v] -= 1
        laplacian[v][u] -= 1
    return determinant_mod([row[:-1] for row in laplacian[:-1]], modulus)
