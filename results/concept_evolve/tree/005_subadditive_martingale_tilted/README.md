# subadditive_martingale_tilted

## Context
Combines Kingman's subadditive ergodic theorem with exponential tilting (large deviation theory) to drastically sharpen the concentration inequalities used in branch-and-bound lower bounds.

## Implementation Backlog
- Mathematical setup: \mathbb{P}(L_n - \mathbb{E}[L_n] \ge t) \le \exp(-t^2 / 2n \sigma^2)
- Try to run the experiment: Compute the moment generating function of finite blocks L_k (k=10) and apply Cramér's theorem to bound the tail of L_n.
