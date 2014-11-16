"""Bayesian Language Learner from Niyogi paper"""

class DDist:
    def __init__(self, dictionary):
        total = sum([dictionary[key] for key in dictionary.keys()])
        if total - 1.0 > 1.0e-10:
            raise Exception('Distributions must sum to 1.0. Total: ' + str(total))
        self.dictionary = dictionary
    def prob(self,elt):
        return self.dictionary.get(elt,0)
    def support(self, dimension = None):
        if dimension != None:
            return list({elt[dimension] for elt in self.dictionary.keys()})
        return self.dictionary.keys()
    def total_probability(self, dimension = None, elt = None):
        if dimension == 0:
            return sum([self.dictionary.get((elt,elt2)) for elt2 in self.support(dimension)])
        else:
            return sum([self.dictionary.get((elt2,elt)) for elt in self.support(dimension)])

    @staticmethod
    def normalize_probability_table(table):
        total = sum([table.get(e, 0) for e in table.keys()])
        return {key : table[key]/total for key in table.keys()}

    def __str__(self):
        return "DDist: " + str(self.dictionary)

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

def makeConditionalFromJoint(joint):
    conditional_table = {}
    p_v_table = {v : sum(joint.prob((c,v)) for c in joint.support(0)) for v in joint.support(1)}
    p_v_dist = DDist(p_v_table)
    total = 0
    for c in joint.support(0):
        for v in joint.support(1):
            prob = joint.prob((c,v))/p_v_dist.prob(v)
            conditional_table[(c,v)] = prob
            total += prob
    conditional_table = DDist.normalize_probability_table(conditional_table)
    return DDist(conditional_table)

def syntatic_bootstrapping_probabilities(hypothesis_space, observations, p_c_v_joint, priors):
    """Calculates posterior probabilities for a syntatic hypothesis space given observations using Bayes Theorem"""
    p_c_given_v_dist = makeConditionalFromJoint(p_c_v_joint)
    posteriors_table = {}
    posteriors_sum = 0
    for hypothesis in hypothesis_space:
        posterior = 1
        for oi in observations:
            prob_h = priors.prob(hypothesis)
            prob_x_given_h = p_c_given_v_dist.prob((oi,hypothesis))
            prob = prob_h*prob_x_given_h
            posterior *= prob
        posteriors_sum += posterior
        posteriors_table[hypothesis] = posterior

    posteriors_table = DDist.normalize_probability_table(posteriors_table)
    posteriors = DDist(posteriors_table)
    return posteriors

def syntatic_bootstrapping_test():
    """Tests the syntatic bootstrapping results against those from the paper."""

    hypothesis_space = ['0', '1', '*']
    p_c_v_table = {\
    ('0','0'): 0.22, ('0','1'): 0.01, ('0','*'): 0.11,\
    ('1','0'): 0.01, ('1','1'): 0.22, ('1','*'): 0.11,\
    ('-','0'): 0.11, ('-','1'): 0.11, ('-','*'): 0.12\
    }
    p_c_v_table = {key : p_c_v_table[key]/1.2 for key in p_c_v_table.keys()} # values from paper don't sum to 1
    p_c_v_dist = DDist(p_c_v_table)
    priors_table = {'0': 1.0/3.0, '1': 1.0/3.0, '*': 1.0/3.0}
    priors_dist = DDist(priors_table)

    test_1_obs = ['0','0','0','0']
    test_2_obs = ['-','-','-','-']
    test_3_obs = ['0','0','1','1']
    test_4_obs = ['-','-','0','0']
    test_5_obs = ['0' for i in range(23)] + ['-' for i in range(10)]
    test_6_obs = ['0' for i in range(23)] + ['-' for i in range(10)] + ['1' for i in range(5)]

    all_observations = [test_1_obs, test_2_obs, test_3_obs, test_4_obs,test_5_obs, test_6_obs]

    test_num = 1
    for observations in all_observations:
        p_hypotheses_given_data = syntatic_bootstrapping_probabilities(hypothesis_space, observations, p_c_v_dist, priors_dist)
        print 'test:', test_num
        print 'observations:', observations
        print "posteriors:", p_hypotheses_given_data
        test_num += 1
    return

syntatic_bootstrapping_test()
