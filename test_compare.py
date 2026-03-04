import numpy as np
from numba import njit

@njit
def nb_beam(X, Y, N, W):
    active_packed = np.zeros(1, dtype=np.int64)
    active_packed[0] = 0
    L = 0
    while True:
        K_len = len(active_packed)
        next_packed = np.empty(K_len * 2, dtype=np.int64)
        next_len = 0
        for k in range(K_len):
            p = active_packed[k]
            i = p // (N + 1)
            j = p % (N + 1)
            
            i0, j0 = i, j
            while i0 < N and X[i0] != 0: i0 += 1
            while j0 < N and Y[j0] != 0: j0 += 1
            if i0 < N and j0 < N:
                next_packed[next_len] = (i0 + 1) * (N + 1) + (j0 + 1)
                next_len += 1
                
            i1, j1 = i, j
            while i1 < N and X[i1] != 1: i1 += 1
            while j1 < N and Y[j1] != 1: j1 += 1
            if i1 < N and j1 < N:
                next_packed[next_len] = (i1 + 1) * (N + 1) + (j1 + 1)
                next_len += 1
                
        if next_len == 0: break
        L += 1
        sorted_next = np.sort(next_packed[:next_len])
        unique_len = 1
        unique_packed = np.empty(next_len, dtype=np.int64)
        unique_packed[0] = sorted_next[0]
        for k in range(1, next_len):
            if sorted_next[k] != sorted_next[k-1]:
                unique_packed[unique_len] = sorted_next[k]
                unique_len += 1
                
        if unique_len > W:
            sums = np.empty(unique_len, dtype=np.int64)
            for k in range(unique_len):
                p = unique_packed[k]
                i = p // (N + 1)
                j = p % (N + 1)
                sums[k] = (i + j) * (N + 1) + abs(i - j)
            sorted_idx = np.argsort(sums)
            active_packed = np.empty(W, dtype=np.int64)
            for k in range(W):
                active_packed[k] = unique_packed[sorted_idx[k]]
        else:
            active_packed = unique_packed[:unique_len].copy()
    return L

def py_beam(X, Y, N, W):
    active = {(0, 0)}
    L = 0
    while active:
        next_active = set()
        for (i, j) in active:
            i0, j0 = i, j
            while i0 < N and X[i0] != 0: i0 += 1
            while j0 < N and Y[j0] != 0: j0 += 1
            if i0 < N and j0 < N: next_active.add((i0 + 1, j0 + 1))
            
            i1, j1 = i, j
            while i1 < N and X[i1] != 1: i1 += 1
            while j1 < N and Y[j1] != 1: j1 += 1
            if i1 < N and j1 < N: next_active.add((i1 + 1, j1 + 1))
                
        if not next_active: break
        L += 1
        if len(next_active) > W:
            next_active = set(sorted(list(next_active), key=lambda x: (x[0] + x[1], abs(x[0]-x[1])))[:W])
        active = next_active
    return L

def test():
    np.random.seed(42)
    N = 10000
    W = 100
    X = np.random.randint(0, 2, N, dtype=np.int8)
    Y = np.random.randint(0, 2, N, dtype=np.int8)
    
    L_nb = nb_beam(X, Y, N, W)
    L_py = py_beam(X, Y, N, W)
    print("NB:", L_nb, "PY:", L_py)
    
test()
