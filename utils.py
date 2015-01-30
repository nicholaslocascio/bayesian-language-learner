from math import fabs

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

def approx_equal(value1, value2, threshold=1.0e-6):
    """returns true if two values are approximately correct"""
    return fabs(value1-value2) < threshold
    
def compare_probabilitiy_tables(results, paper_results):
    """returns true if probability tables are approximately correct"""
    for key in paper_results.keys():
        paper_result = paper_results.get(key,0.0)
        result = results.get(key,0.0)
        if not approx_equal(result, paper_result, 0.05):
            return False
    return True