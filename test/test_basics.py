import sys
sys.path.insert(1, '../core')

from structs import *
from problem_gen import *
from algorithms import *
from util_test import *

num_restarts = 35
iterations = 7000
prob_params = {'num_workers':10, 'num_nodes':50, 'max_time':100, 'window_length_range':(25, 40), 'ptime_size_range':(0.25, 0.65), 'reward_range':(1, 5),
               'origin_dest_time_pad':2, 'role_frequencies':[0.4, 0.8, 0.1, 0.22, 0.13], 'role_benefit_ranges':[(-10,10) for i in range(5)],
               'job_demand_range':(3, 8), 'travel_time_range':(5, 15), 'correlate_reward_to_ptime':True, 'correlate_benefit_to_ptime':True, 'M':99999999.0}

pb = RandomizedWindowProblemGenerator(prob_params).generate()
pb.to_opl_file('../data/pb.dat')
pb.to_json_file('../data/pb.json')

ec = as_encoded_solution(pb)
wf = build_most_flexible_first_worker_ordering_f#(pb)
jnf = build_earliest_endtime_first_job_node_ordering_f#(pb)
rf = build_rarest_role_first_ordering_f#(pb)
ord_ec = OrderedSolutionSetInitializer(worker_ordering_f=wf, job_node_ordering_f=jnf, 
                                       role_ordering_f=rf).generate(pb, 1)[0]

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
 
alns_params = {'mutators':mutators, 'reward_points':[1,2,3,4], 'accept_criteria_f':improve_accept_criteria,
               'reaction_factor':0.5, 'max_iter':iterations, 'max_unimprove_iter':None, 'max_time':None, 
               'max_unimprove_time':None, 'num_restarts':num_restarts}
ls_params = {'mutators':[basic_mutate], 'reward_points':[1,2,3,4], 'accept_criteria_f':improve_accept_criteria,
             'reaction_factor':0.5, 'max_iter':iterations, 'max_unimprove_iter':None, 'max_time':None, 
             'max_unimprove_time':None, 'num_restarts':num_restarts}
 
print('Initial Solution:')
print(construct_solution(pb, ec)['objective_f'])
print('\nGreedy Solution:')
print(construct_solution(pb, ord_ec)['objective_f'])
print('\nLocal Search Solution:')
improved_alns = alns(pb, ord_ec, ls_params)
print(construct_solution(pb, improved_alns)['objective_f'])
print('\nALNS Solution:')
improved_alns = alns(pb, ord_ec, alns_params)
print(construct_solution(pb, improved_alns)['objective_f'])