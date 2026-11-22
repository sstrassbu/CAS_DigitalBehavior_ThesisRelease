# feedback_loop_tests.csv

## Contents
Results of the two paper-grounded feedback-loop hypothesis tests — the core deliverable of
this notebook. Each row reports both the raw correlation and the partial correlation
(controlling for the corresponding baseline psychosocial level), per the
regression-to-the-mean caution in the blueprint.

## Unit of observation
One row per (loop × flow variable) test (3 rows: Loop 1 tested with two flow variables,
Loop 2 with one).

## Column reference

| Column | Type | Description |
|---|---|---|
| `loop` | str | Loop1_pressure_reinforcement or Loop2_self_regulation_correction |
| `flow` | str | Behavioral flow variable used (mean_N_baseline, mu_hat_baseline, or volume_change) |
| `outcome` | str | Psychosocial change variable (addiction_index_change or self_control_index_change) |
| `n_raw`, `n_partial` | int | Complete-case N for the raw / partial test |
| `r_raw`, `p_raw` | float | Raw Pearson correlation and p-value |
| `r_partial`, `p_partial` | float | Partial correlation and p-value, controlling for the outcome's own baseline (pre) level |

## Production
- Source: `participant_stock_flow.csv` (this folder)
- Producing notebook: `notebooks/78_ds6_system_dynamics.ipynb`

## Cleaning / derivation steps applied
- Partial correlation via residualization: both the flow variable and the outcome are regressed (simple linear) on the baseline level, and the residuals' Pearson correlation is reported.
- Complete-case only; no imputation.

## Known limitations
- **All 3 tests are non-significant, both raw and partial** (p ranges 0.14–0.83) — a genuine null result, not a data quality issue. See `model_run_summary.md` "Headline finding."
- Only linear correlation tested — does not rule out nonlinear or threshold relationships.
- Only 2 named loops tested (not an exploratory search across all possible flow×outcome combinations) — per blueprint FLAG SyD-2, deliberately scoped to paper-motivated hypotheses.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/system_dynamics/feedback_loop_tests.csv'))
```
