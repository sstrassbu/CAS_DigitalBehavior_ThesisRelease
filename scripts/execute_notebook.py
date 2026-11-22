"""Execute a notebook in place with an explicit kernel working directory."""

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    kernel_cwd = args.cwd.resolve()
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name=notebook.metadata.get("kernelspec", {}).get("name", "python3"),
    )
    executed = client.execute(cwd=str(kernel_cwd))
    nbformat.write(executed, notebook_path)
    print(f"Executed {notebook_path} with kernel cwd {kernel_cwd}")


if __name__ == "__main__":
    main()
