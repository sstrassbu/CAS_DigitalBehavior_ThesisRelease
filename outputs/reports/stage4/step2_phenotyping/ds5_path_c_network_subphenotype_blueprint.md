# DS5 Step 2 Path C — Network-Structural Sub-Phenotyping Blueprint

**Notebook:** `101_ds5_network_subphenotype.ipynb`
**Written:** 2026-04-19
**Stage:** Stage 4, Step 2 — Path C (first of six paths)
**Depends on:** `100_phenotype_exploration.ipynb` outputs in `outputs/model_outputs/phenotyping/`
**Priority:** Execute first among all Step 2 paths

---

## 0. Why this notebook comes first

Phase 1 clustering found a k=2 solution where HHI_net and rho_self explained virtually all
the between-profile separation. Profile B (N=289, 70% of the sample) occupies the
near-ceiling region of both features (HHI_net median = 1.0, rho_self median = 1.0).

The unresolved question is: **Is Profile B behaviorally homogeneous, or does it contain
interpretable sub-types?**

Profile B is large enough (N=289) to support sub-clustering. The Phase 1 clustering was
tuned to maximize separation across the full feature space including behavior variables —
it was not designed to find fine-grained structure within a near-ceiling NeT segment.
This notebook is designed specifically for that question.

---

## 1. Theoretical motivation

From the paper's §4.2.4 (NeT behavioral framing), the relevant phenotype taxonomy for
hub-dominated users is:

- **Single-loop lockers:** One app dominates all transitions; essentially no network
  diversity; rho_self ≈ 1.0 AND HHI_net ≈ 1.0 AND H_trans ≈ 0
- **Multi-hub lockers:** Two or three apps share dominance; HHI_net still high but not
  at ceiling; some transition entropy exists between a small set of apps
- **Consistent returners:** Primarily hub-locked but with occasional diversification;
  rho_self high but H_trans slightly elevated

These are the types the paper anticipates but Phase 1 did not distinguish because the
full-sample k=2 was absorbing all of Profile B into one cluster.

Additionally, for Profile A (distributed network, N=125), a sub-analysis will test
whether the distributed-network users differ by degree of network diversity — i.e.,
whether there are "moderately distributed" vs. "highly distributed" sub-types.

---

## 2. Input files

| File | Used for |
|---|---|
| `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` | Phase 1 cluster labels — split population into Profile A / Profile B |
| `outputs/model_outputs/network_models/participant_network_metrics.csv` | All NeT features |
| `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | Behavior features for post-hoc overlay |
| `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` | H_emp, H_hour for overlay |

---

## 3. Feature specification

### 3.1 Primary clustering features (NeT-only)

| Feature | Role | Notes |
|---|---|---|
| `HHI_net` | PRIMARY | Bounded [0,1]; near-ceiling in Profile B |
| `rho_self` | PRIMARY | Bounded [0,1]; near-ceiling in Profile B |
| `H_trans` | PRIMARY | Conditional transition entropy; main discriminator within Profile B |
| `H_app` | PRIMARY | App diversity; correlated with H_trans via I_consec |
| `H_pi` | SECONDARY | Stationary entropy; N=378 only; use in supplementary sub-analysis |

**WARNING on collinearity:**
- I_consec = H_app − H_trans (exact arithmetic relationship)
- Never include all three simultaneously
- Use H_app AND H_trans (these two are the independent inputs)
- Report I_consec as a descriptive, not a clustering feature

**WARNING on near-ceiling features in Profile B:**
- Standard scaling will amplify tiny variance differences at the ceiling
- For Profile B sub-clustering: consider whether 1 − HHI_net and 1 − rho_self improve
  interpretation (distance from ceiling rather than raw value)
- Report raw values in profiles; use scaled values for clustering only

**IMPLEMENTATION FINDING (added 2026-04-19 after notebook 101 ran):**
- H_trans and H_app are zero-inflated within Profile B: 70.6% of Profile B participants
  (204/289) have H_trans=H_app=0 (pure single-app users with no inter-app transitions)
- This creates a discrete, not continuous, sub-structure; the k=2 split recovers this
  naturally: B1 (H_trans≈0) and B2 (H_trans>0, meaningful transition diversity)
- HHI_net and rho_self provide near-zero discriminating variance within Profile B;
  H_trans and H_app dominate the clustering after StandardScaler
- The "1−HHI" transformation is not needed in practice — H_trans/H_app carry the signal

### 3.2 Post-hoc overlay features (NOT used in clustering)

After clustering, overlay these to characterize the sub-profiles:
- `sig_hat`, `H_emp`, `x_mean` — does behavioral variability differ within sub-clusters?
- `study_condition` — are sub-clusters condition-independent?
- `chi_behav`, `H_out` — susceptibility and outcome variability (descriptive only)
- Psychosocial scales — FoMO, belonging, ostracism, digital wellbeing

---

## 4. Analysis populations

### 4.1 Primary analysis: Profile B sub-clustering

- Load Phase 1 cluster assignments from `ds5_cluster_assignments.csv`
- Filter to Profile B (N=289 in Phase 1 solution)
- Merge with NeT features; retain participants with complete NeT data
- Expected N: ~250–280 (NeT-eligible subset of Profile B)

### 4.2 Secondary analysis: Profile A sub-clustering

- Same process; Profile A N=125
- Expected N: ~100–115
- NOTE: small N; interpret with caution; bootstrap stability is mandatory

### 4.3 Full NeT-eligible sample (robustness)

- Run NeT-only clustering on all N=463 NeT-eligible participants (not split by Phase 1)
- Compare resulting cluster assignments with Phase 1 assignments using ARI
- This tests whether Phase 1 network structure split is reproducible without condition on
  behavior features

---

## 5. Analysis plan

### Step 1 — Descriptive: within-Profile variance inspection

Before clustering, inspect the variance of NeT features within Profile B:
- For each NeT feature: compute mean, std, IQR within Profile B
- For HHI_net and rho_self: many values will be exactly 1.0; report proportion at ceiling
- For H_trans and H_app: these should show more variance; plot histograms
- PCA within Profile B: how many components explain 80% of variance?
  (If 1 component explains 90%, clustering will be 1-dimensional and trivial)

**Decision gate:** If Profile B variance is extremely low across all NeT features
(e.g., all std < 0.05), report this as a finding ("Profile B is behaviorally
homogeneous at the NeT level") and do NOT force sub-clusters.

### Step 2 — Feature scaling

- StandardScaler on the primary NeT features within Profile B (fit on Profile B only)
- Re-fit separately on Profile A
- Store scalers for reproducibility

### Step 3 — Sub-cluster selection within Profile B

For k in [2, 3, 4]:
- K-means (k-means++ init, 10 seeds, random_state=42)
- Compute: silhouette, Calinski-Harabasz, Davies-Bouldin, min cluster size
- Bootstrap Jaccard stability (100 bootstraps, 80% sample) for top candidate k

**Minimum acceptable size:** N ≥ 30 per sub-cluster for interpretable profiles.
If k=3 produces a cluster with N < 30, report k=2 as the sub-cluster solution.

### Step 4 — Sub-cluster profiles within Profile B

For the selected k:
- Mean and median of all NeT features per sub-cluster (clustering features)
- Mean and median of behavior overlay features (sig_hat, H_emp, x_mean) per sub-cluster
- Condition distribution χ² test (sub-cluster × condition)
- Psychosocial Kruskal-Wallis tests (same 5 scales as Phase 1; Bonferroni correction)

### Step 5 — Same analysis for Profile A

- Repeat Steps 1–4 for Profile A sub-clustering
- Report whether a meaningful sub-structure exists or not
- NOTE: Profile A is smaller; k=2 is the maximum meaningful sub-cluster count here

### Step 6 — Full-sample NeT-only clustering (robustness)

- Run k-means on all N=463 NeT-eligible participants using NeT features only
- k selection: same procedure as above
- Compute ARI(NeT-only full-sample cluster labels vs. Phase 1 cluster labels)
- High ARI → network structure drives Phase 1 results even before behavior features
- Low ARI → behavior features were contributing more than it appeared

### Step 7 — H_pi supplementary sub-analysis

- Restrict to the N=378 stationary-eligible participants
- Add H_pi to the Profile B sub-clustering feature set
- Compare: does H_pi (stationary distribution entropy) change the sub-cluster structure?
- Report ARI between H_pi-inclusive and H_pi-exclusive solutions

---

## 6. Figures to produce

| Figure | Content |
|---|---|
| `fig_c1_profileB_net_distributions.png` | Histograms of HHI_net, rho_self, H_trans, H_app within Profile B — show variance structure |
| `fig_c2_profileB_pca.png` | PCA biplot within Profile B — shows effective dimensionality |
| `fig_c3_profileB_subcluster_selection.png` | Silhouette, CH, DB vs. k for Profile B sub-clustering |
| `fig_c4_profileB_subcluster_profiles.png` | Radar or bar chart of sub-cluster profiles on NeT features |
| `fig_c5_profileB_overlay.png` | Overlay of sig_hat, H_emp, x_mean across sub-clusters |
| `fig_c6_profileA_subcluster.png` | Profile A sub-cluster analysis (condensed; single figure) |
| `fig_c7_fullsample_net_only.png` | Full-sample NeT-only clustering solution and comparison with Phase 1 |

---

## 7. Output files

| File | Content |
|---|---|
| `ds5_net_subcluster_assignments.csv` | Per-participant sub-cluster labels for Profile B, Profile A, and full NeT-only solution |
| `ds5_net_subcluster_profiles.csv` | Mean/median of all features per sub-cluster |
| `ds5_net_subcluster_stability.csv` | Bootstrap Jaccard scores for each k and each analysis population |
| Companion `ds5_net_subcluster_assignments.md` | Required output documentation |
| Companion `ds5_net_subcluster_profiles.md` | Required output documentation |

All files → `outputs/model_outputs/phenotyping/`

---

## 8. Expected findings and interpretation guidance

**Most likely outcome — Profile B:**
k=2 or k=3 sub-structure within Profile B, driven by H_trans. Expected sub-profiles:
- B1: Pure single-app lockers (H_trans ≈ 0, H_app ≈ 0, rho_self = 1.0, HHI_net = 1.0)
- B2: Multi-app returners (H_trans slightly > 0, H_app slightly > 0, but HHI still high)
- If k=3: B3 = transitional cases between B and Profile A

**Alternative outcome — Profile B is truly homogeneous:**
If variance is near zero across all NeT features within Profile B, report that the k=2
Phase 1 solution correctly identifies the hub-locked group as a single behavioral type
at the network level. This is still a finding — it means the hub-lock is a floor/ceiling
effect, not a gradient.

**Most likely outcome — Profile A:**
Weaker sub-structure. Profile A already has genuine network diversity (H_app ≈ 1.05,
H_trans ≈ 0.79). A k=2 split may yield "moderately distributed" vs. "highly distributed"
sub-types, but stability may be low. Report honestly.

**Theoretical label guide (use cautiously):**
- B1 type: "Habitual single-loop" — one app, always returns, no network
- B2 type: "Hub-anchored multi-app" — one dominant app, occasional others
- A1 type: "Network explorer" — genuinely distributed across apps
- A2 type (if found): "Moderate network user" — distributed but less than A1

---

## ACTUAL RESULTS (notebook 101 run 2026-04-19)

**Profile B sub-clustering (k=2; silhouette=0.866; Jaccard=0.996 STABLE):**
- B1: N=260 (89.9%) — HHI=0.995, rho=0.998, H_trans=0.010, H_app=0.018
  → Single/near-single-app locked; 70.6% have exactly H_trans=H_app=0
- B2: N=29 (10.1%) — HHI=0.821, rho=0.946, H_trans=0.230, H_app=0.475
  → Multi-app hub-anchored; genuine but limited transition diversity
  ⚠ N=29 is just below the 30-participant threshold; stability=0.996 justifies inclusion
- Condition χ²=4.567, p=0.1019 → phenotype independent of friction condition ✓
- Psychosocial: 0/5 significant after Bonferroni ✓
- Behavioral overlay (sig_hat, H_emp, x_mean): small differences between B1 and B2 — x_mean (KW p=0.0136) and H_emp (p=0.0420) are nominally significant uncorrected, sig_hat is not (p=0.1344); none survives a 3-test Bonferroni correction (α=0.0167)
  → Network sub-structure is not accompanied by behavioral-dynamic differences

**Profile A sub-clustering (k=2; Jaccard=0.835 STABLE but std=0.157 wide):**
- A1: N=85 (68%) — HHI=0.599, H_trans=0.649 → moderately distributed
- A2: N=40 (32%) — HHI=0.429, H_trans=1.087 → highly distributed
- Tentative — report with stability caveat

**Full-sample NeT-only robustness (k=2; Jaccard=0.994; ARI vs Phase 1 = 0.990):**
→ Phase 1 network split is almost perfectly reproduced from NeT features alone.
  Behavior features (sig_hat, H_emp, x_mean) amplified but did not create the split.

**H_pi supplementary (ARI vs H_pi-exclusive = 0.948):**
→ Adding stationary distribution entropy does not change the sub-cluster structure.

All labels are descriptive, not diagnostic. Add uncertainty qualifiers.

---

## 9. What this notebook does NOT do

- Does NOT use condition as a clustering feature
- Does NOT test intervention effects within clusters (Step 3)
- Does NOT prescribe friction types
- Does NOT make claims about stability across datasets (DS4 replication is later)
- Does NOT treat sub-cluster labels as validated behavioral traits —
  these are exploratory, DS5-specific, and require replication

---

## 10. Connections to later paths

| Path | How this notebook feeds it |
|---|---|
| Path A (behavior-only) | Knowing Profile B is homogeneous vs. heterogeneous at NeT level informs whether A needs to sub-cluster within network-type groups |
| Path F (hierarchical) | Profile B sub-cluster labels become the Stage 1 → Stage 2 first-level split |
| Path E (condition-stratified) | Sub-cluster assignments will be used as the fine-grained unit for condition × cluster interaction |
| GaT / ABM (Step 3 prep) | Sub-cluster types define the behavioral agent types: single-loop vs. hub-anchored vs. explorer |
