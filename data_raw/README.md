# `data_raw/` — intentionally empty

No data are distributed with this repository ([`../DATA_AVAILABILITY.md`](../DATA_AVAILABILITY.md)). This folder only documents **where the original data must be placed** for the code to run. Everything in here except this file is excluded by `.gitignore`.

Expected layout (names exactly as below — the notebooks and `src/io/` loaders hard-code them):

```
data_raw/
├── 1. data set, compact friction intervention testing/        DS1
├── 4. data set, large non-experimental data/                  DS4
├── 5. data set, German adolescents/                           DS5
├── 6. data set, Danish adolescents/                           DS6  (notebooks read its Data/ subfolder)
└── structured/
    └── Retrospective/                                         Structured (snapshot of 2026-07-22)
        ├── retro_behavioraldata_2026_07_22.csv
        └── retro_surveydata_2026_07_22.csv
```

Rules followed by all code: raw files are **read-only sources** — never edited, renamed or overwritten; every transformation is implemented in code and written to `outputs/`.
