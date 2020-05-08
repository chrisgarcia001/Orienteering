import json
import os
from structs import *
from algorithms import *

# -------------------------------------------- Algorithm Runner Class ------------------------------------------------------------------------------------

# This class allows the running of any algorithm which takes the following inputs: 1) a Problem, 2) an EncodedSolution, and 3) a set of params
class AlgorithmRunner:
    def __init__(self, params):
        self.params = params
        self.algorithm = self.params['algorithm']
        self.problem_folder = self.params['problem_folder']
        self.solution_folder = self.params['solution_folder'] if 'solution_folder' in params else None
        self.solution_set_initializer = self.params['solution_set_initializer']
    
    def run(self):
        try:
            os.makedirs(self.solution_folder)
        except:
            pass
        summary_csv_text = "Problem,Objective Function,Elapsed Time\n"
        solutions = []
        for filename in [x for x in os.listdir(self.problem_folder) if x.endswith('json')]:
            try:
                prob_name = filename[:len('_.json')]
                print('Solving problem: ' + filename + '...')
                problem = Problem()
                problem.from_json_file(os.path.join(self.problem_folder, filename))
                initial_ec = self.solution_set_initializer.generate(problem, 1)[0]
                start_time = time.time()
                best_ec = self.algorithm(problem, initial_ec, self.params)
                sol = construct_solution(problem, best_ec)
                elapsed_time = time.time() - start_time
                sol['elapsed_time'] = elapsed_time
                sol['problem_name'] = prob_name
                solutions.append(sol)
                summary_csv_text += str(prob_name) + ',' + str(sol['objective_f']) + ',' + str(elapsed_time) + "\n"
                if self.solution_folder != None:
                    print('..writing to file ' + os.path.join(self.solution_folder, filename))
                    with open(os.path.join(self.solution_folder, filename), 'w') as outfile:
                        json.dump(sol, outfile)
            except:
               print('Unable to read file as Problem: ' + filename)
        if self.solution_folder != None:
            print('Writing summary CSV file: ' + os.path.join(self.solution_folder, 'summary.csv') + '.....')
            with open(os.path.join(self.solution_folder, 'summary.csv'), 'w') as outfile:
                outfile.write(summary_csv_text)
        print('Done!')    
        return solutions
            
