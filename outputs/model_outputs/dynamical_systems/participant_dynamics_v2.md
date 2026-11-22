# participant_dynamics_v2.csv

**Produced by:** `notebooks/60_ds5_dys_v2_potential_well.ipynb` (DS5_02 A1)  
**Source data:** `outputs/cleaned/ds5_behavioral_clean.csv`  
**Supersedes:** Does NOT replace `participant_dynamics_parameters.csv` (DS5_01 baseline, kept intact)

## What this file contains

Per-participant summary of V(x) = −log p̂(x) computed from KDE of the daily X_t series
(daily override rate). This is DS5_02 A1: replacing FLAG2's median-split `behaviorally_deterministic`
with a data-grounded fixed-point classification from the participant's own potential well.

**Unit of observation:** one row per participant (414 total, same population as DS5_01).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier (primary key) |
| `study_condition` | str | control / default / reintervention |
| `n_xt` | int | Number of daily X_t observations used for KDE |
| `kde_bw` | float | Effective KDE bandwidth (Silverman rule) |
| `has_stable_fp` | bool | True if at least one stable fixed point (V''>0) found |
| `n_fps` | int | Total fixed points found (stable + unstable) |
| `n_stable_fps` | int | Number of stable fixed points (attractors) |
| `x_fp_primary` | float | Location x* of primary stable FP (highest KDE density among stable FPs) |
| `V_curvature_primary` | float | V''(x*) at primary stable FP — used as β_v2 in notebook 60b |
| `p_at_fp_primary` | float | KDE density p̂(x*) at primary stable FP |
| `low_confidence` | bool | True if n_xt < 10 (KDE reliability reduced) |

## Key result (A1)

| | Count | % of 414 |
|---|---|---|
| has_stable_fp = True (v2) | 66 | 15.9% |
| behaviorally_deterministic = 1 (DS5_01 FLAG2) | 154 | 37.2% |
| Agreement between methods (full-sample concordance, all 414) | 58.0% | — |

> Note: notebook 60 cell 11 prints '34.8%' for this row. That figure is the v2 positive predictive
> value (23/66 v2-stable-FP participants that are also orig-deterministic), not a concordance rate.
> The correct full-sample agreement is 58.0%.

## How produced

1. Load `ds5_behavioral_clean.csv`, filter to `{opened, dismissed, closed}` outcomes
2. Compute daily X_t = n_opened / n_events per participant-day (identical to notebook 43)
3. Per participant (≥7 days): reflection-corrected KDE on x_t ∈ [0,1]
4. V(x) = −log p̂(x), smoothed with Savitzky-Golay filter (window=21, poly=3)
5. Fixed points: sign changes in dV/dx (interior of grid, avoiding boundary artefacts)
6. Stability: d²V/dx² > 0 at FP → stable; < 0 → unstable

## Known limitations

- 7–43 daily data points per participant (median 40, 25th percentile 28, minimum 7): KDE is bandwidth-sensitive and over-smoothed for small N
- `low_confidence=True` for n_xt < 10 (14 of 414 = 3.4% of eligible participants)
- Single-app users (Profile B, rho_self ≈ 1.0) tend to have x_t ≈ 0 → trivial V(x) spike at 0 → FP at x*=0
- Fixed-point detection depends on smoothing parameters; results sensitive to bandwidth choice

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/dynamical_systems/participant_dynamics_v2.csv')
stable = df[df['has_stable_fp'] == True]
```
