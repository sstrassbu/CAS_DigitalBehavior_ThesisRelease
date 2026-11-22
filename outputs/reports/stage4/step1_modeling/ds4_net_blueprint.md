# DS4 NeT (Network Theory) Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_network_models/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/54_ds4_network_models.ipynb`
**Generator script (to be created):** `notebooks/make_54_ds4_net.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Network Theory (NeT)
**Prerequisites:** None of the other 4 DS4 families — NeT only needs sequence
engineering. Completing this notebook closes DS4 Step 1 (all 5 fixed families).

---

## 1. The central methodological decision — verified before writing this blueprint

DS5's NeT notebook (`44_ds5_network_models.ipynb`) built its app-transition sequence
from "all valid outcomes" (FLAG 2A) because DS5 has a single event class — every row is
a genuine attempt to engage with an app. **DS4 cannot use that same rule unmodified**:
DS4 has a structurally different `app_close_event` class (47.1% of all rows) that is not
a new engagement attempt at all — it is the closing tail of a session whose opening was
already logged as a separate `intervention_event` or `no_intervention` row.

**Verified real evidence this matters (2026-08-06):** pooling all 3 event classes into
one timestamp-ordered sequence and computing the self-transition rate gives
`rho_self=0.743`. Breaking that down by class-pair reveals why: an `intervention_event`
immediately followed by an `app_close_event` has `rho_self=0.959` (n=348,028) — this is
overwhelmingly "friction shown on app X, then X's own close event fires next," not a
behavioral decision to stay on the same app. Restricting the sequence to genuine
**attempt** rows only (`intervention_event` + `no_intervention`, excluding
`app_close_event`) drops `rho_self` to **0.624** — a real, substantively different
number, not a rounding difference.

**Decision: build the NeT sequence from attempt rows only** (`intervention_event_class
in {'intervention_event', 'no_intervention'}`), excluding `app_close_event`. This is not
a DS5 port — DS5 never had this class to exclude in the first place. It also is not the
same restriction StoP/InT/DyS/StM used (`intervention_event` class only) — NeT needs
`no_intervention`'s genuine opens/dismissals too, since a close-tail is not being
excluded there, only a same-session close artifact.

---

## 2. Verified facts this blueprint is grounded in

| Quantity | Value |
|---|---|
| Total DS4 events | 2,490,260 |
| Attempt rows (`intervention_event`+`no_intervention`, excl. `app_close_event`) | 1,318,331 (52.9%) |
| Unique apps overall | 399 |
| Top-20-app coverage of attempt rows | 91.7% |
| Participants with ≥1 attempt-to-attempt transition | 1,031 |
| Eligible at MIN_TRANSITIONS=50 | **950 (91.4%)** |
| `rho_self`, naive all-class pooling (not used) | 0.743 |
| `rho_self`, `intervention_event` class only (not used — loses `no_intervention`'s real opens) | 0.631 |
| **`rho_self`, attempt rows only (used)** | **0.624** |

---

## 3. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 (state space) | Top-20 apps by attempt-row frequency, encoded to indices; remainder → `'other'` (21 states total) | Real coverage check: top-20 covers 91.7% of attempt rows. DS4's 399-app vocabulary is far larger than DS1's 48, so a generous but bounded K is needed — DS5 never faced this tail-length problem |
| FLAG 2 (event scope) | Attempt rows only (`intervention_event`+`no_intervention`), excluding `app_close_event` | §1 — real, verified `rho_self` difference (0.624 vs 0.743 naive pooled), not a stylistic choice |
| FLAG 3 (eligibility) | MIN_TRANSITIONS=50 consecutive attempt-to-attempt pairs per participant | Real eligible N=950 (91.4%) — deliberately not copying DS5's exact 20/50 pair (DS5 also used 50 as its "stationary-eligible" tier; for DS4 the base eligibility check is verified directly rather than assumed) |
| FLAG 4 (Markov order) | First-order Markov (app_previous → app_current), same as DS5 | No textual basis in the shared theory paper for higher-order chains; matches DS5's own FLAG M1 |
| FLAG 5 (self-loops) | Included in the transition matrix | Matches DS5's FLAG S1 — excluding them would hide the (now more meaningful, since app_close_event is already excluded) self-transition signal |
| FLAG 6 (time gaps) | No time-gap filter between consecutive attempt rows | Matches DS5's FLAG G1 — a gap filter would require an arbitrary session-boundary definition DS4 does not have pre-engineered (unlike DS6's `group_id`, which memory already flags as unreliable anyway) |

---

## 4. Quantities

| Quantity | Definition | DS4-specific note |
|---|---|---|
| Transition matrix `T_ij` | Row-normalized counts of `(app_prev→app_current)` over attempt rows, per participant | 21×21 (20 apps + other) |
| `rho_self` | `T_ii` diagonal mass / total, on the top-20+'other' encoded matrix | Real DS4 value ≈0.62 pooled, not DS5's ≈0.92 — do not expect similar magnitude. Note the encoding inflates it: 'other'->'other' pairs count as self-transitions (+0.0107 mean, +0.05 or more for 57/950 participants) |
| `H_trans` | Shannon entropy of the transition distribution, per participant | Same construction as DS5 |
| `HHI_net` | Herfindahl of each participant's **attempt-row** app-usage share | Computed on the NeT-filtered (attempts-only) subset for internal consistency with `T_ij` — expected close to, but not identical to, Stage 1's `app_herfindahl` (computed on all events); both reported, correlation checked as a redundancy sanity check |
| Stationary distribution `π` | Power iteration on `T` | **NOT the same construction as DS5 (as implemented):** DS4 pads every chain to the fixed 21-state grid, gives unvisited states an absorbing self-loop row and starts from a uniform 21-state π; DS5 restricts to the participant's own visited state set and applies a `residual < 1e-6` convergence gate. No irreducibility or convergence screen exists in the DS4 code. |
| `H_pi` | Entropy of `π` | Computed for every eligible participant, no screen. Because of the 21-state padding above, H_pi is dominated by probability mass trapped in never-visited absorbing states and is pushed toward the log2(21)=4.3923 ceiling (143/950 = 15.05% sit exactly at it). Treat the shipped `H_pi` and `median_H_pi` as invalid. |
| `I_consec` (InT-NeT bridge) | `H_app − H_trans` (using InT's already-computed `H_app`, joined not recomputed) | Must verify `I_consec≥0` for all participants (mirrors DS5's own verified bridge) |

---

## 5. Notebook structure — `notebooks/54_ds4_network_models.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope: attempt-only sequence decision, why (§1) |
| 2 | MD | FLAG decisions table |
| 3 | MD | DS4 structural cautions: 3 event classes, why `app_close_event` is excluded here specifically (different reason than StoP/InT/DyS/StM's exclusion of it) |
| 4 | MD+LaTeX | Theory: Markov transition matrix, stationary distribution, entropy, InT-NeT bridge `I=H_app−H_trans` |
| 5 | MD | Theory-to-data mapping table |
| 6 | Code | Setup: imports, paths, `TOP_K=20`, `MIN_TRANSITIONS=50` |
| 7 | Code | Load `ds4_behavioral_clean.csv`; filter to attempt rows; build `app_prev`/`app_current` sequence per participant (sorted by `timestamp_utc`) |
| 8 | Code | Encode apps to top-20 + `'other'`; verify real coverage (reproduce §2's 91.7%) |
| 9 | Code | Per-participant transition matrix `T_ij`, `rho_self`, `H_trans`; eligibility funnel (reproduce §2's real N=950) |
| 10 | Code | Per-participant `HHI_net` (attempts-only); load Stage 1 `app_herfindahl`; redundancy check correlation |
| 11 | Code | Stationary distribution `π` via power iteration on the 21-state matrix for every eligible participant; `H_pi`. **As implemented, no irreducibility or convergence check was applied** — this pre-registered step was not built. |
| 12 | Code | InT-NeT bridge: join InT's `H_app`; compute `I_consec=H_app−H_trans`; verify `I_consec≥0` |
| 13 | Code | Export `participant_network_metrics.csv`, `transition_edge_list.csv` |
| 14 | Code | Distribution summaries; export `ds4_net_summary.csv`, `model_run_summary.md` |
| 15 | Code | Figure 1: `rho_self` distribution (DS4 vs the DS5 value stated as a text annotation, descriptive only) |
| 16 | Code | Figure 2: `H_trans` distribution |
| 17 | Code | Figure 3: pooled transition heatmap, top-20 apps + other |
| 18 | Code | Figure 4: `HHI_net` (NeT, attempts-only) vs Stage 1 `app_herfindahl` (all events) scatter — the redundancy check |
| 19 | MD | Interpretation and limits |
| 20 | MD | Forward connections |

---

## 6. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_network_models/`

| File | Description | Rows |
|---|---|---|
| `participant_network_metrics.csv` | Per participant: `n_transitions`, `rho_self`, `H_trans`, `HHI_net`, `H_pi` (where stationary-eligible), `I_consec`, eligibility flags | 1,039 |
| `transition_edge_list.csv` | Pooled `(app_prev, app_current, count, probability)` across all eligible participants | ~441 (21×21) |
| `ds4_net_summary.csv` | Sample-level distribution summary + eligibility funnel | 1 |
| `model_run_summary.md` | Full run record | — |
| `figures/fig1_ds4_rho_self_distribution.png` | rho_self histogram | — |
| `figures/fig2_ds4_htrans_distribution.png` | H_trans histogram | — |
| `figures/fig3_ds4_transition_heatmap.png` | Pooled transition matrix heatmap | — |
| `figures/fig4_ds4_hhi_redundancy_check.png` | HHI_net (NeT) vs app_herfindahl (Stage 1) scatter | — |

---

## 7. DS4 weakness flags

- ⚠ FLAG I: Excluding `app_close_event` means this notebook does not use ~47% of DS4's
  raw events. This is a deliberate, verified choice (§1), not data loss by oversight —
  but must be stated plainly, since it's the largest single-class exclusion of any DS4
  Step 1 notebook.
- ⚠ FLAG II: No experimental condition — transition structure describes naturalistic
  heterogeneity only.
- ⚠ FLAG III: First-order Markov assumption unverified (matches DS5's own unresolved
  caveat — no textual basis to test higher-order structure).
- ⚠ FLAG IV: `π` (stationary distribution) is a long-run approximation; only meaningful
  for participants with enough transitions to plausibly approach it.
- ⚠ FLAG V: `rho_self≈0.62` should **not** be compared in magnitude to DS5's `≈0.92`
  without the caveat that the two are constructed from structurally different event
  universes (DS5: all valid outcomes in a single-class dataset; DS4: attempt rows only,
  explicitly excluding a close-tail class DS5 never had).

---

## 8. Forward connections

| Connection | Mechanism | Target |
|---|---|---|
| DS4 NeT → DS4 Step 2 (Phenotyping) | `rho_self`, `HHI_net`, `H_trans` as network-topology phenotype dimensions, completing the 5-family feature set (mirrors DS5's Layer 1/Layer 2 structure question) | Future — after all 5 DS4 families are done (this notebook is the last) |
| DS4 NeT → Paper | Attempt-only sequence construction and the `app_close_event`-exclusion finding are not yet in the conceptual paper |

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.

When approved:
1. Create `notebooks/make_54_ds4_net.py`
2. Run generator, execute notebook, verify against §2's pre-registered numbers
3. Write companion `.md` docs for every output file
4. Update `memory/project_stage.md` and `memory/cross_dataset_strategy.md` — **this
   closes DS4 Step 1** (all 5 fixed families: StoP/InT/DyS/StM/NeT complete)
