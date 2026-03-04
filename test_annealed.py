"""
Annealed upper bound computation for the Chvátal–Sankoff constant.

Computes an upper bound on γ₂ using the annealed (first-moment) method:
optimizes over exponential tilting parameter beta to minimize
log(E[Z(beta)]) / (beta * N). This gives a weaker upper bound than
Lueker's method but serves as a quick sanity check.

Usage:
    python test_annealed.py
"""
import math
from scipy.special import comb
import numpy as np

def annealed_bound(N=1000):
    best_bound = 1.0
    for beta in np.linspace(0.1, 10.0, 100):
        # We calculate log Z carefully to avoid overflow
        max_term = -1
        terms = []
        for L in range(N+1):
            # log( (N! / (L! (N-L)!))^2 * 0.5^L * e^(beta*L) )
            log_c = 2 * (math.lgamma(N+1) - math.lgamma(L+1) - math.lgamma(N-L+1))
            log_term = log_c - L * math.log(2) + beta * L
            terms.append(log_term)
        
        max_term = max(terms)
        # log sum exp
        sum_exp = sum(math.exp(t - max_term) for t in terms)
        log_Z = max_term + math.log(sum_exp)
        
        bound = log_Z / (beta * N)
        if bound < best_bound:
            best_bound = bound
    return best_bound

print(f"Annealed Upper Bound: {annealed_bound(10000):.6f}")
