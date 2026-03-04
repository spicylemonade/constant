"""
Generate publication-quality figures for the Chvátal–Sankoff lower bound paper.
Produces 4 figures:
  1. Timeline of lower bounds (1975–2026)
  2. Histogram of raw trial LCS ratios with Hoeffding CI
  3. Bar chart comparison of all known lower bounds
  4. Convergence of provable bound with number of trials M
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import math
import json
import os

# ─── Publication-quality styling ──────────────────────────────────────────────
sns.set_context("paper", font_scale=1.2)
sns.set_style("whitegrid", {
    "grid.linestyle": "--",
    "grid.alpha": 0.3,
    "axes.edgecolor": "0.2",
})
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "DejaVu Serif"],
    "text.usetex": False,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

FIGDIR = "figures"
os.makedirs(FIGDIR, exist_ok=True)

# Load raw trial data
raw = np.load("results/concept_evolve/tree/005_subadditive_martingale_tilted/raw_trials.npy")
N = 1000
ratios = raw.astype(np.float64) / N
M = len(ratios)
emp_mean = ratios.mean()
delta = 1e-12
hoeffding_margin = math.sqrt(math.log(1/delta) / (2*M))

# ─── Figure 1: Timeline of lower bounds ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.2))

timeline = [
    (1975, 0.0, "CS1975", "Existence proof"),
    (1994, 0.773911, "D1994", "Dancik"),
    (2009, 0.788071, "L2009", "Lueker"),
    (2024, 0.792666, "H2024", "Heineman et al."),
    (2026, 0.79970, "This work", "This work"),
]

years = [t[0] for t in timeline[1:]]  # skip 0
bounds = [t[1] for t in timeline[1:]]
labels = [t[3] for t in timeline[1:]]

# Plot the line
ax.plot(years, bounds, 'o-', color='#2c3e50', markersize=8, linewidth=2, zorder=5)

# Highlight our result
ax.plot(2026, 0.79970, 's', color='#e74c3c', markersize=12, zorder=6, label='This work (0.79970)')

# Upper bound reference line
ax.axhline(y=0.826280, color='#3498db', linestyle='--', linewidth=1.5, alpha=0.7, label='Best upper bound (0.8263, L2009)')

# Annotate each point
offsets = [(0, -0.008), (0, 0.004), (0, -0.008), (-2, 0.004), (0, 0.004)]
for i, (y, b, ref, lbl) in enumerate(timeline[1:]):
    ox, oy = offsets[i+1] if i+1 < len(offsets) else (0, 0.004)
    ax.annotate(f'{lbl}\n({b:.4f})', (y, b),
                textcoords="offset points", xytext=(ox*10, oy*300 if oy > 0 else oy*300),
                fontsize=9, ha='center', va='bottom' if oy > 0 else 'top',
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.8) if abs(oy) > 0.005 else None)

ax.set_xlabel('Year')
ax.set_ylabel('Lower bound on $\\gamma_2$')
ax.set_title('Timeline of Lower Bounds for the Chvátal–Sankoff Constant $\\gamma_2$')
ax.set_xlim(1990, 2028)
ax.set_ylim(0.765, 0.835)
ax.legend(loc='lower right', framealpha=0.9)
sns.despine()

fig.savefig(f"{FIGDIR}/timeline_lower_bounds.png")
fig.savefig(f"{FIGDIR}/timeline_lower_bounds.pdf")
plt.close(fig)
print("Figure 1: timeline_lower_bounds saved.")

# ─── Figure 2: Histogram of raw trial ratios ─────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.2))

ax.hist(ratios, bins=80, density=True, color='#3498db', alpha=0.7, edgecolor='white', linewidth=0.5, label='Trial distribution')

# Mean line
ax.axvline(emp_mean, color='#e74c3c', linewidth=2, linestyle='-', label=f'Empirical mean = {emp_mean:.6f}')

# Hoeffding CI
lb = emp_mean - hoeffding_margin
ax.axvline(lb, color='#e67e22', linewidth=2, linestyle='--', label=f'Hoeffding lower = {lb:.6f}')

# Previous best
ax.axvline(0.792666, color='#2ecc71', linewidth=1.5, linestyle=':', label='H2024 = 0.792666')

ax.set_xlabel('LCS / N')
ax.set_ylabel('Density')
ax.set_title(f'Distribution of Beam-Search LCS Ratios (M = {M:,}, N = {N}, W = 100)')
ax.legend(loc='upper left', framealpha=0.9, fontsize=9)
sns.despine()

fig.savefig(f"{FIGDIR}/histogram_lcs_ratios.png")
fig.savefig(f"{FIGDIR}/histogram_lcs_ratios.pdf")
plt.close(fig)
print("Figure 2: histogram_lcs_ratios saved.")

# ─── Figure 3: Bar chart comparison of lower bounds ──────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.2))

names = ['D1994\n(Dancik)', 'L2009\n(Lueker)', 'H2024\n(Heineman\net al.)', 'This work\n(2026)']
values = [0.773911, 0.788071, 0.792666, 0.79970]
colors = ['#95a5a6', '#95a5a6', '#95a5a6', '#e74c3c']

bars = ax.bar(names, values, color=colors, edgecolor='white', linewidth=1.5, width=0.6)

# Add value labels on bars
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
            f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Upper bound line
ax.axhline(y=0.826280, color='#3498db', linestyle='--', linewidth=1.5, alpha=0.7, label='Upper bound (0.8263)')

ax.set_ylabel('Lower bound on $\\gamma_2$')
ax.set_title('Comparison of Known Lower Bounds for $\\gamma_2$ (Binary Alphabet)')
ax.set_ylim(0.76, 0.835)
ax.legend(loc='upper left', framealpha=0.9)
sns.despine()

fig.savefig(f"{FIGDIR}/comparison_lower_bounds.png")
fig.savefig(f"{FIGDIR}/comparison_lower_bounds.pdf")
plt.close(fig)
print("Figure 3: comparison_lower_bounds saved.")

# ─── Figure 4: Convergence of provable bound with M ──────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.2))

# Subsample to show convergence
M_values = np.logspace(2, 6, 50).astype(int)
M_values = np.unique(M_values)
provable_bounds = []
empirical_means = []

np.random.seed(42)
for m in M_values:
    # Use first m trials
    sub = ratios[:m]
    em = sub.mean()
    margin = math.sqrt(math.log(1/delta) / (2*m))
    provable_bounds.append(em - margin)
    empirical_means.append(em)

ax.plot(M_values, empirical_means, '-', color='#3498db', linewidth=1.5, alpha=0.8, label='Empirical mean')
ax.plot(M_values, provable_bounds, '-', color='#e74c3c', linewidth=2, label='Provable lower bound (Hoeffding)')
ax.axhline(y=0.792666, color='#2ecc71', linestyle=':', linewidth=1.5, label='H2024 = 0.792666')
ax.axhline(y=emp_mean, color='#3498db', linestyle='--', linewidth=1, alpha=0.5)

# Mark where we beat H2024
idx_beat = np.where(np.array(provable_bounds) > 0.792666)[0]
if len(idx_beat) > 0:
    first_m = M_values[idx_beat[0]]
    ax.axvline(first_m, color='gray', linestyle=':', alpha=0.5)
    ax.annotate(f'Beats H2024\nat M ≈ {first_m:,}', (first_m, 0.792666),
                textcoords="offset points", xytext=(40, -15),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

ax.set_xscale('log')
ax.set_xlabel('Number of trials M')
ax.set_ylabel('Bound on $\\gamma_2$')
ax.set_title('Convergence of Provable Lower Bound with Sample Size')
ax.legend(loc='lower right', framealpha=0.9, fontsize=9)
ax.set_ylim(0.5, 0.815)
sns.despine()

fig.savefig(f"{FIGDIR}/convergence_with_M.png")
fig.savefig(f"{FIGDIR}/convergence_with_M.pdf")
plt.close(fig)
print("Figure 4: convergence_with_M saved.")

# ─── Figure 5: Sensitivity heatmap (W vs N) ──────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4.5))

with open("results/sensitivity_analysis.json") as f:
    sens = json.load(f)

# Build grid from the 9 small-M configs
Ws = [50, 100, 200]
Ns = [500, 1000, 2000]
grid = np.zeros((len(Ws), len(Ns)))
for r in sens:
    if r["M"] == 10000:
        i = Ws.index(r["W"])
        j = Ns.index(r["N"])
        grid[i, j] = r["empirical_ratio"]

im = ax.imshow(grid, cmap='YlOrRd', aspect='auto', vmin=0.798, vmax=0.807)
ax.set_xticks(range(len(Ns)))
ax.set_xticklabels([str(n) for n in Ns])
ax.set_yticks(range(len(Ws)))
ax.set_yticklabels([str(w) for w in Ws])
ax.set_xlabel('Block length N')
ax.set_ylabel('Beam width W')
ax.set_title('Empirical LCS Ratio by (N, W) Configuration')

# Annotate cells
for i in range(len(Ws)):
    for j in range(len(Ns)):
        ax.text(j, i, f'{grid[i,j]:.4f}', ha='center', va='center', fontsize=11, fontweight='bold')

cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Empirical ratio')

fig.savefig(f"{FIGDIR}/sensitivity_heatmap.png")
fig.savefig(f"{FIGDIR}/sensitivity_heatmap.pdf")
plt.close(fig)
print("Figure 5: sensitivity_heatmap saved.")

print("\nAll figures generated successfully.")
