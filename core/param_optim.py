import sys

import json
from functools import *
from structs import *
from problem_gen import *
from algorithms import *
from algorithm_runner import *

# Turns param grid into a dict of form {param_name:index_list}
# @param param_grid: a dict of form {param_name:values_list}
def indexify(param_grid):
    return dict([(v, list(range(len(param_grid[v])))) for v in param_grid.keys()])

# Given a param grid and an indexed parameter set, get the corresponding param set
def deindexify(param_grid, indexed_params):
    return dict([(k, param_grid[k][indexed_params[k]]) for k in indexed_params.keys()])

# Given a param grid (in regular or indexed form), get a set of corresponding param sets over all possible param value combinations.
def build_param_sets(param_grid):
    if len(param_grid) == 0:
        return [{}]
    else:
        itms = list(param_grid.items())
        key, vals = itms[0]
        rest = [list(x.items()) for x in build_param_sets(dict(itms[1:]))]
        return reduce(lambda x,y: x+y, [[dict([(key, val)] + r) for val in vals] for r in rest])

def params_to_str(params, select_keys=None):
    if select_keys == None:
        select_keys = list(params.keys()) 
    s = ''
    strvs = [str(p) + ':' + str(v) for (p, v) in sorted([(x,y) for (x,y) in params.items() if x in select_keys], key=lambda x:x[0])]
    return '_'.join(strvs)

class GridSearchParamOptimizer:
    def __init__(self, param_grid, root_prob_folder, output_filename):
        self.param_grid = param_grid
        self.variable_params = [k for k in param_grid.keys() if len(param_grid[k]) > 1]
        self.root_prob_folder = root_prob_folder    
        self.output_filename = output_filename
    
    def optimize(self):
        pg = indexify(self.param_grid)
        combs = build_param_sets(pg)
        prob_folders = os.listdir(self.root_prob_folder)
        headers = 'Param Combination'
        data = [params_to_str(x, self.variable_params) for x in combs]
        
        for pset_folder in prob_folders:
            try:
                print('--- Testing Problem Set: ' + pset_folder + ' ----')
                results = [] 
                for comb in combs:
                    print(' Running Param Set: ' + params_to_str(comb, self.variable_params))
                    params = deindexify(self.param_grid, comb)
                    params['problem_folder'] = os.path.join(self.root_prob_folder, pset_folder)
                    runner = AlgorithmRunner(params)
                    results.append(runner.run())
                best_obj = [max([results[i][j]['objective_f'] for i in range(len(combs))]) for j in range(len(results[0]))]
                wins = [sum([int(results[i][j]['objective_f'] == best_obj[j]) for j in range(len(best_obj))]) for i in range(len(combs))]
                avg = lambda x: sum(x) / float(len(x))
                pbest = lambda x: [x[j] / best_obj[j] for j in range(len(x))]
                avg_pbest = [round(avg(pbest([results[i][j]['objective_f'] for j in range(len(results[0]))])), 3) for i in range(len(combs))]
                avg_time = [round(avg([results[i][j]['elapsed_time'] for j in range(len(results[0]))]), 3) for i in range(len(combs))]
                pn = str(pset_folder)
                headers += ',wins(' + pn + '),avg_pbest(' + pn + '),avg_time(' + pn + ')' 
                data = [data[i] + ',' + ','.join([str(wins[i]), str(avg_pbest[i]), str(avg_time[i])]) for i in range(len(data))]
            except:
                pass
        print('Writing Param Results to ' + self.output_filename)
        with open(self.output_filename, 'w') as outfile:
            outfile.write("\n".join([headers] + data))

