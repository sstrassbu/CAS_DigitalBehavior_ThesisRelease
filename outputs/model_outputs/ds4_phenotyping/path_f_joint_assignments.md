# path_f_joint_assignments.csv

**Unit of observation:** one row per participant present in both Path A′ and Path C′
(641 — both used the identical complete-case population).

**Model:** DS4 Step 2, Path F′ — joint taxonomy crossing Path A′ (behavior, k=4) and
Path C′ (network, k=3).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `path_a_cluster` | int | Behavior-only cluster (0–3) |
| `path_c_cluster` | int | Network-focused cluster (0–2) |

---

## How this file was produced

- **Sources:** `path_a_feature_matrix.csv`, `path_c_feature_matrix.csv`
- **Producing notebook:** `notebooks/133_ds4_hierarchical_phenotype.ipynb`
- **Generator script:** `notebooks/make_133_ds4_path_f.py`
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Actual run results (2026-08-06)

Chi-square test of independence (see `path_f_joint_crosstab.md` for the full table):
**chi2=31.444, dof=6, p=2.08e-05 — the two axes are NOT statistically independent, but the association is weak (Cramér's V = 0.157).**
Despite Path A′ and Path C′ each having low ARI overlap with Phase 1 in different ways,
crossing them directly reveals real, non-random coupling — echoing Structured's own
Path F finding of a coupled (not fully independent) secondary dimension.

## Known limitations

- One of 12 cells has an expected count below 5 (4.3) — the standard chi-square
  reliability caveat; 1/12 (8.3%) is within the usual tolerance (rule of thumb: <20% of
  cells below 5), but noted rather than hidden.
- Same complete-case, no-condition caveats as Phase 1/Path A′/Path C′.

## How to load

```python
import pandas as pd

joint = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_f_joint_assignments.csv")
```
