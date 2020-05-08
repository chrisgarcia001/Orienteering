import os
from structs import Problem
from util_data import *


class RandomizedWindowProblemGenerator:
    def __init__(self, params):
        self.num_workers = params['num_workers']
        self.num_roles = len(params['role_frequencies'])
        self.num_nodes = params['num_nodes']
        self.max_time = params['max_time']
        self.window_length_range = params['window_length_range']
        self.ptime_size_range = params['ptime_size_range']
        self.reward_range = params['reward_range']
        self.origin_dest_time_pad = params['origin_dest_time_pad']
        self.role_frequencies = params['role_frequencies']
        self.role_benefit_ranges = params['role_benefit_ranges']
        self.job_demand_range = params['job_demand_range']
        self.travel_time_range = params['travel_time_range']    
        self.correlate_reward_to_ptime = params['correlate_reward_to_ptime']
        self.correlate_benefit_to_ptime = params['correlate_benefit_to_ptime']
        self.M = params['M']
        
    def generate(self):
        job_time_range = (self.origin_dest_time_pad, self.max_time - self.origin_dest_time_pad)
        windows = [rand_segment(*(list(self.window_length_range) + list(job_time_range))) for i in range(self.num_nodes - 2)]
        ptimes = [rand_float(*self.ptime_size_range) * (x2 - x1) for (x1, x2) in windows]
        windows = [(0, 0)] + windows + [(0, self.max_time)]
        ptimes = [0] + ptimes + [0]
        qualifications = rand_bin_matrix(self.num_workers, [round(f * self.num_workers) for f in self.role_frequencies])
        rewards = [rand_float(*self.reward_range) for i in range(self.num_nodes - 2)]
        rewards = [ptimes[i + 1] * rewards[i] for i in range(len(rewards))] if self.correlate_reward_to_ptime else rewards
        demands = [rand_slot_distribute(rnd.randint(*self.job_demand_range), self.num_roles) for i in range(self.num_nodes - 2)]
        demands = [list(c) for c in zip(*demands)]
        benefits = [[[rand_float(*self.role_benefit_ranges[i]) for j in range(self.num_nodes - 2)] 
                      for i in range(self.num_roles)] for h in range(self.num_workers)]
        if self.correlate_benefit_to_ptime:
            for h in range(self.num_workers):
                for i in range(self.num_roles):
                    for j in range(self.num_nodes - 2):
                        benefits[h][i][j] *= ptimes[j + 1]
        transp_times = const_matrix(self.num_nodes, self.num_nodes, 0)
        for i in range(len(transp_times)):
            for j in range(i + 1):
                if i == j:
                    transp_times[i][j] = self.M
                else:
                    transp_times[i][j] = rand_float(*self.travel_time_range)
                transp_times[j][i] = transp_times[i][j]
        return Problem(self.num_workers, self.num_roles, self.num_nodes, windows, ptimes, self.M,
                       qualifications, demands, rewards, benefits, transp_times)

class ProblemSetGenerator:
    def __init__(self, params):
        params = self.eval_params(params)
        #print(params)
        #exit()
        self.problem_generator = params['problem_generator_class'](params)
        self.problem_set_name = params['problem_set_name']
        self.num_replicates = params['num_replicates']
        self.json_output_folder = params['json_output_folder'] if 'json_output_folder' in params else None
        self.opl_output_folder = params['opl_output_folder'] if 'opl_output_folder' in params else None
    
    def eval_params(self, params):
        pms = {}
        for param in params:
            try:
                pms[param] = eval(params[param])
            except:
                pms[param] = params[param]
        return pms
    
    def generate(self):
        if self.json_output_folder != None:
            try:
                os.makedirs(self.json_output_folder)
            except:
                pass
        if self.opl_output_folder != None:
            try:
                os.makedirs(self.opl_output_folder)
            except:
                pass
        
        print('---- Generating Problem Set ' + str(self.problem_set_name) + '----')
        for i in range(self.num_replicates):
            problem = self.problem_generator.generate()
            problem_name = str(self.problem_set_name) + '_' + str(i + 1)
            if not(self.json_output_folder == None):
                print(' Writing problem to file: ' + os.path.join(self.json_output_folder, problem_name + '.json'))
                problem.to_json_file(os.path.join(self.json_output_folder, problem_name + '.json'))
            if not(self.opl_output_folder == None):
                print(' Writing problem to file: ' + os.path.join(self.opl_output_folder, problem_name + '.dat'))
                problem.to_opl_file(os.path.join(self.opl_output_folder, problem_name + '.dat'))
        print('---------------------- DONE! -------------------------------------')
        

# TODO: Implement this (currently just a copy of above)        
class RegularWindowProblemGenerator:
    # window_specs = [{'window_length':length, 'num_windows':horizon, 'num_jobs_per_window':replicates, 'ptime_size_range':(min, max)}
    def __init__(self, num_workers=10, num_nodes=5, window_length=10, ptime_size_range=(0.1, 0.5), 
                 reward_range=(1, 5), origin_dest_time_pad=2, role_frequencies=[0.3, 0.8, 0.1], role_benefit_ranges=[(1,1),(1,1),(1,1)],
                 job_demand_range=(1,3), travel_time_range=(1,10), correlate_reward_to_ptime=True, correlate_benefit_to_ptime=True, 
                 M=9999999999.9):
        self.num_workers = num_workers
        self.num_roles = len(role_frequencies)
        self.num_nodes = num_nodes
        self.max_time = max_time
        self.window_length_range = window_length_range
        self.ptime_size_range = ptime_size_range
        self.reward_range = reward_range
        self.origin_dest_time_pad = origin_dest_time_pad
        self.role_frequencies = role_frequencies
        self.role_benefit_ranges = role_benefit_ranges
        self.job_demand_range = job_demand_range
        self.travel_time_range = travel_time_range    
        self.correlate_reward_to_ptime = correlate_reward_to_ptime
        self.correlate_benefit_to_ptime = correlate_benefit_to_ptime
        self.M = M
        
    def generate(self):
        job_time_range = (self.origin_dest_time_pad, self.max_time - self.origin_dest_time_pad)
        windows = [rand_segment(*(list(self.window_length_range) + list(job_time_range))) for i in range(self.num_nodes - 2)]
        ptimes = [rand_float(*self.ptime_size_range) * (x2 - x1) for (x1, x2) in windows]
        windows = [(0, 0)] + windows + [(0, self.max_time)]
        ptimes = [0] + ptimes + [0]
        qualifications = rand_bin_matrix(self.num_workers, [round(f * self.num_workers) for f in self.role_frequencies])
        rewards = [rand_float(*self.reward_range) for i in range(self.num_nodes - 2)]
        rewards = [ptimes[i + 1] * rewards[i] for i in range(len(rewards))] if self.correlate_reward_to_ptime else rewards
        demands = [rand_slot_distribute(rnd.randint(*self.job_demand_range), self.num_roles) for i in range(self.num_nodes - 2)]
        demands = [list(c) for c in zip(*demands)]
        benefits = [[[rand_float(*self.role_benefit_ranges[i]) for j in range(self.num_nodes - 2)] 
                      for i in range(self.num_roles)] for h in range(self.num_workers)]
        if self.correlate_benefit_to_ptime:
            benefits = [[[j * ptimes[i] for j in range(self.num_nodes - 2)] 
                          for i in range(self.num_roles)] for h in range(self.num_workers)] 
        transp_times = const_matrix(self.num_nodes, self.num_nodes, 0)
        for i in range(len(transp_times)):
            for j in range(i + 1):
                if i == j:
                    transp_times[i][j] = self.M
                else:
                    transp_times[i][j] = rand_float(*self.travel_time_range)
                transp_times[j][i] = transp_times[i][j]
        return Problem(self.num_workers, self.num_roles, self.num_nodes, windows, ptimes, self.M,
                       qualifications, demands, rewards, benefits, transp_times)
                
        
                  