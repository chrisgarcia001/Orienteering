#-----------------------------------------------------------------------------------------------------
# Author: cgarcia@umw.edu
# Created: 2/14/2020
# About: This file contains some component structures used in solving the Multi-skill Dynamic Team
#        Orienteering problem.
#
# Revision History:
# Date        Author            Change Description
# 2/14/2020   cgarcia           Initial version.
#-----------------------------------------------------------------------------------------------------

import json

class Problem:
    def __init__(self, num_workers=0, num_roles=0, num_nodes=0, windows=[], ptimes=[], M=9999999999.9,
                 worker_role_qualifications=[], demands=[], rewards=[], benefits=[], travel_times=[]):
        self.num_workers = num_workers
        self.num_roles = num_roles
        self.num_nodes = num_nodes  # all nodes
        self.w = windows            # all nodes
        self.p = ptimes             # all nodes
        self.e = worker_role_qualifications
        self.d = demands            # [roles][job nodes]
        self.r = rewards            # job nodes
        self.b = benefits           # [worker][role][job_node]
        self.t = travel_times       # all nodes
        self.M = M
        
        
    def to_dict(self):
        return {'num_workers':self.num_workers, 'num_roles':self.num_roles, 'num_nodes':self.num_nodes, 
                'w':self.w, 'p':self.p, 'e':self.e, 'd':self.d, 'r':self.r, 'b':self.b, 't':self.t, 'M':self.M}
    
    def to_json_file(self, output_filename):
        with open(output_filename, 'w') as outfile:
            json.dump(self.to_dict(), outfile)
    
    def from_dict(self, dct):
        self.num_workers = dct['num_workers']
        self.num_roles = dct['num_roles']
        self.num_nodes = dct['num_nodes']
        self.w = dct['w']
        self.p = dct['p']
        self.e = dct['e']
        self.d = dct['d']
        self.r = dct['r']
        self.b = dct['b']
        self.t = dct['t']
        self.M = dct['M']
        
    def from_json_file(self, input_filename):
        with open(input_filename, 'r') as infile:
            self.from_dict(json.load(infile))

    def to_opl(self):
        s = 'M = ' + str(self.M) + ";\n"
        s += 'numWorkers = ' + str(self.num_workers) + ";\n"
        s += 'numRoles = ' + str(self.num_roles) + ";\n"
        s += 'numNodes = ' + str(self.num_nodes) + ";\n"
        s += 'wStart = ' + str([w[0] for w in self.w]) + ";\n"
        s += 'wEnd = ' + str([w[1] for w in self.w]) + ";\n"
        s += 'p = ' + str(self.p) + ";\n"
        s += 'e = ' + str(self.e) + ";\n"
        s += 'd = ' + str(self.d) + ";\n"
        s += 'r = ' + str(self.r) + ";\n"
        s += 'b = ' + str(self.b) + ";\n"
        s += 't = ' + str(self.t) + ";\n"
        return s
        
    def to_opl_file(self, output_filename):
        with open(output_filename, 'w') as outfile:
            outfile.write(self.to_opl())
