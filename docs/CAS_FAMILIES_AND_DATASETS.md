# CAS model families × datasets

Where each Complex Adaptive Systems model family is implemented, where its results are, and which thesis chapter file reports it. Notebook numbers refer to files in [`../notebooks/`](../notebooks/README.md) (match on the number **and** the dataset tag: `61_ds5_…` ≠ `61_structured_…`). Output folders are under [`../outputs/model_outputs/`](../outputs/README.md).

**Families:** StM statistical mechanics · DyS dynamical systems · StoP stochastic processes · NeT network theory · InT information theory · GaT game theory · ABM agent-based modelling · SyD system dynamics.

## Thesis chapter files (LaTeX sources are not part of this repository)

| Family | Thesis file |
|---|---|
| StM | `include/results/01_statistical_mechanics.tex` |
| DyS | `include/results/02_dynamical_systems.tex` |
| StoP | `include/results/03_stochastic_processes.tex` |
| NeT | `include/results/04_network_theory.tex` |
| InT | `include/results/05_information_theory.tex` |
| GaT | `include/results/06_game_theory.tex` |
| ABM | `include/results/07_agent_based.tex` |
| SyD | `include/results/08_system_dynamics.tex` |
| cross-family synthesis | `include/results/09_lenses_framework.tex` |

## DS5 — German adolescents, randomized friction trial (N = 573)

Output folders carry **no dataset prefix** (DS5 was the first dataset worked through).

| Family | Notebook(s) | Output folder |
|---|---|---|
| StM | `41_ds5_statistical_mechanics` · v2: `60b_ds5_stm_v2_boltzmann` | `statistical_mechanics/` |
| DyS | `42_ds5_dynamical_systems` · v2: `60_ds5_dys_v2_potential_well` | `dynamical_systems/` |
| StoP | `43_ds5_stochastic_processes` · v2: `62_ds5_stop_v2_mle` | `stochastic_processes/` |
| NeT | `44_ds5_network_models` · v2: `61_ds5_net_v2_no_selfloop` | `network_models/` |
| InT | `45_ds5_information_theory` | `information_theory/` |
| GaT | `46_ds5_game_theory` | `game_theory/` |
| ABM | `47_ds5_agent_based` | `agent_based/` |
| SyD | not implemented (needs repeated survey waves; reserved for DS6) | — |
| Phenotyping (Step 2) | `100_phenotype_exploration` (Phase 1) · six paths `101`–`106` · figures `107`, `108` · GMM v2 `63`, `64` | `phenotyping/` |
| Personalization (Step 3, exploratory) | `200_ds5_personalization_exploration` | — |

Read first: `outputs/reports/stage4/post_analysis/ds5_step2_master_synthesis.md`, `outputs/reports/stage4/ds5_step2_phenotype_exploration_plan.md`.

## DS4 — large non-experimental One Sec cohort (N = 1,039)

Output folders are prefixed `ds4_`.

| Family | Notebook | Output folder |
|---|---|---|
| StM | `51_ds4_statistical_mechanics` | `ds4_statistical_mechanics/` |
| InT | `52_ds4_information_theory` | `ds4_information_theory/` |
| StoP | `53_ds4_stochastic_processes` | `ds4_stochastic_processes/` |
| NeT | `54_ds4_network_models` | `ds4_network_models/` |
| DyS | `55_ds4_dynamical_systems` | `ds4_dynamical_systems/` |
| GaT | `56_ds4_game_theory` | `ds4_game_theory/` |
| ABM | `57_ds4_agent_based` | `ds4_agent_based/` |
| SyD | structurally excluded (no repeated survey structure) | — |
| Phenotyping (Step 2) | `59_ds4_phenotype_exploration` · paths `131`, `132`, `133` | `ds4_phenotyping/` |

## DS6 — Danish adolescents, baseline → intervention (N = 243)

Output folders are nested under `ds6/`.

| Family | Notebook | Output folder |
|---|---|---|
| StM | `71_ds6_statistical_mechanics` | `ds6/statistical_mechanics/` |
| DyS | `72_ds6_dynamical_systems` | `ds6/dynamical_systems/` |
| StoP | `73_ds6_stochastic_processes` | `ds6/stochastic_processes/` |
| NeT | `74_ds6_network_models` | `ds6/network_models/` |
| InT | `75_ds6_information_theory` | `ds6/information_theory/` |
| SyD | `78_ds6_system_dynamics` | `ds6/system_dynamics/` |
| GaT, ABM | formally deferred (rationale in `outputs/reports/stage4/post_analysis/ds6/ds6_deferred_models_rationale.md`) | — |
| Phenotyping (Step 2) | `140_ds6_phenotype_exploration` · behaviour-only `141_ds6_behavior_only_phenotype` | `ds6/phenotyping/`, `ds6/phenotyping_path_a/` |

## Structured — retrospective task-planning export (N = 61)

Output folders are nested under `structured/`. The behavioural object is task planning (create / update / delete a task), **not** app-opening friction — there is no intervention, so the OneSec constructs do not carry over. Read `outputs/reports/structured/structured_cas_modeling_plan.md` first.

| Family | Notebook | Output folder |
|---|---|---|
| StM | `61_structured_statistical_mechanics` | `structured/statistical_mechanics/` |
| DyS | `62_structured_dynamical_systems` | `structured/dynamical_systems/` |
| StoP | `63_structured_stochastic_processes` | `structured/stochastic_processes/` |
| NeT | `64_structured_network_theory` | `structured/network_theory/` |
| InT | `65_structured_information_theory` | `structured/information_theory/` |
| GaT | `66_structured_game_theory` | `structured/game_theory/` |
| ABM | `67_structured_agent_based` | `structured/agent_based/` |
| SyD | `68_structured_system_dynamics` | `structured/system_dynamics/` |
| Phenotyping (Step 2) | `120_structured_phenotype_exploration` · paths `121` (network), `122` (behaviour-only), `123` (hierarchical), `124` (secondary features) | `structured/phenotyping/` |

Preprocessing notebooks: `15_structured_inspection`, `16_structured_cleaning`, `17_structured_feature_extraction`.

## Preprocessing notebooks per dataset

| Dataset | Inspect | Clean | Features |
|---|---|---|---|
| DS1 | `01_dataset_1_inspection` | `02_dataset_1_cleaning` | `11_ds1_feature_extraction` |
| DS4 | `03_dataset_4_inspection` | `04_dataset_4_cleaning` | `12_ds4_feature_extraction` |
| DS5 | `05_dataset_5_inspection` | `06_dataset_5_cleaning` | `13_ds5_feature_extraction` |
| DS6 | `07_dataset_6_inspection` | `08_dataset_6_cleaning` | `14_ds6_feature_extraction` |
| Structured | `15_structured_inspection` | `16_structured_cleaning` | `17_structured_feature_extraction` |
