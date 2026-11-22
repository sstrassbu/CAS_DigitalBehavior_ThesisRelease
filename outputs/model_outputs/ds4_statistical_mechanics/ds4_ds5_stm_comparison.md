# ds4_ds5_stm_comparison.csv

**Unit of observation:** one row per dataset (2 rows) — descriptive side-by-side
comparison of StM's central quantity, `beta`, between DS4 (exact) and DS5 (approximate).

**⚠ Not directly comparable in magnitude.** DS4's `beta_OU` and DS5's `beta_behav` come
from different underlying SDEs (OU mean-reverting vs constant-drift). This file is for
descriptive interest only, not a statistical test of a difference.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `dataset` | string | `"DS5 (approximate)"` or `"DS4 (exact, daily-scale)"` |
| `n` | int | Eligible participant count for that dataset's StM model |
| `median_beta` | float | Median `beta_behav` (DS5) or `beta_OU` (DS4) |
| `median_T` | float | Median `T_behav` (DS5) or `T_OU` (DS4) |

---

## How this file was produced

- **Sources:** `outputs/model_outputs/statistical_mechanics/participant_stm_parameters.csv`
  (DS5), `outputs/model_outputs/ds4_statistical_mechanics/participant_ds4_stm_parameters.csv` (DS4)
- **Producing notebook:** `notebooks/51_ds4_statistical_mechanics.ipynb`, cell 16
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md`

## Actual run results (2026-08-06)

```
dataset                        n  median_beta  median_T
DS5 (approximate)            414        60.90     0.016
DS4 (exact, daily-scale)     641        36.55     0.027
```

## Interpretation

DS5's `beta_behav` is higher (median 60.9) than DS4's `beta_OU` (median 36.5), but this
difference should not be read as "DS4 participants run hotter" — the two betas are
computed from different physical analogies (DS5's is an approximation over a
non-confining constant-drift process; DS4's is exact for a genuinely confining OU
process). No causal or magnitude claim is supported by this table alone.

## How to load

```python
import pandas as pd

comparison = pd.read_csv("outputs/model_outputs/ds4_statistical_mechanics/ds4_ds5_stm_comparison.csv")
```
