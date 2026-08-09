def small_combination_mod_prime(n, k, prime):
    """Run the small combination mod prime operation."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for value in range(1, k + 1):
        numerator = numerator * (n - value + 1) % prime
        denominator = denominator * value % prime
    return numerator * pow(denominator, prime - 2, prime) % prime


def lucas(n, k, prime):
    """Run the lucas operation."""
    result = 1
    while n or k:
        n_digit, k_digit = n % prime, k % prime
        if k_digit > n_digit:
            return 0
        result = result * small_combination_mod_prime(n_digit, k_digit, prime) % prime
        n //= prime
        k //= prime
    return result
