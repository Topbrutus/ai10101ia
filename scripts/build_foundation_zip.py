#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation_tools.zip_tools import build_zip  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Construit une archive ZIP propre du dépôt de fondation.")
    parser.add_argument("--root", default=str(ROOT), help="Racine du projet à archiver.")
    parser.add_argument("--output", default=str(ROOT / "dist" / "ai10101ia.zip"), help="Chemin du ZIP produit.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    output = build_zip(args.root, args.output)
    print(f"OK: archive créée -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
