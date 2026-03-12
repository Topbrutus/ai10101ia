"""Outils de fondation pour le dépôt GitHub contrôlé par tâches."""

from .registry_tools import load_yaml, render_master_todo, validate_registry_data, verify_master_todo
from .pr_tools import extract_task_ids, validate_pr_body
from .zip_tools import build_zip
from .score_points import calculer_points, appliquer_points, get_bareme
from .score_prestige import calculer_prestige, appliquer_prestige, get_bareme_prestige
from .score_social import calculer_credit_social, appliquer_credit_social, get_niveau_credit_social
from .academy_workflows import inscrire_robot, passer_examen, promouvoir_robot, sanctionner_robot, classer_robots
from .reproduction import creer_robot_descendant, creer_lignee, verifier_eligibilite_reproduction

__all__ = [
    "load_yaml",
    "render_master_todo",
    "validate_registry_data",
    "verify_master_todo",
    "extract_task_ids",
    "validate_pr_body",
    "build_zip",
    "calculer_points",
    "appliquer_points",
    "get_bareme",
    "calculer_prestige",
    "appliquer_prestige",
    "get_bareme_prestige",
    "calculer_credit_social",
    "appliquer_credit_social",
    "get_niveau_credit_social",
    "inscrire_robot",
    "passer_examen",
    "promouvoir_robot",
    "sanctionner_robot",
    "classer_robots",
    "creer_robot_descendant",
    "creer_lignee",
    "verifier_eligibilite_reproduction",
]
