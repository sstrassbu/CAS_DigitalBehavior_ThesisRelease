# `scripts/` — thesis figure scripts

Scripts that redraw the thesis figures in one common style (A4 text width, fixed font sizes, no in-figure titles — the LaTeX caption carries the description). They **restyle only**: no analysis is recomputed; each reads the result tables the notebooks write.

* `thesis_style.py` — shared style, colours, figure widths and the `save()` helper.
* `regenerate_*.py`, `plot_ds6_susceptibility_condition.py` — one script per figure or figure family. Which script produces which thesis figure: [`../thesis_figures/README.md`](../thesis_figures/README.md).
* `run_supplemental_thesis_analyses.py` — supplementary analyses reported in the thesis.
* `structured_old_data.py` — loader for the Structured result tables of the thesis snapshot (61 participants); see [`../docs/REPRODUCING.md`](../docs/REPRODUCING.md) §5 for how to supply the tables in this release.
* `execute_notebook.py` — executes a notebook with an explicit working directory.

Figures are written to `latex_master_thesis/figure/<subdir>/` (the thesis folder layout of the development repository) and, for some, to `outputs/`. The finished figures are frozen in [`../thesis_figures/`](../thesis_figures/).

These scripts need the notebook result tables, which in turn need the (withheld) data.
