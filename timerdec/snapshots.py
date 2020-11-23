import timeit
from inspect import getframeinfo, stack

from .shared_data import prev_runs, reference_start


def now(label=None, enabled=True, funcname=None, level=1):
    caller = getframeinfo(stack()[level][0])
    funcname = funcname if funcname else caller.function
    if label == None:
        label = '{0}:{1}:{2}'.format(
            caller.filename.split('/')[-1], caller.lineno, funcname)
    reference_new = timeit.default_timer()
    delta = reference_new - reference_start
    delta_self = prev_runs.get(funcname, None)
    if delta_self:
        delta_self = reference_new - delta_self
    prev_runs[funcname] = reference_new
    if enabled:
        if delta_self:
            print('Time at {0}: {1:.5E}. Since previous call to self: {2:.5E}'.format(
                label.ljust(25), delta, delta_self))
        else:
            print('Time at {0}: {1:.5E}.'.format(
                label.ljust(25), delta))
