from algorithms import *

def print_iteneraries(problem, assignments):
    print("\nWORKER ITENERARIES:")
    for w in range(problem.num_workers):  
        it = []
        for j, start, asmts in assignments:
            for x, a, r in asmts:
                if x == w:
                    it.append({'job':j, 'window':(round(problem.w[j][0], 2), round(problem.w[j][1], 2)), 'arrive':round(a, 2), 
                               'assigned':r, 'start':round(start, 2), 'leave':round(problem.p[j] + start, 2)})
        it = sorted(it, key=lambda x: x['arrive'])
        for i in range(len(it)):
            if i == len(it) - 1:
                it[i]['travel'] = round(problem.t[it[i]['job']][problem.num_nodes - 1], 2)
            else:
                it[i]['travel'] = round(problem.t[it[i]['job']][it[i + 1]['job']], 2)
        print('  Worker ' + str(w) + ' Itenerary: ')
        for i in it:
            print('   ' + str(i))
        

def print_solution(encoded_solution, problem):
    print('Num Job Nodes: ' + str(problem.num_nodes - 2))
    sol = construct_solution(problem, encoded_solution)
    print('Num Selected Job Nodes: ' + str(len(sol['assignments'])))
    print('Selected Node Vector: ' + str([1 if x in [a[0] for a in sol['assignments']] else 0 for x in range(1, problem.num_nodes - 1)]))
    print('Selected Nodes: ' + str([a[0] for a in sol['assignments']]))
    print_iteneraries(problem, sol['assignments'])
    