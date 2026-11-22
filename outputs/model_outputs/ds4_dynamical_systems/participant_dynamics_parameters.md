# participant_dynamics_parameters.csv

**Unit of observation:** one row per DS4 participant (all 1,039).

**Model:** DS4 Dynamical Systems (DyS) — characterizes the OU fixed point `X*=mu_hat_OU`
as a genuine interior attractor, checks it for arithmetic consistency against the raw empirical mean, and splits
participants into control regimes.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `mu_hat_OU` | float | Copied from StoP — also `X*`, the OU fixed point / attractor location |
| `theta_hat_OU` | float | Copied from StoP — mean-reversion rate, also the basis for the regime split |
| `x_mean_raw` | float | Simple empirical mean of daily `X_t` (not model-fitted) — `NaN` unless the participant has ≥1 daily observation |
| `fixed_point_deviation` | float | `\|x_mean_raw - mu_hat_OU\|` — gap between the all-days mean and the consecutive-pair mean the AR(1) was fitted on (plus 1/(1−phi) estimation noise). **Not a model-fit statistic** — no residual enters it. Strongest correlate is observation coverage: r=−0.569 with the fraction of days in a consecutive pair, r=−0.447 with n_consec_pairs, vs only r=+0.204 with sigma_hat_OU. `NaN` unless `fit_valid` |
| `regime_label` | string | `high_control` (`theta_hat_OU`≥median) or `low_control` (<median). **The names are historical and normatively misleading** — read them as `fast_reversion`/`slow_reversion`. theta is a mean-reversion RATE, not a level of self-control (that is mu): the `high_control` group actually has a HIGHER long-run override rate (mu 0.7164 vs 0.6623, Welch p=3.0e-06) and ~38% fewer intervention events per day (median 10.5 vs 17.0). `NaN` unless `fit_valid` |
| `behaviorally_deterministic` | bool | `True` iff `regime_label=='high_control'` AND `H_emp`<median(H_emp). `NaN` unless `fit_valid` |
| `H_emp` | float | Copied from InT's `participant_entropy_metrics.csv` |
| `fit_valid` | bool | Copied from StoP |

---

## How this file was produced

- **Sources:** `outputs/cleaned/ds4_behavioral_clean.csv`,
  `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv`,
  `outputs/model_outputs/ds4_information_theory/participant_entropy_metrics.csv`
- **Producing notebook:** `notebooks/55_ds4_dynamical_systems.ipynb`
- **Generator script:** `notebooks/make_55_ds4_dys.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_dys_blueprint.md`

## Actual run results (2026-08-06)

- Fixed-point internal-consistency check (n=641): `corr(x_mean_raw, mu_hat_OU)=0.9925`, mean absolute
  deviation=0.0108, max=0.129. This is an arithmetic identity, not a fit test — OLS with an intercept
  forces `mu_hat_OU=c/(1−phi)` to equal the fitted pair-series mean; a temporally shuffled null scores
  better (corr=0.9979, mean deviation=0.0048, n=272). No goodness-of-fit conclusion follows from it.
- `theta_hat_OU` median = 1.587/day → regime split: 321 `high_control`, 320 `low_control`
  (398 `NaN` for participants without a valid StoP fit).
- InT bridge: `corr(theta_hat_OU, H_emp) = -0.176` (n=641) — real direction, weak
  magnitude. 173 participants flagged `behaviorally_deterministic`.

## Known limitations

- **The theta/H_emp bridge is weak (r=−0.176), not the moderate-strength bridge DS5
  found between its own DyS/InT quantities.** Do not present `behaviorally_deterministic`
  as strongly cross-validated.
- **Regime split is daily-timescale-only** — inherits StoP's own daily-vs-weekly
  relaxation-time divergence (see `ds4_stochastic_processes/participant_parameters.md`).
  A participant's regime label under a weekly-scale θ̂ was not tested.
- **theta is confounded with daily event volume.** Spearman(theta_hat_OU, mean daily
  intervention-event count) = −0.362 (p=2.7e-21, n=641): X_t is a ratio over few daily
  events for low-volume participants, so day-to-day sampling noise pushes phi toward 0 and
  theta up. This is StoP's own unresolved "genuine fast habitual reversion vs. daily-ratio
  sampling noise" reading (`ds4_stochastic_processes/model_run_summary.md`), inherited here
  and not resolved.
- No experimental condition — regime differences are naturalistic heterogeneity, not a
  friction effect.
- Every `fit_valid=True` participant has θ̂>0 by construction, so every one of them has a
  genuine stable attractor — but this is a **selection effect**, not a DS4-wide property.
  StoP's funnel: 1,039 total → 785 attempted (≥30 daily observations and ≥10 consecutive
  pairs) → 641 valid; the 144 dropped (18.3% of attempted) were dropped precisely because
  φ̂ fell outside (0,1), i.e. they showed no mean reversion. An interior attractor is
  established for 641/1,039 = 61.7% of DS4, not for DS4 as a whole. `regime_label`
  distinguishes *how fast* reversion is within that 61.7%, not *whether* an attractor exists.
- `X_t` is a behavioral proxy, not a latent psychological state.

## How to load

```python
import pandas as pd

dys = pd.read_csv("outputs/model_outputs/ds4_dynamical_systems/participant_dynamics_parameters.csv")
valid = dys[dys["fit_valid"]]  # 641 rows with a real regime label
```
