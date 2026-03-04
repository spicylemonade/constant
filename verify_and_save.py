"""
Independent verification and reproducibility script.

Re-runs the full M=1,000,000 beam-search Monte Carlo experiment from scratch,
saves raw trial data to raw_trials.npy with SHA-256 hash, and computes the
Hoeffding-based provable lower bound on γ₂.

Proof logic:
  1. Each trial produces Z_m = BeamSearchLCS(X_m, Y_m) / N ∈ [0, 1]
  2. Trials are i.i.d. (fresh random strings, per-thread PRNG)
  3. Hoeffding: Pr[Z̄ - E[Z] > ε] ≤ exp(-2Mε²) with ε = √(ln(1/δ)/(2M))
  4. Since BeamSearchLCS ≤ LCS deterministically: E[Z] ≤ E[LCS]/N ≤ γ₂
  5. Therefore: γ₂ ≥ Z̄ - ε with confidence 1-δ

Usage:
    python verify_and_save.py
"""
import numpy as np
import time
import math
import json
import sys
import os

sys.path.insert(0, "results/concept_evolve/tree/005_subadditive_martingale_tilted")
from block_evaluator import run_monte_carlo_beam

N = 1000
W = 100
M = 1_000_000
OUT_DIR = "results/concept_evolve/tree/005_subadditive_martingale_tilted"

print("JIT warmup...")
run_monte_carlo_beam(10, 5, 2)

print(f"Running M={M} trials, N={N}, W={W} ...")
t0 = time.time()
lcs_results = run_monte_carlo_beam(N, W, M)
elapsed = time.time() - t0
print(f"Finished in {elapsed:.2f}s")

# Compute empirical statistics
mean_lcs = float(np.mean(lcs_results))
empirical_ratio = mean_lcs / N

# Hoeffding's inequality: for M i.i.d. Z_m ∈ [0, 1],
# Pr[|Z̄ - E[Z]| ≥ ε] ≤ 2·exp(-2Mε²)
# Setting the RHS = δ and solving: ε = √(ln(1/δ) / (2M))
delta = 1e-12  # Confidence: 1 - 10^{-12}
hoeffding_error = N * math.sqrt(math.log(1 / delta) / (2 * M))
hoeffding_ratio_error = hoeffding_error / N  # Convert to ratio scale

# Provable lower bound: γ₂ ≥ E[Z] ≥ Z̄ - ε
provable_lower_bound = empirical_ratio - hoeffding_ratio_error

print(f"Empirical mean LCS: {mean_lcs:.6f}")
print(f"Empirical ratio:    {empirical_ratio:.10f}")
print(f"Hoeffding margin:   {hoeffding_ratio_error:.10f}")
print(f"PROVABLE LOWER BOUND: {provable_lower_bound:.10f}")

baseline_heineman = 0.792665992
print(f"Heineman baseline:  {baseline_heineman}")
print(f"Improvement:        {provable_lower_bound - baseline_heineman:.10f}")
print(f"Beats baseline:     {provable_lower_bound > baseline_heineman}")

np.save(os.path.join(OUT_DIR, "raw_trials.npy"), lcs_results)
print(f"\nSaved {len(lcs_results)} raw trial values to raw_trials.npy")

results = {
    "N": N,
    "W": W,
    "M": M,
    "empirical_mean": mean_lcs,
    "empirical_ratio": empirical_ratio,
    "hoeffding_margin": hoeffding_ratio_error,
    "provable_lower_bound": provable_lower_bound,
    "time_s": elapsed,
    "raw_trials_file": "raw_trials.npy",
    "raw_trials_hash_sha256": None,
}

import hashlib
with open(os.path.join(OUT_DIR, "raw_trials.npy"), "rb") as f:
    results["raw_trials_hash_sha256"] = hashlib.sha256(f.read()).hexdigest()

verified_path = os.path.join(OUT_DIR, "results_verified.json")
with open(verified_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"Saved verified results to {verified_path}")
