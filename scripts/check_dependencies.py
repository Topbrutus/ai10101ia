#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation_tools.pr_tools import extract_task_ids, read_body  # noqa: E402
from foundation_tools.registry_tools import load_yaml  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vérifie que les dépendances des tâches référencées sont satisfaites.")
    parser.add_argument("--registry", default=str(ROOT / "project" / "todo_registry.yaml"))
    parser.add_argument("--policy", default=str(ROOT / "project" / "project_policy.yaml"))
    parser.add_argument("--task-ids", nargs="*", help="Liste explicite d'identifiants de tâche.")
    parser.add_argument("--body-file", help="Corps de PR pour extraire les identifiants de tâche.")
    parser.add_argument("--body-text", help="Texte brut pour extraire les identifiants de tâche.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    registry = load_yaml(args.registry)
    policy = load_yaml(args.policy)
    done_statuses = set(policy.get("done_statuses_for_dependencies", ["done", "waived"]))
    tasks = {task["id"]: task for task in registry["tasks"]}

    task_ids = set(args.task_ids or [])
    if args.body_file or args.body_text:
        task_ids.update(extract_task_ids(read_body(args.body_file, args.body_text)))

    if not task_ids:
        print("ERREUR: aucune tâche à vérifier.", file=sys.stderr)
        return 1

    errors: list[str] = []
    for task_id in sorted(task_ids):
        if task_id not in tasks:
            errors.append(f"Tâche inconnue: {task_id}")
            continue
        task = tasks[task_id]
        for dep in task.get("dependances", []):
            dep_task = tasks.get(dep)
            if dep_task is None:
                errors.append(f"Tâche {task_id}: dépendance inconnue '{dep}'.")
                continue
            if dep_task["statut"] not in done_statuses:
                errors.append(
                    f"Tâche {task_id}: dépendance '{dep}' non satisfaite (statut actuel: {dep_task['statut']})."
                )

    if errors:
        for error in errors:
            print(f"ERREUR: {error}", file=sys.stderr)
        return 1

    print("OK: dépendances satisfaites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
