"""
Tests de sauvegarde et restauration locale AI10101IA (T0034).

Couvre :
- création d'une sauvegarde
- présence du manifeste
- restauration round-trip dans un dossier temporaire
- échec propre si sauvegarde absente ou invalide
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# T0034 — Sauvegarde et restauration
# ---------------------------------------------------------------------------

class TestBackupLocalState:
    """Tests du script de sauvegarde (T0034)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "backup_local_state.py").exists()

    def test_backup_creates_directory(self, tmp_path: Path) -> None:
        result = run_script(
            "backup_local_state.py",
            "--output", str(tmp_path / "backups"),
            "--include", "docs", "project",
        )
        assert result.returncode == 0, f"Sauvegarde échouée :\n{result.stderr}"
        backups = list((tmp_path / "backups").iterdir())
        assert len(backups) == 1, "Un seul dossier de sauvegarde attendu."

    def test_backup_creates_manifest(self, tmp_path: Path) -> None:
        backup_dir = tmp_path / "backups"
        result = run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
        )
        assert result.returncode == 0, result.stderr
        backup_subdirs = list(backup_dir.iterdir())
        assert backup_subdirs, "Dossier de sauvegarde vide."
        manifest_path = backup_subdirs[0] / "manifest.json"
        assert manifest_path.exists(), f"Manifeste absent : {manifest_path}"

    def test_manifest_content(self, tmp_path: Path) -> None:
        backup_dir = tmp_path / "backups"
        result = run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
        )
        assert result.returncode == 0, result.stderr
        backup_subdirs = list(backup_dir.iterdir())
        manifest_path = backup_subdirs[0] / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest.get("version") == 1
        assert "timestamp_utc" in manifest
        assert "fichiers" in manifest
        assert isinstance(manifest["fichiers"], list)
        assert manifest["total_fichiers"] > 0
        # Chaque entrée doit avoir fichier + sha256
        for entry in manifest["fichiers"]:
            assert "fichier" in entry
            assert "sha256" in entry
            assert len(entry["sha256"]) == 64  # SHA-256 hex

    def test_backup_dry_run_creates_nothing(self, tmp_path: Path) -> None:
        backup_dir = tmp_path / "backups_dry"
        result = run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
            "--dry-run",
        )
        assert result.returncode == 0, result.stderr
        assert not backup_dir.exists(), "Dry-run ne doit pas créer de dossier."

    def test_backup_invalid_source_skipped(self, tmp_path: Path) -> None:
        backup_dir = tmp_path / "backups_partial"
        result = run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs", "nonexistent_source_xyz",
        )
        # Une source valide (docs) → succès malgré source invalide
        assert result.returncode == 0, result.stderr


class TestRestoreLocalState:
    """Tests du script de restauration (T0034)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "restore_local_state.py").exists()

    def test_restore_round_trip(self, tmp_path: Path) -> None:
        """Crée une sauvegarde puis restaure dans un dossier temporaire."""
        backup_dir = tmp_path / "backups"
        restore_dir = tmp_path / "restored"

        # Étape 1 : sauvegarde
        result = run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
        )
        assert result.returncode == 0, f"Sauvegarde échouée :\n{result.stderr}"

        backup_subdirs = list(backup_dir.iterdir())
        backup_path = backup_subdirs[0]

        # Étape 2 : restauration
        result = run_script(
            "restore_local_state.py",
            "--backup", str(backup_path),
            "--target", str(restore_dir),
        )
        assert result.returncode == 0, f"Restauration échouée :\n{result.stderr}"

        # Vérification : les fichiers du manifeste sont présents dans la cible
        manifest = json.loads((backup_path / "manifest.json").read_text(encoding="utf-8"))
        for entry in manifest["fichiers"]:
            restored_file = restore_dir / entry["fichier"]
            assert restored_file.exists(), f"Fichier non restauré : {entry['fichier']}"

    def test_restore_fails_without_backup(self, tmp_path: Path) -> None:
        result = run_script(
            "restore_local_state.py",
            "--backup", str(tmp_path / "nonexistent_backup"),
            "--target", str(tmp_path / "restore"),
        )
        assert result.returncode != 0, "Doit échouer si la sauvegarde est absente."

    def test_restore_fails_without_manifest(self, tmp_path: Path) -> None:
        fake_backup = tmp_path / "fake_backup"
        fake_backup.mkdir()
        # Pas de manifest.json
        result = run_script(
            "restore_local_state.py",
            "--backup", str(fake_backup),
            "--target", str(tmp_path / "restore"),
        )
        assert result.returncode != 0, "Doit échouer si le manifeste est absent."

    def test_restore_refuses_repo_root_without_force(self, tmp_path: Path) -> None:
        """La restauration vers la racine du dépôt sans --force doit échouer."""
        backup_dir = tmp_path / "backups"
        run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
        )
        backup_subdirs = list(backup_dir.iterdir())
        backup_path = backup_subdirs[0]

        result = run_script(
            "restore_local_state.py",
            "--backup", str(backup_path),
            "--target", str(ROOT),  # racine du dépôt, sans --force
        )
        assert result.returncode != 0, "Doit refuser sans --force."

    def test_restore_dry_run(self, tmp_path: Path) -> None:
        backup_dir = tmp_path / "backups"
        restore_dir = tmp_path / "restore_dry"
        run_script(
            "backup_local_state.py",
            "--output", str(backup_dir),
            "--include", "docs",
        )
        backup_subdirs = list(backup_dir.iterdir())
        backup_path = backup_subdirs[0]

        result = run_script(
            "restore_local_state.py",
            "--backup", str(backup_path),
            "--target", str(restore_dir),
            "--dry-run",
        )
        assert result.returncode == 0, result.stderr
        # Aucun fichier ne doit avoir été écrit
        assert not restore_dir.exists() or not any(restore_dir.iterdir()), (
            "Dry-run ne doit pas créer de fichiers."
        )
