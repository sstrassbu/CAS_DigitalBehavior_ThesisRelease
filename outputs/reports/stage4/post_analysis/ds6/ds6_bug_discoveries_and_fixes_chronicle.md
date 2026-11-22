# Bug Discoveries and Fixes — DS6 Chronicle

**Written:** 2026-08-08
**Overlap check:** Read in full — the DS5 post-analysis folder has no equivalent single
bug-chronicle document (DS5's bugs are scattered across `ds5_v2_revision_and_phenotype_addendum.md`
and individual blueprint sections), so this file has no direct DS5 template to mirror
structurally; it follows the general reporting conventions of the other DS6 post-analysis
files instead. Also read in full: `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md`
§2 (places DS6's NeT/InT bugs in a cross-dataset bug-class pattern — cited, not re-derived)
and `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` (source for items
e and f below). **Scope of this file:** DS6-only, full technical detail for every independently
found bug across the DS6 build history (2026-08-05 through 2026-08-07), consolidated from
`data_docs/modeling_cautions.md` §6, `data_docs/stage1_feature_qc_notes.md` addenda,
`outputs/reports/stage0/ds6_audit_report.md` §8a–8b, individual blueprint addenda, and the
`model_run_summary.md`/companion `.md` files for InT and StM — none of which individually
narrates the full six-item arc as a single chronology.

---

## Why DS6 has an unusually rich bug history

DS6 is the only dataset in this project where two independent, structural, pre-modeling data
artifacts were found and fixed **before** the first CAS model notebook was written (items a
and b), followed by two independent bridge-computation bugs found **during** Step 1
implementation (items c and d), followed by a dedicated sanity-check audit that found two
more (item e), followed by a documentation/figure audit that found one more (item f). Every
single one of these six was caught by a check performed *before* trusting a result — the
project's own "catch it before you trust it" discipline, applied six separate times on one
dataset. This chronicle exists because that density of independently-caught, well-documented
bugs is itself a notable feature of DS6's build history, worth preserving as one connected
narrative rather than six scattered mentions.

---

## (a) The `group_id` / session-structure bug — found 2026-08-05, before any DS6 model was built

**Trigger:** before implementing the first DS6 CAS model (StoP), the claim that `group_id`
enables session-level (open→close) analysis — asserted in `ds6_features.md` and
`ds6_audit_report.md` as "DS6-unique: session structure not available in DS1/DS4/DS5" — was
checked directly against the raw file rather than taken on faith, because it was about to
become the anchor for a model's state variable.

**What was wrong:** verified on the full raw file
(`session_time_dataset_97_5_cutoff_data_forwarded.csv`, all 353,796 rows, not a sample):
- `group_id` is unique per row (`nunique() == len(df)`) — it does not group multiple events into a session at all.
- `first_in_group == 1` for every single row; `last_close_in_group == 0` for every single row; `unmatched_open == False` for every single row.
- `close_ts − openedapp_open_time` equals `time_diff_secs` exactly (max absolute difference ≈1e-12, i.e. float rounding).
- The same pattern was confirmed in `baseline_sessions_filt3.csv` (no `group_id` column there, but its own `close_ts − timestamp` also tracks `time_diff_secs`).

**Direct, exact-duplication consequence, checked numerically, not assumed:** `n_sessions_total`
was numerically identical to `total_events`; `session_rate_baseline` identical to
`events_per_day_baseline`; `session_rate_ratio` identical to
`event_rate_ratio_intervention_vs_baseline` — checked as 0.0 max difference across all 243
participants. This was not a near-duplicate (unlike the separately-noted
`app_entropy_baseline`/`app_entropy` correlation) — it was an **exact duplicate under a
different, session-suggestive name**.

**How caught:** a direct verification pass on the raw file, performed specifically because
the claim was about to be load-bearing for a model's design, not a routine audit.

**What was fixed:**
- `src/features/ds6_features.py`: `ds6_session_features()` removed entirely; renamed to
  `ds6_timing_features()`, now returning only `mean_time_diff_secs` (genuine — computed
  directly from `time_diff_secs`, which is real dwell time, just not evidence of session
  *grouping*). `session_rate_early`/`session_rate_late` removed from
  `ds6_longitudinal_adaptation()`.
- `notebooks/14_ds6_feature_extraction.ipynb` re-run (2 cells patched that printed the
  now-removed columns) → `ds6_behavior_features.csv` regenerated at **243×67**, down from
  **243×77** — 10 columns removed, all confirmed non-informative duplicates.
- Corrected in 8 downstream files the same session: `ds6_features.md`,
  `data_docs/modeling_cautions.md` (§1, §4, §5, §6), `data_docs/stage1_feature_qc_notes.md`,
  `outputs/reports/stage0/ds6_audit_report.md` (new §8a), `outputs/cleaned/ds6_behavioral_clean.md`,
  and 3 Stage 3 planning docs that had independently picked up the same false claim in April
  (`dataset_strengths_summary.md`, `dataset_strengths_table.csv`, `modeling_readiness_summary.md`).

**Did any CAS headline number change?** No — this was caught and fixed entirely before the
first DS6 model notebook (StoP, 73) was written. No published model result was ever built on
the removed features.

**A mis-step embedded in this same fix, later itself corrected (see item b):** the original
2026-08-05 write-up additionally claimed `close_ts` "is the timestamp of the next open event,
not a real app-close event." That specific interpretive claim was wrong (the underlying
arithmetic was right; only its meaning was misread) and was retracted the very next day when
item (b) was found — see below.

---

## (b) The `app_next` look-ahead artifact — found 2026-08-06, while designing NeT

**Trigger:** while designing the DS6 Network Theory (NeT) model — which was about to use
`app_next` as its primary transition-edge data — `app_next` was verified to genuinely mean
"the next app the participant opened" before building on it, applying the same mindfulness
check that had caught bug (a) the day before.

**What was wrong:** DS6's true underlying event log alternates Open→Close→Open→Close; the
exported file keeps only the Open rows, but the look-ahead columns (`app_next`,
`resolution_next`, etc.) were computed against the **full, unfiltered** alternating sequence:
- `resolution_next == 'closedApp'` for 351,446/353,796 rows (**99.4%**) — the very next
  logged event after an Open is almost always that same app's own close.
- Conditioned on `resolution_next == 'closedApp'`, `app_next == app_name` **99.3%** of the
  time — `app_next` is mechanically echoing the current app's own close record, not
  recording a real subsequent app choice.
- `app_next2`/`resolution_next2` (which skip the intervening close) do **not** have this
  problem: `resolution_next2 == 'openedApp'` for 64.7% of rows (the true next Open), and
  conditioned on that, `app_next2 == app_name` only 38.8% of the time — a believable,
  non-mechanical same-app-vs-switch split.
- `app_prev` (looking backward) also does **not** have the forward problem: `app_prev ==
  app_name` only ~42% overall, stable (39–64%) across `resolution_last` categories.

**Direct consequence, previously undetected:** every DS6 "Group 4" sequence feature except
`max_consecutive_same_app` was built on the broken `app_next`/`resolution_next` fields:
`self_transition_rate` (previously mean=0.989, sd=0.018 — near-ceiling, at the time
attributed to "within-session re-opening," an explanation that could not have been correct
anyway since bug (a) had already shown DS6 has no real sessions at all), `cross_app_transition_rate`,
`app_next_entropy`, `n_unique_next_apps`, `top_next_app`, `top_next_app_share`, and
`resolution_next_open_rate`. Worse: `app_next_entropy` and `n_unique_next_apps` had been the
**explicitly recommended** DS6 substitution-tendency features in an earlier version of
`modeling_cautions.md` §3/§4 — the bug had already propagated into stated modeling guidance
before it was caught.

**A related retraction, same finding:** because `resolution_next == 'closedApp'` 99.4% of the
time, the very next logged event after an Open genuinely usually **is** a real close event —
which means item (a)'s claim that `close_ts` "is the timestamp of the next open event, not a
real close event" was itself wrong and is retracted here. The arithmetic in item (a)
(`close_ts − openedapp_open_time == time_diff_secs`) was always correct; only the
interpretation was wrong. `close_ts`/`time_diff_secs` are genuine open→close dwell time for
~99% of rows. This retraction is itself the origin of the stale-documentation finding later
caught and separately fixed in item (f)'s companion finding (`ds6_features.md` had not yet
picked up this correction as of the 2026-08-07 documentation audit).

**How caught:** the same discipline that caught bug (a) — verifying a field's actual meaning
against the raw file before building a model's primary data source on it, one day later, on a
different field in the same feature family.

**What was fixed:**
- `src/features/ds6_features.py::ds6_sequence_features()` rebuilt on `app_prev` instead of
  `app_next`. `self_transition_rate`/`cross_app_transition_rate` keep their names but change
  value (now mean=0.512, sd=0.217 — genuinely informative, not near-ceiling). Renamed:
  `app_next_entropy`→`app_transition_entropy`, `n_unique_next_apps`→`n_unique_transition_apps`,
  `top_next_app`→`top_transition_app`, `top_next_app_share`→`top_transition_app_share`.
  `resolution_next_open_rate` removed (verified near-constant-near-zero, 0.5% overall).
  `max_consecutive_same_app` untouched (never used `app_next`/`app_prev` — built only from
  the exported file's own real Open-event row order).
- `notebooks/14_ds6_feature_extraction.ipynb` re-run; `ds6_behavior_features.csv` and
  `ds6_features.md` regenerated/updated; `data_docs/modeling_cautions.md` (new §6 entry) and
  `data_docs/stage1_feature_qc_notes.md` (new addendum) updated; `ds6_audit_report.md` (new §8b).

**Did any CAS headline number change?** No, in the strongest sense available here: NeT (74),
the family this check was performed *for*, never ended up using `app_next` **or** `app_prev`
directly — it self-derives transitions via `shift(-1)` on time-sorted rows instead (a more
conservative choice than strictly required, since `app_prev` was separately cleared). The
Stage 1 feature table itself changed (the numbers above), but no Step 1 CAS model result was
ever computed from the broken columns.

**Lesson recorded in CLAUDE.md, worth repeating here explicitly:** clearing one field in a
feature family (`app_prev`, cleared as a side effect of this same investigation) does not
clear a different field in the same family (`app_next`) — each needs its own independent
check, which is exactly what happened here one bug apart.

---

## (c) The NeT–InT bridge wrong-marginal bug — found 2026-08-06, during InT implementation, two failed attempts

**Trigger:** computing `I_consec = H_app_marginal − H_trans` for the NeT–InT bridge, the
mandatory `I_consec >= 0` sanity gate (mutual information cannot be negative — the same
discipline that had already caught an identical bug class in Structured's own NeT–InT
bridge) failed **twice in a row** before landing on the correct fix.

**Attempt 1 — Stage 1's `app_entropy` as `H_app_marginal`:** failed the gate for a small
number of participant-periods (small negative `I_consec` values). Root cause: a last-event-
per-period boundary mismatch between Stage 1's `app_entropy` computation window and NeT's
transition-edge computation window — the two features were not computed over exactly the
same event population.

**Attempt 2 — the transition edge list's `app_from` (source) marginal:** reduced but did not
eliminate the violation (1 participant, `I_consec = −0.0493`). Root cause, correctly
identified this time: this was the **wrong side of the mutual-information identity**.
`I(X_t; X_{t+1}) = H(X_{t+1}) − H(X_{t+1} | X_t)` requires the **destination** marginal
(`app_to`), not the source (`app_from`).

**Final fix:** `H_app_marginal` computed from the transition edge list's `app_to` column
(destination marginal) — **0 violations across all 486 participant-periods** (243
participants × 2 periods) after the fix.

**How caught:** the mandatory `I_consec >= 0` gate, applied as a non-negotiable check before
any downstream use of `I_consec`, exactly as Structured's own NeT–InT bridge implementation
had already established. DS6's own model_run_summary explicitly notes that the correct fix
("target-state marginal from NeT's own edge list") was already on record from Structured's
prior instance of this exact bug class, and that it should have been applied directly on the
first attempt rather than re-derived from the wrong side twice — a process lesson stated
honestly in the notebook's own documentation, not glossed over.

**Did any CAS headline number change?** No — both failed attempts were caught by the gate
before either was published or used in any downstream figure or summary statistic. The
published `I_consec` means (baseline 0.069, intervention 0.053 bits) reflect only the final,
correct computation.

---

## (d) The StM–InT bridge granularity mismatch, plus a NaN-handling gotcha found immediately after — 2026-08-06, during StM implementation

**Bug 1 — sanity-gate comparability mismatch:** the mandatory `H_joint >= max(H_app, H_hour)`
sanity gate (a standard entropy-chain-rule identity, used here as a mandatory check before
trusting `H_joint`) initially compared `H_joint` — built on a coarse 4-category `hour_bucket`
— against InT's `H_hour`, which is built on the full 24-value `hour_of_day`. This is an
invalid granularity mismatch (comparing an entropy computed on a 4-bin partition against one
computed on a 24-bin partition of the same underlying variable is not a valid instance of the
chain-rule inequality), and it produced near-universal false "violations": 239/240 baseline,
240/240 intervention. **Fix:** compute `H_hour_bucket` fresh, on the exact same 4-category
partition as `H_joint`, rather than reusing InT's `H_hour` for this specific comparison.

**Bug 2 — found immediately after fixing Bug 1, in the fix's own validation code:** the gate
assertion used `.dropna()` on the boolean `gate_valid` column, but `NaN >= number` evaluates
to `False` in pandas (not `NaN`), so participants with missing `H_joint` showed up as an
explicit `False` rather than being dropped by `.dropna()`. This produced a visible
contradiction: the print statement reported "240/240 passing" while the assertion beneath it
still failed — caught by reading the actual assertion failure rather than trusting the
printed summary line alone. **Fix:** filter on `H_joint`'s own null mask directly, before
evaluating the `>=` comparison, rather than relying on `.dropna()` after the fact.

**Result after both fixes:** 240/243 participants have valid `H_joint`; all 240 pass the
gate in both periods; the 3 participants with missing `H_joint` are correctly excluded, not
counted as violations.

**Did any CAS headline number change?** No — DS6's StM headline finding (susceptibility by
condition, F=5.437, p=0.0049) was computed after both fixes; neither bug touched the
`susceptibility` computation itself, only the separate sanity-gate check surrounding it.

---

## (e) The 2026-08-06 sanity-check audit's own two findings — a recurrence of the same pandas gotcha, one export layer removed

**Trigger:** a user-requested, dataset-wide sanity-check audit (30+ headline numbers across
StoP/NeT/InT/DyS/SyD/StM/phenotyping recomputed directly from the saved CSVs, not read from
prose) — the same discipline Structured's own 2026-08-05 audit had already established.

**What was wrong, in both cases — the exact same underlying bug as item (d)'s Bug 2, but
recurring independently in two separate notebooks' export code, one day after that exact bug
class had already been fixed once elsewhere:**
- `outputs/model_outputs/ds6/information_theory/net_int_bridge_check.csv`:
  `bridge_valid_baseline`/`bridge_valid_intervention` stored explicit `False` (not `NaN`) for
  **4 (baseline) / 8 (intervention) participant-periods** where `I_consec` is itself `NaN`
  (the participant is NeT-ineligible that period) — because the export code used a bare
  `I_consec >= -1e-9` comparison rather than an explicit NaN-aware check. A naive read of the
  raw CSV (as opposed to trusting the notebook's own print statement) would have misreported
  these as real bridge violations.
- `outputs/model_outputs/ds6/statistical_mechanics/int_bridge_check.csv`: the identical issue,
  independently, in `gate_valid_baseline`/`gate_valid_intervention`, for **3 participant-
  periods per period**.

**Crucially — these are column-export labeling bugs, not computation bugs.** In both cases,
the notebook's own in-line assertion had *already* correctly excluded the NaN rows before
declaring the gate PASSED (that is precisely how items (c) and (d) were themselves verified
clean at the time). The bug was confined to what got written to the CSV for anyone reading
the file directly, not to any number that had already been reported in a summary or figure.

**Fix, applied identically in both notebooks:** replace the bare `>=` comparison with
`np.where(quantity.notna(), quantity >= threshold, np.nan)` at the point the boolean column
is computed, not just at export time. Both notebooks re-executed; both CSVs regenerated (0
`False` values remain in either file, only `True`/`NaN`); both companion `.md` docs updated
with a "Known limitations — audit fix" note; both `model_run_summary.md` files re-enriched.

**A process lesson recorded alongside this fix:** re-running a notebook to fix a bug also
re-runs its own summary-writing cell, which overwrites the *entire* `model_run_summary.md`
file — including any hand-added enrichment text from the original run. Both summaries had to
be manually re-enriched after the re-run, not just re-generated.

**Did any CAS headline number change?** No — confirmed explicitly in both companion `.md`
files: "No result changed." Both fixes affected only how already-correct exclusions were
labeled in an exported column, not any statistic, cluster assignment, or p-value.

---

## (f) The 2026-08-07 documentation and figure audit's blank-figure fix

**Trigger:** a full documentation and figure audit (~245 figures across every dataset visually
inspected, not just checked by metadata) found `outputs/model_outputs/ds6/information_theory/figures/fig3_int_net_bridge_scatter.png`
rendering **completely blank**.

**What was wrong:** the plotting cell joined an integer-`RangeIndex` dataframe against a
string-participant-ID-indexed dataframe using pandas' `.join()` (an index-based join), which
silently matched **zero rows** because the two indices were of incompatible types/values —
no error was raised, the plot simply had no data to draw. Every other cell in the same
notebook used `.merge(on='participant_id_canonical')` instead; this single plotting cell was
the only place in the notebook that used `.join()`.

**How caught:** direct visual inspection of the rendered PNG during the audit, not a
numerical check — the underlying bridge-check numbers (239/243 baseline, 235/243
intervention valid, 0 violations, from item (c)'s already-correct computation) were never
wrong; only this one figure's plotting code failed to retrieve the data to draw.

**Fix:** `set_index` both sides consistently on `participant_id_canonical` (equivalently,
switch to the same `.merge()` pattern used everywhere else in the notebook) before plotting.
Notebook re-executed; both panels of the figure now show real scattered data, with all points
on or above the `I_consec ≥ 0` diagonal, as the already-verified gate result predicts.

**Did any CAS headline number change?** No — explicitly confirmed in
`documentation_audit_findings_2026-08-07.md`: "Bridge-check numbers (239/235 valid, 0
violations) unchanged." This was a pure rendering bug.

**A related, separately-tracked documentation-lag finding from the same audit pass, not a
computational bug:** the same audit found that `ds6_features.md` still described `close_ts`
as "the timestamp of the next open event, not a real close event" — the exact interpretation
already retracted in item (b) above on 2026-08-06. The correction had propagated to
`modeling_cautions.md` and `ds6_audit_report.md` at the time but had not yet reached this one
file. Fixed in both places it appeared in `ds6_features.md` during the same audit pass — a
documentation-propagation gap, not a new finding about the data itself.

---

## Summary: six findings, one consistent discipline, zero surviving headline-number errors

| Item | Date found | Trigger | Bug class | Headline number affected? |
|---|---|---|---|---|
| (a) `group_id` session-structure | 2026-08-05 | Pre-modeling verification, before StoP | Data artifact — exact-duplicate features under a misleading name | No — caught before any model notebook existed |
| (b) `app_next` look-ahead | 2026-08-06 | Pre-modeling verification, before NeT | Data artifact — mechanical field echo mistaken for real sequence data | No — NeT never used the broken field, even after `app_prev` cleared |
| (c) NeT–InT wrong marginal | 2026-08-06 | Mandatory `I_consec>=0` gate, during InT | Computation — wrong side of a mutual-information identity (2 failed attempts) | No — gate caught both failed attempts pre-publication |
| (d) StM–InT granularity + NaN gate | 2026-08-06 | Mandatory `H_joint>=max(...)` gate, during StM | Computation (granularity) + logic (pandas NaN comparison) | No — both fixed before the susceptibility headline was computed |
| (e) Audit's 2 column-export bugs | 2026-08-06 | Full sanity-check audit, next day | Export-layer labeling — same `NaN>=threshold` pandas gotcha recurring in raw CSV columns | No — explicitly confirmed unchanged in both cases |
| (f) Blank figure + doc-lag | 2026-08-07 | Full documentation/figure audit | Rendering (`.join()` index mismatch) + documentation propagation lag | No — rendering-only; underlying numbers already correct |

**The pattern worth naming explicitly:** across six independently-found, real issues spanning
three days of build history and two subsequent audit passes, **not one surviving DS6 headline
number, cluster assignment, correlation, or p-value was ever affected** — every fix either
occurred before the relevant result was first published (a–d) or corrected a label/rendering
issue that never touched the substantive numbers (e–f). This stands in useful contrast to the
same-week documentation audit's finding for a *different* dataset (DS4's ABM
`participant_abm_simulation_results.md`, corrected from "113/641 (17.6%)" to "133/641
(20.7%)" — a real number that did change; see `documentation_audit_findings_2026-08-07.md`
§2 item 1). DS6's own record is not evidence that DS6 is bug-free — six real, independently
caught issues say the opposite — but it is evidence that the project's layered discipline
(mandatory sanity gates during implementation, a dedicated audit pass afterward, a
documentation/figure audit after that) worked as intended for this dataset: catching
everything before it reached a number anyone would cite.

---

*Written 2026-08-08 as part of the DS6 post-analysis reporting set.*
