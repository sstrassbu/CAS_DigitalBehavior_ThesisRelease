# path_a_feature_matrix.csv

**Unit of observation:** one row per complete-case DS4 participant (641 — same
population as Phase 1).

**Model:** DS4 Step 2, Path A′ — behavior-only phenotyping (drop NeT's `rho_self`).
Tests whether Phase 1's taxonomy depends on network structure.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `tau_hat`, `H_emp`, `fixed_point_deviation`, `chi_OU` | float | Raw feature values (StoP/InT/DyS/StM — same as Phase 1 minus NeT) (`fixed_point_deviation` is a coverage/estimation-noise diagnostic, not OU fit quality) |
| `path_a_cluster` | int | Cluster label, 0–3 (k=4, stability-first selection) |
| `phase1_cluster` | int | Phase 1's own cluster label (0–2, k=3), joined for comparison |

---

## How this file was produced

- **Sources:** DS4 StoP/InT/DyS/StM outputs + Phase 1's `ds4_cluster_assignments.csv`
- **Producing notebook:** `notebooks/131_ds4_behavior_only_phenotype.ipynb`
- **Generator script:** `notebooks/make_131_ds4_path_a.py`
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Actual run results (2026-08-06)

```
k=2: silhouette=0.2654, jaccard=0.7753 (STABLE)
k=3: silhouette=0.3315, jaccard=0.8874 (STABLE)
k=4: silhouette=0.3477, jaccard=0.8714 (STABLE)   <- chosen
k=5: silhouette=0.2819, jaccard=0.7957 (STABLE)
k=6: silhouette=0.2750, jaccard=0.7513 (STABLE)
```

Unlike Phase 1, **every candidate k was stable** here — no silhouette-vs-stability
conflict. k=4 chosen (highest silhouette among stable candidates).

Cluster sizes: 174/72/368/27.

**ARI(Path A′ k=4, Phase 1 k=3) = 0.664 — high.** Dropping the network feature barely
changes the taxonomy: DS4's phenotype space is primarily behavior/thermodynamics-driven,
not network-driven — opposite of DS5 (Phase 1 network-dominated, its own Path A
near-orthogonal at ARI=0.020) and different from Structured (fully behavior-dominated,
ARI=1.000). DS4 sits between the two.

## Known limitations

Same complete-case, no-condition, and daily-timescale caveats as Phase 1
(`ds4_phenotype_feature_matrix.md`). The 0.664 ARI number uses Path A′'s own
stability-first k=4, not an artificially forced k=3 — a same-k (k=3) comparison gives a
similar but not identical ARI (0.724, computed during planning, not the notebook's own
reported number — use 0.664 as the primary, executed figure).

## How to load

```python
import pandas as pd

path_a = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_a_feature_matrix.csv")
```
