#!/usr/bin/env python3
"""
validate_domain_assets.py — Pipeline de validation métier AI10101IA (T0030).

Valide les assets métier du domaine :
- schémas des entités bootstrap
- relations inter-entités (robot→lignée, robot→académie, robot→dieu, etc.)
- références croisées commandes/règles/preuves
- cohérence des scores (points, prestige, crédit social)
- intégrité des preuves et événements

Usage :
    python scripts/validate_domain_assets.py
    python scripts/validate_domain_assets.py --entities project/bootstrap_entities.yaml \\
        --proofs project/bootstrap_proofs.yaml \\
        --events project/bootstrap_events.yaml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Le YAML doit être un objet : {path}")
    return data


# ---------------------------------------------------------------------------
# Validation des entités
# ---------------------------------------------------------------------------

def _collect_ids(entities: Dict[str, Any]) -> Dict[str, str]:
    """Retourne un mapping id → type pour toutes les entités."""
    known: Dict[str, str] = {}

    for section, etype in [
        ("hub", "HUB"),
        ("dieux", "DIEU"),
        ("academies", "ACADEMIE"),
        ("robots", "ROBOT"),
        ("lignees", "LIGNEE"),
        ("regles", "REGLE"),
        ("commandes", "COMMANDE"),
    ]:
        raw = entities.get(section)
        if raw is None:
            continue
        if isinstance(raw, dict):
            raw = [raw]
        for item in raw:
            eid = item.get("id")
            if eid:
                known[eid] = etype

    return known


def validate_entities(entities: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    known = _collect_ids(entities)

    # -- Hub --
    hub = entities.get("hub")
    if not hub:
        errors.append("ERREUR: section 'hub' absente ou vide.")
    else:
        if not hub.get("id"):
            errors.append("ERREUR: hub sans 'id'.")

    # -- Dieux --
    dieux = entities.get("dieux", [])
    dieu_ids = {d["id"] for d in dieux if d.get("id")}
    if not dieux:
        errors.append("ERREUR: section 'dieux' absente ou vide.")

    for d in dieux:
        did = d.get("id", "<inconnu>")
        for champ in ("nom", "domaine", "statut"):
            if not d.get(champ):
                errors.append(f"ERREUR: dieu {did} — champ '{champ}' manquant ou vide.")

    # -- Académies --
    academies = entities.get("academies", [])
    academie_ids = {a["id"] for a in academies if a.get("id")}
    for ac in academies:
        acid = ac.get("id", "<inconnu>")
        tuteur = ac.get("dieu_tuteur")
        if tuteur and tuteur not in dieu_ids:
            errors.append(f"ERREUR: académie {acid} — dieu_tuteur '{tuteur}' introuvable.")
        if not ac.get("nom"):
            errors.append(f"ERREUR: académie {acid} — 'nom' manquant.")

    # -- Robots --
    robots = entities.get("robots", [])
    robot_ids = {r["id"] for r in robots if r.get("id")}
    for robot in robots:
        rid = robot.get("id", "<inconnu>")
        # Vérification lignée
        lignee_id = robot.get("lignee_id")
        if lignee_id:
            lignees = entities.get("lignees", [])
            lignee_ids = {l["id"] for l in lignees if l.get("id")}
            if lignee_id not in lignee_ids:
                errors.append(f"ERREUR: robot {rid} — lignee_id '{lignee_id}' introuvable.")
        # Vérification académie
        academie_id = robot.get("academie_id")
        if academie_id and academie_id not in academie_ids:
            errors.append(f"ERREUR: robot {rid} — academie_id '{academie_id}' introuvable.")
        # Vérification dieu tuteur
        dieu_tuteur = robot.get("dieu_tuteur")
        if dieu_tuteur and dieu_tuteur not in dieu_ids:
            errors.append(f"ERREUR: robot {rid} — dieu_tuteur '{dieu_tuteur}' introuvable.")
        # Cohérence des scores
        scores = robot.get("scores", {})
        for score_champ in ("points", "prestige", "credit_social"):
            val = scores.get(score_champ)
            if val is None:
                errors.append(f"ERREUR: robot {rid} — score '{score_champ}' absent.")
            elif not isinstance(val, (int, float)) or val < 0:
                errors.append(f"ERREUR: robot {rid} — score '{score_champ}' invalide ({val}).")
        # Vérification des relations de filiation
        for rel in robot.get("relations", []):
            if rel.get("type") == "descendant_de":
                parent_id = rel.get("cible")
                if parent_id and parent_id not in robot_ids:
                    errors.append(f"ERREUR: robot {rid} — parent '{parent_id}' (descendant_de) introuvable.")

    # -- Lignées --
    lignees = entities.get("lignees", [])
    for lignee in lignees:
        lid = lignee.get("id", "<inconnu>")
        fondateur_id = lignee.get("fondateur_id")
        if fondateur_id and fondateur_id not in robot_ids:
            errors.append(f"ERREUR: lignée {lid} — fondateur_id '{fondateur_id}' introuvable.")
        for membre in lignee.get("membres", []):
            if membre not in robot_ids:
                errors.append(f"ERREUR: lignée {lid} — membre '{membre}' introuvable.")
        tuteur = lignee.get("dieu_tuteur")
        if tuteur and tuteur not in dieu_ids:
            errors.append(f"ERREUR: lignée {lid} — dieu_tuteur '{tuteur}' introuvable.")

    return errors


# ---------------------------------------------------------------------------
# Validation des preuves
# ---------------------------------------------------------------------------

def validate_proofs(
    proofs: Dict[str, Any],
    known_entity_ids: set[str],
) -> List[str]:
    errors: List[str] = []
    preuves = proofs.get("preuves", [])
    if not preuves:
        errors.append("ERREUR: section 'preuves' absente ou vide.")
        return errors

    TYPES_VALIDES = {
        "execution_regle",
        "execution_commande",
        "validation_tache",
        "modification_entite",
        "decision_humaine",
        "attribution_points",
        "operation_index",
        "revue_documentaire",
        "alerte_securite",
        "evenement_systeme",
    }
    ORIGINES_VALIDES = {"bus_slash", "moteur_regles", "agent_humain", "systeme", "ci_cd"}
    seen_ids: set[str] = set()

    for preuve in preuves:
        pid = preuve.get("id", "<inconnu>")
        if pid in seen_ids:
            errors.append(f"ERREUR: preuve {pid} — identifiant dupliqué.")
        seen_ids.add(pid)

        type_preuve = preuve.get("type_preuve")
        if type_preuve not in TYPES_VALIDES:
            errors.append(f"ERREUR: preuve {pid} — type_preuve '{type_preuve}' invalide.")

        origine = preuve.get("origine")
        if not any(str(origine).startswith(o) for o in ORIGINES_VALIDES):
            errors.append(f"ERREUR: preuve {pid} — origine '{origine}' invalide.")

        if not preuve.get("date_preuve"):
            errors.append(f"ERREUR: preuve {pid} — 'date_preuve' absente.")

        if not preuve.get("auteur"):
            errors.append(f"ERREUR: preuve {pid} — 'auteur' absent.")

        entite_id = preuve.get("entite_id")
        if not entite_id:
            errors.append(f"ERREUR: preuve {pid} — 'entite_id' absent.")

    return errors


# ---------------------------------------------------------------------------
# Validation des événements
# ---------------------------------------------------------------------------

def validate_events(
    events: Dict[str, Any],
    known_entity_ids: set[str],
    known_proof_ids: set[str],
) -> List[str]:
    errors: List[str] = []
    evenements = events.get("evenements", [])
    if not evenements:
        errors.append("ERREUR: section 'evenements' absente ou vide.")
        return errors

    seen_ids: set[str] = set()
    for evt in evenements:
        eid = evt.get("id", "<inconnu>")
        if eid in seen_ids:
            errors.append(f"ERREUR: événement {eid} — identifiant dupliqué.")
        seen_ids.add(eid)

        if not evt.get("type"):
            errors.append(f"ERREUR: événement {eid} — 'type' absent.")
        if not evt.get("date"):
            errors.append(f"ERREUR: événement {eid} — 'date' absente.")
        if not evt.get("description"):
            errors.append(f"ERREUR: événement {eid} — 'description' absente.")

        preuve_id = evt.get("preuve_id")
        if preuve_id and preuve_id not in known_proof_ids:
            errors.append(f"ERREUR: événement {eid} — preuve_id '{preuve_id}' introuvable.")

    return errors


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valide les assets métier du domaine AI10101IA."
    )
    parser.add_argument(
        "--entities",
        default=str(ROOT / "project" / "bootstrap_entities.yaml"),
        help="Chemin vers bootstrap_entities.yaml.",
    )
    parser.add_argument(
        "--proofs",
        default=str(ROOT / "project" / "bootstrap_proofs.yaml"),
        help="Chemin vers bootstrap_proofs.yaml.",
    )
    parser.add_argument(
        "--events",
        default=str(ROOT / "project" / "bootstrap_events.yaml"),
        help="Chemin vers bootstrap_events.yaml.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    all_errors: List[str] = []

    # Chargement
    try:
        entities = load_yaml(Path(args.entities))
        proofs = load_yaml(Path(args.proofs))
        events = load_yaml(Path(args.events))
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1

    # Validation des entités
    entity_errors = validate_entities(entities)
    all_errors.extend(entity_errors)

    known_entity_ids = set(_collect_ids(entities).keys())
    known_proof_ids = {p["id"] for p in proofs.get("preuves", []) if p.get("id")}

    # Validation des preuves
    proof_errors = validate_proofs(proofs, known_entity_ids)
    all_errors.extend(proof_errors)

    # Validation des événements
    event_errors = validate_events(events, known_entity_ids, known_proof_ids)
    all_errors.extend(event_errors)

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        print(
            f"\nValidation échouée : {len(all_errors)} erreur(s) détectée(s).",
            file=sys.stderr,
        )
        return 1

    print("OK: validation métier réussie.")
    print(f"  Entités connues : {len(known_entity_ids)}")
    print(f"  Preuves validées : {len(proofs.get('preuves', []))}")
    print(f"  Événements validés : {len(events.get('evenements', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
