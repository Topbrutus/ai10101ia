#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation_tools.registry_tools import load_yaml, render_master_todo, save_text, verify_master_todo  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Génère ou vérifie docs/MASTER_TODO.md depuis le registre.")
    parser.add_argument("--registry", default=str(ROOT / "project" / "todo_registry.yaml"))
    parser.add_argument("--output", default=str(ROOT / "docs" / "MASTER_TODO.md"))
    parser.add_argument("--mode", choices=["check", "write"], default="check")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    data = load_yaml(args.registry)

    if args.mode == "write":
        content = render_master_todo(data)
        save_text(args.output, content)
        print(f"OK: checklist écrite dans {args.output}")
        return 0

    result = verify_master_todo(data, args.output)
    if result.errors:
        for error in result.errors:
            print(f"ERREUR: {error}", file=sys.stderr)
        return 1
    print(f"OK: checklist synchronisée ({args.output})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
