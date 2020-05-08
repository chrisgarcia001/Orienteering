#-----------------------------------------------------------------------------------------------------
# Author: cgarcia@umw.edu
# Created: 2/17/2020
# About: This file contains the main algorithm implementations and requisite structures for solving 
#        the Multiskill Dynamic Team Orienteering problem.
#
# Revision History:
# Date        Author            Change Description
# 2/17/2020   cgarcia           Initial version.
#-----------------------------------------------------------------------------------------------------

import os
import time
import json
import random as rnd
import util_data as du

# -------------------------------------------- Prerequisite Structures and Functions ---------------------------------------

# This class provides a permutable solution encoding which can be used to construct a solution.
class EncodedSolution:
    # @param workers: [worker_id]
    # @param: job_nodes: [(node_id, [(role_index, demand)])]
    def __init__(self, workers, job_nodes):
        self.workers = list(workers)
        self.job_nodes = list(job_nodes)
    
    # Returns a copy of self
    def copy(self):
        return EncodedSolution(self.workers, self.job_nodes)

# Converts a problem into an encoded solution with jobs, workers, and demands ordered as they appear listed in the problem.
# @param problem: a Problem object
# @returns: an EncodedSolution object
def as_encoded_solution(problem):
    workers = list(range(problem.num_workers))
    nodes = [(j + 1, [(i, problem.d[i][j]) for i in range(problem.num_roles) if problem.d[i][j] > 0]) for j in range(problem.num_nodes - 2)]
    return EncodedSolution(workers, nodes)

# This function constructs a feasible solution for the problem, obtained by using the encoded_solution.
# @param problem: a Problem object
# @param encoded_sol: an EncodedSolution object
# @returns: a dict of form {'assignments' : [(job_id, start_time, [(worker_id, arrival_time, assigned_role)])], 'objective_f' : <obj. func. val.>}
def construct_solution(problem, encoded_sol):
    alpha = 0
    omega = problem.num_nodes - 1
    workers = dict([(h, [0, problem.w[0][0] + problem.p[0]]) for h in list(encoded_sol.workers)]) # {worker_id: [curr_node_id, available_departure_time]}
    job_nodes = list(encoded_sol.job_nodes) # NOTE: When accessing problem.b, problem.d, or problem.r - MAKE SURE to convert node_id to (node_id - 1)
    assignments = [] # [(job_id, start_time, [(worker_id, arrival_time, assigned_role)])]   
    total_reward = 0
    total_benefit = 0
    for (j, demands) in job_nodes:
        curr_d_met = [0 for r in range(problem.num_roles)]
        demands = [list(d) for d in demands]
        curr_workers = [] # [(worker_id, arrival_time, assigned_role)]
        for h in encoded_sol.workers: 
            prev_node = workers[h][0]
            depart_time = workers[h][1]
            if demands == []:
                break
            travel_time = problem.t[prev_node][j]
            if depart_time + travel_time < problem.w[j][1]:
                i = 0
                while i < len(demands):
                    if problem.e[h][demands[i][0]] == 1:
                        curr_workers.append((h, depart_time + travel_time, demands[i][0]))
                        demands[i][1] -= 1
                        if demands[i][1] == 0:
                            del demands[i]  
                        i = len(demands)
                    i += 1
        start_time = max([x[1] for x in curr_workers] + [problem.w[j][0]]) 
        if demands == [] and start_time + problem.p[j] + problem.t[j][omega] <= problem.w[omega][1]:
            total_reward += problem.r[j - 1]
            assignments.append((j, start_time, curr_workers))
            for h, arrival, role in curr_workers:
                workers[h][0] = j
                workers[h][1] = start_time + problem.p[j]
                total_benefit += problem.b[h][role][j - 1]
    return {'assignments':assignments, 'objective_f':total_reward + total_benefit}
    
# -------------------------------------------- Solution Set Initializers ---------------------------------------------------
# Base class for all SolutionSetInitializers
class SolutionSetInitializer:
    def __init__(self):
        raise 'SolutionSetInitializer.__init__ is an abstract method: please subclass and provide an implementation'
        
    def generate(self):
        raise 'SolutionSetInitializer.generate is an abstract method: please subclass and provide an implementation'
 
# This class privides a completely randomized set of inital encoded solutions. Specifically, it shuffles the
# workers, job nodes, and job demands at each node. 
class RandomizedSolutionSetInitializer:
    def __init__(self):
        pass
       
    # Generates a list of specified length of initial solutions
    def generate(self, problem, n):
        sols = []
        initial_sol = as_encoded_solution(self.problem)
        for i in range(n):
            workers = list(initial_sol.workers)
            rnd.shuffle(workers)
            job_nodes = list(initial_sol.job_nodes)
            rnd.shuffle(job_nodes)
            for j, demands in job_nodes:
                rnd.shuffle(demands)
            sols.append(EncodedSolution(workers, job_nodes))
        return sols

# This class allows a set of solutions to be created with a specified ordering for workers, job nodes, and requred roles at jobs.            
class OrderedSolutionSetInitializer:
    def __init__(self, worker_ordering_f=None, job_node_ordering_f=None, role_ordering_f=None):
        self.worker_ordering_f = worker_ordering_f
        self.job_node_ordering_f = job_node_ordering_f
        self.role_ordering_f = role_ordering_f
        
    def generate(self, problem, n):
        sols = []
        initial_sol = as_encoded_solution(problem)
        for i in range(n):
            workers = list(initial_sol.workers)
            if self.worker_ordering_f != None:
                workers = self.worker_ordering_f(problem, list(initial_sol.workers))
            job_nodes = []
            for j, demands in list(initial_sol.job_nodes):
                if self.role_ordering_f != None:
                    job_nodes.append((j, self.role_ordering_f(problem, list(demands))))
                else:
                    job_nodes.append((j, list(demands)))
            if self.job_node_ordering_f != None:
                job_nodes = self.job_node_ordering_f(problem, job_nodes)
            sols.append(EncodedSolution(workers, job_nodes))
        return sols
        
# ******** Specific ordering function generators to be used with the OrderedSolutionSetInitializer **********

# Returns a new list consisting of a random ordering of the original elements.
def randomly_order(elements):
    e = list(elements)
    rnd.shuffle(e)
    return e

# Orders workers in least-skills/roles-first (i.e. most-flexible-first) order.
def build_most_flexible_first_worker_ordering_f(problem, workers):
    skill_counts = dict([(h, sum(problem.e[h])) for h in range(problem.num_workers)])
    #return lambda workers: sorted(list(workers), key=lambda h: skill_counts[h])
    return sorted(list(workers), key=lambda h: skill_counts[h])

# Orders job nodes in earliest-end-time-first order.    
def build_earliest_endtime_first_job_node_ordering_f(problem, job_nodes):
    job_node_end_times = dict([(j, problem.w[j][1]) for j in range(problem.num_nodes)])
    #return lambda job_nodes: sorted(list(job_nodes), key=lambda j: job_node_end_times[j[0]])
    return sorted(list(job_nodes), key=lambda j: job_node_end_times[j[0]])
 
# Orders roles in overall least-common-first ordering. 
def build_rarest_role_first_ordering_f(problem, demands):
    role_occurrences = dict([(i, sum(problem.d[i])) for i in range(problem.num_roles)])
    #return lambda demands: sorted(list(demands), key=lambda i: role_occurrences[i[0]])
    return sorted(list(demands), key=lambda i: role_occurrences[i[0]])
    

# -------------------------------------------- Encoded Solution Mutators and Local Search ----------------------------------

# Builds a randomized mutator function of form m : EncodedSolution -> EncodedSolution
# @param max_worker_swap_dist: the maximum distance in the worker list that any two workers can exchange position
# @param max_job_node_swap_dist: the maximum distance in the job node list that any two workers can exchange position
# @param max_role_swap_dist: the maximum distance in any job node's demand list that two role demands can exchange position
# @param role_swap_prob: the probability that a job node will have a swap occur in its demand list
# @returns: a mutator function of form m : EncodedSolution -> EncodedSolution
def build_randomized_mutator_f(max_worker_swap_dist, max_job_node_swap_dist, max_role_swap_dist, role_swap_prob):
    def swap(elems, a, b):
        if len(elems) <= 1:
            return elems
        a = min(len(elems) - 1, max(0, a))
        b = max(0, min(len(elems) - 1, b))
        ne = list(elems)
        t = ne[a]
        ne[a] = ne[b]
        ne[b] = t
        return ne
        
    def mutate(ec):
        wa, wb = du.rand_segment(1, min(len(ec.workers) - 1, max_worker_swap_dist), 0, len(ec.workers) - 1, integer=True)
        na, nb = du.rand_segment(1, min(len(ec.job_nodes) - 1, max_job_node_swap_dist), 0, len(ec.job_nodes), integer=True)
        workers = swap(ec.workers, wa, wb)
        job_nodes = []
        for j, demands in ec.job_nodes:
            if rnd.random() < role_swap_prob and len(demands) > 1:
                ra, rb = du.rand_segment(1, min(len(demands) - 1, max_role_swap_dist), 0, len(demands) - 1, integer=True)
                job_nodes.append((j, swap(demands, ra, rb)))
            else:
                job_nodes.append((j, list(demands)))
        job_nodes = swap(job_nodes, na, nb)
        return EncodedSolution(workers, job_nodes)
    return mutate

# Performs local search on an encoded solution
# @param problem: a Problem instance
# @param initial_ec: an EncodedSolution instance - the initial solution
# @param mutator_f: a mutator function of form f : EncodedSolution -> EncodedSolution
# @param max_iter: the maximum number of total iterations allowed
# @param max_unimprove_iter: the maximum number of total iterations allowed for no improvement to be found
# @param max_time: the maximum number of seconds allowed overall
# @param max_unimprove_time: the maximum amount of time allowed with no improvements to the solution
# @returns: the best EncodedSolution encountered
def local_search(problem, initial_ec, mutator_f, max_iter=None, max_unimprove_iter=None, max_time=None, max_unimprove_time=None):
    best_ec = initial_ec
    best_sol = construct_solution(problem, initial_ec)
    current_ec = initial_ec.copy()
    i = 0
    unimprove_i = 0
    start_time = time.time()
    improve_time = time.time()
    time_up = lambda: time.time() - start_time >= max_time if max_time != None else False
    improve_time_up = lambda: time.time() - improve >= max_unimprove_time if max_unimprove_time != None else False
    max_i_reached = lambda: i >= max_iter if max_iter != None else False
    max_unimprove_i_reached = lambda: unimprove_i >= max_unimprove_iter if max_unimprove_iter != None else False
    while not(time_up()) and not(improve_time_up()) and not(max_i_reached()) and not(max_unimprove_i_reached()):
        current_ec = mutator_f(current_ec)
        current_sol = construct_solution(problem, current_ec)
        if current_sol['objective_f'] > best_sol['objective_f']:
            best_ec = current_ec.copy()
            best_sol = current_sol
            unimprove_i = 0
            improve_time = time.time()
        else:
            unimprove_i += 1
        i += 1
    return best_ec

# -------------------------------------------- Adaptive Large Neighborhood Search & Associated Destroy/Repair Functions ----------------------------------

# An encapsulated termination determination function.
def terminate(i, unimprove_i, start_time, improve_time, max_iter=None, max_unimprove_iter=None, max_time=None, max_unimprove_time=None):
    time_up = lambda: time.time() - start_time >= max_time if max_time != None else False
    improve_time_up = lambda: time.time() - improve >= max_unimprove_time if max_unimprove_time != None else False
    max_i_reached = lambda: i >= max_iter if max_iter != None else False
    max_unimprove_i_reached = lambda: unimprove_i >= max_unimprove_iter if max_unimprove_iter != None else False
    return time_up() or improve_time_up() or max_i_reached() or max_unimprove_i_reached()

improve_accept_criteria = lambda curr_sol, next_sol, i: next_sol['objective_f'] > curr_sol['objective_f'] 

# The main Adaptive Large Neighborhood Search alorithm.
# TODO: Test!
def alns(problem, initial_ec, params):#mutators, reward_points=[1,2,3,4], accept_criteria_f=improve_accept_criteria, 
         #reaction_factor=0.25, max_iter=None, max_unimprove_iter=None, max_time=None, max_unimprove_time=None):
    best_ec = initial_ec
    best_sol = construct_solution(problem, initial_ec)
    for restart in range(params['num_restarts']):
        current_ec = initial_ec.copy()
        current_sol = construct_solution(problem, initial_ec)
        accum_rewards = [1.0 for i in range(len(params['mutators']))]
        conditions = [] # Add numbers corresponding to condition each iteration: 0=best improved, 1=current improved, 2=sol. accepted, 3=sol. rejected
        i = 0
        unimprove_i = 0
        start_time = time.time()
        improve_time = time.time()
        while not(terminate(i, unimprove_i, start_time, improve_time, params['max_iter'], 
                            params['max_unimprove_iter'], params['max_time'], params['max_unimprove_time'])):
            selected_mutator = du.random_weighted_index(accum_rewards)
            mutate = params['mutators'][selected_mutator]
            next_ec = mutate(current_ec)
            next_sol = construct_solution(problem, next_ec)
            if next_sol['objective_f'] > best_sol['objective_f']:
                best_ec = next_ec.copy()
                best_sol = next_sol
                conditions.append(3)
                unimprove_i = -1
                improve_time = time.time()
            if next_sol['objective_f'] > current_sol['objective_f']:
                conditions.append(2)
            if params['accept_criteria_f'](current_sol, next_sol, i):
                current_ec = next_ec
                current_sol = next_sol
                conditions.append(1)
            else:
                conditions.append(0)
            reward = params['reward_points'][max(conditions)]
            conditions = []
            accum_rewards[selected_mutator] += (params['reaction_factor'] * reward) + ((1 - params['reaction_factor']) * accum_rewards[selected_mutator]) 
            i += 1
            unimprove_i += 1
        print(' Restart ' + str(restart) + ' best solution = ' + str(best_sol['objective_f']))
    return best_ec

# --------- Destroy/repair functions (i.e. mutators) ------------------  
build_worker_mutator = lambda max_worker_swap_dist: build_randomized_mutator_f(max_worker_swap_dist, 0, 0, 0)   
build_job_node_mutator = lambda max_job_node_swap_dist: build_randomized_mutator_f(0, max_job_node_swap_dist, 0, 0)   
build_role_mutator = lambda max_role_swap_dist, role_swap_prob: build_randomized_mutator_f(0, 0, max_role_swap_dist, role_swap_prob)   
    
# -------------------------------------------- Acceptance Criteria Functions and Related Components ------------------------------------------------------

# Constructs a linearly decreasing accept probability function begining with start_p and ending with end_p. 
# The function will reach end_p for all i > iteration_span.
def build_decreasing_prob_accept_criteria_f(start_p, end_p, iteration_span):
    def f(curr_sol, next_sol, i):
        curr_p = end_p + ((max(float(iteration_span - i), 0) / float(iteration_span)) * (start_p - end_p)) 
        if next_sol['objective_f'] > curr_sol['objective_f'] or rnd.random() < curr_p:
            return True
        return False
    return f
















