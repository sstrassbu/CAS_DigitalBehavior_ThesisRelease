# DS4 StM Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**  
**Written:** 2026-04-17  
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_statistical_mechanics/model_run_summary.md` for actual
executed results. Blueprint preserved below as the pre-registration record (already
carrying its own §0 dated revision note); unmodified except for this status line.  
**Notebook (to be created):** `notebooks/51_ds4_statistical_mechanics.ipynb`  
**Generator script (to be created):** `notebooks/make_51_ds4_stm.py`  
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)  
**Model family:** Statistical Mechanics (StM)  
**Prerequisites:** DS5 StM (nb 41 — complete); DS4 StoP (53), DS4 InT (52), DS4 DyS (55)
— all complete, real output loaded directly (see §0).

---

## 0. Re-verification note (2026-08-06) — read before implementing

This blueprint was written 2026-04-17, before DS4 StoP/InT/DyS existed. Per this
project's binding rule (never implement a pre-existing blueprint on the assumption it's
still current), it has now been checked against their real output and revised where
needed. Everything below in §§1–14 is the *original* 2026-04-17 text except the specific
edits called out here — this is a transparent revision, not a silent rewrite.

**What changed:**

1. **Do not re-estimate μ̂_OU/θ̂_OU/σ̂_OU here.** StoP's `participant_parameters.csv`
   already has them (real N=641 valid fits, closed-form AR(1)-OLS conditional MLE — see
   below). §6 cells 9–11 (originally "OU parameter estimation per participant") are
   replaced by a single "load StoP output directly" cell. Recomputing would risk a
   silently-inconsistent second estimate of the same quantity.
2. **Do not recompute H_StM independently.** For DS4 specifically (unlike DS5), the
   formula this blueprint's own §6 cell 16 already specified —
   `H_StM = 0.5*log2(2*pi*e*sigma_hat_OU^2/(2*theta_hat_OU))` — is **the exact same
   formula** InT's `H_SDE` already uses (`ds4_int_blueprint.md` §2, item 6). This isn't a
   DS5-style "H_StM≈H_SDE, both from σ̂" approximate correlation — for DS4 they are
   mathematically identical. StM should join InT's `H_SDE` column directly rather than
   recompute a second, redundant copy under a different name.
3. **Real eligible N = 641**, not the "~600-800 (estimate)" in §7/§11 — StoP's actual
   `fit_valid` population, which StM inherits directly (no separate re-filtering).
4. **The illustrative "if τ̂=14 days..." example in §10 point 4 was always hypothetical
   and is now known to be off by roughly an order of magnitude.** StoP's real result:
   median τ̂≈0.63 days at daily aggregation, but ≈0.91 weeks (≈6.4 days) at weekly
   aggregation — a genuine, unresolved timescale divergence (r=0.316 between daily and
   weekly θ̂ per participant). β_OU/χ_OU/H_StM in this notebook are built from the
   **daily**-scale StoP parameters specifically — state this explicitly, matching the
   same caveat already carried through InT and DyS.
5. **§13's forward-connections direction is backwards** relative to the order actually
   implemented (StoP→InT→DyS→StM, matching the project-wide established order — this
   blueprint was written before that order was locked in). InT and DyS did not wait for
   StM; they already used StoP's μ̂/θ̂/σ̂ directly. StM now *consumes* InT's H_SDE and
   DyS's attractor/regime characterization, rather than producing inputs for them to
   consume later. See the corrected table in §13.
6. **§14 (DS5 NeT continuation notes) is obsolete** — DS5 NeT finished 2026-04-17, the
   same day this blueprint was written, and the rest of DS5 Step 1 has been complete for
   months. Left in place below for historical record only; not relevant to DS4 StM
   implementation.
7. **FLAG 2 (§3)** is updated to reflect the estimator StoP actually used (closed-form
   AR(1) OLS on consecutive-day pairs = the exact conditional MLE for fixed Δt=1) rather
   than the originally-proposed generic "MLE via scipy/statsmodels."
8. **Free energy is implemented as the two-state partition-function form, not §5's U − TS.**
   §5 specifies `F_i = E_use_i − (1/β_OU_i)·H_emp_i`. The notebook (cell 12, and its own
   Theory 2 markdown) instead computes `F_OU = −(1/β_OU)·ln(Z_2state)`, consistent with §4's
   own `F = −(1/β) ln Z` row and with the two-state apparatus actually built. The §5 version
   would have mixed a two-state energy with InT's binned-X_t entropy, which are on different
   state spaces. [Recorded 2026-08-08 by audit — deviation was previously undocumented.]
9. **Two §7 output files were not produced.** `participant_vx_parameters.csv` was folded into
   `participant_ds4_stm_parameters.csv` (columns `V_min_location`/`V_curvature`/`V_depth`),
   and `psychosocial_ds4_stm_correlations.csv` was dropped — cell 19 computes and prints
   `corr(activity_persistence, beta_OU)` but exports no file, since DS4 has no psychosocial
   instrument and only one usable behavioural correlate. [Recorded 2026-08-08 by audit.]

---

## Notebook numbering convention

DS4 notebooks follow the 5x_ prefix:
- 51 = DS4 StM (this blueprint)
- 52 = DS4 InT
- 53 = DS4 StoP ← **this should actually be built first; see §12 below**
- 54 = DS4 NeT
- etc.

DS5 notebooks use the 4x_ prefix (41–48 reserved).

---

## 1. Why DS4 is the right dataset for rigorous StM

### The central argument

DS5 StM implemented the Boltzmann bridge as an approximation (FLAG A in notebook 41).
The approximation exists because the DS5 StoP model used a constant-drift SDE
(dX_t = μ dt + σ dW_t), which has a linear, non-confining potential V(x) = −μx.
This does not produce a proper Boltzmann stationary distribution.

DS4 provides the conditions to make the Boltzmann bridge rigorous for the first time:

1. **Longer observation windows than DS5.** The Ornstein-Uhlenbeck (OU) process has
   a mean-reversion parameter θ that cannot be reliably estimated from 7-45 day windows
   (DS5). [Corrected 2026-08-08 by audit: the often-quoted 897-day figure is computed over
   all three DS4 event classes. Restricted to the `intervention_event` rows that actually
   form X_t, the per-participant span is max 165 days, mean 62, median 65, giving a median
   of 57 observed daily X_t values, max 137.] These windows are still several times DS5's
   and make θ estimable, but not "with high precision" — treat θ̂ as a real but noisy
   per-participant estimate.

2. **The OU stationary distribution is exactly Gaussian.** For the OU SDE
   dX_t = θ(μ − X_t) dt + σ dW_t, the stationary distribution is exactly:
   P_inf(x) = N(μ, σ²/2θ)
   This means V(x) = (θ/2)(x − μ)² is a true confining quadratic potential. The
   Boltzmann bridge is exact, not approximate.

3. **β_OU = 2θ/σ² is rigorous.** Compared to DS5's approximate β_behav = 2/σ̂²,
   the OU-based β explicitly encodes the mean-reversion rate θ. ~~Two participants with
   identical σ̂ but different θ have different β_OU — a distinction invisible in DS5.~~
   [Corrected 2026-08-08 by audit: **this specific claim is empirically false for these
   estimates.** σ̂ is not independently observed — StoP back-solves it from the same AR(1)
   fit as θ̂ (`sigma2 = 2·θ̂·v̂/(1−φ̂²)`), so θ cancels out of β_OU entirely and
   β_OU = (1−φ̂²)/v̂ = 1/Var_stationary exactly (verified to 6e−14 on the shipped CSV).
   Measured corr(β_OU, θ̂_OU) = **0.0087** Pearson / **−0.0157** Spearman across the 641
   valid fits: β_OU carries essentially no θ information. Two participants cannot have
   "identical σ̂ but different θ" under this estimator except by coincidence of v̂ and φ̂.
   Treat β_OU as an inverse stationary-variance measure, not as a θ-aware refinement of
   DS5's β_behav.]

4. **Individual-level V(x) becomes defensible analytically.** [Corrected 2026-08-08 by
   audit.] V(x) = (θ/2)(x−μ)² follows directly from the fitted OU parameters, so no KDE of
   P̂_inf(x) is needed — and none was computed (notebook 51 cell 13 evaluates V(x) on demand
   from θ̂/μ̂). The original "hundreds of daily observations" justification is withdrawn: the
   median participant contributes 57 observed daily X_t values.

5. **True interior fixed points.** For the OU process, the fixed point of the deterministic
   ODE dX/dt = θ(μ−X) is X* = μ — an interior attractor, not a boundary. This resolves
   DS5 DyS's boundary-only limitation and allows genuine "attractor" language.

### Paper value of the DS4 implementation

The DS4 StM notebook enables a direct comparison that is valuable for the paper:

> "In DS5, the Statistical Mechanics framework is implemented as a behavioral analog —
> the Boltzmann bridge is approximate because the underlying SDE is a constant-drift model.
> In DS4, the longer observation windows enable an Ornstein-Uhlenbeck process, which has
> an exact confining potential and an exact Gaussian stationary distribution. This makes
> DS4 the first dataset in this project where Statistical Mechanics is fully defensible as
> a thermodynamic analogy rather than a behavioral approximation."

This comparison strengthens the paper in two ways:
1. It shows intellectual honesty: the paper openly acknowledges where the framework is
   approximate and where it becomes rigorous.
2. It demonstrates the framework's scalability: the same conceptual model works across
   datasets with different data richness, with transparency about what changes.

---

## 2. DS4 structural notes — critical for all DS4 notebooks

These are required reading before implementation. All cautions are from
`data_docs/modeling_cautions.md` §6 (DS4).

### 2.1 Three event classes — do NOT mix

DS4 has three structurally different event classes:
- `intervention_event` (36.5%): friction shown; has interventionType + duration
- `app_close_event` (47.1%): close events only; no intervention fields
- `no_intervention` (16.4%): open/dismiss but no friction logged

**For StM (and DS4 StoP):** Use only `intervention_event_class == 'intervention_event'`
for computing X_t. The state variable should be:
```
X_t = n_opened_intervention_events / n_outcome_bearing_intervention_events per day
```
This gives `rate_opened_intervention_events` per day as the daily behavioral state proxy.
Do NOT use `rate_opened_all` — it mixes friction and non-friction events.

### 2.2 No experimental condition

DS4 has no RCT. Participants selected the OneSec app themselves (self-selected usage).
There is no control group, no randomized condition assignment, and no reference group
for computing condition-level friction effects.

**Consequence for StM:** Condition-level comparisons (which were the primary DS5 StM
result) are not available. The DS4 StM analysis is therefore a **within-participant**
and **cross-participant** analysis of behavioral thermodynamics, not an experimental
comparison. Results describe the heterogeneity of behavioral temperature β_OU and
susceptibility χ_OU across naturalistic users.

### 2.3 Longitudinal time axis

Use `days_since_first_event` as the temporal axis, not `secondsSinceStudySetup`
(which is documented as inverted in the DS4 behavioral file).

### 2.4 No psychosocial Likert scales

DS4 survey features contain only demographics and qualitative flags (no validated
Likert scales). The psychosocial correlation section (analogous to DS5 StM Cell 20)
will use available demographic features but will have much less psychosocial content
than DS5.

### 2.5 `obs_window_days_ds4` removed

Column `obs_window_days_ds4` was removed in Stage 1 QC. Use `obs_window_days` only.

### 2.6 Minimum days threshold

For OU estimation, MIN_DAYS should be substantially higher than DS5's 7-day threshold.
Recommended: **MIN_DAYS = 30** for OU parameter estimation (allows at least 30 daily
increments for stable θ estimation). This is a FLAG decision for the implementation.

---

## 3. FLAG decisions for DS4 StM Step 1

| Flag | Default decision | Alternative (deferred) | Why deferred |
|---|---|---|---|
| FLAG 1 | OU SDE: dX_t = θ(μ−X_t)dt + σ dW_t; β_OU = 2θ/σ²; individual V(x) defensible | Nonlinear potential with multiple wells | Nonlinear V(x) requires empirical estimation beyond OU; would need spline fitting or deep history |
| FLAG 2 | **[Updated 2026-08-06]** Reuse StoP's own estimates directly — closed-form conditional MLE via AR(1) OLS on consecutive-day pairs, already computed in `participant_parameters.csv` | Re-fitting independently here | Would risk a second, silently-inconsistent estimate of the same μ̂/θ̂/σ̂; StoP already did this correctly (real N=641 valid fits) — see §0 |
| FLAG 3 | No condition comparison (DS4 is observational) | Quartile-based heterogeneity analysis (high/low β_OU groups) | Quartile grouping is a post-hoc partition; implement as visualization only, not as primary analysis |
| FLAG 4 | Phase transition: T_c estimated from β_OU distribution (simulated sweep) | Empirical phase diagram from within-participant β trajectory over time | Time-varying β requires rolling estimation; feasible but adds complexity; defer to DS4 Step 2 |

---

## 4. Core equations — with paper status

### Already in paper (inherited from DS5 StM)

| Eq. | Formula | Paper location | Role |
|---|---|---|---|
| General Boltzmann | P(s) ∝ exp(−βH(s)) | §4.1.1 | Core |
| Partition function | Z = Σ exp(−βE_i) | §4.1.1 | Core |
| Free energy | F = −(1/β) ln Z | §4.1.1 | Core |
| Susceptibility | χ = ∂⟨M⟩/∂h | §4.1.1 | Core |

### Required for DS4 — NOT in paper (new additions beyond DS5 gaps)

| Equation | Formula | Status | Action |
|---|---|---|---|
| OU SDE | dX_t = θ(μ − X_t) dt + σ dW_t | NOT in paper | **Must add** to §4.1.3 or §4.2.3 as the Step 2 StoP extension |
| OU stationary distribution | P_inf(x) = N(μ, σ²/2θ) | NOT in paper | **Must add** §4.2.1 — this is the exact Boltzmann distribution for OU |
| OU confining potential | V(x) = (θ/2)(x − μ)² | NOT in paper | **Must add** — the exact quadratic potential that makes Boltzmann rigorous |
| Rigorous β_OU | β_OU = 2θ/σ² | NOT in paper | **Must add** §4.2.1 — contrasted explicitly with DS5's approximate β_behav = 2/σ̂² |
| OU mean-reversion timescale | τ = 1/θ | NOT in paper | **Add as interpretive quantity** — τ is the behavioral relaxation time; highly intuitive |
| OU fixed point | X* = μ (stable interior attractor when θ > 0) | NOT in paper | **Add** to DyS or StM DS4 section — first true interior attractor in the project |
| OU quadratic V(x) individual level | V_i(x) = (θ̂_i/2)(x − μ̂_i)² | NOT in paper | **Add** §4.2.1 — individual-level energy landscape, now defensible |
| Individual susceptibility (OU) | χ_i = β_OU_i · p̂_use_i · (1 − p̂_use_i) | Already in DS5 (same formula) | No new addition needed; formula already proposed for paper |

**Note:** DS4-specific equations (OU SDE, P_inf, V(x) = quadratic, β_OU, τ) should be added
to `structures/paper_equation_additions.md` once this blueprint is approved and implemented.

---

## 5. Theory-to-data mapping for DS4

| Theoretical quantity | DS4 variable / derived quantity | Mapping type | Confidence vs DS5 |
|---|---|---|---|
| State variable X_t | n_opened_intervention_events / n_outcome_bearing_intervention_events per day | Proxy (same logic as DS5, cleaner denominator) | Medium — same proxy warning applies |
| OU drift μ | μ̂_OU = long-run mean of X_t per participant | Direct reuse | High — more stable than DS5 (longer windows) |
| Mean-reversion rate θ | θ̂_OU from MLE of OU likelihood | New parameter — requires estimation | Medium-High — estimable with 30+ observations |
| Diffusion σ | σ̂_OU from MLE residuals | Estimated from OU fit | High |
| Relaxation time τ | τ̂ = 1/θ̂_OU (days) | Direct transform | High — τ is the most interpretable OU quantity |
| Confining potential V(x) | V̂_i(x) = (θ̂_i/2)(x − μ̂_i)² | Exact formula (OU) | High (individual level) — first reliable individual V(x) in the project |
| Fixed point X* | X* = μ̂_OU (interior attractor for θ > 0) | Direct (OU) | High — resolves DS5 DyS boundary-only limitation |
| Effective temperature β_OU | β_OU = 2θ̂/σ̂² | Rigorous (OU) | High — exact, not approximate |
| Susceptibility χ | χ_i = β_OU_i · p̂_use_i · (1−p̂_use_i) | Derived | Medium-High |
| Free energy F | F_i = E_use_i − (1/β_OU_i) · H_emp_i | Derived | Medium |
| External field h | NOT AVAILABLE — no condition variable in DS4 | — | None |

---

## 6. Notebook structure — `notebooks/51_ds4_statistical_mechanics.ipynb`

This structure follows the same template as `41_ds5_statistical_mechanics.ipynb`.
The generator script will follow the same pattern as `make_41_stm.py`.

| Cell | Type | Content |
|---|---|---|
| 1 | Markdown | **Scope statement**: Goal = rigorous OU-based StM; contrast with DS5 approximation; what this notebook resolves (FLAG A, FLAG B) |
| 2 | Markdown | **FLAG decisions table** (FLAG 1–4) |
| 3 | Markdown | **Proxy warning** + DS4-specific structural caveat (intervention_event class only; no condition) |
| 4 | Markdown + LaTeX | **Theory section 1**: OU SDE; stationary distribution N(μ, σ²/2θ); V(x) = quadratic; β_OU = 2θ/σ² — all exact for OU |
| 5 | Markdown + LaTeX | **Theory section 2**: StM equations (reused from DS5 StM theory cells) |
| 6 | Markdown + LaTeX | **DS5 vs DS4 comparison**: what changes when we go from constant-drift to OU; FLAG A resolved |
| 7 | Markdown | **Theory-to-data mapping table** |
| 8 | Markdown | **Equation gaps table** (DS4-specific) |
| 9 | Code | **Setup**: imports, paths, constants (THRESHOLD_USE=0.5, etc.) — no MIN_DAYS here, StoP's own `fit_valid` population is inherited directly |
| 10 | Code | **[Updated 2026-08-06] Load StoP's `participant_parameters.csv`, InT's `participant_entropy_metrics.csv`, and DyS's `participant_dynamics_parameters.csv` directly** — μ̂_OU, θ̂_OU, σ̂_OU, τ̂, `H_SDE`, `regime_label` all come from these files, not recomputed (see §0) |
| 11 | *(removed — was "OU parameter estimation per participant"; superseded by cell 10, see §0)* |
| 12 | Code | **Level 1 — β_OU, T_OU per participant**: β_OU = 2θ̂/σ̂²; T_OU = σ̂²/(2θ̂); distribution summaries |
| 13 | Code | **Level 1 — two-state model**: p_use, E_use, Z_2, χ_OU, F_OU |
| 14 | Code | **Level 2 — individual V(x)**: V̂_i(x) = (θ̂_i/2)(x − μ̂_i)² for each participant; no KDE needed — exact formula |
| 15 | Code | **Level 2 — V(x) statistics**: V_min = X* = μ̂_OU per participant; depth of V (β_OU); spread vs DS5 |
| 16 | Code | **[Updated 2026-08-06] H_StM = InT's `H_SDE`, joined directly (identical formula for DS4 — do not recompute, see §0)**; compare with H_emp |
| 17 | Code | **DS4 vs DS5 StM comparison**: compare β_OU (DS4) vs β_behav (DS5) — note they are not directly comparable (different SDE) |
| 18 | Code | **Relaxation time distribution**: τ̂ = 1/θ̂; what does the median τ mean behaviorally? |
| 19 | Code | **Cross-participant heterogeneity**: β_OU distribution; identify high-T (low-β) and low-T (high-β) participants |
| 20 | Code | **Psychosocial correlates** (DS4 survey: demographics, dominant_intervention_type, activity_persistence) |
| 21 | Code | **Export outputs** (all CSVs and model_run_summary.md) |
| 22 | Code | **Figure 1**: β_OU and T_OU distribution across all DS4 participants |
| 23 | Code | **Figure 2**: τ̂ (relaxation time) distribution; behavioral interpretation |
| 24 | Code | **Figure 3**: Individual V(x) curves — sample of participants; compare low-β vs high-β shapes |
| 25 | Code | **Figure 4**: β_OU vs x_mean scatter; colored by τ̂; size coded by χ_OU |
| 26 | Code | **model_run_summary.md writer** |
| 27 | Markdown | **Interpretation and limits** — DS4-specific weakness flags; comparison with DS5 |
| 28 | Markdown | **Forward connections** |

---

## 7. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_statistical_mechanics/`

Note: DS4 outputs go in a DS4-specific subdirectory (not `statistical_mechanics/` which
is already used by DS5).

| File | Description | Rows |
|---|---|---|
| `participant_ds4_stm_parameters.csv` | Per-participant: μ̂_OU, θ̂_OU, σ̂_OU, τ̂, β_OU, T_OU, p_use, E_use, Z_2state, χ_OU, F_OU, H_StM (=InT's H_SDE), regime_label (from DyS) | 1,039 (641 with real StM values — **[Updated 2026-08-06]** real N, was "~600-800 estimate") |
| `ds4_stm_summary.csv` | Overall sample-level statistics | 1 row + percentile profile |
| `participant_vx_parameters.csv` | **[Not produced — folded into `participant_ds4_stm_parameters.csv`.]** Per-participant V(x) parameters: V_min_location (= μ̂_OU), V_curvature (= θ̂_OU/2 — note this is the quadratic coefficient, NOT the curvature V''(x)=θ̂_OU), V_depth (= β_OU — an inverse temperature, not a well depth; a quadratic well has no finite depth) | same as above |
| `ds4_ds5_stm_comparison.csv` | Side-by-side comparison of StM quantities for DS4 (OU) vs DS5 (constant-drift): β, T, χ — with clear caveat that they are not directly comparable | summary-level |
| `psychosocial_ds4_stm_correlations.csv` | Correlations with available DS4 demographic/behavioral features | — |
| `model_run_summary.md` | Full run record | — |
| `figures/fig1_ds4_beta_distribution.png` | β_OU histogram | — |
| `figures/fig2_ds4_relaxation_time.png` | τ̂ = 1/θ distribution | — |
| `figures/fig3_ds4_vx_sample.png` | Individual V(x) curves — sample | — |
| `figures/fig4_ds4_beta_xmean_scatter.png` | β_OU vs x_mean colored by τ | — |

---

## 8. DS4 weakness flags

These must appear in the DS4 StM notebook interpretation cell.

### ⚠ FLAG A (resolved): OU Boltzmann bridge is rigorous

Unlike DS5, the OU bridge is exact. **This flag is resolved in DS4.** State explicitly:
> "This notebook resolves DS5's FLAG A. The OU process produces an exact Gaussian stationary
> distribution and an exact confining quadratic potential. β_OU = 2θ/σ² is rigorous."

### ⚠ FLAG I: No experimental condition

DS4 is observational. There is no control group, no randomized condition, and no reference
friction "field" h. All StM analysis is within-participant or cross-participant heterogeneity.
Condition-level StM results (the primary DS5 finding) are not available.

### ⚠ FLAG II: Self-selected users — attrition and behavioral confounds

DS4 users chose to install OneSec. Long-window users are those who kept using the app,
which may be systematically different from short-window users (attrition = non-random).
β_OU for long-stay users may be different from β_OU for users who quit — and the
former are overrepresented in the MIN_DAYS=30 eligible sample.

### ⚠ FLAG III: Individual V(x) is exact but not causally identified

The OU quadratic V(x) = (θ̂/2)(x − μ̂)² is mathematically exact for the OU model.
However, the OU model itself is a model assumption — participants may not actually follow
OU dynamics. The individual V(x) should be labeled "OU model-implied energy landscape,"
not "true behavioral energy landscape."

### ⚠ FLAG IV: θ estimation requires long windows

**[Updated 2026-08-06 — real number, not estimate]** 641/1,039 DS4 participants (61.7%)
have a valid StoP fit; 641/785 (81.7%) of those meeting the MIN_DAYS=30 threshold.
Participants without a valid fit get NaN θ̂ and therefore NaN β_OU/χ_OU/H_StM — inherited
directly from StoP's `fit_valid` flag, not re-derived. Report this exclusion explicitly.

### ⚠ FLAG VI (new, 2026-08-06): β_OU/χ_OU/H_StM are daily-timescale specific

StoP's own weekly-aggregation sensitivity check found a meaningfully different
relaxation time at weekly resolution (median τ̂≈0.91 weeks vs 0.63 days daily, only
r=0.316 correlation between daily and weekly θ̂ per participant). Every quantity in this
notebook is built from StoP's **daily**-scale μ̂/θ̂/σ̂. State this explicitly — do not
present β_OU as a timescale-independent "behavioral temperature."

### ⚠ FLAG V: Behavioral proxy limitation persists

X_t = n_opened_intervention_events / n_outcome_bearing_intervention_events inherits all
DS5 proxy limitations. It is a behavioral rate, not a latent psychological state.
The OU model's elegance does not change the underlying measurement limitation.

---

## 9. OU parameter estimation — technical notes

### State variable (DS4)

```python
# Load behavioral clean file
df = pd.read_csv('outputs/cleaned/ds4_behavioral_clean.csv')

# Filter to intervention events only
df = df[df['intervention_event_class'] == 'intervention_event'].copy()

# Filter to valid outcomes
df = df[df['event_outcome_simple'].isin(['opened', 'dismissed'])].copy()
df['opened_flag'] = (df['event_outcome_simple'] == 'opened').astype(int)

# Daily aggregation — same as DS5 StoP
df['event_date'] = pd.to_datetime(df['timestamp_utc']).dt.date
daily = df.groupby(['participant_id_canonical', 'event_date']).agg(
    n_opened=('opened_flag', 'sum'),
    n_events=('opened_flag', 'count')
).reset_index()
daily['X_t'] = daily['n_opened'] / daily['n_events']
```

### OU MLE estimation

The exact discrete-time OU likelihood (Euler discretization with Δt=1 day):

```
X_{n+1} | X_n ~ N(μ + (X_n − μ)·e^{-θ}, σ²(1 − e^{-2θ}) / (2θ))
```

MLE parameters: maximize log-likelihood over (μ, θ, σ). Scipy optimize or statsmodels
can handle this. Key properties:
- μ̂ = mean(X_t) is the unconditional mean (identical to method of moments)
- θ̂ encodes the mean-reversion speed — larger θ = faster return to μ
- σ̂ is the noise level (NOT identical to StoP's σ̂, which is std(ΔX))

Alternative: use the autocorrelation estimator for θ:
```
θ̂ ≈ -log(r₁) / Δt   where r₁ = autocorrelation of X_t at lag 1
```
This is biased but fast. Prefer MLE if feasible.

### Minimum days constraint

With Δt=1 day and MIN_DAYS=30, the autocorrelation-based estimator is reliable.
MLE convergence may require more; use MIN_DAYS=30 as a starting threshold and report
the actual distribution of n_days for eligible participants.

---

## 10. Theoretical coherence

The DS4 StM implementation is theoretically coherent in a way DS5 could not be:

1. **Exact stationary distribution.** The OU process has P_inf = N(μ, σ²/2θ) — there is no
   ambiguity about whether the empirical distribution approximates or equals the stationary
   distribution in the long run (assuming stationarity is reached, which is plausible for
   participants with θ̂ > 0 and observation windows >> τ̂ = 1/θ̂).

2. **Exact energy landscape.** V(x) = (θ/2)(x−μ)² is a true confining potential with a
   unique minimum at X* = μ. This is the first instance in the project where "energy
   landscape minimum" = "behavioral attractor" in a mathematically precise sense.

3. **β_OU encodes a behavioral timescale.** β_OU = 2θ/σ² combines mean-reversion speed
   (θ) and noise level (σ²). Two participants with the same β_OU could have different θ
   and σ but the same "thermal order." The ratio θ/σ² is a true model parameter, not a
   derived proxy.

4. **τ = 1/θ is interpretable.** The relaxation time τ = 1/θ̂ is the number of days it
   takes for a behavioral displacement to decay by a factor of 1/e. **[Updated
   2026-08-06 — the "if τ̂=14 days" wording below was always a hypothetical illustration,
   written before any DS4 OU fit existed; the real result is very different in
   magnitude.]** StoP's actual median τ̂≈0.63 days at daily aggregation — a perturbation
   fades within about a day at that timescale, not weeks. StoP's own weekly-aggregation
   check found a slower median (≈0.91 weeks) with only weak correlation to the daily
   value per participant (r=0.316) — a genuine, unresolved divergence across timescales,
   not a single clean number. This is still a directly interpretable behavioral quantity
   with no DS5 equivalent, but "how fast" depends on which timescale you ask at.

5. **No FLAG A caveat needed.** The paper section on DS4 StM can state without qualification
   that the Boltzmann bridge is rigorous for this dataset.

---

## 11. Implementation feasibility

| Requirement | Assessment | Note |
|---|---|---|
| OU parameters | **[Updated] Already computed by StoP** — load directly, do not re-fit | `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv` |
| Daily X_t computation from intervention_event class | Not needed here — StoP already did this | See §0 |
| Individual V(x) — no KDE needed | Straightforward — exact formula | V(x) = (θ̂/2)(x−μ̂)² |
| H_StM per participant | **[Updated] Already computed by InT as `H_SDE`** — identical formula, join directly | See §0 point 2 |
| Comparison table DS4 vs DS5 | Feasible — summary-level | Note that β_OU ≠ β_behav (different models) |
| Generator script (make_51_ds4_stm.py) | Feasible — same pattern as make_41_stm.py | Reuse cell structure; adapt DS4-specific pipeline |
| Expected eligible N | **[Updated] 641 (real, not estimate)** | StoP's real `fit_valid` count |

**Implementation dependencies — [Updated 2026-08-06]:**

DS4 StoP (53), DS4 InT (52), and DS4 DyS (55) are all **complete**. DS4 StM (51) now
consumes their real output directly rather than re-estimating anything internally —
matching this project's binding rule against redundant re-derivation. The order actually
implemented was StoP→InT→DyS→StM→NeT (the project-wide established order), not the
"StM before DyS" sequencing this section originally sketched.

**Actual implementation order for DS4 (as executed):**
1. `53_ds4_stochastic_processes.ipynb` — OU-StoP (μ̂_OU, θ̂_OU, σ̂_OU, τ̂) — **done**
2. `52_ds4_information_theory.ipynb` — InT (H_emp, H_out, exact H_SDE) — **done**
3. `55_ds4_dynamical_systems.ipynb` — DyS (true interior attractor, regime split) — **done**
4. `51_ds4_statistical_mechanics.ipynb` — StM (this notebook) — next

---

## 12. Usefulness for the paper

The DS4 StM implementation contributes the following to the paper:

### Validation of DS5 approximation

DS4 allows the paper to say: "The DS5 StM analysis produced approximate results because of
the constant-drift SDE assumption. The DS4 analysis with OU confirms that the qualitative
ordering (higher noise = higher behavioral temperature) is robust, while also providing exact
quantitative values for a naturalistic long-run sample." This adds credibility to the DS5
findings retroactively.

### New substantive result: relaxation time τ

No other dataset in the project has a measurable behavioral relaxation timescale.
τ̂ = 1/θ̂ (in days) is a new quantity that characterizes how quickly individual behavioral
patterns return to their personal baseline after disruption. This has direct implications
for friction intervention design (how long must an intervention last to produce a lasting
shift?). This finding has no equivalent in DS5.

### Individual-level energy landscapes

The first reliable individual V(x) estimates in the project. These provide per-participant
"potential well depth" as a phenotyping dimension. Participants with steep wells (high θ̂)
return quickly to baseline — they are harder to shift. Participants with shallow wells (low
θ̂) are more susceptible but also more volatile.

### Closing the DS5 approximation argument

The paper can present the two implementations as a contrast: "In a short-window experimental
dataset (DS5), the StM framework requires approximations that limit its rigor. In a long-window
naturalistic dataset (DS4), the same framework becomes exact. This demonstrates that the
theoretical framework is sound, and its limitations are data-structural, not conceptual."

---

## 13. Unification potential — DS4 StM connections

**[Updated 2026-08-06 — direction corrected.** The original table below had StM
producing inputs for DyS and InT to consume. That's backwards relative to the order
actually implemented (StoP→InT→DyS→StM) — InT and DyS already ran using StoP's output
directly, without waiting for StM. The corrected direction:]

| Connection | Mechanism | Status |
|---|---|---|
| DS4 DyS → DS4 StM | DyS's `X*=mu_hat_OU` interior-attractor characterization and `regime_label` are consumed here, giving StM's V(x) minimum an already-established behavioral-attractor interpretation | DyS complete, consumed by this notebook |
| DS4 InT → DS4 StM | InT's `H_SDE` (already the exact same formula as this blueprint's own `H_StM`) is joined directly, not recomputed | InT complete, consumed by this notebook |
| DS4 StM → Phenotyping | β_OU, τ̂, χ_OU as three phenotype dimensions — now with interpretable timescale | Pending — DS4 Step 2, after all 5 Step 1 families are done |
| DS4 StM → Paper §4.2.1 | Add OU equations (listed in §4 of this blueprint) | Before submission |
| DS4 StM → DS5 StM | Cross-dataset comparison: which participants in DS4 have β_OU similar to DS5 control vs friction conditions? | Synthesis section, future |
| DS4 StM → Paper §4.3 | OU-based exact StM completes the "rigor ladder" from DS5 (approximate) to DS4 (exact) | §4.3 unification, future |

---

## 14. How this blueprint connects to future DS5 model implementations

**⚠ [Marked obsolete 2026-08-06] — kept for historical record only.** This section was
written 2026-04-17 as a "what's next on DS5" note for the session that would return to
DS5 after this blueprint. DS5 NeT (44) finished the same day this blueprint was written,
and the rest of DS5 Step 1 (all 5 active families) has been complete for months — none of
the guidance below is still actionable. Not relevant to implementing DS4 StM.

### NeT (notebook 44) — continuing DS5 after this blueprint

The next DS5 Step 1 model to implement is NeT (Network Models, notebook 44). When you
return to DS5 NeT after DS4 StM, the standard structure applies:

**Blueprint file to create:** `outputs/reports/stage4/ds5_net_blueprint.md`  
**Notebook:** `notebooks/44_ds5_network_models.ipynb`  
**Generator:** `notebooks/make_44_net.py`  
**Output directory:** `outputs/model_outputs/network_models/`

**What NeT needs that StM did not:**
- Sequence engineering: `app_next` and `app_prev` columns — require consecutive-event pairing
  within participant (sorted by timestamp), filtered to intervention events
- Transition probability matrix T_{ij} from (app_previous → app_current) pairs
- App mapping to integer indices (encode top-K apps; remainder = 'other')
- Stationary distribution π (left eigenvector of T for λ=1)
- Network entropy H_net = − Σ_{ij} T_{ij} log₂ T_{ij}

**NeT is currently a placeholder (notebook 44 exists but is empty/blocked)** because the
sequence engineering has not been implemented. The sequence engineering can be done in the
NeT notebook's setup cells or in a standalone preprocessing step.

**Before starting NeT, revisit:**
1. `data_docs/modeling_cautions.md` — no DS5-specific NeT cautions yet; check if any arise
2. `notebooks/00_model_notebook_template.ipynb` — start from this template
3. `outputs/reports/stage4/stage4_implementation_plan.md` — update when NeT is confirmed

**For GaT (46), ABM (47), SyD (48):** These remain deferred. ABM explicitly requires the
completed StoP/DyS/InT/StM characterization as agent parameter inputs — the DS5 cluster
now provides exactly this. ABM could proceed after the DS4 StM notebook if desired.
SyD remains deferred to DS6.

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.

When the user approves:
1. Create `notebooks/make_51_ds4_stm.py` (generator script, same pattern as `make_41_stm.py`)
2. Run generator to create `notebooks/51_ds4_statistical_mechanics.ipynb`
3. Execute notebook; verify all outputs
4. Update `stage4_implementation_plan.md` with DS4 StM status
5. Update `memory/project_stage.md` with DS4 StM section
6. Add DS4-specific equations to `structures/paper_equation_additions.md`
