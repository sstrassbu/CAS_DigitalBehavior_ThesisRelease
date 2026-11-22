# participant_entropy_metrics.csv

**Unit of observation:** one row per DS4 participant (all 1,039).

**Model:** DS4 Information Theory (InT) — 5 entropy quantities plus the StoP parameters
they're built from, joined so downstream models can use one file.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat`, `fit_valid` | — | Copied directly from StoP's `participant_parameters.csv` — see its companion `.md` |
| `H_SDE` | float | Exact OU stationary-distribution differential entropy: `0.5*log2(2*pi*e*sigma_hat_OU^2/(2*theta_hat_OU))`. `NaN` unless `fit_valid` |
| `H_out_intervention` | float | Shannon entropy (bits) of `{opened,dismissed}` outcome PMF, `intervention_event` class only |
| `H_out_all_classes` | float | Shannon entropy (bits) of `{opened,dismissed,closed,dismissed_other}` outcome PMF, pooled across all 3 event classes — **exploratory only**, mixes structurally different logging paths |
| `H_app` | float | Copied from Stage 1 `ds4_behavior_features.csv`'s `app_entropy` (all events, unfiltered by class) |
| `H_hour` | float | Copied from Stage 1 `ds4_behavior_features.csv`'s `hour_entropy` |
| `H_emp` | float | Empirical Shannon entropy (bits) of daily `X_t`, binned into K=10 equal bins over [0,1]. **Computed for all 1,036 participants with ≥1 observed day — NOT restricted to the StoP-eligible population, despite what `ds4_int_blueprint.md` §2 item 5 specifies.** `H_emp` is mechanically bounded above by log2(n_days_obs), so it is not comparable across participants with very different observation lengths. |

---

## How this file was produced

- **Sources:** `outputs/cleaned/ds4_behavioral_clean.csv`,
  `outputs/features/ds4/ds4_behavior_features.csv`,
  `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv`
- **Producing notebook:** `notebooks/52_ds4_information_theory.ipynb`
- **Generator script:** `notebooks/make_52_ds4_int.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_int_blueprint.md`

## Actual run results (2026-08-06)

| Column | N non-NaN | Mean | Median |
|---|---|---|---|
| `H_out_intervention` | 1,036 | 0.826 | 0.885 |
| `H_out_all_classes` | 1,039 | 1.194 | 1.292 |
| `H_app` | 1,039 | 1.060 | 1.063 |
| `H_hour` | 1,000 | 4.078 | 4.163 |
| `H_emp` | 1,036 | 2.174 | 2.328 |
| `H_SDE` | 641 (valid StoP fits only) | −0.541 | −0.549 |

**Population caveat for `H_emp` (added 2026-08-08 by audit):** the 1,036-participant row above is
NOT the StoP population. Restricted to the 641 valid StoP fits, `H_emp` mean = 2.394, median = 2.451,
min = 0.650; restricted to the 786 participants with ≥30 observed days, mean = 2.371, median = 2.434.
The 250 participants with 1–29 observed days average 1.553 bits and the 78 with ≤3 days average 0.361
bits — an observation-count artefact (H_emp ≤ log2(n_days_obs)), not low behavioural variety. Use the
fit_valid subset for any comparison against StoP-derived quantities.

**Bridge validation:** `r(H_emp, H_SDE)` = 0.721 (n=641) — comparable in magnitude to
DS5's own `r(H_SDE,H_emp)=0.650`, a reassuring cross-dataset sanity check even though the
two datasets' `H_SDE` formulas are not directly comparable (DS4's is exact, DS5's is an
approximation).

**Redundancy check:** `r(H_out_intervention, mu_hat_OU)` = −0.631 (n=641) — real but
partial; both columns are kept, neither is dropped as redundant.

## Known limitations

- **`H_out_all_classes` deliberately mixes event-logging paths** DS4's own structural
  cautions warn against mixing (`app_close_event` is 100% `closed`, `intervention_event`
  is only `opened`/`dismissed`). Use `H_out_intervention` as the primary friction-
  uncertainty metric; treat `H_out_all_classes` as descriptive only.
- **`H_SDE` is daily-timescale specific.** It uses only `sigma_hat_OU`/`theta_hat_OU`
  from StoP's daily fit. StoP's own weekly-aggregation sensitivity check found a
  meaningfully different relaxation time at weekly resolution (median τ̂≈0.91 weeks vs
  0.63 days daily) — this bridge inherits that same timescale-dependence. Do not treat
  `H_SDE` as a timescale-independent property of the participant.
- `H_hour` has 39 `NaN` (1,000/1,039 non-NaN), inherited directly from the Stage 1
  feature's own NaN rate.
- All entropy measures inherit `X_t`'s behavioral-proxy limitation — none of these are
  direct measurements of a psychological state.

## How to load

```python
import pandas as pd

entropy = pd.read_csv("outputs/model_outputs/ds4_information_theory/participant_entropy_metrics.csv")
valid = entropy[entropy["fit_valid"]]  # 641 rows with H_SDE populated
```
