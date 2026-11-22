# ds4_demographic_overlay.csv

**Unit of observation:** one row per complete-case participant who *also* has DS4
survey data (149 of 641 — DS4's survey coverage is thin, 283/1,039 overall).

**Status: exploratory/secondary**, per the blueprint's FLAG 5 — DS4 has no validated
Likert scales, only demographics and qualitative flags.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `cluster` | int | Phenotype cluster (0/1/2) |
| `survey_age` | float | Age in years, from `ds4_survey_features.csv` |
| `gender_clean` | string | Recoded gender category |

---

## How this file was produced

- **Sources:** phenotype cluster assignments + `outputs/features/ds4/ds4_survey_features.csv`
- **Producing notebook:** `notebooks/59_ds4_phenotype_exploration.ipynb`, cell 11/13
- **Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`

## Actual run results (2026-08-06)

| Cluster | N | Age mean | Age std |
|---|---|---|---|
| 0 | 45 | 27.8 | 6.6 |
| 1 | 93 | 25.9 | 7.4 |
| 2 | 11 | 29.0 | 10.7 |

**ANOVA age by cluster: F=1.564, p=0.213 — not significant.** No age difference across
phenotype clusters detected at this N.

## Known limitations

- N=149 is a small subset of the already-restricted 641 complete-case population —
  results here are exploratory, not confirmatory.
- Cluster 2's demographic subset (N=11) is especially small — its age statistics are
  unreliable.
- No Likert-scale psychosocial measures exist in DS4 at all — this overlay cannot
  approach DS5's psychosocial interpretability.

## How to load

```python
import pandas as pd

overlay = pd.read_csv("outputs/model_outputs/ds4_phenotyping/ds4_demographic_overlay.csv")
```
