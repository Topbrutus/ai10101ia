from __future__ import annotations

from pathlib import Path
from typing import List, Sequence
import re

from foundation_tools.registry_tools import load_yaml

TASK_REF_RE = re.compile(r"\bT\d{4}\b")
HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
CHECKBOX_RE = re.compile(r"^- \[(?P<state>[ xX])\] (?P<label>.+)$", re.MULTILINE)
PLACEHOLDER_VALUES = {"", "_A compléter_", "A compléter", "À compléter", "TODO", "N/A", "n/a", "...", "Sans objet.", "Sans objet", "_Sans objet_"}


def read_body(body_file: str | Path | None = None, body_text: str | None = None) -> str:
    if body_text is not None:
        return body_text
    if body_file is None:
        raise ValueError("Un corps de PR doit être fourni.")
    return Path(body_file).read_text(encoding="utf-8")


def extract_task_ids(body: str) -> List[str]:
    return sorted(set(TASK_REF_RE.findall(body)))


def parse_sections(body: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group("title").strip()] = body[start:end].strip()
    return sections


def parse_checkboxes(body: str) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for match in CHECKBOX_RE.finditer(body):
        results[match.group("label").strip()] = match.group("state").lower() == "x"
    return results


def is_section_filled(value: str | None) -> bool:
    if value is None:
        return False
    cleaned = value.strip()
    if cleaned in PLACEHOLDER_VALUES:
        return False
    return any(line.strip() and line.strip() not in PLACEHOLDER_VALUES for line in cleaned.splitlines())


def validate_pr_body(
    *,
    body: str,
    registry_path: str | Path,
    policy_path: str | Path,
    changed_files: Sequence[str] | None = None,
    head_ref: str | None = None,
) -> list[str]:
    errors: list[str] = []
    policy = load_yaml(policy_path)
    registry = load_yaml(registry_path)
    task_lookup = {task["id"]: task for task in registry["tasks"]}
    sections = parse_sections(body)
    checkboxes = parse_checkboxes(body)
    task_ids = extract_task_ids(body)

    if not task_ids:
        errors.append("La pull request doit référencer au moins un identifiant de tâche T0001.")
    else:
        for task_id in task_ids:
            if task_id not in task_lookup:
                errors.append(f"L'identifiant de tâche '{task_id}' n'existe pas dans le registre.")

    for section_name in policy.get("required_pr_sections", []):
        if section_name not in sections:
            errors.append(f"Section PR manquante: '{section_name}'.")
        elif not is_section_filled(sections[section_name]):
            errors.append(f"Section PR vide ou insuffisante: '{section_name}'.")

    for checkbox in policy.get("required_pr_checkboxes", []):
        if checkbox not in checkboxes:
            errors.append(f"Case à cocher manquante: '{checkbox}'.")
        elif not checkboxes[checkbox]:
            errors.append(f"Case à cocher non validée: '{checkbox}'.")

    critical_files = set(policy.get("critical_files", []))
    changed_files = list(changed_files or [])
    if critical_files.intersection(changed_files):
        section_name = policy.get("justification_section_for_critical_changes")
        if not section_name or section_name not in sections or not is_section_filled(sections[section_name]):
            errors.append("Modification critique détectée sans justification explicite dans la PR.")

    if head_ref:
        if not head_ref.startswith("codex/"):
            single_pattern = re.compile(policy["branch_patterns"]["single_task"])
            multi_pattern = re.compile(policy["branch_patterns"]["multi_task"])
            maintenance_pattern = re.compile(policy["branch_patterns"]["maintenance"])
            if not (single_pattern.match(head_ref) or multi_pattern.match(head_ref) or maintenance_pattern.match(head_ref)):
                errors.append(
                    f"Nom de branche invalide '{head_ref}'. Utiliser task/T0001-slug, batch/T0001-T0002-slug ou maintenance/slug."
                )
            elif task_ids and not maintenance_pattern.match(head_ref) and not any(task_id in head_ref for task_id in task_ids):
                errors.append("Le nom de branche ne contient aucun identifiant de tâche référencé dans la PR.")

    return errors
