# int_bridge_check.csv

## Contents
Per-participant validity record for the StM-InT sanity gate `H_joint >= max(H_app,
H_hour_bucket)`. Produced for auditability — this file exists because getting this bridge
right took two fixes during implementation (a comparability bug and an assertion-logic bug;
see `model_run_summary.md` "Two bugs found and fixed").

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `H_joint_baseline`, `H_joint_intervention` | float | From `participant_macrostate_metrics.csv` |
| `max_marginal_baseline`, `max_marginal_intervention` | float | max(H_app, H_hour_bucket) — H_app from InT (notebook 75), H_hour_bucket computed fresh in this notebook on the same 4-category partition as H_joint |
| `gate_valid_baseline`, `gate_valid_intervention` | bool / NaN | True if H_joint >= max_marginal − 1e-9; **NaN** if H_joint itself is missing — fixed 2026-08-06, see Known Limitations |

## Production
- Source: `participant_macrostate_metrics.csv` (this folder) + `outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv` (H_app only)
- Producing notebook: `notebooks/71_ds6_statistical_mechanics.ipynb`

## Cleaning / derivation steps applied
- `H_hour_bucket` computed fresh (NOT reused from InT's `H_hour`, which is on the full 24-value `hour_of_day` — comparing against that produced near-universal false violations on the first attempt; see `model_run_summary.md`).
- `gate_valid` computed via `np.where(H_joint.notna(), H_joint >= max_marginal - 1e-9, np.nan)` (fixed 2026-08-06 — see Known Limitations).

## Known limitations
- **Audit fix (2026-08-06):** an earlier version of this file stored `False` (not NaN) for
  the 3 participants per period with missing `H_joint`, because `NaN >= number` evaluates to
  `False` in pandas — a naive read of the file would have miscounted these as real gate
  violations. Fixed at the source. Current file: 240/243 show `True` per period, the
  remaining 3 show `NaN` (not applicable), **zero** `False` values.
- All 240 participants with valid H_joint pass the gate in both periods (verified) — if this file is ever regenerated and any row shows explicit `False`, treat it as a blocking bug before trusting downstream H_joint/susceptibility values.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/statistical_mechanics/int_bridge_check.csv'))
assert (df['gate_valid_baseline'] != False).all() and (df['gate_valid_intervention'] != False).all()
```
