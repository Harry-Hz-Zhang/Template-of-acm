def _factor_prime_powers(modulus):
    """Run the internal factor prime powers step."""
    factors = []
    prime = 2
    while prime * prime <= modulus:
        if modulus % prime == 0:
            power = 1
            while modulus % prime == 0:
                modulus //= prime
                power *= prime
            factors.append((prime, power))
        prime = 3 if prime == 2 else prime + 2
    if modulus > 1:
        factors.append((modulus, modulus))
    return factors


def _exponent_in_factorial(n, prime):
    """Run the internal exponent in factorial step."""
    exponent = 0
    while n:
        n //= prime
        exponent += n
    return exponent


def _modular_inverse(value, modulus):
    """Run the internal modular inverse step."""
    old_r, r = value, modulus
    old_x, x = 1, 0
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
    if old_r != 1:
        raise ValueError('inverse does not exist')
    return old_x % modulus


def _combination_mod_prime_power(n, k, prime, prime_power):
    """Run the internal combination mod prime power step."""
    if k < 0 or k > n:
        return 0
    prefix = [1] * prime_power
    for value in range(1, prime_power):
        prefix[value] = prefix[value - 1]
        if value % prime:
            prefix[value] = prefix[value] * value % prime_power
    block_product = prefix[-1]

    def factorial_without_prime(value):
        """Run the factorial without prime operation."""
        if value == 0:
            return 1
        result = pow(block_product, value // prime_power, prime_power)
        result = result * prefix[value % prime_power] % prime_power
        return result * factorial_without_prime(value // prime) % prime_power

    exponent = (_exponent_in_factorial(n, prime)
                - _exponent_in_factorial(k, prime)
                - _exponent_in_factorial(n - k, prime))
    prime_power_exponent = 0
    current = prime_power
    while current % prime == 0:
        prime_power_exponent += 1
        current //= prime
    if exponent >= prime_power_exponent:
        return 0
    numerator = factorial_without_prime(n)
    denominator = factorial_without_prime(k) * factorial_without_prime(n - k) % prime_power
    return (numerator * _modular_inverse(denominator, prime_power) % prime_power
            * pow(prime, exponent, prime_power) % prime_power)


def binomial_mod(n, k, modulus):
    """Compute C(n, k) modulo any positive modulus."""
    if modulus <= 0:
        raise ValueError('modulus must be positive')
    if modulus == 1 or k < 0 or k > n:
        return 0
    remainder = 0
    combined_modulus = 1
    for prime, prime_power in _factor_prime_powers(modulus):
        next_remainder = _combination_mod_prime_power(n, k, prime, prime_power)
        inverse = _modular_inverse(combined_modulus, prime_power)
        multiplier = (next_remainder - remainder) * inverse % prime_power
        remainder += combined_modulus * multiplier
        combined_modulus *= prime_power
        remainder %= combined_modulus
    return remainder
