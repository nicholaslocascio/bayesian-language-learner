"""Integrated Bootstrapping"""

from dist import DDist
import numpy as np

def p_s_k_given_h_func(d_k, s_k, h_k, eps=0.1, delta=0.01):
    d_k = 1 # Results from paper seem to ignore differing d_k values, so set d_k = 1 here
    if s_k == '0' and h_k == '*':
        return 1 - d_k*eps
    elif s_k != '0' and h_k == '*':
        return eps
    elif s_k == h_k and h_k != '*':
        return 1 - d_k*delta
    elif s_k != h_k and h_k != '*':
        return delta
    else:
        raise Exception('Invalid h and s space.')

def multiply(lis):
    prod = 1.0
    for el in lis:
        prod *= el
    return prod

def average(lis):
    return sum(lis)/float(len(lis))

def get_attention_from_u_j(u_j):
    if u_j[0] == '0':
        return 'G'
    elif u_j[0] == '1':
        return 'W'
    else:
        return '-'

def compute_p_s_given_h(hypothesis_features, s_j):
    return multiply([p_s_k_given_h_func(k, s_j[k], hypothesis_features[k]) for k in range(1,len(s_j))])

def integrated_probabilities(hypothesis_space, observations, priors_table):
    """Calculates posterior probabilities for a syntatic hypothesis space given observations using Bayes Theorem"""
    posteriors_table = {}
    p_c_v_joint_table = {\
    ('0','0'): 0.22, ('0','1'): 0.01, ('0','*'): 0.11,\
    ('1','0'): 0.01, ('1','1'): 0.22, ('1','*'): 0.11,\
    ('*','0'): 0.11, ('*','1'): 0.11, ('*','*'): 0.12\
    }
    p_u_given_h_dist = DDist.make_conditional_from_joint(DDist(DDist.normalize_probability_table(p_c_v_joint_table)))
    for hypothesis_key in hypothesis_space.keys():
        posterior = 1
        hypothesis_features = hypothesis_space[hypothesis_key]
        for oi in observations:
            s_j = oi.get("s", None)
            u_j = oi.get("u")
            a_j = get_attention_from_u_j(u_j)
            hypothesis_fig = hypothesis_features[0]
            p_u_given_h = multiply([p_u_given_h_dist.prob((hypothesis_fig, u_j[k])) for k in range(len(u_j))])
            p_s_given_h = 1.0
            if s_j != None:
                if a_j == '-':
                    attentions = ["G", "W"]
                    p_s_given_h = average([compute_p_s_given_h(hypothesis_features, s_j[a]) for a in attentions])
                else:
                    p_s_given_h = compute_p_s_given_h(hypothesis_features, s_j[a_j])
            else:
                p_s_given_h = 1.0/3.0
            prob = p_u_given_h*p_s_given_h*priors_table[hypothesis_key]
            posterior *= prob
        posteriors_table[hypothesis_key] = posterior

    posteriors_table = DDist.normalize_probability_table(posteriors_table)
    posteriors = DDist(posteriors_table)
    return posteriors