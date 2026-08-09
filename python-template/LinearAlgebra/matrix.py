def matrix_multiply(a, b, modulus=None):
    """Multiply compatible dense matrices with an optional modulus."""
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('incompatible matrix dimensions')
    result = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i][k] == 0:
                continue
            for j in range(len(b[0])):
                result[i][j] += a[i][k] * b[k][j]
                if modulus is not None:
                    result[i][j] %= modulus
    return result


def matrix_power(matrix, exponent, modulus=None):
    """Raise a square matrix to a nonnegative integer power."""
    if exponent < 0 or any(len(row) != len(matrix) for row in matrix):
        raise ValueError('require a square matrix and nonnegative exponent')
    result = [[int(i == j) for j in range(len(matrix))] for i in range(len(matrix))]
    base = [row[:] for row in matrix]
    while exponent:
        if exponent & 1:
            result = matrix_multiply(result, base, modulus)
        base = matrix_multiply(base, base, modulus)
        exponent >>= 1
    return result


def matrix_add(a, b, modulus=None):
    """Add equally shaped matrices with an optional modulus."""
    if len(a) != len(b) or any(len(left) != len(right) for left, right in zip(a, b)):
        raise ValueError('matrix dimensions must match')
    result = [[left + right for left, right in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]
    return result if modulus is None else [[value % modulus for value in row] for row in result]


def matrix_subtract(a, b, modulus=None):
    """Subtract equally shaped matrices with an optional modulus."""
    if len(a) != len(b) or any(len(left) != len(right) for left, right in zip(a, b)):
        raise ValueError('matrix dimensions must match')
    result = [[left - right for left, right in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]
    return result if modulus is None else [[value % modulus for value in row] for row in result]
