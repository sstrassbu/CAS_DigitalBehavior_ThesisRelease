"""Integrity tests for this release. They need no data and no third-party packages.

Run:  python -m unittest discover -s tests          (or: pytest tests)

They guard the repository's central promises:
  1. it contains no data and no participant-level tables,
  2. notebooks carry no stored outputs,
  3. no participant identifiers or absolute home paths leaked into text files,
  4. all modules and notebook code cells are syntactically valid Python.
"""
from __future__ import annotations

import csv
import json
import py_compile
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".ipynb_checkpoints"}

UUID_RX = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
ID_COL = re.compile(r"(participant|user|subject|pid|uuid|session_id|person)|(^id$)|(_id$)", re.I)
MAX_AGG_ROWS = 60
DATA_SUFFIXES = {".parquet", ".zip", ".xlsx", ".xls", ".sav", ".dta", ".feather", ".pkl", ".sqlite", ".db"}


def files(*suffixes: str):
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            if not suffixes or p.suffix.lower() in suffixes:
                yield p


class NoDataTests(unittest.TestCase):
    def test_data_raw_holds_only_readme(self):
        extra = [p.name for p in (ROOT / "data_raw").iterdir() if p.name not in {"README.md", ".DS_Store"}]
        self.assertEqual(extra, [], f"data_raw/ must be empty apart from README.md, found {extra}")

    def test_no_data_file_formats(self):
        bad = [str(p.relative_to(ROOT)) for p in files() if p.suffix.lower() in DATA_SUFFIXES]
        self.assertEqual(bad, [])

    def test_cleaned_and_features_are_documentation_only(self):
        for sub in ("outputs/cleaned", "outputs/features"):
            bad = [str(p.relative_to(ROOT)) for p in (ROOT / sub).rglob("*")
                   if p.is_file() and p.suffix.lower() not in {".md"}]
            self.assertEqual(bad, [], f"{sub} must contain .md documentation only")

    def test_csvs_are_small_aggregate_tables(self):
        for p in files(".csv"):
            with open(p, newline="", encoding="utf-8", errors="replace") as fh:
                rdr = csv.reader(fh)
                header = next(rdr, [])
                n = sum(1 for _ in rdr)
            rel = p.relative_to(ROOT)
            self.assertFalse([h for h in header if ID_COL.search(h or "")], f"{rel}: ID-like column")
            self.assertLessEqual(n, MAX_AGG_ROWS, f"{rel}: {n} rows is not a small aggregate table")


class HygieneTests(unittest.TestCase):
    def test_notebooks_have_no_outputs(self):
        for p in files(".ipynb"):
            nb = json.loads(p.read_text(encoding="utf-8"))
            for i, c in enumerate(nb["cells"]):
                if c["cell_type"] == "code":
                    self.assertEqual(c.get("outputs", []), [], f"{p.name}: cell {i} has stored output")
                    self.assertIsNone(c.get("execution_count"), f"{p.name}: cell {i} has execution count")

    def test_no_participant_uuids_or_home_paths(self):
        for p in files(".md", ".py", ".ipynb", ".csv", ".cff", ".txt"):
            if p.name == "test_release_integrity.py":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            rel = p.relative_to(ROOT)
            self.assertIsNone(UUID_RX.search(text), f"{rel}: contains a UUID")
            self.assertNotIn("/Users/", text, f"{rel}: contains an absolute home path")


class SyntaxTests(unittest.TestCase):
    def test_python_files_compile(self):
        with tempfile.TemporaryDirectory() as tmp:
            for p in files(".py"):
                py_compile.compile(str(p), cfile=str(Path(tmp) / (p.name + "c")), doraise=True)

    def test_notebook_code_cells_are_valid_python(self):
        for p in files(".ipynb"):
            nb = json.loads(p.read_text(encoding="utf-8"))
            for i, c in enumerate(nb["cells"]):
                if c["cell_type"] != "code":
                    continue
                lines = ["" if ln.lstrip().startswith(("%", "!")) else ln
                         for ln in "".join(c["source"]).splitlines()]
                try:
                    compile("\n".join(lines), f"{p.name}[cell {i}]", "exec")
                except SyntaxError as e:  # pragma: no cover
                    self.fail(f"{p.name} cell {i}: {e}")


if __name__ == "__main__":
    unittest.main()
