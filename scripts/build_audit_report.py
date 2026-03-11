#!/usr/bin/env python3
"""
build_audit_report.py — Générateur de vues d'audit lisibles AI10101IA (T0032).

Génère un rapport d'audit structuré à partir du registre bootstrap :
- synthèse du registre
- relations de filiation
- preuves par entité
- incohérences détectées
- synthèse exportable

Usage :
    python scripts/build_audit_report.py
    python scripts/build_audit_report.py --format markdown --output /tmp/audit_report.md
    python scripts/build_audit_report.py --format json --output /tmp/audit_report.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
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


def collect_entities(entities: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
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
# Construction du rapport
# ---------------------------------------------------------------------------

def build_report(
    entities: Dict[str, Any],
    proofs: Dict[str, Any],
    events: Dict[str, Any],
) -> Dict[str, Any]:
    all_entities = collect_entities(entities)
    preuves = proofs.get("preuves", [])
    evenements = events.get("evenements", [])

    # 1. Synthèse du registre
    synthese: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hub": entities.get("hub", {}).get("id", "absent"),
        "entites_par_type": {},
        "total_entites": len(all_entities),
        "total_preuves": len(preuves),
        "total_evenements": len(evenements),
    }
    for section in ENTITY_SECTIONS[1:]:
        items = entities.get(section, [])
        if isinstance(items, dict):
            items = [items]
        synthese["entites_par_type"][section] = len(items)

    # 2. Relations de filiation
    filiation: List[Dict[str, str]] = []
    for eid, entity in all_entities.items():
        for rel in entity.get("relations", []):
            if rel.get("type") == "descendant_de":
                filiation.append({"enfant": eid, "parent": rel.get("cible", "")})

    # 3. Preuves par entité
    preuves_par_entite: Dict[str, List[str]] = {}
    for preuve in preuves:
        entite_id = preuve.get("entite_id", "")
        if entite_id:
            preuves_par_entite.setdefault(entite_id, []).append(preuve.get("id", ""))

    # 4. Détection des incohérences
    incoherences: List[str] = []
    robot_ids = {r["id"] for r in entities.get("robots", []) if r.get("id")}
    dieu_ids = {d["id"] for d in entities.get("dieux", []) if d.get("id")}
    academie_ids = {a["id"] for a in entities.get("academies", []) if a.get("id")}
    lignee_ids = {l["id"] for l in entities.get("lignees", []) if l.get("id")}
    preuve_ids = {p["id"] for p in preuves if p.get("id")}

    for robot in entities.get("robots", []):
        rid = robot.get("id", "<inconnu>")
        scores = robot.get("scores", {})
        for champ in ("points", "prestige", "credit_social"):
            val = scores.get(champ)
            if val is None or (isinstance(val, (int, float)) and val < 0):
                incoherences.append(f"Robot {rid}: score '{champ}' invalide ({val}).")
        if robot.get("lignee_id") and robot["lignee_id"] not in lignee_ids:
            incoherences.append(f"Robot {rid}: lignee_id '{robot['lignee_id']}' introuvable.")
        if robot.get("academie_id") and robot["academie_id"] not in academie_ids:
            incoherences.append(f"Robot {rid}: academie_id '{robot['academie_id']}' introuvable.")
        if robot.get("dieu_tuteur") and robot["dieu_tuteur"] not in dieu_ids:
            incoherences.append(f"Robot {rid}: dieu_tuteur '{robot['dieu_tuteur']}' introuvable.")

    for lignee in entities.get("lignees", []):
        lid = lignee.get("id", "<inconnu>")
        fondateur = lignee.get("fondateur_id")
        if fondateur and fondateur not in robot_ids:
            incoherences.append(f"Lignée {lid}: fondateur '{fondateur}' introuvable.")
        for m in lignee.get("membres", []):
            if m not in robot_ids:
                incoherences.append(f"Lignée {lid}: membre '{m}' introuvable.")

    for preuve in preuves:
        pid = preuve.get("id", "<inconnu>")
        entite_id = preuve.get("entite_id", "")
        if entite_id and not entite_id.startswith("TACHE-") and entite_id not in all_entities:
            incoherences.append(f"Preuve {pid}: entite_id '{entite_id}' introuvable.")

    for evt in evenements:
        eid_evt = evt.get("id", "<inconnu>")
        preuve_id = evt.get("preuve_id")
        if preuve_id and preuve_id not in preuve_ids:
            incoherences.append(f"Événement {eid_evt}: preuve_id '{preuve_id}' introuvable.")

    return {
        "synthese": synthese,
        "filiation": filiation,
        "preuves_par_entite": preuves_par_entite,
        "incoherences": incoherences,
        "statut": "OK" if not incoherences else "ATTENTION",
    }


# ---------------------------------------------------------------------------
# Rendu Markdown
# ---------------------------------------------------------------------------

def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    s = report["synthese"]
    lines.append("# Rapport d'audit AI10101IA")
    lines.append("")
    lines.append(f"> Généré le : {s['generated_at']}")
    lines.append(f"> Statut global : **{report['statut']}**")
    lines.append("")

    lines.append("## 1. Synthèse du registre bootstrap")
    lines.append("")
    lines.append(f"- **Hub** : {s['hub']}")
    lines.append(f"- **Total entités** : {s['total_entites']}")
    lines.append(f"- **Total preuves** : {s['total_preuves']}")
    lines.append(f"- **Total événements** : {s['total_evenements']}")
    lines.append("")
    lines.append("| Type | Nombre |")
    lines.append("|---|---|")
    for section, count in s.get("entites_par_type", {}).items():
        lines.append(f"| {section.capitalize()} | {count} |")
    lines.append("")

    lines.append("## 2. Relations de filiation")
    lines.append("")
    filiation = report["filiation"]
    if filiation:
        lines.append("| Enfant | Parent |")
        lines.append("|---|---|")
        for rel in filiation:
            lines.append(f"| `{rel['enfant']}` | `{rel['parent']}` |")
    else:
        lines.append("_Aucune relation de filiation détectée._")
    lines.append("")

    lines.append("## 3. Preuves par entité")
    lines.append("")
    pbe = report["preuves_par_entite"]
    if pbe:
        lines.append("| Entité | Preuves |")
        lines.append("|---|---|")
        for entite_id, pids in sorted(pbe.items()):
            lines.append(f"| `{entite_id}` | {', '.join(f'`{p}`' for p in pids)} |")
    else:
        lines.append("_Aucune preuve rattachée._")
    lines.append("")

    lines.append("## 4. Incohérences détectées")
    lines.append("")
    incoherences = report["incoherences"]
    if incoherences:
        for inc in incoherences:
            lines.append(f"- ⚠️  {inc}")
    else:
        lines.append("_Aucune incohérence détectée._")
    lines.append("")

    lines.append("## 5. Bilan")
    lines.append("")
    if not incoherences:
        lines.append("✅ Le registre bootstrap est cohérent. Aucune incohérence détectée.")
    else:
        lines.append(f"⚠️  {len(incoherences)} incohérence(s) détectée(s). Voir section 4.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Génère un rapport d'audit lisible pour AI10101IA."
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
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Format de sortie du rapport (défaut : markdown).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Fichier de sortie. Si absent, affichage sur stdout.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        entities = _load_yaml(Path(args.entities))
        proofs = _load_yaml(Path(args.proofs))
        events = _load_yaml(Path(args.events))
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1

    report = build_report(entities, proofs, events)

    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = render_markdown(report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"OK: rapport d'audit écrit dans {args.output}")
    else:
        print(output)

    if report["statut"] != "OK":
        print(
            f"\nATTENTION: {len(report['incoherences'])} incohérence(s) détectée(s).",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
