# DS4 InT (Information Theory) Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_information_theory/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/52_ds4_information_theory.ipynb`
**Generator script (to be created):** `notebooks/make_52_ds4_int.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Information Theory (InT)
**Prerequisite:** DS4 StoP (53) — **complete**, real output loaded directly.

---

## 1. What this notebook does, and what it explicitly is not

Same five-quantity structure as DS5's InT notebook (`45_ds5_information_theory.ipynb`):
outcome entropy, app entropy, hour entropy, empirical state entropy, and a StoP-derived
bridge entropy. **The structure is reused; the content is not.** Every quantity below is
re-derived from DS4's own confirmed data facts (three event classes, no condition, OU
process) — none of DS5's condition-comparison framing carries over, and one quantity
(the bridge entropy) is mathematically different, not just relabeled.

---

## 2. Quantities and their DS4-specific grounding

| # | Quantity | DS4 source | Why it differs from DS5's version |
|---|---|---|---|
| 1 | `H_out_intervention` | `event_outcome_simple` within `intervention_event_class=='intervention_event'` only | DS4's intervention_event class has **exactly 2** outcomes (opened/dismissed — verified, see §3) vs DS5's 3-outcome pooled entropy. Restricting to this class matches StoP's own state-variable population exactly. |
| 2 | `H_out_all_classes` | `event_outcome_simple` pooled across **all** DS4 events (4 categories: opened/dismissed/closed/dismissed_other) | DS5 has one event class, so pooling was never a concern there. DS4 explicitly warns against mixing event classes (`data_docs/modeling_cautions.md` §6) — this quantity is reported as descriptive/exploratory only, never as the primary friction-uncertainty metric, precisely because it violates that caution on purpose to show what's lost by ignoring it. |
| 3 | `H_app` | Stage 1 `app_entropy` from `ds4_behavior_features.csv` (all events, unfiltered by class — confirmed by reading `src/features/ds4_features.py`) | Same role as DS5: broader behavioral-distribution summary, not friction-specific. |
| 4 | `H_hour` | Stage 1 `hour_entropy` from `ds4_behavior_features.csv` | Same role as DS5. |
| 5 | `H_emp` | Empirical Shannon entropy of daily `X_t` (K=10 bins over [0,1]), rebuilt via StoP's own state-variable construction (blueprint §5 of `ds4_stop_blueprint.md`), computed for the same population StoP itself uses | Same K=10 convention as DS5 for comparability of the *method*, but the underlying `X_t` construction is DS4's own (intervention_event class, not DS5's pooled events). |
| 6 | `H_SDE` | **Exact** OU stationary-distribution differential entropy: `H_SDE = 0.5*log2(2*pi*e*sigma_hat_OU^2/(2*theta_hat_OU))`, from `ds4_stochastic_processes/participant_parameters.csv` | This is the real methodological upgrade. DS5's `H_SDE = 0.5*log2(2*pi*e*sig_hat^2)` treats `sig_hat` as a free-diffusion increment std — an **approximation**, since DS5's constant-drift SDE has no true stationary distribution. DS4's OU process has an *exact* Gaussian stationary distribution `N(mu,sigma^2/2theta)`, so this formula is the literal, exact differential entropy of that distribution — not an analogy. This is the quantity `ds4_stm_blueprint.md` §4 already named as belonging to this notebook (its own forward-connections table: "DS4 StM → DS4 InT: H_StM ... target: `52_ds4_information_theory.ipynb`"). |
| 7 (bonus, DS4-only) | `MI(intervention_type; outcome)` | `interventionType` vs `event_outcome_simple`, pooled across `intervention_event` rows | DS4 uniquely logs 6 distinct intervention types (breathingExercise, minimalBreathingExercise, followTheDot, blackScreen, mirror, rotatePhone) — no other dataset in this project has this. DS5's InT explicitly deferred MI/KL (FLAG 4) for lack of a natural pair; DS4 has one that DS5 structurally cannot have. Included as a modest, single, well-motivated addition — not the full MI/KL apparatus DS5 deferred, which stays deferred here too for the same reason (no textual basis in the shared theory paper for a broader MI program). |

---

## 3. Verified facts this blueprint is grounded in (computed 2026-08-06, not assumed)

- Confirmed via crosstab of `intervention_event_class` × `event_outcome_simple`: `intervention_event` rows are **only** `opened`/`dismissed` (909,948 rows total: 603,079 opened + 306,869 dismissed — zero `closed`, zero `dismissed_other`). `app_close_event` is 100% `closed`. `dismissed_other` (812 rows) sits entirely inside `no_intervention`. This confirms item 1 above is a genuine 2-category entropy, and item 2 is a genuine 4-category entropy built by deliberately crossing class boundaries.
- **Redundancy check, done before writing this blueprint (matching this project's established practice):** `H_out_intervention` correlates with StoP's `mu_hat_OU` at **r=−0.631** (n=641, valid fits only). Moderate-strong, not near-1 — the two are related (binary entropy is a deterministic function of the raw opened-proportion, and `mu_hat_OU` is the OU-model-fitted mean of the same series, so some correlation is expected) but not so collinear that either is redundant. Both are reported.
- **Bridge sanity check:** `H_SDE` computed from the 641 valid StoP fits is finite for all 641 (no negative-variance or log-of-nonpositive failures), mean=−0.541 bits, range [−2.59, 0.96] — same plausible order of magnitude as DS5's own `H_SDE` values (control=−0.691, default=−0.118, reintervention=−0.496), which is a reassuring cross-dataset sanity check on the formula/implementation even though the two aren't directly comparable (different underlying SDE).

---

## 4. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | Report both `H_out_intervention` (primary) and `H_out_all_classes` (exploratory, explicitly caveated) | DS4's 3-class architecture has no DS5 analog; §2 items 1–2 explain why neither alone tells the full story |
| FLAG 2 | K=10 bins for `H_emp` | Same convention as DS5, for cross-dataset method comparability; DS4's underlying `X_t` construction is its own, not DS5's |
| FLAG 3 | `H_SDE` uses the **daily**-scale OU fit only (`participant_parameters.csv`), not the weekly sensitivity file | `participant_parameters_weekly_sensitivity.csv` does not export a weekly `sigma_hat_OU` (StoP's cell 14 only fit `theta`/`tau` at weekly resolution, not the full OU triple) — recomputing it here would mean re-deriving StoP content inside InT, which the blueprint-then-notebook cycle exists to avoid. Instead this notebook inherits and states StoP's own documented timescale caveat explicitly (§5) rather than silently presenting a single daily-scale `H_SDE` as "the" bridge entropy. |
| FLAG 4 | MI/KL apparatus stays deferred, except one DS4-specific addition: `MI(intervention_type; outcome)` | Matches DS5's own FLAG 4 deferral (no textual basis in the shared theory paper for a broader MI program); the one addition is included because DS4's 6-type intervention vocabulary has no DS5 equivalent to defer from — this is new ground, not a gap DS5 also had |

---

## 5. Headline carry-forward caveat from StoP — must appear in this notebook

StoP's own weekly-aggregation sensitivity check found DS4's relaxation time is
timescale-dependent: daily median τ̂≈0.63 days vs weekly median τ̂≈0.91 weeks (≈6.4 days),
with only r=0.316 correlation between daily and weekly θ̂ per participant
(`participant_parameters_weekly_sensitivity.md`). `H_SDE` in this notebook is built from
the **daily**-scale `sigma_hat_OU`/`theta_hat_OU` only (FLAG 3). This notebook must state
plainly that `H_SDE` therefore describes daily-timescale uncertainty specifically, not a
timescale-independent property of the participant.

---

## 6. Notebook structure — `notebooks/52_ds4_information_theory.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope statement: 5+1 quantities, what's reused from StoP, what's new |
| 2 | MD | FLAG decisions table (§4) |
| 3 | MD | DS4 structural cautions: 3 event classes (§2 items 1–2), no condition |
| 4 | MD+LaTeX | Theory: Shannon entropy `H=-sum p*log2(p)`; OU stationary differential entropy `H=0.5*log2(2*pi*e*sigma^2/2theta)` derivation from `N(mu,sigma^2/2theta)` |
| 5 | MD | Theory-to-data mapping table (the 7 rows of §2) |
| 6 | Code | Setup: imports, paths, `K_BINS=10` |
| 7 | Code | Load `ds4_behavioral_clean.csv`, `ds4_behavior_features.csv`, and StoP's `participant_parameters.csv` |
| 8 | Code | `H_out_intervention` and `H_out_all_classes` per participant (Shannon entropy over outcome PMFs, each class scope from §2) |
| 9 | Code | Load `H_app`/`H_hour` directly from Stage 1 features (rename to InT column names) |
| 10 | Code | Rebuild daily `X_t` (identical construction to StoP §5) and compute `H_emp` (K=10 binned entropy) for the StoP-eligible population |
| 11 | Code | `H_SDE` from StoP's `sigma_hat_OU`/`theta_hat_OU` (exact OU stationary entropy formula) |
| 12 | Code | Redundancy check: `corr(H_out_intervention, mu_hat_OU)` — reproduce and report the real §3 number from live data |
| 13 | Code | `MI(intervention_type; outcome)` — pooled contingency table over `intervention_event` rows; verify `MI>=0` |
| 14 | Code | Merge all entropy measures + StoP parameters into one participant-level table; export `participant_entropy_metrics.csv` |
| 15 | Code | Distribution summaries (mean/median/percentiles) for all 6 entropy quantities |
| 16 | Code | Export `int_stop_bridge_summary.csv` (H_SDE vs H_emp correlation, the InT-StoP bridge validation, mirroring DS5's own `r(H_SDE,H_emp)` check) |
| 17 | Code | Export `model_run_summary.md` |
| 18 | Code | Figure 1: `H_out_intervention` vs `H_out_all_classes` scatter, colored by `intervention_event_share` (shows how much the two outcome-entropy views diverge per participant) |
| 19 | Code | Figure 2: `H_emp` vs `H_SDE` scatter (the bridge validation plot, DS5-style) |
| 20 | Code | Figure 3: `H_app`/`H_hour` distributions (histograms) |
| 21 | Code | Figure 4: `MI(intervention_type; outcome)` bar chart by intervention type (which types are most/least predictive of outcome) |
| 22 | MD | Interpretation and limits — restate §5's daily-timescale caveat; report the §3 redundancy number live; state MI(type;outcome) findings without overclaiming causality |
| 23 | MD | Forward connections — what DyS(55)/StM(51)/NeT(54) each consume from this notebook |

---

## 7. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_information_theory/`

| File | Description | Rows |
|---|---|---|
| `participant_entropy_metrics.csv` | Per participant: `H_out_intervention`, `H_out_all_classes`, `H_app`, `H_hour`, `H_emp`, `H_SDE`, plus StoP's `mu_hat_OU`/`theta_hat_OU`/`sigma_hat_OU`/`tau_hat`/`fit_valid` for direct joint use | 1,039 (NaN where inputs are NaN) |
| `int_stop_bridge_summary.csv` | `r(H_SDE,H_emp)`, `r(H_out_intervention,mu_hat_OU)`, sample sizes | 1 |
| `intervention_type_outcome_mi.csv` | Per-type outcome PMF + overall `MI(intervention_type;outcome)` | 1 (+ 6 type rows) |
| `model_run_summary.md` | Full run record | — |
| `figures/fig1_ds4_hout_comparison.png` | H_out_intervention vs H_out_all_classes | — |
| `figures/fig2_ds4_hemp_hsde_bridge.png` | H_emp vs H_SDE | — |
| `figures/fig3_ds4_happ_hhour_dist.png` | H_app/H_hour histograms | — |
| `figures/fig4_ds4_mi_by_type.png` | MI(type;outcome) contribution by intervention type | — |

---

## 8. DS4 weakness flags

- ⚠ FLAG I: `H_out_all_classes` mixes structurally different logging paths (per §2 item 2)
  — descriptive only, never the primary metric.
- ⚠ FLAG II: `H_SDE` is daily-timescale specific (§5) — do not present as "the" DS4
  behavioral-uncertainty bridge without that qualifier.
- ⚠ FLAG III: `H_out_intervention` and `mu_hat_OU` share real but partial variance
  (r=−0.631) — report both, do not treat as two fully independent lines of evidence.
- ⚠ FLAG IV: `MI(intervention_type;outcome)` is correlational; intervention type is not
  randomly assigned in DS4 (naturalistic, participant/app-context-driven), so this is not
  a causal claim about which intervention type "works better."
- ⚠ FLAG V: All entropy measures inherit `X_t`'s behavioral-proxy limitation (same as
  StoP, same as DS5).

---

## 9. Forward connections

| Connection | Mechanism | Target |
|---|---|---|
| DS4 InT → DS4 DyS | `H_emp` as the model-selection criterion between deterministic/stochastic regimes, same role as DS5's StoP↔DyS↔InT bridge | `55_ds4_dynamical_systems.ipynb` |
| DS4 InT → DS4 StM | `H_SDE` formula is identical to `ds4_stm_blueprint.md`'s own `H_StM` — this notebook computes it first; StM reuses it for its own convergence check | `51_ds4_statistical_mechanics.ipynb` |
| DS4 InT → Paper | Exact OU stationary entropy formula, and the daily/weekly `H_SDE` timescale caveat, are not yet in the conceptual paper |

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.

When approved:
1. Create `notebooks/make_52_ds4_int.py`
2. Run generator, execute notebook, verify against §3's pre-registered numbers
3. Write companion `.md` docs for every output file
4. Update `memory/project_stage.md` and `memory/cross_dataset_strategy.md`
5. Move to DS4 DyS (55) blueprint, informed by this notebook's real output
