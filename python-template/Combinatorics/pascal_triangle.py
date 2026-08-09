def pascal_triangle(limit, modulus=None):
    """Run the pascal triangle operation."""
    combinations = [[1]]
    for n in range(1, limit + 1):
        row = [1] * (n + 1)
        for k in range(1, n):
            row[k] = combinations[n - 1][k - 1] + combinations[n - 1][k]
            if modulus is not None:
                row[k] %= modulus
        combinations.append(row)
    return combinations
