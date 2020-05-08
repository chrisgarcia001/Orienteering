# This script generates the problems in this vignette.

import os
import sys
sys.path.insert(1, '../../../core')

import json
from structs import *
from problem_gen import *
from algorithms import *
from algorithm_runner import *

param_folder = './pgen_params'

for filename in [x for x in os.listdir(param_folder) if x.endswith('json')]:
    params = {}
    with open(os.path.join(param_folder, filename), 'r') as infile:
        params = json.load(infile)
    pg = ProblemSetGenerator(params)
    pg.generate()