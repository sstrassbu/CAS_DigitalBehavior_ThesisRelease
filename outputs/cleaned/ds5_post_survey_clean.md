# ds5_post_survey_clean.csv

**Source dataset:** Dataset 5 — German adolescents  
**Source file:** `data_raw/5. data set, German adolescents/Survey data sets/Post-survey/post_survey_data_set_5.csv`  
**Producing notebook:** `notebooks/06_dataset_5_cleaning.ipynb`  
**Rows:** 311 (3 duplicates removed from 314 raw rows)  
**Columns:** 38 (33 original + 5 derived)  
**Unit of observation:** One post-intervention survey response per participant

---

## What this file contains

Each row represents a post-study survey response from one participant. This file mirrors the pre-survey structure (same belonging, ostracism, and FoMO scales) but adds two intervention-specific outcome questions: `solve_prob` (did the intervention help solve the stated problem) and `address_goal` (did the intervention address the stated goal). No condition column is present — join from pre-survey.

---

## Column Reference

### Identity
| Column | Type | Description |
|---|---|---|
| `uuid` | string | Original participant UUID |
| `participant_id_raw` | string | Same as `uuid` |
| `participant_id_canonical` | string | Canonical ID matching behavioral and pre-survey |

### Post-intervention outcome questions
| Column | Type | Description |
|---|---|---|
| `solve_prob` | int | Did the intervention help solve the stated problem? (Likert) |
| `address_goal` | int | Did the intervention address the stated goal? (Likert) |

### Self-reported digital use (same as pre-survey)
| Column | Type | Description |
|---|---|---|
| `digital_wellbeing` | int | Perceived digital well-being |
| `time` | int | Perceived screen time |
| `prob_peers` | int | Perceived peer problem severity |
| `time_peers` | int | Perceived peer screen time |
| `prob_self` | int | Perceived personal problem severity |
| `social_media_wellbeing` | int | Social media well-being |
| `social_media_updated` | int | Whether apps were updated |

### Belonging scale (8 items)
| Column | Type | Description |
|---|---|---|
| `belong_1` – `belong_8` | int | Individual items |
| `belong_mean` | float | **Derived:** row mean |

### Ostracism scale (5 items)
| Column | Type | Description |
|---|---|---|
| `ostracism_1` – `ostracism_5` | int | Individual items |
| `ostracism_mean` | float | **Derived:** row mean |

### FoMO scale (10 items)
| Column | Type | Description |
|---|---|---|
| `fomo_1` – `fomo_10` | int | Individual items |
| `fomo_mean` | float | **Derived:** row mean |

---

## Cleaning Steps Applied

1. Loaded raw CSV with semicolon delimiter
2. Added `participant_id_raw` and `participant_id_canonical` columns (copied from `uuid`)
3. Cast all scale items to numeric (`errors='coerce'`)
4. Computed `belong_mean`, `ostracism_mean`, `fomo_mean`
5. Cast outcome and rating columns to numeric
6. Identified 3 duplicate UUIDs (each appearing twice) → kept first occurrence → 311 rows
7. No condition column in post-survey — join from `ds5_pre_survey_clean.csv`

---

## Known Limitations

- Only 311 of 792 pre-survey participants completed the post-survey (~39% retention)
- No condition column — must join from pre-survey
- 3 duplicate UUIDs had identical or near-identical responses; first row kept (cause unknown)
- Outcome questions `solve_prob` and `address_goal` are only interpretable for intervention groups (control group received no intervention)

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

post = pd.read_csv(OUT / "ds5_post_survey_clean.csv")
pre  = pd.read_csv(OUT / "ds5_pre_survey_clean.csv")

# Join to get condition and pre-survey baselines for comparison
merged = post.merge(
    pre[["participant_id_canonical", "cond",
         "belong_mean", "ostracism_mean", "fomo_mean"]],
    on="participant_id_canonical", how="left",
    suffixes=("_post", "_pre")
)
print(merged.shape)
```
