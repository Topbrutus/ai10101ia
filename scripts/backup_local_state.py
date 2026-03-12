#!/usr/bin/env python3
"""
backup_local_state.py — Sauvegarde locale de l'état du dépôt AI10101IA (T0034).

Crée une sauvegarde horodatée dans un dossier dédié, avec un manifeste
listant les fichiers inclus et leurs checksums SHA-256.

Usage :
    python scripts/backup_local_state.py
    python scripts/backup_local_state.py --output /tmp/mes_sauvegardes
    python scripts/backup_local_state.py --include docs project scripts
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Dossiers sauvegardés par défaut (relatifs à la racine du dépôt)
DEFAULT_SOURCES = ["docs", "project", "scripts", "src", "tests", "Makefile", "pyproject.toml", "requirements.txt"]
DEFAULT_BACKUP_DIR = ROOT / "backups"
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


def _collect_files(sources: list[Path]) -> list[Path]:
    """Retourne tous les fichiers réguliers dans les sources données."""
    files: list[Path] = []
    for source in sources:
        if source.is_file():
            files.append(source)
        elif source.is_dir():
            files.extend(sorted(source.rglob("*")))
    return [f for f in files if f.is_file()]


def _relative(path: Path, base: Path) -> str:
    """Retourne le chemin relatif par rapport à la base."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# Logique principale
# ---------------------------------------------------------------------------

def run_backup(sources: list[str], backup_dir: Path, dry_run: bool = False) -> int:
    """Effectue la sauvegarde et retourne 0 en cas de succès."""
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_name = f"backup_{timestamp}"
    dest = backup_dir / backup_name

    source_paths = []
    for s in sources:
        candidate = ROOT / s if not Path(s).is_absolute() else Path(s)
        if not candidate.exists():
            print(f"  ⚠  Source introuvable, ignorée : {candidate}", file=sys.stderr)
        else:
            source_paths.append(candidate)

    if not source_paths:
        print("ERREUR : aucune source valide à sauvegarder.", file=sys.stderr)
        return 1

    all_files = _collect_files(source_paths)
    if not all_files:
        print("ERREUR : aucun fichier trouvé dans les sources.", file=sys.stderr)
        return 1

    print(f"Sauvegarde AI10101IA — {timestamp}")
    print(f"  Sources   : {', '.join(sources)}")
    print(f"  Fichiers  : {len(all_files)}")
    print(f"  Dossier   : {dest}")

    if dry_run:
        print("  (mode dry-run : aucune écriture)")
        return 0

    dest.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict] = []
    errors = 0

    for src_file in all_files:
        rel = _relative(src_file, ROOT)
        dst_file = dest / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src_file, dst_file)
            checksum = _sha256(dst_file)
            manifest_entries.append({"fichier": rel, "sha256": checksum})
        except OSError as exc:
            print(f"  ✗ Erreur lors de la copie de {rel} : {exc}", file=sys.stderr)
            errors += 1

    manifest = {
        "version": 1,
        "backup_name": backup_name,
        "timestamp_utc": timestamp,
        "sources": sources,
        "fichiers": manifest_entries,
        "total_fichiers": len(manifest_entries),
        "erreurs": errors,
    }
    manifest_path = dest / MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    if errors == 0:
        print(f"  ✓ Sauvegarde terminée : {backup_name}")
        print(f"  ✓ Manifeste écrit    : {manifest_path}")
    else:
        print(f"  ⚠ Sauvegarde partielle : {errors} erreur(s). Manifeste : {manifest_path}", file=sys.stderr)
        return 1

    return 0


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sauvegarde locale de l'état du dépôt AI10101IA (T0034)."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_BACKUP_DIR),
        help=f"Dossier de destination des sauvegardes (défaut : {DEFAULT_BACKUP_DIR}).",
    )
    parser.add_argument(
        "--include",
        nargs="+",
        default=DEFAULT_SOURCES,
        metavar="SOURCE",
        help="Fichiers ou dossiers à inclure (relatifs à la racine du dépôt).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simule la sauvegarde sans écrire de fichiers.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_backup(
        sources=args.include,
        backup_dir=Path(args.output),
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
