# DS5 InT Model — Implementation Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**  
**Written:** 2026-04-17  
**Notebook:** `notebooks/45_ds5_information_theory.ipynb`  
**Producing dataset:** DS5 (German Adolescents RCT, N=573)  
**Model family:** Information Theory (InT)

---

## Purpose

This document is the companion blueprint for the DS5 InT implementation. It records the design decisions, the theory-to-data translation, the FLAG decisions in effect, the relation to the completed StoP notebook, and the outputs produced. It is the primary reference for understanding the notebook and for extending the analysis in future stages.

---

## FLAG decisions in effect

| Flag | Decision | Rationale |
|---|---|---|
| FLAG 1 | Discrete Shannon entropy as the primary measure | Lowest-complexity and most defensible first-pass formulation; directly aligned with paper Eq. 25 |
| FLAG 2 | Empirical PMF from raw frequency counts (no smoothing) | Avoids introducing subjective smoothing hyperparameters in Step 1 |
| FLAG 3 | StoP→InT bridge via Gaussian differential entropy: `H_SDE = 1/2 log2(2πeσ²)` | Cleanest mathematical bridge from completed StoP model; uses already-estimated `sig_hat` |
| FLAG 4 | Mutual information, conditional entropy, KL divergence deferred | Stronger estimation choices and bias corrections are better deferred to later extension |

---

## Core model

### Primary Shannon entropy (paper Eq. 25)

    H(X) = - Σ p(x) log2 p(x)

This is the core Information Theory quantity used in the notebook.

### Core entropy dimensions implemented

1. **H_out** — entropy of friction outcomes (`opened`, `dismissed`, `closed`)
2. **H_app** — entropy of app distribution
3. **H_hour** — entropy of hour-of-day distribution
4. **H_emp** — empirical entropy of the daily behavioral state proxy `X_t`
5. **H_SDE** — StoP bridge quantity derived from `sig_hat`

### StoP→InT bridge (not currently in paper)

    H_SDE = 1/2 * log2(2πeσ²)

This is the differential entropy of a Gaussian with variance `σ²`. In this notebook it is used only as a **bridge quantity** derived from the completed StoP notebook. It is not an independent empirical measure in the same sense as `H_out`, `H_app`, `H_hour`, or `H_emp`.

**BRIDGE WARNING:** `H_SDE` is mathematically standard but is not currently written explicitly in the conceptual paper. It should be added before final paper submission if StoP↔InT bridge results are reported.

---

## Theory-to-data mapping

| Theoretical quantity | Data source | Column / computation | Proxy limitation |
|---|---|---|---|
| Outcome entropy `H_out` | `outputs/cleaned/ds5_behavioral_clean.csv` | Shannon entropy over `event_outcome_simple` frequency distribution per participant | Outcome mix is condition-sensitive; control-group structure must be interpreted cautiously |
| App entropy `H_app` | `outputs/features/ds5/ds5_behavior_features.csv` | `app_entropy` (Stage 1 feature, reframed as InT quantity) | Computed over app distribution, not only friction-triggered states |
| Hour entropy `H_hour` | `outputs/features/ds5/ds5_behavior_features.csv` | `hour_entropy` (Stage 1 feature, reframed as InT quantity) | Based on cleaned time extraction; broader behavioral timing, not only friction-response uncertainty |
| Empirical state entropy `H_emp` | `outputs/cleaned/ds5_behavioral_clean.csv` | Shannon entropy of binned daily `X_t` distribution per participant (`K=10` bins over `[0,1]`) | Inherits all proxy limitations of `X_t`; sensitive to short windows |
| Bridge entropy `H_SDE` | `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | `0.5 * log2(2πe * sig_hat^2)` | Derived from StoP assumptions; monotone transform of `sig_hat`, not independent evidence |
| Outcome PMF `p(outcome)` | `outputs/cleaned/ds5_behavioral_clean.csv` | Frequency counts of `opened`, `dismissed`, `closed` | Missing / excluded outcomes must be filtered consistently |
| Behavioral state `X_t` | Recomputed from event-level DS5 behavioral file | Daily override rate: `n_opened_day / n_events_day` | Same proxy warning as StoP: behavioral rate, not latent urge or self-control |
| Psychosocial correlates | `outputs/features/ds5/ds5_survey_features.csv` | `fomo_mean_pre`, `belong_mean_pre`, `ostracism_mean_pre`, `digital_wellbeing_pre` | Exploratory only; no multiple-comparison correction in Step 1 |

---

## Data pipeline

### Sources

| File | Role |
|---|---|
| `outputs/cleaned/ds5_behavioral_clean.csv` | Event-level behavioral data |
| `outputs/features/ds5/ds5_behavior_features.csv` | Stage 1 app/time entropy features already computed |
| `outputs/features/ds5/ds5_survey_features.csv` | Study condition and psychosocial scales |
| `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | StoP output used for `sig_hat` and `H_SDE` bridge |

### Key pipeline steps

1. Load event-level behavioral data
2. Filter to valid DS5 outcome rows with `event_outcome_simple` in `{opened, dismissed, closed}`
3. Compute participant-level outcome PMFs and `H_out`
4. Re-aggregate daily `X_t` from event-level data
5. Bin `X_t` into `K=10` bins over `[0,1]` and compute `H_emp`
6. Load Stage 1 `app_entropy` and `hour_entropy` as `H_app` and `H_hour`
7. Load StoP `sig_hat` and compute `H_SDE`
8. Merge all entropy measures into one participant-level table
9. Join condition and psychosocial covariates
10. Export participant table, condition summaries, StoP↔InT comparison table, correlation table, and figures

### DS5 structural notes (required reading)

- `H_out` is the most directly friction-related entropy measure
- `H_app` and `H_hour` are broader behavioral-distribution summaries and should not be interpreted as direct measures of friction-response uncertainty
- `H_SDE` is a StoP-derived bridge quantity, not an independent primary InT metric
- `H_emp` depends on the same proxy state variable `X_t` used in StoP, so it shares StoP’s proxy limitations
- Condition comparisons are strongest for `H_out`; weaker and more contextual for `H_app` / `H_hour`

---

## Equations in use

### Already in the paper

| Equation | Paper reference | Status | Role |
|---|---|---|---|
| `H(X) = - Σ p(x) log2 p(x)` | Eq. 25 | In paper | Core entropy estimator |
| `H(X,Y) = - Σ p(x,y) log2 p(x,y)` | Eq. 26 | In paper | Deferred; theoretical background only |
| `H(Y|X) = H(X,Y) - H(X)` | Eq. 27 | In paper | Deferred |
| `I(X;Y) = H(X) + H(Y) - H(X,Y)` | Eq. 28 | In paper | Deferred |
| `D_KL(P||Q) = Σ p_i (log p_i - log q_i)` | Eq. 29 | In paper | Deferred |

### Not explicitly in the paper but used / needed

| Equation | Status | Action required |
|---|---|---|
| `H_SDE = 1/2 log2(2πeσ²)` | Standard result, not currently in paper | **Add to paper** if StoP↔InT bridge is reported |
| `p_hat(x) = count(x) / n` | Standard implementation detail | No paper addition needed |
| `H_emp = - Σ p_hat_k log2 p_hat_k` over binned `X_t` | Standard implementation detail | Document as implementation choice only |

### Interpretation note on `H_SDE`

Differential entropy may be negative for narrow Gaussian distributions. This is mathematically valid. In this notebook, `H_SDE` is used comparatively, not as an absolute “amount of information” in the colloquial sense.

---

## Outputs

**Output directory:** `outputs/model_outputs/information_theory/`  
**Figures directory:** `outputs/model_outputs/information_theory/figures/`

| File | Description |
|---|---|
| `participant_entropy_metrics.csv` | Per-participant entropy profile table |
| `participant_entropy_metrics.md` | Companion column reference |
| `condition_entropy_summary.csv` | Condition-level means, medians, std for entropy measures |
| `condition_entropy_summary.md` | Companion documentation |
| `stop_int_comparison.csv` | StoP↔InT bridge table for participants with both `sig_hat` and `H_emp` |
| `stop_int_comparison.md` | Companion documentation |
| `psychosocial_entropy_correlations.csv` | Exploratory correlations of entropy measures with psychosocial scales |
| `psychosocial_entropy_correlations.md` | Companion documentation |
| `model_run_summary.md` | Run record with parameters, decisions, and key findings |
| `figures/fig1_int_entropy_by_condition.png` | Condition-wise entropy distributions |
| `figures/fig2_int_stop_bridge.png` | `H_SDE` vs `H_emp` bridge-validation scatter |
| `figures/fig3_int_entropy_correlation_matrix.png` | Correlation matrix of entropy dimensions |
| `figures/fig4_int_fomo_vs_entropy.png` | FoMO vs selected entropy measures |

---

## Actual results (2026-04-17 run)

### Eligibility and row counts

- `participant_entropy_metrics.csv`: **572 rows × 9 columns**
- `stop_int_comparison.csv`: **414 rows**
- `condition_entropy_summary.csv`: **15 rows**
- `psychosocial_entropy_correlations.csv`: **25 rows**

### Key condition-level findings

#### Outcome entropy `H_out`

| Condition | Mean `H_out` |
|---|---|
| control | 0.691 bits |
| default | 0.940 bits |
| reintervention | 0.902 bits |

**Interpretation note:** Friction conditions show higher `H_out`, but this is partly structural because control participants have a more concentrated outcome distribution by design. Do not overstate this as a pure intervention effect on uncertainty.

#### StoP bridge entropy `H_SDE`

| Condition | Mean `H_SDE` |
|---|---|
| control | -0.691 bits |
| default | -0.118 bits |
| reintervention | -0.496 bits |

This ordering exactly mirrors the StoP `sig_hat` ordering and is therefore a **re-expression of StoP in entropy units**, not independent new evidence.

#### Bridge validation: `H_SDE` vs `H_emp`

- Pearson `r = 0.650` (`n = 414`)

This indicates that increment-scale dispersion (H_SDE, a deterministic monotone transform of sig_hat) and level-scale dispersion (H_emp) co-vary across participants. It is a descriptive cross-model consistency check, NOT a test of the Gaussian increment assumption: H_SDE carries no information about the shape of the increment distribution, and H_emp is the entropy of the daily level series, not of the increments. A control quantity with no Gaussian content, log2(SD of the daily X_t levels), correlates with H_emp at r = 0.720 — higher than the bridge itself — and r(H_SDE, log2 SD_level) = 0.911, confirming H_SDE is essentially log-spread. A genuine test would require a normality test on diff(X_t) (Shapiro rejects normality for 98/414 participants, 23.7%).

#### App and hour entropy

- No condition differences in `H_app` (one-way ANOVA F = 1.01, p = 0.364; Kruskal-Wallis H = 1.17, p = 0.556; n = 184/197/187) or `H_hour` (F = 1.39, p = 0.251; H = 0.16, p = 0.924; n = 157/168/156)
- This is expected and should be interpreted as contextual descriptive information, not direct friction-response evidence

#### Condition tests for all five measures (added in audit; computed from `participant_entropy_metrics.csv`)

| Measure | n (ctrl/def/reint) | ANOVA F | ANOVA p | Kruskal H | Kruskal p |
|---|---|---|---|---|---|
| H_out | 156/166/156 | 39.01 | 2.07e-16 | 82.63 | 1.14e-18 |
| H_app | 184/197/187 | 1.01 | 0.364 | 1.17 | 0.556 |
| H_hour | 157/168/156 | 1.39 | 0.251 | 0.16 | 0.924 |
| H_emp | 137/142/135 | 66.31 | 1.10e-25 | 102.19 | 6.46e-23 |
| H_SDE | 137/142/135 | 21.67 | 1.13e-09 | 44.23 | 2.49e-10 |

Note: the original 2026-04-17 run computed no inferential statistics at all; these were added retrospectively during the audit and confirm every claim made from the means alone.

### Exploratory psychosocial findings

- **FoMO ~ `H_SDE`**: `r = -0.13`, `p = 0.038`
  - This is a mathematical replication of the StoP FoMO ~ `sig_hat` association, not an independent discovery
- **Social media wellbeing ~ `H_app`**: `r = +0.10`, `p = 0.044` — **not robust; do not report as a finding.** `H_app` is exactly 0 for 212/384 (55.2%) of this sample (320/573 DS5 participants use only one distinct app), so Pearson is inappropriate here. Spearman gives `r = 0.063`, `p = 0.215`, and the zero/non-zero indicator alone gives `r = 0.024`, `p = 0.642`: the association exists only in the small multi-app tail.
- **Social media wellbeing ~ `H_hour`**: `r = -0.13`, `p = 0.024`
- **Social media wellbeing ~ `H_SDE`**: `r = +0.12`, `p = 0.042`
  - Same caveat as FoMO ~ `H_SDE`: re-expresses the StoP social media wellbeing ~ `sig_hat` association in entropy units, not independent evidence

All psychosocial findings are exploratory and uncorrected for multiple testing. (4 of 25 tests are nominally significant at p<0.05; see `psychosocial_entropy_correlations.csv` for the full table.)

---

## What is genuinely new vs re-expressed from StoP

### Re-expressions of StoP

| Quantity | Why it is not independent |
|---|---|
| `H_SDE` | Deterministic monotone transform of `sig_hat` |
| FoMO ~ `H_SDE` | Same information as FoMO ~ `sig_hat` in different units |

### Genuinely new InT contributions

| Quantity | What it adds |
|---|---|
| `H_out` | Outcome-level unpredictability not captured by StoP |
| `H_app` | App repertoire diversity |
| `H_hour` | Temporal-context diversity |
| `H_emp` | Non-parametric entropy of the behavioral state proxy; partial validation of StoP assumptions |

---

## Known limitations

1. **`H_SDE` is not in the paper yet**  
   The bridge equation must be added if the StoP↔InT bridge is reported.

2. **`H_SDE` is not independent evidence**  
   It is a transform of `sig_hat`, not a new model output in the empirical sense.

3. **`H_SDE` is volume-confounded**  
   X_t is a binomial proportion, so daily event volume mechanically drives increment scale: r(H_SDE, mean events/day) = −0.511, r(H_SDE, share of 1-event days) = +0.541. The default arm has the lowest daily volume (15.43 vs 21.76 control / 21.10 reintervention, ANOVA F = 5.27, p = 0.0055) and the highest H_SDE. Residualising H_SDE on log(mean events/day) leaves the condition contrast significant (F 21.67 → 19.57, p = 7.6e-09) and the H_SDE~H_emp relation intact (r 0.650 → partial 0.697), so no reported result changes — but H_SDE is not a pure behavioural-unpredictability measure.

4. **`H_out` is a non-monotonic transform of the outcome mix**  
   The outcome mix is itself the RCT's primary endpoint, so `H_out` is not confounded by an external design factor — it re-encodes the endpoint. Pooled event-level shares: control 73.1% opened / 15.4% dismissed / 11.5% closed; default 50.5 / 31.0 / 18.5; reintervention 61.2 / 20.9 / 17.9 (per-participant mean `rate_opened`: 0.7635 / 0.5287 / 0.6097). Because entropy peaks at the uniform mix (p_opened = 1/3), participants on opposite sides of that point map to the same `H_out` — r(`H_out`, `rate_opened`) = −0.701 versus r(`H_out`, |`rate_opened` − 1/3|) = −0.861, with 39/478 participants below the turning point. Report `H_out` alongside `rate_opened`, not instead of it.

5. **`H_emp` depends on binning choice (`K=10`)**  
   This is reasonable for Step 1, but still an implementation choice.

6. **`H_app` and `H_hour` are broader behavioral measures**  
   They do not isolate friction-response uncertainty.

7. **All entropy measures inherit DS5 scope limits**  
   No phenotype labeling, no mutual information, no transfer entropy, no cross-dataset entropy claims yet.

8. **Psychosocial correlations are exploratory**  
   Multiple comparisons are uncorrected.

---

## Forward connections

| Connection | Mechanism | Target notebook |
|---|---|---|
| InT → StoP | `H_SDE` is derived from StoP `sig_hat` | `43_ds5_stochastic_processes.ipynb` |
| InT → DyS | Low `H_emp` participants are candidates for deterministic-limit interpretation | `42_ds5_dynamical_systems.ipynb` |
| InT → StM | Stationary-distribution / entropy framing can later connect to thermodynamic interpretation | `41_ds5_statistical_mechanics.ipynb` |
| InT → Phenotyping | Entropy profile dimensions contribute to Step 2 behavioral profile vector | future Step 2 notebook |

---

## Equation gaps resolved vs deferred

| Gap | Status | Resolution |
|---|---|---|
| Core Shannon entropy | Resolved | Paper Eq. 25 used directly |
| Outcome / app / hour entropy | Resolved | Implemented as participant-level entropy measures |
| StoP→InT bridge | Resolved in notebook, missing in paper | Must add Gaussian differential entropy equation to paper |
| Empirical entropy of `X_t` | Resolved | Implemented as binned entropy (`K=10`) |
| Mutual information | Deferred | Step 2 extension |
| Conditional entropy | Deferred | Step 2 extension |
| KL divergence | Deferred | Step 2 extension |
| Bias corrections for sparse PMFs | Deferred | Later methodological refinement if needed |

---

## How to load the output

```python
import pandas as pd
from pathlib import Path

entropy = pd.read_csv(
    Path("outputs/model_outputs/information_theory/participant_entropy_metrics.csv")
)

# One row per participant
# Main columns: H_out, H_app, H_hour, H_emp, H_SDE, sig_hat, study_condition