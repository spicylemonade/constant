import numpy as np
import time

def beam_search_lcs(N=10000, W=100):
    np.random.seed(42)
    # Generate two random binary strings
    X = np.random.randint(0, 2, N, dtype=np.int8)
    Y = np.random.randint(0, 2, N, dtype=np.int8)
    
    # Beam search state: dict mapping (i, j) to max length
    # Actually, we can just keep a set of active (i, j) and advance them.
    # To maximize length, state is (i, j), value is L.
    # It's better to process by L!
    # For each L, what are the best (i, j) pairs (minimum i+j)?
    
    # Active states: list of (i, j) for a given L
    # We want to minimize i+j. So we keep the top W states with smallest i+j.
    active = {(0, 0)} # (i, j)
    
    L = 0
    while active:
        next_active = set()
        for (i, j) in active:
            # We want to find the NEXT match.
            # Look ahead to find the next 0 and 1 in X and Y
            # Instead of a full search, just scan up to say 20 characters
            # to find the next match of '0' and '1'
            
            # Find next 0 in X
            i0 = i
            while i0 < N and X[i0] != 0: i0 += 1
            j0 = j
            while j0 < N and Y[j0] != 0: j0 += 1
            if i0 < N and j0 < N:
                next_active.add((i0 + 1, j0 + 1))
                
            # Find next 1 in X
            i1 = i
            while i1 < N and X[i1] != 1: i1 += 1
            j1 = j
            while j1 < N and Y[j1] != 1: j1 += 1
            if i1 < N and j1 < N:
                next_active.add((i1 + 1, j1 + 1))
                
        if not next_active:
            break
            
        L += 1
        
        # Prune next_active
        if len(next_active) > W:
            # Sort by i+j
            sorted_next = sorted(list(next_active), key=lambda x: x[0] + x[1])
            next_active = set(sorted_next[:W])
            
        active = next_active
        
    print(f"LCS length for N={N}, W={W}: {L}")
    print(f"Ratio: {L/N:.6f}")
    return L/N

if __name__ == "__main__":
    t0 = time.time()
    beam_search_lcs(10000, 100)
    print(f"Time: {time.time()-t0:.2f}s")
