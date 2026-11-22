# DS6 NeT -- Model Run Summary

**Run at:** 2026-08-11 01:17:46
**Notebook:** notebooks/74_ds6_network_models.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_net_blueprint.md

## Eligibility
- Total participants: 243
- Baseline: NeT-eligible 239/243 (98.4%), stationary-eligible 231
- Intervention: NeT-eligible 235/243 (96.7%), stationary-eligible 224

## Key results
- Mean HHI_net (baseline): 0.4950
- Mean HHI_net (intervention): 0.5022
- Mean rho_self (baseline): 0.5063
- Mean rho_self (intervention): 0.5000
- Mean H_trans (baseline): 1.1972 bits
- Mean H_trans (intervention): 1.1951 bits
- StoP-NeT bridge: corr(HHI_net change, daily-volume change) = -0.2134, p=0.0012, n=227

## Data integrity note
This notebook derives transitions directly from time-sorted rows (shift(-1) within
participant x period), NOT from the pre-engineered `app_next` column, which was verified
2026-08-06 to mechanically echo the current row's own app_name 99.3% of the time (not a
real subsequent app choice) -- see `data_docs/modeling_cautions.md` S6 for the full finding.

## Proxy warning
Edges represent temporal adjacency between logged app-opening attempts, not causal
substitution or complete smartphone ecology. DS6's small (10-app) vocabulary likely inflates
HHI_net relative to DS1/DS4 independent of any behavioral effect.

## Known limitations
- Small closed app vocabulary (10 apps globally) limits network complexity compared to DS1/DS4.
- Quasi-experimental condition assignment (cohort-level), not individually randomized.
- Transitions reflect only One Sec-triggered events, not complete smartphone ecology (paper S2.4).
