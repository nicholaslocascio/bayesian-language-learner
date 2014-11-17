def observation_is_in_hypothesis(obs, hyp):
    """
    Returns True if the observation can be
    made from the hypotheses, False otherwise.
    """
    if len(obs) != len(hyp):
        return False

    for i in range(len(obs)):
        if obs[i] != hyp[i] and hyp[i] != '*':
            return False
    return True

def q_from_hypothesis(hypothesis):
    return hypothesis.count('*')