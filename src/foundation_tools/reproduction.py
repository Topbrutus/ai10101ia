"""
reproduction.py — Workflow de reproduction contrôlée AI10101IA (T0028).

Permet la création de nouvelles lignées et robots avec contrôle
des quotas et héritages.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

QUOTA_DEFAUT_LIGNEE = 10
SCORE_MIN_REPRODUCTION = 50
PRESTIGE_MIN_REPRODUCTION = 5
CREDIT_SOCIAL_MIN_REPRODUCTION = 60

HERITAGE_POINTS_RATIO = 0.6
HERITAGE_PRESTIGE_RATIO = 0.8
HERITAGE_CREDIT_SOCIAL_RATIO = 1.0


# ---------------------------------------------------------------------------
# Résultat
# ---------------------------------------------------------------------------

@dataclass
class ReproductionResult:
    succes: bool
    operation: str
    parent_id: str
    details: Dict[str, Any] = field(default_factory=dict)
    erreurs: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.succes and not self.erreurs


# ---------------------------------------------------------------------------
# Vérification des pré-conditions
# ---------------------------------------------------------------------------

def verifier_eligibilite_reproduction(
    robot: Dict[str, Any],
    lignee: Dict[str, Any],
    niveau_maitrise_requis: int = 1,
) -> List[str]:
    """
    Vérifie si un robot est éligible à la reproduction.

    Returns:
        Liste d'erreurs. Vide si éligible.
    """
    erreurs: List[str] = []
    robot_id = robot.get("id", "<inconnu>")

    if robot.get("statut") != "actif":
        erreurs.append(f"Robot {robot_id} : statut '{robot.get('statut')}' incompatible avec la reproduction.")

    scores = robot.get("scores", {})
    points = scores.get("points", 0)
    prestige = scores.get("prestige", 0)
    credit_social = scores.get("credit_social", 0)

    if points < SCORE_MIN_REPRODUCTION:
        erreurs.append(
            f"Robot {robot_id} : points insuffisants pour reproduction "
            f"({points} < {SCORE_MIN_REPRODUCTION})."
        )
    if prestige < PRESTIGE_MIN_REPRODUCTION:
        erreurs.append(
            f"Robot {robot_id} : prestige insuffisant pour reproduction "
            f"({prestige} < {PRESTIGE_MIN_REPRODUCTION})."
        )
    if credit_social < CREDIT_SOCIAL_MIN_REPRODUCTION:
        erreurs.append(
            f"Robot {robot_id} : crédit social insuffisant pour reproduction "
            f"({credit_social} < {CREDIT_SOCIAL_MIN_REPRODUCTION})."
        )

    niveau = robot.get("niveau_maitrise", 0)
    if niveau < niveau_maitrise_requis:
        erreurs.append(
            f"Robot {robot_id} : niveau de maîtrise insuffisant "
            f"({niveau} < {niveau_maitrise_requis})."
        )

    membres = lignee.get("membres", [])
    quota_max = lignee.get("quota_membres_max", QUOTA_DEFAUT_LIGNEE)
    if len(membres) >= quota_max:
        erreurs.append(
            f"Lignée {lignee.get('id', '<inconnu>')} : quota atteint "
            f"({len(membres)}/{quota_max} membres)."
        )

    return erreurs


# ---------------------------------------------------------------------------
# Calcul de l'héritage
# ---------------------------------------------------------------------------

def calculer_heritage(
    parent: Dict[str, Any],
    points_ratio: float = HERITAGE_POINTS_RATIO,
    prestige_ratio: float = HERITAGE_PRESTIGE_RATIO,
    credit_social_ratio: float = HERITAGE_CREDIT_SOCIAL_RATIO,
) -> Dict[str, int]:
    """
    Calcule les scores hérités d'un parent.

    Returns:
        Dict avec les scores hérités (points, prestige, credit_social).
    """
    scores_parent = parent.get("scores", {})
    return {
        "points": max(0, int(scores_parent.get("points", 0) * points_ratio)),
        "prestige": max(0, int(scores_parent.get("prestige", 0) * prestige_ratio)),
        "credit_social": max(
            0,
            min(100, int(scores_parent.get("credit_social", 70) * credit_social_ratio)),
        ),
    }


# ---------------------------------------------------------------------------
# Création d'un robot descendant
# ---------------------------------------------------------------------------

def creer_robot_descendant(
    parent: Dict[str, Any],
    lignee: Dict[str, Any],
    nouvel_id: str,
    nom: str,
    niveau_maitrise_requis: int = 1,
) -> ReproductionResult:
    """
    Crée un robot descendant à partir d'un parent.

    Vérifie les pré-conditions, calcule l'héritage et instancie le nouveau robot.

    Args:
        parent: Entité robot parent.
        lignee: Entité lignée dans laquelle créer le descendant.
        nouvel_id: Identifiant du nouveau robot.
        nom: Nom du nouveau robot.
        niveau_maitrise_requis: Niveau de maîtrise minimum requis du parent.

    Returns:
        ReproductionResult avec le nouveau robot dans details['robot'] si succès.
    """
    parent_id = parent.get("id", "<inconnu>")

    erreurs = verifier_eligibilite_reproduction(parent, lignee, niveau_maitrise_requis)
    if erreurs:
        return ReproductionResult(succes=False, operation="creation_descendant", parent_id=parent_id, erreurs=erreurs)

    if not nouvel_id or not nouvel_id.strip():
        return ReproductionResult(
            succes=False,
            operation="creation_descendant",
            parent_id=parent_id,
            erreurs=["nouvel_id ne peut pas être vide."],
        )

    scores_herites = calculer_heritage(parent)

    nouveau_robot: Dict[str, Any] = {
        "id": nouvel_id,
        "nom": nom,
        "type": "ROBOT",
        "version": 1,
        "statut": "actif",
        "classe": parent.get("classe"),
        "lignee_id": lignee.get("id"),
        "academie_id": None,
        "dieu_tuteur": parent.get("dieu_tuteur"),
        "hub_id": parent.get("hub_id"),
        "niveau_maitrise": 0,
        "scores": scores_herites,
        "relations": [
            {"type": "descendant_de", "cible": parent_id},
            {"type": "appartient_a", "cible": lignee.get("id")},
        ],
        "metadonnees": {
            "parent_id": parent_id,
            "generation": (parent.get("metadonnees", {}).get("generation", 1) + 1),
        },
    }

    if "membres" not in lignee:
        lignee["membres"] = []
    if nouvel_id not in lignee["membres"]:
        lignee["membres"].append(nouvel_id)

    return ReproductionResult(
        succes=True,
        operation="creation_descendant",
        parent_id=parent_id,
        details={
            "robot": nouveau_robot,
            "lignee_id": lignee.get("id"),
            "scores_herites": scores_herites,
        },
    )


# ---------------------------------------------------------------------------
# Création d'une nouvelle lignée
# ---------------------------------------------------------------------------

def creer_lignee(
    fondateur: Dict[str, Any],
    nouvel_id: str,
    nom: str,
    dieu_tuteur_id: str,
    quota_max: int = QUOTA_DEFAUT_LIGNEE,
) -> ReproductionResult:
    """
    Crée une nouvelle lignée à partir d'un robot fondateur.

    Args:
        fondateur: Entité robot fondateur.
        nouvel_id: Identifiant de la nouvelle lignée.
        nom: Nom de la nouvelle lignée.
        dieu_tuteur_id: Identifiant du dieu tuteur.
        quota_max: Quota maximal de membres.

    Returns:
        ReproductionResult avec la nouvelle lignée dans details['lignee'] si succès.
    """
    fondateur_id = fondateur.get("id", "<inconnu>")
    erreurs: List[str] = []

    if fondateur.get("statut") != "actif":
        erreurs.append(
            f"Fondateur {fondateur_id} : statut '{fondateur.get('statut')}' "
            "incompatible avec la création d'une lignée."
        )

    if not nouvel_id or not nouvel_id.strip():
        erreurs.append("nouvel_id de la lignée ne peut pas être vide.")

    if not nom or not nom.strip():
        erreurs.append("Le nom de la lignée ne peut pas être vide.")

    if not dieu_tuteur_id:
        erreurs.append("Le dieu_tuteur_id ne peut pas être vide.")

    if quota_max < 1:
        erreurs.append(f"quota_max invalide : {quota_max} (doit être >= 1).")

    if erreurs:
        return ReproductionResult(succes=False, operation="creation_lignee", parent_id=fondateur_id, erreurs=erreurs)

    nouvelle_lignee: Dict[str, Any] = {
        "id": nouvel_id,
        "nom": nom,
        "type": "LIGNEE",
        "version": 1,
        "statut": "actif",
        "classe_dominante": fondateur.get("classe"),
        "fondateur_id": fondateur_id,
        "hub_id": fondateur.get("hub_id"),
        "dieu_tuteur": dieu_tuteur_id,
        "membres": [fondateur_id],
        "quota_membres_max": quota_max,
        "relations": [],
        "metadonnees": {"bootstrap": False},
    }

    fondateur["lignee_id"] = nouvel_id

    return ReproductionResult(
        succes=True,
        operation="creation_lignee",
        parent_id=fondateur_id,
        details={
            "lignee": nouvelle_lignee,
            "fondateur_id": fondateur_id,
        },
    )
