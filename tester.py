from syntactic_bootstrap import syntactic_probabilities
from semantic_bootstrap import semantic_probabilities
from dist import DDist
from math import fabs
""" Tests semantic and syntactic probabilities against those from the Niyogi paper. """

def approx_equal(value1, value2, threshold=1.0e-6):
    """returns true if two values are approximately correct"""
    return fabs(value1-value2) < threshold
def compare_probabilitiy_tables(results, paper_results):
    """returns true if probability tables are approximately correct"""
    for key in paper_results.keys():
        paper_result = paper_results.get(key,0.0)
        result = results.get(key,0.0)
        if not approx_equal(result, paper_result, 1.0e-2):
            return False
    return True

def semantic_bootstrapping_test(verbose=False):
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

    all_observations = [test_1_obs, test_2_obs, test_3_obs, test_4_obs, test_5_obs, test_6_obs]

    paper_res_1 = {'000' : 0.30, '00*' : 0.15, '0**' : 0.07, '***' : .03}
    paper_res_2 = {'000' : 0.70, '00*' : 0.09, '0**' : 0.01, '***' : .001}
    paper_res_3 = {'000' : 0.00, '00*' : 0.64, '0**' : 0.16, '***' : .04}
    paper_res_4 = {'000' : 0.00, '00*' : 0.79, '0**' : 0.10, '***' : .01}
    paper_res_5 = {'000' : 0.00, '00*' : 0.94, '0**' : 0.03, '***' : .001}
    paper_res_6 = {'000' : 0.00, '00*' : 0.00, '0**' : 0.00, '***' : 1.0}

    all_paper_results = [paper_res_1, paper_res_2, paper_res_3, paper_res_4, paper_res_5, paper_res_6]
    passed_tests_count = 0
    test_num = 1
    num_tests = len(all_paper_results)

    print "Testing the semantic bootstrapping results against those from the paper."
    for i in range(len(all_observations)):
        observations = all_observations[i]
        paper_results = all_paper_results[i]
        p_hypotheses_given_data = semantic_probabilities(hypothesis_space, observations)
        p_hypotheses_given_data_table = p_hypotheses_given_data.dictionary
        if not compare_probabilitiy_tables(p_hypotheses_given_data_table, all_paper_results[test_num-1]):
            print "Failed test:", test_num
            print str(paper_results), "does not equal", str(p_hypotheses_given_data_table)
        else:
            passed_tests_count += 1
            if verbose:
                print 'Passed test:',  test_num
                print 'observations:',  observations
                print "posteriors:", p_hypotheses_given_data
        test_num +=1

    if passed_tests_count == num_tests:
        print "Passed all", num_tests, "tests"
    else:
        print "Passed (", passed_tests_count, '/', num_tests, ") tests"
    return


def syntactic_bootstrapping_test(verbose=False):
    """Tests the syntatic bootstrapping results against those from the paper."""

    hypothesis_space = ['0', '1', '*']
    p_c_v_table = {\
    ('0','0'): 0.22, ('0','1'): 0.01, ('0','*'): 0.11,\
    ('1','0'): 0.01, ('1','1'): 0.22, ('1','*'): 0.11,\
    ('-','0'): 0.11, ('-','1'): 0.11, ('-','*'): 0.12\
    }
    p_c_v_table = DDist.normalize_probability_table(p_c_v_table) # values from paper don't sum to 1
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


    paper_res_1 = {'0' : 0.941, '1' : 0.000, '*' : 0.059}
    paper_res_2 = {'0' : 0.292, '1' : 0.292, '*' : 0.416}
    paper_res_3 = {'0' : 0.032, '1' : 0.032, '*' : 0.936}
    paper_res_4 = {'0' : 0.769, '1' : 0.000, '*' : 0.230}
    paper_res_5 = {'0' : 1.000, '1' : 0.000, '*' : 0.000}
    paper_res_6 = {'0' : 0.960, '1' : 0.000, '*' : 0.040}

    all_paper_results = [paper_res_1, paper_res_2, paper_res_3, paper_res_4, paper_res_5, paper_res_6]
    passed_tests_count = 0
    test_num = 1
    num_tests = len(all_paper_results)

    print "Testing the syntatic bootstrapping results against those from the paper."
    for i in range(len(all_observations)):
        observations = all_observations[i]
        paper_results = all_paper_results[i]
        p_hypotheses_given_data = syntactic_probabilities(hypothesis_space, observations, p_c_v_dist, priors_dist)
        p_hypotheses_given_data_table = p_hypotheses_given_data.dictionary
        if not compare_probabilitiy_tables(p_hypotheses_given_data_table, all_paper_results[test_num-1]):
            print "Failed test:", test_num
            print 'observations:',  observations
            print str(paper_results), "does not equal", str(p_hypotheses_given_data_table)
        else:
            passed_tests_count += 1
            if verbose:
                print 'Passed test:',  test_num
                print 'observations:',  observations
                print "posteriors:", p_hypotheses_given_data
        test_num +=1

    if passed_tests_count == num_tests:
        print "Passed all", num_tests, "tests"
    else:
        print "Passed (", passed_tests_count, '/', num_tests, ") tests"


syntactic_bootstrapping_test()
semantic_bootstrapping_test()
