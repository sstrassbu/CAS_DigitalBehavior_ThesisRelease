# Deferred/Excluded Models — DS4's SyD Exclusion, Explained and Compared to DS5

**Written:** 2026-08-08
**Overlap check:** Read in full before drafting — `outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md` and `outputs/reports/stage4/post_analysis/ds5_gat_abm_deferred_resolution.md` (DS5 templates; §4 of the latter is cited directly below per the task's own instruction, not re-derived), `outputs/reports/stage4/cross_dataset_implementation_strategy.md`, `outputs/reports/stage4/stage4_implementation_plan.md`, `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §0/§2 (SyD row). This document is scoped narrowly to DS4's own SyD exclusion and DS4's own (now-resolved) GaT/ABM deferral — not a re-statement of DS5's deferral reasoning, which followed a different logical path (DS5 deferred GaT/ABM pending phenotyping and deferred SyD pending a better-suited dataset; DS4 deferred GaT/ABM for the identical structural reason and later resolved it identically, but excludes SyD for a reason that has no DS5 parallel: DS4's own data can never satisfy SyD's requirement, not "not yet").
**Purpose:** State precisely why DS4 has 7/8 model families implemented and SyD is the one exclusion, whether this is permanent or revisitable, and how this compares to DS5's own SyD deferral.

---

## 1. Current status: 7 of 8 CAS model families implemented for DS4

| Family | Status | Notebook |
|---|---|---|
| StoP | Complete | 53 |
| InT | Complete | 52 |
| DyS | Complete | 55 |
| StM | Complete | 51 |
| NeT | Complete | 54 |
| GaT | Complete (originally deferred, later revisited — see §3) | 56 |
| ABM | Complete (originally deferred, later revisited — see §3) | 57 |
| **SyD** | **Excluded** | Not attempted; no notebook number reserved |

This is a different final shape from DS5, which also reached 7/8 (SyD deferred to DS6, all others including GaT/ABM eventually complete) — the numeric outcome (7/8) is the same, but the *kind* of gap is not: DS5's missing family was moved to a different dataset in the same active research program and has since actually been implemented there; DS4's missing family has no such destination.

---

## 2. Why SyD is excluded for DS4 — the precise, verified data constraint

System Dynamics, per this project's own established framing (`deferred_models_why_phenotyping_first.md` §2, written for DS5), requires **repeated within-person survey measurements** to identify a feedback-loop structure between psychosocial stocks (e.g., boredom, addiction pressure, self-control) and behavioral flows (app-opening events). The project's own stated minimum is "at least 3–4 measurement waves per person" or, at minimum, a genuine pre/post design with two waves (DS5's own SyD deferral was made even though DS5 *did* have two waves, because two waves were judged insufficient — see §4 below).

**DS4's actual survey structure, verified directly against its cleaning and feature documentation:**

- **One survey wave only**, administered **after** participants had already been using OneSec for an extended period (`outputs/cleaned/ds4_survey_clean.md`: "The survey was administered after participants had been using the OneSec friction app for an extended period... There is no pre-survey — this is post-use only; no pre/post comparison possible within DS4.")
- **299 total respondents, 283 linkable to behavioral data** (of 1,039 total behavioral participants — 756 have no survey data of any kind).
- **Zero psychometric/Likert scales exist in the survey at all.** Every substantive survey column (`reason_use`, `benefits`, `negatives`, `usage_format`) is open-ended qualitative text, not a validated scale (`outputs/features/ds4/ds4_features.md`: "DS4's survey contains ONLY open-text qualitative responses. No Likert scales exist.").

This means DS4 does not merely fall short of SyD's "3–4 waves" ideal — it has **zero** waves of any quantitative psychosocial measure, and **zero** possibility of constructing a pre/post comparison at all, since there is no "pre" survey to compare a "post" survey against. DS4 is structurally further from SyD-readiness than DS5 was (DS5 had two real waves of validated Likert scales; DS4 has one wave of qualitative text). SyD's core mechanism — a stock (psychosocial state) changing in response to, or driving, a flow (behavior) — has no quantitative stock variable to build on in DS4 at all, independent of the wave-count question.

**This is confirmed as the intended reading of the exclusion, not an inference made for this document:** `ds4_abm_blueprint.md` (written 2026-08-07, when ABM was being revisited after DS4 Step 2 completed) states directly: *"This is the last of the originally-excluded DS4 families to be revisited (SyD stays excluded — DS4 has no repeated survey waves, a hard data constraint unrelated to phenotyping)."* The phrase "hard data constraint" is DS4's own project documentation's characterization, not an interpretation added here.

---

## 3. GaT and ABM were also originally excluded for DS4 — and were later resolved, unlike SyD

It is important not to conflate SyD's exclusion with GaT/ABM's *original* exclusion, since all three initially appear together in early DS4 planning documents (`ds4_stm_blueprint.md` §14, obsolete section: "For GaT (46), ABM (47), SyD (48): These remain deferred... SyD remains deferred to DS6" — note this section was written 2026-04-17 using DS5's own notebook numbers as a placeholder, before DS4's own 50s-decade numbering was locked in, and is explicitly marked obsolete in the blueprint itself).

**GaT and ABM's original exclusion reason was structural but temporary** — both explicitly required DS4's own Step 2 phenotyping output as an input (`ds4_abm_blueprint.md` §1: "ABM was excluded because it 'needs DS4 Step 2 phenotyping output' as agent inputs. Step 2 (Phase 1 + Paths A′/C′/F′) is now complete... that blocking condition no longer holds."). Once DS4 Step 2 finished (2026-08-06), both were revisited and implemented the same arc (2026-08-06/07), exactly mirroring DS5's own GaT/ABM resolution timeline.

**SyD's exclusion reason is a different kind of constraint entirely — not resolved by Step 2, and not resolvable by anything internal to the DS4 pipeline.** GaT and ABM were blocked on *work not yet done* (phenotyping); SyD is blocked on *data that does not exist and cannot be produced from what does exist*. Completing DS4 Step 2, Step 3, or any further internal analysis has no bearing on whether DS4 will ever have repeated psychosocial survey waves — it will not, because DS4 is a fixed, already-collected retrospective dataset (see §5).

---

## 4. Comparison to DS5's own SyD deferral

Per the DS5 template this document is instructed to cite rather than re-derive (`ds5_gat_abm_deferred_resolution.md` §4):

> "`deferred_models_why_phenotyping_first.md` §2 deferred System Dynamics (SyD) to DS6 for a structural reason unrelated to phenotyping: DS5 has only two survey waves (pre/post), and SyD needs at least 3–4 waves to identify a feedback-loop structure. This reasoning has since been confirmed correct and acted on: DS6's SyD notebook (`78_ds6_system_dynamics.ipynb`) was implemented and completed on 2026-08-06, using `addiction_index_change` and `self_control_index_change` as formal stock quantities — exactly the kind of repeated-wave psychosocial measurement DS5 lacks. DS6's SyD result was a genuine null (both feedback-loop hypotheses non-significant after regression-to-the-mean control), which does not bear on whether the deferral reasoning itself was sound — it was, and the dataset match (DS6 over DS5) was the correct call."

**The structural difference between DS5's and DS4's SyD exclusions:**

| | DS5 | DS4 |
|---|---|---|
| Survey waves | 2 (pre + post) | 1 (post-use only) |
| Scale type | Validated Likert (FoMO, belonging, ostracism, digital wellbeing) | None — open-text qualitative only |
| Was a quantitative psychosocial "stock" variable available at all? | Yes (pre/post change scores exist, e.g. `belong_change`, `fomo_change`) — just not enough waves for a full feedback-loop model | No — no quantitative psychosocial variable exists in DS4 at any wave count |
| Was there another dataset in the same active research program with the needed design? | **Yes — DS6**, which has 2+ survey waves (`survey_nr` 1/2) with validated `addiction_index`/`self_control_index` scales, and SyD has since been implemented there | **No** — no other DS1/DS4/DS5/DS6 dataset shares DS4's specific naturalistic, long-window, no-condition design; DS4's own gap cannot be filled by "moving SyD to a sibling dataset" the way DS5's was |
| Nature of the exclusion | **Deferred** — pending the correct dataset, which existed in the project's own planned sequence (`stage4_implementation_plan.md`'s DS5→DS4→DS6→DS1 order) | **Excluded** — DS4 itself is retrospective, already-collected historic data; there is no future DS4 data collection wave that could add the missing survey structure |

**The key distinction to state plainly, since the task requires it:** DS5's SyD gap was a **"deferred, with a path forward"** situation — the reasoning explicitly named a specific other dataset (DS6) that could satisfy the requirement, and that dataset was later used exactly as planned. DS4's SyD gap is a **permanent exclusion for this dataset specifically** — not because DS4 is unimportant to the project's SyD ambitions, but because DS4's own data collection is closed and retrospective (a one-time historic export, not an ongoing study), so no future wave of DS4 survey data will ever arrive to fill the gap. If SyD is ever desired for a DS4-*like* dataset (naturalistic, long-window, no experimental condition), it would require locating or collecting an entirely different dataset with that profile plus repeated psychosocial waves — DS4 itself cannot be revisited to supply this, unlike DS5's gap, which was always going to be filled by continuing the project's existing dataset sequence rather than requiring a wholly new data source.

---

## 5. Is this exclusion truly permanent, or could DS4 support a weaker/partial SyD analysis?

Worth stating honestly rather than treating "excluded" as an unexamined final word: a few weaker alternatives were considered implicitly by this project's own documentation and are worth naming explicitly here, each with why it does not actually resolve the exclusion.

- **Could a single wave + a behavioral proxy for "prior state" substitute for a second wave?** No natural candidate exists. DS5's SyD-adjacent analyses (and DS6's actual SyD implementation) both used a genuine second measurement of a psychosocial construct as the "before" state; DS4 has no first-wave psychosocial measurement of any kind to pair even a single post-use wave against.
- **Could behavioral-only stocks and flows (e.g., a "backlog" or "activity persistence" analog, as Structured's own SyD notebook did) work instead?** This is the one genuinely open door, and it is worth flagging precisely because it does not require survey data at all — Structured's own SyD notebook (`68_structured_system_dynamics.ipynb`) built its stock-flow model entirely from behavioral quantities (a task backlog), explicitly checked for non-redundancy against other completed model families first. DS4 was **not** checked for a behavioral-only SyD candidate before being excluded — the exclusion documented across DS4's blueprints is specifically about the *psychosocial* feedback-loop framing SyD's paper section names (§2.8, per the DS6 precedent), not an exhaustive test of every possible SyD operationalization. This is a genuine, stated gap in DS4's own exclusion reasoning, not a hidden option — if a future session wants to revisit DS4 SyD, the behavioral-only-stock route (following Structured's precedent, checked for redundancy against DS4's own already-completed StoP/DyS/NeT outputs first) is the one path not yet ruled out by anything in DS4's existing documentation.
- **Could the qualitative survey text (`reason_use`, `benefits`, `negatives`) be NLP-coded into a quantitative proxy and used as a single "state" measurement?** `ds4_features.md` explicitly flags these columns as "available for future NLP-based extraction but... NOT numerically featurized here." Even if coded, this would still be a single wave — useful as a cross-sectional covariate, but not sufic to construct a feedback loop (which requires observing a stock changing over time in response to a flow, or vice versa).

**Conclusion:** the psychosocial-feedback-loop version of SyD (matching the paper's own framing, and matching how SyD was actually implemented for DS6) is permanently excluded for DS4 — no amount of further DS4-internal analysis can produce the repeated psychosocial measurement this specific model family's paper-motivated framing requires. A **behavioral-only** stock-flow SyD variant, following Structured's own precedent, remains a genuinely open (not yet attempted, not yet ruled out) possibility for DS4 specifically — this project's documentation has not tested and rejected it, only the survey-dependent version.

---

## Source documents

- `outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md` (DS5 template)
- `outputs/reports/stage4/post_analysis/ds5_gat_abm_deferred_resolution.md` §4 (cited directly, per task instruction)
- `outputs/reports/stage4/step1_modeling/ds4_abm_blueprint.md` §1 (source of the "hard data constraint" phrase)
- `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md` §14 (obsolete original deferral note)
- `outputs/reports/stage4/step1_modeling/ds4_gat_blueprint.md` §1
- `outputs/cleaned/ds4_survey_clean.md`
- `outputs/features/ds4/ds4_features.md`
- `outputs/reports/stage4/cross_dataset_implementation_strategy.md`
- `outputs/reports/stage4/stage4_implementation_plan.md`
- `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §0, §2 (SyD row)

---

*Written 2026-08-08 as part of the DS4 post-analysis synthesis, mirroring the DS5 template (`outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md`).*
