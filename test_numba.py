"""
Simple Numba installation verification test.

Confirms that Numba JIT compilation works correctly in the current
environment by compiling and running a trivial random-number generation.

Usage:
    python test_numba.py
"""
from numba import njit
import numpy as np

@njit
def test():
    X = np.random.randint(0, 2, 10)
    print(X)

if __name__ == "__main__":
    test()
