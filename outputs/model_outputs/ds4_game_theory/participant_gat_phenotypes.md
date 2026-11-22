# participant_gat_phenotypes.csv

**Unit of observation:** one row per DS4 participant with ≥5 dismissal-then-next-event
pairs (986 of 1,039).

**Model:** DS4 Game Theory (GaT) — rule-based classification into the OneSec paper's
own 4 named phenotypes (§2.6): commitment-oriented, reward-oriented, chronic overrider,
adaptive switcher. No formal payoff matrix — matches the paper's own explicit caution.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `rate_opened_intervention_events` | float | Stage 1 feature — primary reward/commitment axis |
| `p_open_after_dismiss` | float | Stage 1 feature — kept in the file for reference, **not used** in classification (r=0.934 with opened-rate, near-tautological) |
| `max_consecutive_opens` | float | Stage 1 feature — override-streak axis |
| `open_rate_change_calendar` | float | Stage 1 feature — used only in the adaptation cross-check |
| `substitution_after_dismissal_rate` | float | **New quantity**: `P(app_next≠app_current \| outcome=dismissed)`, attempt rows |
| `n_dismissal_events_with_next` | int | Sample size behind `substitution_after_dismissal_rate` |
| `gat_phenotype` | string | One of `commitment_oriented`/`reward_oriented`/`chronic_overrider`/`adaptive_switcher` |

---

## How this file was produced

- **Sources:** `outputs/cleaned/ds4_behavioral_clean.csv`,
  `outputs/features/ds4/ds4_behavior_features.csv`
- **Producing notebook:** `notebooks/56_ds4_game_theory.ipynb`
- **Generator script:** `notebooks/make_56_ds4_gat.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_gat_blueprint.md`

## Classification rule (descriptive, not clustering)

```
if rate_opened_intervention_events >= 0.682 (median):
    if max_consecutive_opens >= 23 (top tertile): chronic_overrider
    else:                                          reward_oriented
else:
    if substitution_after_dismissal_rate >= 0.343 (top tertile): adaptive_switcher
    else:                                                          commitment_oriented
```

## Actual run results (2026-08-07)

Pooled substitution-after-dismissal rate = 0.283 (most dismissals are followed by
returning to the *same* app, not switching).

| Phenotype | N |
|---|---|
| commitment_oriented | 352 |
| chronic_overrider | 304 |
| reward_oriented | 190 |
| adaptive_switcher | 140 |

**Three cross-checks, all real, all significant:**
- `chi_OU` (StM susceptibility) by phenotype: **ANOVA F=12.09, p<0.0001**. Chronic
  overriders show the highest mean susceptibility (10.01), commitment-oriented the
  lowest (7.01).
- GaT phenotype × Phase 1 cluster: **chi2=136.4, p<0.0001**. Chronic overrider strongly
  associates with Phase 1 cluster 0 (131/232 = 56%) — the same cluster independently
  identified as highest-susceptibility in Step 2. A genuine convergent-validity finding
  across two independently-built model families.
- `|open_rate_change_calendar|` (adaptation trajectory) by phenotype: **ANOVA F=35.57,
  p<0.0001**. Chronic overriders show the *least* change over time (mean 0.080) —
  most behaviorally "locked in" — while commitment-oriented and adaptive-switcher show
  more trajectory change (means 0.156, 0.154).

## Known limitations

- Correlational only — no causal claim about which phenotype "performs better."
- The paper's 5th named phenotype ("friction-avoidant") is not operationalized — no
  DS4 quantity distinguishes it from commitment-oriented.
- `substitution_after_dismissal_rate` inherits the same attempt-row convention as NeT
  (excludes `app_close_event`).

## How to load

```python
import pandas as pd

gat = pd.read_csv("outputs/model_outputs/ds4_game_theory/participant_gat_phenotypes.csv")
```
