"""
score_prestige.py — Calculateur de prestige AI10101IA (T0025).

Calcule le prestige des entités et ses motifs d'attribution audités.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Barèmes de prestige versionnés
# ---------------------------------------------------------------------------

BAREME_PRESTIGE_V1: Dict[str, int] = {
    "niveau_1_academique": 5,
    "niveau_2_academique": 15,
    "niveau_3_academique": 40,
    "contribution_majeure": 20,
    "distinction_hub": 30,
    "election_remportee": 50,
    "violation_de_quota": -10,
    "faille_securite": -25,
    "sanction_formelle": -15,
    "inactivite_prolongee": -5,
}


def get_bareme_prestige(version: int = 1) -> Dict[str, int]:
    """Retourne le barème de prestige pour une version donnée."""
    baremes = {1: BAREME_PRESTIGE_V1}
    if version not in baremes:
        raise ValueError(f"Version de barème de prestige inconnue : {version}")
    return baremes[version]


# ---------------------------------------------------------------------------
# Résultat
# ---------------------------------------------------------------------------

@dataclass
class PrestigeResult:
    entite_id: str
    motif: str
    delta: int
    ancien_prestige: int
    nouveau_prestige: int
    version_bareme: int
    description: str = ""
    erreurs: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.erreurs


# ---------------------------------------------------------------------------
# Calculateur
# ---------------------------------------------------------------------------

def calculer_prestige(
    entite_id: str,
    motif: str,
    prestige_courant: int,
    version_bareme: int = 1,
    description: str = "",
) -> PrestigeResult:
    """
    Calcule le nouveau prestige d'une entité après un motif d'attribution.

    Args:
        entite_id: Identifiant de l'entité.
        motif: Clé du motif dans le barème.
        prestige_courant: Prestige actuel de l'entité.
        version_bareme: Version du barème à utiliser.
        description: Description libre de l'événement.

    Returns:
        PrestigeResult avec le delta et le nouveau prestige.
    """
    erreurs: List[str] = []

    if not entite_id:
        erreurs.append("entite_id ne peut pas être vide.")
    if prestige_courant < 0:
        erreurs.append(f"prestige_courant invalide : {prestige_courant} (doit être >= 0).")

    try:
        bareme = get_bareme_prestige(version_bareme)
    except ValueError as exc:
        erreurs.append(str(exc))
        return PrestigeResult(
            entite_id=entite_id,
            motif=motif,
            delta=0,
            ancien_prestige=prestige_courant,
            nouveau_prestige=prestige_courant,
            version_bareme=version_bareme,
            description=description,
            erreurs=erreurs,
        )

    if motif not in bareme:
        erreurs.append(f"Motif de prestige inconnu dans le barème v{version_bareme} : '{motif}'.")
        return PrestigeResult(
            entite_id=entite_id,
            motif=motif,
            delta=0,
            ancien_prestige=prestige_courant,
            nouveau_prestige=prestige_courant,
            version_bareme=version_bareme,
            description=description,
            erreurs=erreurs,
        )

    delta = bareme[motif]
    nouveau_prestige = max(0, prestige_courant + delta)

    return PrestigeResult(
        entite_id=entite_id,
        motif=motif,
        delta=delta,
        ancien_prestige=prestige_courant,
        nouveau_prestige=nouveau_prestige,
        version_bareme=version_bareme,
        description=description,
        erreurs=erreurs,
    )


def appliquer_prestige(
    entite: Dict[str, Any],
    motif: str,
    version_bareme: int = 1,
    description: str = "",
) -> PrestigeResult:
    """
    Applique le calcul de prestige à une entité dict et met à jour son score.

    L'entité doit avoir une clé 'scores' avec une clé 'prestige'.
    L'entité est modifiée en place.
    """
    entite_id = entite.get("id", "<inconnu>")
    scores = entite.get("scores", {})
    prestige_courant = scores.get("prestige", 0)

    result = calculer_prestige(
        entite_id=entite_id,
        motif=motif,
        prestige_courant=prestige_courant,
        version_bareme=version_bareme,
        description=description,
    )

    if result.ok:
        if "scores" not in entite:
            entite["scores"] = {}
        entite["scores"]["prestige"] = result.nouveau_prestige

    return result
