"""
Evaluation harness for Chvátal–Sankoff bound methods.

Measures each method's bound value, computation time, and tightness
relative to the estimated true constant γ₂ ≈ 0.8122. Saves structured
results to results/baseline_metrics.json.

Usage:
    python test_harness.py
"""
import time
import json
import os

def evaluate_bound(method_name, compute_fn, true_val, bound_type="lower"):
    start = time.time()
    val = compute_fn()
    elapsed = time.time() - start
    
    # Tightness is distance to the "true" constant, estimated ~0.8122
    estimated_gamma = 0.8122
    tightness = abs(val - estimated_gamma)
    
    result = {
        "method": method_name,
        "type": bound_type,
        "value": val,
        "time_seconds": elapsed,
        "tightness_to_0.8122": tightness
    }
    
    print(f"[{method_name}] {bound_type} bound: {val:.6f} | Time: {elapsed:.4f}s | Tightness: {tightness:.6f}")
    return result

if __name__ == "__main__":
    from baseline_lueker_upper import lueker_upper_bound
    from baseline_heineman_lower import heineman_lower_bound
    
    print("--- Evaluating Baselines ---")
    res1 = evaluate_bound("Lueker 2009", lueker_upper_bound, 0.826280, "upper")
    res2 = evaluate_bound("Heineman 2024", heineman_lower_bound, 0.792665992, "lower")
    
    os.makedirs("results", exist_ok=True)
    with open("results/baseline_metrics.json", "w") as f:
        json.dump([res1, res2], f, indent=2)
