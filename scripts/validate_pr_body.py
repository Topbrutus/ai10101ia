#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation_tools.pr_tools import read_body, validate_pr_body  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Valide le corps d'une pull request.")
    parser.add_argument("--body-file", help="Fichier contenant le corps de PR.")
    parser.add_argument("--body-text", help="Corps de PR transmis en ligne de commande.")
    parser.add_argument("--registry", default=str(ROOT / "project" / "todo_registry.yaml"))
    parser.add_argument("--policy", default=str(ROOT / "project" / "project_policy.yaml"))
    parser.add_argument("--changed-files-file", help="Fichier texte avec la liste des fichiers modifiés.")
    parser.add_argument("--head-ref", help="Nom de la branche source de la PR.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    body = read_body(args.body_file, args.body_text)

    changed_files: list[str] = []
    if args.changed_files_file:
        changed_files = [line.strip() for line in Path(args.changed_files_file).read_text(encoding="utf-8").splitlines() if line.strip()]

    errors = validate_pr_body(
        body=body,
        registry_path=args.registry,
        policy_path=args.policy,
        changed_files=changed_files,
        head_ref=args.head_ref,
    )
    if errors:
        for error in errors:
            print(f"ERREUR: {error}", file=sys.stderr)
        return 1

    print("OK: corps de PR valide")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
