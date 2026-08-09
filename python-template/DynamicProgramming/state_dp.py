from functools import lru_cache


def digit_dp_count(limit, transition, accept, base=10, initial_state=0):
    """Count integers in [0, limit] with a user-defined digit automaton."""
    if limit < 0:
        return 0
    if base < 2:
        raise ValueError('base must be at least two')
    digits = []
    value = limit
    while value:
        digits.append(value % base)
        value //= base
    digits = digits[::-1] or [0]

    @lru_cache(None)
    def solve(position, state, tight, started):
        """Count valid suffixes of the current digit-DP state."""
        if position == len(digits):
            return int(accept(state, started))
        result = 0
        upper = digits[position] if tight else base - 1
        for digit in range(upper + 1):
            next_state = transition(state, digit, started)
            if next_state is not None:
                result += solve(position + 1, next_state, tight and digit == upper, started or digit != 0)
        return result

    return solve(0, initial_state, True, False)


def count_numbers_with_digit_sum(limit, target, base=10):
    """Count integers in [0, limit] with the requested digit sum."""
    return digit_dp_count(limit, lambda state, digit, started: state + digit
                          if state + digit <= target else None,
                          lambda state, started: state == target, base)


def count_accepted_strings(length, transitions, initial_state, accepting, modulus=None):
    """Count fixed-length strings accepted by a finite automaton."""
    if length < 0:
        raise ValueError('length must be nonnegative')
    dp = {initial_state: 1}
    for _ in range(length):
        next_dp = {}
        for state, count in dp.items():
            for next_state in transitions[state]:
                next_dp[next_state] = next_dp.get(next_state, 0) + count
                if modulus is not None:
                    next_dp[next_state] %= modulus
        dp = next_dp
    result = sum(dp.get(state, 0) for state in accepting)
    return result % modulus if modulus is not None else result


def subset_sums(values):
    """Apply the SOS zeta transform over all submasks."""
    result = list(values)
    if len(result) == 0 or len(result) & (len(result) - 1):
        raise ValueError('length must be a positive power of two')
    bits = (len(result) - 1).bit_length()
    for bit in range(bits):
        for mask in range(len(result)):
            if mask >> bit & 1:
                result[mask] += result[mask ^ (1 << bit)]
    return result


def superset_sums(values):
    """Apply the SOS zeta transform over all supermasks."""
    result = list(values)
    if len(result) == 0 or len(result) & (len(result) - 1):
        raise ValueError('length must be a positive power of two')
    bits = (len(result) - 1).bit_length()
    for bit in range(bits):
        for mask in range(len(result)):
            if not mask >> bit & 1:
                result[mask] += result[mask | (1 << bit)]
    return result
