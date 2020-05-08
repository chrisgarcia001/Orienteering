import sys
sys.path.insert(1, '../core')
#sys.path.insert(1, '../hyperparam_optim')

import json
from structs import *
from problem_gen import *
from algorithms import *
from algorithm_runner import *
from param_optim import *

test_pg = {'a':['q','r','s'], 'b':['t','u'], 'c':['v','w']}
print(indexify(test_pg))
print(build_param_sets(test_pg))
print(deindexify(test_pg, {'a':1, 'b':0, 'c':1}))
print(params_to_str({'a':1, 'b':0, 'c':1}))
print(params_to_str({'a':1, 'b':0, 'c':1}, ['a', 'c']))

# ------------------------ Main Tests -------------------------------------------
root_prob_folder = '../hyperparam_optim/test'
output_filename = '../hyperparam_optim/test_report.csv'

num_restarts = [10, 35, 50]
iterations = [1000, 3000, 5000]
unimprove_iterations = [100, 500]
accept_fs = [improve_accept_criteria,
             #build_decreasing_prob_accept_criteria_f(0.2, 0.001, iterations * 0.8)
             #build_decreasing_prob_accept_criteria_f(0.9, 0.001, 1000),
             #build_decreasing_prob_accept_criteria_f(0.9, 0.001, 5000),
             build_decreasing_prob_accept_criteria_f(0.4, 0.001, 2500),
             
            ]
basic_mutate = build_randomized_mutator_f(3, 3, 2, 0.5)
mutator_sets = [#[basic_mutate],
                [build_randomized_mutator_f(0, 0, 1, 0.1),
                 build_randomized_mutator_f(1, 1, 1, 0.1),
                 build_randomized_mutator_f(1, 1, 1, 0.5),
                 build_randomized_mutator_f(2, 4, 2, 0.1), 
                 build_randomized_mutator_f(2, 4, 2, 0.5),
                 build_randomized_mutator_f(8, 15, 3, 0.5),
                 build_randomized_mutator_f(8, 15, 1, 0.1)]
                ]


wf = build_most_flexible_first_worker_ordering_f
jnf = build_earliest_endtime_first_job_node_ordering_f
rf = build_rarest_role_first_ordering_f
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, role_ordering_f=rf)

#accept_f = build_decreasing_prob_accept_criteria_f(0.2, 0.001, iterations * 0.8)
basic_mutate = build_randomized_mutator_f(3, 3, 2, 0.5)
mutators = [build_randomized_mutator_f(0, 0, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.5),
            build_randomized_mutator_f(2, 4, 2, 0.1), 
            build_randomized_mutator_f(2, 4, 2, 0.5),
            build_randomized_mutator_f(8, 15, 3, 0.5),
            build_randomized_mutator_f(8, 15, 1, 0.1)
            ]

#decreasing_accept_prob_criteria = build_decreasing_prob_accept_criteria_f(0.99, 0, iterations)
 
alns_param_grid = {'mutators':mutator_sets, 'reward_points':[[1,2,3,4]], 'accept_criteria_f':accept_fs,
                   'reaction_factor':[0.5], 'max_iter':iterations, 'max_unimprove_iter':unimprove_iterations, 'max_time':[None], 
                   'max_unimprove_time':[None], 'num_restarts':num_restarts,
                   'algorithm':[alns], 
                   #'problem_folder':'../data/test_gen_problems',
                   #'solution_folder':'../data/test_solutions',
                   'solution_set_initializer':[ord_ec]
                   }
gs = GridSearchParamOptimizer(alns_param_grid, root_prob_folder, output_filename)
gs.optimize()