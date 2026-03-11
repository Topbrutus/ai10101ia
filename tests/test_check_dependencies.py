from pathlib import Path
import os
import subprocess
import sys
import yaml

from foundation_tools.pr_tools import extract_task_ids, validate_pr_body


def make_registry(tmp_path: Path) -> tuple[Path, Path]:
    registry = {
        "version": 1,
        "metadata": {"nom": "Test", "description": "Desc", "owner": "Topbrutus", "langue": "fr"},
        "phases": [{"id": "P1", "ordre": 1, "titre": "Phase 1"}],
        "tasks": [
            {
                "id": "T0001",
                "ordre": 1,
                "phase": "P1",
                "titre": "Tâche 1",
                "description": "Desc",
                "obligatoire": True,
                "dependances": [],
                "statut": "done",
                "preuve_requise": "preuve",
                "validation_requise": "validation",
                "livrables_attendus": ["a.md"],
                "fichiers_impactes": ["a.md"],
            },
            {
                "id": "T0002",
                "ordre": 2,
                "phase": "P1",
                "titre": "Tâche 2",
                "description": "Desc",
                "obligatoire": True,
                "dependances": ["T0001"],
                "statut": "todo",
                "preuve_requise": "preuve",
                "validation_requise": "validation",
                "livrables_attendus": ["b.md"],
                "fichiers_impactes": ["b.md"],
            },
            {
                "id": "T0003",
                "ordre": 3,
                "phase": "P1",
                "titre": "Tâche 3",
                "description": "Desc",
                "obligatoire": True,
                "dependances": ["T0002"],
                "statut": "todo",
                "preuve_requise": "preuve",
                "validation_requise": "validation",
                "livrables_attendus": ["c.md"],
                "fichiers_impactes": ["c.md"],
            },
        ],
    }
    policy = {
        "branch_patterns": {
            "single_task": r"^task/(T\d{4})-[a-z0-9._-]+$",
            "multi_task": r"^batch/(T\d{4}(?:-T\d{4})+)-[a-z0-9._-]+$",
            "maintenance": r"^maintenance/[a-z0-9._-]+$",
        },
        "required_pr_sections": [
            "Tâches liées",
            "Objectif",
            "Portée",
            "Risques",
            "Preuves",
            "Validations",
            "Impacts fichiers",
            "Plan de rollback",
        ],
        "required_pr_checkboxes": [
            "Je confirme avoir lu docs/MASTER_TODO.md, project/todo_registry.yaml et docs/WORKFLOW_RULES.md.",
            "Je confirme ne pas avoir contourné la checklist maître.",
            "Je confirme que les dépendances des tâches référencées sont satisfaites ou explicitement levées.",
        ],
        "critical_files": ["project/todo_registry.yaml"],
        "justification_section_for_critical_changes": "Justification des modifications critiques",
        "done_statuses_for_dependencies": ["done", "waived"],
    }
    registry_path = tmp_path / "registry.yaml"
    policy_path = tmp_path / "policy.yaml"
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=True), encoding="utf-8")
    policy_path.write_text(yaml.safe_dump(policy, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return registry_path, policy_path


def valid_pr_body() -> str:
    return """## Tâches liées

- T0002

## Objectif

Faire un changement.

## Portée

Portée limitée.

## Risques

Faibles.

## Preuves

pytest -q

## Validations

Revue documentaire.

## Impacts fichiers

scripts/x.py

## Plan de rollback

git revert.

## Justification des modifications critiques

Sans objet.

## Checklist de conformité

- [x] Je confirme avoir lu docs/MASTER_TODO.md, project/todo_registry.yaml et docs/WORKFLOW_RULES.md.
- [x] Je confirme ne pas avoir contourné la checklist maître.
- [x] Je confirme que les dépendances des tâches référencées sont satisfaites ou explicitement levées.
"""


def test_extract_task_ids() -> None:
    body = "Cette PR traite T0001 et T0003."
    assert extract_task_ids(body) == ["T0001", "T0003"]


def test_pr_without_task_id_rejected(tmp_path: Path) -> None:
    registry_path, policy_path = make_registry(tmp_path)
    body = valid_pr_body().replace("T0002", "")
    errors = validate_pr_body(
        body=body,
        registry_path=registry_path,
        policy_path=policy_path,
        changed_files=[],
        head_ref="task/T0002-demo",
    )
    assert any("au moins un identifiant" in err for err in errors)


def test_check_dependencies_script_rejects_unsatisfied_dependency(tmp_path: Path) -> None:
    registry_path, policy_path = make_registry(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_dependencies.py",
            "--registry",
            str(registry_path),
            "--policy",
            str(policy_path),
            "--task-ids",
            "T0003",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, **{"PYTHONPATH": str(Path(__file__).resolve().parents[1] / 'src')}},
    )
    assert result.returncode == 1
    assert "non satisfaite" in result.stderr
