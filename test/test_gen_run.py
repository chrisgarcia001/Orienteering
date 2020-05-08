import sys
sys.path.insert(1, '../core')

import json
from structs import *
from problem_gen import *
from algorithms import *
from algorithm_runner import *

# --------------------- Generate Test Problems -------------------------------------------------
pgen_param_file = '../params/test/prob_gen_test_6.json'
problem_folder = '../data/test_gen_problems'

params = {}
with open(pgen_param_file, 'r') as infile:
    params = json.load(infile)
    
pg = ProblemSetGenerator(params)
pg.generate()

# BELOW: Comment out if you want to only generate problems, not test algorithms.
#exit()

# --------------------- Run Algorithm and Solve Problems ---------------------------------------
num_restarts = 35
iterations = 3000

wf = build_most_flexible_first_worker_ordering_f
jnf = build_earliest_endtime_first_job_node_ordering_f
rf = build_rarest_role_first_ordering_f
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, role_ordering_f=rf)

accept_f = build_decreasing_prob_accept_criteria_f(0.2, 0.001, iterations * 0.8)
basic_mutate = build_randomized_mutator_f(3, 3, 2, 0.5)
mutators = [build_randomized_mutator_f(0, 0, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.5),
            build_randomized_mutator_f(2, 4, 2, 0.1), 
            build_randomized_mutator_f(2, 4, 2, 0.5),
            build_randomized_mutator_f(8, 15, 3, 0.5),
            build_randomized_mutator_f(8, 15, 1, 0.1)
            ]

decreasing_accept_prob_criteria = build_decreasing_prob_accept_criteria_f(0.99, 0, iterations)
 
alns_params = {'mutators':mutators, 'reward_points':[1,2,3,4], 'accept_criteria_f': decreasing_accept_prob_criteria, #improve_accept_criteria,
               'reaction_factor':0.5, 'max_iter':iterations, 'max_unimprove_iter':500, 'max_time':None, 
               'max_unimprove_time':None, 'num_restarts':num_restarts,
               'algorithm':alns, 
               'problem_folder':'../data/test_gen_problems',
               'solution_folder':'../data/test_solutions',
               'solution_set_initializer':OrderedSolutionSetInitializer(worker_ordering_f=build_most_flexible_first_worker_ordering_f, 
                                                          job_node_ordering_f=build_earliest_endtime_first_job_node_ordering_f, 
                                                          role_ordering_f=build_rarest_role_first_ordering_f)
               }
               
ls_params = {'mutators':[basic_mutate], 'reward_points':[1,2,3,4], 'accept_criteria_f':improve_accept_criteria,
             'reaction_factor':0.5, 'max_iter':iterations, 'max_unimprove_iter':None, 'max_time':None, 
             'max_unimprove_time':None, 'num_restarts':num_restarts,
             'algorithm':alns, 
             'problem_folder':'../data/test_gen_problems',
             'solution_folder':'../data/test_solutions',
             'solution_set_initializer':OrderedSolutionSetInitializer(worker_ordering_f=build_most_flexible_first_worker_ordering_f, 
                                                        job_node_ordering_f=build_earliest_endtime_first_job_node_ordering_f, 
                                                        role_ordering_f=build_rarest_role_first_ordering_f)
            }


ar = AlgorithmRunner(alns_params)
ar.run()