# Baseline Verification Log

## 1. Lueker Upper Bound
- **Command executed:** `python3 baseline_lueker_upper.py`
- **Console Output:** `Lueker 2009 Upper Bound for binary alphabet: 0.826280`
- **Expected Literature Bound:** 0.826280
- **Verification Result:** SUCCESS. The script correctly outputs the precise Lueker upper bound.

## 2. Heineman Lower Bound
- **Command executed:** `python3 baseline_heineman_lower.py`
- **Console Output:** `Heineman 2024 Lower Bound for binary alphabet: 0.792665992`
- **Expected Literature Bound:** 0.792665992
- **Verification Result:** SUCCESS. The script correctly outputs the precise Heineman lower bound.

## 3. Exact Expected LCS for n=8
- **Command executed:** `python3 baseline_exact_lcs.py 8`
- **Console Output:** `Exact expected LCS for n=8: 5.4691162109375`
- **Analysis and Verification:** 
  The computed expectation for the length of the Longest Common Subsequence of two random binary strings of length $n=8$ is $E[L_8] = 5.4691162109375$.
  Calculating the expected fractional length gives $E[L_8] / 8 = 0.6836395263671875$.
  Because $E[L_n] / n$ approaches the Chvátal-Sankoff constant ($\gamma$) monotonically from below as $n \to \infty$, it is theoretically sound that for a small length like $n=8$, this fractional value ($0.683640$) remains strictly less than the asymptotic Heineman lower bound ($0.792665992$).

## Conclusion
All three scripts execute successfully and yield outputs that exactly match or align with the established literature bounds for the Chvátal-Sankoff constant.
