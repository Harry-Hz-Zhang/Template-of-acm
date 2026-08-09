def expected_value(outcomes):
    """Return sum(probability * value) for finite outcomes."""
    return sum(probability * value for probability, value in outcomes)


def geometric_expected_trials(success_probability):
    """Return expected trials until the first Bernoulli success."""
    if not 0 < success_probability <= 1:
        raise ValueError('success probability must be in (0, 1]')
    return 1.0 / success_probability


def geometric_expected_failures(success_probability):
    """Return expected failures before the first Bernoulli success."""
    return geometric_expected_trials(success_probability) - 1.0


def geometric_probability(trial, success_probability):
    """Return the probability that the first success occurs on trial."""
    if trial <= 0 or not 0 < success_probability <= 1:
        raise ValueError('require a positive trial and probability in (0, 1]')
    return (1.0 - success_probability) ** (trial - 1) * success_probability
