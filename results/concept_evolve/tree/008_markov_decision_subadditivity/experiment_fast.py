import numpy as np
import time
import json

def solve_lcs_mdp_vectorized(K=8):
    S = 1 << K
    mask = S - 1
    
    # Precompute the two possible next states for each state
    # T[x, 0] = (x << 1) & mask
    # T[x, 1] = ((x << 1) & mask) + 1
    x_idx = np.arange(S)
    T0 = (x_idx << 1) & mask
    T1 = T0 + 1
    
    # MSB check
    msb_x = x_idx >> (K - 1)
    msb_y = x_idx >> (K - 1) # Same for y
    
    # Create match mask: match_mask[x, y] is True if msb_x[x] == msb_y[y]
    match_mask = msb_x[:, None] == msb_y[None, :]
    
    print(f"MDP states: {S}x{S} = {S*S}. Starting binary search for gamma.")
    
    low = 0.70
    high = 0.85
    
    V = np.zeros((S, S), dtype=np.float32)
    
    for _ in range(35):
        mid = (low + high) / 2.0
        
        # We solve the Average Reward equation relative to 'mid'
        # V(x,y) = max(
        #    -0.5*mid + 0.5*(V[T0(x), y] + V[T1(x), y]),   # Drop X
        #    -0.5*mid + 0.5*(V[x, T0(y)] + V[x, T1(y)]),   # Drop Y
        #    match_mask * (1.0 - mid + 0.25*(V[T0x, T0y] + V[T0x, T1y] + V[T1x, T0y] + V[T1x, T1y])) # Match
        # )
        
        V = np.zeros((S, S), dtype=np.float32)
        
        for vi_step in range(2000):
            EV_drop_x = 0.5 * (V[T0, :] + V[T1, :])
            val_drop_x = -0.5 * mid + EV_drop_x
            
            EV_drop_y = 0.5 * (V[:, T0] + V[:, T1])
            val_drop_y = -0.5 * mid + EV_drop_y
            
            EV_match = 0.5 * (EV_drop_x[:, T0] + EV_drop_x[:, T1])
            val_match = 1.0 - mid + EV_match
            val_match = np.where(match_mask, val_match, -np.inf)
            
            V_new = np.maximum(np.maximum(val_drop_x, val_drop_y), val_match)
            
            offset = V_new[0, 0]
            V_new -= offset
            
            diff = np.max(np.abs(V_new - V))
            V = V_new
            if diff < 1e-6:
                break
            
        # To determine if mid is feasible, we evaluate the exact steady state or use the fact that
        # if the value function drifted positively, it means the true average reward > mid.
        # Actually, in Relative Value Iteration, the 'offset' is exactly the average reward!
        # Since we use V_new -= offset, the average reward relative to 'mid' is 'offset'.
        # So if offset > 0, the policy achieves > mid.
        # Wait, if offset > 0, then the true gamma is > mid.
        if offset > 0:
            low = mid
        else:
            high = mid
            
        print(f"lambda={mid:.6f} offset={offset:.6f} range=[{low:.6f}, {high:.6f}]")
        
    print(f"Optimal lower bound with lookahead K={K}: {low:.6f}")
    return low

if __name__ == "__main__":
    results = {}
    for k in [8, 9, 10]:
        t0 = time.time()
        lb = solve_lcs_mdp_vectorized(k)
        print(f"Time for K={k}: {time.time()-t0:.2f}s", flush=True)
        results[f"lookahead_{k}"] = float(lb)
        
        with open("results/concept_evolve/tree/008_markov_decision_subadditivity/results_fast.json", "w") as f:
            json.dump(results, f, indent=2)
