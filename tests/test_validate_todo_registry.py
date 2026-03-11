from pathlib import Path
import yaml

from foundation_tools.registry_tools import load_yaml, render_master_todo, validate_registry_data, verify_master_todo


def make_registry() -> dict:
    return {
        "version": 1,
        "metadata": {"nom": "Test", "description": "Test", "owner": "x", "langue": "fr"},
        "phases": [
            {"id": "P1", "ordre": 1, "titre": "Phase 1"},
            {"id": "P2", "ordre": 2, "titre": "Phase 2"},
        ],
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
                "phase": "P2",
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
        ],
    }


def test_registry_valid(tmp_path: Path) -> None:
    registry = make_registry()
    path = tmp_path / "registry.yaml"
    path.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=True), encoding="utf-8")
    data = load_yaml(path)
    result = validate_registry_data(data)
    assert result.ok


def test_registry_duplicate_id_rejected() -> None:
    registry = make_registry()
    registry["tasks"][1]["id"] = "T0001"
    result = validate_registry_data(registry)
    assert not result.ok
    assert any("Identifiant dupliqué" in err for err in result.errors)


def test_registry_broken_dependency_rejected() -> None:
    registry = make_registry()
    registry["tasks"][1]["dependances"] = ["T9999"]
    result = validate_registry_data(registry)
    assert not result.ok
    assert any("dépendance inconnue" in err for err in result.errors)


def test_registry_inconsistent_numbering_rejected() -> None:
    registry = make_registry()
    registry["tasks"][1]["id"] = "T0003"
    result = validate_registry_data(registry)
    assert not result.ok
    assert any("Numérotation non continue" in err for err in result.errors)


def test_master_sync_verification(tmp_path: Path) -> None:
    registry = make_registry()
    master = tmp_path / "MASTER_TODO.md"
    master.write_text(render_master_todo(registry), encoding="utf-8")
    result = verify_master_todo(registry, master)
    assert result.ok
