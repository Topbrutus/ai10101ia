# Flux pilote bout-en-bout AI10101IA

> Référence canonique pour T0033.  
> Ce document décrit le flux pilote complet et traçable permettant de valider
> le système de bout en bout sur le dataset bootstrap.

---

## 1. Objectif

Le flux pilote démontre que le système AI10101IA est opérationnel localement :
toutes les briques fondamentales fonctionnent ensemble de manière cohérente
sur un jeu de données réel et versionné.

---

## 2. Prérequis

```bash
pip install -r requirements.txt
```

Fichiers requis :

- `project/bootstrap_entities.yaml`
- `project/bootstrap_proofs.yaml`
- `project/bootstrap_events.yaml`

---

## 3. Étapes du flux

Le flux se compose de 7 étapes exécutées en séquence :

| Étape | Nom | Description |
|---|---|---|
| 1 | Chargement | Charger les entités, preuves et événements bootstrap |
| 2 | Validation | Valider le domaine (schémas, relations, scores, preuves) |
| 3 | Consultation | Consulter et lister des entités par type |
| 4 | Preuves | Vérifier que les preuves sont rattachées à des entités existantes |
| 5 | Multi-index | Reconstruire et afficher le multi-index pilote |
| 6 | Audit | Générer la vue d'audit complète |
| 7 | Cohérence | Vérification finale de cohérence globale |

---

## 4. Exécution

### Via make (recommandé)

```bash
make pilot
```

### Directement

```bash
python scripts/run_pilot_flow.py
```

### Avec rapport d'audit dans un fichier

```bash
python scripts/run_pilot_flow.py --audit-output /tmp/pilot_audit.md
```

### Mode verbeux

```bash
python scripts/run_pilot_flow.py --verbose
```

---

## 5. Sortie attendue

```
╔══════════════════════════════════════════════╗
║    Flux pilote bout-en-bout — AI10101IA       ║
╚══════════════════════════════════════════════╝

[Étape 1] Chargement du dataset bootstrap
  ✓ Hub chargé : HUB-001
  ✓ Dieux        : 3 entité(s)
  ...

[Étape 2] Validation du domaine
  ✓ OK: validation métier réussie.
  ...

[Étape 7] Vérification de cohérence globale
  ✓ Cohérence globale validée.

╔══════════════════════════════════════════════╗
║    Bilan du flux pilote                       ║
╚══════════════════════════════════════════════╝
  ✓ Chargement
  ✓ Validation
  ✓ Consultation
  ✓ Preuves
  ✓ Multi-index
  ✓ Audit
  ✓ Cohérence

RÉSULTAT: flux pilote réussi. Toutes les étapes sont OK.
```

---

## 6. Rejouer le flux

Le flux est entièrement rejouable à partir des fichiers versionés :

```bash
# Depuis la racine du dépôt
make pilot
```

Aucune donnée manuelle n'est nécessaire.
Le flux est déterministe : le même dataset produit toujours le même résultat.

---

## 7. Tests automatisés

Le flux pilote est couvert par des tests dans `tests/test_pilot_flow.py` :

```bash
make test
```

Les tests vérifient :

- la validation du domaine sur le dataset bootstrap
- le chargement et la cohérence des entités
- la génération du rapport d'audit
- le résultat global du flux pilote

---

## 8. Dépendances du flux

| Composant | Tâche | Fichier |
|---|---|---|
| Dataset bootstrap | T0029 | `project/bootstrap_entities.yaml` |
| Validation métier | T0030 | `scripts/validate_domain_assets.py` |
| CLI de pilotage | T0031 | `scripts/run_registry_cli.py` |
| Vue d'audit | T0032 | `scripts/build_audit_report.py` |
| Flux pilote | T0033 | `scripts/run_pilot_flow.py` |

---

## 9. Limites du flux pilote

Ce flux pilote couvre uniquement le périmètre bootstrap :

- il ne simule pas les académies en fonctionnement (T0027+)
- il ne déclenche pas de reproduction (T0028+)
- il ne simule pas d'élection (T0029 originel)
- il ne déploie pas en production (T0034+)

Il sert de base solide pour les phases suivantes.
