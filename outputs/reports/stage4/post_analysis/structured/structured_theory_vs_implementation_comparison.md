# Theory vs. Implementation Comparison — Structured Model Families

**Written:** 2026-08-08
**Overlap check:** Read in full before writing — `outputs/reports/stage4/post_analysis/theory_vs_implementation_comparison.md`
(DS5's version, whose per-family "theory intended / what was implemented / assessment" structure this
document follows), all 8 Structured model blueprints (each of which already contains its own theory
quotation and an inline "why this cannot be a DS5 port" argument for its own family), and
`structured_cas_modeling_plan.md`. **No existing Structured document assembles all 8 families' theory-
fidelity assessments into one place** — each blueprint argues its own case individually, in isolation from
the other 7. This document's contribution is the cross-family table and the single combined verdict table
at the end; the underlying theory quotations and per-family reasoning are drawn directly from each
blueprint, not reinterpreted.

---

## Background

The theory paper (`Structured Planning as a Complex Adaptive System.pdf`, Strassburger, Schmiedmayer &
Grüning) proposes applying the same eight CAS model families used elsewhere in this project to digital
task-planning behavior. Unlike DS5 (whose source paper commits early to a single scalar proxy, `X_t =
n_opened/n_events`), the Structured paper names a **different state variable, and often a different
proxy structure, for nearly every model family** — daily creation counts for StoP, a 5-dimensional weekly
vector for DyS, a joint multi-property configuration for StM, a commitment scalar for GaT. This means the
"theory vs. implementation" question for Structured is less about whether one shared proxy was
approximated well (DS5's central question) and more about whether **each family's own, separately-stated**
paper section was faithfully translated — and, in three cases (StoP, DyS, StM), about whether the DS5
implementation's own general *pattern* (a specific proxy formula, a specific dependency chain) was
correctly recognized as **not** transferable and was deliberately not ported.

The paper's own §1.3 groups the eight families by data requirement and adds one caution not present in
DS5's source paper: it explicitly warns, in its own words, that GaT and StM in particular "require more
careful proxy definitions" because payoff/utility and energy/temperature/equilibrium are not directly
observed in task-log data. This caution shapes those two families' implementations directly (see below)
and is itself a data point on theory-fidelity: **the Structured paper is more self-aware about its own
proxy risk than DS5's source paper was**, and the implementation record below shows that caution was
respected, not overridden.

---

## NeT — Network Theory

### Theory intended

Paper Table 1: "Build task-state transition networks, e.g., created → inbox, inbox → timed, timed →
moved, moved → completed, or timed → unresolved. Identify central states and loops." §2.4 names nodes as
task states and phenotypes as inbox-hub, timeline-centered, rescheduling-loop, or completion-path users.

### What was implemented

A 7-state vocabulary (`inbox, timed, all_day, moved, completed, reopened, deleted`) derived by a
documented priority-order rule from `event_type` + `update_type_list_str` + `task_type`; edges built
per-task then pooled to the participant level; HHI_net, rho_self, H_trans, stationary π — identical
formulas to DS5's own NeT, applied to a different (state, not app) vocabulary.

### Assessment

**Highly theory-faithful.** The paper's own worked example (`created→inbox→timed→moved→completed`) is
directly reproduced by the pooled transition matrix (verified: `moved` is the dominant intermediate hub,
`timed→moved` 2,919 / `moved→completed` 2,794 transitions — see
`outputs/model_outputs/structured/network_theory/model_run_summary.md` and
`structured_cas_modeling_plan.md`'s second status update). The one genuine structural correction needed
was not a theory-fidelity issue but a data-coverage one: 60.7% of tasks are left-censored, so entry-state
statistics (how tasks are "born") had to be restricted to the 39.3% non-censored subset (FLAG W1) — a
data limitation, not an implementation shortcut.

**Approximations to note, all explicitly flagged in the blueprint (mirroring DS5's own NeT weakness-flag
discipline):** self-loops included by design (cosmetic edits collapse to a self-loop, FLAG NET-S2); no
higher-order Markov test (FLAG W3); small 7-state vocabulary bounds all entropy/HHI comparisons well below
DS5's own app-vocabulary NeT values, so the two datasets' NeT magnitudes are **not directly comparable**
(FLAG W4) — a point worth stating explicitly if NeT results from both datasets are ever discussed side by
side.

**Most defensible finding:** the NeT–InT bridge identity (`I_consec_state = H_state_marginal − H_trans`),
verified at 0 chain-rule violations across all 45 eligible participants after a wrong-marginal bug was
caught and fixed during implementation (see below, InT section) — directly analogous to DS5's own
`I_consec = H_app − H_trans` bridge, and, like DS5's, empirically clean once the correct marginal was
used.

---

## InT — Information Theory

### Theory intended

Paper §2.5 (quoted in full in the blueprint): entropy over task types, creation sources, time of day,
recurrence, alert use, categories, energy levels, or completion outcomes; mutual information asking
whether task type reduces uncertainty about completion, energy level about movement/delay, creation
source about inbox/timeline placement, and time of day about task type.

### What was implemented

Seven per-participant entropy measures (`H_type_first/last`, `H_creation_source`, `H_hour_creation`,
`H_recurrence`, `H_completion`, `H_reschedule`) and three of the paper's four named mutual-information
pairs, pooled across the sample. The fourth (`energy level → movement/delay`) is explicitly reported as
not-implementable (energy level absent from the export), not silently dropped.

### Assessment

**Highly theory-faithful — deliberately not a DS5 port.** Every implemented quantity traces to a specific
sentence in the paper's own §2.5, quoted directly in the blueprint before any code was written (Part 0).
This is a stronger direct-traceability discipline than DS5's own InT notebook needed, since DS5's InT
built two DS5-specific constructs (`H_out`, `H_emp`) that have no textual anchor of this kind.

**One real implementation bug, caught and fixed before results were trusted:** the first attempt at the
NeT–InT bridge computed `H_state_marginal` from the raw per-event state-label distribution, which wrongly
included 15,301 single-event tasks contributing zero transitions — producing a mathematically impossible
negative mutual information (`I_consec_state` as low as −0.676) for several participants. Fixed by using
the `state_to` marginal from NeT's own edge list. This is the **same bug class** independently found in
DS6's own NeT–InT bridge and flagged in `cross_dataset_cas_model_synthesis.md` §2 as "found three times
independently" (Structured, DS6, DS4) — worth stating explicitly here since it is one of this project's
most-repeated lessons, not a one-off Structured issue.

**Known power caveat, stated in advance rather than discovered after running:** the
creation-source→placement mutual-information test has a severely imbalanced target (1.4% inbox / 98.6%
timeline); a near-degenerate normalized-MI result there should be attributed to class imbalance, not
necessarily absence of dependency — the blueprint reports a supplementary 3-class version for this reason.

**Main gap to note for the paper:** three of the paper's named entropy dimensions (alert use, task
category, energy level) are structurally unavailable in this export, confirmed in
`structured_cas_modeling_plan.md` §2. This is a data-availability limitation, not an implementation
shortfall — the paper's own promised codebook fields simply do not exist in the real export.

---

## StoP — Stochastic Processes

### Theory intended

Paper's own worked example (quoted in the blueprint): "a concrete Stochastic Processes example would
model the number of timed tasks created per user-day... temporal role: useful for modeling planning
activity, completion marking, inbox use, task complexity, and recurrence."

### What was implemented

Two count-based daily state variables (`N_t^created`, `N_t^completed`), zero-filled to a regular daily
grid on the participant's **local calendar day**, method-of-moments `mu_hat`/`sig_hat`, plus a new
count-process-specific burstiness measure (`Fano_factor`) not used anywhere in DS5.

### Assessment

**A deliberate and well-justified non-port, not a simplification of DS5's design.** DS5's StoP state
variable (`X_t`, a bounded [0,1] daily override rate) and Structured's (`N_t`, an unbounded daily count)
are genuinely different mathematical objects — the paper's own worked example names a count, not a rate,
so porting DS5's proportion-based SDE machinery would have **misrepresented** the paper's own intent, not
merely simplified it. This is the single clearest place in the whole Structured arc where "not a DS5 port"
is a theory-fidelity improvement over blind reuse, not a weakening.

**Real, verified data decision (not assumed):** binning by local calendar day rather than UTC day was
checked against actual data before implementation — 24/61 participants (39%) have more than one distinct
`event_timezone`, so naive UTC binning would have misclassified genuinely same-session planning activity
across day boundaries.

**Headline theory-confirming result:** Fano factor mean ≈ 6, with 97.7% (`N_t^created`) and 94.7%
(`N_t^completed`) of eligible participants showing Fano > 1 — this **directly answers** the paper's own
StoP framing question ("is planning behavior mainly stable, drifting, noisy, or bursty?") in a way DS5's
bounded-rate StoP model structurally cannot, since Fano is not defined for a rate. Stability is the rarest
descriptive label (1–3 participants) — a genuinely paper-anticipated finding ("Example B" names `stable`
as one possible type among several), empirically confirmed as the exception rather than the rule.

**Approximation to note:** the method-of-moments estimation technique itself (not the state variable) is
reused from DS5 as a general statistical tool, explicitly separated in the blueprint from DS5's
domain-specific proxy choice — worth stating this distinction explicitly, since "reuses DS5's method" and
"ports DS5's model" are easy to conflate and this notebook deliberately does only the former.

---

## DyS — Dynamical Systems

### Theory intended

Paper §2.2 (quoted in the blueprint): a user-day represented by a vector of planning variables (tasks
created, proportion timed, proportion inbox, proportion completed, task complexity); different planning
styles as attractor-like regions; the paper's own worked example is explicitly **weekly**
("in the first week... in the second week...").

### What was implemented

A 5-dimensional weekly state vector (`n_created_w`, `timed_share_w`, `inbox_share_w`, `completed_share_w`,
`complexity_w`), participant-relative week indexing, trajectory metrics (`state_space_volatility`,
`volume_trend_slope`, `dropout_score`), and 6 rule-based descriptive region labels drawn directly from the
paper's own named regimes (`high-structure`, `sparse-consistent`, `inbox-heavy`, `dropout-prone`, plus
`oscillatory` and `mixed`).

### Assessment

**Highly theory-faithful, and a genuine structural improvement over a literal DS5 port.** DS5's DyS
notebook reduces its own *single-variable* StoP SDE to a σ→0 deterministic limit — a 1D reduction. The
paper's own Structured DyS text describes a **multi-dimensional** state-space trajectory at **weekly**
resolution, which is what was actually built. Recognizing that DS5's 1D reduction technique simply does
not apply to a 5D paper-specified vector, and that StoP's own daily resolution (justified by its own
different worked example) does not match DyS's weekly resolution, is the correct reading of two
independently-stated paper sections — not an arbitrary design choice.

**One real reporting bug, caught and fixed:** the first run silently dropped 4 fully-censored
participants from the eligibility denominator (reporting "42/57, 73.7%" instead of the correct "42/61,
68.9%"). Fixed by counting them explicitly as ineligible, matching the convention already established in
the NeT notebook.

**Approximation to note, stated honestly in the blueprint:** `completed_share_w` measures a task's
*eventual* fate, not same-week completion — a deliberate reading of the paper's "proportion of completed
tasks" that avoids penalizing tasks that simply haven't had time to complete yet, but means the weekly
vector mixes same-week creation composition with a longer-horizon outcome measure. This is disclosed, not
hidden.

**Convergent finding worth flagging for the paper:** `dropout-prone` is the single most common region
label (14/42, 33%), and `high-structure` (the paper's most "ideal" category) is the rarest (2/42) —
matching StoP's own independent finding that "stability is the exception." Two independently-built model
families (StoP's phenotype labels, DyS's region labels) converge on the same substantive story via
different methods, a genuine cross-model finding worth stating in the paper alongside the individual
per-family results.

---

## SyD — System Dynamics

### Theory intended

Paper §2.8 (quoted in the blueprint): stocks (planned/inbox/unresolved/recurring/completed tasks), flows
(creation, scheduling, completion, rescheduling, abandonment); a productive reinforcing loop (creation →
structure → completion → continued use), an overload loop (excessive creation → unresolved tasks →
rescheduling → disengagement), and a balancing loop (overload response via simplification or
rescheduling).

### What was implemented

A running backlog stock (`Backlog_w`, non-censored tasks only), and three feedback-loop correlation tests
mapped 1:1 onto the paper's three named loops, each with a **predicted sign stated in advance** (a
falsifiable design choice, not a fit-after-the-fact one).

### Assessment

**Highly theory-faithful**, and the one family with an explicit, written non-redundancy check (Part 0.5
of the blueprint) confirming before any code was written that SyD's stock (a running total) is genuinely
new information beyond NeT's static edge counts, StoP's isolated flow rates, or DyS's composition/trend
metrics — a discipline DS5's own SyD deferral document never had to perform, since DS5 never implemented
SyD at all (deferred to DS6 for a structural survey-wave reason).

**A real, material methodological correction, directly informative for theory-fidelity:** the pooled
`productive`-loop correlation (`r=0.9456`) was **implausibly strong** for a genuine week-to-week
mechanism, and turned out to be almost entirely a between-participant volume confound. After
person-mean-centering, the within-participant productive-loop correlation drops to `r=0.12`. More
importantly for theory-fidelity: **the overload loop's predicted sign (negative) is only correct after
this correction** — the pooled version has the wrong sign (`r=0.42`, positive). Without the
within-participant check, this notebook would have reported the paper's central overload-loop prediction
as **falsified**, when the corrected analysis shows it is, modestly, **supported** (`r=-0.18`
within-participant). This is a case where a naive theory-vs-data comparison would have reached the wrong
conclusion about theory fidelity, caught only by a methodological safeguard applied proactively (this
lesson was then carried forward and applied *in advance*, not just reactively, in the GaT and StM
notebooks — see below).

**Genuine partial non-replication, reported honestly:** the balancing loop's predicted sign (positive:
backlog co-occurring with more rescheduling) does **not** replicate in the within-participant version
(`r=-0.11`, wrong sign even after correction) — the paper's third loop is the one loop this notebook does
not confirm, stated plainly rather than reframed.

---

## StM — Statistical Mechanics

### Theory intended

Paper §2.1 (quoted directly in the blueprint, in language noticeably more cautious than DS5's own source
paper): "quantities such as energy, temperature, and equilibrium are not directly observed in task-log
data. They would need to be treated as analogy-based constructs or derived proxy quantities rather than
literal physical variables." The paper's own worked example defines a microstate as a **joint task
configuration** across multiple properties (timed/all-day, inbox status, duration, recurrence, notes,
subtasks, alerts, eventual completion) — not a binary outcome.

### What was implemented

**No literal β/T/Z/F thermodynamic apparatus was built at all** — the largest single departure from DS5
anywhere in the Structured arc, and one made *because* the paper's own text demanded it, not despite the
paper. Instead: joint configuration entropy (`H_config`), macrostate concentration/persistence, a
susceptibility measure (completion-rate sensitivity to configuration), and a path-dependence test — direct
operationalizations of the paper's own named constructs (stability, susceptibility, path dependence)
using statistical rather than thermodynamic machinery.

### Assessment

**The most theory-faithful possible response to an explicit paper caution.** DS5's own StM notebook had
to carry a permanent "FLAG A: an approximation" caveat because its source paper did not itself warn
against the literal thermodynamic reading. Structured's paper does warn against it, and the implementation
respected that warning by not building the apparatus at all, rather than building it anyway with a caveat
attached. This is arguably a **stronger** theory-fidelity outcome than DS5's own StM, precisely because
the paper's own caution was followed rather than worked around.

**Two real design bugs, both caught by the notebook's own built-in chain-rule sanity check, both material
enough to change what counted as the "correct" microstate definition:** (1) a first draft defined the
microstate without completion status, then invalidly compared its entropy against InT's `H_completion`
marginal, producing 21/53 spurious chain-rule "violations" — fixed by including completion status
directly in `full_config`, matching the paper's own property list exactly. (2) even after that fix, 4/53
violations remained, traced to using a binary completed-vs-not flag against InT's *3-class*
`lifecycle_status` marginal — collapsing categories can only reduce entropy relative to a finer marginal.
Fixed by using the 3-class variable directly. **0 violations after both fixes**, across all 53 eligible
participants — a clean, verified result, but one that required two rounds of correction to reach, both
recorded honestly rather than only reporting the final clean number.

**Genuine null result, reported as such:** path dependence after repeated non-completion streaks — the
paper's own named "path-dependent changes after repeated unresolved tasks" phenotype — is **not
supported** (pooled `r=-0.022`, nominally significant but negligible effect size; within-participant
`r=-0.0018`, `p=0.85`). This null directly converges with GaT's own independent null on strategy
adaptation after rescheduling (see below) — two separately-built model families agreeing that this
dataset shows no evidence of tactical learning at the task-to-task level, a real (if negative) finding
worth stating in the paper rather than omitting.

**Approximation to note:** macrostate persistence (mean 0.953) is flagged in the notebook itself as likely
a ceiling effect (since `timed` already dominates 93–97% of activity per InT/NeT, there is rarely a viable
alternative type for the dominant label to shift to) — a self-aware caveat about over-interpreting a high
stability number, applied proactively rather than only after the fact.

---

## GaT — Game Theory

### Theory intended

Paper §2.6 (quoted in the blueprint), grouped explicitly by the paper's own §1.3 with StM under the same
proxy-definition caution: committed strategy (specific time, duration, alert, recurrence, subtasks) vs.
flexible strategy (inbox, all-day, low structure); "neither strategy is inherently better... the meaning
depends on the user's goals, task context, and later outcomes."

### What was implemented

**No formal game matrix, best-response analysis, or equilibrium concept** — the same discipline applied
to StM's thermodynamic apparatus, applied here to "payoff" and "utility." Instead: an explicit, named
`commitment_score` (0–5) proxy built strictly from the paper's own listed commitment signals (alerts
excluded, confirmed unavailable), and correlational outcome tests.

### Assessment

**Highly theory-faithful**, and the clearest empirical confirmation of the paper's own central GaT claim
anywhere in the Structured arc. The commitment-outcome relationship is genuinely **non-monotonic** —
completion peaks at moderate commitment (score 2, simply `timed` with nothing extra: 79.0%, verified in
`outputs/model_outputs/structured/game_theory/commitment_outcome_curve.csv`) and *declines* at maximum
commitment (score 5: 58.7%). This directly and literally confirms the paper's own sentence: "neither
strategy is inherently better... a timed task with an alert may represent a stronger commitment... but
also creates a higher expectation for execution." A single pooled linear correlation (`r=-0.0054`, n.s.)
would have completely missed this U-shaped relationship — the decision to report the binned curve as
primary evidence, made **before** running the analysis (verified against real data at blueprint-writing
time, not decided after seeing a null linear result), is a methodologically important choice that
correctly anticipated a nonlinear finding a linear default would have hidden.

**The SyD lesson applied proactively, not reactively:** the within-participant check (to rule out a
between-participant confound) was designed in from the start here, rather than discovered as a fix after
a suspicious pooled result — the trade-off curve's non-monotonic shape is confirmed to persist in the
demeaned population (`r=0.063, p=4.5×10⁻²⁵`, n=26,680), meaning the finding is not a between-participant
artifact.

**Genuine null result, converging with StM's:** strategy adaptation after rescheduling shows no
meaningful effect, pooled (`r=-0.003, p=0.78`) or within-participant (`r=0.011, p=0.25`) — this dataset
shows no evidence that rescheduling a task changes a user's subsequent commitment level, directly
paralleling StM's own null on path dependence after non-completion streaks.

**One real implementation bug, caught by cross-checking printed output against the generated summary
(not by a built-in assertion):** two unrelated within-participant correlation tests reused the same
variable names, so the auto-generated summary silently reported the second test's numbers under the
first test's heading. Caught by noticing a printed value didn't match the summary's value for what should
have been the same statistic — fixed by renaming variables.

---

## ABM — Agent-Based Modeling

### Theory intended

Paper §2.7 (quoted in the blueprint): heterogeneous users with simple, data-estimated behavioral rules;
"the value of ABM is that it can test whether simple local rules are sufficient to reproduce larger
observed patterns"; features from other models (entropy, burstiness, network centrality) can inform agent
rules or types; ABM as a test of whether phenotypes are "dynamically plausible."

### What was implemented

Two generative models — Model 1 (static-rate Poisson baseline, no temporal structure) and Model 2
(two-state session on/off, one added mechanism) — with every rule parameter read directly from already-
fitted StoP/Stage-1/Step-2 outputs, per the paper's own explicit instruction not to re-estimate from raw
data. A phenotype-mixture validation using Step 2's Profile A/B mean rules as two archetypal agent types.

### Assessment

**Highly theory-faithful in method; a mixed, honestly-reported result in outcome — directly comparable in
kind (though not in magnitude) to DS5's own ABM validation-gate failure.** Model 1's Fano≈1 result is
mathematically guaranteed (a Poisson process has Var=Mean by construction) and was run anyway specifically
to turn an abstract fact into a quantified gap (real Fano≈6.0 vs. simulated≈1.0) — a deliberate,
pre-stated design choice, not a wasted analysis. Model 2's single added mechanism (session clustering)
closes 47% of that gap and achieves a strong individual-agent rank correlation (`r=0.914` between real and
simulated Fano across agents) — the model identifies *which* agents are burstier than others very well.

**The phenotype-mixture test is the clearest theory-fidelity result in this family, and it is a genuine,
reported limitation, not a clean success.** The separation *magnitude* between Profile A and Profile B is
well reproduced (KS statistic 0.351 real vs. 0.375 simulated), but the *direction* is **reversed** (real:
A > B, 7.49 vs. 4.61; simulated: B > A, 5.04 vs. 4.60). This was caught by explicitly checking direction
rather than accepting the magnitude match at face value — collapsing each profile to a single mean rule
set loses enough within-profile heterogeneity to flip which group looks burstier. This is the same
qualitative failure mode as DS5's own ABM gate failure (a simple agent built from already-fitted
individual/phenotype parameters under-reproduces some real structure) and is explicitly named as a
"three independent failures of the same kind" pattern (alongside DS5 and DS4) in
`cross_dataset_cas_model_synthesis.md` §2.

**Two real implementation bugs, both caught before running by reviewing the simulation code rather than
its output:** a Markov transition probability (`p_on`) that could mathematically exceed 1.0 for
high-activity agents, fixed with proper clipping; and a non-reproducible RNG seed (Python's built-in
`hash()`, randomized per-process by default) for the phenotype-mixture simulation, fixed with a
deterministic seed mapping.

---

## Overall assessment: which families were theory-faithful vs. required departure from DS5's approach

| Model | Theory faithfulness | Primary approximation / departure | Should be defended in the paper? |
|---|---|---|---|
| NeT | **HIGH** | Self-loops included; no session-boundary filter; small state vocabulary bounds entropy/HHI magnitudes below DS5's — not directly comparable across datasets | Yes — note FLAG W4 (cross-dataset magnitude non-comparability) explicitly if NeT results are ever compared side by side with DS5 |
| InT | **HIGH** | 3 paper-named dimensions (alerts, category, energy level) unavailable in the export — a data gap, not an implementation gap; one power-imbalance caveat on the placement MI test | Yes — state the export-vs-codebook gap plainly; it affects InT, StM, and GaT identically |
| StoP | **HIGH** | Deliberate, well-justified non-port of DS5's proxy (count vs. rate); MoM estimation technique reused as a general tool only | Yes — the count-vs-rate distinction is worth a sentence explaining why DS5's SDE formula could not simply be reused |
| DyS | **HIGH** | Deliberate non-port (multi-dimensional weekly vector vs. DS5's 1D σ→0 reduction); `completed_share_w` mixes same-week composition with eventual-fate outcome | Yes — flag the same-week-vs-eventual-fate reading of "completed tasks" explicitly |
| SyD | **HIGH**, with one real correction | Person-mean-centering was *required*, not optional, to get the overload loop's predicted sign right; balancing loop does not replicate even after correction | **Requires explicit paper section** — a naive pooled reading would have wrongly falsified the paper's own overload-loop prediction |
| StM | **HIGH — arguably the strongest fidelity result in the whole arc** | No literal β/T/Z/F apparatus, following the paper's own explicit caution rather than working around it; path-dependence is a genuine null | Yes — the null on path dependence should be reported plainly, not omitted |
| GaT | **HIGH** | No formal game/equilibrium apparatus, matching the paper's own §1.3 caution (paired with StM); commitment index is an explicit proxy, not a utility function | Yes — the non-monotonic commitment-outcome curve is a strong, citable confirmation of the paper's own "neither strategy is inherently better" claim |
| ABM | **MODERATE** | Individual-rank reproduction strong; population-magnitude partial; 2-archetype direction reversed — same failure class as DS5's own ABM gate failure | Yes — report the direction reversal honestly, exactly as `model_run_summary.md` does; do not reframe the magnitude match as a full success |

---

## What should be explicitly added to the paper's own methods discussion, based on this comparison

1. **The count-vs-rate state-variable distinction (StoP)** — DS5's bounded-rate SDE formula is not a
   general template; Structured's own worked example independently justifies an unbounded-count Fano-
   factor approach instead. Worth a sentence contrasting the two state-variable types directly.
2. **The person-mean-centering correction (SyD, applied proactively in GaT and StM)** — without it, one
   of the paper's three named SyD loops (overload) would have been reported as falsified when it is
   actually supported once the between-participant volume confound is removed. This methodological point
   generalizes beyond SyD and is worth stating as a general panel-data caution in the paper's methods
   section, not just a Structured-specific footnote.
3. **The NeT–InT bridge identity** (`I_consec_state = H_state_marginal − H_trans`) and its correct-marginal
   requirement — not yet stated formally in the theory paper, and the same bug class recurred independently
   in two other datasets in this project (see `cross_dataset_cas_model_synthesis.md` §2), making it a
   cross-cutting methodological note worth generalizing in any combined write-up.
4. **The three structurally unavailable paper-promised dimensions** (task alerts, task category, energy
   level) — affecting InT, StM, and GaT identically. A single sentence in the paper's data-availability
   discussion would cover all three, rather than three separate per-family caveats.
5. **StM's and GaT's shared "no literal formal apparatus" decision** — both followed the paper's own §1.3
   caution rather than the DS5 precedent of building the apparatus with a flag attached. This is worth
   stating as a deliberate methodological choice, not an omission, since a reader familiar with DS5's StM
   might otherwise expect the same β/T/Z/F machinery here.

---

*Written 2026-08-08 as part of the Structured post-analysis waypoint, mirroring
`outputs/reports/stage4/post_analysis/theory_vs_implementation_comparison.md`.*
