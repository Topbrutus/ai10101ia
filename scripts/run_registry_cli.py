#!/usr/bin/env python3
"""
run_registry_cli.py — CLI de pilotage du registre AI10101IA (T0031).

Commandes disponibles :
    load        Charge et résume le dataset bootstrap
    validate    Valide le domaine (entités, preuves, événements)
    show <id>   Affiche une entité par son identifiant canonique
    list <type> Liste toutes les entités d'un type donné
    index       Reconstruit et affiche le multi-index pilote
    audit       Génère une vue d'audit résumée (équivalent de build_audit_report)

Usage :
    python scripts/run_registry_cli.py load
    python scripts/run_registry_cli.py validate
    python scripts/run_registry_cli.py show ROBOT-0001
    python scripts/run_registry_cli.py list ROBOT
    python scripts/run_registry_cli.py index
    python scripts/run_registry_cli.py audit
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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
# Chargement
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_all() -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    return _load_yaml(ENTITIES_PATH), _load_yaml(PROOFS_PATH), _load_yaml(EVENTS_PATH)


def collect_entities(entities: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Retourne un mapping id → entité pour toutes les entités."""
    result: Dict[str, Dict[str, Any]] = {}
    for section in ENTITY_SECTIONS:
        raw = entities.get(section)
        if raw is None:
            continue
        if isinstance(raw, dict):
            raw = [raw]
        for item in raw:
            eid = item.get("id")
            if eid:
                result[eid] = item
    return result


# ---------------------------------------------------------------------------
# Commandes CLI
# ---------------------------------------------------------------------------

def cmd_load(entities: Dict[str, Any], proofs: Dict[str, Any], events: Dict[str, Any]) -> int:
    print("=== Chargement du dataset bootstrap ===")
    print(f"  Hub    : {entities.get('hub', {}).get('id', 'absent')}")
    for section in ENTITY_SECTIONS[1:]:
        items = entities.get(section, [])
        if isinstance(items, dict):
            items = [items]
        print(f"  {section.capitalize():<12}: {len(items)} entité(s)")
    preuves = proofs.get("preuves", [])
    evenements = events.get("evenements", [])
    print(f"  Preuves      : {len(preuves)}")
    print(f"  Événements   : {len(evenements)}")
    print("OK: dataset chargé.")
    return 0


def cmd_validate() -> int:
    script = ROOT / "scripts" / "validate_domain_assets.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=False,
    )
    return result.returncode


def cmd_show(entity_id: str, entities: Dict[str, Any]) -> int:
    all_entities = collect_entities(entities)
    entity = all_entities.get(entity_id)
    if entity is None:
        print(f"ERREUR: entité '{entity_id}' introuvable.", file=sys.stderr)
        return 1
    print(f"=== {entity_id} ===")
    print(yaml.dump(entity, allow_unicode=True, sort_keys=False, default_flow_style=False))
    return 0


def cmd_list(entity_type: str, entities: Dict[str, Any]) -> int:
    etype = entity_type.upper()
    section_map = {
        "HUB": "hub",
        "DIEU": "dieux",
        "ACADEMIE": "academies",
        "ROBOT": "robots",
        "LIGNEE": "lignees",
        "REGLE": "regles",
        "COMMANDE": "commandes",
    }
    section = section_map.get(etype)
    if section is None:
        print(
            f"ERREUR: type '{etype}' inconnu. Types valides : {', '.join(section_map)}.",
            file=sys.stderr,
        )
        return 1
    items = entities.get(section, [])
    if isinstance(items, dict):
        items = [items]
    if not items:
        print(f"Aucune entité de type '{etype}'.")
        return 0
    print(f"=== {etype} ({len(items)} entité(s)) ===")
    for item in items:
        eid = item.get("id", "<inconnu>")
        nom = item.get("nom") or item.get("slash") or item.get("titre", "")
        statut = item.get("statut", "")
        print(f"  {eid:<20} {nom:<35} [{statut}]")
    return 0


def cmd_index(entities: Dict[str, Any]) -> int:
    all_entities = collect_entities(entities)
    index_identite: Dict[str, Dict[str, Any]] = {}
    index_type: Dict[str, List[str]] = {}
    index_statut: Dict[str, List[str]] = {}

    for eid, entity in all_entities.items():
        etype = entity.get("type", "INCONNU")
        statut = entity.get("statut", "inconnu")
        index_identite[eid] = {"type": etype, "statut": statut, "version": entity.get("version", 1)}
        index_type.setdefault(etype, []).append(eid)
        index_statut.setdefault(statut, []).append(eid)

    # Index de filiation
    index_filiation: Dict[str, List[str]] = {}
    for eid, entity in all_entities.items():
        for rel in entity.get("relations", []):
            if rel.get("type") == "descendant_de":
                parent = rel.get("cible", "")
                index_filiation.setdefault(parent, []).append(eid)

    # Index des scores
    index_scores: List[Dict[str, Any]] = []
    for eid, entity in all_entities.items():
        scores = entity.get("scores")
        if scores:
            index_scores.append({"id": eid, **scores})
    index_scores.sort(key=lambda r: r.get("points", 0), reverse=True)

    print("=== Multi-index pilote ===")
    print(f"\n[index_identite] {len(index_identite)} entrée(s)")
    for eid, info in list(index_identite.items())[:5]:
        print(f"  {eid:<20} type={info['type']:<12} statut={info['statut']}")
    if len(index_identite) > 5:
        print(f"  ... ({len(index_identite) - 5} de plus)")

    print(f"\n[index_type]")
    for etype, ids in index_type.items():
        print(f"  {etype:<12} : {ids}")

    print(f"\n[index_statut]")
    for statut, ids in index_statut.items():
        print(f"  {statut:<12} : {len(ids)} entité(s)")

    print(f"\n[index_filiation]")
    if index_filiation:
        for parent, enfants in index_filiation.items():
            print(f"  {parent} → {enfants}")
    else:
        print("  (aucune relation de filiation)")

    print(f"\n[index_scores] (top par points)")
    for entry in index_scores[:5]:
        print(
            f"  {entry['id']:<20} points={entry.get('points',0):>5}"
            f"  prestige={entry.get('prestige',0):>4}"
            f"  credit={entry.get('credit_social',0):>4}"
        )

    print("\nOK: multi-index reconstruit.")
    return 0


def cmd_audit(entities: Dict[str, Any], proofs: Dict[str, Any], events: Dict[str, Any]) -> int:
    script = ROOT / "scripts" / "build_audit_report.py"
    if not script.exists():
        print("ERREUR: scripts/build_audit_report.py introuvable.", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=False,
    )
    return result.returncode


# ---------------------------------------------------------------------------
# Parser principal
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI de pilotage du registre AI10101IA.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commandes :
  load              Charge et résume le dataset bootstrap
  validate          Valide le domaine (entités, preuves, événements)
  show <id>         Affiche une entité par son identifiant canonique
  list <type>       Liste les entités d'un type (ROBOT, DIEU, ACADEMIE, ...)
  index             Reconstruit et affiche le multi-index pilote
  audit             Génère une vue d'audit résumée
        """,
    )
    parser.add_argument(
        "commande",
        choices=["load", "validate", "show", "list", "index", "audit"],
        help="Commande à exécuter.",
    )
    parser.add_argument(
        "argument",
        nargs="?",
        default=None,
        help="Argument de la commande (id ou type selon la commande).",
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

    # Chargement des fichiers (sauf pour validate qui délègue)
    if args.commande != "validate":
        try:
            entities = _load_yaml(Path(args.entities))
            proofs = _load_yaml(Path(args.proofs))
            events = _load_yaml(Path(args.events))
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERREUR: {exc}", file=sys.stderr)
            return 1
    else:
        entities = proofs = events = {}

    if args.commande == "load":
        return cmd_load(entities, proofs, events)
    elif args.commande == "validate":
        return cmd_validate()
    elif args.commande == "show":
        if not args.argument:
            print("ERREUR: 'show' requiert un identifiant d'entité.", file=sys.stderr)
            return 1
        return cmd_show(args.argument, entities)
    elif args.commande == "list":
        if not args.argument:
            print("ERREUR: 'list' requiert un type d'entité.", file=sys.stderr)
            return 1
        return cmd_list(args.argument, entities)
    elif args.commande == "index":
        return cmd_index(entities)
    elif args.commande == "audit":
        return cmd_audit(entities, proofs, events)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
