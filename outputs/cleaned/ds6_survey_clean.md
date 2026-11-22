# ds6_survey_clean.csv

**Source dataset:** Dataset 6 — Danish adolescents  
**Source file:** `data_raw/6. data set, Danish adolescents/Data/behavioral data/survey_data_clean.csv`  
**Producing notebook:** `notebooks/08_dataset_6_cleaning.ipynb`  
**Rows:** 478  
**Columns:** 20 (17 original + 3 derived)  
**Unit of observation:** One survey response per participant per wave (long format)

---

## What this file contains

Each row is one survey response for one participant at one time point. Participants appear up to twice (survey_nr 1 = pre-intervention wave, survey_nr 2 = post-intervention wave). This file contains pre-computed psychometric indices. Raw item-level data is available in `survey_data_full.csv`.

---

## Column Reference

### Identity
| Column | Type | Description |
|---|---|---|
| `response_id` | string | Participant ID — directly matches `ID` in behavioral and demographic files |
| `participant_id_canonical` | string | Same as `response_id` (derived for consistency) |
| `cond` | string | Condition: `control`, `default`, `intervention` |
| `cond_exp2` | string | Simplified binary condition: `OneSec Default`, `Control` |
| `survey_nr` | int | Wave number: 1 = pre-intervention, 2 = post-intervention |
| `survey_nr_fact` | int | Same as survey_nr (categorical encoding from R) |

### Survey timing
| Column | Type | Description |
|---|---|---|
| `start_date` | string / datetime | Survey start time |
| `end_date` | string / datetime | Survey end time |
| `survey_start_dt` | datetime | **Derived:** `start_date` parsed as datetime |
| `survey_end_dt` | datetime | **Derived:** `end_date` parsed as datetime |

### Psychometric indices (pre-computed)
| Column | Type | Description |
|---|---|---|
| `addiction_index` | float | Social media addiction index (mean of 6 items) |
| `retention_index` | float | Social media retention index |
| `self_control_index` | float | Self-control index (mean of 5 items) |
| `trivsel` | float | Well-being / thriving index |
| `socialconnection` | float | Social connectedness index |
| `fo_mo` | float | Fear of missing out (FoMO) index |
| `kontrolover_so_me` | float | Perceived control over social media use |
| `taenkerpa_so_me` | float | Thinking about social media |
| `tilfredsmed_so_me` | float | Satisfaction with social media use |
| `socialtforbundet` | string/float | Social connectedness label or score |

---

## Key Distributions

### Survey waves
| survey_nr | Count | Unique participants |
|---|---|---|
| 1 | 269 | 269 |
| 2 | 209 | 209 |

### Conditions
| cond | Count |
|---|---|
| default | 165 |
| intervention | 159 |
| control | 154 |

---

## Cleaning Steps Applied

1. Loaded raw CSV with comma delimiter
2. Added `participant_id_canonical` = `response_id`
3. Parsed `start_date` and `end_date` → `survey_start_dt` and `survey_end_dt`
4. Cast all psychometric index columns to numeric (`errors='coerce'`)
5. Cast `survey_nr` to int

---

## Known Limitations

- Only 2 waves represented in this file; survey_data_full.csv contains a 3rd wave
- 269 unique participants — 60 participants completed only wave 1, 209 completed both waves
- Indices are pre-computed — individual item-level responses require `survey_data_full.csv`
- `socialtforbundet` column has mixed format (string label in some rows)
- Survey dates are formatted as US date strings (`9/26/2024 5:34`) — parsing may vary by locale

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

survey = pd.read_csv(OUT / "ds6_survey_clean.csv",
                     parse_dates=["survey_start_dt", "survey_end_dt"])

# Wide format: pre vs post indices per participant
pre  = survey[survey["survey_nr"] == 1].set_index("participant_id_canonical")
post = survey[survey["survey_nr"] == 2].set_index("participant_id_canonical")
merged = pre[["addiction_index", "self_control_index", "fo_mo"]].join(
    post[["addiction_index", "self_control_index", "fo_mo"]],
    lsuffix="_pre", rsuffix="_post", how="inner"
)
print(merged.shape)  # 209 rows with both waves
```
