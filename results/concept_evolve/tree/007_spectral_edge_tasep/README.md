# spectral_edge_tasep

## Context
Relates the fluctuations of the LCS length to the Tracy-Widom distribution and the largest eigenvalue of the GUE random matrix ensemble.

## Implementation Backlog
- Mathematical setup: \lim_{n \to \infty} \mathbb{P}\left(\frac{L_{n} - \gamma_2 n}{c n^{1/3}} \le s\right) = F_2(s)
- Try to run the experiment: Generate 10,000 pairs of n=5000. Fit the empirical distribution of L_n to the Tracy-Widom F_2 distribution and solve for \gamma_2 and c.
