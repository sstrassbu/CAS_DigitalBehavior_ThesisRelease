# DS4 DyS (Dynamical Systems) Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_dynamical_systems/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/55_ds4_dynamical_systems.ipynb`
**Generator script (to be created):** `notebooks/make_55_ds4_dys.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Dynamical Systems (DyS)
**Prerequisites:** DS4 StoP (53) and DS4 InT (52) — both complete, real output loaded directly.

---

## 1. The central methodological upgrade: a true interior attractor

DS5's DyS notebook (`42_ds5_dynamical_systems.ipynb`) used cautious terminology
throughout — `predicted_boundary_fp`, "empirical resting state," never "attractor" —
because DS5's constant-drift SDE only has a *boundary* fixed point in the σ→0 limit, not
a genuine interior one.

DS4's OU process, `dX_t = θ(μ−X_t)dt + σdW_t`, has an exact deterministic skeleton
`dX/dt = θ(μ−X)`, whose fixed point `X* = μ` is a genuine **interior, stable attractor**
whenever θ>0 (already guaranteed by StoP's own `fit_valid` criterion — every valid StoP
fit already implies a real attractor at `X* = mu_hat_OU`). This is not a DS5 port with
new vocabulary bolted on — it is the resolution of a limitation `ds4_stm_blueprint.md`
and `ds4_01_branch_blueprint.md` both flagged in advance, and it is real: **DS4 can use
the word "attractor" where DS5 explicitly could not — for the 641 of 1,039 participants
(61.7%) with a valid mean-reverting fit. The θ>0 guarantee is a selection: 144 of the 785
participants whose fit was attempted (18.3%) were excluded for φ̂ outside (0,1), i.e. for
not mean-reverting at all.**

---

## 2. What's genuinely new vs. DS5, verified before writing this blueprint

| Quantity | DS5 approach | DS4 approach | Why different |
|---|---|---|---|
| Fixed point | `predicted_boundary_fp` (σ→0 limit approximation) | `X* = mu_hat_OU` (exact, already computed by StoP) | DS4's fixed point is a direct StoP output, not a separate derivation |
| Regime split | `is_dys_eligible` via σ̂<median (deterministic vs stochastic) | `is_high_control` via **θ̂**<median vs ≥median | DS5 never had θ to split on; θ̂ is literally "how strongly does behavior get pulled back," a more direct determinism indicator than σ̂ alone |
| Fixed-point validity check | `deviation_from_predicted_fixed_point` (boundary approx vs. `x_mean`) | `x_mean_raw` (simple empirical mean of daily X_t) vs. `mu_hat_OU` (AR(1)-fitted mean) | **Verified (2026-08-06):** these agree closely — mean absolute deviation 0.0108, `corr=0.9925` (n=641). This is an internal-consistency (arithmetic) check, **not** a goodness-of-fit test: OLS with an intercept forces `mu_hat_OU = c/(1−phi)` to equal the mean of the fitted consecutive-pair series, so the agreement is algebraic (verified: max \|mu(1−phi) − (mean x_t+1 − phi·mean x_t)\| = 1e-15). A null control — the same code on each participant's temporally shuffled daily X_t — scores *better* (`corr=0.9979`, mean deviation 0.0048, n=272 surviving fits), so this check cannot fail and provides no evidence that the OU model fits DS4. |
| InT bridge | `behaviorally_deterministic` = DyS-eligible AND `H_emp`<median | Same construction, using θ̂ instead of σ̂ | **Verified (2026-08-06): `corr(theta_hat_OU, H_emp) = -0.176`** — real direction (higher θ̂, i.e. faster reversion, weakly associates with lower entropy) but **weak**, not the moderate-strength bridge DS5 found between its own DyS/InT quantities. Reported honestly as weak, not oversold. |

---

## 3. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | Fixed point `X* = mu_hat_OU`, taken directly from StoP's output (no re-derivation) | It is StoP's own model parameter — recomputing it here would duplicate StoP, which the blueprint-then-notebook cycle exists to avoid |
| FLAG 2 | Regime split via `theta_hat_OU` median (1.587/day, from StoP's real output) → `high_control` / `low_control` | θ̂ is DS4's own richer parameter; median-split matches DS5's *methodological pattern* (magnitude-based regime split) without reusing DS5's σ-based *content* |
| FLAG 3 | `behaviorally_deterministic` = `high_control` AND `H_emp`<median(H_emp) | Reuses the DS5 bridge-construction pattern; reports the real (weak) correlation honestly rather than assuming DS5's bridge strength transfers |
| FLAG 4 | No bifurcation / multi-well analysis — single fixed point per participant only | Same deferral as DS5 (FLAG 4 there); DS4's OU model is linear-in-drift by construction, so there is exactly one fixed point per participant regardless — a genuinely single-well system, not a simplification being deferred |
| FLAG 5 | Regime split (θ̂) uses **daily**-scale StoP output only | Same daily-timescale caveat as InT's `H_SDE` — StoP's weekly sensitivity file has no weekly θ regime to cross-check against here without re-deriving StoP content |

---

## 4. Theory-to-data mapping

| Theoretical quantity | DS4 variable | Mapping type | Confidence |
|---|---|---|---|
| Deterministic skeleton `dX/dt=θ(μ−X)` | From StoP's `theta_hat_OU`, `mu_hat_OU` | Direct reuse | High |
| Fixed point `X*` | `mu_hat_OU` | Exact (not approximate — first time in this project) | High |
| Stability | Always stable for `fit_valid=True` (θ>0 by construction) | Direct | High |
| Regime label | `high_control` (θ̂≥median) / `low_control` (θ̂<median) — read as fast/slow reversion | Derived, magnitude-based | Low–Medium — real split, but the "control" naming is contradicted by the data (high_control has HIGHER mu, p=3.0e-06) and θ̂ is confounded with daily event volume (ρ=−0.362) |
| Fixed-point internal-consistency check | `\|x_mean_raw − mu_hat_OU\|` | Arithmetic identity check, not a fit test (§2) | n/a — cannot fail |

---

## 5. Notebook structure — `notebooks/55_ds4_dynamical_systems.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope: true interior attractor, what's reused from StoP/InT |
| 2 | MD | FLAG decisions table |
| 3 | MD | DS4 structural cautions (no condition; daily-timescale-only regime split) |
| 4 | MD+LaTeX | Theory: deterministic skeleton `dX/dt=θ(μ−X)`, fixed point `X*=μ`, stability (`θ>0` ⟹ stable) |
| 5 | MD | Theory-to-data mapping table |
| 6 | Code | Setup: load StoP `participant_parameters.csv`, InT `participant_entropy_metrics.csv` |
| 7 | Code | Fixed-point validation: rebuild daily X_t, compute `x_mean_raw` per participant, compare to `mu_hat_OU` (reproduce §2's real numbers) |
| 8 | Code | Regime split: `theta_hat_OU` median, `high_control`/`low_control` labels |
| 9 | Code | InT bridge: `behaviorally_deterministic` flag; reproduce §2's `corr(theta_hat_OU,H_emp)` live |
| 10 | Code | Merge into one table; export `participant_dynamics_parameters.csv` |
| 11 | Code | Distribution summaries: regime counts, `X*` distribution by regime |
| 12 | Code | Export `dys_stop_int_bridge_summary.csv`, `model_run_summary.md` |
| 13 | Code | Figure 1: AR(1) phase plot — `X_t` vs `X_{t+1}` scatter for a sample of participants, with the fitted line and the `X_t=X_{t+1}` diagonal, fixed point marked at intersection (direct visualization of the genuine attractor) |
| 14 | Code | Figure 2: `X*` (mu_hat_OU) distribution, colored/split by regime |
| 15 | Code | Figure 3: `x_mean_raw` vs `mu_hat_OU` scatter with y=x line (validation plot) |
| 16 | Code | Figure 4: `theta_hat_OU` vs `H_emp` scatter (the bridge, shown honestly weak) |
| 17 | MD | Interpretation and limits — state the weak bridge plainly; note this is a single-fixed-point (single-well) system by construction, not a simplification |
| 18 | MD | Forward connections — what StM(51)/NeT(54) consume |

---

## 6. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_dynamical_systems/`

| File | Description | Rows |
|---|---|---|
| `participant_dynamics_parameters.csv` | Per participant: `mu_hat_OU` (=X*), `theta_hat_OU`, `x_mean_raw`, `fixed_point_deviation`, `regime_label`, `behaviorally_deterministic`, `fit_valid` | 1,039 |
| `dys_stop_int_bridge_summary.csv` | Regime counts, `corr(x_mean_raw,mu_hat_OU)`, `corr(theta_hat_OU,H_emp)` | 1 |
| `model_run_summary.md` | Full run record | — |
| `figures/fig1_ds4_phase_plot_sample.png` | AR(1) phase plot, sample participants | — |
| `figures/fig2_ds4_fixed_point_by_regime.png` | X* distribution by regime | — |
| `figures/fig3_ds4_fixedpoint_validation.png` | x_mean_raw vs mu_hat_OU | — |
| `figures/fig4_ds4_theta_hemp_bridge.png` | theta_hat_OU vs H_emp | — |

---

## 7. DS4 weakness flags

- ⚠ FLAG I: InT bridge (`theta_hat_OU` vs `H_emp`) is weak (r=−0.176) — do not present
  `behaviorally_deterministic` as a strongly cross-validated construct; it is a real but
  modest signal.
- ⚠ FLAG II: Regime split is daily-timescale-only — inherits StoP's daily/weekly
  divergence caveat.
- ⚠ FLAG III: No condition variable — regime differences are naturalistic heterogeneity,
  not a friction effect.
- ⚠ FLAG IV: Single-fixed-point system by construction (OU is linear-in-drift) — this is
  a real structural property of the model, not an unexamined simplification, but it does
  mean no multi-stable/bistable dynamics can be found even if they existed behaviorally.
- ⚠ FLAG V: Behavioral proxy limitation persists — `X_t` is a rate, not a latent state.

---

## 8. Forward connections

| Connection | Mechanism | Target |
|---|---|---|
| DS4 DyS → DS4 StM | Interior attractor `X*=mu_hat_OU` gives StM's `V(x)` minimum a genuine behavioral-attractor interpretation, not just a formal minimum | `51_ds4_statistical_mechanics.ipynb` |
| DS4 DyS → DS4 NeT | None directly — NeT is independent (sequence engineering only) | `54_ds4_network_models.ipynb` |
| DS4 DyS → Paper | True interior attractor, resolving DS5 DyS's boundary-only limitation, is not yet in the conceptual paper |

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.

When approved:
1. Create `notebooks/make_55_ds4_dys.py`
2. Run generator, execute notebook, verify against §2's pre-registered numbers
3. Write companion `.md` docs for every output file
4. Update `memory/project_stage.md` and `memory/cross_dataset_strategy.md`
5. Move to DS4 StM (51) — blueprint already exists, re-verify it's still current against
   real StoP/InT/DyS output before implementing
