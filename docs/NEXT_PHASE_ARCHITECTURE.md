# Architecture de la prochaine phase — AI10101IA

> Référence : T0040 — Préparation de la suite industrielle

## Objet

Ce document décrit l'architecture cible de la phase d'industrialisation qui suit la fondation.
Il pose les blocs structurels sans les implémenter dans cette PR.

---

## Positionnement

```
[ FONDATION ]  →  [ INDUSTRIALISATION ]  →  [ PRODUCTION ]
T0001–T0040         T0034–T0038+              Post-go/no-go
  (done)            (à construire)             (futur)
```

La fondation est le socle. L'industrialisation construit sur ce socle.
La production n'est pas ouverte dans cette phase.

---

## Blocs architecturaux de la phase d'industrialisation

### 1. Infrastructure d'exploitation

**Périmètre** :
- Installation reproductible sur environnement staging
- Sauvegarde automatisée et testée
- Procédures de restauration documentées et exercées

**Dépendances fondation** : T0029, T0030, T0031, T0032, T0033

**Nouveaux composants** :
- `docs/OPERATIONS.md`
- Scripts de sauvegarde/restauration dans `scripts/`
- Runbook staging dans `docs/`

---

### 2. Readiness production

**Périmètre** :
- Checklist go/no-go production formelle
- Workflows CI renforcés pour l'environnement cible
- Validation des rulesets GitHub et CODEOWNERS

**Dépendances** : Infrastructure d'exploitation complète

**Nouveaux composants** :
- `docs/PRODUCTION_READINESS.md`
- Workflows CI mis à jour dans `.github/workflows/`

---

### 3. Exploitation quotidienne

**Périmètre** :
- Runbooks opérateur (support L1/L2, maintenance, escalade)
- Procédures de mise à jour sécurisées

**Dépendances** : Readiness production

**Nouveaux composants** :
- `docs/RUNBOOKS.md`

---

### 4. Hub étendu

**Périmètre** :
- Extension du hub minimal pilote
- Support de volumes supérieurs au bootstrap
- APIs ou interfaces de chargement de données réelles

**Dépendances** :
- Exploitation quotidienne opérationnelle
- Tests de charge validés

**Nouveaux composants** (à définir en détail) :
- `src/foundation_tools/hub_extended.py` ou équivalent
- `docs/HUB_EXTENDED.md`

---

### 5. Académies exécutables complètes

**Périmètre** :
- Parcours d'entraînement, d'examen et de promotion opérationnels sur données réelles
- Volume représentatif de la production

**Dépendances** :
- Hub étendu opérationnel
- Tests de charge académies validés

**Nouveaux composants** (à définir en détail) :
- Extensions de `src/foundation_tools/academy_workflows.py`
- Nouveaux jeux de données de test

---

### 6. Reproduction réelle

**Périmètre** :
- Workflow de reproduction activé sur données réelles
- Quotas et garde-fous validés sous charge

**Dépendances** :
- Hub étendu opérationnel
- Académies exécutables complètes
- Go/no-go production validé

**Nouveaux composants** (à définir en détail) :
- Extensions de `src/foundation_tools/reproduction.py`
- Preuves de reproduction archivées dans `records/`

---

### 7. Gouvernance multi-hub

**Périmètre** :
- Charte de synchronisation inter-hubs
- Audit multi-hub
- Règles d'arbitrage entre hubs

**Dépendances** :
- Hub étendu opérationnel
- Reproduction réelle maîtrisée

**Nouveaux composants** :
- `docs/MULTI_HUB_GOVERNANCE.md`
- Architecture inter-hub à définir

---

### 8. Robot élu

**Périmètre** :
- Critères formels d'élection
- Simulation puis activation réelle du robot élu
- Gouvernance du robot élu dans le système

**Dépendances** :
- Multi-hub gouverné
- Reproduction réelle maîtrisée
- Tests avancés validés
- Crédit social validé en production

**Nouveaux composants** (à définir en détail) :
- Plan de simulation formalisé
- Critères d'élection documentés
- Workflows d'activation

---

## Interfaces entre fondation et industrialisation

| Interface | Source fondation | Cible industrialisation |
|---|---|---|
| Dataset bootstrap | `project/bootstrap_*.yaml` | Données réelles de staging |
| Schémas métier | `src/foundation_tools/` | Extensions versionnées |
| Registre central | `project/todo_registry.yaml` | Registre de tâches étendu |
| CLI pilote | `scripts/run_registry_cli.py` | CLI industrielle |
| Flux pilote | `scripts/run_pilot_flow.py` | Flux de production |
| Politiques | `project/project_policy.yaml` | Politique de production |

---

## Répertoires futurs à réserver

Les répertoires suivants sont réservés pour la phase d'industrialisation
mais ne doivent pas être créés prématurément :

```
records/          ← archivage des preuves et décisions formelles
docs/runbooks/    ← documentation opérateur détaillée (si volume important)
staging/          ← configuration staging (si nécessaire)
```

---

## Contraintes architecturales à respecter

1. **Rétrocompatibilité des schémas** : toute évolution doit être versionnée.
2. **Traçabilité des décisions** : chaque choix architectural doit être enregistré.
3. **Tests avant activation** : aucun bloc ne s'active sans tests de non-régression.
4. **Preuves obligatoires** : chaque bloc doit produire des preuves archivables.
5. **Gouvernance maintenue** : les règles de la fondation s'appliquent à l'industrialisation.

---

## Références croisées

- `docs/INDUSTRIALIZATION_ROADMAP.md` — feuille de route détaillée
- `docs/PROJECT_PHASES.md` — phases officielles du projet
- `docs/RELEASE_GATES.md` — gates de release
- `docs/REPOSITORY_STRUCTURE.md` — structure du dépôt
