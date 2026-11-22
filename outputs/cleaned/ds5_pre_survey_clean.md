# ds5_pre_survey_clean.csv

**Source dataset:** Dataset 5 — German adolescents  
**Source file:** `data_raw/5. data set, German adolescents/Survey data sets/Pre-survey/pre_survey_data_set_5.csv`  
**Producing notebook:** `notebooks/06_dataset_5_cleaning.ipynb`  
**Rows:** 792  
**Columns:** 42 (37 original + 5 derived)  
**Unit of observation:** One pre-intervention survey response per participant

---

## What this file contains

Each row represents a pre-study survey response from one participant. This file contains the study condition assignment (`cond`), demographic information (age), and pre-intervention psychosocial measures including digital well-being, social media use perception, and three validated psychometric scales: sense of belonging (8 items), ostracism (5 items), and fear of missing out / FoMO (10 items). Derived mean score columns are added for each scale.

---

## Column Reference

### Identity and design
| Column | Type | Description |
|---|---|---|
| `uuid` | string | Original participant UUID from raw file |
| `participant_id_raw` | string | Same as `uuid` (preserved for traceability) |
| `participant_id_canonical` | string | Canonical ID matching behavioral file after prefix strip |
| `cond` | string | Study condition: `control`, `default`, `reintervention` |
| `age` | int | Age in years (13–25) |

### Self-reported digital use
| Column | Type | Description |
|---|---|---|
| `digital_wellbeing` | int | Perceived digital well-being rating |
| `time` | int | Perceived screen time rating |
| `prob_peers` | int | Perceived problem severity among peers |
| `time_peers` | int | Perceived time spent on social media by peers |
| `prob_self` | int | Perceived personal social media problem severity |
| `social_media_wellbeing` | int | Social media–specific well-being rating |
| `prob` | string | Main stated problem (open text or category) |
| `prob_other` | string | Other stated problem (94% NaN — optional free text) |
| `goal` | string | Stated goal for intervention |
| `goal_other` | string | Other stated goal (98% NaN) |
| `social_media_updated` | int | Whether social media apps were updated recently |

### Belonging scale (8 items, Likert)
| Column | Type | Description |
|---|---|---|
| `belong_1` – `belong_8` | int | Individual belonging items |
| `belong_mean` | float | **Derived:** mean of `belong_1`–`belong_8` (NaN if all items missing) |

### Ostracism scale (5 items, Likert)
| Column | Type | Description |
|---|---|---|
| `ostracism_1` – `ostracism_5` | int | Individual ostracism items |
| `ostracism_mean` | float | **Derived:** mean of `ostracism_1`–`ostracism_5` |

### FoMO scale (10 items, Likert)
| Column | Type | Description |
|---|---|---|
| `fomo_1` – `fomo_10` | int | Individual FoMO items |
| `fomo_mean` | float | **Derived:** mean of `fomo_1`–`fomo_10` |

---

## Key Distributions

### Study condition
| Condition | Count |
|---|---|
| control | 265 |
| default | 264 |
| reintervention | 263 |

### Age
Range 13–25; modal ages 18–20; sample includes young adults despite "adolescent" label.

---

## Cleaning Steps Applied

1. Loaded raw CSV with semicolon delimiter
2. Preserved `uuid` as `participant_id_raw` and `participant_id_canonical` (no transformation needed — already canonical format)
3. Cast all Likert item columns to numeric (`errors='coerce'`)
4. Computed `belong_mean` = mean of `belong_1`–`belong_8`
5. Computed `ostracism_mean` = mean of `ostracism_1`–`ostracism_5`
6. Computed `fomo_mean` = mean of `fomo_1`–`fomo_10`
7. Cast demographic and rating columns to numeric
8. Zero duplicate UUIDs confirmed — no deduplication needed

---

## Known Limitations

- 792 pre-survey participants but only 572 have matching behavioral records
- 220 participants enrolled but have no behavioral data (dropped out before activating app, or data not captured)
- `prob_other` and `goal_other` are 94–98% NaN — essentially unusable as structured variables
- `reason` text in behavioral file is German; no English equivalents provided
- Scale items have 5–7% missingness; means are based on available items (partial scale responses included)

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

pre = pd.read_csv(OUT / "ds5_pre_survey_clean.csv")

# Load behavioral and join condition
beh = pd.read_csv(OUT / "ds5_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

merged = beh.merge(
    pre[["participant_id_canonical", "cond", "age", "belong_mean",
         "ostracism_mean", "fomo_mean"]],
    on="participant_id_canonical", how="left"
)
print(merged.shape)
```
