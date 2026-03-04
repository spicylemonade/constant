# markov_decision_subadditivity

## Context
Formulates the step-by-step pairing of characters as a Markov Decision Process (MDP) and uses Reinforcement Learning to discover near-optimal local alignment policies that establish rigorous expected lower bounds.

## Implementation Backlog
- Mathematical setup: V^*(s) = \max_a \left( R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^*(s') \right)
- Try to run the experiment: Train PPO with a lookahead of 15 characters to choose DP moves. Evaluate expected reward per step.
