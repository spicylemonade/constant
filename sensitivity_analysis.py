"""
Hyperparameter sensitivity analysis for beam-search LCS heuristic.
Tests configurations: W={50, 100, 200}, N={500, 1000, 2000}.
Uses M=10,000 trials per config for tractability, plus reference from M=1M run.
"""
import numpy as np
import time
import math
import json
import sys
import os

sys.path.insert(0, "results/concept_evolve/tree/005_subadditive_martingale_tilted")
from block_evaluator import run_monte_carlo_beam

# Warmup JIT
print("JIT warmup...")
run_monte_carlo_beam(10, 5, 2)

configs = [
    {"N": 500,  "W": 50,  "M": 10000},
    {"N": 500,  "W": 100, "M": 10000},
    {"N": 500,  "W": 200, "M": 10000},
    {"N": 1000, "W": 50,  "M": 10000},
    {"N": 1000, "W": 100, "M": 10000},
    {"N": 1000, "W": 200, "M": 10000},
    {"N": 2000, "W": 50,  "M": 10000},
    {"N": 2000, "W": 100, "M": 10000},
    {"N": 2000, "W": 200, "M": 10000},
]

results = []
delta = 1e-12

for cfg in configs:
    N, W, M = cfg["N"], cfg["W"], cfg["M"]
    print(f"\nRunning N={N}, W={W}, M={M}...")
    t0 = time.time()
    lcs = run_monte_carlo_beam(N, W, M)
    elapsed = time.time() - t0

    ratio = lcs.astype(np.float64) / N
    emp_mean = float(ratio.mean())
    emp_std = float(ratio.std())
    hoeffding_margin = math.sqrt(math.log(1/delta) / (2 * M))
    provable_lb = emp_mean - hoeffding_margin

    row = {
        "N": N, "W": W, "M": M,
        "empirical_ratio": round(emp_mean, 8),
        "std": round(emp_std, 8),
        "hoeffding_margin": round(hoeffding_margin, 8),
        "provable_lower_bound": round(provable_lb, 8),
        "time_s": round(elapsed, 2),
    }
    results.append(row)
    print(f"  ratio={emp_mean:.6f}  std={emp_std:.6f}  provable_lb={provable_lb:.6f}  time={elapsed:.1f}s")

# Add the reference M=1M run
results.append({
    "N": 1000, "W": 100, "M": 1000000,
    "empirical_ratio": 0.80341686,
    "std": 0.00685680,
    "hoeffding_margin": round(math.sqrt(math.log(1/delta) / (2 * 1000000)), 8),
    "provable_lower_bound": 0.79969994,
    "time_s": 2619.28,
    "note": "reference run from raw_trials.npy"
})

out_path = "results/sensitivity_analysis.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved results to {out_path}")

# Print summary table
print(f"\n{'N':>6} {'W':>6} {'M':>10} {'ratio':>10} {'std':>10} {'provable_lb':>12}")
print("-" * 60)
for r in results:
    print(f"{r['N']:>6} {r['W']:>6} {r['M']:>10} {r['empirical_ratio']:>10.6f} {r['std']:>10.6f} {r['provable_lower_bound']:>12.6f}")
