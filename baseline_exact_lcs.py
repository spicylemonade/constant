"""
Exact expected LCS computation for short binary strings.

Computes E[LCS(X_n, Y_n)] exactly for uniformly random binary strings of
length n, using DP over the frontier (row difference representation).
Practical for n <= 12 in pure Python.

Usage:
    python baseline_exact_lcs.py [n]

Verified: n=8 yields E[LCS] = 5.4691162109375 (ratio 0.683640).
"""
import sys

def get_next_frontier(frontier, x, y_char):
    # frontier is a tuple of n integers (the DP row)
    # Actually, it's better to store the differences. diff[i] = DP[i] - DP[i-1] in {0, 1}
    # frontier is a bit-tuple of length n.
    n = len(x)
    new_frontier = [0] * n
    # We can compute the new row using the standard DP:
    # DP[i, j] = DP[i-1, j-1] + 1 if X[i] == Y[j]
    # else max(DP[i-1, j], DP[i, j-1])
    # Let DP[i] be the previous row. DP[0] is the current row.
    
    dp_prev = 0
    dp_curr_j_minus_1 = 0
    new_diffs = []
    
    for i in range(n):
        dp_i_prev = dp_prev + frontier[i]
        
        if x[i] == y_char:
            dp_curr = dp_prev + 1
        else:
            dp_curr = max(dp_i_prev, dp_curr_j_minus_1)
            
        new_diffs.append(dp_curr - dp_curr_j_minus_1)
        dp_prev = dp_i_prev
        dp_curr_j_minus_1 = dp_curr
        
    return tuple(new_diffs)

def expected_lcs_for_X(x):
    n = len(x)
    # state: (frontier_diffs) -> probability
    initial_frontier = tuple([0] * n)
    state_probs = {initial_frontier: 1.0}
    
    for step in range(n):
        new_state_probs = {}
        for frontier, p in state_probs.items():
            for y_char in (0, 1):
                nf = get_next_frontier(frontier, x, y_char)
                new_state_probs[nf] = new_state_probs.get(nf, 0.0) + p * 0.5
        state_probs = new_state_probs
        
    expected_val = 0.0
    for frontier, p in state_probs.items():
        expected_val += p * sum(frontier)
    return expected_val

def exact_expected_lcs(n):
    if n == 0: return 0.0
    total_expected = 0.0
    # Average over all X
    for i in range(1 << n):
        x = tuple((i >> j) & 1 for j in range(n))
        total_expected += expected_lcs_for_X(x)
        
    return total_expected / (1 << n)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"Exact expected LCS for n={n}: {exact_expected_lcs(n)}")
