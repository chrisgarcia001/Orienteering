# This script runs the LS algorithm on the generated problems.

import sys
sys.path.insert(1, '../../../core')

import json
from structs import *
from algorithms import *
from algorithm_runner import *

# --------------------- Setup Algorithm Params and Solve Problems ---------------------------------------
num_restarts = 1
iterations = 5000

wf = build_least_flexible_first_worker_ordering_f
jnf = build_earliest_endtime_first_job_node_ordering_f
rf = build_rarest_role_first_ordering_f
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, role_ordering_f=rf)

basic_mutate = build_randomized_mutator_f(3, 3, 2, 0.5)
 
ls_params = {'mutators':[basic_mutate], 'reward_points':[1,1,1,1], 'accept_criteria_f':improve_accept_criteria,
             'reaction_factor':0.5, 'max_iter':iterations, 'max_unimprove_iter':None, 'max_time':None, 
             'max_unimprove_time':None, 'num_restarts':num_restarts,
             'algorithm':alns, 
             'problem_folder':'./problems/json',
             'solution_folder':'./solutions/ls',
             'solution_set_initializer':ord_ec}

ar = AlgorithmRunner(ls_params)
ar.run()