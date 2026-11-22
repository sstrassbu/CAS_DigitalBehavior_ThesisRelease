# structured_survey_features.csv

**Source dataset:** Structured — Retrospective
**Source file:** `outputs/cleaned/structured_survey_clean.csv`
**Producing notebook:** `notebooks/17_structured_feature_extraction.ipynb`
**Producing module:** `src/features/structured_features.py::build_structured_survey_features`
**Rows:** 61 (restricted to participants with behavioral data)
**Columns:** 21
**Unit of observation:** One participant

---

## What this file contains

A restriction of `structured_survey_clean.csv` to the analysis-relevant columns, joined to the 61
behavioral participants only (56 survey-only respondents from the full survey file are excluded here —
they have no behavioral data to pair with). **Rows are not filtered on `consent_given` / `is_finished`**
— of the 61 behavioral participants, **all 61 have `consent_given = True`** (no explicit non-consenter
appears in the behavioral file — verified in `notebooks/15_structured_inspection.ipynb`); 55 also have
`is_finished = True`, and the remaining 6 have `is_finished = False`, i.e. partial responses, not
withheld consent. The "explicit non-consenters all show `Finished = Wahr`" caveat in
`structured_survey_clean.md` applies to the full 117-row survey file, **not** to this 61-row
behavioral subset. Always filter on `consent_given & is_finished` before using these features
as psychosocial correlates.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `participant_id` | string (UUID) | Participant identifier |
| `consent_given` | bool | From survey `Q12`; filter on this before use |
| `is_finished` | bool | See caveat above — not sufficient alone |
| `age` | float | Age in years |
| `gender` | string | Self-reported gender |
| `structured_use_duration` | string | How long actively using Structured |
| `life_happiness_score` | float | 1–7 general life happiness |
| `productivity_happiness_score` | float | 1–7 happiness with daily productivity |
| `pct_tasks_planned_num` | float | Self-reported % of daily tasks planned (0–100) |
| `pct_planned_tasks_completed_num` | float | Self-reported % of planned tasks completed (0–100) |
| `productivity_importance_general_score` | float | 1–7 importance of productivity in general |
| `productivity_importance_personal_score` | float | 1–7 importance of productivity personally |
| `productivity_rating_vs_others_score` | float | 1–7 self-rated productivity vs. others |
| `autism_status` | string | Self-reported autism status (categorical) |
| `adhd_status` | string | Self-reported ADHD/ADD status (categorical) |
| `asrs_1_finish_details_score` … `asrs_6_overactive_score` | float | ASRS-v1.1 Part A items, ordinally recoded 0–4 (see `structured_survey_clean.md` — not official clinical scoring) |

---

## Construct-Validity Check Performed in This Notebook

A direct test of whether self-reported planning completion tracks logged behavior:
`pct_planned_tasks_completed_num` (survey, ÷100) vs. `pct_tasks_completed` (behavioral, from
`structured_participant_features.csv`), among the 54 participants with both measures available and
`consent_given & is_finished`.

**Result: r = 0.127** — a weak, near-null correlation. Self-reported completion percentage does **not**
track behaviorally-derived task completion rate in this sample. This is consistent with the theory
paper's own framing (planning-behavior research literature: "plans rarely survive reality... intentions
often diverge from actual behavior") but should be treated as exploratory given N=54 and the
non-validated single-item self-report measure.

---

## Known Limitations

- N=61 total, N=55 fully consented+finished, N=54 with both self-report and behavioral completion data
  available for the construct-validity check — small samples throughout; treat all correlations here as
  exploratory, not confirmatory.
- ASRS items are 54.7% missing in the source survey (see `structured_survey_clean.md`) — expect
  substantial missingness in any analysis using the `asrs_*_score` columns.
- `autism_status` / `adhd_status` are self-report categories, not diagnoses (even where a respondent
  reports a "formal diagnosis" — this is still a self-report field, not verified).

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/features/structured")

sf = pd.read_csv(OUT / "structured_survey_features.csv")
usable = sf[sf["consent_given"] & sf["is_finished"]]  # 55 rows

pf = pd.read_csv(OUT / "structured_participant_features.csv")
merged = usable.merge(pf, on="participant_id", how="left")
```
