# tensor_network_alignment

## Context
Represents the dynamic programming alignment matrix as a 2D tensor network, reducing the computation of the expected exponential partition function to Matrix Product State (MPS) compression.

## Implementation Backlog
- Mathematical setup: Z = \text{tr}(T^n), \gamma = \lim_{\beta \to \infty} \frac{1}{\beta} \ln(\lambda_{\max}(T_\beta))
- Try to run the experiment: Implement a tensor network with bond dimension \chi=16. Compute \lambda_{\max} for varying temperatures \beta and extrapolate to \beta \to \infty.
