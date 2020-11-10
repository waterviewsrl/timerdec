import os
import timeit
import statistics
import atexit
from tqdm import tqdm


def timerdec(reps=os.getenv('TIMERDEC_REPS', 4), rerun=os.getenv('TIMERDEC_RERUN', 'true'), always=os.getenv('TIMERDEC_ALWAYS', 'false'), progress=False):
    """A decorator for measuring method execution time statistics

    Args:
        reps ([int], optional): Number of repetitions. Defaults to os.getenv('TIMERDEC_REPS', 4).
        rerun (string, optional): Controls rerun of the measurement if the method is called many times. 'true' for True, 'false' for False. Defaults to os.getenv('TIMERDEC_RERUN', 'true').
        always (string, optional): Controls if the decorator has to be executed anyway, or should be requested at runtime. 'true' for True, 'false' for False. Defaults to os.getenv('TIMERDEC_ALWAYS', 'false').
        progress (bool, optional): Draw a progress bar. Defaults to False.
    """
    def decorator(func):
        # Define the progress bar, if requested
        def progressbar(a):
            return tqdm(a) if progress else a
        # Build the list of methods requested for measurment at runtime
        check = os.getenv('TIMERDEC_METHODS', None)
        check = check.split(';') if check else None
        if (check and func.__qualname__ in check) or always == 'true':
            # Register callback for measurments printing at exit
            @atexit.register
            def final():
                if (len(data['times']) > 0):
                    avg = statistics.mean(data['times'])
                    std = statistics.variance(data['times']) if len(
                        data['times']) > 1 else 0
                    print("Average time and variance for method {0}: {1} {2}. Total numer of reps: {3}".format(
                        func.__qualname__, avg, std, data['cnt']))
                else:
                    print("Method {0} was never called".format(
                        func.__qualname__))
            data = {}
            data['times'] = []
            data['cnt'] = 0
            data['runs'] = 0
            # Real Wrapper

            def wrapper(*args, **kwargs):
                # Check if should rerun
                if (data['runs'] == 0 or rerun == 'true'):
                    data['runs'] = data['runs'] + 1
                    # Loop over reps
                    for i in progressbar(range(reps)):
                        start = timeit.default_timer()
                        res = func(*args, **kwargs)
                        end = timeit.default_timer()
                        data['times'].append(end - start)
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
