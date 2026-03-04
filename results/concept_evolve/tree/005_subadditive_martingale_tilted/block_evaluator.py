import numpy as np
import time
import math
import json
from numba import njit, prange

@njit
def run_single_trial(N, W):
    X = np.random.randint(0, 2, N).astype(np.int8)
    Y = np.random.randint(0, 2, N).astype(np.int8)
    
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

@njit(parallel=True)
def run_monte_carlo_beam(N, W, M):
    lcs_results = np.zeros(M, dtype=np.int32)
    for m in prange(M):
        lcs_results[m] = run_single_trial(N, W)
    return lcs_results

def main():
    N = 1000
    W = 100
    M = 1000000
    
    print("JIT compilation warmup...")
    run_monte_carlo_beam(10, 5, 2)
    
    print(f"Running M={M} trials for N={N}, W={W}...")
    t0 = time.time()
    lcs_results = run_monte_carlo_beam(N, W, M)
    elapsed = time.time() - t0
    print(f"Finished in {elapsed:.2f}s")
    
    mean_lcs = np.mean(lcs_results)
    empirical_ratio = mean_lcs / N
    
    delta = 1e-12
    hoeffding_error = N * math.sqrt(math.log(1/delta) / (2 * M))
    hoeffding_ratio_error = hoeffding_error / N
    
    provable_lower_bound = empirical_ratio - hoeffding_ratio_error
    
    print(f"Empirical mean LCS per block: {mean_lcs:.2f}")
    print(f"Empirical ratio: {empirical_ratio:.6f}")
    print(f"Hoeffding 99.9999999999% confidence margin: {hoeffding_ratio_error:.6f}")
    print(f"PROVABLE LOWER BOUND: {provable_lower_bound:.6f}")
    
    results = {
        "N": N,
        "W": W,
        "M": M,
        "empirical_mean": float(mean_lcs),
        "empirical_ratio": float(empirical_ratio),
        "hoeffding_margin": float(hoeffding_ratio_error),
        "provable_lower_bound": float(provable_lower_bound),
        "time_s": float(elapsed)
    }
    
    with open("results/concept_evolve/tree/005_subadditive_martingale_tilted/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
