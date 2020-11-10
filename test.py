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

def ultima(s):
    time.sleep(1)
    return s

#We can also wrap function calls
res = timerdec_always()(ultima)("Bye!")

print(res)
