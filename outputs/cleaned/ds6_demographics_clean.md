# ds6_demographics_clean.csv

**Source dataset:** Dataset 6 — Danish adolescents  
**Source file:** `data_raw/6. data set, Danish adolescents/Data/behavioral data/demographic_data.csv`  
**Producing notebook:** `notebooks/08_dataset_6_cleaning.ipynb`  
**Rows:** 399  
**Columns:** 6 (4 original + 2 derived)  
**Unit of observation:** One row per participant (demographic profile)

---

## What this file contains

Demographic characteristics for all 399 enrolled participants. Includes age, gender, and Danish region. 243 of these participants also have behavioral data; the remaining 156 are enrolled-only.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `ID` | string | Participant ID — matches `participant_id_canonical` in behavioral, survey, and linkage files |
| `participant_id_canonical` | string | Same as `ID` (derived for consistency) |
| `age` | int | Age in years (13–17) |
| `gender_raw` | string | Original Danish gender label (`kvinde` / `mand`) |
| `gender` | string | **Derived:** English gender label (`female` / `male`) |
| `region` | string | Danish region name |

---

## Key Distributions

### Age
| Age | Count |
|---|---|
| 13 | 127 |
| 14 | 71 |
| 15 | 74 |
| 16 | 68 |
| 17 | 59 |

### Gender
| Gender | Count |
|---|---|
| female | 269 |
| male | 129 |
| NaN | 1 |

### Region
| Region | Count |
|---|---|
| Midtjylland | 120 |
| Hovedstaden | 116 |
| Syddanmark | 74 |
| Sjælland | 62 |
| Nordjylland | 27 |

---

## Cleaning Steps Applied

1. Loaded raw CSV with comma delimiter
2. Added `participant_id_canonical` = `ID`
3. Preserved original `gender` as `gender_raw`
4. Mapped Danish labels → English: `kvinde` → `female`, `mand` → `male`
5. Cast `age` to numeric

---

## Known Limitations

- 399 total participants, but only 243 have behavioral data (156 enrolled without behavioral events)
- 1 participant has NaN gender
- Region encodes school/district — may correlate with cohort condition assignment

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

demo = pd.read_csv(OUT / "ds6_demographics_clean.csv")
beh  = pd.read_csv(OUT / "ds6_behavioral_clean.csv",
                   parse_dates=["event_timestamp_utc"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

merged = beh.merge(demo[["participant_id_canonical", "age", "gender", "region"]],
                   on="participant_id_canonical", how="left")
print(merged.shape)
```
