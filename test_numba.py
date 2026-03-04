from numba import njit
import numpy as np

@njit
def test():
    X = np.random.randint(0, 2, 10)
    print(X)
test()
