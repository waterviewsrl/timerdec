import os
import timeit
import statistics
import atexit
from tqdm import tqdm
import psutil
from inspect import getframeinfo, stack


from .shared_data import prev_runs, reference_start

from .snapshots import now


def nowdec(enabled=True):

    def decorator(func):

        def wrapper(*args, **kwargs):
            caller = getframeinfo(stack()[1][0])
            now(None, enabled, caller.function, level=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def timerdec(reps=os.getenv('TIMERDEC_REPS', 4), rerun=os.getenv('TIMERDEC_RERUN', 'true'), always=os.getenv('TIMERDEC_ALWAYS', 'false'), progress=False, verbose=False):
    """A decorator for measuring method execution time statistics

    Args:
        reps ([int], optional): Number of repetitions. Defaults to os.getenv('TIMERDEC_REPS', 4).
        rerun (string, optional): Controls rerun of the measurement if the method is called many times. 'true' for True, 'false' for False. Defaults to os.getenv('TIMERDEC_RERUN', 'true').
        always (string, optional): Controls if the decorator has to be executed anyway, or should be requested at runtime. 'true' for True, 'false' for False. Defaults to os.getenv('TIMERDEC_ALWAYS', 'false').
        progress (bool, optional): Draw a progress bar. Defaults to False.
    """

    p = psutil.Process()

    def decorator(func):
        # Define the progress bar, if requested
        def progressbar(a):
            return tqdm(a) if progress else a

        class WrapperContext(object):
            def __init__(self, func, reps):
                self.func = func
                self.reps = reps

            def __enter__(self):
                return self.func, progressbar(range(self.reps))

            def __exit__(self, type, value, traceback):
                if verbose:
                    datadump()

        # Build the list of methods requested for measurment at runtime
        check = os.getenv('TIMERDEC_METHODS', None)
        check = check.split(';') if check else None
        if (check and func.__qualname__ in check) or always == 'true':
            # Register callback for measurments printing at exit
            def datadump():
                if (len(data['time']) > 0):
                    avg = statistics.mean(data['time'])
                    std = statistics.variance(data['time']) if len(
                        data['time']) > 1 else 0
                    avg_usr = statistics.mean(data['usr'])
                    avg_sys = statistics.mean(data['sys'])
                    avg_usr_child = statistics.mean(data['usr_child'])
                    avg_sys_child = statistics.mean(data['sys_child'])
                    print("Avg time and std dev (usr, sys, usr_child, sys_child) for method {0}: {1:.2E} {2:.2E} ({3:.2E}, {4:.2E} {5:.2E}, {6:.2E}). Reps: {7}".format(
                        func.__qualname__.ljust(25), avg, std, avg_usr, avg_sys, avg_usr_child, avg_sys_child, data['cnt']))
                else:
                    print("Method {0} was never called".format(
                        func.__qualname__))

            @atexit.register
            def final():
                datadump()
            data = {}
            data['time'] = []
            data['usr'] = []
            data['sys'] = []
            data['usr_child'] = []
            data['sys_child'] = []
            data['cnt'] = 0
            data['runs'] = 0

            # Real Wrapper
            def wrapper(*args, **kwargs):
                # Check if should rerun

                if (data['runs'] == 0 or rerun == 'true'):
                    with WrapperContext(func, reps) as (wrap, iterator):
                        data['runs'] = data['runs'] + 1
                        # Loop over reps
                        for i in iterator:
                            ct = p.as_dict(attrs=['cpu_times'])['cpu_times']
                            usr_start = ct.user
                            usr_child_start = ct.children_user
                            sys_start = ct.system
                            sys_child_start = ct.children_system
                            start = timeit.default_timer()
                            res = wrap(*args, **kwargs)
                            end = timeit.default_timer()
                            ct = p.as_dict(attrs=['cpu_times'])['cpu_times']
                            usr_end = ct.user
                            usr_child_end = ct.children_user
                            sys_end = ct.system
                            sys_child_end = ct.children_system
                            data['time'].append(end - start)
                            data['usr'].append(usr_end - usr_start)
                            data['usr_child'].append(
                                usr_child_end - usr_child_start)
                            data['sys'].append(sys_end - sys_start)
                            data['sys_child'].append(
                                sys_child_end - sys_child_start)
                            data['cnt'] = data['cnt'] + 1
                else:
                    res = func(*args, **kwargs)
                return res
            return wrapper
        else:
            # Dummy wrapper, if method was not requested at runtime
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                return res
            return wrapper
    return decorator


def timerdec_always(reps=os.getenv('TIMERDEC_REPS', 4), rerun=os.getenv('TIMERDEC_RERUN', 'true')):
  # Always measure
    return timerdec(reps, rerun, 'true')
