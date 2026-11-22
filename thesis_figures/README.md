# Thesis figures

Final figures exactly as used in the thesis, copied from the thesis sources. The table maps each
figure to the thesis file/label that includes it and to the script or notebook whose code
contains the figure's file name (automatic text match — a match means the file name occurs in
that code, so confirm by opening it; `—` means no code in this repository writes that exact
file name, e.g. hand-composed diagrams or figures post-processed outside Python).

| Figure file (`thesis_figures/`) | Thesis source | Label | Produced by (code match) |
|---|---|---|---|
| `general/ds5_indivTrajectory_groupMean_final.png` | `include/Introduction.tex` | `fig:individual-trajectories` | `scripts/regenerate_ds5_thesis_figures.py` |
| `DS5_onesec/architecture_final_stpr-new_cropped.png` | `include/Theory.tex` | `fig:onesec-arch` | — |
| `structured/Mapping_Architecture_Structured_Models.png` | `include/Theory.tex` | `fig:structured-arch` | — |
| `DS6_onesec/fig3_stm_susceptibility_distribution.png` | `include/backmatter/Empirical_Results_Appendix.tex` | `fig:app-ds6-stm-pooled` | `scripts/regenerate_ds6_susceptibility_distribution.py`<br>`notebooks/61_structured_statistical_mechanics.ipynb`<br>`notebooks/71_ds6_statistical_mechanics.ipynb` |
| `DS4_onesec/fig3_ds4_fixedpoint_validation.png` | `include/backmatter/Empirical_Results_Appendix.tex` | `fig:ds4-fixedpoint` | `scripts/regenerate_ds4_fixedpoint_validation.py`<br>`notebooks/55_ds4_dynamical_systems.ipynb` |
| `DS4_onesec/fig4_daily_vs_weekly_theta.png` | `include/backmatter/Empirical_Results_Appendix.tex` | `fig:ds4-theta` | `scripts/regenerate_ds4_daily_vs_weekly_theta.py`<br>`notebooks/53_ds4_stochastic_processes.ipynb` |
| `structured/fig2_stop_fano_distribution.png` | `include/backmatter/Empirical_Results_Appendix.tex` | `fig:structured-fano` | `scripts/regenerate_structured_fano_distribution.py`<br>`notebooks/63_structured_stochastic_processes.ipynb` |
| `DS5_onesec/fig3_stm_potential_landscape.png` | `include/results/01_statistical_mechanics.tex` | `fig:ds5-stm` | `scripts/regenerate_fig4_1_ds5_stm_potential.py`<br>`notebooks/41_ds5_statistical_mechanics.ipynb` |
| `DS6_onesec/fig3_stm_susceptibility_by_condition.png` | `include/results/01_statistical_mechanics.tex` | `fig:ds6-stm` | `scripts/plot_ds6_susceptibility_condition.py` |
| `structured/fig_time_valid_path_dependence.png` | `include/results/01_statistical_mechanics.tex` | `fig:structured-path-dependence` | `scripts/regenerate_supplemental_thesis_figures.py`<br>`scripts/run_supplemental_thesis_analyses.py` |
| `DS5_onesec/fig4_dys_stop_int.png` | `include/results/02_dynamical_systems.tex` | `fig:ds5-dys-stop-int` | `scripts/regenerate_fig4_4_ds5_dys_stop_int.py`<br>`scripts/thesis_style.py`<br>`notebooks/42_ds5_dynamical_systems.ipynb` |
| `DS6_onesec/fig2_dys_regime_window_comparison.png` | `include/results/02_dynamical_systems.tex` | `fig:ds6-dys-window` | `scripts/regenerate_supplemental_thesis_figures.py`<br>`scripts/run_supplemental_thesis_analyses.py` |
| `DS5_onesec/fig1_stop_params_four_panel.png` | `include/results/03_stochastic_processes.tex` | `fig:ds5-stop` | `scripts/regenerate_ds5_thesis_figures.py` |
| `DS6_onesec/fig1_stop_mu_sigma_by_period.png` | `include/results/03_stochastic_processes.tex` | `fig:ds6-stop` | `scripts/regenerate_fig4_7_ds6_stop_scatter.py`<br>`notebooks/73_ds6_stochastic_processes.ipynb` |
| `DS5_onesec/fig1_net_hhi_h_trans_by_condition.png` | `include/results/04_network_theory.tex` | `fig:ds5-net` | `scripts/regenerate_fig4_8_ds5_net_violin.py`<br>`notebooks/44_ds5_network_models.ipynb` |
| `structured/fig2_net_pooled_state_graph.png` | `include/results/04_network_theory.tex` | `fig:structured-net` | `scripts/regenerate_fig4_9_structured_net_graph.py`<br>`scripts/regenerate_structured_net_pooled_graph.py`<br>`notebooks/64_structured_network_theory.ipynb` |
| `DS5_onesec/fig1_int_entropy_by_condition.png` | `include/results/05_information_theory.tex` | `fig:ds5-int` | `scripts/regenerate_fig4_10_ds5_entropy_panels.py`<br>`notebooks/45_ds5_information_theory.ipynb` |
| `structured/fig1_syd_backlog_trajectories.png` | `include/results/08_system_dynamics.tex` | `fig:structured-backlog` | `scripts/regenerate_fig4_11_structured_backlog.py`<br>`notebooks/68_structured_system_dynamics.ipynb` |
| `DS5_onesec/fig4_fontphenotype_profiles_enhanced_notitle.png` | `include/results/09_lenses_framework.tex` | `fig:ds5-radar` | `scripts/regenerate_ds5_phenotype_radar.py`<br>`notebooks/100_phenotype_exploration.ipynb`<br>`notebooks/108_ds5_balanced_profile_radar.ipynb` |
| `DS4_onesec/fig5_ds4_phenotype_radar.png` | `include/results/09_lenses_framework.tex` | `fig:ds4-radar` | `scripts/regenerate_ds4_phenotype_radar.py`<br>`notebooks/59_ds4_phenotype_exploration.ipynb` |
| `DS4_onesec/path_f_fig1_joint_heatmap.png` | `include/results/09_lenses_framework.tex` | `fig:ds4-jointmap` | `scripts/regenerate_fig4_14_ds4_joint_heatmap.py`<br>`notebooks/133_ds4_hierarchical_phenotype.ipynb` |
| `DS6_onesec/fig4_phenotype_profiles_enhanced.png` | `include/results/09_lenses_framework.tex` | `fig:ds6-radar` | `scripts/regenerate_ds6_phenotype_radar.py`<br>`scripts/regenerate_structured_phenotype_radar.py`<br>`notebooks/100_phenotype_exploration.ipynb`<br>`notebooks/120_structured_phenotype_exploration.ipynb` … |
| `structured/fig4_phenotype_profiles_enhanced_notitle.png` | `include/results/09_lenses_framework.tex` | `fig:structured-radar` | `scripts/regenerate_structured_phenotype_radar.py`<br>`notebooks/120_structured_phenotype_exploration.ipynb` |
