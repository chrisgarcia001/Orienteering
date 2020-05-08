jruby batch_oplrun.rb ./models/multiskill-dynamic-team-orientering-V0.1-timelimit.mod ./problems/opl  ./solutions/cplex
jruby ilog_output_summarizer.rb ./solutions/cplex
pypy3 alns_runner.py
pypy3 ls_runner.py