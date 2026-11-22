# phenotype_feature_matrix.csv

## Contents
Complete-case feature matrix for Path A' (behavior-only, DyS removed) — the 4 continuous
features remaining after dropping DyS's dominant `regime_changed` binary feature from the
main Step 2 pass (notebook 140).

## Unit of observation
One row per participant with all 4 features present (N=227, same complete-case set as the
main pass since dropping a feature only relaxes the constraint).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `h_period` | float | StoP (73): mu_hat_intervention − mu_hat_baseline |
| `hhi_change` | float | NeT (74): HHI_net_intervention − HHI_net_baseline |
| `H_emp_baseline` | float | InT (75): empirical entropy of the baseline daily attempt-count series |
| `susceptibility` | float | StM (71): Jensen-Shannon divergence between baseline/intervention (app, hour) distributions |

## Production
- Source: same 4 model-family CSVs as `outputs/model_outputs/ds6/phenotyping/phenotype_feature_matrix.csv`, minus DyS
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`
- Blueprint: `outputs/reports/stage4/step2_phenotyping/ds6_path_a_behavior_only_blueprint.md`

## Cleaning / derivation steps applied
- Same merge/complete-case logic as the main pass, with `regime_changed` (DyS) dropped entirely per the blueprint's Part 1 design (test dominance by removal, not substitution).

## Known limitations
- This feature set does NOT produce a min-cell-valid clustering solution at N=227 (see `cluster_assignments.md`) — the matrix itself is fine, but downstream clustering results should be read with that caveat.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/phenotype_feature_matrix.csv'))
```
