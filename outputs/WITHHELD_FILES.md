# Withheld output files

The development project produced participant-level tables (cleaned data, feature tables, per-participant
model parameters, cluster assignments, event-level edge lists). **None of these are released.** Only small
aggregate result tables (no ID-like column, ≤ 60 rows) are included.

This list shows what exists in the original project (path, size) so the released documentation (the
companion `.md` files, which describe these tables' columns) can be read in context. Re-running the
notebooks on the original data regenerates them.

| File in original project | Rows | Columns | Reason withheld |
|---|---:|---:|---|
| `outputs/features/ds1/ds1_behavior_features.csv` | 619 | 43 | ID-like column (619 rows) |
| `outputs/features/ds1/ds1_prepost_features.csv` | 168 | 14 | ID-like column (168 rows) |
| `outputs/features/ds1/ds1_survey_features.csv` | 527 | 16 | ID-like column (527 rows) |
| `outputs/features/ds4/ds4_behavior_features.csv` | 1039 | 59 | ID-like column (1039 rows) |
| `outputs/features/ds4/ds4_survey_features.csv` | 283 | 9 | ID-like column (283 rows) |
| `outputs/features/ds5/ds5_behavior_features.csv` | 573 | 57 | ID-like column (573 rows) |
| `outputs/features/ds5/ds5_prepost_features.csv` | 284 | 18 | ID-like column (284 rows) |
| `outputs/features/ds5/ds5_survey_features.csv` | 572 | 12 | ID-like column (572 rows) |
| `outputs/features/ds6/ds6_behavior_features.csv` | 243 | 69 | ID-like column (243 rows) |
| `outputs/features/ds6/ds6_prepost_features.csv` | 188 | 10 | ID-like column (188 rows) |
| `outputs/features/ds6/ds6_survey_features.csv` | 243 | 19 | ID-like column (243 rows) |
| `outputs/features/structured/structured_participant_features.csv` | 61 | 34 | ID-like column (61 rows) |
| `outputs/features/structured/structured_survey_features.csv` | 61 | 21 | ID-like column (61 rows) |
| `outputs/features/structured/structured_task_lifecycle_features.csv` | 26729 | 33 | ID-like column (26729 rows) |
| `outputs/harmonized/stage2/harmonized_core_features.csv` | 2474 | 28 | ID-like column (2474 rows) |
| `outputs/model_outputs/agent_based/participant_abm_summary.csv` | 414 | 8 | ID-like column (414 rows) |
| `outputs/model_outputs/ds4_agent_based/participant_abm_simulation_results.csv` | 641 | 10 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_dynamical_systems/participant_dynamics_parameters.csv` | 1039 | 9 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds4_game_theory/participant_gat_phenotypes.csv` | 986 | 8 | ID-like column (986 rows) |
| `outputs/model_outputs/ds4_information_theory/participant_entropy_metrics.csv` | 1039 | 12 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds4_network_models/participant_network_metrics.csv` | 1039 | 12 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds4_network_models/transition_edge_list.csv` | 441 | 4 | 441 rows > 60 (not a small aggregate table) |
| `outputs/model_outputs/ds4_phenotyping/ds4_cluster_assignments.csv` | 641 | 2 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_phenotyping/ds4_demographic_overlay.csv` | 149 | 4 | ID-like column (149 rows) |
| `outputs/model_outputs/ds4_phenotyping/ds4_phenotype_feature_matrix.csv` | 641 | 7 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_phenotyping/path_a_feature_matrix.csv` | 641 | 7 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_phenotyping/path_c_feature_matrix.csv` | 641 | 5 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_phenotyping/path_f_joint_assignments.csv` | 641 | 3 | ID-like column (641 rows) |
| `outputs/model_outputs/ds4_statistical_mechanics/participant_ds4_stm_parameters.csv` | 1039 | 19 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv` | 1039 | 9 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds4_stochastic_processes/participant_parameters_weekly_sensitivity.csv` | 1039 | 7 | ID-like column (1039 rows) |
| `outputs/model_outputs/ds6/dynamical_systems/participant_regime_classification.csv` | 243 | 12 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/information_theory/net_int_bridge_check.csv` | 243 | 9 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv` | 243 | 14 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/network_models/participant_network_metrics.csv` | 243 | 20 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/network_models/stop_net_period_comparison.csv` | 243 | 11 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/network_models/transition_edge_list.csv` | 6205 | 7 | ID-like column (6205 rows) |
| `outputs/model_outputs/ds6/phenotyping/cluster_assignments.csv` | 227 | 7 | ID-like column (227 rows) |
| `outputs/model_outputs/ds6/phenotyping/phenotype_feature_matrix.csv` | 227 | 6 | ID-like column (227 rows) |
| `outputs/model_outputs/ds6/phenotyping_path_a/cluster_assignments.csv` | 227 | 6 | ID-like column (227 rows) |
| `outputs/model_outputs/ds6/phenotyping_path_a/phenotype_feature_matrix.csv` | 227 | 5 | ID-like column (227 rows) |
| `outputs/model_outputs/ds6/statistical_mechanics/int_bridge_check.csv` | 243 | 7 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/statistical_mechanics/participant_macrostate_metrics.csv` | 243 | 10 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/stochastic_processes/daily_series_long.csv` | 10242 | 5 | ID-like column (10242 rows) |
| `outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv` | 243 | 17 | ID-like column (243 rows) |
| `outputs/model_outputs/ds6/system_dynamics/participant_stock_flow.csv` | 188 | 13 | ID-like column (188 rows) |
| `outputs/model_outputs/dynamical_systems/dys_stop_int_comparison.csv` | 414 | 12 | ID-like column (414 rows) |
| `outputs/model_outputs/dynamical_systems/participant_dynamics_parameters.csv` | 414 | 15 | ID-like column (414 rows) |
| `outputs/model_outputs/dynamical_systems/participant_dynamics_v2.csv` | 414 | 11 | ID-like column (414 rows) |
| `outputs/model_outputs/game_theory/participant_gat_parameters.csv` | 573 | 10 | ID-like column (573 rows) |
| `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` | 572 | 9 | ID-like column (572 rows) |
| `outputs/model_outputs/information_theory/stop_int_comparison.csv` | 414 | 6 | ID-like column (414 rows) |
| `outputs/model_outputs/network_models/net_stop_int_dys_stm_comparison.csv` | 569 | 27 | ID-like column (569 rows) |
| `outputs/model_outputs/network_models/participant_network_metrics.csv` | 569 | 17 | ID-like column (569 rows) |
| `outputs/model_outputs/network_models/participant_network_metrics_v2_no_selfloop.csv` | 569 | 9 | ID-like column (569 rows) |
| `outputs/model_outputs/network_models/transition_edge_list.csv` | 1726 | 5 | ID-like column (1726 rows) |
| `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` | 414 | 6 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` | 209 | 5 | ID-like column (209 rows) |
| `outputs/model_outputs/phenotyping/ds5_condition_cluster_assignments.csv` | 414 | 8 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_dynamic_cluster_assignments.csv` | 414 | 9 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_gmm_augmented_assignments.csv` | 414 | 3 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_gmm_k3_assignments.csv` | 414 | 9 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_gmm_layer2_assignments.csv` | 125 | 2 | ID-like column (125 rows) |
| `outputs/model_outputs/phenotyping/ds5_gmm_phase1_assignments.csv` | 414 | 5 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_hierarchical_assignments.csv` | 414 | 8 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_intervention_cluster_assignments.csv` | 414 | 9 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_net_subcluster_assignments.csv` | 414 | 6 | ID-like column (414 rows) |
| `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` | 209 | 23 | ID-like column (209 rows) |
| `outputs/model_outputs/statistical_mechanics/condition_potential.csv` | 600 | 8 | 600 rows > 60 (not a small aggregate table) |
| `outputs/model_outputs/statistical_mechanics/participant_stm_parameters.csv` | 414 | 23 | ID-like column (414 rows) |
| `outputs/model_outputs/statistical_mechanics/participant_stm_parameters_v2.csv` | 414 | 8 | ID-like column (414 rows) |
| `outputs/model_outputs/statistical_mechanics/stm_stop_int_dys_comparison.csv` | 414 | 15 | ID-like column (414 rows) |
| `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | 414 | 16 | ID-like column (414 rows) |
| `outputs/model_outputs/stochastic_processes/participant_parameters_v2_mle.csv` | 414 | 11 | ID-like column (414 rows) |
| `outputs/model_outputs/stochastic_processes/representative_simulations.csv` | 91 | 9 | ID-like column (91 rows) |
| `outputs/model_outputs/structured/agent_based/agent_rule_parameters.csv` | 43 | 11 | ID-like column (43 rows) |
| `outputs/model_outputs/structured/agent_based/simulation_results_model1.csv` | 43 | 2 | ID-like column (43 rows) |
| `outputs/model_outputs/structured/agent_based/simulation_results_model2.csv` | 43 | 2 | ID-like column (43 rows) |
| `outputs/model_outputs/structured/dynamical_systems/participant_trajectory_metrics.csv` | 61 | 14 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/dynamical_systems/weekly_state_vectors_long.csv` | 561 | 8 | ID-like column (561 rows) |
| `outputs/model_outputs/structured/game_theory/participant_gat_summary.csv` | 61 | 7 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/information_theory/participant_entropy_metrics.csv` | 61 | 16 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/network_theory/entry_state_distribution.csv` | 26729 | 4 | ID-like column (26729 rows) |
| `outputs/model_outputs/structured/network_theory/participant_network_metrics.csv` | 61 | 15 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/network_theory/transition_edge_list.csv` | 717 | 4 | ID-like column (717 rows) |
| `outputs/model_outputs/structured/phenotyping/cluster_assignments.csv` | 36 | 9 | ID-like column (36 rows) |
| `outputs/model_outputs/structured/phenotyping/path_a/behavior_only_cluster_assignments.csv` | 41 | 8 | ID-like column (41 rows) |
| `outputs/model_outputs/structured/phenotyping/path_a/behavior_only_feature_matrix.csv` | 41 | 7 | ID-like column (41 rows) |
| `outputs/model_outputs/structured/phenotyping/path_c/net_only_cluster_assignments.csv` | 45 | 6 | ID-like column (45 rows) |
| `outputs/model_outputs/structured/phenotyping/path_c/net_only_feature_matrix.csv` | 45 | 5 | ID-like column (45 rows) |
| `outputs/model_outputs/structured/phenotyping/path_d/secondary_cluster_assignments.csv` | 0 | 7 | ID-like column (0 rows) |
| `outputs/model_outputs/structured/phenotyping/path_d/secondary_feature_matrix.csv` | 41 | 6 | ID-like column (41 rows) |
| `outputs/model_outputs/structured/phenotyping/path_f/joint_taxonomy_assignments.csv` | 36 | 14 | ID-like column (36 rows) |
| `outputs/model_outputs/structured/phenotyping/phenotype_feature_matrix.csv` | 36 | 8 | ID-like column (36 rows) |
| `outputs/model_outputs/structured/statistical_mechanics/configuration_counts_long.csv` | 321 | 7 | ID-like column (321 rows) |
| `outputs/model_outputs/structured/statistical_mechanics/participant_stm_summary.csv` | 61 | 11 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/stochastic_processes/daily_series_long.csv` | 9828 | 4 | ID-like column (9828 rows) |
| `outputs/model_outputs/structured/stochastic_processes/participant_stop_parameters.csv` | 61 | 20 | ID-like column (61 rows) |
| `outputs/model_outputs/structured/system_dynamics/backlog_stock_long.csv` | 792 | 7 | ID-like column (792 rows) |
| `outputs/model_outputs/structured/system_dynamics/participant_syd_summary.csv` | 61 | 9 | ID-like column (61 rows) |
