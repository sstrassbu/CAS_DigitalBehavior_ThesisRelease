# participant_stm_parameters_v2.csv

**Produced by:** `notebooks/60b_ds5_stm_v2_boltzmann.ipynb` (DS5_02 A2)  
**Depends on:** `participant_dynamics_v2.csv` (notebook 60, A1) for V_curvature_primary  
**Supersedes:** Does NOT replace `participant_stm_parameters.csv` (DS5_01 baseline, kept intact)

## What this file contains

Per-participant StM v2 parameters derived via Boltzmann inversion of V(x).
This is DS5_02 A2: replacing FLAG A's parabolic approximation (β=2/σ²) with
β_v2 = V''(x*), the curvature of the KDE potential well at the stable fixed point.

**Unit of observation:** one row per participant (414 total).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier (primary key) |
| `study_condition` | str | control / default / reintervention |
| `has_stable_fp` | bool | From notebook 60: stable fixed point exists |
| `is_stm_eligible_v2` | bool | has_stable_fp AND NOT low_confidence |
| `low_confidence` | bool | n_xt < 10 in notebook 60 |
| `x_fp_primary` | float | Attractor location x* from V(x) minimum |
| `beta_v2` | float | V''(x*) at stable FP — inverse temperature analog |
| `chi_v2` | float | β_v2 · x* · (1−x*) — susceptibility at attractor state |

## Relationship to DS5_01 StM parameters

| Quantity | DS5_01 (FLAG A) | DS5_02 v2 | Gaussian limit |
|---|---|---|---|
| β | 2/σ² | V''(x*) | β_v2 = β_behav/2 |
| χ | β · x̄ · (1−x̄) | β_v2 · x* · (1−x*) | similar if x̄ ≈ x* |
| N eligible | 414 (all) | 66 (stable FP only) | — |

## Key results (A2)

**β_v2 condition ordering (median):**
- control: 2.594  
- reintervention: 2.088  
- default: 1.759  
- **Ordering preserved: control > reintervention > default** (same as DS5_01)

**Spearman ρ(β_behav, β_v2) = 0.578** (n=66, moderate positive correlation)

**Factor offset:** β_behav / β_v2 ≈ 34× median (n=66; min 2.5, 25% 17.2, 75% 80.4, max 691.8).
⚠ There is no analytic benchmark to compare this against — β_behav uses the SDE **increment**
variance σ̂² while β_v2 = V''(x*) reflects the **level** curvature of the X_t distribution, and
β_v2 is additionally attenuated by notebook 60's reflected-sample bandwidth and Savitzky-Golay
smoothing (median β_v2 = 2.26 vs median 1/s_level² = 42.75). The ratio therefore does NOT
quantify non-Gaussianity; report it descriptively only.

## Known limitations

- Only 66/414 participants have β_v2 defined (stable FP required)
- Condition-level ordering based on small per-condition N (16–25 participants)
- β_v2 is a local curvature measure; sensitive to KDE bandwidth
- χ_v2 uses x* (attractor) not x̄ (mean) — different interpretation from DS5_01's χ_behav

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/statistical_mechanics/participant_stm_parameters_v2.csv')
eligible = df[df['is_stm_eligible_v2'] == True]
```
