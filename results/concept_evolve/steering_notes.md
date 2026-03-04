# Concept Evolve Steering Notes

## Direction 1: RL-Guided Automaton Search
- **Concept Card:** `markov_decision_subadditivity`
- **Implementation Hypothesis:** Train a Deep Q-Network on a finite lookahead window of the two random strings. Prove the policy is stationary and its average reward per step strictly lower-bounds $\gamma_2$.
- **Bridge Chains:** `markov_decision_subadditivity -> subadditive_martingale_tilted` (RL policy value function provides the martingale required for tight subadditive bounds.)
- **Rubric Items Informed:** item_011 (Concept-tree exploration for lower bounds), item_013 (Develop extended finite automata for lower bound), item_016 (Execute lower bound large-scale experiments).

## Direction 2: Tensor Network Ground State Bounds
- **Concept Card:** `tensor_network_alignment`
- **Implementation Hypothesis:** Construct the transfer matrix for the finite-temperature LCS problem. Use Density Matrix Renormalization Group (DMRG) to find the leading eigenvalue.
- **Bridge Chains:** `cavity_method_message_passing -> tensor_network_alignment -> spectral_edge_tasep` (Spin Glass to Quantum Entanglement to Random Matrix)
- **Rubric Items Informed:** item_012 (Concept-tree exploration for upper bounds), item_014 (Develop improved weighting scheme for upper bound), item_017 (Execute upper bound large-scale experiments).

## Direction 3: Thermodynamic / PDE Control Bounds
- **Concept Card:** `thermodynamic_lcs_relaxation`
- **Implementation Hypothesis:** Formulate a continuous control problem whose objective is bounded by Vachkovskaia's thermodynamic limits, and use finite element methods to establish a strict upper bound.
- **Bridge Chains:** `push_tasep_duality -> hydrodynamic_limit_shockwaves -> thermodynamic_lcs_relaxation` (Particle to Fluid to PDE Control)
- **Rubric Items Informed:** item_012 (Concept-tree exploration for upper bounds), item_014 (Develop improved weighting scheme for upper bound), item_017 (Execute upper bound large-scale experiments).
