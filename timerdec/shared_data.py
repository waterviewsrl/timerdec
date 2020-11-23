import timeit

def init():
    global reference_start
    global prev_runs
    reference_start = timeit.default_timer()
    prev_runs={}