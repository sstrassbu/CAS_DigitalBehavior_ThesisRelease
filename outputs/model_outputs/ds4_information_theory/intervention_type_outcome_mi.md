# intervention_type_outcome_mi.csv

**Unit of observation:** first row (`intervention_type=="__ALL__"`) is the overall
mutual-information summary; remaining 6 rows are per-intervention-type outcome PMFs.
Computed pooled across all DS4 participants (not per-participant), on
`intervention_event` class rows only.

**Purpose:** DS4-only addition (no DS5 equivalent — DS5 has a single friction type, DS4
logs 6). Tests whether which intervention type was shown predicts the outcome.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `intervention_type` | string | `__ALL__` for the summary row, else one of the 6 DS4 intervention types |
| `opened` | float | P(opened \| this type) — `NaN` on the `__ALL__` row |
| `dismissed` | float | P(dismissed \| this type) — `NaN` on the `__ALL__` row |
| `n_events` | int | Event count for this type (or overall, on `__ALL__`) |
| `MI_bits` | float | `MI(intervention_type;outcome)` in bits — only populated on the `__ALL__` row |

---

## How this file was produced

- **Source:** `outputs/cleaned/ds4_behavioral_clean.csv`, `intervention_event` class rows
- **Producing notebook:** `notebooks/52_ds4_information_theory.ipynb`, cell 13/16
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_int_blueprint.md`

## Actual run results (2026-08-06)

```
intervention_type            opened  dismissed  n_events
__ALL__                         NaN        NaN    909948   (MI=0.0010 bits)
blackScreen                   0.611      0.389     54105
breathingExercise             0.672      0.328    552424
followTheDot                  0.638      0.362    131438
minimalBreathingExercise      0.672      0.328    135358
mirror                        0.660      0.340     36613
rotatePhone                   0.800      0.200        10
```

## Interpretation

**MI(intervention_type;outcome) = 0.0010 bits pooled — a genuine near-null result, reported
honestly, not reframed. [Added 2026-08-08 by audit] This is the POOLED estimand. The
within-participant conditional MI I(type;outcome | participant), event-weighted over the 606
participants who saw ≥2 types, is 0.0107 bits — 10.8× larger, because participants differ both
in which types they see and in their own base override rate (the same pooled-panel confound
already on record from the Structured SyD work). The near-null conclusion survives either way:
0.0107 bits is still only 1.2% of H(outcome) = 0.9222 bits. The pooled χ² is 1269.9 (dof=5,
p=2.2e-272), significant purely on N=909,948 events.** Per-type opened-rates do visibly differ (61%–80% across types),
but `rotatePhone` (the type with the most extreme rate) has only 10 events — negligible
probability mass — so it barely moves the population-level MI. The five
highest-volume types (blackScreen, breathingExercise, followTheDot,
minimalBreathingExercise, mirror — together >99.9% of events) cluster within a narrower
61%–67% range, which is why the information-theoretic summary is small even though the
raw rate table looks more varied at a glance.

## Known limitations

- **Correlational, not causal.** Intervention type in DS4 is not randomly assigned — it
  reflects whatever the OneSec app's own logic selected for that context, not an
  experimental manipulation. Do not read this as "which intervention type works better."
- `rotatePhone`'s rate (80% opened) is based on only 10 events — not a reliable estimate
  of that type's true effect, shown for completeness only.
- **Between-participant confounded.** The per-type opened-rate column is a pooled rate, not
  a within-person contrast; participants are not randomly assigned to types, so type-to-type
  rate differences partly reflect which people saw which type.

## How to load

```python
import pandas as pd

mi = pd.read_csv("outputs/model_outputs/ds4_information_theory/intervention_type_outcome_mi.csv")
mi_bits = mi.loc[mi["intervention_type"] == "__ALL__", "MI_bits"].iloc[0]
type_rates = mi[mi["intervention_type"] != "__ALL__"]
```
