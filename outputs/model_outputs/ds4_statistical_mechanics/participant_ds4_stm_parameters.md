# participant_ds4_stm_parameters.csv

**Unit of observation:** one row per DS4 participant (all 1,039).

**Model:** DS4 Statistical Mechanics (StM) — the rigorous OU Boltzmann bridge. Resolves
DS5 StM's FLAG A: `beta_OU=2*theta/sigma^2` is exact here, not an approximation, because
the OU stationary distribution really is Gaussian.

**Caveat on "exact" (added by audit):** the OU→Boltzmann algebra is exact, but the *estimates*
are not free of DS5's FLAG A objection. Given how sigma is recovered from the same AR(1) fit,
`beta_OU` collapses to `1/Var_AR1(X_t)` and `T_OU` to that variance; `corr(beta_OU,
theta_hat_OU) = 0.009`, so beta_OU carries essentially no information about the mean-reversion
rate it is claimed to encode.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat` | — | Copied directly from StoP — not re-estimated |
| `beta_OU` | float | `2*theta_hat_OU/sigma_hat_OU^2`. **Numerically this is 1/Var_AR1(X_t):** because StoP recovers sigma from the same AR(1) fit (`sigma^2 = 2*theta*v/(1-phi^2)`), beta_OU reduces algebraically to `(1-phi^2)/v`, so theta cancels. Verified: corr(beta_OU, 1/Var(X_t)) = 0.964, corr(beta_OU, theta_hat_OU) = 0.009. "Exact" refers to the OU→Boltzmann algebra, not to the estimate. |
| `T_OU` | float | `1/beta_OU` — numerically the fitted AR(1) stationary variance of the daily override rate (corr with raw Var(X_t) = 0.981, median ratio 0.986) |
| `p_use` | float | `mu_hat_OU`, clipped to (1e-6, 1-1e-6) — two-state "opened" probability |
| `E_use` | float | Two-state energy of the "opened" state, inverted from `p_use` and `beta_OU` |
| `Z_2state` | float | Two-state partition function, `1/(1-p_use)` |
| `chi_OU` | float | Susceptibility, `beta_OU*p_use*(1-p_use)`. **Redundancy warning:** since beta_OU ≈ 1/Var(X_t) and Var(X_t) is largely binomial sampling noise, chi_OU behaves as a proxy for daily event volume — Spearman(chi_OU, harmonic mean of daily n_events) = 0.888 (median chi_OU 6.85 vs harmonic-mean n 8.46). Interpret with caution wherever it is used as a phenotype dimension (nb59) or as the StM outcome in the GaT ANOVA (nb56). |
| `F_OU` | float | Free energy, `-(1/beta_OU)*ln(Z_2state)` |
| `V_min_location` | float | Location of the OU potential minimum, = `mu_hat_OU` |
| `V_curvature` | float | **Misnamed — holds `theta_hat_OU/2`, the QUADRATIC COEFFICIENT of V(x)=(θ/2)(x−μ)², not the curvature.** The actual curvature is V''(x) = `theta_hat_OU` (twice this column). DS5's v2 work defines its analogous `beta_v2` as V''(x*), so do not compare the two columns without multiplying this one by 2. |
| `V_depth` | float | **Misnamed — holds `beta_OU`, an inverse temperature, not a well depth.** A quadratic potential has no finite depth; this column is an **exact duplicate column of `beta_OU`** (cell 14 assigns `stm["V_depth"] = stm["beta_OU"]`; verified max abs difference = 0 across all 641 valid rows) and carries no additional information. |
| `H_StM` | float | **Identical to InT's `H_SDE`** (verified: max absolute difference 4.4e-16, floating-point noise only) — joined directly, not recomputed |
| `regime_label` | string | Copied from DyS's `participant_dynamics_parameters.csv` |
| `temperature_group` | string | `low_T_high_beta` / `high_T_low_beta`, split on `beta_OU` median (36.55) |
| `fit_valid` | bool | Copied from StoP |

---

## How this file was produced

- **Sources:** `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv`,
  `outputs/model_outputs/ds4_information_theory/participant_entropy_metrics.csv`,
  `outputs/model_outputs/ds4_dynamical_systems/participant_dynamics_parameters.csv`
- **Producing notebook:** `notebooks/51_ds4_statistical_mechanics.ipynb`
- **Generator script:** `notebooks/make_51_ds4_stm.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md` (re-verified
  2026-08-06 against real StoP/InT/DyS output — see its §0)

## Actual run results (2026-08-06)

| Quantity | Median (n=641) |
|---|---|
| `beta_OU` | 36.55 |
| `T_OU` | 0.027 |
| `chi_OU` | 6.85 |
| `tau_hat` | 0.63 days |

- **DS4 vs DS5 (descriptive only):** DS5's `beta_behav` median = 60.9 (approximate);
  DS4's `beta_OU` median = 36.5 (exact). Not directly comparable in magnitude — different
  underlying SDE — reported side-by-side for descriptive interest only.
- **H_StM ≡ H_SDE**, confirmed exactly (not just correlated) — `r(H_StM,H_emp)=0.7206`,
  identical to InT's own `r(H_emp,H_SDE)=0.7206`.
- **`corr(activity_persistence, beta_OU) = 0.0058`** — genuine null, reported honestly.
- **`beta_OU` barely differs by DyS `regime_label`** (`high_control` mean=48.2 vs
  `low_control` mean=49.1) — despite `regime_label` being defined on `theta_hat_OU`
  alone, `beta_OU` combines `theta` and `sigma`, so the two splits don't align strongly.
  Not a strong differentiator; reported as-is, not forced into a narrative.

## Known limitations

- **All quantities are daily-timescale specific** (FLAG VI) — built from StoP's daily
  `theta_hat_OU`/`sigma_hat_OU` only. Inherits StoP's daily-vs-weekly relaxation-time
  divergence.
- **Individual `V(x)` is exact for the OU model assumption, not a direct measurement**
  (FLAG III) — label as "OU model-implied energy landscape."
- No experimental condition — all results are within/cross-participant heterogeneity.
- Real N=641 (not the original blueprint's "~600-800 estimate").
- `X_t` is a behavioral proxy, not a latent psychological state.

## How to load

```python
import pandas as pd

stm = pd.read_csv("outputs/model_outputs/ds4_statistical_mechanics/participant_ds4_stm_parameters.csv")
valid = stm[stm["fit_valid"]]  # 641 rows with real StM values
```
