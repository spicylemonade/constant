import numpy as np

def run_test():
    np.random.seed(42)
    N = 100
    W = 1
    X = np.random.randint(0, 2, N, dtype=np.int8)
    Y = np.random.randint(0, 2, N, dtype=np.int8)
    
    active = {(0, 0)}
    
    L = 0
    while active:
        if L == 1:
            print("Py L=1:", sorted(list(active)))
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
            # stable sort by sum, then by i to break ties
            sorted_next = sorted(list(next_active), key=lambda x: (x[0] + x[1], x[0]))
            next_active = set(sorted_next[:W])
        active = next_active
    print("Python L:", L)

run_test()
