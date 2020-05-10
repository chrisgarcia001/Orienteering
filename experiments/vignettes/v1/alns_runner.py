# This script runs the ALNS algorithm on the generated problems.

import sys
sys.path.insert(1, '../../../core')

import json
from structs import *
from algorithms import *
from algorithm_runner import *

# --------------------- Setup Algorithm Params and Solve Problems ---------------------------------------
num_restarts = 50
iterations = 10000000

wf = build_least_flexible_first_worker_ordering_f
jnf = build_earliest_endtime_first_job_node_ordering_f
rf = build_rarest_role_first_ordering_f
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, role_ordering_f=rf)

unimprove_iterations = 3000
accept_f = build_decreasing_prob_accept_criteria_f(0.2, 0.001, unimprove_iterations * 0.8)
mutators = [build_randomized_mutator_f(0, 0, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.5),
            build_randomized_mutator_f(2, 4, 2, 0.1), 
            build_randomized_mutator_f(2, 4, 2, 0.5),
            build_randomized_mutator_f(8, 15, 3, 0.5),
            build_randomized_mutator_f(8, 15, 1, 0.1)]
 
alns_params = {'mutators':mutators, 'reward_points':[1,2,4,8], 'accept_criteria_f':accept_f,
               'reaction_factor':0.75, 'max_iter':iterations, 'max_unimprove_iter':unimprove_iterations, 'max_time':None, 
               'max_unimprove_time':None, 'num_restarts':num_restarts,
               'algorithm':alns, 
               'problem_folder':'./problems/json',
               'solution_folder':'./solutions/alns',
               'solution_set_initializer':ord_ec}

ar = AlgorithmRunner(alns_params)
ar.run()