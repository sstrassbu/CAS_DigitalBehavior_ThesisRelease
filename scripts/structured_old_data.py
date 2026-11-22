"""Loader for the PRE-RERUN Structured model outputs (61-participant era).

Why: the Structured pipeline was re-run on 2026-08-30/31 on 217 participants, but the
thesis text and figures still report the original 61-participant results. Thesis figures
must therefore be redrawn from the OLD tables, not the current working-tree CSVs.

Resolution order for a path like "system_dynamics/backlog_stock_long.csv"
(relative to outputs/model_outputs/structured/):
  1. $STRUCTURED_OLD_DATA_DIR/<path>   (a directory holding the restored old CSVs)
  2. `git show OLD_COMMIT:outputs/model_outputs/structured/<path>`  (default; read-only,
     never touches the working tree)

OLD_COMMIT is pinned to the last commit before the 2026-08-30 re-run was made
(the re-run is uncommitted working-tree state on top of this commit).
"""

from __future__ import annotations

import io
import os
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OLD_COMMIT = "067279b"  # HEAD before the Aug-2026 217-participant re-run was committed
REL_ROOT = "outputs/model_outputs/structured"


def read_old_csv(relpath: str, **kwargs) -> pd.DataFrame:
    """Read a Structured output CSV as it was before the 217-participant re-run."""
    env_dir = os.environ.get("STRUCTURED_OLD_DATA_DIR")
    if env_dir and (Path(env_dir) / relpath).exists():
        return pd.read_csv(Path(env_dir) / relpath, **kwargs)
    blob = subprocess.run(
        ["git", "show", f"{OLD_COMMIT}:{REL_ROOT}/{relpath}"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    return pd.read_csv(io.BytesIO(blob), **kwargs)
