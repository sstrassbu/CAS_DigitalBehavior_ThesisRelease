# Structured Step 2 — Master Synthesis Note

**Written:** 2026-08-05
**Mirrors:** `outputs/reports/stage4/post_analysis/ds5_step2_master_synthesis.md` (DS5's own six-path
synthesis). Read that document alongside this one — the value of this note is the *contrast*, not just
the standalone result.
**Status:** Step 2 exploration COMPLETE for Structured — Phase 1 + four adapted paths (A, C, D, F)
executed; Paths B and E not portable in DS5's original form (see §5).

---

## 0. What this exploration was trying to establish

Phase 1 (`notebooks/120_structured_phenotype_exploration.ipynb`) found one stable k=2 split across all 7
curated Step 1 features (N=36, Jaccard=0.775). That result alone cannot say *why* the split exists, or
whether it reflects one dominant axis of individual difference or several coincidentally-aligned ones —
exactly the question DS5's six-path exploration was built to answer for its own dataset. This exploration
asks the same question of Structured, using the same logic, adapted to what this dataset can actually
support (see `structured_step2_exploration_plan.md` for the adaptation decisions).

---

## 1. The headline finding: Structured inverts DS5's layer structure

| | DS5 | Structured |
|---|---|---|
| Dominant phenotype axis | Network topology (NeT) | Behavioral dynamics (StoP/DyS/StM/SyD/InT/GaT) |
| Path A (drop the dominant axis's own features) vs. Phase 1 | ARI=0.020 — orthogonal | **ARI=1.000 — near-perfect reproduction** |
| Secondary axis's own standalone clustering vs. Phase 1 | ARI=0.990 — near-perfect (NeT alone reproduces Phase 1) | **ARI=0.173 — weak** |
| Relationship between the two axes | Fully orthogonal (independent) | **Not independent (Fisher's exact p=0.029), but not redundant either** |

DS5's Phase 1 split was almost entirely a network-topology phenomenon (hub-locked vs. distributed app
use); its behavioral-dynamics axis was a *second, independent* layer discovered only once NeT was
excluded. **Structured is the mirror image**: Phase 1's split is almost entirely a behavioral-dynamics
phenomenon, and network topology is the *secondary*, partially-coupled axis. This was not assumed — it
was a falsifiable prediction stated in the Path A blueprint before running (based on Phase 1's own
`cluster_profiles.csv` already showing a far smaller NeT gap than DS5's), and it was confirmed by two
independent notebooks (Path A directly, Path C by elimination) before being formalized by Path F's
independence test.

---

## 2. Path A — Behavior-only phenotyping (Layer 2 analog)

**N=41** (6 non-NeT curated features). k=2 selected, bootstrap Jaccard=0.885 **STABLE**.

**ARI(Path A vs. Phase 1) = 1.000** on the N=36 overlap — a perfect cross-tabulation. Removing the
network feature entirely removed almost nothing from Phase 1's structure, because Phase 1 was never
substantially driven by it in the first place.

**Path E analog (subscription-stratified, folded in as a short check):** free subgroup (N=12) infeasible
(min_cell=3<10, correctly ruled out — an earlier implementation bug that would have wrongly called this
"STABLE" was caught and fixed). Pro subgroup (N=29) genuinely feasible, Jaccard=0.895 STABLE — but this
is an observational, non-randomized comparison and cannot claim condition-invariance the way DS5's
randomized-arm version could.

---

## 3. Path C — Network-substructure (Layer 1 analog)

**N=45** (full NeT-eligible population, independent of Phase 1). Features: `HHI_net`, `rho_self`,
`H_trans`, `H_state_marginal` (`top1_share_net` dropped, r=0.961 collinear with `HHI_net`). k=2 selected,
Jaccard=0.822 **STABLE**.

**ARI(Path C vs. Phase 1) = 0.173** (DS5's equivalent: 0.990). Low, as predicted, but not as close to
zero as DS5's fully-orthogonal case — classified PARTIAL. Network structure carries real signal, just
clearly secondary to the behavioral axis.

**Within-profile NeT sub-clustering** (Phase 1 Profile A, N=22; Profile B, N=14): both produced
bootstrap-stable 2-way splits using N-scaled `min_cell` floors, but reported as tentative regardless of
the stability numbers, matching DS5's own caution at 6-9x this sample size.

---

## 4. Path D — Secondary/robustness features: a genuine null result

**N=41** (identical to Path A). Five features not in the curated set: `created_mu_hat`,
`volume_trend_slope`, `dropout_score`, `H_hour_creation`, `persistence_rate` (`H_config` dropped, a
replication of Phase 1's own established H_config/H_completion redundancy finding, not a fresh
discovery).

**No feasible k.** Every candidate k (2, 3, 4) was driven entirely by a single extreme outlier
(`volume_trend_slope=-32.1`, the same participant DyS's own report already named as "driving most of the
spread"). Reported honestly as infeasible — matching this project's own precedent from DS5's
default-condition Path E result — rather than forced into a degenerate 1-vs-40 split. A real
implementation bug (a silent k=2 fallback that would have reported that degenerate split as "STABLE",
Jaccard=0.893) was caught by reading the printed cluster sizes before accepting the result, and fixed.

This extends, rather than contradicts, DS5's own finding that Path D was its lowest-yield path even at
N=285 (DS5 still found a stable k=2 there; Structured's much smaller N does not support even that much).

---

## 5. Why Paths B and E were not built as full paths

**Path B (intervention-sensitive)** needs `H_out`, friction-outcome entropy. Structured has no friction
intervention at all — the behavioral object is task planning, not app-opening friction. There is no
honest proxy construction that would not fabricate a construct this dataset does not contain. **Not
built**, documented the same way InT's "energy level → reschedule occurrence: NOT IMPLEMENTABLE" pairing
was — an honest absence, not a silent skip.

**Path E (condition-stratified)** used DS5's three randomized RCT arms. Structured has no randomized
conditions; the only available stratifier is observational `subscription_type_last` (free/pro), already
used elsewhere only as a descriptive, non-causal comparison. **Shrunk to a short check appended inside
Path A's notebook** rather than a full path — the free arm (N=11-12) is 8-12x smaller than even DS5's
own thinnest, already-struggling condition arm (N≈137-142).

---

## 6. Path F — Joint taxonomy: reconciling Path A and Path C

Deliberately **not** a fresh within-group clustering (DS5's literal design) and **not** a repeat of Path
C's own within-profile sub-clustering — instead, the first cross-tabulation of Path A's and Path C's
already-fitted global clusters.

**Joint taxonomy (N=36):**

| | NetProfile A | NetProfile B |
|---|---|---|
| **BehavProfile A** | 4 | 18 |
| **BehavProfile B** | 8 | 6 |

**Fisher's exact test: p=0.029, odds ratio=0.167 — the two axes are NOT statistically independent.**

This is the number that reconciles Path A's ARI=1.000 and Path C's ARI=0.173 into one coherent
statement, rather than leaving them as two seemingly-contradictory results: **network membership is not
redundant with the behavioral split (Path A alone doesn't capture everything Path C sees), but it is also
far from an independent second layer the way DS5's two axes were** — it is a real, weaker, coupled
secondary dimension.

---

## 7. The complete Structured phenotype picture, compared to DS5's

### DS5: two genuinely orthogonal layers
- Layer 1 (network) dominates and is condition-invariant.
- Layer 2 (behavioral) is a fully independent second layer (ARI=0.020 vs. Layer 1), and is itself
  condition-*modulated* (collapses under the default friction condition).
- A third candidate layer (friction-response diversity, Path B) turned out not to be independent of
  Layer 2.

### Structured: one dominant layer with a coupled, non-independent secondary layer
- The behavioral-dynamics axis dominates (Path A: ARI=1.000 vs. Phase 1) — the inverse emphasis from DS5.
- The network axis is real but secondary, and **statistically coupled** to the behavioral axis
  (Path F: p=0.029) rather than orthogonal to it — a structurally different relationship than DS5's two
  fully-independent layers.
- The secondary/robustness feature set (Path D) shows no independent structure at all at this N — a
  genuine null, not merely a weaker echo of Path A the way DS5's own Path D was.
- No condition-modulation test is possible (no randomized conditions exist in this data) — the single
  biggest structural limitation relative to DS5's synthesis, not a finding in its own right.

---

## 8. What remains genuinely unresolved

1. **Sample size dominates every result's confidence interval.** N=36-45 across these four paths is
   6-12x smaller than DS5's equivalent populations (N=125-414). Every ARI, Jaccard, and p-value here
   should be read as suggestive, not confirmatory, in a way DS5's larger-N results were not.
2. **The coupling mechanism behind Path F's p=0.029 is not identified.** The test establishes the two
   axes are not independent; it does not explain *why* (e.g., whether burstier planners also happen to
   use fewer distinct task states, or whether some third factor drives both).
3. **No condition/intervention-modulation claim is possible at all** for Structured, unlike DS5's central
   finding that its own behavioral layer collapses under a specific friction design — this is a data
   limitation (no randomized intervention exists in this dataset), not a null result to interpret.
4. **Cross-dataset replication** would need a comparably-sized planning-app dataset; none currently
   exists in this project.
5. **Psychosocial correlates:** not re-tested in any of these four paths (Phase 1's own null finding,
   consistent with DS5's own mostly-null Step 2 overlays, was not re-litigated here — would need its own
   dedicated pass if pursued further).

---

## 9. Strongest overall conclusion

> **Structured's behavioral heterogeneity is organized primarily along a single dominant axis —
> behavioral dynamics (burstiness, completion-outcome diversity, backlog trend, structural
> susceptibility, commitment level) — with network topology contributing a real but secondary,
> statistically-coupled (not independent) dimension. This is structurally different from DS5, where
> network topology and behavioral dynamics formed two fully orthogonal layers. The inversion of which
> axis dominates, combined with the coupling (rather than independence) of the secondary axis, suggests
> that the relationship between network structure and behavioral dynamics in digital-behavior phenotyping
> is not a fixed, universal pattern — it depends on what the behavioral object actually is (task planning
> vs. app-opening friction), and should be treated as an empirical question for each new dataset, not
> assumed to replicate DS5's specific two-layer structure.**

---

*Document written 2026-08-05. Based on executed notebooks 120-124 (Phase 1, Path A, Path C, Path D,
Path F), their blueprints, and all model run summaries in
`outputs/model_outputs/structured/phenotyping/`.*
