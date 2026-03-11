# Utilisation de la CLI AI10101IA

> Référence canonique pour T0031.  
> Ce document décrit les commandes locales disponibles pour piloter
> le registre AI10101IA sans interface utilisateur finale.

---

## 1. Prérequis

```bash
pip install -r requirements.txt
```

Python 3.10+ requis. PyYAML doit être installé.

---

## 2. Commandes disponibles via `make`

| Commande | Description |
|---|---|
| `make validate` | Valide le registre de tâches et la checklist |
| `make validate-domain` | Valide les assets métier (entités, preuves, événements) |
| `make test` | Lance tous les tests automatisés |
| `make audit` | Génère le rapport d'audit dans `/tmp/audit_report.md` |
| `make pilot` | Exécute le flux bout-en-bout pilote complet |

---

## 3. CLI `run_registry_cli.py`

### 3.1 Chargement du dataset bootstrap

```bash
python scripts/run_registry_cli.py load
```

Résumé du nombre d'entités, preuves et événements chargés.

### 3.2 Validation du domaine

```bash
python scripts/run_registry_cli.py validate
```

Exécute `validate_domain_assets.py` sur les fichiers bootstrap par défaut.
Retourne 0 si tout est valide, 1 sinon.

### 3.3 Affichage d'une entité par identifiant

```bash
python scripts/run_registry_cli.py show ROBOT-0001
python scripts/run_registry_cli.py show DIEU-001
python scripts/run_registry_cli.py show ACADEMIE-002
```

Affiche les détails complets de l'entité au format YAML.

### 3.4 Liste des entités par type

```bash
python scripts/run_registry_cli.py list ROBOT
python scripts/run_registry_cli.py list DIEU
python scripts/run_registry_cli.py list ACADEMIE
python scripts/run_registry_cli.py list LIGNEE
python scripts/run_registry_cli.py list REGLE
python scripts/run_registry_cli.py list COMMANDE
```

Types disponibles : `ROBOT`, `DIEU`, `ACADEMIE`, `LIGNEE`, `REGLE`, `COMMANDE`.

### 3.5 Reconstruction du multi-index pilote

```bash
python scripts/run_registry_cli.py index
```

Affiche les cinq index : identité, type, statut, filiation, scores.

### 3.6 Vue d'audit résumée

```bash
python scripts/run_registry_cli.py audit
```

Délègue à `build_audit_report.py` et affiche le rapport sur stdout.

### 3.7 Options communes

Tous les sous-commandes acceptent :

```bash
--entities <chemin>    # Chemin vers bootstrap_entities.yaml
--proofs <chemin>      # Chemin vers bootstrap_proofs.yaml
--events <chemin>      # Chemin vers bootstrap_events.yaml
```

---

## 4. Script `validate_domain_assets.py`

```bash
python scripts/validate_domain_assets.py
python scripts/validate_domain_assets.py \
  --entities project/bootstrap_entities.yaml \
  --proofs project/bootstrap_proofs.yaml \
  --events project/bootstrap_events.yaml
```

Valide :

- présence et cohérence des sections (hub, dieux, académies, robots, lignées, règles, commandes)
- relations inter-entités (lignée, académie, dieu tuteur)
- filiation des robots (parent existant)
- cohérence des scores (>= 0)
- format et cohérence des preuves
- références des événements

**Code de retour** : 0 = succès, 1 = erreur.

---

## 5. Script `build_audit_report.py`

```bash
# Sortie Markdown sur stdout
python scripts/build_audit_report.py

# Sortie JSON dans un fichier
python scripts/build_audit_report.py --format json --output /tmp/audit.json

# Sortie Markdown dans un fichier
python scripts/build_audit_report.py --format markdown --output /tmp/audit.md
```

Génère :

- synthèse du registre bootstrap
- relations de filiation
- preuves par entité
- incohérences détectées
- bilan global

---

## 6. Script `run_pilot_flow.py`

```bash
# Flux complet
python scripts/run_pilot_flow.py

# Avec rapport d'audit dans un fichier
python scripts/run_pilot_flow.py --audit-output /tmp/pilot_audit.md

# Mode verbeux
python scripts/run_pilot_flow.py --verbose
```

Exécute les 7 étapes du flux bout-en-bout pilote (T0033).

---

## 7. Codes de retour

| Code | Signification |
|---|---|
| 0 | Succès |
| 1 | Erreur détectée (voir stderr) |

---

## 8. Exemples de session complète

```bash
# Valider tout le domaine
make validate-domain

# Inspecter un robot
python scripts/run_registry_cli.py show ROBOT-0001

# Inspecter la lignée Axiom
python scripts/run_registry_cli.py show LIGNEE-001

# Générer un rapport d'audit complet
python scripts/build_audit_report.py --output /tmp/audit_ai10101ia.md

# Rejouer le flux pilote bout-en-bout
make pilot
```
