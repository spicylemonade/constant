# thermodynamic_lcs_relaxation

## Context
Treats the discrete LCS matrix as a discretized PDE. Derives a macroscopic differential equation for the 'average speed' of optimal alignments using calculus of variations.

## Implementation Backlog
- Mathematical setup: \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0, \gamma_2 = \int_0^1 v(x) dx
- Try to run the experiment: Solve the Hamilton-Jacobi-Bellman equation corresponding to the fluid limit of the LCS path ensemble.
