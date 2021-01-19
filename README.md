# timerdec
Simple decorators for measuring Python methods execution time. 
Methods are called a configurable number of times (4 by default), and statistics are printed at the end of execution.

## API

### Decorators

There are two decorators available, timerdec and timerdec_always. The difference between the two is that timerdec_always is always executed, while timerdec is executed only if a decorated method is specifically requested at runtime by setting the TIMERDEC_METHODS environment variable as explained below.

#### Decorators Code Example

```python
from timerdec.decorators import timerdec, timerdec_always, nowdec
from timerdec.snapshots import now
import time
import numpy as np

#We can require timing information collection for function r at run time.
@timerdec()
def r(size1, size2):
    return np.random.rand(size1, size2)

class cl():
    def __init__(self):
        pass
        
    #We can require timing information collection for method f at run time. A progress bar will be printed
    
    @timerdec(progress=True)
    def f(self):
        a = r(1000, 1000)
        b = r(1000, 1000)
        c = np.dot(a,b)

    #Timing information will always be collected for this method. Method is run 1000 times
    @timerdec_always(1000)
    def dummy(self, a):
        pass

c = cl()

def do():
    c.f()
    c.dummy(a="dummy data")

now('before do')
do()
now('after do')


def ultima(s):
    time.sleep(1)
    return s



#We can also wrap function calls
res1 = timerdec_always()(ultima)("Hello!")
print(res1)

#Subsequent calls of functions with inline (non decorator) wrapping will not be object of measures
res2 = ultima('Bye!')
print(res2)

vec = np.zeros((1000,1000))

now()

#It is possible to inline wrap object methods as well
res3 =  timerdec_always()(vec.astype)(np.uint8)

now()


```

#### Execution and Configuration

On execution, statistics are collected and results are printed at the end of execution. Fore each measured methid there will be a line containin wall clock time average and variance, user, system, children user and children system time. 

If no environment variable is set, timerdec will collect information only for the methods decorated with timerdec_always.
``` shell
python3 test.py
```
which outputs:
```
Avg time and std dev (usr, sys, usr_child, sys_child) for method ndarray.astype           : 1.33E-03 4.33E-06 (2.50E-03, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method ultima                   : 1.00E+00 2.21E-07 (0.00E+00, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method cl.dummy                 : 2.54E-07 3.38E-15 (2.00E-05, 0.00E+00 0.00E+00, 0.00E+00). Reps: 1000

```

The TIMERDEC_METHODS can be set including a list of semicolon separated method names.
``` shell
TIMERDEC_METHODS="cl.f;r"   python3 test.py
```
```
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:04<00:00,  1.04s/it]
Avg time and std dev (usr, sys, usr_child, sys_child) for method ndarray.astype           : 8.41E-04 4.00E-07 (0.00E+00, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method ultima                   : 1.00E+00 8.45E-09 (0.00E+00, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method cl.dummy                 : 3.12E-07 4.43E-14 (3.00E-05, 0.00E+00 0.00E+00, 0.00E+00). Reps: 1000
Avg time and std dev (usr, sys, usr_child, sys_child) for method cl.f                     : 6.21E-01 1.91E-04 (5.97E-01, 2.00E-02 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method r                        : 8.21E-03 2.43E-05 (6.25E-03, 2.50E-03 0.00E+00, 0.00E+00). Reps: 32


```

To avoid benchmarking the same method many times, set the variable TIMERDEC_RERUN to false:
``` shell
TIMERDEC_METHODS="cl.f;r" TIMERDEC_RERUN=false   python3 test.py
```
```
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:04<00:00,  1.04s/it]
Avg time and std dev (usr, sys, usr_child, sys_child) for method ndarray.astype           : 8.41E-04 4.00E-07 (0.00E+00, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method ultima                   : 1.00E+00 8.45E-09 (0.00E+00, 0.00E+00 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method cl.dummy                 : 3.12E-07 4.43E-14 (3.00E-05, 0.00E+00 0.00E+00, 0.00E+00). Reps: 1000
Avg time and std dev (usr, sys, usr_child, sys_child) for method cl.f                     : 6.21E-01 1.91E-04 (5.97E-01, 2.00E-02 0.00E+00, 0.00E+00). Reps: 4
Avg time and std dev (usr, sys, usr_child, sys_child) for method r                        : 8.21E-03 2.43E-05 (6.25E-03, 2.50E-03 0.00E+00, 0.00E+00). Reps: 32


```


### Snapshots

To evaluate the time taken btween two points in the code, the now() method in module timerdec.snapshots is provided.

```python
import time
from timerdec.snapshots import now

def do():
    now()
    time.sleep(3)
    now()

do()

```

Will print time from startup and from previous call to now itself:

```python
Time at <stdin>:2:do             : 3.41271E+01.
Time at <stdin>:4:do             : 3.71351E+01. Since previous call to self: 3.00798E+00

```


