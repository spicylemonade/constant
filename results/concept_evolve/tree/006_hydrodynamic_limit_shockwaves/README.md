# hydrodynamic_limit_shockwaves

## Context
Models the DP matrix anti-diagonals as a fluid density profile undergoing Burgers' equation. The LCS constant is bounded by the speed of the macroscopic shockwave.

## Implementation Backlog
- Mathematical setup: \partial_t u + u \partial_x u = \nu \partial_{xx} u, \text{ speed } s = \frac{u_L + u_R}{2}
- Try to run the experiment: Track the expected maximum value along anti-diagonals k=1..2n. Measure the linear propagation speed.
