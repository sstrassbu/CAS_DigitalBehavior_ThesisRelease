# ds5_dynamic_cluster_assignments.csv

**Unit of observation:** One row per participant
**Total rows:** 414 (StoP-eligible participants, complete behavioral features)
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
| `cluster_d_full` | str | Full-sample Path D cluster (D1 set), k=2 selected: D_sde1 (lower sig_hat) and D_sde2 (higher sig_hat) — or 'undifferentiated' if no stable solution. k=3 was rejected (min_cell=11), so no D_sde3 exists in this file. |
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
| D_sde1 | 172 | 0.1201 | 1.5401 | **31.59** | Deterministic — low diffusion, high StM susceptibility |
| D_sde2 | 242 | 0.2676 | 2.3850 | 8.20 | Stochastic — noise-dominated, far from a deterministic tipping point |

**Note:** chi_behav ordering is counterintuitive — the low-noise group has the highest
StM susceptibility purely because β=2/σ̂² is largest when σ is small (D_sde1 mean σ̂=0.120 vs
D_sde2 0.268). It is NOT a threshold-proximity effect: D_sde1's mean x_mean is 0.730, far from
the p=0.5 that maximizes χ=β·p·(1−p). (x_mean ≈ 0.36 is Path A's C1 mean, not D_sde1's.)

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
