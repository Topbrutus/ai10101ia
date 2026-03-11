#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation_tools.registry_tools import load_yaml, validate_registry_data, verify_master_todo  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Valide le registre machine des tâches.")
    parser.add_argument("--registry", default=str(ROOT / "project" / "todo_registry.yaml"), help="Chemin du registre YAML.")
    parser.add_argument(
        "--master-todo",
        default=str(ROOT / "docs" / "MASTER_TODO.md"),
        help="Chemin de la checklist maître Markdown.",
    )
    parser.add_argument(
        "--check-master",
        action="store_true",
        help="Vérifie que docs/MASTER_TODO.md est synchronisé avec le registre.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    data = load_yaml(args.registry)
    result = validate_registry_data(data)
    errors = list(result.errors)

    if args.check_master:
        sync_result = verify_master_todo(data, args.master_todo)
        errors.extend(sync_result.errors)

    if errors:
        for error in errors:
            print(f"ERREUR: {error}", file=sys.stderr)
        return 1

    print(f"OK: registre valide ({args.registry})")
    if args.check_master:
        print(f"OK: checklist synchronisée ({args.master_todo})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
