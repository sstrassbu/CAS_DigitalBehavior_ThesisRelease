"""Regenerate Fig 4.11 (Structured weekly backlog trajectories) at thesis width, no title.

Restyle only: redraws from the already-computed weekly backlog panel; no re-fitting.
Data: PRE-RERUN (61-participant) tables via structured_old_data.read_old_csv, because the
thesis text still reports the original 61-participant results (see that module).
Source notebook: notebooks/68_structured_system_dynamics.ipynb (cell "fig1_syd_backlog_trajectories").
LaTeX placement: width=0.75\\textwidth (08_system_dynamics.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402
from structured_old_data import read_old_csv  # noqa: E402

OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "structured" / "system_dynamics" / "figures"


def main() -> None:
    ts.apply()
    backlog_long = read_old_csv("system_dynamics/backlog_stock_long.csv")
    syd_summary = read_old_csv("system_dynamics/participant_syd_summary.csv")
    eligible_ids = syd_summary.loc[syd_summary["is_syd_eligible"], "participant_id"]
    print(f"SyD-eligible participants plotted: {len(eligible_ids)} of {len(syd_summary)}")

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.5))
    cmap = plt.get_cmap("tab20")
    for i, (pid, g) in enumerate(
        backlog_long[backlog_long["participant_id"].isin(eligible_ids)].groupby("participant_id")
    ):
        g = g.sort_values("week_idx")
        ax.plot(g["week_idx"], g["Backlog_w"], alpha=0.5, color=cmap(i % 20), linewidth=1.0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Week (participant-relative)")
    ax.set_ylabel("Open non-censored tasks (Backlog$_w$)")
    fig.tight_layout()

    for path in ts.save(fig, "structured", "fig1_syd_backlog_trajectories.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
