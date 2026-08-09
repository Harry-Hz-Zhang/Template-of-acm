MODULUS = 998244353
PRIMITIVE_ROOT = 3


def ntt(values, invert=False, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Transform one power-of-two coefficient array in place."""
    n = len(values)
    if n == 0 or n & (n - 1):
        raise ValueError('length must be a positive power of two')
    if modulus <= 1 or (modulus - 1) % n:
        raise ValueError('transform length is unsupported by the modulus')
    for i in range(n):
        values[i] %= modulus
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            values[i], values[j] = values[j], values[i]
    length = 2
    while length <= n:
        root = pow(primitive_root, (modulus - 1) // length, modulus)
        if invert:
            root = pow(root, modulus - 2, modulus)
        for start in range(0, n, length):
            factor = 1
            half = length // 2
            for i in range(start, start + half):
                even = values[i]
                odd = values[i + half] * factor % modulus
                values[i] = (even + odd) % modulus
                values[i + half] = (even - odd) % modulus
                factor = factor * root % modulus
        length <<= 1
    if invert:
        inverse_n = pow(n, modulus - 2, modulus)
        for i in range(n):
            values[i] = values[i] * inverse_n % modulus
    return values


def convolution(a, b, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Multiply coefficient arrays with an NTT-friendly prime modulus."""
    if not a or not b:
        return []
    size = 1
    result_size = len(a) + len(b) - 1
    while size < result_size:
        size <<= 1
    left = list(a) + [0] * (size - len(a))
    right = list(b) + [0] * (size - len(b))
    ntt(left, modulus=modulus, primitive_root=primitive_root)
    ntt(right, modulus=modulus, primitive_root=primitive_root)
    for i in range(size):
        left[i] = left[i] * right[i] % modulus
    ntt(left, True, modulus, primitive_root)
    return left[:result_size]


def _resize(values, size, modulus=MODULUS):
    """Truncate or zero-pad a coefficient list to an exact size."""
    return [value % modulus for value in values[:size]] + [0] * max(0, size - len(values))


def poly_trim(polynomial, modulus=MODULUS):
    """Normalize coefficients and remove trailing zero terms."""
    result = [value % modulus for value in polynomial]
    while result and result[-1] == 0:
        result.pop()
    return result


def poly_add(a, b, modulus=MODULUS):
    """Add two polynomials and trim trailing zeros."""
    size = max(len(a), len(b))
    return poly_trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                      for i in range(size)], modulus)


def poly_subtract(a, b, modulus=MODULUS):
    """Subtract two polynomials and trim trailing zeros."""
    size = max(len(a), len(b))
    return poly_trim([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
                      for i in range(size)], modulus)


def poly_scalar_multiply(polynomial, scalar, modulus=MODULUS):
    """Multiply every coefficient by one scalar."""
    return poly_trim([value * scalar for value in polynomial], modulus)


def poly_multiply(a, b, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Multiply and trim two polynomials."""
    return poly_trim(convolution(a, b, modulus, primitive_root), modulus)


def poly_divmod(dividend, divisor, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return polynomial quotient and remainder over a prime field."""
    dividend, divisor = poly_trim(dividend, modulus), poly_trim(divisor, modulus)
    if not divisor:
        raise ZeroDivisionError('polynomial division by zero')
    if len(dividend) < len(divisor):
        return [], dividend
    quotient_size = len(dividend) - len(divisor) + 1
    reversed_dividend = list(reversed(dividend[-quotient_size:]))
    reversed_divisor = list(reversed(divisor))
    quotient = convolution(reversed_dividend,
                           poly_inverse(reversed_divisor, quotient_size, modulus, primitive_root),
                           modulus, primitive_root)[:quotient_size]
    quotient.reverse()
    remainder = poly_subtract(dividend, convolution(divisor, quotient, modulus, primitive_root), modulus)
    return poly_trim(quotient, modulus), poly_trim(remainder[:len(divisor) - 1], modulus)


def poly_derivative(polynomial, modulus=MODULUS):
    """Return the formal derivative of a polynomial."""
    return poly_trim([index * polynomial[index] for index in range(1, len(polynomial))], modulus)


def poly_integral(polynomial, modulus=MODULUS):
    """Return the formal integral with zero constant term."""
    if len(polynomial) >= modulus:
        raise ValueError('coefficient index must stay below the modulus')
    return [0] + [value * pow(index, modulus - 2, modulus) % modulus
                  for index, value in enumerate(polynomial, 1)]


def poly_inverse(polynomial, size, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return the formal inverse modulo x**size."""
    if size < 0:
        raise ValueError('size must be nonnegative')
    if size == 0:
        return []
    if not polynomial or polynomial[0] % modulus == 0:
        raise ValueError('constant coefficient must be invertible')
    result = [pow(polynomial[0] % modulus, modulus - 2, modulus)]
    while len(result) < size:
        length = min(size, 2 * len(result))
        product = _resize(convolution(polynomial[:length], result, modulus, primitive_root), length, modulus)
        correction = [(-value) % modulus for value in product]
        correction[0] = (correction[0] + 2) % modulus
        result = _resize(convolution(result, correction, modulus, primitive_root), length, modulus)
    return result


def poly_log(polynomial, size, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return the formal logarithm modulo x**size."""
    if size < 0 or not polynomial or polynomial[0] % modulus != 1:
        raise ValueError('require nonnegative size and constant coefficient one')
    product = convolution(poly_derivative(polynomial, modulus),
                          poly_inverse(polynomial, size, modulus, primitive_root),
                          modulus, primitive_root)
    return _resize(poly_integral(product[:max(0, size - 1)], modulus), size, modulus)


def poly_exp(polynomial, size, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return the formal exponential modulo x**size."""
    if size < 0 or (polynomial and polynomial[0] % modulus):
        raise ValueError('require nonnegative size and zero constant coefficient')
    if size == 0:
        return []
    result = [1]
    while len(result) < size:
        length = min(size, 2 * len(result))
        logarithm = poly_log(result, length, modulus, primitive_root)
        correction = [((polynomial[i] if i < len(polynomial) else 0) - logarithm[i]) % modulus
                      for i in range(length)]
        correction[0] = (correction[0] + 1) % modulus
        result = _resize(convolution(result, correction, modulus, primitive_root), length, modulus)
    return result


def poly_power(polynomial, exponent, size=None, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Raise a polynomial to a nonnegative power with optional truncation."""
    if exponent < 0:
        raise ValueError('exponent must be nonnegative')
    polynomial = poly_trim(polynomial, modulus)
    if size is None:
        size = 1 if exponent == 0 else ((len(polynomial) - 1) * exponent + 1 if polynomial else 0)
    if size < 0:
        raise ValueError('size must be nonnegative')
    if exponent == 0:
        return _resize([1], size, modulus)
    if not polynomial or size == 0:
        return [0] * size
    leading = next(index for index, value in enumerate(polynomial) if value)
    shift = leading * exponent
    if shift >= size:
        return [0] * size
    coefficient = polynomial[leading]
    inverse = pow(coefficient, modulus - 2, modulus)
    normalized = [value * inverse % modulus for value in polynomial[leading:]]
    length = size - shift
    logarithm = poly_log(normalized, length, modulus, primitive_root)
    powered = poly_exp([value * exponent % modulus for value in logarithm],
                       length, modulus, primitive_root)
    scale = pow(coefficient, exponent, modulus)
    return [0] * shift + [value * scale % modulus for value in powered]


def _modular_sqrt(value, modulus):
    """Return one square root modulo an odd prime, or None."""
    value %= modulus
    if value in (0, 1) or modulus == 2:
        return value
    if pow(value, (modulus - 1) // 2, modulus) != 1:
        return None
    if modulus % 4 == 3:
        return pow(value, (modulus + 1) // 4, modulus)
    odd, power = modulus - 1, 0
    while odd % 2 == 0:
        odd //= 2
        power += 1
    non_residue = 2
    while pow(non_residue, (modulus - 1) // 2, modulus) != modulus - 1:
        non_residue += 1
    current = pow(non_residue, odd, modulus)
    root = pow(value, (odd + 1) // 2, modulus)
    remainder = pow(value, odd, modulus)
    order = power
    while remainder != 1:
        index, squared = 0, remainder
        while squared != 1:
            squared = squared * squared % modulus
            index += 1
        factor = pow(current, 1 << (order - index - 1), modulus)
        root = root * factor % modulus
        current = factor * factor % modulus
        remainder = remainder * current % modulus
        order = index
    return root


def poly_sqrt(polynomial, size=None, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return one formal square root or raise when none exists."""
    polynomial = poly_trim(polynomial, modulus)
    if size is None:
        size = len(polynomial)
    if size < 0:
        raise ValueError('size must be nonnegative')
    if not polynomial:
        return [0] * size
    leading = next(index for index, value in enumerate(polynomial) if value)
    if leading & 1:
        raise ValueError('leading zero count must be even')
    shift = leading // 2
    if shift >= size:
        return [0] * size
    target = polynomial[leading:]
    root = _modular_sqrt(target[0], modulus)
    if root is None:
        raise ValueError('constant coefficient is not a quadratic residue')
    length_limit = size - shift
    result = [root]
    inverse_two = (modulus + 1) // 2
    while len(result) < length_limit:
        length = min(length_limit, 2 * len(result))
        quotient = convolution(target[:length],
                               poly_inverse(result, length, modulus, primitive_root),
                               modulus, primitive_root)
        quotient = _resize(quotient, length, modulus)
        result = [((result[i] if i < len(result) else 0) + quotient[i]) * inverse_two % modulus
                  for i in range(length)]
    return [0] * shift + result


def poly_mul_transpose(a, b, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Multiply by a reversed polynomial and discard its initial shift."""
    if not b:
        return []
    return convolution(a, list(reversed(b)), modulus, primitive_root)[len(b) - 1:]


def poly_evaluate(polynomial, point, modulus=MODULUS):
    """Evaluate a coefficient list with Horner's rule."""
    result = 0
    for coefficient in reversed(polynomial):
        result = (result * point + coefficient) % modulus
    return result


def multipoint_evaluate(polynomial, points, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Evaluate a polynomial at many points using a product tree."""
    points = [point % modulus for point in points]
    if not points:
        return []
    products = [None] * (4 * len(points))

    def build(node, left, right):
        """Build products of (x - point) for one point interval."""
        if right - left == 1:
            products[node] = [(-points[left]) % modulus, 1]
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        products[node] = poly_multiply(products[node * 2], products[node * 2 + 1],
                                       modulus, primitive_root)

    answers = [0] * len(points)

    def solve(node, left, right, remainder):
        """Propagate polynomial remainders down the product tree."""
        if right - left == 1:
            answers[left] = remainder[0] if remainder else 0
            return
        middle = (left + right) // 2
        left_remainder = poly_divmod(remainder, products[node * 2], modulus, primitive_root)[1]
        right_remainder = poly_divmod(remainder, products[node * 2 + 1], modulus, primitive_root)[1]
        solve(node * 2, left, middle, left_remainder)
        solve(node * 2 + 1, middle, right, right_remainder)

    build(1, 0, len(points))
    root_remainder = poly_divmod(polynomial, products[1], modulus, primitive_root)[1]
    solve(1, 0, len(points), root_remainder)
    return answers


def lagrange_interpolate(points, values, modulus=MODULUS, primitive_root=PRIMITIVE_ROOT):
    """Return coefficients of the polynomial through distinct field points."""
    if len(points) != len(values):
        raise ValueError('point and value counts must match')
    points = [point % modulus for point in points]
    if len(set(points)) != len(points):
        raise ValueError('interpolation points must be distinct')
    product = [1]
    for point in points:
        product = poly_multiply(product, [(-point) % modulus, 1], modulus, primitive_root)
    derivative = poly_derivative(product, modulus)
    result = []
    for point, value in zip(points, values):
        basis = poly_divmod(product, [(-point) % modulus, 1], modulus, primitive_root)[0]
        denominator = poly_evaluate(derivative, point, modulus)
        if denominator == 0:
            raise ValueError('interpolation denominator is not invertible')
        scale = value * pow(denominator, modulus - 2, modulus) % modulus
        result = poly_add(result, poly_scalar_multiply(basis, scale, modulus), modulus)
    return result


def cyclic_convolution(a, b, length, modulus=MODULUS):
    """Multiply coefficient lists modulo x**length - 1."""
    if length <= 0:
        raise ValueError('length must be positive')
    result = [0] * length
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            result[(i + j) % length] = (result[(i + j) % length] + left * right) % modulus
    return result


def cyclic_power(polynomial, exponent, length, modulus=MODULUS):
    """Raise a cyclic polynomial to a nonnegative integer power."""
    if exponent < 0 or length <= 0:
        raise ValueError('require a nonnegative exponent and positive length')
    result = [0] * length
    result[0] = 1
    base = _resize(polynomial, length, modulus)
    while exponent:
        if exponent & 1:
            result = cyclic_convolution(result, base, length, modulus)
        base = cyclic_convolution(base, base, length, modulus)
        exponent >>= 1
    return result


def subset_sum_residue_counts(n, residue_modulus, modulus=MODULUS):
    """Count subsets of 1..n by sum residue modulo residue_modulus."""
    if n < 0 or residue_modulus <= 0:
        raise ValueError('require nonnegative n and positive residue modulus')
    period = [1] + [0] * (residue_modulus - 1)
    for residue in range(residue_modulus):
        factor = [0] * residue_modulus
        factor[0] = 1
        factor[residue] += 1
        period = cyclic_convolution(period, factor, residue_modulus, modulus)
    result = cyclic_power(period, n // residue_modulus, residue_modulus, modulus)
    for residue in range(1, n % residue_modulus + 1):
        factor = [0] * residue_modulus
        factor[0] = factor[residue] = 1
        result = cyclic_convolution(result, factor, residue_modulus, modulus)
    return result
