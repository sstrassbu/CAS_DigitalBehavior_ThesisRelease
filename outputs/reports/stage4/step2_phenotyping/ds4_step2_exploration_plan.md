# DS4 Step 2 — Further Exploration Plan

**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** Paths A′/C′/F′ all ran as
notebooks 131/132/133 (see §6). Real numbers below matched the pre-registered ones from
this plan (with one documented exception: Path A′'s final ARI vs Phase 1 is 0.664 using
its own chosen k=4, not the 0.724 shown in §2 below, which was a same-k=3 preliminary
comparison done before k=4 was selected as final — see
`outputs/model_outputs/ds4_phenotyping/path_a_feature_matrix.md`'s "Known limitations"
for the reconciliation). Plan preserved below as the pre-registration record; unmodified
except for this status line.
**Prerequisite:** DS4 Step 2 Phase 1 — complete (`59_ds4_phenotype_exploration.ipynb`)

---

## 1. Why not a mechanical port of DS5's six paths

DS5's six-path plan included two paths tied to structure DS4 does not have:

- **Path E (condition-stratified)** — DS4 has no experimental condition at all.
  Checked for a substitute quasi-grouping variable (`dominant_intervention_type`,
  DS4's per-participant most-common intervention type): real distribution is
  705/157/139/23/12 across 5 types — far too imbalanced for a stratified split
  (`min_cell` would be single digits). No usable substitute exists. Skipped, same
  honest reasoning Structured used to skip/fold this path.
- **Path B (intervention-sensitive, H_out-based)** — DS5's version specifically
  measured *friction-response* sensitivity, which requires a condition to respond to.
  DS4 has no condition. Skipped.

Two paths **are** well-motivated by real DS4 data, verified below, plus one natural
combination path once both exist:

---

## 2. Path A′ — Behavior-only (drop NeT)

**Question:** does DS4's Phase 1 taxonomy depend on network structure (`rho_self`), or
is it already behavior-dominated?

**Features:** `tau_hat`, `H_emp`, `fixed_point_deviation`, `chi_OU` (Phase 1's 5 minus
`rho_self`). Same complete-case N=641.

**Verified (2026-08-06):**

```
k=2: silhouette=0.2654, jaccard=0.7753 (STABLE)
k=3: silhouette=0.3315, jaccard=0.8874 (STABLE)
k=4: silhouette=0.3477, jaccard=0.8714 (STABLE)
```

All three candidate k's are stable — unlike Phase 1, no silhouette-vs-stability
conflict here. **k=4 chosen** (highest silhouette among stable candidates).

**ARI vs Phase 1's k=3 solution: 0.724 (using Path A′'s own k=3 for a fair comparison)
— HIGH.** Dropping the network feature barely changes the taxonomy. **DS4's phenotype
space is primarily behavior/thermodynamics-driven, not network-driven** — the opposite
of DS5 (whose Phase 1 was NeT-dominated, Path A there was near-orthogonal, ARI=0.020)
and different again from Structured (whose Path A fully recovered Phase 1, ARI=1.000).
DS4 sits in between: real but partial network contribution.

---

## 3. Path C′ — Network-focused

**Question:** does DS4's network structure form its own independent phenotype axis?

**Feature-selection finding, checked before designing this path:** NeT's own richer
feature set (`rho_self`, `HHI_net`, `H_trans`) is **severely internally redundant** —
`corr(rho_self,HHI_net)=0.867`, `corr(rho_self,H_trans)=-0.950`,
`corr(HHI_net,H_trans)=-0.919`. This is close to mechanical: high self-transition rate
almost necessarily means high concentration and low transition entropy. Using all three
would not be a genuine multi-dimensional network view — it would be one signal
triple-counted. **This also retroactively validates Phase 1's choice of `rho_self`
alone** for NeT's slot — adding `HHI_net`/`H_trans` there would have been redundant, not
richer. Only `I_consec` (the InT-NeT mutual-information bridge) is close to independent
of the other three (`corr(rho_self,I_consec)=-0.014`).

**Features:** `rho_self` + `I_consec` — the two non-redundant NeT-side quantities.

**Verified (2026-08-06):**

```
k=2: silhouette=0.4018, jaccard=0.8055 (STABLE)
k=3: silhouette=0.5147, jaccard=0.9658 (STABLE)  <- chosen
k=4: silhouette=0.4486, jaccard=0.9033 (STABLE)
```

**k=3 chosen** — very clean, well-separated, highly stable (Jaccard=0.966, the
strongest stability of any DS4 clustering result so far).

**ARI vs Phase 1: 0.047 — near-zero, essentially orthogonal.** Network structure forms
its own clean, real taxonomy that Phase 1's blended feature set (1 NeT feature diluted
among 4 behavioral ones) barely captured. Combined with Path A′'s result, DS4's
structure looks like: **a dominant behavioral axis (Path A′ ≈ Phase 1) plus a
genuinely separate, independently-clean network axis (Path C′, orthogonal to both)** —
a two-layer picture, but with the *dominance* reversed from DS5's (DS5: network
dominant, behavior secondary; DS4: behavior dominant, network secondary-but-real).

---

## 4. Path F′ — Joint taxonomy (Path A′ × Path C′)

**Question:** what does crossing the two independent axes reveal — is DS4's true
structure better described by 4 (behavior×network) cells than either axis alone?

Only well-motivated once A′ and C′ both exist as real, stable results (they now do).
Cross-tabulate Path A′'s k=4 labels against Path C′'s k=3 labels; test independence
(Fisher's exact / chi-square, matching Structured's Path F method — structural reuse of
the *test*, not its DS4-inapplicable result). Report whichever cells are populated
enough to interpret (`min_cell` check before over-reading any cross-tab cell).

---

## 5. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | 3 paths only (A′, C′, F′) — not 6 | Paths E/B have no DS4 analog (§1); D is redundant with Phase 1's already-dynamical feature set |
| FLAG 2 | Same stability-first k-selection as Phase 1 | Established this session's own precedent (Phase 1's k=4→k=3 correction) |
| FLAG 3 | Path C′ drops `HHI_net`/`H_trans` for `rho_self`+`I_consec` only | Real redundancy check (§3), not an arbitrary reduction |
| FLAG 4 | Path F′ implemented only after A′/C′ both run, using their real k's | Cannot pre-specify the cross-tab shape before both real solutions exist |

---

## 6. Notebooks

**Numbering note (checked, corrected before writing this final version):** the 100s
range is already fully claimed — DS5:100-108, Stanford Health:110-111,
**Structured:120-124** (not free — an earlier draft of this plan wrongly assumed 121-123
were open). Next free round decade is 130s (verified via `ls notebooks/`).

- `notebooks/131_ds4_behavior_only_phenotype.ipynb` — Path A′
- `notebooks/132_ds4_network_focused_phenotype.ipynb` — Path C′
- `notebooks/133_ds4_hierarchical_phenotype.ipynb` — Path F′

Each gets its own generator script, real-number verification, companion `.md` docs, and
memory update — same cycle as every DS4 Step 1/Step 2 Phase 1 notebook.

**Output root:** `outputs/model_outputs/ds4_phenotyping/` (same directory as Phase 1,
each path's files prefixed `path_a_`/`path_c_`/`path_f_`).

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during plan review and has since been cleared; all three generator
scripts (Paths A′/C′/F′) were approved and implemented. Kept below for the historical
record.
