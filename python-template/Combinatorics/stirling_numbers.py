def stirling_second_kind(n, k, modulus=None):
    """Run the stirling second kind operation."""
    dp = [0] * (k + 1)
    dp[0] = 1
    for size in range(1, n + 1):
        for groups in range(min(size, k), 0, -1):
            dp[groups] = dp[groups - 1] + groups * dp[groups]
            if modulus is not None:
                dp[groups] %= modulus
        dp[0] = 0
    return dp[k]


def stirling_first_kind_unsigned(n, k, modulus=None):
    """Run the stirling first kind unsigned operation."""
    dp = [0] * (k + 1)
    dp[0] = 1
    for size in range(1, n + 1):
        for cycles in range(min(size, k), 0, -1):
            dp[cycles] = dp[cycles - 1] + (size - 1) * dp[cycles]
            if modulus is not None:
                dp[cycles] %= modulus
        dp[0] = 0
    return dp[k]
