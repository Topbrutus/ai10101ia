"""
score_points.py — Calculateur de points AI10101IA (T0024).

Calcule et trace les points attribués aux entités et aux actions
selon des règles versionnées.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Barèmes versionnés
# ---------------------------------------------------------------------------

BAREME_V1: Dict[str, int] = {
    "action_validee": 10,
    "regle_respectee": 5,
    "commande_executee": 8,
    "niveau_academique_atteint": 50,
    "preuve_produite": 3,
    "contribution_majeure": 100,
    "erreur_mineure": -5,
    "erreur_majeure": -20,
    "violation_quota": -30,
    "faille_securite": -50,
}


def get_bareme(version: int = 1) -> Dict[str, int]:
    """Retourne le barème de points pour une version donnée."""
    baremes = {1: BAREME_V1}
    if version not in baremes:
        raise ValueError(f"Version de barème inconnue : {version}")
    return baremes[version]


# ---------------------------------------------------------------------------
# Résultat de calcul
# ---------------------------------------------------------------------------

@dataclass
class PointsResult:
    entite_id: str
    action: str
    delta: int
    ancien_total: int
    nouveau_total: int
    version_bareme: int
    motif: str = ""
    erreurs: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.erreurs


# ---------------------------------------------------------------------------
# Calculateur
# ---------------------------------------------------------------------------

def calculer_points(
    entite_id: str,
    action: str,
    points_courants: int,
    version_bareme: int = 1,
    motif: str = "",
) -> PointsResult:
    """
    Calcule les nouveaux points après une action.

    Args:
        entite_id: Identifiant de l'entité.
        action: Clé de l'action dans le barème.
        points_courants: Score de points actuel de l'entité.
        version_bareme: Version du barème à utiliser.
        motif: Motif libre de l'opération.

    Returns:
        PointsResult avec le delta et le nouveau total.
    """
    erreurs: List[str] = []

    if not entite_id:
        erreurs.append("entite_id ne peut pas être vide.")
    if points_courants < 0:
        erreurs.append(f"points_courants invalide : {points_courants} (doit être >= 0).")

    try:
        bareme = get_bareme(version_bareme)
    except ValueError as exc:
        erreurs.append(str(exc))
        return PointsResult(
            entite_id=entite_id,
            action=action,
            delta=0,
            ancien_total=points_courants,
            nouveau_total=points_courants,
            version_bareme=version_bareme,
            motif=motif,
            erreurs=erreurs,
        )

    if action not in bareme:
        erreurs.append(f"Action inconnue dans le barème v{version_bareme} : '{action}'.")
        return PointsResult(
            entite_id=entite_id,
            action=action,
            delta=0,
            ancien_total=points_courants,
            nouveau_total=points_courants,
            version_bareme=version_bareme,
            motif=motif,
            erreurs=erreurs,
        )

    delta = bareme[action]
    nouveau_total = max(0, points_courants + delta)

    return PointsResult(
        entite_id=entite_id,
        action=action,
        delta=delta,
        ancien_total=points_courants,
        nouveau_total=nouveau_total,
        version_bareme=version_bareme,
        motif=motif,
        erreurs=erreurs,
    )


def appliquer_points(
    entite: Dict[str, Any],
    action: str,
    version_bareme: int = 1,
    motif: str = "",
) -> PointsResult:
    """
    Applique le calcul de points à une entité dict et met à jour son score.

    L'entité doit avoir une clé 'scores' avec une clé 'points'.
    L'entité est modifiée en place.
    """
    entite_id = entite.get("id", "<inconnu>")
    scores = entite.get("scores", {})
    points_courants = scores.get("points", 0)

    result = calculer_points(
        entite_id=entite_id,
        action=action,
        points_courants=points_courants,
        version_bareme=version_bareme,
        motif=motif,
    )

    if result.ok:
        if "scores" not in entite:
            entite["scores"] = {}
        entite["scores"]["points"] = result.nouveau_total

    return result
