# psychosocial_overlays.csv

## Contents
Kruskal-Wallis test results comparing SyD's psychosocial change scores
(`addiction_index_change`, `self_control_index_change`) across the 2 phenotype clusters —
**the first statistically significant psychosocial result in the entire DS6 Step 1+2
program** (see `model_run_summary.md` "Headline finding 2").

## Unit of observation
One row per psychosocial scale (2 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `scale` | str | addiction_index_change or self_control_index_change |
| `H_stat` | float | Kruskal-Wallis H statistic |
| `p_raw` | float | Uncorrected p-value |
| `p_bonferroni` | float | Bonferroni-corrected p-value (×2 tests) |

## Production
- Source: `cluster_assignments.csv` (this folder) merged with `outputs/model_outputs/ds6/system_dynamics/participant_stock_flow.csv` (SyD's own output — the psychosocial CHANGE scores, not static pre-scores, per blueprint Part 1's architectural decision to use SyD as the overlay source)
- Producing notebook: `notebooks/140_ds6_phenotype_exploration.ipynb`

## Cleaning / derivation steps applied
- Inner merge of cluster assignment (N=227) with SyD's prepost-eligible participants (N=188) → overlay N=176.
- Kruskal-Wallis (non-parametric, appropriate given no assumption of normality for change scores) per scale; Bonferroni correction applied across the 2 tests.

## Known limitations
- **`self_control_index_change` is significant even after Bonferroni correction** (p_raw=0.009, p_bonferroni=0.018) — Profile A (stable DyS regime) improves (mean +0.164), Profile B (regime changed) worsens (mean −0.086). Associational, not causal — `study_condition` is quasi-experimental, and self-reported change may partly reflect regression to the mean (the same caution already recorded for SyD's own loop tests).
- `addiction_index_change` shows no significant difference (p_raw=0.847).
- Overlay N=176 is smaller than both the full behavioral N=243 and the phenotyping N=227 — participants without a usable wave-2 survey are excluded, not imputed.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping/psychosocial_overlays.csv'))
```
