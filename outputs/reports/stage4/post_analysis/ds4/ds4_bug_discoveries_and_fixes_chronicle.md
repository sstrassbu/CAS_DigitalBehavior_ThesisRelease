# Bug Discoveries and Fixes Chronicle — DS4

**Written:** 2026-08-08
**Overlap check:** Read in full before drafting — `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §2 (already references the DS4 `rho_self`/`app_close_event` finding and the ABM number error at a cross-dataset summary level; this document gives the full technical detail behind both, plus a third bug not mentioned there), `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` item 1 (source of the corrected ABM number, re-verified here directly against the current companion file rather than trusted from the audit note). This document consolidates three genuine, non-trivial bugs caught and fixed during DS4's own implementation and documentation — the task's threshold for producing this optional file (3+) is met.
**Purpose:** Give full technical detail — what was wrong, how it was caught, what was fixed, whether any headline number changed — for every real bug found in DS4's Step 1/Step 2 build, in one place.

---

## Bug 1 — NeT self-transition rate inflated by a logging artifact (`app_close_event`)

**Where:** `54_ds4_network_models.ipynb`, caught during blueprint verification, before the notebook's final construction was written (`ds4_net_blueprint.md` §1).

**What was wrong:** DS5's NeT notebook built its app-transition sequence from "all valid outcomes," because DS5 has a single event class where every row is a genuine attempt to engage with an app. Applying that same rule unmodified to DS4 — pooling all three of DS4's event classes (`intervention_event`, `app_close_event`, `no_intervention`) into one timestamp-ordered sequence — produces `rho_self = 0.743`.

**How it was caught:** the naive pooled number was broken down by class-pair transition before being accepted. An `intervention_event` row immediately followed by an `app_close_event` row showed `rho_self = 0.959` on that specific pair type alone (n=348,028 such pairs) — a near-universal "self-transition." This is not plausible as genuine habitual repetition; it was recognized as the mechanical signature of DS4's own logging architecture: friction is shown on app X (an `intervention_event` row), and the very next logged row is simply that same session's own close event (`app_close_event`) — not a new engagement attempt at all.

**Root cause:** `app_close_event` (47.1% of all DS4 rows) is not a new attempt to open an app; it is the closing tail of a session whose opening was already logged as a separate row. Including it in the transition sequence manufactures artificial self-transitions at the rate sessions naturally close (i.e., almost always), inflating `rho_self` for a reason that has nothing to do with real behavioral habit strength.

**Fix:** restrict the NeT sequence to attempt rows only (`intervention_event_class` in `{intervention_event, no_intervention}`), excluding `app_close_event` entirely. This is a different restriction from the one used by StoP/InT/DyS/StM (`intervention_event` class only) — NeT specifically needs `no_intervention`'s genuine opens/dismissals too, since no close-tail artifact needs excluding there.

**Numbers, before and after:**

| Construction | `rho_self` |
|---|---|
| Naive: pool all 3 event classes | 0.743 |
| `intervention_event` class only (not used — loses `no_intervention`'s real opens) | 0.631 |
| **Attempt rows only (used)** | **0.624** (median across the 950 eligible participants: 0.680) |

**Did a headline number change?** Yes, substantially — the difference between 0.743 and 0.624 is a ~16% relative reduction, not a rounding difference, and it is the number reported everywhere downstream (Phase 1 phenotyping's `rho_self` feature, Path C′'s clustering, GaT's construction notes). Because this was caught during blueprint verification rather than after a notebook run, no output file was ever produced with the wrong number — but had it not been caught, every DS4 network-topology-derived phenotype result would have inherited an artificially inflated self-transition signal.

**Cross-dataset context:** the cross-dataset synthesis already records this finding in one sentence (`cross_dataset_cas_model_synthesis.md` §2, NeT section: "DS4's `app_close_event` inflating `rho_self` to 0.96 before being excluded (true value 0.62–0.68)") — the "0.96" figure there is the specific `intervention_event`→`app_close_event` class-pair rate (0.959), not the naive whole-sequence pooled rate (0.743); this document distinguishes the two numbers precisely since they answer slightly different questions (one class-pair's self-transition rate vs. the whole-sequence aggregate rate) and both appear in the source blueprint.

---

## Bug 2 — NeT-InT bridge (`I_consec`) computed on the wrong marginal population

**Where:** `54_ds4_network_models.ipynb`, caught mid-implementation via a mandatory sanity gate (`I_consec >= 0`), documented in `model_run_summary.md` and `participant_network_metrics.md`.

**What was wrong:** the InT-NeT mutual-information bridge is defined as `I_consec = H_app − H_trans` (app entropy minus conditional transition entropy) — this quantity is mathematically guaranteed to be ≥ 0 for a true `H(Y) − H(Y|X)` (mutual information cannot be negative). The first implementation computed it as InT's own `H_app` (already available in `ds4_information_theory/participant_entropy_metrics.csv`) minus NeT's freshly-computed `H_trans`. This produced **138 of 950 (14.5%) negative values**, with a minimum of −0.631 bits — mathematically impossible for a genuine mutual information.

**How it was caught:** the mandatory `I_consec ≥ 0` gate, applied before trusting any bridge result (the same discipline this project has applied to every InT-NeT bridge since Structured's own version of this exact bug class was first found).

**Root cause, verified concretely on one real participant** (`<participant-id>`): InT's `H_app` is computed over **all** of that participant's events, including `app_close_event` rows. This participant had 647 `app_close_event` rows, 98% of which were the same app (reddit) — dragging their all-events `H_app` down to 0.86 bits. But their 158 real attempt rows (the population NeT's own `H_trans` is built from) were far more diverse, giving `H_trans = 1.49` bits on that same attempts-only population. Because `H_app` and `H_trans` were computed over two different populations (all events vs. attempts-only), the identity `I_consec = H_app − H_trans ≥ 0` — which only holds when both terms describe the same underlying joint distribution — no longer holds; `H_app` was smaller than `H_trans` for this and 137 other participants, producing an impossible negative value.

**Fix:** compute `H_app_attempts` — the current-app marginal entropy **within the exact same attempts-only, top-20-app-encoded population `H_trans` is built from** — instead of reusing InT's differently-scoped `H_app`. This is a fresh, in-notebook computation, not a reuse of InT's output for this specific bridge (NeT still keeps InT's original `H_app` in the output file, renamed `H_app_all_events`, "for reference only... NOT the bridge partner").

**Numbers, before and after:**

| Version | Negative `I_consec` count (of 950 eligible) | Minimum value |
|---|---|---|
| Buggy (InT's all-events `H_app` − `H_trans`) | 138 (14.5%) | −0.631 bits |
| **Fixed (`H_app_attempts` − `H_trans`)** | **0 (0%)** | ≥0 for all 950 |

The buggy count is deliberately preserved in the output file under the column name `n_Iconsec_negative_naive_buggy_version` — "kept for the record" per `ds4_net_summary.md` — rather than deleted from the historical trace once fixed.

**Did a headline number change?** Yes — `I_consec` itself (median 0.079 bits in the final, correct version) did not exist in a trustworthy form before the fix; 14.5% of the eligible population would have had a nonsensical negative value in any downstream use (e.g., as a Path C′ clustering feature, where `I_consec` is one of only two features used). Since Path C′ was built using the corrected values, this bug was fully resolved before it could propagate into Step 2.

**Cross-dataset context:** this is explicitly the same bug class already on record for Structured's own NeT-InT bridge (wrong-marginal-population mismatch) and for DS6's own version of the same bug (source vs. destination marginal mismatch). The cross-dataset synthesis (`cross_dataset_cas_model_synthesis.md` §2, InT section) already names this as "the single most-repeated lesson in the project's own build history" — DS4 is the third independent dataset to hit this exact bug class, each time caught by the same mandatory non-negativity gate rather than avoided by applying the lesson pre-emptively. Worth stating plainly rather than glossing over: even with two prior, well-documented instances of this exact bug class already on record elsewhere in this project by the time DS4's NeT notebook was built, the bug still had to be independently re-discovered here rather than pre-empted by reading the existing lesson first.

---

## Bug 3 — ABM documentation reported the wrong population for a headline percentage (113/641 vs. 133/641)

**Where:** `outputs/model_outputs/ds4_agent_based/participant_abm_simulation_results.md`, caught during the 2026-08-07 full documentation audit (`outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` item 1), re-verified directly against the current file for this document.

**What was wrong:** the companion doc's headline text originally stated "113/641 (17.6%) of Model 1's simulated series produce a valid weekly refit at all." The true count of Model 1 series with **any** valid mean-reverting weekly refit is **133/641 (20.7%)**.

**How it was caught:** the 2026-08-07 documentation audit cross-checked every headline number in every companion `.md` against its source CSV rather than trusting prose that had already been written once. The discrepancy was traced to a population-scope confusion, not a computation error: `abm_model_comparison_summary.csv`'s own `n` column (113 for `model1_pure_OU`) is the count of simulated series with **both** a valid daily refit **and** a valid weekly refit — the stricter population required for the daily-vs-weekly correlation/ratio statistics reported alongside it. This is a different, smaller population than "valid weekly refit at all" (133), which does not require the daily refit to also be valid.

**Root cause of why this was easy to miss:** for **real** participants, these two counts are identical by construction — the real daily OU refit is valid 100% of the time for anyone in the eligible population (since `fit_valid` was already required to be a member of this analysis population upstream, in StoP), so "valid weekly refit at all" (291) and "valid on both daily and weekly" (291) coincide exactly for the real data (291=291). For **Model 1's simulated** series, this coincidence breaks down: only 549 of 641 (85.6%) of simulated daily refits themselves converge to a valid mean-reverting fit, so the "both valid" population (113) is smaller than the "weekly valid at all" population (133). Whoever wrote the original headline sentence appears to have used the real-data intuition (where the two counts are always equal) and applied the `n=113` figure from the comparison table to a claim about "weekly-valid at all," where the correct figure was 133.

**Fix:** `participant_abm_simulation_results.md` now states the corrected 133/641 (20.7%) figure as the primary claim, with an explicit reconciliation note explaining why 113 also appears (correctly) elsewhere in the same file, for a different, narrower population.

**Did a headline number change?** The percentage stated in prose changed (17.6% → 20.7%), but **no underlying computation, model comparison, or substantive conclusion changed** — this was a documentation-labeling bug, not a computation bug. The ABM's real headline finding (neither Model 1 nor Model 2 reproduces the real daily-weekly divergence direction; both invert it) is unaffected by which of the two correctly-computed-but-differently-scoped counts is quoted in the summary prose.

**A methodological note worth preserving:** this bug is a variant of a broader pattern already on record in this project — a statistic that is trivially true or coincidental in one population (real data, where two counts are always equal) silently stops being trivially true in a second population (simulated data, where they diverge) without anyone noticing the underlying assumption had quietly stopped holding. This is conceptually adjacent to (though not identical to) the `NaN >= threshold` pandas-evaluates-to-`False`-not-`NaN` bug class already on record for DS6's own documentation audit — both are cases where a comparison or count that is well-behaved on the "easy" population (real/valid data) silently misbehaves on a "harder" population (simulated/NaN-containing data) without an explicit check catching the divergence until an independent cross-check was run.

---

## Summary table

| # | Bug | Model family | When caught | Headline number affected? | Same class as a prior project bug? |
|---|---|---|---|---|---|
| 1 | `rho_self` inflated by including `app_close_event` in the transition sequence | NeT | During blueprint verification, before notebook build | Yes — 0.743 (naive) vs. 0.624 (correct), ~16% relative difference | New pattern for this project (a close-tail logging class, not seen in DS5/DS6/Structured) |
| 2 | `I_consec` computed on mismatched marginal populations (all-events `H_app` vs. attempts-only `H_trans`) | NeT (InT bridge) | Mid-implementation, via mandatory `I_consec≥0` gate | Yes — 138/950 (14.5%) impossible negative values before the fix, 0 after | Yes — same class as Structured's and DS6's own NeT-InT bridge bugs |
| 3 | ABM companion doc quoted the wrong population's count for a headline percentage (113 vs. 133 of 641) | ABM | 2026-08-07 documentation audit (post-implementation) | Prose percentage only (17.6%→20.7%); no computation changed | Loosely related to the DS6 `NaN>=threshold` labeling-bug class (a comparison silently misbehaves outside the "easy" population) |

All three were caught before they could silently propagate further: Bug 1 before any notebook output existed at all; Bug 2 via an in-notebook mandatory sanity gate before Step 2 consumed the feature; Bug 3 via an independent, systematic documentation audit that recomputed every headline number directly from source CSVs rather than trusting previously-written prose.

---

## Source documents

- `outputs/reports/stage4/step1_modeling/ds4_net_blueprint.md` §1–2 (Bug 1)
- `outputs/model_outputs/ds4_network_models/model_run_summary.md`, `participant_network_metrics.md`, `ds4_net_summary.md` (Bugs 1 and 2, executed numbers)
- `outputs/model_outputs/ds4_agent_based/participant_abm_simulation_results.md`, `abm_model_comparison_summary.md` (Bug 3, corrected and reconciled)
- `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` item 1 (Bug 3, original discovery)
- `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §2 (cross-dataset context for Bugs 1 and 2)

---

*Written 2026-08-08 as part of the DS4 post-analysis synthesis. No DS5 template exists for this specific document (DS5's own bug history is scattered across its model_run_summary files and the `documentation_audit_findings_2026-08-07.md` synthesis rather than consolidated in the post_analysis folder); this file follows the task's own instruction to consolidate DS4's bugs in one place given 3+ were found.*
