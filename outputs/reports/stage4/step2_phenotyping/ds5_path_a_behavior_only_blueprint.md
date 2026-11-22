# DS5 Step 2 Path A — Behavior-Only Phenotyping Blueprint

**Notebook:** `102_ds5_behavior_only_phenotype.ipynb`
**Written:** 2026-04-19
**Stage:** Stage 4, Step 2 — Path A (second of six paths)
**Depends on:**
- `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` — behavior features
- `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` — Phase 1 labels (post-hoc overlay)
- `outputs/model_outputs/phenotyping/ds5_net_subcluster_assignments.csv` — Path C sub-labels (post-hoc comparison)

---

## 0. Why this notebook comes second

Path C established that the Phase 1 k=2 split is driven almost entirely by NeT features
(ARI of NeT-only full-sample solution vs. Phase 1 = 0.990). The behavioral features
sig_hat, H_emp, x_mean show only small mean differences across all four Path C sub-profiles
(four-group Kruskal-Wallis p=0.031 / 0.042 / 0.059, none surviving a 3-test correction)
(B1, B2, A1, A2).

The unresolved question is: **Does a genuinely different phenotype structure emerge when
network topology is excluded entirely?**

If the behavioral dynamics axes (variability, entropy, override tendency) have their own
grouping structure, it is orthogonal to the network topology structure — and both
dimensions jointly define the full behavioral phenotype space that Path F will synthesize
hierarchically.

If behavior-only clustering yields weak structure (low silhouette, unstable partitions),
that is also a finding: it means behavioral dynamics are approximately continuous in DS5
and the dominant axis of individual difference is structural (network-topological), not
dynamical.

---

## 1. Theoretical motivation

The core behavior features map onto distinct theoretical model families:

- `sig_hat` (StoP / OU noise / diffusion parameter): how unpredictably a participant
  responds to each friction event; high sig_hat = high within-person variability; a
  measure of impulsivity or weak attractor structure
- `H_emp` (InT / behavioral entropy): Shannon entropy (bits) of the K=10-binned daily
  X_t series, where X_t = n_opened / n_events on day t; high H_emp = the participant's
  daily override rate ranges widely across days; correlated with sig_hat (r=0.538) but
  not identical. **NOTE:** entropy over the outcome space {opened, dismissed, closed}
  is `H_out`, a *different* feature — see
  `outputs/model_outputs/information_theory/participant_entropy_metrics.md`.
- `x_mean` (StoP / mean override rate): the time-average of the same daily X_t series;
  a summary individual-difference measure of friction compliance
- `H_hour` (InT / temporal entropy): how uniformly friction events are distributed
  across hours of day; captures circadian structure of phone use; independent from
  sig_hat/H_emp in theory but r=−0.510 with sig_hat in DS5 (see below)

**Theoretical expectation:**
The primary separation, if any, will come from sig_hat and H_emp (diffusion vs. entropy
axis). x_mean may add a secondary compliance dimension. H_hour may contribute a
temporal regularity axis that is partially correlated with the sig_hat axis.

**Caveat on "three independent axes":** sig_hat, H_emp and x_mean are all summary
statistics of the *same* univariate series X_t — its increment standard deviation, its
binned distributional entropy, and its mean. r(sig_hat, H_emp)=0.538,
r(H_emp, x_mean)=−0.251; PCA on the three gives PC1=54.0%, PC2=31.7%, PC3=14.3%. So
"behavior-only" here means three moments of one behavioral signal, not three independent
theoretical constructs; the collinearity screen in §3.2 (which flags only H_hour at
r=−0.510) does not capture this.

---

## 2. Input files

| File | Used for |
|---|---|
| `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` | All behavior features (sig_hat, H_emp, x_mean, H_hour, mu_hat, sigma_mu_ratio) |
| `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` | Phase 1 labels — post-hoc overlay only |
| `outputs/model_outputs/phenotyping/ds5_net_subcluster_assignments.csv` | Path C sub-cluster labels — post-hoc ARI comparison |

---

## 3. Feature specification

### 3.1 Core clustering features (minimal, clean)

| Feature | Role | Notes |
|---|---|---|
| `sig_hat` | PRIMARY | Noise / diffusion; no NaN; N=414 complete |
| `H_emp` | PRIMARY | Behavioral entropy; no NaN; N=414 complete |
| `x_mean` | PRIMARY | Mean override rate; no NaN; N=414 complete |

These three are the minimal core. They are complete for all 414 participants and cover
the three main theoretical axes (noise, entropy, compliance).

### 3.2 Secondary sensitivity feature

| Feature | Role | Notes |
|---|---|---|
| `H_hour` | SECONDARY | Temporal entropy; no NaN; N=414 complete |

**Critical collinearity warning:**
`H_hour` has r=−0.510 with `sig_hat` in DS5. This is a strong negative relationship:
participants with high noise (sig_hat) tend to have lower temporal spread (H_hour).
This may reflect that high-impulsivity participants concentrate their usage in shorter
bursts. If H_hour is included in the clustering feature set, it partially duplicates
sig_hat's discriminative axis. Include only in a sensitivity run (not the primary solution).

### 3.3 Post-hoc overlay features (NOT used in clustering)

After clustering, overlay these for interpretation:
- `mu_hat` — behavioral drift: 56.5% near-zero (|mu_hat|<0.01); not discriminative
  in DS5; report distributional statistics only
- `sigma_mu_ratio` — impulsivity ratio: 31.2% NaN; overlay on the subset where available
- `H_hour` — if not used in clustering, overlay to characterize temporal habits
- `study_condition` — χ² test: are clusters condition-independent?
- `chi_behav` — susceptibility overlay
- `H_out_resid` — condition-residualized friction outcome entropy (do not use raw H_out)
- Psychosocial scales (from `ds5_psychosocial_overlays.csv`) — Kruskal-Wallis
- Phase 1 profile assignments (`profile_p1`) — ARI comparison
- Path C sub-cluster labels (`subprofile_B`, `subprofile_A`, `cluster_net_only`) — ARI

**Features to EXCLUDE from clustering entirely:**
- All NeT features (HHI_net, rho_self, H_trans, H_app, H_pi, I_consec, top1_share_net)
- `H_out` raw (condition-confounded)

> **Known inconsistency in this exclusion rule (documented, not resolved).** The
> "condition-confounded" criterion is applied only to `H_out`. Measured on the same
> N=414 feature matrix, the three PRIMARY features are themselves condition-loaded —
> `H_emp` η²=0.244 (F=66.31, p=1.1e-25), `x_mean` η²=0.127 (F=29.78, p=8.3e-13),
> `sig_hat` η²=0.074 (F=16.54, p=1.2e-07) — and `H_emp`'s condition-explained variance
> is in fact *larger* than `H_out`'s (η²=0.155, F=37.63, p=9.8e-16). No residualized
> version of the three core features was built, so the resulting clusters are strongly
> condition-associated (χ²=91.885, p=5.2e-19). The split is dominated by `x_mean`
> (standardized centroid range 2.63), ahead of `H_emp` (1.56) and `sig_hat` (1.44).
> Any DS4/DS6 Path A analogue should either residualize all clustering features on
> condition or drop the "condition-confounded" wording as the reason for excluding
> `H_out`.

- Redundant transforms (H_SDE, beta_behav, chi_behav.1, F_behav, four_model_convergent)
- `sigma_mu_ratio` (31.2% NaN — reduces N to ~285)
- `mu_hat` (56.5% near-zero — expected no discriminative value)

---

## 4. Analysis population

- All N=414 StoP-eligible participants with complete behavior features
- No sub-population split (this path is full-sample)
- If sensitivity run with H_hour is included: same N=414 (H_hour has no NaN)

---

## 5. Analysis plan

### Step 1 — Descriptive: behavior-only feature space inspection

Before clustering, inspect:
- Univariate distributions: histograms for sig_hat, H_emp, x_mean, H_hour
- Pairwise scatter plots: sig_hat vs. H_emp, sig_hat vs. x_mean, H_emp vs. x_mean
- PCA on [sig_hat, H_emp, x_mean]: how many components explain 80% of variance?
  (If PC1 explains >90%, clustering will be effectively 1-dimensional)
- Correlation matrix: confirm sig_hat–H_hour = −0.510 and document other correlations
- Overlay Phase 1 profile labels to visualize where Profile A / Profile B participants
  sit in the behavior-only feature space — do they separate or overlap?

**Decision gate:** If variance across all three features is extremely low relative to their
scale (i.e., the distribution is tightly unimodal on all axes), report "behavior-only space
has insufficient heterogeneity for meaningful cluster extraction in DS5" and document this
as the Path A finding. Do NOT force clusters.

### Step 2 — Feature scaling

- StandardScaler on [sig_hat, H_emp, x_mean] for the primary analysis
  (fit on full N=414 sample)
- Store scaler for reproducibility

### Step 3 — Cluster selection on core 3-feature set

For k in [2, 3, 4]:
- K-means (k-means++ init, n_init=10, random_state=42)
- Compute: silhouette, Calinski-Harabasz, Davies-Bouldin, min cluster size
- Bootstrap Jaccard stability (100 bootstraps, 80% sample) for top candidate k

**Minimum acceptable size:** N ≥ 30 per cluster.
If no k has all clusters ≥ 30, report k=2 as fallback with explicit caveat.

**Silhouette baseline expectation:** Path A may yield lower silhouette scores than
Path C (Phase 1 silhouette was driven by NeT features). If silhouette < 0.30 for all k,
treat this as a weak-structure finding and report honestly.

### Step 4 — Sensitivity run with H_hour

- Add H_hour to the clustering feature set: [sig_hat, H_emp, x_mean, H_hour]
- Run the same k-selection procedure
- Report:
  - ARI(4-feature solution vs. 3-feature solution) — how much does H_hour change assignments?
  - Whether H_hour adds a genuinely new cluster dimension or absorbs variance from sig_hat

### Step 5 — Cluster profiles on behavior features

For the selected k (3-feature primary solution):
- Mean and median of all behavior features per cluster (sig_hat, H_emp, x_mean, H_hour)
- Mean and median of overlay features: mu_hat (where not NaN), sigma_mu_ratio (subset)
- Condition distribution χ² test (cluster × condition)
- Psychosocial Kruskal-Wallis (Bonferroni correction; 5 scales same as Phase 1)
- H_out_resid overlay: does condition-residualized friction outcome entropy differ across
  behavior-only clusters?

### Step 6 — Cross-path comparison: Path A vs. Phase 1 and Path C

This is the core comparison that differentiates Path A from Phase 1.

**Comparison 1:** ARI(Path A cluster vs. Phase 1 cluster)
- If ARI is high (>0.5): behavior-only clustering mostly reproduces the NeT-driven split
  (behavior and network co-vary strongly → no new information from Path A)
- If ARI is low (<0.2): behavior-only clustering reveals a genuinely orthogonal structure
  (behavior and network are independent dimensions → Path F is essential)
- If intermediate: partial overlap; report mixed structure honestly

**Comparison 2:** ARI(Path A cluster vs. Path C network sub-clusters)
- Compare against the composite Path C label combining profile_p1 and sub-profile
  (e.g., B1, B2, A1, A2 as a 4-class variable)

**Comparison 3:** Contingency table (Path A cluster × Phase 1 profile)
- Cross-tabulate to identify whether one Path A cluster is disproportionately Profile B or A
- If cluster 1 is 85% Profile B: behavior-only just recovered the network split via
  correlated features (even after excluding NeT features, H_emp and x_mean may retain
  some correlation with network type)

Report these three comparisons in a dedicated section with explicit interpretation.

---

## 6. Figures to produce

| Figure | Content |
|---|---|
| `fig_a1_behav_only_distributions.png` | Histograms of sig_hat, H_emp, x_mean, H_hour (4-panel) |
| `fig_a2_behav_pairplot.png` | Pairwise scatter plots with Phase 1 profile overlay (color by Profile A/B) |
| `fig_a3_behav_pca.png` | PCA biplot on [sig_hat, H_emp, x_mean] showing effective dimensionality |
| `fig_a4_cluster_selection.png` | Silhouette, CH, DB vs. k for primary 3-feature clustering |
| `fig_a5_cluster_profiles.png` | Radar or grouped bar chart of cluster profiles on behavior features |
| `fig_a6_cluster_overlay.png` | Overlay of mu_hat, sigma_mu_ratio, H_out_resid, condition distribution |
| `fig_a7_crosspath_comparison.png` | Sankey or stacked bar showing Path A clusters × Phase 1 profile |

---

## 7. Output files

| File | Content |
|---|---|
| `ds5_behav_only_cluster_assignments.csv` | Per-participant cluster labels + Path C labels for ARI |
| `ds5_behav_only_cluster_profiles.csv` | Mean/median of all features per cluster |
| `ds5_behav_only_cluster_stability.csv` | Bootstrap Jaccard scores (3-feature, 4-feature, sensitivity) |
| Companion `ds5_behav_only_cluster_assignments.md` | Required output documentation |
| Companion `ds5_behav_only_cluster_profiles.md` | Required output documentation |
| `model_run_summary_path_a.md` | Complete run record with all parameters and key numbers |

All files → `outputs/model_outputs/phenotyping/`
Figures → `outputs/model_outputs/phenotyping/figures/`

---

## 8. Expected findings and interpretation guidance

**Scenario 1 — Behavior-only has genuine structure (likely: moderate):**
- Expected: k=2 solution with moderate silhouette (0.30–0.55)
- Dominant axis: sig_hat / H_emp (diffusion and entropy co-vary; r=0.538)
- Low-entropy / low-noise group: consistent, low-variability friction responses
- High-entropy / high-noise group: variable friction responses, higher x_mean
- ARI vs. Phase 1: likely LOW (0.1–0.3) — network type and behavioral dynamics are
  partially independent dimensions

**Scenario 2 — Weak structure (possible):**
- Silhouette < 0.30 for all k; no stable partition
- Report this as the finding: "In DS5, behavioral dynamics (sig_hat, H_emp, x_mean)
  do not form a discrete phenotype structure. The feature space is approximately
  continuous."
- This does NOT invalidate Step 2 — it makes Path F more theoretically important by
  showing that network structure is the only dimension that yields discrete types

**Scenario 3 — Behavior-only reproduces network split (unlikely based on Path C):**
- If ARI(Path A vs. Phase 1) > 0.5: behavioral features, despite not including NeT,
  are strongly correlated with network structure
- Investigate via contingency table which behavior features are driving the overlap
- This would suggest behavioral dynamics and network topology are not orthogonal in DS5

**Label guidance (use cautiously — all exploratory):**
- Low-sig_hat / low-H_emp cluster: "Behaviorally stable" — consistent friction responses
- High-sig_hat / high-H_emp cluster: "Behaviorally variable" — noisy, entropy-rich
- If x_mean clearly separates: "High-compliance" vs. "Low-compliance" variant possible

---

## 9. What this notebook does NOT do

- Does NOT use NeT features at any point (not even for stratification)
- Does NOT treat condition as a clustering feature
- Does NOT use raw H_out (condition-confounded)
- Does NOT make causal claims (behavior-only clusters describe patterns, not causes)
- Does NOT prescribe friction types (Step 3)
- Does NOT claim DS5 behavior-only clusters generalize across datasets

---

## 10. Connections to later paths

| Path | How this notebook feeds it |
|---|---|
| Path F (hierarchical) | Behavior-only cluster labels become the Stage 2 sub-split within each NeT-type group; ARI between Path A and Phase 1 determines whether hierarchical decomposition adds information |
| Path E (condition-stratified) | Behavior-only solution provides a baseline for "does friction change behavioral cluster structure?" |
| Path B (intervention-sensitive) | sig_hat and x_mean from this path connect to friction response variability |
| GaT / ABM (Step 3 prep) | Behavior-only cluster types define agent noise/compliance parameters independently of network topology |

---

## 11. Key numbers from prior paths (for comparison)

| Metric | Path C (NeT-only) | Phase 1 (joint) |
|---|---|---|
| Best k | 2 (within each sub-population) | 2 (full sample) |
| Best silhouette | 0.866 (Profile B) | Not reported |
| Bootstrap Jaccard | 0.996 / 0.835 | 0.995 |
| ARI vs. Phase 1 | 0.990 (full-sample NeT-only) | — |
| Behavioral features differ? | No (B1/B2/A1/A2 near-identical) | No |

Path A is designed to find structure in the dimension where both Phase 1 and Path C
found none. Low silhouette is therefore the expected baseline, not a failure.
