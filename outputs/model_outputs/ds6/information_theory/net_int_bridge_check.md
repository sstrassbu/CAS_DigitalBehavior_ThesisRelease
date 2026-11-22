# net_int_bridge_check.csv

## Contents
Per-participant validity record for the NeT-InT bridge identity `I_consec = H_app_marginal
− H_trans`. Produced specifically to make the bridge verification auditable — this file
exists because getting this bridge right took two failed attempts during implementation
(see `model_run_summary.md`).

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `H_app_marginal_baseline`, `H_app_marginal_intervention` | float | Entropy of the transition edge list's `app_to` marginal, per period |
| `I_consec_baseline`, `I_consec_intervention` | float | H_app_marginal − H_trans |
| `H_trans_baseline`, `H_trans_intervention` | float | From NeT's `participant_network_metrics.csv` |
| `bridge_valid_baseline`, `bridge_valid_intervention` | bool / NaN | True if I_consec >= -1e-9 (the mandatory sanity gate); **NaN** if I_consec itself is NaN (participant NeT-ineligible that period) — fixed 2026-08-06, see Known Limitations |

## Production
- Source: `participant_entropy_metrics.csv` (this folder) + `outputs/model_outputs/ds6/network_models/participant_network_metrics.csv`
- Producing notebook: `notebooks/75_ds6_information_theory.ipynb`

## Cleaning / derivation steps applied
- H_app_marginal computed from `outputs/model_outputs/ds6/network_models/transition_edge_list.csv`'s `app_to` column (destination marginal) — required after two earlier attempts (Stage 1 `app_entropy`, then the `app_from` marginal) both failed the `I_consec >= 0` mandatory gate. See `model_run_summary.md` "Bug found and fixed" section for the full diagnostic trail.
- `bridge_valid_*` computed via `np.where(I_consec.notna(), I_consec >= -1e-9, np.nan)` (fixed 2026-08-06 — see Known Limitations).

## Known limitations
- **Audit fix (2026-08-06):** an earlier version of this file stored `False` (not NaN) for
  the 4 (baseline) / 8 (intervention) participant-periods where `I_consec` is NaN
  (NeT-ineligible that period), because `NaN >= -1e-9` evaluates to `False` in pandas. A
  naive read of the file would have miscounted these as real bridge violations. Fixed at
  the source; current file: 239/243 (baseline) and 235/243 (intervention) show `True`, the
  remainder `NaN` (not applicable), **zero** `False` values. If this file is ever
  regenerated and any row shows explicit `False`, treat it as a blocking bug.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/information_theory/net_int_bridge_check.csv'))
assert (df['bridge_valid_baseline'] != False).all() and (df['bridge_valid_intervention'] != False).all()
```
