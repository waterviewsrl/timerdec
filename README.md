# timerdec
Simple decorators for measuring Python methods execution time. 
Methods are called a configurable number of times (4 by default), and statistics are printed at the end of execution.

## API

There are two decorators available, timerdec and timerdec_always. The difference between the two is that timerdec_always is always executed, while timerdec is executed only if a decorated method is specifically requested at runtime by setting the TIMERDEC_METHODS environment variable as explained below.

### Code Example

```python
from timerdec.decorators import timerdec, timerdec_always
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
        time.sleep(0.2)
        b = r(1000, 1000)
        time.sleep(0.2)
        c = np.dot(a,b)

    #Timing information will always be collected for this method. Method is run 1000 times
    @timerdec_always(1000)
    def dummy(self, a):
        pass

c = cl()

c.f()
c.dummy(a="dummy data")
```

### Execution and Configuration

If no environment variable is set, timerdec will collect information only for the methods decorated with timerdec_always.
``` shell
python3 test.py
```
which outputs:
```
Average time and variance for method cl.dummy: 1.48697174154222e-07 2.5282403906653095e-14. Total numer of reps: 1000
```

The TIMERDEC_METHODS can be set including a list of semicolon separated method names.
``` shell
TIMERDEC_METHODS="cl.f;r"   python3 test.py
```
```
100%|██████████████████████████████████████████████████████████████████████████████| 4/4 [00:04<00:00,  1.04s/it]
Average time and variance for method cl.dummy: 1.962226815521717e-07 2.0575390157789076e-12. Total numer of reps: 1000
Average time and variance for method cl.f: 1.0413964999606833 0.00014622954992246043. Total numer of reps: 4
Average time and variance for method r: 0.009776858667464694 2.8456450978724894e-05. Total numer of reps: 32

```

To avoid benchmarking the same method many times, set the variable TIMERDEC_RERUN to false:
``` shell
TIMERDEC_METHODS="cl.f;r" TIMERDEC_RERUN=false   python3 test.py
```
```
100%|███████████████████████████████████████████████████████████████████████████████| 4/4 [00:04<00:00,  1.02s/it]
Average time and variance for method cl.dummy: 2.154293470084667e-07 1.7538931690329252e-12. Total numer of reps: 1000
Average time and variance for method cl.f: 1.0227295864897314 0.00067336464983955. Total numer of reps: 4
Average time and variance for method r: 0.01273957351804711 3.958873168578572e-05. Total numer of reps: 4

```
