# participant_abm_summary.csv

**Produced by:** `notebooks/47_ds5_agent_based.ipynb`
**Date:** 2026-08-06
**Depends on:** `outputs/model_outputs/stochastic_processes/participant_parameters.csv`,
`outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv`

## What this file contains

Per-participant ABM simulation results for DS5. One row per participant (N=414 with StoP params).
Unit of observation: one participant, summarized over a 30-day simulated trajectory.

Each agent is parameterized by their individual StoP-fitted μ_hat and σ_hat. The simulation
validates whether SDE agents reproduce observed x_mean distributions. FLAG AB1: This is a
*validation* of StoP parameterization, not an independent structural ABM.

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | RCT arm: control / default / reintervention |
| `profile_p1` | str | DS5_01 phenotype label (Profile A / Profile B) |
| `x_mean_obs` | float | Observed mean daily override rate (from behavioral data) |
| `x_mean_sim` | float | Simulated 30-day trajectory mean override rate |
| `sig_sim` | float | Standard deviation of simulated 30-day trajectory |
| `mu_hat` | float | StoP-fitted drift parameter (from StoP Step 1) |
| `sig_hat` | float | StoP-fitted noise parameter (from StoP Step 1) |

## Key results

**Individual validation gate — FAIL ✗**

- Spearman ρ (x_mean_obs vs x_mean_sim) = 0.4284
- RMSE = 0.2411
- Gate threshold: rho ≥ 0.80

**Why the gate fails — SDE boundary ergodics (genuine structural limitation, not a bug):**

A bounded random walk clipped to [0,1] has an ergodic mean near 0.5 when σ is large relative to
drift |μ|. DS5 agents have σ_hat (median≈0.19) >> |μ_hat| (median≈0.006), so 30-step simulations
systematically pull toward 0.5, underestimating observed x_mean for high-rate participants
(x_mean≈0.85 simulates to ≈0.60). The StoP SDE captures short-step dynamics correctly but does
not extrapolate reliably to 30-day trajectory means.

**Archetype pool validation (200 synthetic agents per profile):**

| Profile | Obs mean x | Sim mean x |
|---|---|---|
| Profile A | 0.6688 | 0.5549 |
| Profile B | 0.7052 | 0.6025 |

The rank ordering (Profile B > Profile A) is reproduced, but absolute values are underestimated
by ≈11–12pp due to boundary ergodics. Phenotype SEPARATION is reproduced in relative terms.

## Known limitations

1. FLAG AB1: Agent rules = StoP SDE; not an independent structural model
2. FLAG AB2: No agent interaction, social influence, or learning — real smartphone use is embedded in social contexts
3. FLAG AB3: SDE clip-to-[0,1] is a censoring (clipping) boundary, not a reflection: excursions are truncated onto the boundary, which puts point masses of roughly 11% at each of 0 and 1 in the stationary distribution (verified by simulation at μ=0, σ=0.19). This partially mimics, rather than excludes, an absorbing state; genuine absorbing dynamics (chronic non-use / constant override) are still not modeled
4. FLAG AB4: Simulation validates StoP parameterization; it does not introduce genuinely new generative claims
5. FLAG AB5: No substitution/redirect behavior modeled (no redirect target data in DS5)
6. N_DAYS=30 is standardized; actual observation windows vary per participant
7. **GATE FAILURE IS A REAL FINDING:** the SDE agent parameterization from daily increments does not scale to 30-day trajectory prediction because boundary clipping introduces a systematic ergodic bias

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/agent_based/participant_abm_summary.csv')
```
