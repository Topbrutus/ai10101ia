# Dataset pilote AI10101IA

> Référence canonique pour T0029.  
> Ce document décrit le dataset bootstrap canonique, son contenu, sa cohérence
> et la façon de l'utiliser pour valider le système localement.

---

## 1. Objectif

Le dataset bootstrap est le jeu de données pilote minimal permettant de :

- charger le système sans données manuelles
- valider les schémas, règles et relations inter-entités
- démontrer un flux bout-en-bout traçable
- servir de base aux tests automatisés

Il est versionné, canonique et cohérent avec les schémas métier (T0018),
le registre central (T0019), le moteur de règles (T0020), le bus slash (T0021),
le multi-index (T0022) et le modèle d'audit (T0023).

---

## 2. Fichiers du dataset

| Fichier | Contenu |
|---|---|
| `project/bootstrap_entities.yaml` | Toutes les entités pilotes (hub, dieux, académies, robots, lignées, règles, commandes) |
| `project/bootstrap_proofs.yaml` | Preuves pilotes rattachées aux entités et aux tâches |
| `project/bootstrap_events.yaml` | Événements pilotes jalonnant le flux bout-en-bout |

---

## 3. Contenu du dataset

### 3.1 Hub

Un hub pilote unique :

| ID | Nom | Statut |
|---|---|---|
| `HUB-001` | Hub Pilote AI10101IA | actif |

### 3.2 Dieux

Trois dieux couvrant les domaines fondamentaux :

| ID | Nom | Domaine | Académie supervisée |
|---|---|---|---|
| `DIEU-001` | Anaxis | Logique et cohérence | ACADEMIE-001 |
| `DIEU-002` | Orialys | Mémoire et audit | ACADEMIE-002 |
| `DIEU-003` | Vortex | Exécution et performance | ACADEMIE-001 |

### 3.3 Académies

Deux académies reliées aux dieux tuteurs :

| ID | Nom | Dieu tuteur | Robots hébergés |
|---|---|---|---|
| `ACADEMIE-001` | Académie de Logique Appliquée | DIEU-001 | ROBOT-0001, ROBOT-0002, ROBOT-0004 |
| `ACADEMIE-002` | Académie de la Mémoire Structurée | DIEU-002 | ROBOT-0003 |

### 3.4 Robots

Quatre robots de trois classes différentes :

| ID | Nom | Classe | Lignée | Génération | Points | Prestige | Crédit social |
|---|---|---|---|---|---|---|---|
| `ROBOT-0001` | Axiom-Alpha | Validateur | LIGNEE-001 | 1 | 150 | 12 | 85 |
| `ROBOT-0002` | Axiom-Beta | Validateur | LIGNEE-001 | 2 | 60 | 4 | 70 |
| `ROBOT-0003` | Mnemo-Prime | Archiviste | LIGNEE-002 | 1 | 200 | 18 | 90 |
| `ROBOT-0004` | Exec-One | Exécuteur | LIGNEE-003 | 1 | 30 | 2 | 65 |

Filiation : `ROBOT-0002` est descendant de `ROBOT-0001` (même lignée `LIGNEE-001`).

### 3.5 Lignées

Trois lignées cohérentes :

| ID | Nom | Classe dominante | Fondateur | Membres |
|---|---|---|---|---|
| `LIGNEE-001` | Lignée Axiom | Validateur | ROBOT-0001 | ROBOT-0001, ROBOT-0002 |
| `LIGNEE-002` | Lignée Mnemo | Archiviste | ROBOT-0003 | ROBOT-0003 |
| `LIGNEE-003` | Lignée Exec | Exécuteur | ROBOT-0004 | ROBOT-0004 |

### 3.6 Règles

Deux règles métier pilotes :

| ID | Nom | Action |
|---|---|---|
| `REGLE-0001` | Règle de cohérence des scores | Valider que les scores sont positifs ou nuls |
| `REGLE-0002` | Règle de filiation | Valider que le parent déclaré existe dans la même lignée |

### 3.7 Commandes

Trois commandes slash pilotes :

| ID | Slash | Description |
|---|---|---|
| `COMMANDE-0001` | `/entite.afficher` | Afficher une entité par ID |
| `COMMANDE-0002` | `/entite.lister` | Lister les entités par type |
| `COMMANDE-0003` | `/audit.exporter` | Générer et exporter une vue d'audit |

### 3.8 Preuves

Six preuves pilotes couvrant : validation de tâche, création d'entités,
exécution de règles, opération d'index.

### 3.9 Événements

Six événements jalonnant le flux bout-en-bout : chargement, validation,
exécution de règles, reconstruction d'index, export d'audit.

---

## 4. Cohérence et invariants

Les invariants suivants doivent être vérifiés par le pipeline de validation (T0030) :

1. Tout robot référence un `lignee_id` existant dans `lignees`.
2. Tout robot référence un `academie_id` existant dans `academies`.
3. Tout robot référence un `dieu_tuteur` existant dans `dieux`.
4. Toute académie référence un `dieu_tuteur` existant dans `dieux`.
5. Toute lignée référence un `fondateur_id` existant dans `robots`.
6. Les membres d'une lignée existent tous dans `robots`.
7. Toute relation `descendant_de` pointe vers un robot existant.
8. Les scores (points, prestige, crédit social) sont des entiers >= 0.
9. Toute preuve référence une `tache_id` ou `entite_id` existante.
10. Tout événement référence un `hub_id` existant.

---

## 5. Chargement

```bash
# Valider le dataset
make validate-domain

# Charger via CLI
python scripts/run_registry_cli.py load

# Afficher une entité
python scripts/run_registry_cli.py show ROBOT-0001

# Lister par type
python scripts/run_registry_cli.py list ROBOT
```

---

## 6. Dépendances

Ce dataset s'appuie sur :

- `docs/CENTRAL_REGISTRY.md` (T0019) : structure des entités
- `docs/RULE_ENGINE_CONTRACT.md` (T0020) : format des règles
- `docs/SLASH_BUS_CONTRACT.md` (T0021) : format des commandes
- `docs/MULTI_INDEX.md` (T0022) : structure du multi-index
- `docs/AUDIT_MODEL.md` (T0023) : format des preuves

Il est utilisé par :

- `scripts/validate_domain_assets.py` (T0030)
- `scripts/run_registry_cli.py` (T0031)
- `scripts/build_audit_report.py` (T0032)
- `scripts/run_pilot_flow.py` (T0033)
