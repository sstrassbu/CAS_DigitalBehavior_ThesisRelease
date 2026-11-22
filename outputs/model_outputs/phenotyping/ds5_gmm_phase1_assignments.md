# ds5_gmm_phase1_assignments.csv

**Produced by:** `notebooks/63_ds5_phenotype_v2.ipynb` (DS5_02 Phase B, Track 1)  
**Depends on:** `ds5_phenotype_feature_matrix.csv`, `ds5_cluster_assignments.csv`  
**Supersedes:** Does NOT replace `ds5_cluster_assignments.csv` (DS5_01 k-means baseline, kept intact)

## What this file contains

Per-participant GMM soft cluster assignments for the Phase B algorithm stress test.
Replaces k-means hard assignment (DS5_01 FLAG P2) with GaussianMixture k=2 (full covariance)
on the same original Phase 1 features.

**Unit of observation:** one row per participant (414 total — same as DS5_01 Phase 1 population).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier (primary key) |
| `profile_gmm` | str | GMM hard label (Profile A / Profile B), aligned by majority vote to DS5_01 |
| `prob_profile_a_gmm` | float | GMM posterior P(Profile A) — continuous soft membership score |
| `study_condition` | str | control / default / reintervention |
| `profile_p1` | str | DS5_01 k-means label (Profile A / Profile B) — for direct comparison |

## Key results (Track 1)

**ARI(GMM, k-means) = 0.3460** — MATERIAL CHANGE (< 0.70 threshold).

**Cross-tabulation (DS5_01 rows, GMM columns):**

| DS5_01 k-means | GMM Profile A | GMM Profile B |
|---|---|---|
| Profile A (N=125) | **125** | 0 |
| Profile B (N=289) | **85** | 204 |

**Interpretation:**
- All 125 DS5_01 Profile A participants retained in GMM Profile A (100% agreement).
- 85/289 DS5_01 Profile B participants reassigned to GMM Profile A (29.4% of Profile B).
- GMM Profile A expands from 125 → 210 (30.2% → 50.7% of population).
- Mechanism: k-means was dominated by HHI_net/rho_self ceiling (Profile B = HHI_net=1.0). GMM's
  full covariance allows less extreme rho_self/HHI_net participants with Profile-A-like noise/entropy
  to cross the boundary.

**BIC/AIC diagnostic (FLAG B2):**
- k=1 BIC=5102.5, k=2 BIC=215.4, k=3 BIC=-63.0, k=4 BIC=-177.6, k=5 BIC=-210.4
- **CORRECTED (see nb64 / `ds5_gmm_k3_assignments.md`):** this table does not show a minimum at
  k=3 — k=5 (-210.4) is lower. nb64's extended sweep through k=6 (BIC=-370.1) confirmed BIC
  decreases monotonically with no elbow in range. The original claim below ("BIC minimum is at
  k=3") was an artifact of stopping at k=5 and is superseded. k=2 was chosen to maintain
  comparability with DS5_01 Phase 1.
- This is an honest limitation: information criteria do not support k=2 as the optimal solution,
  nor do they single out any other k in range as optimal — see nb64 for the corrected framing.

**Soft membership (P(Profile A)):**
- Distribution is bimodal: most participants have P≈0 or P≈1.
- Ambiguous participants (0.20 < P < 0.80): few — two-group structure is real despite different boundary.

**Silhouette (GMM k=2): 0.1802** — low, consistent with naturally overlapping distributions.

## Known limitations

- ARI = 0.346 means GMM substantially disagrees with k-means — neither is "correct", they answer
  different questions (soft vs. hard boundary).
- **CORRECTED:** this bullet originally read "BIC minimum at k=3 (not k=2) suggests a 3-group
  solution may better fit the data — deferred to Phase C if explicitly requested." nb64 has since
  run that follow-up and found BIC decreases monotonically through k=6 (no minimum in range); k=3
  was retained there as an interpretability choice, not a BIC-mandated one. See
  `ds5_gmm_k3_assignments.md`.
- `profile_gmm` label is anchored to DS5_01 by majority vote; Profile A content changed.

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_gmm_phase1_assignments.csv')
# Use prob_profile_a_gmm for continuous profiling
# Use profile_gmm for group-level comparisons comparable to DS5_01
```
