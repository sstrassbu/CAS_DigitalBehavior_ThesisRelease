# DS5 Step 3 — Personalization / Intervention-Fitting Blueprint

**Written:** 2026-08-07
**Status:** PLANNING ONLY. No notebook, no code, no output files created by this document.
**Stage:** Stage 4, Step 3 (personalization) — first blueprint for this stage, any dataset.
**Audience:** Read before writing or approving any Step 3 implementation notebook.

---

## 0. Why this document exists now

Per `outputs/reports/stage4/step2_vs_step3_priority_note.md`, Step 3 was explicitly
gated behind four conditions: Path C, Path A, Path F, and Path E of the DS5 Step 2
six-path exploration all had to be complete before Step 3 could start. All four are
complete (Path D also complete, closing the full six-path arc — see
`ds5_step2_phenotype_exploration_plan.md` and the memory entry `ds5_step2_focus.md`).
The gate is satisfied. This document is the blueprint the priority note asked for
before any Step 3 code is written — it does not itself start Step 3 implementation.

This blueprint covers **DS5 only**. DS5 is the only RCT in the project (control /
default / reintervention, randomized at the participant level) and is named in
`cross_dataset_implementation_strategy.md` as "the correct first Step 3 dataset."
Structured, DS4, and DS6 have no randomized friction arms (DS6 has a pre/post
baseline→intervention *period*, not parallel arms) and are out of scope here.

---

## 1. The Step 2 / Step 3 boundary, restated

From the priority note:

> **Step 2:** Discover and describe behavioral subgroups. **Step 3:** Use the
> phenotype structure to ask which subgroup responds best to which friction type,
> and prescribe interventions accordingly. The boundary is not ambiguous: Step 3
> begins the moment a cluster assignment is used to recommend a friction type.

Step 3, concretely, asks one question DS5's Step 1 and Step 2 notebooks have not
yet asked directly: **does the effect of experimental condition on behavioral
outcome depend on which phenotype a participant belongs to?** That is a
phenotype × condition **interaction** question, not a main-effect question.

This is a genuinely open question. Checked directly: no existing `model_run_summary.md`
in `game_theory/` or `statistical_mechanics/` contains an interaction term between
`profile_p1` (or any other phenotype label) and `study_condition`. What exists so far:

- GaT (`46_ds5_game_theory.ipynb`) tested the **main effect** of condition on
  `commitment_score` (ANOVA F=40.99, p<0.001) and the **main effect** of NeT profile
  on `commitment_score` (p=0.105, null — "network topology ≠ commitment").
- StM tested condition effects on `chi_behav`/susceptibility and DyS-regime
  distribution, not phenotype × condition jointly.
- Path E (`104_ds5_condition_stratified_phenotype.ipynb`) tested whether cluster
  *geometry* differs by condition (it does), but did not regress an outcome on
  phenotype × condition with an interaction term.

A null main effect for phenotype (GaT, p=0.105) does not imply a null interaction —
a phenotype can have no average effect on the outcome while still moderating how
strongly condition moves that outcome. That gap is what Step 3's first analysis
should fill.

---

## 2. The central feasibility constraint: DS5 is between-subject

This is the single most important constraint on what Step 3 can and cannot claim,
and it must be stated before anything else.

**Confirmed:** `outputs/reports/stage4/ds5_step2_phenotype_exploration_plan.md`
line 269: *"Condition assignment in DS5 is at the participant level (not
within-participant) — so no pre/post comparison is possible; this is purely
between-condition."* Each of the 414 eligible participants was assigned to exactly
one of {control, default, reintervention} and stayed there. No participant is
observed under more than one friction condition.

**Consequence:** there is no individual-level counterfactual in the data. It is
not possible to say "participant X, who got default friction, would have shown a
lower override rate under reintervention" from observation alone — that outcome
for participant X under reintervention was never recorded and cannot be recovered
without a model-based simulation (see Framework C, §6.3, which inherits its own
separate reliability problem).

This rules out any Step 3 framing that implies a validated per-user recommendation
("this user should get condition Y"). What DS5's data *can* support is a
group-level, associational claim: "participants whose behavioral profile looks
like phenotype P show a larger/smaller condition effect than phenotype Q." That
is still a legitimate and useful Step 3 result — it is what "phenotype-sensitive
personalization" can honestly mean in this dataset — but the scope must be stated
this way every time the result is reported, not loosened into an individual
prescriptive claim.

---

## 3. A second constraint, found while preparing this blueprint: post-treatment bias risk in the phenotype choice

This was not previously flagged anywhere in the DS5 Step 2 documentation and is
the main new finding of this planning pass. It determines which of the existing
phenotype solutions is actually usable as a Step 3 moderator.

**The problem:** several of DS5's existing phenotype solutions are themselves
condition-associated (Path A: χ²=91.885, p<0.0001; Path F within-Profile-B:
χ²=60.963, p<0.0001). If a phenotype label is partly *caused by* the condition a
participant received, then using that phenotype as a moderator of the condition
effect is circular — it conditions on a variable that sits downstream of the
treatment (a "post-treatment" or collider-adjacent variable in causal-inference
terms), and any apparent interaction is confounded with the direct effect of
condition on the phenotype label itself, not a real trait-based moderation.

**Verified directly for this blueprint** (not previously computed anywhere in the
repo), GaT's `strategy` label shows the same problem in an even starker form:

| study_condition | adaptive_switcher | chronic_override | reward_oriented |
|---|---|---|---|
| control | 13 | 90 | 48 |
| default | 62 | 12 | 41 |
| reintervention | 33 | 42 | 52 |

`chronic_override` drops from 90 (control) to 12 (default); `adaptive_switcher`
rises from 13 to 62 over the same contrast. GaT `strategy` is overwhelmingly a
function of which condition a participant was in, not a stable individual trait —
consistent with GaT's own already-documented ANOVA (condition F=40.99, p<0.001)
but sharper once shown as a raw crosstab. **GaT `strategy` is not usable as a
Step 3 moderator.**

**By contrast**, checked directly for this blueprint:

| study_condition | Profile A (NeT) | Profile B (NeT) |
|---|---|---|
| control | 43 | 94 |
| default | 46 | 96 |
| reintervention | 36 | 99 |

The Profile A / Profile B split (`profile_p1`, Phase 1's NeT-based phenotype) is
close to proportionally identical across all three conditions (Phase 1's own
χ²=1.22, p=0.545 already established this at the aggregate level; the cell counts
above confirm it holds cell-by-cell too). This is exactly the property a Step 3
moderator needs: **a phenotype that is not itself shaped by condition assignment
is safe to cross with condition**, because any interaction found cannot be
explained away as "the phenotype is just relabeling who got which condition."

**Rule to apply when choosing a Step 3 phenotype input:** prefer phenotype
solutions built from features that are condition-independent (NeT-topological:
`HHI_net`, `rho_self`) over phenotype solutions built from features already shown
to shift with condition (behavioral-dynamic: `sig_hat`, `H_emp`, `x_mean`, and
anything derived from them like `chi_behav` or GaT `strategy`). This inverts the
Step 2 emphasis — Path A/F treated the behavioral-dynamic axis as the *richer*
phenotype dimension for describing heterogeneity, which was the right call for
Step 2's descriptive goal. For Step 3's moderator role specifically, richness is
not the deciding property; condition-independence is.

---

## 4. A third constraint: outcome variable must not overlap with the phenotype's own defining features

Related to §3 but distinct: even a condition-independent phenotype can be
circular if the *outcome variable* chosen for the interaction test was one of the
features used to build the phenotype in the first place.

- ~~NeT profile (`profile_p1`) is built from `HHI_net`/`rho_self` only — structurally
  distinct from any override-rate or entropy outcome. **Any behavioral outcome is
  safe to pair with it** (x_mean, commitment_score, chi_behav, H_out).~~
  **CORRECTION (2026-08-08): the struck bullet above is factually wrong.** `profile_p1`
  is *not* a NeT-only phenotype. Notebook 100 clustered it on the five-feature set
  `PHASE1_CORE = ['sig_hat', 'H_emp', 'x_mean', 'HHI_net', 'rho_self']` and then
  relabelled the clusters by ascending `x_mean`, so `x_mean`, `sig_hat` and `H_emp`
  entered both construction and naming. Consequently `x_mean`, `commitment_score`
  (r=-0.9797 with `x_mean`) and `chi_behav` (= 2·x_mean·(1−x_mean)/sig_hat², an exact
  identity on all 414 participants) all leak into the moderator; no behavioral outcome
  is safe to pair with `profile_p1`. The moderator actually implemented in Step 3 is the
  NeT-only `cluster_net_only` (NetC), built from `HHI_net`/`rho_self`/`H_trans`/`H_app`.
  See `notebooks/200_ds5_personalization_exploration.ipynb` and
  `outputs/model_outputs/personalization/model_run_summary.md`.
- Path A's C1/C2/C3 (or the v2 GMM solution, `profile_k3`) is built partly from
  `x_mean` itself. **`x_mean` cannot be the outcome variable if a behavioral-dynamic
  phenotype is the moderator** — that would test whether a cluster defined in part
  by high x_mean has high x_mean, which is definitionally true and not a finding.
  `chi_behav` is also weak here since it is a direct function of `sig_hat`, also a
  clustering feature.

This is a second, independent reason (on top of §3) to prefer a *NeT-only* moderator:
among the existing phenotype solutions, only `cluster_net_only` (NetC) has no feature
overlap against the candidate outcome variables in §6.2. `profile_p1` does **not**
qualify — see the 2026-08-08 correction above.

---

## 5. Inventory of available inputs (all pre-computed, nothing new to derive)

All quantities below already exist as CSVs from DS5 Step 1 (all 7 active model
families) and Step 2 (six-path exploration + v2 revision arc). Step 3's first pass
needs no new feature engineering — only joining existing tables on
`participant_id_canonical` and `study_condition`.

| Source | File | Relevant columns | N |
|---|---|---|---|
| Phase 1 phenotype | `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` | `profile_p1` (Profile A/B) | 414 |
| GMM v2 phenotype | `outputs/model_outputs/phenotyping/ds5_gmm_k3_assignments.csv` | `profile_k3` (G1/G2/G3), posterior probs | 414 |
| Path A behavior-only | `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` | C1/C2/C3 | ~414 |
| Path F hierarchical | `outputs/model_outputs/phenotyping/ds5_hierarchical_assignments.csv` | `cell_f` (4-cell taxonomy) | 414 |
| Path E within-condition | `outputs/model_outputs/phenotyping/ds5_condition_cluster_assignments.csv` | `cond_cluster_full`, `cond_cluster_B` | 414 |
| Path B friction-response | `outputs/model_outputs/phenotyping/ds5_intervention_cluster_assignments.csv` | `cluster_b_full`, `cluster_b_rei`, `cluster_b_con` | 414 |
| StoP | `outputs/model_outputs/stochastic_processes/participant_parameters.csv` (+ `..._v2_mle.csv`) | `x_mean`, `mu_hat`, `sig_hat`, `sigma_mu_ratio` | 414 |
| StM | `outputs/model_outputs/statistical_mechanics/participant_stm_parameters.csv` (+ `_v2.csv`) | `chi_behav`, `beta_behav`, `F_behav`, `behavioral_regime` | 414 |
| DyS | `outputs/model_outputs/dynamical_systems/participant_dynamics_parameters.csv` | `regime_label`, `is_dys_eligible`, `deviation_from_predicted_fixed_point` | 414 |
| NeT | `outputs/model_outputs/network_models/participant_network_metrics.csv` (+ `_v2_no_selfloop.csv`) | `HHI_net`, `rho_self` | 414 |
| InT | `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` | `H_emp`, `H_out`, `H_app`, `H_hour` | 414 |
| GaT | `outputs/model_outputs/game_theory/participant_gat_parameters.csv` | `commitment_score`, `strategy`, `adaptation_direction`, `p_open_after_dismiss` | 414 |
| ABM | `outputs/model_outputs/agent_based/participant_abm_summary.csv` | `x_mean_obs`, `x_mean_sim` (gate: ρ=0.428, FAILED) | subset |
| Psychosocial | `ds5_psychosocial_overlays.csv` + prepost survey | FoMO, belonging, ostracism, digital wellbeing, social media wellbeing | subset |
| Combined feature matrix | `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` | all of the above, one row per participant | 414 |

Nothing in this table requires new raw-data processing. Step 3's data-preparation
step is a set of joins on already-cleaned, already-validated tables — the actual
Step 1/2 estimation work is done.

---

## 6. Design space: what Step 3 could mean here, laid out as explicit options

### 6.1 Candidate phenotype inputs (the moderator)

| Candidate | Condition-independent? (§3) | N per cell (3 conditions) | Verdict |
|---|---|---|---|
| `profile_p1` (**five-feature** Phase 1, k=2 — not NeT-only) | Condition-independent (χ²=1.22, p=0.545; cell counts 43/46/36 vs 94/96/99) but **outcome-leaking** | 36–99, all >30 | **Superseded** — replaced as primary by the NeT-only `cluster_net_only` (see §4 correction) |
| `profile_k3` (GMM v2, k=3) | Largely (not formally re-tested, but built from same NeT-adjacent features as Phase 1) | G2 row = 17–21 (below 30) | Secondary/robustness only; G2 underpowered for the full 3×3 |
| Path A / GMM behavioral (C1/C2/C3) | **No** (χ²=91.9, p<0.0001) | N/A | Excluded as primary moderator — post-treatment bias (§3) |
| Path F `cell_f` (4-cell) | No (inherits Path A's condition-association within Profile B) | Smallest cells <20 | Excluded — same bias, and underpowered |
| GaT `strategy` | **No**, most strongly of all (§3 table) | N/A | Excluded |
| Path E within-condition clusters | By construction, computed separately per condition | N/A | Not a cross-condition moderator by design — useful only for the descriptive framework in §6.4, not the interaction test in §6.2 |

### 6.2 Candidate outcome variables

| Candidate | Overlaps phenotype-defining features? | Interpretation | Verdict |
|---|---|---|---|
| `x_mean` (StoP/StM, override rate) | No overlap with the NeT-only `cluster_net_only`; **overlaps `profile_p1`** (an x_mean construction/naming input) and Path A/GMM-behavioral phenotypes | Fraction of friction-eligible moments the app was opened anyway | **Primary candidate**, paired only with `cluster_net_only` (NOT `profile_p1` — see §4 correction) |
| `commitment_score` (GaT, rate_not_opened) | No overlap with NeT profile | Inverse-flavored version of `x_mean`, computed from a different event slice (friction events only, not all days) — already flagged FLAG G1 in GaT's own blueprint as "behavioral proxy, not utility" | Secondary candidate, useful as a replication check on `x_mean`'s result using an independently-computed quantity |
| `chi_behav` (StM susceptibility) | Overlaps Path A/GMM (built from `sig_hat`) but not NeT profile | Tipping-point proximity, not a level | Tertiary — theoretically the most Step-3-relevant quantity per `ds5_step2_presentation_summary.md` ("intervention-readiness... very relevant for personalization"), worth a dedicated pass but not the first one |
| `H_out` / `H_out_resid` (InT) | Flagged condition-confounded and excluded from Step 2 clustering entirely (`ds5_step2_phenotype_exploration_plan.md`) | Consistency/entropy of response, not a level | Do not use as a primary outcome without first re-examining exactly why it was excluded in Step 2 — the same confound likely applies here |

### 6.3 Candidate analytic frameworks

**Framework A — Two-way interaction test (recommended primary).**
Regress (or ANOVA) outcome ~ phenotype × condition + phenotype + condition, using
`profile_p1` × `study_condition` on `x_mean` (then replicate on `commitment_score`).
Report the interaction term's F/p and partial η², not just the main effects GaT
already reported. This is a purely associational, group-level claim — exactly what
§2 says DS5's between-subject design can support. Six cells, smallest N=36 (see
§7) — adequately powered for a 2×3 factorial.

**Framework B — Descriptive "who does best under which condition" table.**
For each existing phenotype × condition cell (not just NeT profile — this can
reuse Path E's within-condition clusters too, since Framework B does not need the
moderator to be condition-independent, only the *report* needs to say so), tabulate
mean/median outcome with bootstrap CIs. This is lower rigor than Framework A (no
formal interaction test, more researcher-df in table construction) but easy to
produce, useful as a companion illustration, and can legitimately use the
richer/condition-associated phenotypes (Path A, Path F, GaT strategy) **as long as
every such table is captioned as descriptive-only, not as evidence of
trait-based moderation** given §3.

**Framework C — Model-based simulated counterfactual.**
Use each participant's fitted StoP SDE parameters (or the ABM's agent rules) to
simulate their trajectory under a condition they did not actually receive, then
compare simulated outcome across phenotypes. This is the only framework that could
approach an individual-level counterfactual claim (§2) rather than a purely
group-level one. **Major reliability caveat, already on record:** DS5's own ABM
notebook (47) found the validation gate FAILS — simulated vs. observed trajectory
correlation ρ=0.428 against a 0.80 threshold, with a systematic ~11pp
underestimate for high-rate participants, attributed to the bounded SDE's ergodic
pull toward 0.5 over 30-day horizons. Any Step 3 simulated-counterfactual result
would inherit this known bias. If pursued at all, Framework C should be scoped as
an explicitly-labeled exploratory/illustrative pass, not a claim-bearing analysis,
until the underlying ABM gate is revisited.

**Framework D — GaT-strategy rule-based prescriptive mapping.**
Use the already-computed GaT `strategy` labels to hand-write a rule
("chronic_override participants → recommend reintervention," etc.), matching
what `src/personalization/recommendation_rules.py` (currently a two-line
placeholder) is presumably intended to eventually hold. **Not recommended as a
first pass** — §3 already shows `strategy` is condition-shaped, not a stable trait,
so a rule built on it is prescribing based on an effect of treatment, which is
circular in the same way as using `strategy` as a Framework A moderator. This
framework only becomes defensible after Framework A establishes a real,
condition-independent moderator; then the rule can be re-expressed in terms of
that moderator instead of `strategy`.

### 6.4 Recommended combination

| Priority | Framework | Moderator | Outcome | Role |
|---|---|---|---|---|
| 1st | A | `profile_p1` (NeT) | `x_mean` | Primary interaction test |
| 2nd | A (replication) | `profile_p1` | `commitment_score` | Robustness check on 1st, independent outcome computation |
| 3rd | A (robustness) | `profile_k3` (GMM v2, collapsing G2 if needed) | `x_mean` | Sensitivity check: does the finding hold under an alternate condition-independent-ish phenotype? |
| 4th | B | Path E within-condition clusters / GaT `strategy` | any | Descriptive companion table only, explicitly captioned as non-causal/condition-shaped |
| Deferred | C | StoP/ABM simulation | simulated `x_mean` | Only after the ABM gate (ρ=0.428) is separately revisited; not part of first pass |
| Deferred | D | rule-based | — | Only after Framework A produces a condition-independent moderator to hang rules on |

---

## 7. Power check (computed directly from existing CSVs for this blueprint)

`profile_p1 × study_condition` cross-tabulation (N=414 total, all eligible
participants):

| | control | default | reintervention |
|---|---|---|---|
| Profile A | 43 | 46 | 36 |
| Profile B | 94 | 96 | 99 |

Minimum cell = 36 (Profile A × reintervention). A 2×3 ANOVA/regression with a
smallest cell of 36 is adequately powered to detect small-to-moderate interaction
effects (comparable to, e.g., Path E's own within-condition clustering cells,
which ran with similar or smaller N and were treated as informative). This is
markedly better-powered than any of the excluded richer taxonomies — Path F's
smallest reported cells were already below the N=30 floor used throughout Step 2,
and GMM v2's G2 row (17–21 per condition) would be the binding constraint on any
3×3 design.

---

## 8. Statistical method notes

- **Primary test:** two-way factorial ANOVA (or OLS regression with a
  `profile_p1 × study_condition` interaction term encoded as categorical dummies)
  on `x_mean`. Given DS5's established pattern of non-normal, sometimes skewed
  behavioral distributions (entropy and Fano-type quantities elsewhere in this
  project), **check normality/homogeneity of variance on `x_mean` by cell before
  trusting parametric p-values** — this is the same "mandatory gate before
  trusting a result" discipline used throughout Step 1 (e.g., the NeT-InT bridge
  non-negativity checks in DS6/Structured). If violated, fall back to a rank-based
  interaction test (aligned rank transform ANOVA) rather than assuming parametric
  validity.
- **Effect size:** report partial η² for the interaction term, not just p — Path
  A/B/D/E all reported effect sizes (Jaccard, ARI, ε²) alongside significance, and
  Step 3 should match that standard.
- **Multiplicity:** if all three rows of §6.4 (x_mean, commitment_score, GMM v2
  sensitivity) are run, apply a Bonferroni or Holm correction across the 3 primary
  interaction tests before calling any one "significant," consistent with how the
  psychosocial overlays throughout this project have always been Bonferroni-corrected.
- **Robustness:** bootstrap the interaction effect (resample participants within
  condition × profile cells) to get a CI, not just a point estimate + p-value —
  matches the bootstrap-Jaccard discipline used everywhere else in Step 2.

---

## 9. What a genuine finding vs. a genuine null would each mean

Stated in advance, before any test is run, per this project's established
honesty-first convention (DS6 SyD nulls, ABM gate failure, Structured StM
path-dependence null, GaT's own null main effect):

- **If the `profile_p1 × study_condition` interaction on `x_mean` is
  significant:** this would be DS5's first evidence that network-topological
  phenotype moderates the behavioral response to friction type — a genuinely new
  cross-model finding, since GaT already ruled out a phenotype *main* effect and
  no notebook has tested the interaction specifically. It would motivate a
  dedicated Step 3 notebook (200-series) building the full interaction model,
  visualizations, and — cautiously — Framework D's rule-based mapping re-based on
  `profile_p1` instead of `strategy`.
- **If null:** also a legitimate, reportable result. It would mean the one
  phenotype axis proven safe from post-treatment bias (NeT topology) does not
  moderate condition response — the moderation, if it exists at all, would have to
  live in the behavioral-dynamic axis, which is exactly the axis §3 shows cannot
  be tested cleanly with this between-subject design. That would be a real,
  structural limitation of DS5 for Step 3 specifically (not a failure of
  execution) and worth stating plainly: DS5's RCT design may not be able to
  support a clean personalization claim beyond the network-topology axis, and
  DS4/DS6/Structured (naturalistic, no randomized arms at all) could not do
  better. This possibility should be named in the thesis text regardless of which
  way the test comes out, so it does not read as a result chosen after the fact.

---

## 10. Interpretive scope — what Step 3 must NOT claim from this design

- Not a validated per-user recommender system — no participant was observed under
  more than one condition (§2).
- Not causal evidence that phenotype *causes* differential response — DS5's
  condition assignment is randomized, but phenotype assignment is observational
  and post-hoc; at best this is "condition effect differs by observed phenotype,"
  not "assigning friction by phenotype would improve outcomes" (that would require
  a second, phenotype-stratified RCT this dataset does not contain).
- Not generalizable beyond German adolescents in this specific study window without
  cross-dataset replication — flagged the same way `ds5_path_e_condition_stratified_blueprint.md`
  §13 already flags for its own within-condition clustering result.
- Not a claim that richer phenotypes (Path F, GMM, GaT strategy) are "wrong" —
  they remain valid and valuable for Step 2's descriptive goal. They are simply
  the wrong tool for Step 3's specific moderator role, for the reasons in §3.

---

## 11. Proposed deliverables (if/when this blueprint is approved for implementation)

Naming follows the convention already recorded in
`outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md`
§5.1, which named this exact notebook before any Step 2 path work started:

```
StoP → InT → DyS → StM → NeT → GaT → ABM      (Step 1, all complete)
                              ↓
     100–106_*.ipynb                            (Step 2, all complete)
                              ↓
     200_ds5_personalization_exploration.ipynb  (Step 3 — this blueprint)
```

- Notebook: `notebooks/200_ds5_personalization_exploration.ipynb`
- Output directory: `outputs/model_outputs/personalization/` (new; matches the
  existing `outputs/model_outputs/<family>/` convention used by every Step 1/2
  family so far)
- Expected output files (each with a companion `.md` per the project's output
  documentation rule):
  - `phenotype_condition_interaction_results.csv` — one row per outcome ×
    phenotype-candidate combination from §6.4, with F/p/partial η²/bootstrap CI
  - `phenotype_condition_cell_summary.csv` — cell means/medians/N for the
    descriptive Framework B table
  - `model_run_summary.md` — same convention as every other Step 1/2 notebook
- `src/personalization/` remains untouched at this stage — `recommendation_rules.py`
  and `intervention_matching.py` are the natural eventual homes for Framework D
  logic, but only after Framework A produces a condition-independent moderator to
  base rules on (§6.3).

No files in this list have been created by this planning pass except this
blueprint itself.

---

## 12. Open decisions for the user before implementation starts

1. **Confirm primary moderator/outcome pair** — this blueprint recommends
   `profile_p1` × `x_mean` (Framework A, §6.4 row 1). Agree, or prefer a
   different starting pair?
2. **Scope of the first notebook** — just Framework A rows 1–3 (interaction
   tests), or also include Framework B's descriptive companion table in the same
   pass?
3. **Framework C (simulated counterfactual)** — explicitly deferred here given
   the ABM gate failure (ρ=0.428). Revisit that gate first, or leave Framework C
   out of DS5 Step 3 entirely and treat it as a thesis "limitations/future work"
   item instead?
4. **Framework D (rule-based prescription)** — build a first illustrative version
   now (clearly labeled non-validated), or wait until Framework A's result is in
   hand so any rule is grounded in a real, condition-independent moderator?
5. **`chi_behav` as a dedicated third pass** — the presentation summary already
   calls susceptibility "very relevant for personalization." Worth a dedicated
   Framework A variant (§6.2 tertiary candidate) in the same notebook, or a
   separate follow-up?

---

## 13. Summary

DS5 Step 3 is feasible now — the Step 2 gate is satisfied, all needed inputs
already exist as validated CSVs, and no new raw-data or feature-engineering work
is required. The main contribution of this planning pass is negative-space
mapping: of DS5's roughly six existing phenotype solutions, only one
(`profile_p1`, the NeT-topological Phase 1 split) is safe to use as a Step 3
moderator without post-treatment bias, because it is the only one shown to be
statistically independent of condition assignment. The richer, more
interpretively interesting phenotypes from Path A/F and GaT are exactly the ones
Step 3 cannot cleanly use in the interaction-test role, precisely because
condition shapes them — which is itself a real, citable finding about DS5's
design, not just a constraint to work around quietly. The recommended first
notebook (Framework A, `profile_p1 × study_condition` on `x_mean`, replicated on
`commitment_score`) is small, adequately powered (min cell N=36), and answers a
question no existing DS5 notebook has asked yet.
