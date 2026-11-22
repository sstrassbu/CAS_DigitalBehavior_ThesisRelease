# ds5_phenotype_feature_matrix.csv — Documentation

**Produced by:** `notebooks/100_phenotype_exploration.ipynb` (Stage 4, Step 2)  
**Date:** 2026-04-18  
**Unit of observation:** One row per participant in the Phase 1 analysis population (414 rows)

---

## What this file contains

All behavioral features available for the DS5 phenotyping analysis, assembled from the five
completed Step 1 model outputs. Contains only participants who have complete data on all five
Phase 1 core clustering features (sig_hat, H_emp, x_mean, HHI_net, rho_self), i.e. the
StoP-eligible AND NeT-eligible overlap population (N=414).

Secondary features (H_hour, H_app, chi_behav) are included but have their own missingness
pattern within this population.

---

## Column reference

| Column | Type | Source model | Description |
|---|---|---|---|
| `participant_id_canonical` | str | — | Canonical participant ID |
| `study_condition` | str | InT/Survey | Experimental condition: control / default / reintervention |
| `sig_hat` | float | StoP | Behavioral diffusion — day-to-day variability in X_t; **Phase 1 core** |
| `H_emp` | float | InT/DyS | Empirical entropy of daily X_t distribution (K=10 bins); **Phase 1 core** |
| `x_mean` | float | StoP | Mean daily override rate (time-average of X_t); **Phase 1 core** |
| `HHI_net` | float | NeT | Network Herfindahl index — flow concentration across apps; **Phase 1 core** |
| `rho_self` | float | NeT | Self-loop rate — same-app repetition in consecutive events; **Phase 1 core** |
| `H_hour` | float | InT | Entropy of hour-of-day distribution — temporal spread; **Phase 2 sensitivity** |
| `H_app` | float | InT | Entropy of app distribution — app diversity; **Phase 2 sensitivity** |
| `chi_behav` | float | StM | Behavioral susceptibility = β·p·(1−p); **Phase 2 sensitivity** |
| `H_out` | float | InT | Entropy of friction outcome distribution (condition-confounded; not in Phase 1 clustering) |
| `mu_hat` | float | StoP | Behavioral drift — mean daily increment in X_t |
| `sigma_mu_ratio` | float | StoP | Impulsivity ratio σ/\|μ\|; 31.2% NaN (undefined for \|μ\| < 0.005) |
| `is_dys_eligible` | bool | DyS | σ̂ < σ_median (0.1812) — binarization of sig_hat |
| `behaviorally_deterministic` | bool | DyS | is_dys_eligible AND H_emp < H_emp_median |
| `four_model_convergent` | bool | StM | Low σ̂ AND low H_emp — same as behaviorally_deterministic |
| `beta_behav` | float | StM | Behavioral inverse temperature = 2/σ̂² (monotone transform of sig_hat) |
| `F_behav` | float | StM | Free energy analog = E_use − (1/β)·H_emp |
| `H_trans` | float | NeT | Transition entropy — conditional entropy of app transitions |
| `I_consec` | float | NeT | Mutual information I(app_t; app_t+1) = H_app − H_trans (derived; not independent) |
| `H_SDE` | float | InT | Gaussian differential entropy = ½log₂(2πeσ̂²) (monotone transform of sig_hat) |
| `H_out_resid` | float | InT | H_out residualized on study_condition (used in Phase 2 clustering only) |

---

## Source files

| Model | Source CSV |
|---|---|
| StoP | `outputs/model_outputs/stochastic_processes/participant_parameters.csv` |
| InT | `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` |
| DyS | `outputs/model_outputs/dynamical_systems/participant_dynamics_parameters.csv` |
| StM | `outputs/model_outputs/statistical_mechanics/participant_stm_parameters.csv` |
| NeT | `outputs/model_outputs/network_models/participant_network_metrics.csv` |
| Survey | `outputs/features/ds5/ds5_survey_features.csv` |

---

## Cleaning steps applied

1. Started with InT output (572 participants) as base.
2. Left-merged StoP, DyS, StM, NeT outputs on `participant_id_canonical`.
3. NeT features (HHI_net, rho_self, H_trans, I_consec) set to NaN for participants where
   `is_net_eligible = False` (< 20 app transitions).
4. Filtered to participants with complete data on all 5 Phase 1 core features (N=414).
5. `H_out_resid` computed by residualizing H_out on one-hot-encoded study_condition
   (LinearRegression; all 414 Phase 1 participants had valid H_out after this step).

---

## Known limitations

- **Population:** Only 414/572 participants (72.4%) are represented. Missing participants
  failed the StoP MIN_DAYS=7 threshold (too few observation days) or the NeT MIN_TRANSITIONS=20
  threshold. Missingness is approximately equal across conditions.
- **Proxy:** All features derive from X_t = n_opened / n_events — a behavioral proxy, not a
  direct measurement of urge, self-control, or psychological state.
- **I_consec is derived:** I_consec = H_app − H_trans; do not include alongside both H_app and
  H_trans in any analysis.
- **sigma_mu_ratio:** 31.2% NaN within this population; not suitable for clustering.

---

## How to load

```python
import pandas as pd
from pathlib import Path

df = pd.read_csv(
    Path('outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv')
)
print(df.shape)  # (414, n_cols)
```
