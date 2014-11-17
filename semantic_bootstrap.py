"""Semantic Bootstrapping"""

from dist import DDist
from utils import q_from_hypothesis, observation_is_in_hypothesis

def semantic_probabilities(hypothesis_space, observations):
    """Returns a DDist of posterior probabilities for a hypothesis space given observations using Bayes Theorem"""
    M = len(hypothesis_space[0])+1
    posteriors = {}
    for hypothesis in hypothesis_space:
        q = q_from_hypothesis(hypothesis)
        posterior = 1
        for obs in observations:
            prob_h = 1.0/pow(3.0, M)
            prob_x_given_h = 0.0
            if observation_is_in_hypothesis(obs, hypothesis):
                prob_x_given_h = 1.0/(pow(2.0, q))
            posterior *= prob_x_given_h*prob_h
        if posterior == 0:
            continue
        posteriors[hypothesis] = posterior

    # Normalize posteriors to sum to 1
    posteriors = DDist.normalize_probability_table(posteriors)
    posteriors = DDist(posteriors)
    return posteriors
