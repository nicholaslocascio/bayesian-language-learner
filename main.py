"""Bayesian Language Learner from Niyogi paper"""

def semantic_bootstrapping_test():
    """Tests the semantic bootstrapping results against those from the paper."""

    hypothesis_space = [\
    '000', '001', '010', '011', '100', '101', '110', '111',\
    '00*', '01*', '10*', '11*', '0*0', '0*1', '1*0', '1*1',\
    '*00', '*01', '*10', '*11', '0**', '*0*', '**0', '1**',\
    '*1*', '**1', '***']

    test_1_obs = ['000']
    test_2_obs = ['000', '000', '000']
    test_3_obs = ['000', '001']
    test_4_obs = ['000', '001', '000']
    test_5_obs = ['000', '001', '000', '001', '000']
    test_6_obs = ['000', '101', '010', '111', '000']

    all_observations = [test_1_obs,test_2_obs,test_3_obs,test_4_obs,test_5_obs,test_6_obs]

    test_num = 1
    for observations in all_observations:
        p_hypotheses_given_data = semantic_bootstrapping_probabilities(hypothesis_space, observations)
        print 'test:',  test_num
        print 'observations:',  observations
        print "posteriors:", p_hypotheses_given_data
        test_num +=1
    return

def observation_in_hypothesis(o, h):
    """Returns True if the observation can be made from the hypotheses, False otherwise."""
    if len(o) != len(h):
        return False

    for i in range(len(o)):
        if o[i] != h[i] and h[i] != '*':
            return False
    return True

def q_from_hypothesis(hypothesis):
    return hypothesis.count('*')

def semantic_bootstrapping_probabilities(hypothesis_space, observations):
    """Calculates posterior probabilities for a hypothesis space given observations using Bayes Theorem"""
    M = len(hypothesis_space[0])+1
    posteriors = {}
    posteriors_sum = 0
    for hypothesis in hypothesis_space:
        q = q_from_hypothesis(hypothesis)
        posterior = 1
        for oi in observations:
            prob_h = 1.0/pow(3.0,M)
            prob_x_given_h = 0.0
            if observation_in_hypothesis(oi,hypothesis):
                prob_x_given_h = 1.0/(pow(2.0,q))
            posterior *= prob_x_given_h*prob_h
        if posterior == 0:
            continue
        posteriors_sum += posterior
        posteriors[hypothesis] = posterior

    # Normalize posteriors to sum to 1
    for key in posteriors.keys():
        posteriors[key] = posteriors[key]/posteriors_sum

    return posteriors

semantic_bootstrapping_test()
