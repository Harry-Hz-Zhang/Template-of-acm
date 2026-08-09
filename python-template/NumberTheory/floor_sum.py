def floor_sum(n, modulus, multiplier, offset):
    """Return sum(floor((multiplier*i + offset) / modulus), i=0..n-1)."""
    if n < 0 or modulus <= 0:
        raise ValueError('n must be nonnegative and modulus positive')
    answer = 0
    if multiplier < 0:
        quotient, multiplier = divmod(multiplier, modulus)
        answer += (n - 1) * n // 2 * quotient
    if offset < 0:
        quotient, offset = divmod(offset, modulus)
        answer += n * quotient
    while True:
        if multiplier >= modulus:
            answer += (n - 1) * n * (multiplier // modulus) // 2
            multiplier %= modulus
        if offset >= modulus:
            answer += n * (offset // modulus)
            offset %= modulus
        maximum = multiplier * n + offset
        if maximum < modulus:
            return answer
        n = maximum // modulus
        offset = maximum % modulus
        modulus, multiplier = multiplier, modulus
