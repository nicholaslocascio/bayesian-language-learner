""" Tests semantic and syntactic probabilities against those from the Niyogi paper. """

from syntactic_bootstrap import syntactic_probabilities
from semantic_bootstrap import semantic_probabilities
from integrated_bootstrap import integrated_probabilities

from dist import DDist
from utils import compare_probabilitiy_tables

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
    all_our_results = [semantic_probabilities(hypothesis_space, observations).dictionary for observations in all_observations]
    print "Testing the syntactic bootstrapping results against those from the paper."
    run_test(all_our_results, all_paper_results, all_observations, verbose)


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
    all_our_results = [syntactic_probabilities(hypothesis_space, obs, p_c_v_dist, priors_dist).dictionary for obs in all_observations]
    print "Testing the syntactic bootstrapping results against those from the paper."
    run_test(all_our_results, all_paper_results, all_observations, verbose)

def integrated_bootstrapping_test(verbose=False):
    """Tests the syntatic bootstrapping results against those from the paper."""

    test_1_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['1', '*', '*'],
    }]
    test_2_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['0', '*', '*'],
    }]
    test_3_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    }]
    test_4_obs = [{\
    "s": None,
    "u": ['1', '*', '*'],
    }]
    test_5_obs = [{\
    "s": None,
    "u": ['0', '*', '*'],
    }]
    test_6_obs = [{\
    "s": None,
    "u": ['*', '*', '*'],
    }]
    test_7_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '2'], 'W': ['1', '1', '0']},
    "u": ['1', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '0'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    }]
    test_8_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '2', '0']},
    "u": ['0', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    }]
    test_9_obs = [{\
    "s": {'G': ['0', '0', '1'], 'W': ['1', '1', '0']},
    "u": ['*', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '2'], 'W': ['1', '2', '0']},
    "u": ['*', '*', '*'],
    },
    {\
    "s": {'G': ['0', '0', '0'], 'W': ['1', '3', '0']},
    "u": ['*', '*', '*'],
    }]

    all_observations = [test_1_obs, test_2_obs, test_3_obs, test_4_obs,test_5_obs, test_6_obs, test_7_obs, test_8_obs, test_9_obs]

    paper_res_1 = {'H_pour' : 0.889, 'H_spray' : 0.008, 'H_splash' : 0.008, 'H_fill' : 0.000, 'H_empty' : 0.000, 'H_move' : 0.093}
    paper_res_2 = {'H_pour' : 0.000, 'H_spray' : 0.000, 'H_splash' : 0.000, 'H_fill' : 0.990, 'H_empty' : 0.009, 'H_move' : 0.000}
    paper_res_3 = {'H_pour' : 0.468, 'H_spray' : 0.004, 'H_splash' : 0.004, 'H_fill' : 0.468, 'H_empty' : 0.004, 'H_move' : 0.049}
    paper_res_4 = {'H_pour' : 0.246, 'H_spray' : 0.246, 'H_splash' : 0.246, 'H_fill' : 0.004, 'H_empty' : 0.004, 'H_move' : 0.254}
    paper_res_5 = {'H_pour' : 0.007, 'H_spray' : 0.007, 'H_splash' : 0.007, 'H_fill' : 0.485, 'H_empty' : 0.485, 'H_move' : 0.007}
    paper_res_6 = {'H_pour' : 0.166, 'H_spray' : 0.166, 'H_splash' : 0.166, 'H_fill' : 0.166, 'H_empty' : 0.166, 'H_move' : 0.170}
    paper_res_7 = {'H_pour' : 0.998, 'H_spray' : 0.000, 'H_splash' : 0.000, 'H_fill' : 0.000, 'H_empty' : 0.000, 'H_move' : 0.001}
    paper_res_8 = {'H_pour' : 0.000, 'H_spray' : 0.000, 'H_splash' : 0.000, 'H_fill' : 0.999, 'H_empty' : 0.000, 'H_move' : 0.000}
    paper_res_9 = {'H_pour' : 0.064, 'H_spray' : 0.064, 'H_splash' : 0.064, 'H_fill' : 0.000, 'H_empty' : 0.000, 'H_move' : 0.808}

    all_paper_results = [paper_res_1, paper_res_2, paper_res_3, paper_res_4, paper_res_5, paper_res_6, paper_res_7, paper_res_8, paper_res_9]

    hypothesis_space = {'H_pour': '11*', 'H_spray' : '12*', 'H_splash': '13*', 'H_fill': '0*1', 'H_empty': '0*2', 'H_move': '1**'}

    priors_table = {hypothesis : 1.0/len(hypothesis_space) for hypothesis in hypothesis_space.keys()}

    all_our_results = [integrated_probabilities(hypothesis_space, obs, priors_table).dictionary for obs in all_observations]
    print "Testing the integrated bootstrapping results against those from the paper."
    run_test(all_our_results, all_paper_results, all_observations, verbose)

def run_test(all_our_results, all_paper_results, all_observations, verbose=False):
    passed_tests_count = 0
    test_num = 1
    num_tests = len(all_paper_results)
    for i in range(num_tests):
        observations = all_observations[i]
        paper_result = all_paper_results[i]
        our_result = all_our_results[i]
        if not compare_probabilitiy_tables(our_result, paper_result):
            print "Failed test: ", test_num
            print 'Our result:'
            print str(our_result)
            print "does not match paper result:"
            print str(paper_result)
        else:
            passed_tests_count += 1
            if verbose:
                print 'Passed test #',  test_num
                print 'observations:',  observations
                print "posteriors:", our_result
        test_num +=1
    if passed_tests_count == num_tests:
        print "Passed all", num_tests, "tests"
    else:
        print "Passed (", passed_tests_count, '/', num_tests, ") tests"
    return

integrated_bootstrapping_test(True)
