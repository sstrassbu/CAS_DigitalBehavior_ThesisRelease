# participant_network_metrics.csv

**Unit of observation:** one row per DS4 participant (all 1,039).

**Model:** DS4 Network Theory (NeT) — app-transition network built from **attempt rows
only** (`intervention_event`+`no_intervention`, excluding `app_close_event`).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `n_transitions` | int | Count of attempt-to-attempt consecutive pairs |
| `eligible` | bool | `True` iff `n_transitions>=50` (MIN_TRANSITIONS) |
| `rho_self` | float | Self-transition rate (diagonal mass / total) of the **top-20 + 'other' encoded** matrix, attempts-only. `NaN` unless `eligible`. **Caveat:** a transition between two DIFFERENT apps that both fall outside the top 20 lands in the ('other','other') diagonal cell and is counted as a self-transition. Recomputed on raw app names: mean 0.6876 / median 0.6671 vs the encoded mean 0.6983 / median 0.6795 (mean inflation +0.0107). The tail matters: 57/950 eligible participants are inflated by >0.05, worst case +0.622, and 50 have an 'other' share above 0.5. |
| `H_trans` | float | Conditional entropy `H(current\|previous)`, bits. `NaN` unless `eligible` |
| `HHI_net` | float | Herfindahl of app-usage share, computed on attempt rows |
| `H_pi` | float | Entropy of the stationary distribution `π`. `NaN` unless `eligible`. **`n_stationary_eligible` = `n_eligible` = 950 by construction, not because a screen was passed — no irreducibility or convergence check was implemented** (see `ds4_net_blueprint.md` §4). π is computed on the padded 21-state grid with absorbing rows for never-visited states, so `H_pi` is invalid: 143/950 (15.05%) sit exactly at the log2(21)=4.3923 ceiling and it correlates POSITIVELY with `HHI_net` (r=+0.205). |
| `H_app_all_events` | float | InT's `H_app`, joined for **reference only** — computed on a different (all-events) population, NOT the bridge partner |
| `H_app_attempts` | float | Marginal entropy of `app_current_enc` within the same attempts-only, top-20-encoded population `H_trans` uses — the **correct** InT-NeT bridge partner |
| `I_consec` | float | `H_app_attempts - H_trans`, mutual information between consecutive apps. Verified ≥0 for all 950 eligible participants after the fix below |

---

## How this file was produced

- **Source:** `outputs/cleaned/ds4_behavioral_clean.csv`
- **Producing notebook:** `notebooks/54_ds4_network_models.ipynb`
- **Generator script:** `notebooks/make_54_ds4_net.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_net_blueprint.md`

## Bug caught and fixed during implementation

The first `I_consec = InT's H_app − H_trans` produced **138/950 negative values** (min
−0.63 bits) — mathematically impossible for a true `H(Y)−H(Y|X)`. Root cause, verified
concretely on participant `<participant-id>`: InT's `H_app` is
computed over **all** events, including `app_close_event`. This participant had 647
`app_close_event` rows, 98% reddit, dragging their all-events `H_app` down to 0.86 bits
— but their 158 real attempt rows were far more diverse (`H_trans`=1.49 bits on that
same diverse population). InT's `H_app` was measuring the wrong population for this
bridge. **Fixed** by computing `H_app_attempts` — the current-app marginal within the
exact same population `H_trans` is built from. Result: 0/950 negative after the fix.
Same class of bug as Structured's NeT-InT bridge fix (wrong marginal population).

## Actual run results (2026-08-06)

- 950/1,039 (91.4%) eligible at MIN_TRANSITIONS=50.
- Median `rho_self` = 0.680 (attempts-only) — **not comparable in magnitude to DS5's
  ~0.92** (see `ds4_net_blueprint.md` §1 for why: DS5 never had a close-tail class to
  exclude).
- Median `H_trans` = 0.954 bits, median `HHI_net` = 0.509.
- `corr(HHI_net, Stage 1's app_herfindahl)` = 0.969 — the two measure closely related
  but not identical things (attempts-only vs all-events population).
- `I_consec` median = 0.079 bits (all non-negative after the fix).

## Known limitations

- **Excludes `app_close_event`** — 47.1% of DS4's raw events are not part of this
  network's sequence construction. Deliberate, verified (§1 of the blueprint), not
  oversight.
- `rho_self` here should not be compared in magnitude to DS5's without the construction
  caveat above.
- First-order Markov assumption unverified (same open question as DS5's NeT).
- No experimental condition — describes naturalistic heterogeneity only.

## How to load

```python
import pandas as pd

net = pd.read_csv("outputs/model_outputs/ds4_network_models/participant_network_metrics.csv")
valid = net[net["eligible"]]  # 950 rows with real network metrics
```
