# `src/` — reusable modules

Small, reusable modules imported by the notebooks (`from src.io.load_dataset_5 import …`, with the repository root on `sys.path`). **Most analysis logic is in the notebooks**, not here: the CAS model implementations are inline in the Step 1 notebooks, by design (each dataset's model differs in state variable and quantities, so a shared model library was never built).

| Module | Purpose |
|---|---|
| `io/load_dataset_1.py`, `load_dataset_4.py`, `load_dataset_5.py`, `load_dataset_6.py` | read the raw files of each dataset into dataframes (paths per [`../data_raw/README.md`](../data_raw/README.md)) |
| `features/behavioral_features.py` | shared behavioural feature utilities |
| `features/ds1_features.py`, `ds4_features.py`, `ds5_features.py`, `ds6_features.py` | Stage 1 feature builders per dataset |
| `features/structured_features.py` | Stage 1 feature builders for the Structured dataset (task-lifecycle, participant, survey level) |
| `features/harmonized_core_features.py` | Stage 2 cross-dataset core feature set |
| `phenotyping/path_d_analysis.py` | stand-alone **script** (executes on import, reads participant-level tables from `outputs/`) for the dynamic/stochastic phenotyping path — run it, don't import it |

Feature definitions and their QC history are documented in [`../data_docs/stage1_feature_qc_notes.md`](../data_docs/stage1_feature_qc_notes.md) and in the companion documents under [`../outputs/features/`](../outputs/features/).
