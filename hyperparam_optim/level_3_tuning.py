import sys
sys.path.insert(1, '../core')

import json
from structs import *
from problem_gen import *
from algorithms import *
from algorithm_runner import *
from param_optim import *

root_prob_folder = './tuning/level_2'
output_filename = './level_3_report.csv'

num_restarts = [35]
iterations = [100000]
unimprove_iterations = [800]
it = unimprove_iterations[0] 
accept_fs = [build_decreasing_prob_accept_criteria_f(0.2, 0.001, it * 0.8)]
reward_points = [[1,2,3,4], [1,2,4,8], [1,1,1,10]]
mutator_sets = [
                [build_randomized_mutator_f(0, 0, 1, 0.1),
                 build_randomized_mutator_f(1, 1, 1, 0.1),
                 build_randomized_mutator_f(1, 1, 1, 0.5),
                 build_randomized_mutator_f(2, 4, 2, 0.1), 
                 build_randomized_mutator_f(2, 4, 2, 0.5),
                 build_randomized_mutator_f(8, 15, 3, 0.5),
                 build_randomized_mutator_f(8, 15, 1, 0.1)]
                ]


wf = build_least_flexible_first_worker_ordering_f
jnf = build_earliest_endtime_first_job_node_ordering_f
rf = build_rarest_role_first_ordering_f
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, role_ordering_f=rf)
 
alns_param_grid = {'mutators':mutator_sets, 'reward_points':reward_points, 'accept_criteria_f':accept_fs,
                   'reaction_factor':[0.75], 'max_iter':iterations, 'max_unimprove_iter':unimprove_iterations, 'max_time':[None], 
                   'max_unimprove_time':[None], 'num_restarts':num_restarts,
                   'algorithm':[alns], 
                   'solution_set_initializer':[ord_ec]
                   }
gs = GridSearchParamOptimizer(alns_param_grid, root_prob_folder, output_filename)
gs.optimize()