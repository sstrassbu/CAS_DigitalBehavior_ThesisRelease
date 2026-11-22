# DS6 — Network Theory (NeT) Blueprint

**Notebook:** `notebooks/74_ds6_network_models.ipynb`
**Written:** 2026-08-06
**Position:** 74 in the DS6 70s decade. Does not depend on StoP (73) — independent
implementation, matching why Structured did NeT early too (a dataset's richest asset
shouldn't wait on an unrelated dependency chain). InT (75), if built, can bridge to this
notebook's `H_trans` the same way DS5's InT-NeT bridge did.
**Depends on:** `outputs/cleaned/ds6_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/ds6/network_models/`

---

## Part 0 — Mandatory pre-check: is the sequence data actually usable?

Before any node/edge design, verified whether the pre-engineered `app_next`/`app_prev`
fields genuinely represent app-transition sequences, since this notebook's entire premise
depends on it. **They do not both hold up.** Full verification on the raw file:

- DS6's true underlying event log alternates Open→Close→Open→Close (this exported file
  keeps only the Open rows). `app_next` was computed against the FULL alternating sequence,
  so for 99.3% of rows the very next logged record is the current app's own close event —
  `app_next` mechanically echoes `app_name`, not a real subsequent choice.
  (`resolution_next == 'closedApp'` for 99.4% of rows; conditioned on that, `app_next ==
  app_name` 99.3% of the time.)
- `app_prev` does not have this problem: looking backward, the immediately-prior logged
  record is typically the *previous, different* app's close event. Verified: `app_prev ==
  app_name` only ~42% overall, stable (39–64%) across `resolution_last` categories — a
  plausible, non-mechanical same-app-vs-switch split.
- `app_next2` (skipping the intervening close) is also genuine but requires conditioning on
  `resolution_next2=='openedApp'`; `app_prev` is used here instead since it needs no such
  conditioning and is directly available.

**This blueprint builds all transition edges from `app_prev`, never `app_next`.** Full
verification recorded in `data_docs/modeling_cautions.md` §6 and
`outputs/reports/stage0/ds6_audit_report.md` §8b — read those before extending this notebook.
This finding was made specifically because this NeT notebook was about to be built on the
wrong field; do not assume it "already checked out" from the StoP notebook (73), which
never touched `app_next`/`app_prev` at all (it used raw daily event counts).

---

## Part 1 — Theory grounding (paper §2.4, quoted directly)

> "Nodes may represent target apps, app categories, outcome states, or combined
> app-outcome states... Edges represent consecutive observed One Sec events... A strong
> Instagram → Instagram edge may indicate repeated returns to the same target app. A strong
> Instagram → YouTube edge may indicate possible substitution."
>
> "If the log contains only One Sec-triggered events, the network should be interpreted
> cautiously. It does not represent the user's complete smartphone ecology... Edges should
> be interpreted as temporal adjacencies, not causal effects."

DS6 cannot use "outcome states" or "combined app-outcome states" as nodes (no dismiss/close
outcome variation — same limitation that shaped the StoP blueprint). This notebook uses the
paper's other named option directly: **nodes = target apps**, matching the paper's own
Example A illustration exactly.

---

## Part 2 — Node and edge definition

**Nodes:** target apps. DS6's app vocabulary is small and closed — **10 apps globally**
(snapchat, tikTok, instagram, youtube, facebook, pinterest, reddit, twitter, beReal, twitch;
verified via `app_name.nunique()` on the full file), with a mean of 3.65 unique apps per
participant. This is a much smaller, tighter state space than DS1 (48 apps) or DS4 (399
apps) — closer in spirit to Structured's small 7-state vocabulary than to DS1/DS4/DS5's
wide app spaces. Expect correspondingly higher hub-concentration (HHI_net) than DS1/DS4,
simply from having fewer possible destinations, independent of any behavioral effect —
flagged here so it isn't later mistaken for a substantive finding.

**Edges:** `app_prev[t] → app_name[t]` for every row `t` with non-null `app_prev`, per
participant, per study_period. This reconstructs genuine chronological app-to-app adjacency
(row order in the exported file is itself real Open-event order — the same technique
`max_consecutive_same_app` already relies on) without touching the broken `app_next` field.

**Two networks per participant, not one — mirroring StoP's period split (blueprint Part 1):**
built separately for `study_period ∈ {baseline, intervention}`, matching the notebook 73
design so that HHI_net/rho_self/H_trans become directly comparable to StoP's mu_hat/sig_hat/
Fano_factor across the same baseline→intervention boundary. Verified transition-count
availability per period (non-null `app_prev` rows):

```
Baseline:      mean=653, median=521, min=0     -- 239/243 eligible at MIN_TRANSITIONS=20
Intervention:  mean=809, median=629, min=4     -- 235/243 eligible at MIN_TRANSITIONS=20
```

---

## Part 3 — Network metrics (same definitions as DS5 NeT, re-verified as appropriate for DS6's much smaller vocabulary)

For each participant × period with a valid transition list:

```
T_ij            = count of i->j transitions / total transitions from i   (transition matrix)
HHI_net         = sum_i (out-share_i)^2                                  (hub concentration,
                                                                            Herfindahl on node
                                                                            out-degree share)
rho_self        = sum_i T_ii * (share of transitions starting at i)      (pooled self-loop rate;
                                                                            equals self_transition_rate
                                                                            when computed the same way)
H_trans         = -sum_ij p_ij * log2(p_ij)                              (entropy of the pooled
                                                                            transition distribution)
pi              = stationary distribution (power iteration on T),
                  only for participants whose chain is irreducible/ergodic
```

**FLAG NET-1 (eligibility):** `MIN_TRANSITIONS = 20` per period, matching DS5's own
FLAG NET1 lower bound — reused, not re-derived, since DS6's transition volume so vastly
exceeds this threshold (median 521/629 per period) that a stricter bound would not
meaningfully change eligibility (239/243 and 235/243 either way).

**FLAG NET-2 (self-loops):** included, matching DS5's FLAG S1 — a same-app re-open (verified
genuine via `app_prev`, not the `app_next` artifact) is a real, meaningful transition, not
noise to exclude.

**FLAG NET-3 (stationary distribution):** computed only where the empirical transition
matrix is irreducible (every visited node reachable from every other); reported as NaN
otherwise, not imputed. Given the small (≤10-node, typically ≤4-node per participant) state
space and very high transition counts, expect a much higher stationary-eligible share than
DS5's 66.4% or Structured's 13.1% — this is a testable prediction stated before running, not
after.

---

## Part 4 — Condition × period breakdown, and bridge to StoP

Same design as StoP Part 5: report HHI_net/rho_self/H_trans by `study_condition ×
study_period` (both native columns, no join required). Bridge quantity, new to this
notebook: does network concentration (HHI_net) shift the same direction as StoP's volume
drop (mean daily attempts 45.1→29.1, notebook 73)? A concentration increase alongside a
volume decrease would suggest narrowing to fewer, more habitual apps under friction; a
concentration decrease would suggest more exploratory switching. Stated as an open question
here, not assumed.

---

## Part 5 — Output file structure

```
outputs/model_outputs/ds6/network_models/
  participant_network_metrics.csv    # one row per participant: HHI_net/rho_self/H_trans/
                                      # n_transitions/n_unique_apps for BOTH periods,
                                      # study_condition, stationary-eligibility flags
  transition_edge_list.csv           # long format: participant_id, study_period,
                                      # app_from, app_to, count, share
  condition_period_summary.csv       # study_condition x study_period aggregate table
  stop_net_period_comparison.csv     # per-participant join of notebook 73's mu_hat/Fano
                                      # against this notebook's HHI_net/rho_self, both periods
  figures/
    fig1_net_hhi_rho_by_period.png
    fig2_net_transition_heatmap_examples.png
    fig3_net_condition_period_comparison.png
    fig4_net_stop_bridge_scatter.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Verified `app_prev` (not `app_next`) is the genuine sequence field before any design
      work — this blueprint exists because that check was done first
- [x] Paper §2.4 quoted directly; node=app matches the paper's own Example A
- [x] Small (10-app) vocabulary flagged explicitly as a likely driver of high HHI_net,
      stated before running so it isn't later read as a behavioral finding
- [x] Eligibility reused from DS5's FLAG NET1 threshold, cross-checked against DS6's own
      (much higher) transition-count distribution
- [x] Period split mirrors StoP (notebook 73) for direct cross-model comparability
- [x] Bridge question to StoP's volume finding stated as an open question, not pre-decided
- [x] Notebook 74 implemented and executed — 239/243 (98.4%) baseline / 235/243 (96.7%)
      intervention NeT-eligible; ~96% stationary-eligible in both periods (confirmed the
      pre-registered small-state-space prediction). Headline: corr(HHI_net change,
      daily-volume change) = -0.213, p=0.0012 — cutting usage back under friction narrows
      toward fewer habitual apps rather than spreading evenly. Pre-registered "small
      vocabulary -> high HHI_net" expectation only partly confirmed (mean HHI_net ~0.50,
      moderate not extreme) — reported honestly, not reframed. See `model_run_summary.md`.
