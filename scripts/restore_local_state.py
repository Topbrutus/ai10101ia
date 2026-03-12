#!/usr/bin/env python3
"""
restore_local_state.py — Restauration d'une sauvegarde locale AI10101IA (T0034).

Restaure les fichiers d'une sauvegarde vers un dossier cible, après vérification
du manifeste et contrôle des checksums.

Usage :
    python scripts/restore_local_state.py --backup backups/backup_20260312T010000Z
    python scripts/restore_local_state.py --backup backups/backup_20260312T010000Z --target /tmp/restore
    python scripts/restore_local_state.py --backup backups/backup_20260312T010000Z --target /tmp/restore --force
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_FILENAME = "manifest.json"


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    """Calcule le SHA-256 d'un fichier."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(backup_path: Path) -> dict:
    """Charge et valide la présence du manifeste dans la sauvegarde."""
    manifest_path = backup_path / MANIFEST_FILENAME
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifeste introuvable dans la sauvegarde : {manifest_path}\n"
            "Cette sauvegarde est invalide ou corrompue."
        )
    with manifest_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Logique principale
# ---------------------------------------------------------------------------

def run_restore(backup_path: Path, target: Path, force: bool = False, dry_run: bool = False) -> int:
    """Restaure une sauvegarde vers le dossier cible. Retourne 0 en cas de succès."""
    if not backup_path.is_dir():
        print(f"ERREUR : sauvegarde introuvable ou invalide : {backup_path}", file=sys.stderr)
        return 1

    try:
        manifest = _load_manifest(backup_path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 1

    backup_name = manifest.get("backup_name", backup_path.name)
    timestamp = manifest.get("timestamp_utc", "inconnu")
    fichiers = manifest.get("fichiers", [])

    print(f"Restauration AI10101IA — {backup_name}")
    print(f"  Horodatage : {timestamp}")
    print(f"  Fichiers   : {len(fichiers)}")
    print(f"  Cible      : {target}")

    # Vérification que la cible n'est pas la racine du dépôt sans --force
    if target.resolve() == ROOT.resolve() and not force:
        print(
            "ERREUR : la cible est la racine du dépôt. Utilisez --force pour écraser.",
            file=sys.stderr,
        )
        return 1

    # Vérification des checksums avant restauration
    print("  Vérification des checksums...")
    checksum_errors = 0
    for entry in fichiers:
        rel = entry.get("fichier", "")
        expected = entry.get("sha256", "")
        src = backup_path / rel
        if not src.exists():
            print(f"  ✗ Fichier absent dans la sauvegarde : {rel}", file=sys.stderr)
            checksum_errors += 1
            continue
        actual = _sha256(src)
        if actual != expected:
            print(f"  ✗ Checksum invalide pour {rel}", file=sys.stderr)
            checksum_errors += 1

    if checksum_errors > 0:
        print(f"ERREUR : {checksum_errors} fichier(s) avec checksum invalide. Restauration annulée.", file=sys.stderr)
        return 1

    print(f"  ✓ {len(fichiers)} checksum(s) vérifiés.")

    if dry_run:
        print("  (mode dry-run : aucune écriture)")
        return 0

    # Restauration
    target.mkdir(parents=True, exist_ok=True)
    errors = 0
    for entry in fichiers:
        rel = entry.get("fichier", "")
        src = backup_path / rel
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
        except OSError as exc:
            print(f"  ✗ Erreur lors de la restauration de {rel} : {exc}", file=sys.stderr)
            errors += 1

    if errors == 0:
        print(f"  ✓ Restauration terminée : {len(fichiers)} fichier(s) restauré(s).")
    else:
        print(f"  ⚠ Restauration partielle : {errors} erreur(s).", file=sys.stderr)
        return 1

    return 0


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Restaure une sauvegarde locale du dépôt AI10101IA (T0034)."
    )
    parser.add_argument(
        "--backup",
        required=True,
        metavar="DOSSIER",
        help="Chemin vers le dossier de sauvegarde (ex : backups/backup_20260312T010000Z).",
    )
    parser.add_argument(
        "--target",
        default=str(ROOT),
        metavar="DOSSIER",
        help=f"Dossier cible de restauration (défaut : racine du dépôt = {ROOT}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Permet d'écraser la racine du dépôt (opération destructive).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simule la restauration sans écrire de fichiers.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    backup_path = Path(args.backup)
    if not backup_path.is_absolute():
        backup_path = ROOT / backup_path
    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    return run_restore(
        backup_path=backup_path,
        target=target,
        force=args.force,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
