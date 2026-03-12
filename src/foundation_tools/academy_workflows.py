"""
academy_workflows.py — Workflows d'académie AI10101IA (T0027).

Gère les parcours d'entraînement, d'examen, de classement,
de promotion et de sanction dans les académies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Types et constantes
# ---------------------------------------------------------------------------

NIVEAUX_VALIDES = {1, 2, 3}
STATUTS_ROBOT_VALIDES = {"actif", "en_formation", "en_retraite", "archive", "inactif"}


# ---------------------------------------------------------------------------
# Résultat générique
# ---------------------------------------------------------------------------

@dataclass
class WorkflowResult:
    succes: bool
    operation: str
    entite_id: str
    details: Dict[str, Any] = field(default_factory=dict)
    erreurs: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.succes and not self.erreurs


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------

def inscrire_robot(
    robot: Dict[str, Any],
    academie: Dict[str, Any],
) -> WorkflowResult:
    """
    Inscrit un robot dans une académie.

    Vérifie la capacité de l'académie, le statut du robot et
    qu'il n'est pas déjà inscrit ailleurs.
    """
    robot_id = robot.get("id", "<inconnu>")
    academie_id = academie.get("id", "<inconnu>")
    erreurs: List[str] = []

    if robot.get("statut") not in ("actif", "en_formation"):
        erreurs.append(f"Robot {robot_id} : statut '{robot.get('statut')}' incompatible avec une inscription.")

    if robot.get("academie_id") and robot["academie_id"] != academie_id:
        erreurs.append(
            f"Robot {robot_id} : déjà inscrit à l'académie '{robot['academie_id']}'. "
            f"Désinscription requise avant toute nouvelle inscription."
        )

    membres_actuels = academie.get("membres_actuels", [])
    capacite_max = academie.get("capacite_max", 0)
    if len(membres_actuels) >= capacite_max:
        erreurs.append(
            f"Académie {academie_id} : capacité maximale atteinte ({capacite_max} robots)."
        )

    if erreurs:
        return WorkflowResult(succes=False, operation="inscription", entite_id=robot_id, erreurs=erreurs)

    robot["academie_id"] = academie_id
    robot["statut"] = "en_formation"
    if "membres_actuels" not in academie:
        academie["membres_actuels"] = []
    if robot_id not in academie["membres_actuels"]:
        academie["membres_actuels"].append(robot_id)

    return WorkflowResult(
        succes=True,
        operation="inscription",
        entite_id=robot_id,
        details={"academie_id": academie_id},
    )


# ---------------------------------------------------------------------------
# Passage d'examen
# ---------------------------------------------------------------------------

def passer_examen(
    robot: Dict[str, Any],
    niveau: int,
    score_examen: float,
    seuil_reussite: float = 0.6,
) -> WorkflowResult:
    """
    Valide le passage d'un examen de niveau pour un robot.

    Args:
        robot: Entité robot.
        niveau: Niveau de l'examen (1, 2 ou 3).
        score_examen: Score obtenu (entre 0.0 et 1.0).
        seuil_reussite: Seuil minimal de réussite (défaut 0.60).

    Returns:
        WorkflowResult avec le résultat de l'examen.
    """
    robot_id = robot.get("id", "<inconnu>")
    erreurs: List[str] = []

    if niveau not in NIVEAUX_VALIDES:
        erreurs.append(f"Niveau d'examen invalide : {niveau}. Valeurs attendues : {sorted(NIVEAUX_VALIDES)}.")

    if not (0.0 <= score_examen <= 1.0):
        erreurs.append(f"Score d'examen invalide : {score_examen} (doit être entre 0.0 et 1.0).")

    if robot.get("statut") != "en_formation":
        erreurs.append(f"Robot {robot_id} : le statut doit être 'en_formation' pour passer un examen.")

    niveau_actuel = robot.get("niveau_maitrise", 0)
    if niveau != niveau_actuel + 1:
        erreurs.append(
            f"Robot {robot_id} : tentative d'examen de niveau {niveau} "
            f"mais le niveau courant est {niveau_actuel}. Progression séquentielle requise."
        )

    if erreurs:
        return WorkflowResult(succes=False, operation="examen", entite_id=robot_id, erreurs=erreurs)

    reussi = score_examen >= seuil_reussite

    return WorkflowResult(
        succes=reussi,
        operation="examen",
        entite_id=robot_id,
        details={
            "niveau": niveau,
            "score": score_examen,
            "seuil": seuil_reussite,
            "reussi": reussi,
        },
        erreurs=[] if reussi else [f"Score insuffisant ({score_examen:.0%} < {seuil_reussite:.0%})."],
    )


# ---------------------------------------------------------------------------
# Promotion
# ---------------------------------------------------------------------------

def promouvoir_robot(
    robot: Dict[str, Any],
    nouveau_niveau: int,
) -> WorkflowResult:
    """
    Promeut un robot au niveau de maîtrise suivant.

    Requiert que le robot ait réussi l'examen du niveau précédent.
    """
    robot_id = robot.get("id", "<inconnu>")
    erreurs: List[str] = []

    if nouveau_niveau not in NIVEAUX_VALIDES:
        erreurs.append(f"Niveau de promotion invalide : {nouveau_niveau}.")

    niveau_actuel = robot.get("niveau_maitrise", 0)
    if nouveau_niveau != niveau_actuel + 1:
        erreurs.append(
            f"Robot {robot_id} : promotion au niveau {nouveau_niveau} impossible "
            f"(niveau courant : {niveau_actuel}). Progression séquentielle requise."
        )

    if erreurs:
        return WorkflowResult(succes=False, operation="promotion", entite_id=robot_id, erreurs=erreurs)

    robot["niveau_maitrise"] = nouveau_niveau

    if nouveau_niveau == max(NIVEAUX_VALIDES):
        robot["statut"] = "actif"

    return WorkflowResult(
        succes=True,
        operation="promotion",
        entite_id=robot_id,
        details={"ancien_niveau": niveau_actuel, "nouveau_niveau": nouveau_niveau},
    )


# ---------------------------------------------------------------------------
# Sanction et expulsion
# ---------------------------------------------------------------------------

def sanctionner_robot(
    robot: Dict[str, Any],
    academie: Optional[Dict[str, Any]],
    motif: str,
    expulser: bool = False,
) -> WorkflowResult:
    """
    Applique une sanction académique à un robot.

    Si expulser=True, le robot est retiré de l'académie et perd
    les points de son niveau courant.
    """
    robot_id = robot.get("id", "<inconnu>")
    erreurs: List[str] = []

    if not motif:
        erreurs.append("Le motif de sanction ne peut pas être vide.")

    if erreurs:
        return WorkflowResult(succes=False, operation="sanction", entite_id=robot_id, erreurs=erreurs)

    details: Dict[str, Any] = {"motif": motif, "expulsion": expulser}

    if expulser and academie is not None:
        academie_id = academie.get("id", "<inconnu>")
        membres = academie.get("membres_actuels", [])
        if robot_id in membres:
            membres.remove(robot_id)
        robot["academie_id"] = None
        robot["statut"] = "actif"
        robot["niveau_maitrise"] = max(0, robot.get("niveau_maitrise", 1) - 1)
        details["academie_id"] = academie_id
        details["niveau_apres_expulsion"] = robot["niveau_maitrise"]

    return WorkflowResult(succes=True, operation="sanction", entite_id=robot_id, details=details)


# ---------------------------------------------------------------------------
# Classement
# ---------------------------------------------------------------------------

def classer_robots(
    robots: List[Dict[str, Any]],
    academie_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Classe les robots par score (prestige desc, puis points desc).

    Args:
        robots: Liste d'entités robot.
        academie_id: Si fourni, filtre les robots inscrits à cette académie.

    Returns:
        Liste triée de dicts avec rang, robot_id, prestige, points.
    """
    if academie_id is not None:
        robots = [r for r in robots if r.get("academie_id") == academie_id]

    def sort_key(r: Dict[str, Any]) -> tuple:
        scores = r.get("scores", {})
        return (-(scores.get("prestige", 0)), -(scores.get("points", 0)))

    tries = sorted(robots, key=sort_key)

    classement = []
    for rang, robot in enumerate(tries, start=1):
        scores = robot.get("scores", {})
        classement.append({
            "rang": rang,
            "robot_id": robot.get("id"),
            "prestige": scores.get("prestige", 0),
            "points": scores.get("points", 0),
            "credit_social": scores.get("credit_social", 0),
        })

    return classement
