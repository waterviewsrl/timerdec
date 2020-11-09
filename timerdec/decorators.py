import os
import timeit
import statistics
import atexit


def timerdec(reps=os.getenv('TIMERDEC_REPS', 4), rerun=os.getenv('TIMERDEC_RERUN', 'true'), always=os.getenv('TIMERDEC_ALWAYS', 'false')):
  def decorator(func):
    check = os.getenv('TIMERDEC_METHODS', None)
    check = check.split(';') if check else None
    if (check and func.__qualname__ in check) or always == 'true':
     @atexit.register
     def final():
       if (len(data['times']) > 0):
         avg = statistics.mean(data['times'])
         std = statistics.variance(data['times']) if len(data['times']) > 1 else 0
         print("Average time and variance for method {0}: {1} {2}. Total numer of reps: {3}".format(func.__qualname__, avg, std, data['cnt']))
       else:
         print("Method {0} was never called".format(func.__qualname__))
     data = {}
     data['times'] = []
     data['cnt'] = 0
     data['runs'] = 0
     def wrapper(*args, **kwargs):
      if (data['runs'] == 0 or rerun == 'true'):
        data['runs'] = data['runs'] + 1
        for i in range(reps):
            start = timeit.default_timer()
            res = func(*args, **kwargs)
            end = timeit.default_timer()
            data['times'].append(end - start)
            data['cnt'] = data['cnt']  + 1
      else:
        res = func(*args, **kwargs)
      return res
     return wrapper
    else:
     def wrapper(*args, **kwargs):
       res = func(*args, **kwargs)
       return res
     return wrapper
  return decorator

def timerdec_always(reps=os.getenv('TIMERDEC_REPS', 4), rerun=os.getenv('TIMERDEC_RERUN', 'true')):
    return timerdec(reps, rerun, 'true')

