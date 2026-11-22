# DS6 — Stage 4, Step 1 Implementation Plan

**Written:** 2026-08-06
**Dataset:** DS6 — Danish adolescents (quasi-experimental, N=243 behavioral)
**Purpose:** Record the model family order, numbering/output-path convention, and the
core grounding decision (no shared outcome variable) before any DS6 model code is written.
This mirrors the DS5 (`stage4_implementation_plan.md`) and Structured
(`structured_cas_modeling_plan.md`) precedents: plan first, one blueprint per family before
its notebook, FLAG decisions recorded up front.

---

## 0. Read before this: the DS6 session-structure bug

Before this plan was written, a pre-modeling check found that DS6's `group_id`,
`first_in_group`, `last_close_in_group`, and `close_ts` columns do **not** provide real
session-boundary data (verified on the full raw file — see
`data_docs/modeling_cautions.md` §6 and `outputs/reports/stage0/ds6_audit_report.md` §8a).
8 Stage 1 features built on this were removed 2026-08-05. Any DS6 model notebook must be
built on `outputs/features/ds6/ds6_behavior_features.csv` **as it exists after that fix**
(243 × 67, not the earlier 77-column version) and must not reintroduce group_id-based
session counts.

## 1. Numbering and output-path convention

**Notebook decade: 70s** (not 50s/51-58). `50_ds6_model_prototypes.ipynb` already exists as
an empty scratch placeholder and is left alone. Decade 51–55 is actively claimed by a
concurrent DS4 StoP blueprint (`outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`,
written 2026-08-06, not yet implemented) found in the working tree while this plan was being
written — using it for DS6 would collide. Decade 60–68 is Structured's. 70s is unclaimed.

Suffix convention matches DS5 (41–48) and Structured (61–68) exactly:

| Suffix | Family | DS6 notebook |
|---|---|---|
| 1 | StM | `71_ds6_statistical_mechanics.ipynb` |
| 2 | DyS | `72_ds6_dynamical_systems.ipynb` |
| 3 | StoP | `73_ds6_stochastic_processes.ipynb` |
| 4 | NeT | `74_ds6_network_models.ipynb` |
| 5 | InT | `75_ds6_information_theory.ipynb` |
| 6 | GaT | `76_ds6_game_theory.ipynb` |
| 7 | ABM | `77_ds6_agent_based.ipynb` |
| 8 | SyD | `78_ds6_system_dynamics.ipynb` |

**Output root:** `outputs/model_outputs/ds6/<family_name>/` — dataset-scoped nesting,
matching Structured's convention (`outputs/model_outputs/structured/<family>/`), not DS5's
un-prefixed paths (`outputs/model_outputs/stochastic_processes/` is already DS5's own StoP
output and must not be reused) and not DS4's flat-prefixed style
(`outputs/model_outputs/ds4_stochastic_processes/`, seen in the concurrent DS4 blueprint).
Two naming conventions now coexist across datasets in this project (DS4 flat-prefixed vs.
DS6/Structured nested) — not reconciled here, just noted so it isn't mistaken for an error.

## 2. The core grounding decision: no shared outcome variable

DS1/DS4/DS5's shared "episode" (paper §1.1) ends in one of {opened, dismissed, closed}. DS6's
behavioral log has **only `openedApp`** — confirmed structural, not missing data. This means
any DS5-style state variable built on outcome proportions (`X_t = n_opened/n_events`) is
undefined for DS6 (the denominator and numerator would be identical — X_t ≡ 1 always). Every
DS6 family must therefore use its own, differently-grounded state variable — this is not
optional stylistic variation, it is forced by the data.

The paper's own §1.3 text names the fallback explicitly and by name: *"Stochastic Processes
are also feasible because event logs can be aggregated into user-day or user-week time
series, such as **daily attempt count**, daily dismissal rate, daily opening rate, or daily
friction-success rate."* DS6 uses the first of these — attempt (event) count — because the
other three require the missing outcome variable. This is the anchor decision for DS6 StoP
(see blueprint) and is inherited by every downstream family that needs a state variable.

## 3. What DS6 actually has that DS1/DS4/DS5 don't

- **Explicit `study_period` (baseline/intervention) in every row.** The only dataset with a
  true pre/post design in the behavioral log itself — enables within-participant
  before/after comparison, not just between-condition comparison.
- **Pre-engineered depth-3 `app_next`/`app_prev` sequences.** Richest sequence data in the
  project (confirmed still true after the session-structure correction — this claim never
  depended on `group_id`). **⚠ Superseded by §0a below:** `app_next` was subsequently found
  to be a mechanical artifact (99.3% same-app echo, not a real "next app opened" field) —
  only `app_prev` is genuine. NeT (74) derives transitions independently rather than trusting
  either column. Left here uncorrected-in-place (rather than rewritten) so the chronology of
  what was believed before NeT started is preserved; §0a is the authoritative correction.
- **2–3 survey waves** (`survey_data_clean.csv` = 2 waves; `survey_data_full.csv` = 3).
  DS5's SyD (system dynamics) was explicitly deferred *to DS6* for exactly this reason
  (`stage4_implementation_plan.md` line 279: *"SyD (48): deferred to DS6 — requires repeated
  survey waves"*). This is now actionable.
- **No genuine session data** (corrected 2026-08-05). Do not reach for `group_id` to try to
  recover this DS5/DS1 lack — it doesn't exist here either.

## 4. Recommended family order for DS6

Not a mechanical repeat of DS5's StoP→InT→DyS→StM→NeT chain — re-derived from what DS6
actually has:

1. **StoP (73) — first.** Establishes the count-based state variable (§2) that InT and DyS
   can build on, exactly as it did for DS5. Also the natural home for DS6's single biggest
   structural asset (§3): the baseline-vs-intervention comparison. Blueprint:
   `outputs/reports/stage4/step1_modeling/ds6_stop_blueprint.md` (this session).
2. **NeT (74) — second.** Does not depend on StoP. Uses DS6's richest asset (pre-engineered
   sequences) directly. Doing it early, independent of the StoP chain, mirrors why
   Structured did NeT first — the dataset's standout feature shouldn't wait on an
   unrelated dependency chain.
3. **InT (75) — third.** Entropy of StoP's stationary/count distribution; bridges naturally
   to NeT's transition entropy once both exist (same InT–NeT bridge pattern as DS5,
   re-derived for DS6's count-based state variable, not assumed to transfer unchanged).
4. **DyS (72) — fourth.** σ→0 regime split from StoP, same logic as DS5 notebook 42 but
   re-derived for the count process (no [0,1] bound to exploit here).
5. **SyD (78) — fifth.** Newly feasible (§3) — the reason DS6 exists in this position in the
   project's own sequencing logic. Needs its own blueprint deriving stocks/flows from DS6's
   actual repeated-wave psychosocial indices; not a DS5 port (DS5 never built SyD at all).
6. **StM (71) — sixth.** Same caution as DS5 (analogy-based constructs, not literal
   thermodynamics); built on StoP+DyS once both exist.
7. **GaT (76), ABM (77) — deferred**, same reasoning as DS5: GaT awaits behavioral profiles
   from Step 2 phenotyping; ABM needs prior model characterization.

This order will be revisited if implementation reveals a dependency problem — recorded here
as intent, not a hard commitment, matching how DS5's own order was allowed to evolve.

## 5. Status

| Notebook | Family | Status |
|---|---|---|
| 73_ds6_stochastic_processes.ipynb | StoP | **COMPLETE (2026-08-06).** 230/243 (94.7%) both-period eligible. Headline: mean daily attempt volume drops 45.1→29.1 events/day baseline→intervention (level effect, cross-validates Stage 1's `event_rate_ratio` feature); h_period (drift/trend shift) not significant. See `outputs/model_outputs/ds6/stochastic_processes/model_run_summary.md`. |
| 74_ds6_network_models.ipynb | NeT | **COMPLETE (2026-08-06).** Found and fixed a second real bug before implementing (`app_next` mechanically echoes the current app 99.3% of the time — see §0 addendum below). Built on self-derived transitions (shift(-1) on time-sorted rows), not `app_next`/`app_prev`. 239/243 (98.4%) baseline / 235/243 (96.7%) intervention eligible. Headline: corr(HHI_net change, daily-volume change) = -0.213, p=0.0012 — narrowing to fewer apps under reduced usage. See `outputs/model_outputs/ds6/network_models/model_run_summary.md`. |
| 75_ds6_information_theory.ipynb | InT | **COMPLETE (2026-08-06).** Depends on StoP (73) + NeT (74), both done. Fixed a real two-attempt NeT-InT bridge bug (see §0b below) before results were trustworthy. Headline 1: r(H_SDE,H_emp)=0.58/0.72 both periods — supports StoP's Gaussian-increment assumption. Headline 2: pooled MI(study_period;app_name)=0.0003 bits, genuine null, does not contradict NeT's per-participant finding. See `outputs/model_outputs/ds6/information_theory/model_run_summary.md`. |
| 72_ds6_dynamical_systems.ipynb | DyS | **COMPLETE (2026-08-06).** Depends on StoP (73) + InT (75), both done. sigma→0 limit of StoP's SDE; DS6-specific 3-way asymmetric regime structure (declining/growing/resting, floor-only bound, no ceiling — unlike DS5's double-bounded [0,1] case). Headline: regime-transition analysis independently confirms StoP's "level moved, trend didn't" finding via a completely different method. DyS-InT bridge prediction confirmed. See `outputs/model_outputs/ds6/dynamical_systems/model_run_summary.md`. |
| 78_ds6_system_dynamics.ipynb | SyD | **COMPLETE (2026-08-06).** Depends on StoP (73) + DyS (72), both done. Closes the repeated-wave rationale that specifically justified deferring SyD from DS5 to DS6. Two stocks (app-use pressure = addiction_index, self-regulation = self_control_index, both paper-named). Two feedback-loop hypotheses tested with a regression-to-the-mean control (raw + partial correlation) — **both genuine null results**, reported honestly. See `outputs/model_outputs/ds6/system_dynamics/model_run_summary.md`. |
| 71_ds6_statistical_mechanics.ipynb | StM | **COMPLETE (2026-08-06).** Depends on InT (75) for a sanity check only, not StoP. No β/T/Z/F apparatus (DS6's unbounded StoP variable makes DS5's bridge even less applicable than it was for Structured, which already declined it). Microstate = joint (app, hour_bucket); two bugs found and fixed (sanity-gate granularity mismatch, then an assertion NaN-handling bug in the fix itself). **Headline: control shows significantly lower susceptibility than either friction condition** (p=0.0011, p=0.0075) — DS6's first clearly condition-differentiated result in Step 1. **Closes all 7 active DS6 Step 1 model families.** See `outputs/model_outputs/ds6/statistical_mechanics/model_run_summary.md`. |
| 76, 77 | GaT, ABM | Deferred pending Step 2 phenotyping (matching DS5/Structured precedent) |

**DS6 Step 1 is now COMPLETE for all 7 active model families** (StoP, NeT, InT, DyS, SyD,
StM). This closes the DS6 Step 1 arc started 2026-08-06.

**DS6 Step 2 (phenotyping) also COMPLETE (2026-08-06), same day.** Full details:
`outputs/reports/stage4/step2_phenotyping/ds6_phenotyping_blueprint.md`. Notebook:
`notebooks/140_ds6_phenotype_exploration.ipynb`. Outputs:
`outputs/model_outputs/ds6/phenotyping/`. One clustering pass (not DS5's six-path
exploration), 5 behavioral features (SyD deliberately used as the psychosocial overlay
instead of a 6th clustering feature). k=2, N=227, bootstrap Jaccard=0.714 (MARGINAL).
Headline 1: the k=2 split is almost exactly DyS's `regime_changed` binary feature.
Headline 2: `self_control_index_change` differs significantly by cluster
(p_bonferroni=0.018) — the first significant psychosocial result in the whole DS6 program.

**DS6 sanity-check audit — COMPLETE (2026-08-06), user-requested.** Recomputed 30+ headline
numbers directly from saved CSVs; found and fixed 2 column-export labeling bugs (NaN stored
as False instead of NaN in two bridge-check files — no result changed). Full record in
CLAUDE.md's "DS6 sanity-check audit" section.

**DS6 Step 2 Path A′ (behavior-only, DyS removed) — COMPLETE (2026-08-06), user-triggered.**
User inspected the main pass's radar chart and asked why Profile A showed nothing on the
regime-change axis — correctly spotted that one feature (DyS's `regime_changed`) was
dominating the k=2 split (verified: perfect separation). Blueprint:
`outputs/reports/stage4/step2_phenotyping/ds6_path_a_behavior_only_blueprint.md`. Notebook:
`notebooks/141_ds6_behavior_only_phenotype.ipynb`. Outputs:
`outputs/model_outputs/ds6/phenotyping_path_a/`. Dropped DyS entirely (not substituted),
matching DS5/Structured's own Path A ethos. **Second real bug caught**: the naive k-fallback
would have silently forced k=2 despite NO k meeting the min-cell floor — same failure mode
Structured's Path D already caught once; investigated instead of accepting, found the "k=2"
split was really 218 typical participants vs. 9 genuine multivariate outliers (extreme
susceptibility). Reported honestly as an outlier characterization, not a validated
phenotype. **ARI(Path A′ vs main pass) = 0.0235 (LOW/ORTHOGONAL)** — confirms the main
pass's split really was substantially DyS's own signal; the 4 remaining continuous features
don't offer a competing balanced structure. Coherence check: all 9 outliers are in friction
conditions (0 in control), matching StM's independently-found condition effect.

Not yet discussed: DS6 Step 3 (personalization, matching DS5's precedent) or a return to
DS4/DS1 per the project's original dataset order.

## 0b. Addendum (2026-08-06): NeT-InT bridge bug, two attempts, both caught by the mandatory gate

While computing I_consec = H_app − H_trans for the NeT-InT bridge, the mandatory `I_consec
>= 0` sanity gate (same discipline that caught Structured's own NeT-InT bridge bug) failed
twice in a row before landing on the correct fix: (1) Stage 1's `app_entropy` feature
doesn't match NeT's transition marginal exactly (small last-event-per-period boundary
mismatch); (2) the transition edge list's `app_from` marginal is the WRONG side of the
identity — `I(X_t;X_t+1) = H(X_t+1) - H(X_t+1|X_t)` needs the **destination** ("app_to")
marginal, not the source. Full diagnostic trail in
`outputs/model_outputs/ds6/information_theory/model_run_summary.md`. **This is exactly the
fix already on record for Structured's version of the same bug** ("target-state marginal
from NeT's own edge list") — worth remembering directly next time rather than re-deriving
from the wrong side first.

## 0a. Addendum (2026-08-06): a second real bug found mid-plan

While starting NeT, verified `app_next` before building on it (same discipline that caught
the `group_id` bug the day before) and found it does NOT mean "next app opened" — it
mechanically echoes the current row's own app_name 99.3% of the time, because DS6's true
underlying log alternates Open→Close→Open→Close and the next logged event is almost always
that same app's own close. `app_prev` is unaffected and genuine. This also **retracts part
of the 2026-08-05 `close_ts` finding**: `close_ts`/`time_diff_secs` turn out to be genuine
open→close dwell time for ~99% of rows (the arithmetic was right, the interpretation was
wrong). Full verification: `outputs/reports/stage0/ds6_audit_report.md` §8b,
`data_docs/modeling_cautions.md` §6, `data_docs/stage1_feature_qc_notes.md` addendum. Fixed
in `src/features/ds6_features.py` (Group 4 sequence features rebuilt on `app_prev`) before
NeT was built, and NeT itself derives its own transitions independently rather than trusting
either `app_next` or `app_prev` further. **Lesson recorded in CLAUDE.md: verifying one field
in a feature family doesn't clear a different field in the same family — check each one.**
