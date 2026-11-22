# phenotype_feature_matrix.csv

## Contents
The complete-case feature matrix underlying DS6's Step 2 phenotyping — one curated
behavioral feature per completed Step 1 model family (StoP, NeT, InT, DyS, StM; SyD
deliberately excluded, see blueprint Part 1), before clustering.

## Unit of observation
One row per participant with all 5 features present (N=227, out of 243 behavioral
participants).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `h_period` | float | StoP (73): mu_hat_intervention − mu_hat_baseline (drift/trend shift) |
| `hhi_change` | float | NeT (74): HHI_net_intervention − HHI_net_baseline (network concentration shift) |
| `H_emp_baseline` | float | InT (75): empirical entropy of the baseline-period daily attempt-count series |
| `regime_changed` | float (0/1) | DyS (72): 1 if regime_baseline != regime_intervention, else 0 |
| `susceptibility` | float | StM (71): Jensen-Shannon divergence between baseline/intervention (app, hour) distributions |

## Production
- Source: `outputs/model_outputs/ds6/{stochastic_processes,network_models,information_theory,dynamical_systems,statistical_mechanics}/` (see blueprint Part 1 table for exact source files/columns)
- Producing notebook: `notebooks/140_ds6_phenotype_exploration.ipynb`
- Blueprint: `outputs/reports/stage4/step2_phenotyping/ds6_phenotyping_blueprint.md`

## Cleaning / derivation steps applied
- Outer-merged all 5 feature sources on `participant_id_canonical`, then restricted to complete cases (all 5 non-null) — 227/243 (93.4%) retained.
- `regime_changed` derived here (not a stored column in DyS's own output) from `regime_baseline`/`regime_intervention`.

## Known limitations
- Not all 6 completed model families are represented — SyD is deliberately excluded (its own output is psychosocial, reserved for the overlay instead; see `psychosocial_overlays.csv` companion doc).
- `regime_changed` is binary; the other 4 features are continuous — verified via the feature-redundancy check that this doesn't distort clustering, but see `model_run_summary.md` "Headline finding 1" for how much this one feature ends up dominating the k=2 split.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping/phenotype_feature_matrix.csv'))
```
