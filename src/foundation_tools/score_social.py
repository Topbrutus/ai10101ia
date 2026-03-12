"""
score_social.py — Calculateur de crédit social AI10101IA (T0026).

Calcule le crédit social des entités, ses causes, ses effets et les recours.
Le crédit social est compris entre 0 et 100.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Seuils et barèmes
# ---------------------------------------------------------------------------

CREDIT_SOCIAL_MIN = 0
CREDIT_SOCIAL_MAX = 100

SEUILS_CREDIT_SOCIAL = {
    "critique": 30,
    "avertissement": 50,
    "standard": 70,
    "excellent": 90,
}

BAREME_CREDIT_SOCIAL_V1: Dict[str, int] = {
    "conformite_regles": 5,
    "participation_scrutin": 3,
    "acte_civique": 8,
    "formation_completee": 10,
    "rapport_audit_produit": 4,
    "violation_mineure": -5,
    "violation_majeure": -15,
    "sanction_formelle": -20,
    "inactivite_longue": -8,
    "faille_securite": -30,
    "depassement_quota": -10,
}


def get_bareme_credit_social(version: int = 1) -> Dict[str, int]:
    """Retourne le barème de crédit social pour une version donnée."""
    baremes = {1: BAREME_CREDIT_SOCIAL_V1}
    if version not in baremes:
        raise ValueError(f"Version de barème de crédit social inconnue : {version}")
    return baremes[version]


def get_niveau_credit_social(credit_social: int) -> str:
    """Retourne le niveau qualitatif du crédit social."""
    if credit_social >= SEUILS_CREDIT_SOCIAL["excellent"]:
        return "excellent"
    if credit_social >= SEUILS_CREDIT_SOCIAL["standard"]:
        return "standard"
    if credit_social >= SEUILS_CREDIT_SOCIAL["avertissement"]:
        return "avertissement"
    if credit_social >= SEUILS_CREDIT_SOCIAL["critique"]:
        return "critique"
    return "bloque"


# ---------------------------------------------------------------------------
# Résultat
# ---------------------------------------------------------------------------

@dataclass
class CreditSocialResult:
    entite_id: str
    cause: str
    delta: int
    ancien_credit: int
    nouveau_credit: int
    ancien_niveau: str
    nouveau_niveau: str
    version_bareme: int
    description: str = ""
    effets: List[str] = field(default_factory=list)
    recours_disponibles: List[str] = field(default_factory=list)
    erreurs: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.erreurs

    @property
    def niveau_degrade(self) -> bool:
        niveaux = ["bloque", "critique", "avertissement", "standard", "excellent"]
        return niveaux.index(self.nouveau_niveau) < niveaux.index(self.ancien_niveau)


def _determiner_effets(nouveau_niveau: str) -> List[str]:
    """Détermine les effets systémiques selon le niveau de crédit social."""
    effets_par_niveau = {
        "bloque": [
            "Toutes les actions nécessitant un crédit social > 0 sont bloquées",
            "Inspection systématique déclenchée",
            "Transmission au dieu tuteur pour arbitrage",
        ],
        "critique": [
            "Accès aux commandes avancées suspendu",
            "Supervision renforcée activée",
            "Alerte au dieu tuteur",
        ],
        "avertissement": [
            "Avertissement formel enregistré",
            "Surveillance accrue pendant 10 cycles",
        ],
        "standard": [],
        "excellent": [
            "Éligibilité aux distinctions de hub",
            "Accès aux commandes de rang supérieur",
        ],
    }
    return effets_par_niveau.get(nouveau_niveau, [])


def _determiner_recours(nouveau_niveau: str) -> List[str]:
    """Détermine les recours disponibles selon le niveau de crédit social."""
    recours_par_niveau = {
        "bloque": [
            "Appel formel auprès du dieu tuteur",
            "Demande de révision par un Gardien de niveau 3",
        ],
        "critique": [
            "Accomplir 3 actes civiques pour recouvrer le niveau avertissement",
            "Appel auprès du dieu tuteur",
        ],
        "avertissement": [
            "Accomplir 2 actes civiques pour recouvrer le niveau standard",
        ],
        "standard": [],
        "excellent": [],
    }
    return recours_par_niveau.get(nouveau_niveau, [])


# ---------------------------------------------------------------------------
# Calculateur
# ---------------------------------------------------------------------------

def calculer_credit_social(
    entite_id: str,
    cause: str,
    credit_courant: int,
    version_bareme: int = 1,
    description: str = "",
) -> CreditSocialResult:
    """
    Calcule le nouveau crédit social d'une entité après une cause.

    Args:
        entite_id: Identifiant de l'entité.
        cause: Clé de la cause dans le barème.
        credit_courant: Crédit social actuel (0–100).
        version_bareme: Version du barème à utiliser.
        description: Description libre de l'événement.

    Returns:
        CreditSocialResult avec le delta, le nouveau crédit et les effets.
    """
    erreurs: List[str] = []

    if not entite_id:
        erreurs.append("entite_id ne peut pas être vide.")
    if not (CREDIT_SOCIAL_MIN <= credit_courant <= CREDIT_SOCIAL_MAX):
        erreurs.append(
            f"credit_courant invalide : {credit_courant} "
            f"(doit être entre {CREDIT_SOCIAL_MIN} et {CREDIT_SOCIAL_MAX})."
        )

    ancien_niveau = get_niveau_credit_social(credit_courant)

    try:
        bareme = get_bareme_credit_social(version_bareme)
    except ValueError as exc:
        erreurs.append(str(exc))
        return CreditSocialResult(
            entite_id=entite_id,
            cause=cause,
            delta=0,
            ancien_credit=credit_courant,
            nouveau_credit=credit_courant,
            ancien_niveau=ancien_niveau,
            nouveau_niveau=ancien_niveau,
            version_bareme=version_bareme,
            description=description,
            erreurs=erreurs,
        )

    if cause not in bareme:
        erreurs.append(f"Cause de crédit social inconnue dans le barème v{version_bareme} : '{cause}'.")
        return CreditSocialResult(
            entite_id=entite_id,
            cause=cause,
            delta=0,
            ancien_credit=credit_courant,
            nouveau_credit=credit_courant,
            ancien_niveau=ancien_niveau,
            nouveau_niveau=ancien_niveau,
            version_bareme=version_bareme,
            description=description,
            erreurs=erreurs,
        )

    delta = bareme[cause]
    nouveau_credit = max(CREDIT_SOCIAL_MIN, min(CREDIT_SOCIAL_MAX, credit_courant + delta))
    nouveau_niveau = get_niveau_credit_social(nouveau_credit)

    return CreditSocialResult(
        entite_id=entite_id,
        cause=cause,
        delta=delta,
        ancien_credit=credit_courant,
        nouveau_credit=nouveau_credit,
        ancien_niveau=ancien_niveau,
        nouveau_niveau=nouveau_niveau,
        version_bareme=version_bareme,
        description=description,
        effets=_determiner_effets(nouveau_niveau),
        recours_disponibles=_determiner_recours(nouveau_niveau),
        erreurs=erreurs,
    )


def appliquer_credit_social(
    entite: Dict[str, Any],
    cause: str,
    version_bareme: int = 1,
    description: str = "",
) -> CreditSocialResult:
    """
    Applique le calcul de crédit social à une entité dict et met à jour son score.

    L'entité doit avoir une clé 'scores' avec une clé 'credit_social'.
    L'entité est modifiée en place.
    """
    entite_id = entite.get("id", "<inconnu>")
    scores = entite.get("scores", {})
    credit_courant = scores.get("credit_social", 70)

    result = calculer_credit_social(
        entite_id=entite_id,
        cause=cause,
        credit_courant=credit_courant,
        version_bareme=version_bareme,
        description=description,
    )

    if result.ok:
        if "scores" not in entite:
            entite["scores"] = {}
        entite["scores"]["credit_social"] = result.nouveau_credit

    return result
