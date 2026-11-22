# Structured — Retrospective Dataset Audit

**Status:** Inspection, cleaning, and Stage 1 feature extraction complete (2026-08-03). **Update
(2026-08-05): modeling is now also complete** — all 8 CAS model families (Step 1) plus phenotyping and
a 4-path exploration (Step 2) have since been implemented; see `structured_cas_modeling_plan.md` for the
full, actively-maintained status log and `structured_step2_master_synthesis.md` for the Step 2 synthesis.
This document itself remains scoped to inspection/cleaning/Stage 1 findings and is not being extended
further. Feature extraction (`notebooks/17_structured_feature_extraction.ipynb`,
`outputs/features/structured/`) surfaced one important structural finding not visible during inspection:
**60.7% of tasks are left-censored** (no visible `Task Created` event — pre-existing tasks from before
the extraction window). See §6 below and `structured_cas_modeling_plan.md` §3.1 for the full implication.
**Producing notebooks:** `notebooks/15_structured_inspection.ipynb`, `notebooks/16_structured_cleaning.ipynb`
**Cleaned outputs:** `outputs/cleaned/structured_behavioral_clean.csv`, `structured_survey_clean.csv`, `structured_participant_linkage.csv` (each with a companion `.md`)

---

## 1. What this dataset is

This is a **new dataset category, not part of the DS1–DS6 OneSec series**. It comes from *Structured*,
a digital task-planning / calendar app (Heidelberg University study, run in collaboration with
`unorderly.io`), not from OneSec's smartphone-friction intervention product. The behavioral object is
**task planning** (creating, scheduling, editing, completing, deleting tasks), not app-opening friction.

Two raw files, both dated 2026-07-22:
- `retro_behavioraldata_2026_07_22.csv` — PostHog-logged task lifecycle events (53,686 rows)
- `retro_surveydata_2026_07_22.csv` — Qualtrics intake survey (117 responses)

Plus one partial codebook PDF: `Retrospective_Study_Structured_Task_Created.pdf` (3 pages, documents
only the `Task Created` event schema — `Task Updated` and `Task Deleted` have no codebook coverage).

The theoretical framing for this dataset lives in `data_docs/pdfs/Structured Planning as a Complex
Adaptive System.pdf`, which proposes applying all eight CAS model families used elsewhere in this
project (StM, DyS, StoP, NeT, InT, GaT, ABM, SyD) to digital planning behavior. See the companion
report `structured_cas_modeling_plan.md` for the full theory-vs-data feasibility analysis.

---

## 2. Units of observation

| File | Unit | Rows |
|---|---|---|
| Behavioral | one task-lifecycle event (created / updated / deleted) | 53,686 |
| Survey | one Qualtrics intake response | 117 (119 raw rows incl. 2 Qualtrics header rows) |

`task_id` is stable across a task's full lifetime and is never shared across participants — grouping by
`task_id` reconstructs each task's individual lifecycle (this is the key structural asset for Network
Theory / lifecycle modeling; see the CAS plan report).

---

## 3. Participant structure

- 61 unique participants have behavioral (app-use) data.
- 117 unique participants completed or attempted the survey.
- **All 61 behavioral participants have a matching survey record** (in_behavioral ⊆ in_survey — no orphaned behavioral data).
- 56 participants are survey-only (no linked behavioral data) — either inactive during the extraction window, or not linked/exported.
- Activity span per behavioral participant: median 132 days, 9 participants <7 days, 39 participants ≥90 days. Consent text describes a "last three months" extraction window; observed span is closer to 4.75 months (2026-03-01 to 2026-07-22) — a minor scope discrepancy, not a data defect.

---

## 4. Data quality findings

### Confirmed clean
- Zero duplicate rows in either file.
- Zero parse failures for any timestamp column once `format="mixed"` is used (source mixes fractional- and whole-second precision).
- `task_id` never shared across participants (referential integrity holds).
- **Consent gating verified correct**: none of the 6 explicit non-consenters, nor the 38 respondents who never answered the consent question, appear in the behavioral file. This is an important governance check that passed — analogous to the PII check performed for the Stanford Health dataset in this project.

### Ambiguities / limitations flagged (not resolved by cleaning alone)
1. **`task_name` is 100% empty**, despite the Qualtrics consent text explicitly stating that "task titles" are among the collected fields. Dropped from the cleaned file. Flagged as a consent-text/export mismatch for awareness — not something this preprocessing step can resolve.
2. **No codebook exists for `Task Updated` / `Task Deleted` event schemas** — only `Task Created` is documented (3-page PDF). Column semantics for the other two event types were reverse-engineered from the data (e.g. `update_type` encoding).
3. **`update_type` has a distinct empty-array value** (`"[]"`, 1,607 rows) separate from NaN (12,968 rows, the Created/Deleted events). The empty-array case — an Updated event firing with no field-level change captured — has no documented explanation.
4. **No separate codebook exists for the survey.** Column meanings were reconstructed entirely from the embedded Qualtrics question-text row (preserved in the companion `.md`).
5. **ASRS-6 items are missing beyond the base non-completion rate** (54.7% vs. ~40–44% elsewhere) — suggests additional skip logic (possibly tied to the autism/ADHD screening questions) that no available document explains.
6. **`is_finished` is not a reliable "usable response" filter** — all 6 explicit non-consenters also show `Finished = True` / `Progress = 100`, because the survey flow routes decliners straight to the end. Only `consent_given & is_finished` together (65/117) identifies genuinely analyzable responses.
7. **`subscription_type` changes mid-study for 5/61 participants** — must be treated as time-varying, not a static demographic, in any downstream feature work.

---

## 5. Cleaning steps applied (summary)

See `outputs/cleaned/structured_behavioral_clean.md` and `structured_survey_clean.md` for full detail.

**Behavioral:**
- Mixed-precision timestamp parsing (`format="mixed"`) for `event_timestamp`, `task_start_at`, `task_end_at`
- `update_type` parsed from mixed JSON-array/bare-string encoding into a list + change-count + empty-flag
- Dropped `task_name` (100% empty)
- Renamed `user_id`→`participant_id`, `event`→`event_type`, `task_duration`→`task_duration_min`, `subscription_type`→`subscription_type_at_event`
- Derived `days_since_first_event` per participant

**Survey:**
- Dropped 2-row Qualtrics header (question text + ImportId JSON)
- Renamed 30 `Qxx` columns to descriptive names; question text preserved as the empirical codebook
- Cast metadata and demographic fields to numeric/boolean; extracted numeric grade from Likert-labeled text and percentage strings
- Ordinally recoded ASRS-6 items 0–4 (not official clinical scoring — deferred)
- **No rows deleted** for non-consent or non-completion — `consent_given` / `is_finished` flags provided instead, so provenance is preserved and filtering is explicit and auditable downstream

**Linkage:**
- One row per unique participant across both files, with overlap flags and a per-participant behavioral summary (event counts by type, unique task count, observed days, last-known subscription tier)

---

## 6. Relevance for later modeling

This dataset is structurally richer than the theory paper's own baseline assumption. The CAS-for-Structured
paper (`Structured Planning as a Complex Adaptive System.pdf`, §1.3) explicitly distinguishes a "weaker"
scenario where only `Task Created` data is available from a "full value" scenario requiring
update/movement/rescheduling/completion events for Network Theory. **This export already has the full
three-class lifecycle** (Created/Updated/Deleted with detailed `update_type`), which is the stronger case
the paper anticipated, not the weaker one. See `structured_cas_modeling_plan.md` for the detailed
per-model feasibility assessment and open construct-mapping questions.

---

## 7. Progress update (2026-08-03)

- Stage 1 feature extraction: **complete** (`notebooks/17_structured_feature_extraction.ipynb`,
  `outputs/features/structured/`) — see `structured_cas_modeling_plan.md` status update for the
  left-censoring finding this surfaced.
- Network Theory (NeT), the first model family: **complete** (`notebooks/64_structured_network_theory.ipynb`,
  blueprint `structured_net_blueprint.md`, outputs `outputs/model_outputs/structured/network_theory/`).

## 8. Next steps (as of 2026-08-03; superseded — see below)

1. Information Theory (InT) — next per the modeling plan's proposed order (§6); no dependency, cheap
2. Stochastic Processes (StoP) — daily/weekly planning trajectories; required before DyS/StM
3. Construct mapping table for Structured-specific theoretical constructs (planning stability, override/reschedule tendency, overload) — see CAS plan report §4
4. Cross-dataset comparison: is Structured planning behavior comparable to OneSec friction behavior on any shared dimension (e.g. entropy, network centralization), or should it be treated as fully independent per this project's "no forced harmonization" principle?
5. Confirm survey subgroup sizes are usable before committing to any psychosocial correlate analysis (only 65/117 responses are fully consented + finished)

**Superseded (2026-08-05):** items 1–2 above are complete, along with all remaining model families (DyS,
SyD, StM, GaT, ABM) and Step 2 phenotyping (single pass + 4-path exploration). Item 3 (construct mapping)
is addressed inline throughout each model blueprint rather than as a standalone table. Item 4
(cross-dataset comparison) has not been pursued — Structured continues to be treated as fully independent
per the "no forced harmonization" principle, consistent with how it has been implemented throughout. Item
5 was addressed: psychosocial overlays were run at N=33 (Step 2 Phase 1) and found mostly null, consistent
with DS5's own experience at much larger N. See `structured_cas_modeling_plan.md` for the complete,
chronologically-maintained record of everything that has happened since this document was last extended.
