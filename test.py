from timerdec.decorators import timerdec, timerdec_always
import time
import numpy as np

@timerdec()
def r(size1, size2):
    return np.random.rand(size1, size2)

class cl():
    def __init__(self):
        pass

    @timerdec(progress=True)
    def f(self):
        a = r(1000, 1000)
        time.sleep(0.2)
        b = r(1000, 1000)
        time.sleep(0.2)
        c = np.dot(a,b)

    @timerdec_always(1000)
    def dummy(self, a):
        pass

c = cl()

c.f()
c.dummy(a="dummy data")

