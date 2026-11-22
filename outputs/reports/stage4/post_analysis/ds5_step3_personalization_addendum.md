# Step 3 (Personalization) — Addendum to the Data Usage Map

**Written:** 2026-08-07
**Purpose:** `model_data_usage_map.md` (2026-04-20) documents data provenance for every DS5
Step 1 model family and every Step 2 phenotyping path, but predates Step 3 by roughly four
months — Step 3 did not exist as a concept in this project until
`outputs/reports/stage4/step3_personalization/ds5_step3_personalization_blueprint.md`
(2026-08-07). This is a short, narrow addendum: one new data-usage row, and one specific
historiographical finding worth recording that isn't captured elsewhere. It is deliberately
**not** a restatement of Step 3's methods or results — those are already documented
end-to-end, and in more depth, in `outputs/reports/paper_prep/ds5_personalization_paper_prep.md`
and in `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §3.

---

## 1. Step 3 data usage — the missing row

| Step/Path | Behavioral events | Survey data | Previous model outputs | Notes |
|---|---|---|---|---|
| **Step 3 (`200_ds5_personalization_exploration.ipynb`)** | No | study_condition (essential — the interaction term's second factor) | NetC moderator (`HHI_net`, `rho_self`, `H_trans`, `H_app` — pre-existing NeT output); three candidate outcomes: `x_mean`, `commitment_score` (StoP/GaT), `chi_behav` (StM) | Entirely derived from Step 1 model outputs plus condition; no raw events or new survey fields used |

This fits the same pattern `model_data_usage_map.md` §"What is truly behavior-derived vs
questionnaire-dependent" already established for Path E/B: study_condition is essential to
the analysis structure (Step 3's whole question is a phenotype × condition interaction), not
an overlay. Nothing here required extending that document's own conclusions — it slots into
the existing framework cleanly.

---

## 2. A small historiographical finding: the original data usage map had this right; a later document got it wrong; the notebook caught it

`model_data_usage_map.md` §"Phase 1 — Global Phenotyping" (written 2026-04-20) already states
correctly: "Primary data sources: All 5 model outputs merged at participant level (StoP, InT,
DyS, StM, NeT parameter files)." That is accurate — `profile_p1` was in fact built from five
features (`sig_hat`, `H_emp`, `x_mean`, `HHI_net`, `rho_self`), not from the two NeT features
alone.

Four months later, the Step 3 blueprint's own §4 restated `profile_p1`'s construction
incorrectly, as "built from `HHI_net`/`rho_self` only" — a simplification that, if taken at
face value, would have made `profile_p1` look safe to use as an outcome-feature-free
moderator. It is not: `x_mean` (which entered `profile_p1`'s own construction and its
ascending-`x_mean` naming convention) correlates −0.98 with `commitment_score`, one of the
three candidate Step 3 outcomes, and `chi_behav` is deterministic in `sig_hat` and `x_mean`,
both of which also entered `profile_p1`. Using `profile_p1` as-is would have meant testing
whether a moderator built partly *from* an outcome predicts that same outcome — a leakage
problem, not a substantive finding.

The executed notebook (`200_ds5_personalization_exploration.ipynb`) checked the blueprint's
premise directly against the actual construction code rather than trusting the blueprint's
restatement, found the discrepancy, and corrected course mid-implementation by building a
genuinely outcome-free alternative moderator (NetC — a NeT-only "distributed vs. hub-locked"
split using only `HHI_net`/`rho_self`/`H_trans`/`H_app`, cross-validated at ARI=1.00 against
an independently-built strict two-feature clustering). This is already recorded as a
project-level lesson in `cross_dataset_cas_model_synthesis.md` §3 ("a blueprint's stated
'this feature is safe because X' claim should be re-verified computationally during
implementation").

What is worth adding here specifically: **the original Step 2-era post_analysis
documentation (this file's own `model_data_usage_map.md`) never contained the error.** The
mistake was introduced later, in a planning document written to summarize earlier work, not
in the earlier work itself or in this document. The practical implication for how this
project's documentation should be used going forward: when a later blueprint restates a
fact about an earlier model's construction, the earlier model's own original documentation
(here, `model_data_usage_map.md`) is the more reliable source to check against — not the
other way around. This is a narrow but concrete instance of a broader documentation-hygiene
principle already implicit in this project's practices (e.g., the 2026-08-07 documentation
audit's own finding that "planning docs and blueprints frozen at an earlier project stage"
are a recurring source of staleness), now demonstrated with a specific example where the
staleness could have caused a real analytical error had the notebook not checked it.

---

*Written 2026-08-07 as part of the DS5 post-analysis update, alongside
`ds5_gat_abm_deferred_resolution.md` and `ds5_v2_revision_and_phenotype_addendum.md`. Full
Step 3 methods/results: `outputs/reports/paper_prep/ds5_personalization_paper_prep.md`.
Full cross-dataset Step 3 discussion: `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §3, §5.*
