import os
import sys
sys.path.insert(1, '../core')

from structs import *
from problem_gen import *
from algorithms import *
from util_test import *

p1 = Problem(rewards=[1,2,3,4,5])
p1.to_json_file('./datatest.json')
p2 = Problem()
p2.from_json_file('./datatest.json')
print(p2.to_dict())
print(p2.to_opl())

for i in range(3):
    print(rand_slot_distribute(3, 4))

p3 = RandomizedWindowProblemGenerator(num_workers=15, num_nodes=10, max_time=30, correlate_reward_to_ptime=False, correlate_benefit_to_ptime=False).generate()
p3.to_opl_file('./data/p3.dat')


#def __init__(self, num_workers=10, num_nodes=5, max_time=100, window_length_range=(5, 10), ptime_size_range=(0.1, 0.5), 
#                 reward_range=(1, 5), origin_dest_time_pad=2, role_frequencies=[0.3, 0.8, 0.1], role_benefit_ranges=[(1,1),(1,1),(1,1)],
#                 job_demand_range=(1,3), travel_time_range=(1,10), correlate_reward_to_ptime=True, correlate_benefit_to_ptime=True, 
#                 M=9999999999.9):
p4 = RandomizedWindowProblemGenerator(num_workers=40, num_nodes=100, max_time = 100, 
                                      window_length_range=(25, 40), ptime_size_range=(0.25, 0.65), origin_dest_time_pad=2,
                                      role_frequencies=[0.4, 0.8, 0.1, 0.22, 0.13], role_benefit_ranges=[(-10,10) for i in range(5)],
                                      job_demand_range=(3, 8), travel_time_range=(5, 15),
                                      correlate_reward_to_ptime=True, correlate_benefit_to_ptime=True).generate()
p4.to_opl_file('./data/p4.dat')

ec = as_encoded_solution(p3)
print(ec.workers)
print(ec.job_nodes)
print(construct_solution(p3, ec))

rnd_ecs_1 = RandomizedSolutionSetInitializer(p3, 5).generate()
print(rnd_ecs_1)

rnd_ecs_2 = OrderedSolutionSetInitializer(p3, worker_ordering_f=randomly_order, job_node_ordering_f=randomly_order, 
                                          role_ordering_f=randomly_order, n=5).generate()
print(rnd_ecs_2)


print("\n\n")
wf = build_least_flexible_first_worker_ordering_f(p3)
jnf = build_earliest_endtime_first_job_node_ordering_f(p3)
rf = build_rarest_role_first_ordering_f(p3)

ord_ec = OrderedSolutionSetInitializer(p3, worker_ordering_f=wf, job_node_ordering_f=jnf, 
                                          role_ordering_f=rf, n=5).generate()[0]
print(ord_ec.workers)
print(ord_ec.job_nodes)
#print(p3.e)

print("\n\n")
mutate = build_randomized_mutator_f(3, 3, 2, 0.5)
mec = mutate(ord_ec)
print(ord_ec.workers)
print(mec.workers)
print('-----')
print(ord_ec.job_nodes)
print('-')
print(mec.job_nodes)

print("\n\n----------- Testing Local Search ------------")
print('Initial Solution:')
print(construct_solution(p3, ec))
print('\nGreedy Solution:')
print(construct_solution(p3, ord_ec))
print('\nLocal Search Solution:')
improved = local_search(p3, ec, mutate, max_iter=200)
print(construct_solution(p3, improved))
#print_solution(improved, p3)


print("\n\n----------- Testing ALNS ------------")
num_restarts = 10
iterations = 20000
accept_f = build_decreasing_prob_accept_criteria_f(0.2, 0.001, iterations * 0.8)

p5 = RandomizedWindowProblemGenerator(num_workers=20, num_nodes=50, max_time = 100, 
                                      window_length_range=(25, 40), ptime_size_range=(0.25, 0.65), origin_dest_time_pad=2,
                                      role_frequencies=[0.4, 0.8, 0.1, 0.22, 0.13], role_benefit_ranges=[(-10,10) for i in range(5)],
                                      job_demand_range=(3, 8), travel_time_range=(5, 15),
                                      correlate_reward_to_ptime=True, correlate_benefit_to_ptime=True).generate()
#p5 = p4
p5.to_opl_file('./data/p5.dat')


ec = as_encoded_solution(p5)
wf = build_least_flexible_first_worker_ordering_f(p5)
jnf = build_earliest_endtime_first_job_node_ordering_f(p5)
rf = build_rarest_role_first_ordering_f(p5)
ord_ec = OrderedSolutionSetInitializer(p5, worker_ordering_f=wf, job_node_ordering_f=jnf, 
                                          role_ordering_f=rf, n=5).generate()[0]
print('Initial Solution:')
print(construct_solution(p5, ec)['objective_f'])
print('\nGreedy Solution:')
print(construct_solution(p5, ord_ec)['objective_f'])
print('\nLocal Search Solution:')
for i in range(num_restarts):
    improved = local_search(p5, ord_ec, mutate, max_iter=iterations)
    print(construct_solution(p5, improved)['objective_f'])
    pass
    
#mutators = [build_worker_mutator(3), build_job_node_mutator(3), build_role_mutator(2, 0.5)]#, mutate]#

mutators = [build_randomized_mutator_f(1, 1, 1, 0.1),
            build_randomized_mutator_f(1, 1, 1, 0.5),
            build_randomized_mutator_f(2, 4, 2, 0.1), 
            build_randomized_mutator_f(2, 4, 2, 0.25),
            build_randomized_mutator_f(8, 15, 3, 0.5),
            build_randomized_mutator_f(8, 15, 1, 0.1)
            ]
#mutators = [build_randomized_mutator_f(1, 1, 1, 0.1),
#            build_randomized_mutator_f(2, 4, 2, 0.25), # TODO: Experiment with different mutators for different problem sizes. ALNS works best for larger problems.
#            build_randomized_mutator_f(4, 8, 3, 0.5)]

#mutators = [mutate]
#mutators = [build_worker_mutator(3), build_worker_mutator(8), build_job_node_mutator(4), build_job_node_mutator(15), build_role_mutator(3, 0.5), build_role_mutator(1, 0.1)]#, mutate]

#print_solution(improved, p3)
print('\nALNS Solution (default accept_f):')
for i in range(num_restarts):
    improved_alns = alns(p5, ord_ec, mutators, max_iter=iterations, reaction_factor=0.5)
    print(construct_solution(p5, improved_alns)['objective_f'])

print('\nALNS Solution (custom accept_f):')
for i in range(num_restarts):
    improved_alns = alns(p5, ord_ec, mutators, max_iter=iterations, reaction_factor=0.5, accept_criteria_f=accept_f)
    print(construct_solution(p5, improved_alns)['objective_f'])
