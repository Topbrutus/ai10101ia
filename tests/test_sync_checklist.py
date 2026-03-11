from pathlib import Path

from foundation_tools.registry_tools import render_master_todo, verify_master_todo


def test_sync_checklist_roundtrip(tmp_path: Path) -> None:
    registry = {
        "metadata": {"nom": "Projet", "description": "Desc", "owner": "Topbrutus", "langue": "fr"},
        "phases": [{"id": "P1", "ordre": 1, "titre": "Phase 1", "gate_sortie": "OK"}],
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
                "livrables_attendus": ["README.md"],
                "fichiers_impactes": ["README.md"],
            }
        ],
    }
    content = render_master_todo(registry)
    path = tmp_path / "MASTER_TODO.md"
    path.write_text(content, encoding="utf-8")
    result = verify_master_todo(registry, path)
    assert result.ok
