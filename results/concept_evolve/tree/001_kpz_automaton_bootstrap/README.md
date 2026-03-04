# kpz_automaton_bootstrap

## Context
Combines the exact finite-state automata calculations of Dančík and Paterson with the theoretical scaling laws of the Kardar-Parisi-Zhang (KPZ) universality class to extrapolate infinite-limit bounds.

## Implementation Backlog
- Mathematical setup: \mathbb{E}[L_n]/n = \gamma_2 + A n^{-2/3}
- Try to run the experiment: Simulate LCS for length n=1000..50000. Regress E[L_n] = \gamma_2 n + A n^{1/3} + B. Extract \gamma_2 and test tightness.
