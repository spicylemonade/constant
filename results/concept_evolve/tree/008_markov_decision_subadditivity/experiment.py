import numpy as np
import json
import time

def solve_lcs_mdp(K=3):
    """
    Solve the Fractional MDP to find a provable lower bound for the Chvátal-Sankoff constant.
    State: (X_buf, Y_buf) where each is a tuple of K bits (0 or 1).
    Total states: 2^(2K).
    """
    # Generate all states
    states = []
    for i in range(1 << K):
        for j in range(1 << K):
            x = tuple((i >> bit) & 1 for bit in range(K))
            y = tuple((j >> bit) & 1 for bit in range(K))
            states.append((x, y))
            
    S = len(states)
    state_to_idx = {s: idx for idx, s in enumerate(states)}
    
    # Precompute transitions
    # actions: 0=Drop X, 1=Drop Y, 2=Match (if possible)
    
    def get_transitions(x, y, action):
        # returns list of (prob, next_x, next_y, reward, dx, dy)
        if action == 0: # Drop X
            return [(0.5, x[1:] + (bit,), y, 0, 1, 0) for bit in (0,1)]
        elif action == 1: # Drop Y
            return [(0.5, x, y[1:] + (bit,), 0, 0, 1) for bit in (0,1)]
        elif action == 2: # Match
            if x[0] == y[0]:
                res = []
                for bx in (0,1):
                    for by in (0,1):
                        res.append((0.25, x[1:] + (bx,), y[1:] + (by,), 1, 1, 1))
                return res
            else:
                return []
        return []

    # Value iteration for average reward
    # We want to maximize lambda such that there exist V(s) solving:
    # V(s) = max_a { R_a - lambda * C_a + sum_{s'} P(s'|s,a) V(s') }
    # where C_a = (dx + dy)/2
    
    # We'll use binary search on lambda (the expected LCS rate).
    # Since we know gamma_2 is between 0.79 and 0.83, we can search in [0.0, 1.0]
    
    low = 0.0
    high = 1.0
    
    V = np.zeros(S)
    best_policy = np.zeros(S, dtype=int)
    
    # Pre-build transition lists to speed up VI
    transitions = []
    for s in states:
        x, y = s
        s_trans = []
        for a in (0,1,2):
            t_list = get_transitions(x, y, a)
            if t_list:
                # convert to indices
                compiled = []
                for prob, nx, ny, r, dx, dy in t_list:
                    compiled.append((prob, state_to_idx[(nx, ny)], r, (dx+dy)/2.0))
                s_trans.append((a, compiled))
        transitions.append(s_trans)
        
        print(f"MDP states: {S}. Starting binary search for gamma.", flush=True)
    
    for _ in range(30):
        mid = (low + high) / 2.0
        
        # Value iteration to see if V converges to +infinity (lambda too small) or -infinity (lambda too big)
        # Actually, just run relative value iteration
        V = np.zeros(S)
        for vi_step in range(100):
            V_new = np.zeros(S)
            for s_idx in range(S):
                max_v = -float('inf')
                best_a = -1
                for a, t_list in transitions[s_idx]:
                    q = 0
                    for prob, ns_idx, r, cost in t_list:
                        q += prob * (r - mid * cost + V[ns_idx])
                    if q > max_v:
                        max_v = q
                        best_a = a
                V_new[s_idx] = max_v
                best_policy[s_idx] = best_a
            
            # anchor state 0 to 0
            offset = V_new[0]
            V_new = V_new - offset
            
            # Check convergence
            if np.max(np.abs(V_new - V)) < 1e-6:
                break
            V = V_new
            
        # Determine if the average reward at this lambda is positive or negative
        # The offset drift per step is the average reward relative to lambda.
        # Wait, the true average reward shifted by lambda*cost is exactly `offset` above.
        # But wait, the VI step without offsetting gives V_{n+1} = T V_n.
        # The average growth is approx V_{n+1}[0] - V_n[0].
        # Let's do a more robust evaluation of the policy:
        # P matrix for best_policy
        P = np.zeros((S, S))
        R_minus_lambda_C = np.zeros(S)
        for s_idx in range(S):
            a = best_policy[s_idx]
            # find the t_list for this action
            t_list = next(tl for act, tl in transitions[s_idx] if act == a)
            for prob, ns_idx, r, cost in t_list:
                P[s_idx, ns_idx] += prob
                R_minus_lambda_C[s_idx] += prob * (r - mid * cost)
                
        # Steady state distribution
        # Solve pi P = pi
        eigvals, eigvecs = np.linalg.eig(P.T)
        steady = np.real(eigvecs[:, np.argmax(np.isclose(eigvals, 1.0))])
        steady = steady / np.sum(steady)
        
        avg_val = np.sum(steady * R_minus_lambda_C)
        
        if avg_val > 0:
            low = mid
        else:
            high = mid
            
        print(f"Optimal lower bound with lookahead K={K}: {low:.6f}", flush=True)
    return low

if __name__ == "__main__":
    import time
    results = {}
    for k in range(3, 7):
        t0 = time.time()
        lb = solve_lcs_mdp(k)
        print(f"Time for K={k}: {time.time()-t0:.2f}s")
        results[f"lookahead_{k}"] = lb
    
    with open("results/concept_evolve/tree/008_markov_decision_subadditivity/results.json", "w") as f:
        json.dump(results, f, indent=2)
