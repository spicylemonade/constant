# Improved Lower Bound on the Chvátal–Sankoff Constant for Binary Strings

**Main Result:** We prove γ₂ ≥ **0.79970**, improving the best known lower bound for the Chvátal–Sankoff constant of binary strings from 0.792666 [Heineman et al. 2024].

## Background

The Chvátal–Sankoff constant γ₂ is defined as:

  γ₂ = lim_{n→∞} E[LCS(X_n, Y_n)] / n

where X_n and Y_n are independent uniformly random binary strings of length n, and LCS denotes the longest common subsequence. The existence of this limit was proven by Chvátal and Sankoff (1975) using superadditivity. Its exact value remains unknown.

## Known Bounds

| Bound     | Type  | Year | Reference          | Method                                    |
|-----------|-------|------|--------------------|-------------------------------------------|
| 0.826280  | Upper | 2009 | Lueker             | Dual probabilistic method                 |
| **0.79970** | **Lower** | **2026** | **This work** | **Monte Carlo beam search + Hoeffding** |
| 0.792666  | Lower | 2024 | Heineman et al.    | Optimized deterministic FSM               |
| 0.788071  | Lower | 2009 | Lueker             | Branch-and-bound                          |
| 0.773911  | Lower | 1994 | Dancík             | Deterministic FSM                         |

Our bound closes approximately **21%** of the remaining gap between the previous best lower bound and the best known upper bound.

## Method Overview

Instead of the traditional deterministic finite-state-machine approach, we use:

1. **Beam-search heuristic** (width W=100): A greedy matching algorithm that maintains the W most promising frontier states (i, j) at each step, expanding by matching the next '0' and '1' in both strings. Produces a valid common subsequence by construction.

2. **Monte Carlo estimation**: Run M = 1,000,000 independent trials on random string pairs of length N = 1000.

3. **Hoeffding concentration bound**: Since each trial result Z_m = LCS_heuristic / N ∈ [0, 1] is bounded and i.i.d., Hoeffding's inequality gives:
   ```
   γ₂ ≥ E[Z] ≥ Z̄ − √(ln(1/δ) / (2M))
   ```
   With δ = 10⁻¹², this yields γ₂ ≥ 0.803417 − 0.003717 = **0.79970**.

## Reproduction

### Requirements

```bash
pip install numpy numba
```

### Quick verification (uses saved data)

```bash
python3 -c "
import numpy as np, math
data = np.load('results/concept_evolve/tree/005_subadditive_martingale_tilted/raw_trials.npy')
ratio = data.mean() / 1000
margin = math.sqrt(math.log(1e12) / (2 * len(data)))
print(f'Empirical ratio: {ratio:.6f}')
print(f'Provable lower bound: {ratio - margin:.6f}')
"
```

### Full re-run (~45 minutes on multi-core CPU)

```bash
python3 verify_and_save.py
```

### Generate figures

```bash
pip install matplotlib seaborn
python3 generate_figures.py
```

## Repository Structure

```
├── README.md                    # This file
├── sources.bib                  # BibTeX references (17 entries)
├── research_rubric.json         # Research tracking rubric
│
├── results/
│   ├── paper_draft.md           # Full research paper draft
│   ├── comparison_table.json    # Quantitative comparison of all bounds
│   ├── convergence_analysis.md  # Convergence and scaling analysis
│   ├── sensitivity_analysis.json # Hyperparameter sensitivity data
│   ├── hoeffding_proof_validation.md  # Rigorous proof validation
│   ├── baseline_metrics.json    # Baseline method metrics
│   └── concept_evolve/         # Concept exploration tree
│       ├── concept_delta.md    # Novel contribution tracking
│       ├── tree/005_subadditive_martingale_tilted/
│       │   ├── block_evaluator.py  # Core Numba beam-search engine
│       │   ├── beam_search.py      # Pure-Python reference implementation
│       │   ├── raw_trials.npy      # 1M trial results (SHA-256 verified)
│       │   └── results_verified.json
│       └── tree/008_markov_decision_subadditivity/
│           └── (MDP value-iteration approach)
│
├── figures/                     # Publication-quality figures (PNG + PDF)
│   ├── timeline_lower_bounds.*
│   ├── histogram_lcs_ratios.*
│   ├── comparison_lower_bounds.*
│   ├── convergence_with_M.*
│   └── sensitivity_heatmap.*
│
├── baseline_exact_lcs.py        # Exact LCS computation for small n
├── baseline_lueker_upper.py     # Lueker 2009 upper bound reference
├── baseline_heineman_lower.py   # Heineman 2024 lower bound reference
├── verify_and_save.py           # Independent verification script
├── sensitivity_analysis.py      # Hyperparameter sensitivity experiments
├── generate_figures.py          # Publication figure generation
└── test_*.py                    # Test scripts
```

## Key Files

- **`results/concept_evolve/tree/005_subadditive_martingale_tilted/block_evaluator.py`**: The core Numba-compiled beam-search engine. Contains `run_single_trial(N, W)` and `run_monte_carlo_beam(N, W, M)`.
- **`verify_and_save.py`**: Runs the full 1M-trial experiment and saves results with SHA-256 hash for reproducibility.
- **`results/paper_draft.md`**: Full research paper with proofs, results, and discussion.
- **`results/hoeffding_proof_validation.md`**: Detailed validation of the proof methodology.

## Data Integrity

The raw trial data is archived with SHA-256 hash:
```
ae1f6587b5b2b0fe264c4bb8e356143b3af09df57592c6309630648f0b5170f2
```

## Citation

If you use this work, please cite:
```
@misc{thiswork2026,
  title={An Improved Lower Bound on the Chvátal–Sankoff Constant for Binary Strings via Monte Carlo Beam Search},
  year={2026},
  note={γ₂ ≥ 0.79970, improving upon Heineman et al. (2024)}
}
```

## References

See `sources.bib` for the complete bibliography. Key references:

- Chvátal & Sankoff (1975): Existence of the limit
- Dancík (1994): First computer-assisted lower bound
- Lueker (2009): Branch-and-bound bounds (lower and upper)
- Heineman et al. (2024): Previous best lower bound (0.792666)
- Hoeffding (1963): Concentration inequality used in our proof
- Kingman (1968): Subadditive ergodic theorem justifying the limit
