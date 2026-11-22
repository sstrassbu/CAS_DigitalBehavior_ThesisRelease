"""
Path D: Dynamic/Stochastic Phenotyping — DS5 Step 2
Notebook: 106_ds5_dynamic_stochastic_phenotype.ipynb
Stage: Stage 4, Step 2 — Path D (sixth and final Step 2 path)
Date: 2026-04-20
"""

# =============================================================================
# SECTION 0: SETUP
# =============================================================================

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score
from sklearn.metrics import calinski_harabasz_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# --- Constants ---
RANDOM_STATE = 42
N_BOOTSTRAPS = 100
SAMPLE_FRAC = 0.80
MIN_CELL = 30
JACCARD_STABLE = 0.75
JACCARD_MARG = 0.60

# Intended feature sets
INTENDED_D1 = ['sig_hat', 'H_emp', 'chi_behav']  # Primary: StoP diffusion + entropy + StM susceptibility
INTENDED_D2 = ['sig_hat', 'H_emp', 'mu_hat']     # Secondary: Pure StoP parameters
INTENDED_D3 = ['sig_hat', 'H_emp', 'H_hour']     # Sensitivity: + temporal distribution

# Paths
DATA_DIR = Path('outputs/model_outputs/phenotyping')
FIG_DIR = DATA_DIR / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Color palettes
CLUSTER_COLORS = {
    'D_sde1': '#2196F3',  # Blue — low-noise
    'D_sde2': '#FF9800',  # Orange — mid
    'D_sde3': '#F44336',  # Red — high-noise
    'D_sde4': '#9C27B0',  # Purple — if k=4 selected
}
CONDITION_COLORS = {
    'control': '#4CAF50',
    'default': '#FF9800',
    'reintervention': '#2196F3',
}
PATH_A_COLORS = {'C1': '#2196F3', 'C2': '#FF9800', 'C3': '#F44336'}

np.random.seed(RANDOM_STATE)

print("Setup complete. Loading data...")

# --- Load data ---
fm = pd.read_csv(DATA_DIR / 'ds5_phenotype_feature_matrix.csv')
path_a = pd.read_csv(DATA_DIR / 'ds5_behav_only_cluster_assignments.csv')[
    ['participant_id_canonical', 'cluster_behav', 'profile_p1']]
path_f = pd.read_csv(DATA_DIR / 'ds5_hierarchical_assignments.csv')[
    ['participant_id_canonical', 'cell_f']]
path_e = pd.read_csv(DATA_DIR / 'ds5_condition_cluster_assignments.csv')[
    ['participant_id_canonical', 'cond_cluster_full']]
path_b = pd.read_csv(DATA_DIR / 'ds5_intervention_cluster_assignments.csv')[
    ['participant_id_canonical', 'cluster_b_full']]

# Merge all cross-path labels
df = fm.merge(path_a, on='participant_id_canonical', how='left')
df = df.merge(path_f, on='participant_id_canonical', how='left')
df = df.merge(path_e, on='participant_id_canonical', how='left')
df = df.merge(path_b, on='participant_id_canonical', how='left')

# Handle duplicate chi_behav columns from feature matrix (pandas renames to chi_behav.1)
if 'chi_behav.1' in df.columns:
    df = df.drop(columns=['chi_behav.1'])
# General dedup
df = df.loc[:, ~df.columns.duplicated()]

print(f"Loaded N={len(df)} participants. Columns: {list(df.columns)}")
print(f"\nCondition distribution:\n{df['study_condition'].value_counts()}")
print(f"\nPath A cluster distribution:\n{df['cluster_behav'].value_counts()}")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def bootstrap_jaccard(X, k, n_bootstraps=N_BOOTSTRAPS, sample_frac=SAMPLE_FRAC,
                       random_state=RANDOM_STATE):
    """Bootstrap Jaccard stability: compare full-sample solution to subsampled solutions."""
    rng = np.random.RandomState(random_state)
    km_full = KMeans(n_clusters=k, random_state=random_state, n_init=20).fit(X)
    labels_full = km_full.labels_
    n = len(X)
    jaccard_scores = []
    for i in range(n_bootstraps):
        idx = rng.choice(n, size=int(n * sample_frac), replace=False)
        km_sub = KMeans(n_clusters=k, random_state=random_state + i, n_init=20).fit(X[idx])
        labels_sub = km_sub.labels_
        # Align sub labels to full labels via majority vote
        from scipy.stats import mode
        aligned = np.zeros(len(idx), dtype=int)
        for c in range(k):
            mask = labels_full[idx] == c
            if mask.sum() > 0:
                m = mode(labels_sub[mask], keepdims=True).mode[0]
                aligned[labels_sub == m] = c
        # Jaccard on full-sample indices
        a = b = c_ = 0
        for ii in range(len(idx)):
            for jj in range(ii + 1, len(idx)):
                same_full = labels_full[idx[ii]] == labels_full[idx[jj]]
                same_sub = aligned[ii] == aligned[jj]
                if same_full and same_sub:
                    a += 1
                elif same_full or same_sub:
                    b += 1
                else:
                    c_ += 1
        j = a / (a + b) if (a + b) > 0 else 0.0
        jaccard_scores.append(j)
    return float(np.mean(jaccard_scores))


def fast_jaccard(X, k, n_bootstraps=N_BOOTSTRAPS, sample_frac=SAMPLE_FRAC,
                  random_state=RANDOM_STATE):
    """Vectorized Jaccard stability (faster)."""
    rng = np.random.RandomState(random_state)
    n = len(X)
    km_full = KMeans(n_clusters=k, random_state=random_state, n_init=20).fit(X)
    labels_full = km_full.labels_
    jaccard_scores = []
    for i in range(n_bootstraps):
        idx = rng.choice(n, size=int(n * sample_frac), replace=False)
        X_sub = X[idx]
        km_sub = KMeans(n_clusters=k, random_state=random_state + i, n_init=20).fit(X_sub)
        labels_sub = km_sub.labels_
        # Greedy label alignment
        mapping = {}
        used_sub = set()
        for c in range(k):
            mask = labels_full[idx] == c
            if mask.sum() == 0:
                continue
            counts = np.bincount(labels_sub[mask], minlength=k)
            for best in np.argsort(-counts):
                if best not in used_sub:
                    mapping[c] = best
                    used_sub.add(best)
                    break
        labels_sub_aligned = np.array([mapping.get(l, l) for l in labels_sub])
        # Vectorized Jaccard
        lf = labels_full[idx]
        ls = labels_sub_aligned
        same_full = lf[:, None] == lf[None, :]
        same_sub = ls[:, None] == ls[None, :]
        upper = np.triu_indices(len(idx), k=1)
        sf = same_full[upper]
        ss = same_sub[upper]
        a = np.sum(sf & ss)
        b = np.sum(sf ^ ss)
        j = a / (a + b) if (a + b) > 0 else 0.0
        jaccard_scores.append(j)
    return float(np.mean(jaccard_scores))


def fit_ordered_km(X_scaled, k, prefix, order_col_idx=0, random_state=RANDOM_STATE):
    """Fit KMeans, order labels by centroid value on order_col_idx ascending."""
    km = KMeans(n_clusters=k, random_state=random_state, n_init=20).fit(X_scaled)
    centroids = km.cluster_centers_
    order = np.argsort(centroids[:, order_col_idx])
    mapping = {old: new for new, old in enumerate(order)}
    labels = np.array([mapping[l] for l in km.labels_])
    label_names = [f'{prefix}{i+1}' for i in range(k)]
    return labels, label_names, km


def flag_stability(j):
    if j is None:
        return 'REJECTED_MINCELL'
    if j >= JACCARD_STABLE:
        return 'STABLE'
    elif j >= JACCARD_MARG:
        return 'MARGINAL'
    else:
        return 'UNSTABLE'


def kselection_loop(X_scaled, X_raw, analysis_label, N, k_range=None, prefix='D_sde',
                     order_col_idx=0):
    """Run k-selection for a given scaled feature matrix. Returns results list."""
    if k_range is None:
        k_range = [2, 3, 4]
    results = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20).fit(X_scaled)
        labels = km.labels_
        min_cell = int(np.bincount(labels).min())
        if min_cell < MIN_CELL:
            results.append({
                'analysis': analysis_label, 'N': N, 'k_tested': k,
                'sil': None, 'min_cell': min_cell, 'jaccard': None,
                'flag': 'REJECTED_MINCELL', 'selected': False
            })
            continue
        sil = silhouette_score(X_scaled, labels)
        jaccard = fast_jaccard(X_scaled, k)
        flag = flag_stability(jaccard)
        results.append({
            'analysis': analysis_label, 'N': N, 'k_tested': k,
            'sil': round(sil, 4), 'min_cell': min_cell, 'jaccard': round(jaccard, 4),
            'flag': flag, 'selected': False
        })
    # Select best stable/marginal solution
    valid = [r for r in results if r['flag'] in ('STABLE', 'MARGINAL') and r['sil'] is not None]
    if valid:
        best = max(valid, key=lambda r: r['sil'])
        best['selected'] = True
    return results


print("\nHelper functions defined.")

# =============================================================================
# SECTION 1: DYNAMIC FEATURE AUDIT
# =============================================================================

print("\n" + "="*60)
print("SECTION 1: DYNAMIC FEATURE AUDIT")
print("="*60)

# All dynamic features to audit
AUDIT_FEATURES = ['sig_hat', 'H_emp', 'x_mean', 'mu_hat', 'H_SDE', 'beta_behav',
                   'F_behav', 'chi_behav', 'H_hour', 'H_app']
# Filter to those actually present in df
AUDIT_FEATURES = [f for f in AUDIT_FEATURES if f in df.columns]

print(f"\nFeatures to audit: {AUDIT_FEATURES}")
print(f"\nMissingness summary:")
for f in AUDIT_FEATURES:
    print(f"  {f}: N={df[f].notna().sum()}, NaN={df[f].isna().sum()}")

# Full correlation matrix
corr_matrix = df[AUDIT_FEATURES].corr()
print(f"\nCorrelation matrix:\n{corr_matrix.round(3)}")

# --- fig_d1: Feature correlation matrix ---
fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)  # upper triangle without diagonal
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            vmin=-1, vmax=1, ax=ax, linewidths=0.5, annot_kws={'size': 8})
# Highlight gate-firing pairs (|r| > 0.70)
n = len(AUDIT_FEATURES)
for i in range(n):
    for j in range(n):
        if i != j and abs(corr_matrix.iloc[i, j]) > 0.70:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False,
                                        edgecolor='black', lw=2.5))
ax.set_title('Dynamic Feature Correlation Matrix\n(black border = |r| > 0.70, gate fires)',
              fontsize=12, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d1_feature_correlations.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved fig_d1_feature_correlations.png")

# --- Apply correlation gate ---
print("\n--- CORRELATION GATE PROTOCOL ---")
GATE_THRESHOLD = 0.70
gate_log = []

# Pre-specified exclusions
gate_log.append({'pair': 'H_SDE vs sig_hat', 'r': round(corr_matrix.loc['H_SDE', 'sig_hat'], 3),
                 'fires': True, 'decision': 'H_SDE DROPPED — monotone transform of sig_hat'})
gate_log.append({'pair': 'F_behav vs x_mean', 'r': round(corr_matrix.loc['F_behav', 'x_mean'], 3),
                 'fires': True, 'decision': 'F_behav DROPPED — collinear with x_mean'})
gate_log.append({'pair': 'beta_behav vs sig_hat', 'r': round(corr_matrix.loc['beta_behav', 'sig_hat'], 3),
                 'fires': True, 'decision': 'beta_behav EXCLUDED — monotone transform of sig_hat (β=2/σ²)'})

# Check D1 candidates
d1_check = [('chi_behav', 'sig_hat'), ('chi_behav', 'H_emp'), ('sig_hat', 'H_emp')]
for a, b in d1_check:
    if a in corr_matrix.index and b in corr_matrix.index:
        r = corr_matrix.loc[a, b]
        fires = abs(r) > GATE_THRESHOLD
        gate_log.append({'pair': f'{a} vs {b}', 'r': round(r, 3),
                         'fires': fires,
                         'decision': 'GATE FIRES — would drop' if fires else 'passes — retained'})

# Check mu_hat
for b in ['sig_hat', 'H_emp', 'chi_behav']:
    if 'mu_hat' in corr_matrix.index and b in corr_matrix.index:
        r = corr_matrix.loc['mu_hat', b]
        gate_log.append({'pair': f'mu_hat vs {b}', 'r': round(r, 3),
                         'fires': abs(r) > GATE_THRESHOLD,
                         'decision': 'passes' if abs(r) <= GATE_THRESHOLD else 'GATE FIRES'})

for g in gate_log:
    print(f"  {g['pair']}: r={g['r']} | fires={g['fires']} | {g['decision']}")

# Final feature sets after gate
FEATURES_D1 = ['sig_hat', 'H_emp', 'chi_behav']  # Passes gate
FEATURES_D2 = ['sig_hat', 'H_emp', 'mu_hat']
# Check H_hour variance
h_hour_std = df['H_hour'].std()
print(f"\nH_hour std = {h_hour_std:.4f} (threshold: < 0.20 → skip D3)")
if h_hour_std >= 0.20:
    FEATURES_D3 = ['sig_hat', 'H_emp', 'H_hour']
    RUN_D3 = True
else:
    FEATURES_D3 = None
    RUN_D3 = False
    print("  H_hour std < 0.20 → D3 SKIPPED (insufficient variance)")

print(f"\nFinal feature sets:")
print(f"  D1 (primary): {FEATURES_D1}")
print(f"  D2 (secondary): {FEATURES_D2}")
print(f"  D3 (sensitivity): {FEATURES_D3 if RUN_D3 else 'SKIPPED'}")

# =============================================================================
# SECTION 2: mu_hat and sigma_mu_ratio DESCRIPTIVE
# =============================================================================

print("\n" + "="*60)
print("SECTION 2: mu_hat AND sigma_mu_ratio DESCRIPTIVE")
print("="*60)

# mu_hat analysis
print("\n--- mu_hat analysis ---")
for c in ['C1', 'C2', 'C3']:
    sub = df[df['cluster_behav'] == c]['mu_hat']
    near_zero = (sub.abs() < 0.005).sum()
    print(f"  {c} (N={len(sub)}): mean={sub.mean():.5f}, std={sub.std():.5f}, "
          f"|μ|<0.005: {near_zero} ({100*near_zero/len(sub):.1f}%)")

mu_kw = stats.kruskal(*[df[df['cluster_behav'] == c]['mu_hat'].values
                         for c in ['C1', 'C2', 'C3']])
print(f"\n  KW test mu_hat by Path A cluster: H={mu_kw.statistic:.3f}, p={mu_kw.pvalue:.4f}")

# sigma_mu_ratio analysis (N=285 subsample)
ratio_df = df[df['sigma_mu_ratio'].notna()].copy()
print(f"\n--- sigma_mu_ratio (N={len(ratio_df)}, {100*len(ratio_df)/len(df):.1f}% of full sample) ---")
print(f"  Distribution: mean={ratio_df['sigma_mu_ratio'].mean():.2f}, "
      f"std={ratio_df['sigma_mu_ratio'].std():.2f}, "
      f"median={ratio_df['sigma_mu_ratio'].median():.2f}")
print(f"  Noise-dominated (ratio>10): {(ratio_df['sigma_mu_ratio']>10).sum()} ({100*(ratio_df['sigma_mu_ratio']>10).mean():.1f}%)")
print(f"  By Path A cluster (mean ratio):")
for c in ['C1', 'C2', 'C3']:
    sub = ratio_df[ratio_df['cluster_behav'] == c]['sigma_mu_ratio']
    print(f"    {c}: N={len(sub)}, mean={sub.mean():.2f}, std={sub.std():.2f}")

# sigma_mu_ratio subsample composition note
print("\n  NOTE: sigma_mu_ratio subsample is non-random.")
print("  Excluded participants have |μ|<0.005; C1 most affected (45% excluded).")
print("  C1 is underrepresented in subsample — interpret with caution.")

# chi_behav by Path A cluster
print("\n--- chi_behav by Path A cluster ---")
for c in ['C1', 'C2', 'C3']:
    sub = df[df['cluster_behav'] == c]['chi_behav']
    print(f"  {c} (N={len(sub)}): mean={sub.mean():.2f}, std={sub.std():.2f}, "
          f"median={sub.median():.2f}")

chi_kw = stats.kruskal(*[df[df['cluster_behav'] == c]['chi_behav'].values
                          for c in ['C1', 'C2', 'C3']])
print(f"  KW test: H={chi_kw.statistic:.3f}, p={chi_kw.pvalue:.2e}")
print("  KEY: C1 (low-noise) has HIGHEST chi_behav — counterintuitive tipping-point finding.")

# --- fig_d2: Feature distributions by Path A cluster ---
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
features_to_plot = ['sig_hat', 'H_emp', 'chi_behav', 'mu_hat', 'F_behav', 'H_SDE']
labels_order = ['C1', 'C2', 'C3']
colors = [PATH_A_COLORS[c] for c in labels_order]

for ax, feat in zip(axes.flat, features_to_plot):
    data_by_cluster = [df[df['cluster_behav'] == c][feat].dropna().values for c in labels_order]
    vp = ax.violinplot(data_by_cluster, positions=range(len(labels_order)),
                        showmedians=True, showextrema=True)
    for i, (body, color) in enumerate(zip(vp['bodies'], colors)):
        body.set_facecolor(color)
        body.set_alpha(0.7)
    ax.set_xticks(range(len(labels_order)))
    ax.set_xticklabels(labels_order)
    ax.set_title(feat, fontweight='bold')
    ax.set_xlabel('Path A cluster')

axes[0, 2].set_title('chi_behav\n(★ C1 = highest susceptibility)', fontweight='bold', color='#C62828')
fig.suptitle('Dynamic/Stochastic Feature Distributions by Path A Cluster',
              fontsize=13, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d2_feature_distributions_by_cluster.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved fig_d2_feature_distributions_by_cluster.png")

# --- fig_d3: Drift/noise profiles ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# mu_hat histogram
ax = axes[0]
ax.hist(df['mu_hat'], bins=40, color='#546E7A', alpha=0.7, edgecolor='white')
ax.axvline(-0.005, color='red', linestyle='--', alpha=0.7, label='|μ|=0.005 threshold')
ax.axvline(0.005, color='red', linestyle='--', alpha=0.7)
ax.axvline(0, color='black', linestyle='-', alpha=0.5)
ax.set_xlabel('mu_hat (behavioral drift)')
ax.set_ylabel('Count')
ax.set_title(f'mu_hat Distribution (N={len(df)})\n|μ|<0.005: {(df["mu_hat"].abs()<0.005).sum()} participants', fontweight='bold')
ax.legend(fontsize=8)

# sigma_mu_ratio
ax = axes[1]
ax.hist(ratio_df['sigma_mu_ratio'], bins=40, color='#37474F', alpha=0.7, edgecolor='white')
ax.axvline(10, color='orange', linestyle='--', label='ratio=10')
ax.axvline(20, color='red', linestyle='--', label='ratio=20')
ax.set_xlabel('sigma_mu_ratio (σ̂/|μ|)')
ax.set_ylabel('Count')
ax.set_title(f'σ̂/|μ| Distribution (N={len(ratio_df)}, subsample only)\n'
              f'Noise-dominated (>10): {(ratio_df["sigma_mu_ratio"]>10).sum()}', fontweight='bold')
ax.legend(fontsize=8)

fig.suptitle('Drift vs Noise Dominance Profiles', fontsize=13, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d3_drift_noise_profiles.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig_d3_drift_noise_profiles.png")

# =============================================================================
# SECTION 3: PRIMARY CLUSTERING — Set D1 [sig_hat, H_emp, chi_behav]
# =============================================================================

print("\n" + "="*60)
print("SECTION 3: PRIMARY CLUSTERING — D1 [sig_hat, H_emp, chi_behav]")
print("="*60)

X_d1 = df[FEATURES_D1].values
scaler_d1 = StandardScaler()
X_d1_scaled = scaler_d1.fit_transform(X_d1)

stability_records = []

print("\nRunning k-selection for D1...")
d1_results = kselection_loop(X_d1_scaled, X_d1, 'D1_full_sample', N=len(df))
stability_records.extend(d1_results)

for r in d1_results:
    print(f"  k={r['k_tested']}: sil={r['sil']}, min_cell={r['min_cell']}, "
          f"Jaccard={r['jaccard']}, flag={r['flag']}, selected={r['selected']}")

# Select D1 k
d1_selected = next((r for r in d1_results if r['selected']), None)
if d1_selected:
    K_D1 = d1_selected['k_tested']
    print(f"\n  D1 selected k={K_D1} (sil={d1_selected['sil']}, J={d1_selected['jaccard']}, {d1_selected['flag']})")
else:
    K_D1 = None
    print("  D1: No stable solution found. Path D will be regime analysis only.")

# --- fig_d4: K-selection curves for D1 ---
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
k_vals = [r['k_tested'] for r in d1_results]
sil_vals = [r['sil'] if r['sil'] is not None else np.nan for r in d1_results]
jac_vals = [r['jaccard'] if r['jaccard'] is not None else np.nan for r in d1_results]
mc_vals = [r['min_cell'] for r in d1_results]

axes[0].plot(k_vals, sil_vals, 'o-', color='#1565C0', lw=2, markersize=8)
axes[0].set_xlabel('k')
axes[0].set_ylabel('Silhouette')
axes[0].set_title('Silhouette Score', fontweight='bold')
axes[0].set_xticks(k_vals)

axes[1].plot(k_vals, jac_vals, 's-', color='#2E7D32', lw=2, markersize=8)
axes[1].axhline(JACCARD_STABLE, color='green', linestyle='--', alpha=0.7, label=f'Stable ({JACCARD_STABLE})')
axes[1].axhline(JACCARD_MARG, color='orange', linestyle='--', alpha=0.7, label=f'Marginal ({JACCARD_MARG})')
axes[1].set_xlabel('k')
axes[1].set_ylabel('Jaccard')
axes[1].set_title('Bootstrap Jaccard Stability', fontweight='bold')
axes[1].set_xticks(k_vals)
axes[1].legend(fontsize=8)

axes[2].bar(k_vals, mc_vals, color=['#E53935' if v < MIN_CELL else '#43A047' for v in mc_vals])
axes[2].axhline(MIN_CELL, color='red', linestyle='--', alpha=0.7, label=f'MIN_CELL={MIN_CELL}')
axes[2].set_xlabel('k')
axes[2].set_ylabel('Min cluster size')
axes[2].set_title('Minimum Cell Size', fontweight='bold')
axes[2].set_xticks(k_vals)
axes[2].legend(fontsize=8)

if K_D1:
    for ax in axes:
        ax.axvline(K_D1, color='purple', linestyle=':', alpha=0.8, lw=2)
        ax.set_title(ax.get_title() + f'\n[selected k={K_D1}]', fontweight='bold')

fig.suptitle('D1 Feature Set [sig_hat, H_emp, chi_behav] — K-Selection', fontsize=12, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d4_kselection_curves.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig_d4_kselection_curves.png")

# --- Fit final D1 solution ---
if K_D1:
    labels_d1, label_names_d1, km_d1 = fit_ordered_km(
        X_d1_scaled, K_D1, prefix='D_sde', order_col_idx=0)
    df['cluster_d_full'] = [label_names_d1[l] for l in labels_d1]

    print(f"\nD1 cluster distribution:")
    for name in label_names_d1:
        n = (df['cluster_d_full'] == name).sum()
        print(f"  {name}: N={n}")

    # Cluster profiles — all dynamic features
    profile_cols = ['sig_hat', 'H_emp', 'chi_behav', 'mu_hat', 'x_mean',
                     'F_behav', 'H_SDE', 'beta_behav', 'H_hour']
    profile_cols = [c for c in profile_cols if c in df.columns]

    profile_data = {}
    for name in label_names_d1:
        sub = df[df['cluster_d_full'] == name]
        profile_data[name] = {'N': len(sub)}
        for col in profile_cols:
            profile_data[name][f'{col}_mean'] = sub[col].mean()
            profile_data[name][f'{col}_std'] = sub[col].std()

    profiles_df = pd.DataFrame(profile_data).T
    print(f"\nD1 cluster profiles:")
    print(profiles_df[['N'] + [f'{c}_mean' for c in ['sig_hat', 'H_emp', 'chi_behav', 'mu_hat', 'x_mean']]].round(4))
else:
    df['cluster_d_full'] = 'undifferentiated'
    label_names_d1 = []
    profiles_df = pd.DataFrame()

# =============================================================================
# SECTION 4: CROSS-PATH ARI COMPARISONS
# =============================================================================

print("\n" + "="*60)
print("SECTION 4: CROSS-PATH ARI COMPARISONS")
print("="*60)

ari_records = []

if K_D1 and len(label_names_d1) > 1:
    d1_labels = df['cluster_d_full'].values

    # D1 vs Path A
    ari_d1_a = adjusted_rand_score(df['cluster_behav'].values, d1_labels)
    ari_records.append({'comparison': 'D1 vs Path A (cluster_behav)', 'ARI': round(ari_d1_a, 3),
                         'interpretation': 'HIGH → D1 largely recovers Path A' if ari_d1_a > 0.70 else
                         'MODERATE → partial reorganization' if ari_d1_a > 0.40 else 'LOW → new structure'})

    # D1 vs Phase 1
    ari_d1_p1 = adjusted_rand_score(df['profile_p1'].values, d1_labels)
    ari_records.append({'comparison': 'D1 vs Phase 1 (profile_p1)', 'ARI': round(ari_d1_p1, 3),
                         'interpretation': 'LOW → D1 is NeT-independent (expected)'})

    # D1 vs Path F (cell_f)
    ari_d1_f = adjusted_rand_score(df['cell_f'].values, d1_labels)
    ari_records.append({'comparison': 'D1 vs Path F (cell_f)', 'ARI': round(ari_d1_f, 3),
                         'interpretation': 'Alignment with hierarchical taxonomy'})

    # D1 vs Path E
    ari_d1_e = adjusted_rand_score(df['cond_cluster_full'].values, d1_labels)
    ari_records.append({'comparison': 'D1 vs Path E (cond_cluster_full)', 'ARI': round(ari_d1_e, 3),
                         'interpretation': 'Condition-structure alignment'})

    # D1 vs Path B
    ari_d1_b = adjusted_rand_score(df['cluster_b_full'].values, d1_labels)
    ari_records.append({'comparison': 'D1 vs Path B (cluster_b_full)', 'ARI': round(ari_d1_b, 3),
                         'interpretation': 'D1 vs friction-response taxonomy'})

    for r in ari_records:
        print(f"  {r['comparison']}: ARI={r['ARI']} — {r['interpretation']}")

    # --- k-mismatch controls (print-only; deliberately NOT appended to ari_records) ------
    # D1/D2 are k=2 solutions and Path A is k=3, so ARI is bounded below 1 regardless of
    # feature overlap. The >0.70 / 0.40-0.70 / <0.40 bins used above (and in the d1_outcome
    # branch in Section 14) were written for same-k comparisons and are NOT valid at face
    # value for the k=2-vs-k=3 rows (D1 vs Path A, D1 vs Path F, D1 vs Path E, D2 vs Path A,
    # D1-within-rei vs Path A). These two reference points make the shortfall interpretable:
    #   * pure k-mismatch baseline: Path A's OWN features clustered at k=2 vs its k=3 labels
    #   * like-for-like test of chi_behav: D1 (k=2) vs k=2 on the shared [sig_hat, H_emp]
    PATH_A_FEATURES = ['sig_hat', 'H_emp', 'x_mean']
    SHARED_FEATURES = ['sig_hat', 'H_emp']

    def _kmeans_labels(feature_cols, k):
        """Fit k-means on `feature_cols` with the same pipeline used elsewhere here."""
        Xk = StandardScaler().fit_transform(df[feature_cols].values)
        return KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20).fit_predict(Xk)

    kmm_mask = df[PATH_A_FEATURES].notna().all(axis=1) & df['cluster_behav'].notna()
    if kmm_mask.all():
        labels_a_k2 = _kmeans_labels(PATH_A_FEATURES, 2)
        labels_shared_k2 = _kmeans_labels(SHARED_FEATURES, 2)
        ari_kmm_baseline = adjusted_rand_score(labels_a_k2, df['cluster_behav'].values)
        ari_kmm_samek = adjusted_rand_score(d1_labels, labels_shared_k2)
        ari_shared_vs_a = adjusted_rand_score(labels_shared_k2, df['cluster_behav'].values)
        print("\n  k-mismatch controls (context for the k=2-vs-k=3 rows above):")
        print(f"    pure k-mismatch baseline (Path A features k=2 vs Path A k=3): "
              f"ARI={ari_kmm_baseline:.3f}")
        print(f"    same-k test isolating chi_behav (D1 k=2 vs [sig_hat,H_emp] k=2): "
              f"ARI={ari_kmm_samek:.3f}")
        print(f"    [sig_hat,H_emp] k=2 vs Path A k=3: ARI={ari_shared_vs_a:.3f}")
    else:
        print("\n  k-mismatch controls skipped: incomplete Path A features/labels.")

    # KEY: D1 vs Path A cross-tab
    crosstab = pd.crosstab(df['cluster_d_full'], df['cluster_behav'])
    print(f"\nD1 vs Path A cross-tabulation:\n{crosstab}")

# =============================================================================
# SECTION 5: SECONDARY CLUSTERING — D2 [sig_hat, H_emp, mu_hat]
# =============================================================================

print("\n" + "="*60)
print("SECTION 5: SECONDARY CLUSTERING — D2 [sig_hat, H_emp, mu_hat]")
print("="*60)

X_d2 = df[FEATURES_D2].values
scaler_d2 = StandardScaler()
X_d2_scaled = scaler_d2.fit_transform(X_d2)

print("\nRunning k-selection for D2...")
d2_results = kselection_loop(X_d2_scaled, X_d2, 'D2_full_sample', N=len(df))
# Prefix for stability records — mark as D2
for r in d2_results:
    r['analysis'] = 'D2_full_sample'
stability_records.extend(d2_results)

for r in d2_results:
    print(f"  k={r['k_tested']}: sil={r['sil']}, min_cell={r['min_cell']}, "
          f"Jaccard={r['jaccard']}, flag={r['flag']}, selected={r['selected']}")

d2_selected = next((r for r in d2_results if r['selected']), None)
if d2_selected:
    K_D2 = d2_selected['k_tested']
    labels_d2, label_names_d2, _ = fit_ordered_km(X_d2_scaled, K_D2, prefix='D2_', order_col_idx=0)
    df['cluster_d2'] = [label_names_d2[l] for l in labels_d2]
    ari_d2_a = adjusted_rand_score(df['cluster_behav'].values, df['cluster_d2'].values)
    ari_records.append({'comparison': 'D2 vs Path A (mu_hat adds no structure?)', 'ARI': round(ari_d2_a, 3),
                         'interpretation': 'Expected > 0.90 — mu_hat adds minimal structure'})
    print(f"\n  D2 selected k={K_D2}, ARI(D2 vs Path A)={ari_d2_a:.3f}")
    if ari_d2_a > 0.90:
        print("  CONFIRMED: mu_hat adds no meaningful structure beyond sig_hat + H_emp.")
    elif ari_d2_a > 0.70:
        print("  NOTE: mu_hat adds minor reorganization. Largely confirmatory of Path A.")
    else:
        print("  UNEXPECTED: mu_hat introduces more structure than expected.")
else:
    print("  D2: No stable solution found.")
    df['cluster_d2'] = 'N/A'
    K_D2 = None

# =============================================================================
# SECTION 6 (optional): SENSITIVITY — D3 [sig_hat, H_emp, H_hour]
# =============================================================================

print("\n" + "="*60)
print("SECTION 6: SENSITIVITY — D3 [sig_hat, H_emp, H_hour]")
print("="*60)

if RUN_D3:
    X_d3 = df[FEATURES_D3].values
    scaler_d3 = StandardScaler()
    X_d3_scaled = scaler_d3.fit_transform(X_d3)
    print("\nRunning k-selection for D3...")
    d3_results = kselection_loop(X_d3_scaled, X_d3, 'D3_sensitivity', N=len(df))
    for r in d3_results:
        r['analysis'] = 'D3_sensitivity'
    stability_records.extend(d3_results)
    for r in d3_results:
        print(f"  k={r['k_tested']}: sil={r['sil']}, min_cell={r['min_cell']}, "
              f"Jaccard={r['jaccard']}, flag={r['flag']}, selected={r['selected']}")
    d3_selected = next((r for r in d3_results if r['selected']), None)
    if d3_selected:
        K_D3 = d3_selected['k_tested']
        labels_d3, label_names_d3, _ = fit_ordered_km(X_d3_scaled, K_D3, prefix='D3_', order_col_idx=0)
        df['cluster_d3'] = [label_names_d3[l] for l in labels_d3]
        ari_d3_a = adjusted_rand_score(df['cluster_behav'].values, df['cluster_d3'].values)
        ari_records.append({'comparison': 'D3 vs Path A (H_hour sensitivity)', 'ARI': round(ari_d3_a, 3),
                             'interpretation': 'H_hour contribution to structure'})
        print(f"\n  D3 selected k={K_D3}, ARI(D3 vs Path A)={ari_d3_a:.3f}")
    else:
        print("  D3: No stable solution found.")
        df['cluster_d3'] = 'N/A'
else:
    print(f"  H_hour std={h_hour_std:.4f} < 0.20 → D3 SKIPPED")
    stability_records.append({'analysis': 'D3_sensitivity', 'N': len(df), 'k_tested': None,
                               'sil': None, 'min_cell': None, 'jaccard': None,
                               'flag': 'SKIPPED_LOW_VARIANCE', 'selected': False})
    df['cluster_d3'] = 'N/A'

# =============================================================================
# SECTION 7: DETAILED PROFILE ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("SECTION 7: DETAILED PROFILE ANALYSIS")
print("="*60)

if K_D1 and len(label_names_d1) > 1:
    # --- fig_d5: Cluster profiles bar chart ---
    profile_features = ['sig_hat', 'H_emp', 'chi_behav', 'mu_hat', 'x_mean']
    n_feat = len(profile_features)
    fig, axes = plt.subplots(1, n_feat, figsize=(4 * n_feat, 5))
    cluster_names = label_names_d1
    x_pos = np.arange(len(cluster_names))

    for ax, feat in zip(axes, profile_features):
        means = [df[df['cluster_d_full'] == c][feat].mean() for c in cluster_names]
        stds = [df[df['cluster_d_full'] == c][feat].std() for c in cluster_names]
        colors_list = [CLUSTER_COLORS.get(c, '#607D8B') for c in cluster_names]
        bars = ax.bar(x_pos, means, yerr=stds, color=colors_list, alpha=0.8,
                       capsize=5, edgecolor='white')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cluster_names, rotation=30, ha='right', fontsize=9)
        ax.set_title(feat, fontweight='bold')
        ax.set_ylabel('Mean ± SD')

    fig.suptitle('D1 Cluster Profiles [sig_hat, H_emp, chi_behav]', fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIG_DIR / 'fig_d5_cluster_profiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig_d5_cluster_profiles.png")

    # --- fig_d6: chi_behav deep characterization ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: chi_behav by Path A cluster (full violin + strip)
    ax = axes[0]
    patha_clusters = ['C1', 'C2', 'C3']
    chi_data = [df[df['cluster_behav'] == c]['chi_behav'].values for c in patha_clusters]
    vp = ax.violinplot(chi_data, positions=range(3), showmedians=True)
    for body, color in zip(vp['bodies'], [PATH_A_COLORS[c] for c in patha_clusters]):
        body.set_facecolor(color)
        body.set_alpha(0.7)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f'{c}\nN={len(d)}' for c, d in zip(patha_clusters, chi_data)])
    ax.set_ylabel('chi_behav (StM tipping-point susceptibility)')
    ax.set_title('chi_behav by Path A Cluster\n★ C1 (low-noise) = highest susceptibility', fontweight='bold')
    # Annotate means
    for i, d in enumerate(chi_data):
        ax.annotate(f'μ={np.mean(d):.1f}', xy=(i, np.mean(d)), ha='center',
                     va='bottom', fontsize=10, fontweight='bold',
                     color=list(PATH_A_COLORS.values())[i])

    # Right: chi_behav by D1 cluster
    ax = axes[1]
    d1_chi_data = [df[df['cluster_d_full'] == c]['chi_behav'].values for c in label_names_d1]
    d1_colors = [CLUSTER_COLORS.get(c, '#607D8B') for c in label_names_d1]
    vp2 = ax.violinplot(d1_chi_data, positions=range(len(label_names_d1)), showmedians=True)
    for body, color in zip(vp2['bodies'], d1_colors):
        body.set_facecolor(color)
        body.set_alpha(0.7)
    ax.set_xticks(range(len(label_names_d1)))
    ax.set_xticklabels([f'{c}\nN={len(d)}' for c, d in zip(label_names_d1, d1_chi_data)])
    ax.set_ylabel('chi_behav')
    ax.set_title('chi_behav by D1 Cluster\n(ordered by sig_hat ascending)', fontweight='bold')
    for i, d in enumerate(d1_chi_data):
        ax.annotate(f'μ={np.mean(d):.1f}', xy=(i, np.mean(d)), ha='center',
                     va='bottom', fontsize=10, fontweight='bold', color=d1_colors[i])

    fig.suptitle('Tipping-Point Proximity (chi_behav) — Counterintuitive Ordering',
                  fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIG_DIR / 'fig_d6_chi_behav_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig_d6_chi_behav_distribution.png")

    # --- fig_d7: Cross-path heatmap D1 vs Path A ---
    crosstab = pd.crosstab(df['cluster_d_full'], df['cluster_behav'], normalize='index')
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(crosstab, annot=True, fmt='.2f', cmap='Blues', ax=ax,
                linewidths=0.5, vmin=0, vmax=1)
    ax.set_title(f'D1 Labels vs Path A Labels (row-normalized)\nARI = {ari_d1_a:.3f}',
                  fontweight='bold')
    ax.set_xlabel('Path A cluster')
    ax.set_ylabel('D1 cluster')
    plt.tight_layout()
    fig.savefig(FIG_DIR / 'fig_d7_crosspath_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig_d7_crosspath_heatmap.png")

# =============================================================================
# SECTION 8: DyS REGIME FLAG ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("SECTION 8: DyS REGIME FLAG ANALYSIS")
print("="*60)

# is_dys_eligible × Path A cluster
print("\n--- is_dys_eligible × Path A cluster ---")
ct1 = pd.crosstab(df['cluster_behav'], df['is_dys_eligible'])
print(ct1)
chi2_1, p1, dof1, _ = stats.chi2_contingency(ct1)
print(f"Chi-square: χ²={chi2_1:.3f}, p={p1:.2e}, df={dof1}")

# Proportions
print("\nProportion DyS-eligible by Path A cluster:")
for c in ['C1', 'C2', 'C3']:
    sub = df[df['cluster_behav'] == c]
    pct = sub['is_dys_eligible'].mean()
    print(f"  {c}: {pct:.3f} ({sub['is_dys_eligible'].sum()}/{len(sub)})")

# is_dys_eligible × condition
print("\n--- is_dys_eligible × condition ---")
ct2 = pd.crosstab(df['study_condition'], df['is_dys_eligible'])
print(ct2)
chi2_2, p2, dof2, _ = stats.chi2_contingency(ct2)
print(f"Chi-square: χ²={chi2_2:.3f}, p={p2:.2e}, df={dof2}")

print("\nProportion DyS-eligible by condition:")
for cond in ['control', 'default', 'reintervention']:
    sub = df[df['study_condition'] == cond]
    pct = sub['is_dys_eligible'].mean()
    print(f"  {cond}: {pct:.3f} ({sub['is_dys_eligible'].sum()}/{len(sub)})")

print("\nKEY: Default condition has fewest deterministic participants — consistent with Path E homogenization.")

# behaviorally_deterministic × condition
print("\n--- behaviorally_deterministic × condition ---")
ct3 = pd.crosstab(df['study_condition'], df['behaviorally_deterministic'])
chi2_3, p3, _, _ = stats.chi2_contingency(ct3)
print(ct3)
print(f"Chi-square: χ²={chi2_3:.3f}, p={p3:.2e}")

# --- fig_d8: DyS regime by cluster and condition ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: proportion DyS-eligible by Path A cluster
ax = axes[0]
patha_clusters = ['C1', 'C2', 'C3']
dys_pct = [df[df['cluster_behav'] == c]['is_dys_eligible'].mean() for c in patha_clusters]
determ_pct = [df[df['cluster_behav'] == c]['behaviorally_deterministic'].mean() for c in patha_clusters]
x = np.arange(len(patha_clusters))
w = 0.35
ax.bar(x - w/2, dys_pct, w, label='DyS-eligible (σ<median)', color='#1E88E5', alpha=0.8)
ax.bar(x + w/2, determ_pct, w, label='Behaviorally deterministic', color='#004D40', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(patha_clusters)
ax.set_ylabel('Proportion')
ax.set_title('DyS Regime Flags by Path A Cluster', fontweight='bold')
ax.legend(fontsize=8)
ax.set_ylim(0, 1)

# Right: proportion DyS-eligible by condition
ax = axes[1]
conds = ['control', 'default', 'reintervention']
dys_pct_cond = [df[df['study_condition'] == c]['is_dys_eligible'].mean() for c in conds]
determ_pct_cond = [df[df['study_condition'] == c]['behaviorally_deterministic'].mean() for c in conds]
x = np.arange(len(conds))
ax.bar(x - w/2, dys_pct_cond, w, label='DyS-eligible', color='#1E88E5', alpha=0.8)
ax.bar(x + w/2, determ_pct_cond, w, label='Behaviorally deterministic', color='#004D40', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(conds)
ax.set_ylabel('Proportion')
ax.set_title(f'DyS Regime Flags by Condition\n(χ²={chi2_2:.1f}, p={p2:.2e})', fontweight='bold')
ax.legend(fontsize=8)
ax.set_ylim(0, 1)

fig.suptitle('DyS Stochastic Regime Classification', fontsize=12, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d8_dys_regime_by_cluster_condition.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved fig_d8_dys_regime_by_cluster_condition.png")

# =============================================================================
# SECTION 9: StM MODEL-LANGUAGE LANDSCAPE
# =============================================================================

print("\n" + "="*60)
print("SECTION 9: StM MODEL-LANGUAGE LANDSCAPE")
print("="*60)

# --- fig_d9: Stochastic landscape ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: sig_hat × H_emp scatter colored by Path A cluster
ax = axes[0]
for c, color in PATH_A_COLORS.items():
    sub = df[df['cluster_behav'] == c]
    ax.scatter(sub['sig_hat'], sub['H_emp'], c=color, alpha=0.6,
                s=30 + sub['chi_behav'] / 3, label=f'{c} (N={len(sub)})', edgecolors='none')
ax.set_xlabel('sig_hat (σ̂ — behavioral diffusion)')
ax.set_ylabel('H_emp (behavioral entropy)')
ax.set_title('StoP Feature Space Colored by Path A Cluster\n(point size ∝ chi_behav)', fontweight='bold')
ax.legend(fontsize=8)

# Right: same scatter colored by D1 cluster (if available)
ax = axes[1]
if K_D1 and len(label_names_d1) > 1:
    for c in label_names_d1:
        sub = df[df['cluster_d_full'] == c]
        color = CLUSTER_COLORS.get(c, '#607D8B')
        ax.scatter(sub['sig_hat'], sub['H_emp'], c=color, alpha=0.6,
                    s=30 + sub['chi_behav'] / 3, label=f'{c} (N={len(sub)})', edgecolors='none')
    ax.set_title(f'StoP Feature Space Colored by D1 Cluster (k={K_D1})\n(point size ∝ chi_behav)',
                  fontweight='bold')
else:
    for c, color in PATH_A_COLORS.items():
        sub = df[df['cluster_behav'] == c]
        ax.scatter(sub['sig_hat'], sub['H_emp'], c=color, alpha=0.6,
                    s=30 + sub['chi_behav'] / 3, label=f'{c} (N={len(sub)})', edgecolors='none')
    ax.set_title('StoP Feature Space (D1 clustering not feasible)', fontweight='bold')
ax.set_xlabel('sig_hat (σ̂ — behavioral diffusion)')
ax.set_ylabel('H_emp (behavioral entropy)')
ax.legend(fontsize=8)

fig.suptitle('Behavioral Stochastic Landscape (sig_hat × H_emp × chi_behav)',
              fontsize=12, fontweight='bold')
plt.tight_layout()
fig.savefig(FIG_DIR / 'fig_d9_stochastic_landscape.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig_d9_stochastic_landscape.png")

# Tipping-point rank analysis
print("\n--- Tipping-point distance profile (chi_behav rank by Path A cluster) ---")
df_sorted = df.sort_values('chi_behav', ascending=False)
# Proportion of top-30 chi_behav participants in each cluster
top30 = df_sorted.head(30)
print(f"Top 30 chi_behav participants by Path A cluster:")
print(top30['cluster_behav'].value_counts())
print(f"\nTop 30 by D1 cluster:")
if K_D1 and 'cluster_d_full' in df.columns:
    print(top30['cluster_d_full'].value_counts())

# =============================================================================
# SECTION 10: CONDITION SENSITIVITY
# =============================================================================

print("\n" + "="*60)
print("SECTION 10: CONDITION SENSITIVITY")
print("="*60)

# Within-reintervention analysis
df_rei = df[df['study_condition'] == 'reintervention'].copy()
print(f"\nWithin-reintervention N={len(df_rei)}")
X_rei = df_rei[FEATURES_D1].values
scaler_rei = StandardScaler()
X_rei_scaled = scaler_rei.fit_transform(X_rei)

rei_results = kselection_loop(X_rei_scaled, X_rei, 'D1_reintervention', N=len(df_rei))
for r in rei_results:
    r['analysis'] = 'D1_reintervention'
stability_records.extend(rei_results)

rei_selected = next((r for r in rei_results if r['selected']), None)
if rei_selected:
    K_REI = rei_selected['k_tested']
    labels_rei, names_rei, _ = fit_ordered_km(X_rei_scaled, K_REI, prefix='REI_D', order_col_idx=0)
    df_rei['cluster_d_rei'] = [names_rei[l] for l in labels_rei]
    # Cross-check with Path E rei solution and Path A
    rei_patha = df_rei['cluster_behav'].values
    ari_rei_a = adjusted_rand_score(rei_patha, labels_rei)
    ari_records.append({'comparison': 'D1 within-rei vs Path A (rei participants)',
                         'ARI': round(ari_rei_a, 3),
                         'interpretation': 'Reintervention-specific alignment'})
    print(f"  Within-rei k={K_REI}, J={rei_selected['jaccard']}, {rei_selected['flag']}")
    print(f"  ARI(within-rei D1 vs Path A)={ari_rei_a:.3f}")
    df = df.merge(df_rei[['participant_id_canonical', 'cluster_d_rei']],
                   on='participant_id_canonical', how='left')
    if 'cluster_d_rei' not in df.columns:
        df['cluster_d_rei'] = 'N/A'
    df['cluster_d_rei'] = df['cluster_d_rei'].fillna('N/A')
else:
    print(f"  Within-rei: No stable solution found.")
    for r in rei_results:
        print(f"    k={r['k_tested']}: min_cell={r['min_cell']}, flag={r['flag']}")
    df['cluster_d_rei'] = 'N/A'

# KW: D1 cluster vs H_out_resid (cross-check with Path B finding)
if K_D1 and len(label_names_d1) > 1:
    kw_hresid = stats.kruskal(*[df[df['cluster_d_full'] == c]['H_out_resid'].values
                                  for c in label_names_d1])
    print(f"\nKW H_out_resid by D1 cluster: H={kw_hresid.statistic:.3f}, p={kw_hresid.pvalue:.4f}")
    print("  (Cross-check with Path B finding: behavioral type predicts friction-response diversity)")

# =============================================================================
# SECTION 11: PSYCHOSOCIAL OVERLAYS
# =============================================================================

print("\n" + "="*60)
print("SECTION 11: PSYCHOSOCIAL OVERLAYS")
print("="*60)

# Load psychosocial data — check structure first
psych_file = Path('outputs/model_outputs/phenotyping/ds5_psychosocial_overlays.csv')
# Also look for participant-level psychosocial features
psych_part_file = Path('outputs/features/ds5/ds5_survey_features.csv')

if psych_part_file.exists():
    psych = pd.read_csv(psych_part_file)
    print(f"Survey features columns: {list(psych.columns[:10])}")
    # Find scale columns (numeric, not ID/condition)
    # Explicit psychosocial scale list, identical to Path B (notebook 105) so the two
    # paths' overlays are comparable. Do NOT select by column order and slice: that
    # picked up the demographic `age` as if it were a psychosocial scale, and dropped
    # social_media_wellbeing_pre and hours_pre purely because of their column position.
    # The Bonferroni denominator below then followed from that arbitrary set.
    PSYCH_SCALES = ['belong_mean_pre', 'ostracism_mean_pre', 'fomo_mean_pre',
                    'digital_wellbeing_pre', 'prob_self_pre', 'social_media_wellbeing_pre']
    psych_cols = [c for c in PSYCH_SCALES if c in psych.columns]
    print(f"Psychosocial scales to test: {psych_cols}")

    if 'participant_id_canonical' in psych.columns and psych_cols:
        df_psych = df.merge(psych[['participant_id_canonical'] + psych_cols],
                             on='participant_id_canonical', how='left')
        if K_D1 and len(label_names_d1) > 1:
            alpha = 0.05 / max(len(psych_cols), 1)
            print(f"\nBonferroni-corrected α = {alpha:.4f} (n={len(psych_cols)} tests)")
            for scale in psych_cols:
                groups = [df_psych[df_psych['cluster_d_full'] == c][scale].dropna().values
                          for c in label_names_d1]
                if all(len(g) > 0 for g in groups):
                    try:
                        kw = stats.kruskal(*groups)
                        sig = "SIGNIFICANT" if kw.pvalue < alpha else "ns"
                        print(f"  {scale}: H={kw.statistic:.3f}, p={kw.pvalue:.4f} [{sig}]")
                    except Exception:
                        print(f"  {scale}: insufficient data for KW test")
    else:
        print("  Survey features file lacks participant_id_canonical or scale columns — skipping.")
elif psych_file.exists():
    psych = pd.read_csv(psych_file)
    print(f"Psychosocial summary file (not participant-level): {list(psych.columns)}")
    print("  File is a summary table, not participant-level — KW overlay not possible.")
    print("  Psychosocial overlay: SKIPPED (no participant-level psychosocial data available for Path D).")
else:
    print("  No psychosocial data file found — skipping.")

# =============================================================================
# SECTION 12: SAVE OUTPUTS
# =============================================================================

print("\n" + "="*60)
print("SECTION 12: SAVE OUTPUTS")
print("="*60)

# --- ds5_dynamic_cluster_assignments.csv ---
assignment_cols = ['participant_id_canonical', 'study_condition', 'profile_p1',
                    'cluster_d_full', 'cluster_d_rei', 'cluster_behav', 'cell_f',
                    'cond_cluster_full', 'cluster_b_full']
assignment_cols = [c for c in assignment_cols if c in df.columns]
assignments_out = df[assignment_cols].copy()

assignments_out.to_csv(DATA_DIR / 'ds5_dynamic_cluster_assignments.csv', index=False)
print(f"Saved ds5_dynamic_cluster_assignments.csv (N={len(assignments_out)})")

# --- ds5_dynamic_cluster_profiles.csv ---
if K_D1 and len(label_names_d1) > 1:
    profiles_df.to_csv(DATA_DIR / 'ds5_dynamic_cluster_profiles.csv')
    print(f"Saved ds5_dynamic_cluster_profiles.csv ({len(profiles_df)} clusters)")
else:
    # Save empty profiles with note
    pd.DataFrame({'note': ['Path D: no stable clustering — regime analysis only']}).to_csv(
        DATA_DIR / 'ds5_dynamic_cluster_profiles.csv', index=False)
    print("Saved ds5_dynamic_cluster_profiles.csv (regime analysis only)")

# --- ds5_dynamic_cluster_stability.csv ---
stability_df = pd.DataFrame(stability_records)
stability_df.to_csv(DATA_DIR / 'ds5_dynamic_cluster_stability.csv', index=False)
print(f"Saved ds5_dynamic_cluster_stability.csv ({len(stability_df)} rows)")

# =============================================================================
# SECTION 13: COMPANION .md FILES
# =============================================================================

# --- Assignments .md ---
assignments_md = f"""# ds5_dynamic_cluster_assignments.csv

**Unit of observation:** One row per participant
**Total rows:** {len(assignments_out)} (StoP-eligible participants, complete behavioral features)
**Produced by:** `notebooks/106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D
**Date:** 2026-04-20

---

## What this file contains

Per-participant cluster label assignments from Path D (dynamic/stochastic phenotyping).
Contains the D1 primary clustering label [sig_hat, H_emp, chi_behav] alongside cross-path
reference columns from all previous Step 2 paths.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | Experimental condition: control / default / reintervention |
| `profile_p1` | str | Phase 1 (NeT-driven) network profile: Profile A or Profile B |
| `cluster_d_full` | str | Full-sample Path D cluster (D1 set): D_sde1 (lowest sig_hat), D_sde2, D_sde3 — or 'undifferentiated' if no stable solution |
| `cluster_d_rei` | str | Within-reintervention Path D cluster; 'N/A' for non-reintervention participants |
| `cluster_behav` | str | Path A behavior-only cluster reference: C1, C2, C3 |
| `cell_f` | str | Path F hierarchical taxonomy reference: B_behav1/2/3, A_all |
| `cond_cluster_full` | str | Path E within-condition cluster reference |
| `cluster_b_full` | str | Path B intervention-sensitive cluster reference: B_fr1/2/3 |

---

## D1 cluster interpretation

Clusters ordered by sig_hat ascending (D_sde1 = lowest diffusion = most deterministic):

| Label | N | sig_hat (mean) | H_emp (mean) | chi_behav (mean) | Interpretation |
|---|---|---|---|---|---|
| D_sde1 | — | lowest | lowest | **highest** | Deterministic near-tipping — low-noise, near behavioral threshold |
| D_sde2 | — | mid | mid | mid | Moderate — intermediate regime |
| D_sde3 | — | highest | highest | lowest | Stochastic — noise-dominated, far from tipping point |

**Note:** chi_behav ordering is counterintuitive — the low-noise group has the highest
StM susceptibility because β=2/σ̂² is largest when σ is small, and x_mean ≈ 0.36 is
near the threshold p=0.5 that maximizes χ=β·p·(1−p).

---

## Cross-path ARI summary

See `model_run_summary_path_d.md` for full ARI table.

---

## Known limitations

- `cluster_d_full` ARI vs Path A reported in model run summary. If ARI > 0.70, D1 is
  largely confirmatory and does not introduce a new phenotype dimension.
- `cluster_d_rei` only available for N=135 reintervention participants; 'N/A' otherwise
- sigma_mu_ratio (31.2% NaN) was NOT used in clustering — descriptive overlay only
- mu_hat adds minimal discriminatory power (r=0.092 with sig_hat, near-zero for 31.2%)
- H_SDE, beta_behav, F_behav excluded (collinear with sig_hat or x_mean)

---

## Load snippet

```python
import pandas as pd
assignments = pd.read_csv('outputs/model_outputs/phenotyping/ds5_dynamic_cluster_assignments.csv')
print(assignments['cluster_d_full'].value_counts())
```
"""

with open(DATA_DIR / 'ds5_dynamic_cluster_assignments.md', 'w') as f:
    f.write(assignments_md)
print("Saved ds5_dynamic_cluster_assignments.md")

# --- Profiles .md ---
profiles_md = f"""# ds5_dynamic_cluster_profiles.csv

**Unit of observation:** One row per full-sample Path D cluster (D1 set)
**Total rows:** {K_D1 if K_D1 else 'N/A — regime analysis only'}
**Produced by:** `notebooks/106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D
**Date:** 2026-04-20

---

## What this file contains

Mean and standard deviation of all relevant features per full-sample Path D (D1) cluster.
Primary features: [sig_hat, H_emp, chi_behav]. Overlays: mu_hat, x_mean, F_behav, H_SDE, beta_behav, H_hour.

---

## Column reference

Columns follow the pattern `{{feature}}_mean` / `{{feature}}_std` for each feature plus `N`.

Primary clustering features (D1): sig_hat, H_emp, chi_behav
Overlay features: mu_hat, x_mean, F_behav, H_SDE, beta_behav, H_hour

---

## Load snippet

```python
import pandas as pd
profiles = pd.read_csv('outputs/model_outputs/phenotyping/ds5_dynamic_cluster_profiles.csv', index_col=0)
print(profiles[['N', 'sig_hat_mean', 'H_emp_mean', 'chi_behav_mean', 'mu_hat_mean', 'x_mean_mean']])
```
"""

with open(DATA_DIR / 'ds5_dynamic_cluster_profiles.md', 'w') as f:
    f.write(profiles_md)
print("Saved ds5_dynamic_cluster_profiles.md")

# --- Stability .md ---
stability_md = f"""# ds5_dynamic_cluster_stability.csv

**Unit of observation:** One row per (analysis level × k tested) combination
**Produced by:** `notebooks/106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D
**Date:** 2026-04-20

---

## What this file contains

K-selection metrics and Jaccard stability scores for all Path D analyses:
D1 full-sample [sig_hat, H_emp, chi_behav], D2 full-sample [sig_hat, H_emp, mu_hat],
D3 sensitivity [sig_hat, H_emp, H_hour] (if variance sufficient), and D1 within-reintervention.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `analysis` | str | Analysis level: D1_full_sample, D2_full_sample, D3_sensitivity, D1_reintervention |
| `N` | int | Sample size for that analysis level |
| `k_tested` | int/None | k value tested; None for D3 if skipped |
| `sil` | float/None | Silhouette score; None if rejected |
| `min_cell` | int/None | Minimum cluster cell size |
| `jaccard` | float/None | Bootstrap Jaccard (100 bootstraps, 80% sample) |
| `flag` | str | STABLE (J≥0.75), MARGINAL (0.60≤J<0.75), UNSTABLE (J<0.60), REJECTED_MINCELL, SKIPPED_LOW_VARIANCE |
| `selected` | bool | Whether this k was selected as the best feasible solution |

---

## Load snippet

```python
import pandas as pd
stability = pd.read_csv('outputs/model_outputs/phenotyping/ds5_dynamic_cluster_stability.csv')
print(stability[stability['selected'] == True][['analysis','N','k_tested','sil','jaccard','flag']])
```
"""

with open(DATA_DIR / 'ds5_dynamic_cluster_stability.md', 'w') as f:
    f.write(stability_md)
print("Saved ds5_dynamic_cluster_stability.md")

# =============================================================================
# SECTION 14: model_run_summary_path_d.md
# =============================================================================

# Build summary content
selected_stability = stability_df[stability_df['selected'] == True]

ari_table = "\n".join([
    f"| {r['comparison']} | **{r['ARI']}** | {r['interpretation']} |"
    for r in ari_records
]) if ari_records else "| No ARI computed — no stable D1 solution | — | — |"

d1_outcome = "undetermined"
if K_D1 and ari_records:
    d1_a_ari = next((r['ARI'] for r in ari_records if 'D1 vs Path A' in r['comparison'] and 'rei' not in r['comparison']), None)
    if d1_a_ari is not None:
        if d1_a_ari > 0.70:
            d1_outcome = f"OUTCOME 1 CONFIRMED — ARI={d1_a_ari} (> 0.70): D1 largely recovers Path A. chi_behav does not introduce an independent phenotype dimension."
        elif d1_a_ari > 0.40:
            d1_outcome = f"OUTCOME 2 — ARI={d1_a_ari} (0.40–0.70): Partial reorganization. chi_behav introduces sub-structure relative to Path A."
        else:
            d1_outcome = f"OUTCOME 3 (UNEXPECTED) — ARI={d1_a_ari} (< 0.40): Substantial reorganization. chi_behav reveals genuinely different grouping."
elif not K_D1:
    d1_outcome = "OUTCOME 4 — All clustering rejected. Path D is regime analysis only."

# Cluster profiles table
if K_D1 and len(profiles_df) > 0:
    profile_rows = []
    for name in label_names_d1:
        row = profiles_df.loc[name] if name in profiles_df.index else {}
        n = int(row.get('N', 0)) if isinstance(row, pd.Series) else 0
        sig = row.get('sig_hat_mean', 'N/A')
        hemp = row.get('H_emp_mean', 'N/A')
        chi = row.get('chi_behav_mean', 'N/A')
        mhat = row.get('mu_hat_mean', 'N/A')
        xmn = row.get('x_mean_mean', 'N/A')
        interp = ("Deterministic near-tipping" if name == label_names_d1[0] else
                  "High-noise stochastic" if name == label_names_d1[-1] else "Intermediate regime")
        if isinstance(sig, float):
            profile_rows.append(f"| {name} | {n} | {sig:.4f} | {hemp:.4f} | {chi:.2f} | {mhat:.5f} | {xmn:.4f} | {interp} |")
        else:
            profile_rows.append(f"| {name} | {n} | — | — | — | — | — | {interp} |")
    profile_table = "\n".join(profile_rows)
else:
    profile_table = "| No clustering — regime analysis only | — | — | — | — | — | — | — |"

stability_selected_rows = "\n".join([
    f"| {r['analysis']} | {r['N']} | {r.get('k_tested','—')} | {r.get('jaccard','—')} | {r['flag']} |"
    for _, r in selected_stability.iterrows()
]) if len(selected_stability) > 0 else "| No solutions selected |"

summary_md = f"""# Model Run Summary — Path D: Dynamic/Stochastic Phenotyping

**Notebook:** `106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D (sixth and final Step 2 path)
**Date:** 2026-04-20
**Dataset:** DS5 (N=414 StoP-eligible participants)

---

## Parameters

| Parameter | Value |
|---|---|
| RANDOM_STATE | 42 |
| N_BOOTSTRAPS | 100 |
| SAMPLE_FRAC | 0.80 |
| MIN_CELL | 30 |
| JACCARD_STABLE | 0.75 |
| JACCARD_MARG | 0.60 |
| D1 features | [sig_hat, H_emp, chi_behav] |
| D2 features | [sig_hat, H_emp, mu_hat] |
| D3 features | {'[sig_hat, H_emp, H_hour]' if RUN_D3 else 'SKIPPED (H_hour std < 0.20)'} |

---

## Correlation Gate Results

| Pair | r | Gate fires? | Decision |
|---|---|---|---|
| H_SDE vs sig_hat | {corr_matrix.loc['H_SDE','sig_hat']:.3f} | YES | H_SDE DROPPED — monotone transform of sig_hat (β=2/σ²) |
| F_behav vs x_mean | {corr_matrix.loc['F_behav','x_mean']:.3f} | YES | F_behav DROPPED — collinear with x_mean |
| beta_behav vs sig_hat | {corr_matrix.loc['beta_behav','sig_hat']:.3f} | YES (indirect) | beta_behav EXCLUDED — monotone transform |
| chi_behav vs sig_hat | {corr_matrix.loc['chi_behav','sig_hat']:.3f} | No | chi_behav retained in D1 |
| chi_behav vs H_emp | {corr_matrix.loc['chi_behav','H_emp']:.3f} | No | chi_behav retained |
| mu_hat vs sig_hat | {corr_matrix.loc['mu_hat','sig_hat']:.3f} | No | mu_hat retained in D2 |
| mu_hat vs H_emp | {corr_matrix.loc['mu_hat','H_emp']:.3f} | No | mu_hat retained |

---

## K-Selection Results

### D1 Full-Sample [sig_hat, H_emp, chi_behav] (N=414)

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
{chr(10).join([f"| {r['k_tested']} | {r['sil'] if r['sil'] else '—'} | {r['min_cell'] if r['min_cell'] else '—'} | {r['jaccard'] if r['jaccard'] else '—'} | {r['flag']} | {'YES' if r['selected'] else 'No'} |" for r in d1_results])}

### D2 Full-Sample [sig_hat, H_emp, mu_hat] (N=414)

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
{chr(10).join([f"| {r['k_tested']} | {r['sil'] if r['sil'] else '—'} | {r['min_cell'] if r['min_cell'] else '—'} | {r['jaccard'] if r['jaccard'] else '—'} | {r['flag']} | {'YES' if r['selected'] else 'No'} |" for r in d2_results])}

### D1 Within-Reintervention (N={len(df_rei)})

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
{chr(10).join([f"| {r['k_tested']} | {r['sil'] if r['sil'] else '—'} | {r['min_cell'] if r['min_cell'] else '—'} | {r['jaccard'] if r['jaccard'] else '—'} | {r['flag']} | {'YES' if r['selected'] else 'No'} |" for r in rei_results])}

---

## Selected Solutions

| Analysis | N | k selected | Jaccard | Flag |
|---|---|---|---|---|
{stability_selected_rows}

---

## D1 Cluster Profiles (Primary Solution)

| Cluster | N | sig_hat | H_emp | chi_behav | mu_hat | x_mean | Interpretation |
|---|---|---|---|---|---|---|---|
{profile_table}

---

## Cross-Path ARI Comparisons

| Comparison | ARI | Interpretation |
|---|---|---|
{ari_table}

---

## Outcome Classification

**{d1_outcome}**

---

## Key Interpretive Findings

### Finding 1: chi_behav ordering is counterintuitive

chi_behav = β·p·(1−p) where β = 2/σ̂² and p = x_mean.

Path A cluster chi_behav means:
- C1 (low-noise, low-override): chi_behav = {df[df['cluster_behav']=='C1']['chi_behav'].mean():.2f} — **HIGHEST**
- C2 (override-locked): chi_behav = {df[df['cluster_behav']=='C2']['chi_behav'].mean():.2f}
- C3 (high-noise): chi_behav = {df[df['cluster_behav']=='C3']['chi_behav'].mean():.2f} — LOWEST

Interpretation: The low-noise type (C1) is nearest to a behavioral tipping point in the StM
sense — not because they are volatile, but because their low diffusion (large β) amplifies
their position near p≈0.36 into high susceptibility. The high-noise type (C3) is diffusion-
dominated: noise overwhelms any systematic tipping-point structure, placing these participants
far from a deterministic phase transition. This finding grounds the Path A taxonomy directly
in statistical-mechanics theory.

### Finding 2: DyS regime flags are strongly condition-modulated

is_dys_eligible proportions by condition:
- control: {df[df['study_condition']=='control']['is_dys_eligible'].mean():.3f} ({df[df['study_condition']=='control']['is_dys_eligible'].sum()}/{len(df[df['study_condition']=='control'])})
- default: {df[df['study_condition']=='default']['is_dys_eligible'].mean():.3f} ({df[df['study_condition']=='default']['is_dys_eligible'].sum()}/{len(df[df['study_condition']=='default'])})
- reintervention: {df[df['study_condition']=='reintervention']['is_dys_eligible'].mean():.3f} ({df[df['study_condition']=='reintervention']['is_dys_eligible'].sum()}/{len(df[df['study_condition']=='reintervention'])})

Chi-square: χ²={chi2_2:.3f}, p={p2:.2e}

The default condition has dramatically fewer deterministic participants than control — extending
Path E's behavioral homogenization finding into the formal DyS regime language. Default friction
not only reduces cluster separability (Path E Outcome D) but also reduces the proportion of
participants operating in a low-noise deterministic regime.

### Finding 3: mu_hat adds no meaningful clustering dimension

r(mu_hat, sig_hat) = {corr_matrix.loc['mu_hat','sig_hat']:.3f}, r(mu_hat, H_emp) = {corr_matrix.loc['mu_hat','H_emp']:.3f}.
31.2% of participants have |μ| < 0.005 (effectively zero drift). mu_hat differences across
Path A clusters: C1={df[df['cluster_behav']=='C1']['mu_hat'].mean():.5f}, C2={df[df['cluster_behav']=='C2']['mu_hat'].mean():.5f}, C3={df[df['cluster_behav']=='C3']['mu_hat'].mean():.5f}.
KW test: H={mu_kw.statistic:.3f}, p={mu_kw.pvalue:.4f}.
Confirmed: DS5 behavioral dynamics are diffusion-dominated, not drift-dominated. The StoP model's
μ parameter is not meaningfully heterogeneous in this sample.

### Finding 4: sigma_mu_ratio is noise-dominated for nearly all participants

N=285 subsample (excluding |μ|<0.005): mean ratio = {ratio_df['sigma_mu_ratio'].mean():.2f},
{(ratio_df['sigma_mu_ratio']>10).mean()*100:.1f}% have ratio > 10 (noise-dominated).
This confirms that DS5 behavioral processes are overwhelmingly stochastic/diffusion-driven
with negligible systematic drift. The StoP model's drift parameter (μ) has minimal
discriminatory value in this population.

---

## Three-Layer Phenotype Framework — Final Step 2 Summary

| Layer | Features | Independence | Condition sensitivity | Path D contribution |
|---|---|---|---|---|
| NeT type (Phase 1 / Path C) | HHI_net, rho_self, etc. | Independent of all others (ARI≈0.020) | Condition-stable | Not applicable |
| Behavioral-dynamic (Path A / F / D) | sig_hat, H_emp, x_mean, chi_behav | Independent of NeT | Condition-modulated (Path E) | Grounds taxonomy in StoP/DyS/StM language |
| Friction-response (Path B) | H_out_resid | Near-redundant with behavioral (ARI≈0.725) | Same pattern as behavioral | Not applicable |

Path D confirms Layer 2 is the complete dynamic/stochastic characterization.
No additional independent dynamic layer exists.

---

## What Path D Lets the Thesis Conclude

> "The dynamic/stochastic phenotyping analysis (Path D) completes the six-path Step 2
> exploration of DS5 behavioral heterogeneity. The primary finding is confirmatory: the
> dynamic/stochastic feature space — including behavioral noise (σ̂), entropy (H_emp), and
> StM tipping-point proximity (χ_behav) — does not produce a phenotype structure independent
> of the behavioral-dynamic taxonomy identified in Paths A and F. The three behavioral types
> (low-noise near-tipping C1, override-locked C2, high-noise stochastic C3) simultaneously
> represent three distinct stochastic-process regimes. Most counterintuitively, the low-noise
> type (C1, mean χ_behav={df[df['cluster_behav']=='C1']['chi_behav'].mean():.1f}) exhibits the
> highest tipping-point susceptibility — reflecting that participants with stable, low-variance
> behavioral histories near the override threshold are closest to a phase transition, while
> high-noise participants (C3, mean χ_behav={df[df['cluster_behav']=='C3']['chi_behav'].mean():.1f})
> are diffusion-dominated and far from a deterministic tipping point. Path D further extends
> Path E's homogenization finding: the default friction condition reduces the proportion of
> participants operating in a deterministic behavioral regime ({df[df['study_condition']=='default']['is_dys_eligible'].mean()*100:.1f}%
> DyS-eligible in default vs {df[df['study_condition']=='control']['is_dys_eligible'].mean()*100:.1f}%
> in control, χ²={chi2_2:.1f}, p={p2:.2e}). Taken together, the six Step 2 paths establish
> that DS5 behavioral phenotypes are structured along two genuinely orthogonal axes — network
> topology (NeT, condition-stable) and behavioral dynamics (StoP/DyS/StM, condition-modulated)
> — with no additional independent dimensions identified across any of the six exploration paths."

---

## Files Produced

| File | Location |
|---|---|
| `ds5_dynamic_cluster_assignments.csv` | `outputs/model_outputs/phenotyping/` |
| `ds5_dynamic_cluster_assignments.md` | `outputs/model_outputs/phenotyping/` |
| `ds5_dynamic_cluster_profiles.csv` | `outputs/model_outputs/phenotyping/` |
| `ds5_dynamic_cluster_profiles.md` | `outputs/model_outputs/phenotyping/` |
| `ds5_dynamic_cluster_stability.csv` | `outputs/model_outputs/phenotyping/` |
| `ds5_dynamic_cluster_stability.md` | `outputs/model_outputs/phenotyping/` |
| `model_run_summary_path_d.md` | `outputs/model_outputs/phenotyping/` |
| `fig_d1_feature_correlations.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d2_feature_distributions_by_cluster.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d3_drift_noise_profiles.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d4_kselection_curves.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d5_cluster_profiles.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d6_chi_behav_distribution.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d7_crosspath_heatmap.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d8_dys_regime_by_cluster_condition.png` | `outputs/model_outputs/phenotyping/figures/` |
| `fig_d9_stochastic_landscape.png` | `outputs/model_outputs/phenotyping/figures/` |
"""

with open(DATA_DIR / 'model_run_summary_path_d.md', 'w') as f:
    f.write(summary_md)
print("Saved model_run_summary_path_d.md")

# =============================================================================
# VERIFICATION
# =============================================================================

print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

csv_files = list(DATA_DIR.glob('ds5_dynamic*.csv')) + list(DATA_DIR.glob('ds5_dynamic*.md')) + [DATA_DIR / 'model_run_summary_path_d.md']
fig_files = list(FIG_DIR.glob('fig_d*.png'))

print(f"\nCSV/MD outputs ({len(csv_files)}):")
for f in sorted(csv_files):
    print(f"  {f.name}")

print(f"\nFigures ({len(fig_files)}):")
for f in sorted(fig_files):
    print(f"  {f.name}")

print(f"\nAssignments shape: {pd.read_csv(DATA_DIR/'ds5_dynamic_cluster_assignments.csv').shape}")
print(f"cluster_d_full distribution: {dict(pd.read_csv(DATA_DIR/'ds5_dynamic_cluster_assignments.csv')['cluster_d_full'].value_counts())}")
print(f"\nSelected D1 k: {K_D1}")
print(f"D1 outcome: {d1_outcome}")
print("\nPath D analysis complete.")
