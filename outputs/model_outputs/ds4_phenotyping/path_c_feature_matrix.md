# path_c_feature_matrix.csv

**Unit of observation:** one row per complete-case DS4 participant (641 — same
population as Phase 1).

**Model:** DS4 Step 2, Path C′ — network-focused phenotyping. Tests whether DS4's
network structure forms its own independent phenotype axis.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `rho_self` | float | NeT self-transition rate (attempts-only) |
| `I_consec` | float | InT-NeT mutual-information bridge |
| `path_c_cluster` | int | Cluster label, 0–2 (k=3, stability-first selection) |
| `phase1_cluster` | int | Phase 1's own cluster label (0–2, k=3), joined for comparison |

---

## Feature-selection finding

NeT's full feature set (`rho_self`, `HHI_net`, `H_trans`) is severely internally
redundant — verified live in this notebook:

```
          rho_self  HHI_net  H_trans  I_consec
rho_self     1.000    0.867   -0.950    -0.014
HHI_net      0.867    1.000   -0.919    -0.380
H_trans     -0.950   -0.919    1.000     0.208
I_consec    -0.014   -0.380    0.208     1.000
```

`rho_self`/`HHI_net`/`H_trans` correlate up to \|r\|=0.95 — close to mechanical (high
self-transition rate almost necessarily drives high concentration and low transition
entropy). Using all three would triple-count one signal. Only `I_consec` is close to
independent (`r=-0.014` with `rho_self`). **This retroactively validates Phase 1's
choice of `rho_self` alone** for NeT's slot — adding `HHI_net`/`H_trans` there would
have added redundancy, not richness.

---

## How this file was produced

- **Sources:** DS4 StoP/StM/NeT outputs + Phase 1's `ds4_cluster_assignments.csv`
- **Producing notebook:** `notebooks/132_ds4_network_focused_phenotype.ipynb`
- **Generator script:** `notebooks/make_132_ds4_path_c.py`
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Actual run results (2026-08-06)

```
k=2: silhouette=0.4018, jaccard=0.8055 (STABLE)
k=3: silhouette=0.5147, jaccard=0.9658 (STABLE)   <- chosen, strongest stability of the whole DS4 arc
k=4: silhouette=0.4486, jaccard=0.9033 (STABLE)
k=5: silhouette=0.4539, jaccard=0.8700 (STABLE)
k=6: silhouette=0.4714, jaccard=0.8344 (STABLE)
```

Cluster sizes: 197/341/103.

**ARI(Path C′ k=3, Phase 1 k=3) = 0.047 — near-zero, essentially orthogonal.** Network
structure forms its own clean, highly-stable taxonomy that Phase 1's blended 5-feature
set (1 NeT feature diluted among 4 behavioral ones) barely captured.

## Known limitations

Same complete-case, no-condition, and daily-timescale caveats as Phase 1. `I_consec`
also inherits the caveats documented in `ds4_information_theory`'s companion docs
(daily-scale specific).

## How to load

```python
import pandas as pd

path_c = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_c_feature_matrix.csv")
```
