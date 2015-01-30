"""Syntactic Bootstrapping"""

from dist import DDist

def syntactic_probabilities(hypothesis_space, observations, p_c_v_joint, priors):
    """Calculates posterior probabilities for a syntatic hypothesis space given observations using Bayes Theorem"""
    p_c_given_v_dist = DDist.make_conditional_from_joint(p_c_v_joint)
    posteriors_table = {}
    for hypothesis in hypothesis_space:
        posterior = 1
        for oi in observations:
            prob_h = priors.prob(hypothesis)
            prob_x_given_h = p_c_given_v_dist.prob((oi,hypothesis))
            print "(oi, hyp)", (oi, hypothesis)
            prob = prob_h*prob_x_given_h
            posterior *= prob
        posteriors_table[hypothesis] = posterior

    posteriors_table = DDist.normalize_probability_table(posteriors_table)
    posteriors = DDist(posteriors_table)
    return posteriors
