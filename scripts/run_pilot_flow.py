#!/usr/bin/env python3
"""
run_pilot_flow.py — Flux bout-en-bout pilote AI10101IA (T0033).

Démontre un flux complet et traçable sur le dataset bootstrap :
1. Chargement du dataset
2. Validation du domaine
3. Consultation d'entités (liste et affichage)
4. Vérification des preuves rattachées
5. Reconstruction du multi-index pilote
6. Génération d'une vue d'audit
7. Vérification de cohérence globale

Usage :
    python scripts/run_pilot_flow.py
    python scripts/run_pilot_flow.py --audit-output /tmp/pilot_audit.md
    python scripts/run_pilot_flow.py --verbose
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

ENTITIES_PATH = ROOT / "project" / "bootstrap_entities.yaml"
PROOFS_PATH = ROOT / "project" / "bootstrap_proofs.yaml"
EVENTS_PATH = ROOT / "project" / "bootstrap_events.yaml"
ENTITY_SECTIONS = ["hub", "dieux", "academies", "robots", "lignees", "regles", "commandes"]


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _step(num: int, title: str) -> None:
    print(f"\n[Étape {num}] {title}")
    print("-" * (len(title) + 12))


def _ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def _fail(msg: str) -> None:
    print(f"  ✗ {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Étapes du flux
# ---------------------------------------------------------------------------

def step_load(entities: Dict[str, Any], proofs: Dict[str, Any], events: Dict[str, Any]) -> bool:
    _step(1, "Chargement du dataset bootstrap")
    hub_id = entities.get("hub", {}).get("id", "absent")
    _ok(f"Hub chargé : {hub_id}")
    for section in ENTITY_SECTIONS[1:]:
        items = entities.get(section, [])
        if isinstance(items, dict):
            items = [items]
        _ok(f"{section.capitalize():<12} : {len(items)} entité(s)")
    _ok(f"Preuves      : {len(proofs.get('preuves', []))}")
    _ok(f"Événements   : {len(events.get('evenements', []))}")
    return True


def step_validate() -> bool:
    _step(2, "Validation du domaine")
    script = ROOT / "scripts" / "validate_domain_assets.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        for line in result.stdout.strip().splitlines():
            _ok(line)
        return True
    else:
        for line in result.stderr.strip().splitlines():
            _fail(line)
        return False


def step_consult_entities(entities: Dict[str, Any], verbose: bool) -> bool:
    _step(3, "Consultation d'entités")
    robots = entities.get("robots", [])
    if not robots:
        _fail("Aucun robot trouvé dans le dataset.")
        return False
    first_robot = robots[0]
    rid = first_robot.get("id", "<inconnu>")
    nom = first_robot.get("nom", "")
    classe = first_robot.get("classe", "")
    _ok(f"Robot consulté : {rid} | {nom} | classe={classe}")
    if verbose:
        for robot in robots:
            scores = robot.get("scores", {})
            print(
                f"    {robot.get('id'):<20} {robot.get('nom'):<20}"
                f" points={scores.get('points', 0):>5}"
            )
    _ok(f"Liste des robots : {len(robots)} robot(s) consulté(s).")
    return True


def step_verify_proofs(
    proofs: Dict[str, Any],
    entities: Dict[str, Any],
) -> bool:
    _step(4, "Vérification des preuves rattachées")
    preuves = proofs.get("preuves", [])
    if not preuves:
        _fail("Aucune preuve trouvée.")
        return False

    all_entity_ids: set[str] = set()
    for section in ENTITY_SECTIONS:
        raw = entities.get(section)
        if raw is None:
            continue
        if isinstance(raw, dict):
            raw = [raw]
        for item in raw:
            eid = item.get("id")
            if eid:
                all_entity_ids.add(eid)

    issues = 0
    for preuve in preuves:
        pid = preuve.get("id", "<inconnu>")
        entite_id = preuve.get("entite_id", "")
        if entite_id and not entite_id.startswith("TACHE-") and entite_id not in all_entity_ids:
            _fail(f"Preuve {pid} : entite_id '{entite_id}' introuvable.")
            issues += 1

    if issues == 0:
        _ok(f"{len(preuves)} preuve(s) vérifiée(s), aucune référence cassée.")
        return True
    return False


def step_rebuild_index(entities: Dict[str, Any]) -> bool:
    _step(5, "Reconstruction du multi-index pilote")
    all_entities: Dict[str, Dict[str, Any]] = {}
    for section in ENTITY_SECTIONS:
        raw = entities.get(section)
        if raw is None:
            continue
        if isinstance(raw, dict):
            raw = [raw]
        for item in raw:
            eid = item.get("id")
            if eid:
                all_entities[eid] = item

    index_type: Dict[str, int] = {}
    index_filiation: List[str] = []
    for eid, entity in all_entities.items():
        etype = entity.get("type", "INCONNU")
        index_type[etype] = index_type.get(etype, 0) + 1
        for rel in entity.get("relations", []):
            if rel.get("type") == "descendant_de":
                index_filiation.append(f"{eid} → {rel.get('cible', '')}")

    _ok(f"Index d'identité : {len(all_entities)} entrée(s)")
    for etype, count in index_type.items():
        _ok(f"  {etype:<12} : {count}")
    if index_filiation:
        _ok(f"Index de filiation : {len(index_filiation)} relation(s)")
        for rel in index_filiation:
            _ok(f"  {rel}")
    else:
        _ok("Index de filiation : vide")
    return True


def step_generate_audit(audit_output: str) -> bool:
    _step(6, "Génération de la vue d'audit")
    script = ROOT / "scripts" / "build_audit_report.py"
    cmd = [sys.executable, str(script), "--format", "markdown"]
    if audit_output:
        cmd += ["--output", audit_output]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.strip().splitlines():
            _ok(line)
        return True
    else:
        for line in result.stderr.strip().splitlines():
            _fail(line)
        return False


def step_verify_coherence(entities: Dict[str, Any], proofs: Dict[str, Any]) -> bool:
    _step(7, "Vérification de cohérence globale")
    issues = 0

    # Vérification que tous les robots ont des scores valides
    for robot in entities.get("robots", []):
        rid = robot.get("id", "<inconnu>")
        scores = robot.get("scores", {})
        for champ in ("points", "prestige", "credit_social"):
            val = scores.get(champ)
            if val is None or (isinstance(val, (int, float)) and val < 0):
                _fail(f"Robot {rid} : score '{champ}' invalide.")
                issues += 1

    # Vérification que les preuves ne sont pas en doublon
    seen_ids: set[str] = set()
    for preuve in proofs.get("preuves", []):
        pid = preuve.get("id", "<inconnu>")
        if pid in seen_ids:
            _fail(f"Preuve dupliquée : {pid}")
            issues += 1
        seen_ids.add(pid)

    if issues == 0:
        _ok("Cohérence globale validée. Aucune anomalie détectée.")
        return True
    return False


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Flux bout-en-bout pilote AI10101IA."
    )
    parser.add_argument(
        "--audit-output",
        default=None,
        help="Fichier de sortie pour le rapport d'audit (ex: /tmp/pilot_audit.md).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Affiche plus de détails pour certaines étapes.",
    )
    parser.add_argument(
        "--entities",
        default=str(ENTITIES_PATH),
        help="Chemin vers bootstrap_entities.yaml.",
    )
    parser.add_argument(
        "--proofs",
        default=str(PROOFS_PATH),
        help="Chemin vers bootstrap_proofs.yaml.",
    )
    parser.add_argument(
        "--events",
        default=str(EVENTS_PATH),
        help="Chemin vers bootstrap_events.yaml.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════╗")
    print("║    Flux pilote bout-en-bout — AI10101IA       ║")
    print("╚══════════════════════════════════════════════╝")

    try:
        entities = _load_yaml(Path(args.entities))
        proofs = _load_yaml(Path(args.proofs))
        events = _load_yaml(Path(args.events))
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1

    steps: List[tuple[str, bool]] = []

    def run(name: str, ok: bool) -> None:
        steps.append((name, ok))

    run("Chargement", step_load(entities, proofs, events))
    run("Validation", step_validate())
    run("Consultation", step_consult_entities(entities, args.verbose))
    run("Preuves", step_verify_proofs(proofs, entities))
    run("Multi-index", step_rebuild_index(entities))
    run("Audit", step_generate_audit(args.audit_output or ""))
    run("Cohérence", step_verify_coherence(entities, proofs))

    print("\n╔══════════════════════════════════════════════╗")
    print("║    Bilan du flux pilote                       ║")
    print("╚══════════════════════════════════════════════╝")
    all_ok = True
    for name, ok in steps:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}")
        if not ok:
            all_ok = False

    if all_ok:
        print("\nRÉSULTAT: flux pilote réussi. Toutes les étapes sont OK.")
        return 0
    else:
        failed = [name for name, ok in steps if not ok]
        print(f"\nRÉSULTAT: flux pilote échoué. Étapes KO : {', '.join(failed)}.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
