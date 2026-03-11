from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence
import re

import yaml

TASK_ID_RE = re.compile(r"^T\d{4}$")
ALLOWED_STATUSES = {"todo", "in_progress", "blocked", "done", "waived"}
REQUIRED_TASK_FIELDS = {
    "id",
    "titre",
    "phase",
    "description",
    "obligatoire",
    "dependances",
    "statut",
    "preuve_requise",
    "validation_requise",
    "livrables_attendus",
    "fichiers_impactes",
    "ordre",
}


@dataclass
class ValidationResult:
    errors: List[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_yaml(path: str | Path) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {file_path}")
    with file_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("Le YAML racine doit être un objet.")
    return data


def save_text(path: str | Path, content: str) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def normalize_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip() + "\n"


def task_map(tasks: Sequence[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {task["id"]: task for task in tasks}


def validate_registry_data(data: Dict[str, Any]) -> ValidationResult:
    errors: List[str] = []

    phases = data.get("phases")
    tasks = data.get("tasks")
    if not isinstance(phases, list) or not phases:
        return ValidationResult(["Le registre doit contenir une liste non vide 'phases'."])
    if not isinstance(tasks, list) or not tasks:
        return ValidationResult(["Le registre doit contenir une liste non vide 'tasks'."])

    phase_ids: List[str] = []
    phase_orders: set[int] = set()
    for index, phase in enumerate(phases, start=1):
        if not isinstance(phase, dict):
            errors.append(f"Phase #{index} invalide: chaque phase doit être un objet.")
            continue
        for field in ("id", "ordre", "titre"):
            if field not in phase:
                errors.append(f"Phase #{index} invalide: champ '{field}' manquant.")
        phase_id = phase.get("id")
        phase_order = phase.get("ordre")
        if phase_id:
            phase_ids.append(phase_id)
        if isinstance(phase_order, int):
            if phase_order in phase_orders:
                errors.append(f"Ordre de phase dupliqué: {phase_order}")
            else:
                phase_orders.add(phase_order)

    seen_ids: set[str] = set()
    seen_orders: set[int] = set()
    ids: List[str] = []
    orders: List[int] = []

    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            errors.append(f"Tâche #{index} invalide: chaque tâche doit être un objet.")
            continue
        missing = sorted(REQUIRED_TASK_FIELDS - task.keys())
        if missing:
            errors.append(f"Tâche #{index} invalide: champs manquants {missing}.")
            continue

        task_id = task["id"]
        if not isinstance(task_id, str) or not TASK_ID_RE.match(task_id):
            errors.append(f"Tâche #{index} invalide: id '{task_id}' ne respecte pas le format T0001.")
        elif task_id in seen_ids:
            errors.append(f"Identifiant dupliqué: {task_id}")
        else:
            seen_ids.add(task_id)
            ids.append(task_id)

        order = task["ordre"]
        if not isinstance(order, int) or order <= 0:
            errors.append(f"Tâche {task_id}: 'ordre' doit être un entier positif.")
        elif order in seen_orders:
            errors.append(f"Ordre de tâche dupliqué: {order}")
        else:
            seen_orders.add(order)
            orders.append(order)

        phase = task["phase"]
        if phase not in phase_ids:
            errors.append(f"Tâche {task_id}: phase inconnue '{phase}'.")

        status = task["statut"]
        if status not in ALLOWED_STATUSES:
            errors.append(f"Tâche {task_id}: statut invalide '{status}'.")

        if not isinstance(task["obligatoire"], bool):
            errors.append(f"Tâche {task_id}: 'obligatoire' doit être booléen.")

        for list_field in ("dependances", "livrables_attendus", "fichiers_impactes"):
            if not isinstance(task[list_field], list):
                errors.append(f"Tâche {task_id}: '{list_field}' doit être une liste.")

        for field in ("titre", "description", "preuve_requise", "validation_requise"):
            if not isinstance(task[field], str) or not task[field].strip():
                errors.append(f"Tâche {task_id}: '{field}' doit être une chaîne non vide.")

    if ids:
        expected_ids = [f"T{i:04d}" for i in range(1, len(ids) + 1)]
        if ids != expected_ids:
            errors.append(f"Numérotation non continue ou désordonnée. Attendu {expected_ids}, obtenu {ids}.")

    if orders:
        expected_orders = list(range(1, len(orders) + 1))
        if sorted(orders) != expected_orders:
            errors.append(f"Ordres de tâches incohérents. Attendu {expected_orders}, obtenu {sorted(orders)}.")

    lookup = task_map(tasks)
    for task in tasks:
        task_id = task.get("id", "<inconnue>")
        order = task.get("ordre", 0)
        dependencies = task.get("dependances", [])
        if isinstance(dependencies, list):
            for dep in dependencies:
                if dep not in lookup:
                    errors.append(f"Tâche {task_id}: dépendance inconnue '{dep}'.")
                    continue
                dep_order = lookup[dep]["ordre"]
                if dep_order >= order:
                    errors.append(f"Tâche {task_id}: dépendance '{dep}' hors ordre logique (ordre {dep_order} >= {order}).")

    return ValidationResult(errors)


def group_tasks_by_phase(data: Dict[str, Any]) -> List[tuple[Dict[str, Any], List[Dict[str, Any]]]]:
    phases = sorted(data["phases"], key=lambda item: item["ordre"])
    tasks = sorted(data["tasks"], key=lambda item: item["ordre"])
    grouped: List[tuple[Dict[str, Any], List[Dict[str, Any]]]] = []
    for phase in phases:
        grouped.append((phase, [task for task in tasks if task["phase"] == phase["id"]]))
    return grouped


def render_master_todo(data: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Checklist maître du projet")
    lines.append("")
    lines.append("> Document généré automatiquement depuis `project/todo_registry.yaml`. Ne pas modifier à la main.")
    lines.append("")
    metadata = data.get("metadata", {})
    if metadata:
        lines.append("## Métadonnées")
        lines.append("")
        lines.append(f"- **Nom** : {metadata.get('nom', 'N/A')}")
        lines.append(f"- **Description** : {metadata.get('description', 'N/A')}")
        lines.append(f"- **Propriétaire** : {metadata.get('owner', 'N/A')}")
        lines.append(f"- **Langue** : {metadata.get('langue', 'N/A')}")
        lines.append("")

    for phase, phase_tasks in group_tasks_by_phase(data):
        lines.append(f"## {phase['ordre']:02d}. {phase['titre']} (`{phase['id']}`)")
        lines.append("")
        lines.append(f"- **Gate de sortie** : {phase.get('gate_sortie', 'N/A')}")
        lines.append("")
        if not phase_tasks:
            lines.append("- [ ] Aucune tâche définie pour cette phase.")
            lines.append("")
            continue
        for task in phase_tasks:
            checkbox = "x" if task["statut"] == "done" else " "
            deps = ", ".join(task["dependances"]) if task["dependances"] else "Aucune"
            livrables = ", ".join(task["livrables_attendus"]) if task["livrables_attendus"] else "Aucun"
            impacts = ", ".join(task["fichiers_impactes"]) if task["fichiers_impactes"] else "Aucun"
            lines.append(f"- [{checkbox}] **{task['id']} — {task['titre']}**")
            lines.append(f"  - Ordre : {task['ordre']}")
            lines.append(f"  - Statut : `{task['statut']}`")
            lines.append(f"  - Obligatoire : `{str(task['obligatoire']).lower()}`")
            lines.append(f"  - Dépendances : {deps}")
            lines.append(f"  - Description : {task['description']}")
            lines.append(f"  - Preuve requise : {task['preuve_requise']}")
            lines.append(f"  - Validation requise : {task['validation_requise']}")
            lines.append(f"  - Livrables attendus : {livrables}")
            lines.append(f"  - Fichiers potentiellement impactés : {impacts}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def verify_master_todo(data: Dict[str, Any], master_path: str | Path) -> ValidationResult:
    expected = normalize_text(render_master_todo(data))
    actual = normalize_text(Path(master_path).read_text(encoding="utf-8"))
    if expected != actual:
        return ValidationResult(["docs/MASTER_TODO.md n'est pas synchronisé avec project/todo_registry.yaml."])
    return ValidationResult([])
