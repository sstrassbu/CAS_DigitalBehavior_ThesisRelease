# participant_abm_simulation_results.csv

**Unit of observation:** one row per StoP-valid DS4 participant with ≥14 simulated
days (641).

**Model:** DS4 Agent-Based Modeling (ABM) — tests whether a pure daily-OU agent, built
only from each participant's own already-fitted StoP parameters, reproduces the real
daily-vs-weekly relaxation-time divergence StoP itself found.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `n_days_obs` | int | Simulated series length = real `n_days_obs` |
| `real_theta_daily`, `real_tau_daily` | float | StoP's own real daily-fitted parameters |
| `real_theta_weekly`, `real_tau_weekly` | float | StoP's own real weekly-fitted parameters (`NaN` if not weekly-valid) |
| `model1_theta_daily`, `model1_theta_weekly` | float | Refit on a simulated pure-OU path (no added mechanism) |
| `model2_theta_daily`, `model2_theta_weekly` | float | Refit on a simulated path with an illustrative (not fitted) weekly-periodic drift added |

---

## How this file was produced

- **Source:** `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv`
  and its weekly sensitivity file — agent parameters only, no re-estimation from raw
  behavioral data.
- **Producing notebook:** `notebooks/57_ds4_agent_based.ipynb`
- **Generator script:** `notebooks/make_57_ds4_abm.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_abm_blueprint.md`

## Actual run results (2026-08-07) — a genuine negative result, reported honestly

| | n | corr(daily θ̂, weekly θ̂) | median τ̂ daily | median τ̂ weekly | weekly/daily ratio |
|---|---|---|---|---|---|
| **Real** | 291 | 0.316 | 0.660 | 0.985 | **1.49** |
| Model 1 (pure OU) | 113 | 0.019 | 0.624 | 0.521 | **0.84** |
| Model 2 (+ periodic) | 111 | −0.000 | 0.767 | 0.530 | **0.69** |

**A pure daily-OU agent does not reproduce the real divergence — it gets the direction
wrong.** Real participants' weekly-fitted relaxation time is ~1.5× their daily-fitted
one; both simulated models instead produce weekly τ̂ *smaller* than daily τ̂. The
daily-weekly correlation also collapses in simulation (0.316 real → ~0.02/0.00
simulated) — simulated daily and weekly behavior are essentially statistically
unrelated, unlike real participants. **Model 2's illustrative periodic mechanism does
not fix this — if anything it moves further from the real ratio.**

**Additional finding:** only 133/641 (20.7%) of Model 1's simulated series produce a
valid mean-reverting weekly refit at all, versus 291/641 (45.4%) of real participants —
simulated weekly dynamics are less reliably mean-reverting than real ones too. (The
n=113 in the table above is a stricter population — series with *both* a valid daily
*and* a valid weekly refit, which is what the correlation/ratio calculation requires.
For real participants the daily refit is valid 100% of the time, so that stricter count
happens to equal the weekly-valid-alone count [291=291]; for Model 1 only 549/641
[85.6%] of simulated daily refits converge, so the two counts diverge [113 vs. 133].)

**Conclusion:** the real daily/weekly divergence is not simply a statistical artifact
of aggregating a fixed-parameter mean-reverting process. Real DS4 behavior contains
additional structure — beyond what a single daily-fitted OU triple (μ̂,θ̂,σ̂) encodes —
that a pure local-rule agent, and the one simple non-fitted addition tested here, do
not capture. Reported as a genuine limitation of the simple-agent approach, not spun
into a success.

## Known limitations

- Model 2's amplitude (0.1) is illustrative, not fitted to any real day-of-week
  pattern — a stated simplifying assumption. A negative result does not rule out other
  mechanisms (e.g., non-stationary drift, regime-switching θ).
- Simulated series are gap-free (consecutive days), unlike real data's actual
  observation gaps — a simplification for the generative test.
- Simulated `X_t` is clipped to [0,1] post-hoc; the OU model itself does not respect
  those physical bounds.
- Recoverability/sufficiency test only — not a claim participants literally follow an
  OU process.

## How to load

```python
import pandas as pd

abm = pd.read_csv("outputs/model_outputs/ds4_agent_based/participant_abm_simulation_results.csv")
```
