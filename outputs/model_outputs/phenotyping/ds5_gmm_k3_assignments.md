# ds5_gmm_k3_assignments.csv

**Produced by:** `notebooks/64_ds5_phenotype_v2_k3.ipynb` (DS5_02 Phase B follow-up, k=3 GMM)
**Depends on:** `ds5_phenotype_feature_matrix.csv`, `ds5_cluster_assignments.csv`,
`ds5_gmm_phase1_assignments.csv` (nb63)

## What this file contains

Per-participant GMM k=3 assignments. k=3 was chosen as an interpretability trade-off, **not** mandated
by BIC: the extended sweep (k=1-6) shows BIC decreasing monotonically through
k=6 (BIC at k=6=-370.1 < at k=3=-63.0). The nb63
"BIC minimum at k=3" claim was an artifact of stopping the sweep at k=5. k=3 is retained because it
produces three semantically distinct, very stable (bootstrap ARI=0.964) groups.
Groups labeled by HHI_net ascending: G1 (distributed), G2 (near-hub), G3 (fully hub-locked).

**Unit of observation:** one row per participant (414 total).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier |
| `study_condition` | str | RCT arm |
| `profile_k3` | str | GMM k=3 group (G1 / G2 / G3) |
| `prob_G1_k3` | float | Posterior P(G1) |
| `prob_G2_k3` | float | Posterior P(G2) |
| `prob_G3_k3` | float | Posterior P(G3) |
| `max_posterior_k3` | float | Max posterior across G1/G2/G3 (confidence) |
| `profile_p1` | str | DS5_01 k-means label (for comparison) |
| `profile_gmm` | str | GMM k=2 label from nb63 (for comparison) |

## Key results

| Group | N | HHI_net mean | rho_self mean | sig_hat mean | H_emp mean |
|---|---|---|---|---|---|
| G1 (distributed) | 153 | 0.595 | 0.795 | 0.196 | 2.014 |
| G2 (near-hub) | 57 | 0.978 | 0.988 | 0.237 | 2.133 |
| G3 (hub-locked) | 204 | 1.000 | 1.000 | 0.206 | 2.021 |

- **Bootstrap stability:** Median ARI=0.964 across 200 bootstrap runs — **VERY STABLE**
- **ARI(k=3, DS5_01 k-means) = 0.4914**
- **ARI(k=3, GMM k=2) = 0.7959** — k=3 is essentially splitting GMM k=2 Profile A into G1+G2
- **Ambiguous (max_posterior < 0.80): 1 participant(s) (0.2%)** — extremely sharp GMM assignments

**Cross-tab vs DS5_01 k-means and vs GMM k=2 (nb63):** see notebook Section 3 output (`ct_v1`, `ct_k2`).

## BIC/AIC findings (CORRECTED from nb63)

The extended sweep (k=1-6) shows BIC decreasing monotonically — no elbow or minimum within range:

| k | BIC | AIC |
|---|---|---|
| 1 | 5102.5 | 5022.0 |
| 2 | 215.4 | 50.4 |
| 3 | -63.0 | -312.6 |
| 4 | -269.6 | -603.8 |
| 5 | -324.7 | -743.4 |
| 6 | -370.1 | -873.3 |

The nb63 Phase B gate verdict's claim "BIC minimum at k=3" was an artifact of stopping at k=5.
**k=3 is retained as an interpretability choice** (three semantically distinct groups with stable
assignments), not as a statistically mandated solution. This must be stated explicitly in any write-up.

## Known limitations

- BIC does not mandate k=3 — choosing k=3 over k=6 is an interpretability decision that must be stated
- G2 (near-hub, N=57) is the smallest group; within-group feature variance is modest
- The intermediate G2 group has theoretically ambiguous meaning: near-ceiling HHI_net but not fully hub-locked
- Silhouette (k=3) = 0.0882 — low, reflecting ceiling features in PHASE1_CORE dominating the geometry
- Full covariance GMM with k=3 x p=5 features uses more parameters than k=2; variance-bias trade-off
- Also update the nb63 Phase B gate verdict: its "BIC minimum at k=3" claim is an artifact

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_gmm_k3_assignments.csv')
```
