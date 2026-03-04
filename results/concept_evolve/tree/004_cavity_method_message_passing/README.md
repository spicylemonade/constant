# cavity_method_message_passing

## Context
Adapts the replica symmetry cavity method from spin glass theory to formulate a local message-passing algorithm that computes marginal probabilities of character alignments.

## Implementation Backlog
- Mathematical setup: Z(T) = \sum_{\text{alignments}} \exp(L/T), F = -T \ln Z, \gamma = \lim_{T \to 0} F/n
- Try to run the experiment: Run Belief Propagation on random pairs of strings of length N=1000. Compare the zero-temperature limit of free energy with known lower bounds.
