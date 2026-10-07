"""Run every pattern demo in order. Requires XAI_API_KEY to be set.

Each numbered file is a standalone script, so we execute them with runpy
(their names start with a digit and cannot be imported normally).

Usage:  python run_all.py
"""
from __future__ import annotations

import glob
import os
import runpy

from common import get_client


def main() -> None:
    # Fail fast with a clear message if the key is missing.
    get_client()
    for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "[0-9][0-9]_*.py"))):
        name = os.path.basename(path)
        print("\n" + "=" * 64 + f"\n  {name}\n" + "=" * 64)
        try:
            runpy.run_path(path, run_name="__main__")
        except Exception as e:  # keep going even if one demo errors
            print(f"   [skipped {name}] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
