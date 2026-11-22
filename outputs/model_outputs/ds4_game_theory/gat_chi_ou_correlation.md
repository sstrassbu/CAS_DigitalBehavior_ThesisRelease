# gat_chi_ou_correlation.csv

**Unit of observation:** one row per GaT phenotype (4 rows) — mean/median/std/count of
StM's `chi_OU` (susceptibility) within that phenotype.

---

## How this file was produced

- **Sources:** `participant_gat_phenotypes.csv`,
  `outputs/model_outputs/ds4_statistical_mechanics/participant_ds4_stm_parameters.csv`
- **Producing notebook:** `notebooks/56_ds4_game_theory.ipynb`, cell 7/10
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_gat_blueprint.md`

## Actual run results (2026-08-07)

| Phenotype | N | mean χ_OU | median χ_OU |
|---|---|---|---|
| adaptive_switcher | 97 | 7.92 | 6.28 |
| chronic_overrider | 232 | 10.01 | 8.37 |
| commitment_oriented | 224 | 7.01 | 5.48 |
| reward_oriented | 88 | 7.23 | 5.97 |

**ANOVA: F=12.088, p<0.0001** — real, significant difference. Chronic overriders show
the highest susceptibility, closest to a behavioral tipping point in the StM sense.

## Known limitations

Only `fit_valid=True` participants from StM (641) are represented here — the
denominators above are smaller than GaT's full 986.

## How to load

```python
import pandas as pd

chi_by_phenotype = pd.read_csv("outputs/model_outputs/ds4_game_theory/gat_chi_ou_correlation.csv")
```
