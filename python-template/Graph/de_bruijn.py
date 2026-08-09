def de_bruijn_sequence(order, alphabet_size):
    """Return a linearized de Bruijn sequence as integer symbols."""
    if order < 1 or alphabet_size < 1:
        raise ValueError('order and alphabet_size must be positive')
    a = [0] * (order * alphabet_size + 1)
    cycle = []

    def generate(t, period):
        """Run the generate operation."""
        if t > order:
            if order % period == 0:
                cycle.extend(a[1:period + 1])
            return
        a[t] = a[t - period]
        generate(t + 1, period)
        for symbol in range(a[t - period] + 1, alphabet_size):
            a[t] = symbol
            generate(t + 1, t)

    generate(1, 1)
    return cycle + [cycle[i % len(cycle)] for i in range(order - 1)]
