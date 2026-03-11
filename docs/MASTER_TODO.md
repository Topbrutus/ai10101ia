# Checklist maître du projet

> Document généré automatiquement depuis `project/todo_registry.yaml`. Ne pas modifier à la main.

## Métadonnées

- **Nom** : Registre maître des tâches
- **Description** : Source de vérité machine pour la checklist obligatoire du dépôt.
- **Propriétaire** : Topbrutus
- **Langue** : fr

## 01. Cadrage (`P1-CADRAGE`)

- **Gate de sortie** : Mission, périmètre, vocabulaire et critères d’acceptation validés.

- [x] **T0001 — Formaliser la charte du projet**
  - Ordre : 1
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : Aucune
  - Description : Établir l’objectif, le périmètre, les non-objectifs, le vocabulaire canonique et les critères d’acceptation du dépôt de fondation.
  - Preuve requise : Document de cadrage validé dans docs/PROJECT_PHASES.md et README.md.
  - Validation requise : Revue documentaire.
  - Livrables attendus : README.md, docs/PROJECT_PHASES.md
  - Fichiers potentiellement impactés : README.md, docs/PROJECT_PHASES.md

- [x] **T0002 — Fixer la gouvernance et les règles d’arbitrage**
  - Ordre : 2
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0001
  - Description : Définir qui peut changer quoi, comment une tâche obligatoire peut être modifiée, et quelles validations sont requises.
  - Preuve requise : Gouvernance documentée et versionnée.
  - Validation requise : Revue gouvernance.
  - Livrables attendus : docs/GOVERNANCE.md, project/project_policy.yaml
  - Fichiers potentiellement impactés : docs/GOVERNANCE.md, project/project_policy.yaml

## 02. Fondation du dépôt (`P2-FONDATION`)

- **Gate de sortie** : Dépôt, structure, registre machine et checklist humaine validés.

- [x] **T0003 — Poser la structure du dépôt**
  - Ordre : 3
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0001, T0002
  - Description : Créer l’arborescence de base, les conventions d’édition, les fichiers racine et les répertoires obligatoires.
  - Preuve requise : Arborescence commitée avec règles de placement.
  - Validation requise : Validation structurelle.
  - Livrables attendus : .editorconfig, .gitattributes, .gitignore, docs/REPOSITORY_STRUCTURE.md
  - Fichiers potentiellement impactés : .editorconfig, .gitattributes, .gitignore, docs/REPOSITORY_STRUCTURE.md

- [x] **T0004 — Créer le registre machine des tâches**
  - Ordre : 4
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0001, T0002, T0003
  - Description : Transformer la checklist fondatrice en registre machine stable, ordonné et validable automatiquement.
  - Preuve requise : Registre YAML validé sans doublon ni trou.
  - Validation requise : Validation automatique + revue.
  - Livrables attendus : project/todo_registry.yaml
  - Fichiers potentiellement impactés : project/todo_registry.yaml

- [x] **T0005 — Créer la checklist maître lisible**
  - Ordre : 5
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0004
  - Description : Publier la vue humaine imprimable dérivée du registre machine, sans divergence de contenu.
  - Preuve requise : Checklist synchronisée avec le registre.
  - Validation requise : Validation automatique de synchronisation.
  - Livrables attendus : docs/MASTER_TODO.md
  - Fichiers potentiellement impactés : docs/MASTER_TODO.md

- [x] **T0006 — Écrire les scripts de validation du registre**
  - Ordre : 6
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0004
  - Description : Fournir des scripts Python robustes pour valider le registre, ses dépendances et sa numérotation.
  - Preuve requise : Scripts exécutables avec tests verts.
  - Validation requise : Tests unitaires.
  - Livrables attendus : scripts/validate_todo_registry.py, scripts/check_dependencies.py
  - Fichiers potentiellement impactés : scripts/validate_todo_registry.py, scripts/check_dependencies.py, tests/test_validate_todo_registry.py, tests/test_check_dependencies.py

- [x] **T0007 — Écrire le mécanisme de synchronisation Markdown ↔ registre**
  - Ordre : 7
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0004, T0005
  - Description : Permettre la génération ou la vérification stricte de docs/MASTER_TODO.md depuis le registre machine.
  - Preuve requise : Commande de check et de write fonctionnelle.
  - Validation requise : Tests unitaires.
  - Livrables attendus : scripts/sync_checklist.py
  - Fichiers potentiellement impactés : scripts/sync_checklist.py, tests/test_sync_checklist.py

## 03. Contrôles GitHub (`P3-CONTROLES-GITHUB`)

- **Gate de sortie** : PR gate, issue forms, instructions agents et workflows actifs.

- [x] **T0008 — Imposer le workflow de pull request**
  - Ordre : 8
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0002, T0004, T0005
  - Description : Forcer les contributeurs et agents à référencer les tâches, fournir preuves et validations, et déclarer les risques.
  - Preuve requise : Template de PR et validateur de corps de PR commités.
  - Validation requise : Exécution sur PR test.
  - Livrables attendus : .github/PULL_REQUEST_TEMPLATE.md, scripts/validate_pr_body.py
  - Fichiers potentiellement impactés : .github/PULL_REQUEST_TEMPLATE.md, scripts/validate_pr_body.py

- [x] **T0009 — Installer les garde-fous GitHub Actions**
  - Ordre : 9
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0006, T0007, T0008
  - Description : Bloquer automatiquement les PR non conformes et valider le registre, la checklist et les dépendances.
  - Preuve requise : Workflows GitHub Actions exécutables.
  - Validation requise : Lint YAML + simulation de workflows.
  - Livrables attendus : .github/workflows/validate_todo_registry.yml, .github/workflows/pr_gate.yml, .github/workflows/sync_checklist.yml
  - Fichiers potentiellement impactés : .github/workflows/validate_todo_registry.yml, .github/workflows/pr_gate.yml, .github/workflows/sync_checklist.yml

- [x] **T0010 — Structurer les formulaires d’issues**
  - Ordre : 10
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0004, T0008
  - Description : Fournir des formulaires GitHub pour tâche, bug, fonctionnalité et décision avec référence de tâche quand applicable.
  - Preuve requise : Formulaires d’issues versionnés.
  - Validation requise : Revue manuelle GitHub.
  - Livrables attendus : .github/ISSUE_TEMPLATE/task.yml, .github/ISSUE_TEMPLATE/bug.yml, .github/ISSUE_TEMPLATE/feature.yml, .github/ISSUE_TEMPLATE/decision.yml
  - Fichiers potentiellement impactés : .github/ISSUE_TEMPLATE/config.yml, .github/ISSUE_TEMPLATE/task.yml, .github/ISSUE_TEMPLATE/bug.yml, .github/ISSUE_TEMPLATE/feature.yml, .github/ISSUE_TEMPLATE/decision.yml

- [x] **T0011 — Encadrer Copilot et les agents**
  - Ordre : 11
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0002, T0004, T0008
  - Description : Écrire les consignes de dépôt, Copilot et agents pour interdire toute action hors checklist et hors dépendances.
  - Preuve requise : Fichiers d’instructions commités.
  - Validation requise : Revue documentaire.
  - Livrables attendus : AGENTS.md, .github/copilot-instructions.md, .github/instructions/task-enforcement.instructions.md, .github/instructions/repository-guard.instructions.md
  - Fichiers potentiellement impactés : AGENTS.md, .github/copilot-instructions.md, .github/instructions/task-enforcement.instructions.md, .github/instructions/repository-guard.instructions.md

- [x] **T0012 — Documenter les règles de preuve et de validation**
  - Ordre : 12
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0002, T0008
  - Description : Préciser ce qui compte comme preuve, comme validation et comment le référencer dans issues et PR.
  - Preuve requise : Politiques détaillées versionnées.
  - Validation requise : Revue qualité.
  - Livrables attendus : docs/EVIDENCE_POLICY.md, docs/VALIDATION_POLICY.md
  - Fichiers potentiellement impactés : docs/EVIDENCE_POLICY.md, docs/VALIDATION_POLICY.md

- [x] **T0013 — Documenter la mise en place des rulesets GitHub**
  - Ordre : 13
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0009
  - Description : Décrire les réglages GitHub à activer pour rendre les checks obligatoires et protéger la branche principale.
  - Preuve requise : Procédure GitHub actionnable.
  - Validation requise : Revue opérationnelle.
  - Livrables attendus : docs/GITHUB_RULESET_SETUP.md
  - Fichiers potentiellement impactés : docs/GITHUB_RULESET_SETUP.md

- [x] **T0014 — Fabriquer le ZIP de fondation**
  - Ordre : 14
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0003, T0009
  - Description : Permettre la construction et la publication d’une archive ZIP propre du dépôt de fondation.
  - Preuve requise : Script d’archive et workflow d’artefact fonctionnels.
  - Validation requise : Exécution locale ou GitHub Actions.
  - Livrables attendus : scripts/build_foundation_zip.py, .github/workflows/release_foundation_zip.yml
  - Fichiers potentiellement impactés : scripts/build_foundation_zip.py, .github/workflows/release_foundation_zip.yml

## 04. Modélisation métier (`P4-MODELISATION`)

- **Gate de sortie** : Taxonomie, schémas et catalogues métier approuvés.

- [ ] **T0015 — Définir la taxonomie canonique des 108 dieux**
  - Ordre : 15
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0001, T0002, T0004
  - Description : Compléter la liste des 108 dieux, leurs domaines, leurs responsabilités et leurs relations fonctionnelles.
  - Preuve requise : Registre canonique des dieux.
  - Validation requise : Revue métier + cohérence schéma.
  - Livrables attendus : project/gods_registry.yaml, docs/GODS_TAXONOMY.md
  - Fichiers potentiellement impactés : project/gods_registry.yaml, docs/GODS_TAXONOMY.md

- [ ] **T0016 — Définir les académies et leurs cursus**
  - Ordre : 16
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0015
  - Description : Établir les académies, les examens, les niveaux de maîtrise et les relations avec les dieux et les robots.
  - Preuve requise : Registre des académies et cursus.
  - Validation requise : Revue métier + schémas.
  - Livrables attendus : project/academies_registry.yaml, docs/ACADEMIES.md
  - Fichiers potentiellement impactés : project/academies_registry.yaml, docs/ACADEMIES.md

- [ ] **T0017 — Définir les classes de robots et les lignées**
  - Ordre : 17
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0015, T0016
  - Description : Décrire les classes de robots, leurs permissions, leur cycle de vie et les règles de filiation.
  - Preuve requise : Registre des classes et lignées.
  - Validation requise : Revue métier + validation d’intégrité.
  - Livrables attendus : project/robot_classes.yaml, docs/LINEAGES.md
  - Fichiers potentiellement impactés : project/robot_classes.yaml, docs/LINEAGES.md

- [ ] **T0018 — Fixer les schémas métier détaillés**
  - Ordre : 18
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0015, T0016, T0017
  - Description : Étendre les schémas de base pour couvrir dieux, académies, robots, lignées, scores, preuves et élections.
  - Preuve requise : Jeu de schémas métier versionné.
  - Validation requise : Tests de validation de schéma.
  - Livrables attendus : project/schemas/
  - Fichiers potentiellement impactés : project/schemas/

## 05. Architecture technique (`P5-ARCHITECTURE`)

- **Gate de sortie** : Noyau registre, règles, commandes et multi-index implémentés.

- [ ] **T0019 — Implémenter le registre central des entités**
  - Ordre : 19
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0018
  - Description : Créer la couche qui charge, valide, relie et expose l’ensemble des entités du système.
  - Preuve requise : Registre central exécutable.
  - Validation requise : Tests unitaires et d’intégration.
  - Livrables attendus : src/foundation_tools/entity_registry.py
  - Fichiers potentiellement impactés : src/foundation_tools/entity_registry.py, tests/

- [ ] **T0020 — Implémenter le moteur de règles**
  - Ordre : 20
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019
  - Description : Construire l’évaluateur de règles, la résolution des dépendances et la production de preuves d’exécution.
  - Preuve requise : Prototype du moteur de règles avec journal d’audit.
  - Validation requise : Tests unitaires et scénarios.
  - Livrables attendus : src/foundation_tools/rules_engine.py
  - Fichiers potentiellement impactés : src/foundation_tools/rules_engine.py, tests/

- [ ] **T0021 — Implémenter le bus de commandes slash**
  - Ordre : 21
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019
  - Description : Créer le parseur, le routeur et le contrôle des commandes slash du hub.
  - Preuve requise : Catalogue de commandes exécutable.
  - Validation requise : Tests unitaires et intégration.
  - Livrables attendus : src/foundation_tools/slash_bus.py
  - Fichiers potentiellement impactés : src/foundation_tools/slash_bus.py, tests/

- [ ] **T0022 — Implémenter le multi-index initial**
  - Ordre : 22
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0019
  - Description : Construire l’indexation par identité, phase, statut, filiation, scores et fichiers impactés.
  - Preuve requise : Reconstruction d’index reproductible.
  - Validation requise : Tests d’intégrité et performance.
  - Livrables attendus : src/foundation_tools/multi_index.py
  - Fichiers potentiellement impactés : src/foundation_tools/multi_index.py, tests/

- [ ] **T0023 — Implémenter la couche de preuves et d’audit**
  - Ordre : 23
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0019, T0020
  - Description : Journaliser les décisions, les validations, les preuves et les changements critiques.
  - Preuve requise : Registre d’audit structuré.
  - Validation requise : Tests et revue sécurité.
  - Livrables attendus : src/foundation_tools/evidence.py, templates/evidence_record_template.md
  - Fichiers potentiellement impactés : src/foundation_tools/evidence.py, templates/evidence_record_template.md, records/

## 06. Fonctionnel (`P6-FONCTIONNEL`)

- **Gate de sortie** : Scores, académies, reproduction, élection et hub minimal opérationnels.

- [ ] **T0024 — Implémenter le système de points**
  - Ordre : 24
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019, T0023
  - Description : Calculer et tracer les points attribués aux entités et aux actions selon des règles versionnées.
  - Preuve requise : Calculateur de points et tests.
  - Validation requise : Tests unitaires.
  - Livrables attendus : src/foundation_tools/score_points.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_points.py, tests/

- [ ] **T0025 — Implémenter le système de prestige**
  - Ordre : 25
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0024
  - Description : Ajouter le calcul de prestige et ses motifs d’attribution audités.
  - Preuve requise : Calculateur de prestige et barèmes versionnés.
  - Validation requise : Tests unitaires + revue métier.
  - Livrables attendus : src/foundation_tools/score_prestige.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_prestige.py, tests/

- [ ] **T0026 — Implémenter le système de crédit social**
  - Ordre : 26
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0024, T0023
  - Description : Ajouter le calcul du crédit social, les causes, les effets et les recours.
  - Preuve requise : Calculateur de crédit social et politique appliquée.
  - Validation requise : Tests + revue gouvernance.
  - Livrables attendus : src/foundation_tools/score_social.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_social.py, tests/

- [ ] **T0027 — Implémenter les workflows d’académie**
  - Ordre : 27
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0016, T0017, T0020, T0023, T0024
  - Description : Créer les parcours d’entraînement, d’examen, de classement, de promotion et de sanction.
  - Preuve requise : Workflows d’académie démontrables.
  - Validation requise : Tests d’intégration.
  - Livrables attendus : src/foundation_tools/academy_workflows.py
  - Fichiers potentiellement impactés : src/foundation_tools/academy_workflows.py, tests/

- [ ] **T0028 — Implémenter le workflow de reproduction contrôlée**
  - Ordre : 28
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0017, T0023, T0027
  - Description : Permettre la création de nouvelles lignées et robots avec contrôle des quotas et héritages.
  - Preuve requise : Workflow de reproduction avec garde-fous.
  - Validation requise : Tests d’intégration + revue sécurité.
  - Livrables attendus : src/foundation_tools/reproduction.py
  - Fichiers potentiellement impactés : src/foundation_tools/reproduction.py, tests/

- [ ] **T0029 — Implémenter le workflow d’élection du robot élu**
  - Ordre : 29
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0025, T0026, T0027, T0028
  - Description : Créer les critères, les simulations, le jury, les preuves et le couronnement du candidat.
  - Preuve requise : Workflow d’élection traçable.
  - Validation requise : Tests d’intégration + revue gouvernance.
  - Livrables attendus : src/foundation_tools/election.py
  - Fichiers potentiellement impactés : src/foundation_tools/election.py, tests/

- [ ] **T0030 — Implémenter le hub minimal**
  - Ordre : 30
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0019, T0021, T0022, T0023
  - Description : Publier une interface minimale permettant de consulter les entités, lancer des validations et suivre les preuves.
  - Preuve requise : Prototype du hub exploitable.
  - Validation requise : Revue fonctionnelle + tests d’intégration.
  - Livrables attendus : src/foundation_tools/hub.py
  - Fichiers potentiellement impactés : src/foundation_tools/hub.py, tests/

## 07. Qualité et sécurité (`P7-QUALITE`)

- **Gate de sortie** : Observabilité, sécurité et performance vérifiées.

- [ ] **T0031 — Mettre en place l’observabilité**
  - Ordre : 31
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0019, T0020, T0021, T0022, T0023
  - Description : Ajouter journaux structurés, métriques, traces de validation et tableaux de bord techniques.
  - Preuve requise : Pipeline de logs et métriques décrit et testé.
  - Validation requise : Revue exploitation.
  - Livrables attendus : docs/OBSERVABILITY.md
  - Fichiers potentiellement impactés : docs/OBSERVABILITY.md, src/

- [ ] **T0032 — Renforcer la sécurité et les approbations**
  - Ordre : 32
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0002, T0021, T0023
  - Description : Appliquer les politiques d’approbation, de sandbox, de secrets et de revue des actions sensibles.
  - Preuve requise : Contrôles de sécurité et workflows revus.
  - Validation requise : Revue sécurité.
  - Livrables attendus : docs/SECURITY_CONTROLS.md
  - Fichiers potentiellement impactés : docs/SECURITY_CONTROLS.md, .github/workflows/

- [ ] **T0033 — Préparer la montée en charge**
  - Ordre : 33
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0022, T0030, T0031
  - Description : Mesurer les coûts, reconstruire les index à échelle croissante et corriger les goulots d’étranglement.
  - Preuve requise : Rapport de performance initial.
  - Validation requise : Tests de charge.
  - Livrables attendus : docs/PERFORMANCE_PLAN.md
  - Fichiers potentiellement impactés : docs/PERFORMANCE_PLAN.md, tests/

## 08. Déploiement (`P8-DEPLOIEMENT`)

- **Gate de sortie** : Staging, sauvegardes, restauration et readiness production validés.

- [ ] **T0034 — Préparer staging, sauvegarde et restauration**
  - Ordre : 34
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0030, T0031, T0032
  - Description : Documenter et automatiser l’installation locale, le staging, les sauvegardes et les restaurations.
  - Preuve requise : Runbooks et scripts d’exploitation.
  - Validation requise : Exercice de restauration.
  - Livrables attendus : docs/OPERATIONS.md
  - Fichiers potentiellement impactés : docs/OPERATIONS.md, Makefile, scripts/

- [ ] **T0035 — Préparer la production initiale**
  - Ordre : 35
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0034, T0033
  - Description : Valider les checks finaux, les règles GitHub, le packaging et les procédures de rollback avant mise en service.
  - Preuve requise : Checklist de readiness production.
  - Validation requise : Go/no-go formel.
  - Livrables attendus : docs/PRODUCTION_READINESS.md
  - Fichiers potentiellement impactés : docs/PRODUCTION_READINESS.md, .github/workflows/

## 09. Évolutions (`P9-EVOLUTIONS`)

- **Gate de sortie** : Feuille de route, multi-hub et robot élu préparés.

- [ ] **T0036 — Documenter l’exploitation quotidienne**
  - Ordre : 36
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0034, T0035
  - Description : Rédiger les runbooks opérateur, les procédures de support et les règles de maintenance courante.
  - Preuve requise : Runbooks exploitables.
  - Validation requise : Revue exploitation.
  - Livrables attendus : docs/RUNBOOKS.md
  - Fichiers potentiellement impactés : docs/RUNBOOKS.md

- [ ] **T0037 — Ouvrir le chantier des tests avancés**
  - Ordre : 37
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0033, T0035
  - Description : Planifier les tests de charge, de sécurité, de chaos engineering et de non-régression à grande échelle.
  - Preuve requise : Plan de tests avancés versionné.
  - Validation requise : Revue QA.
  - Livrables attendus : docs/ADVANCED_QA_PLAN.md
  - Fichiers potentiellement impactés : docs/ADVANCED_QA_PLAN.md, tests/

- [ ] **T0038 — Préparer la gouvernance multi-hub**
  - Ordre : 38
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0035
  - Description : Définir comment plusieurs hubs seront gouvernés, synchronisés et audités sans casser la source de vérité.
  - Preuve requise : Charte multi-hub.
  - Validation requise : Revue architecture + gouvernance.
  - Livrables attendus : docs/MULTI_HUB_GOVERNANCE.md
  - Fichiers potentiellement impactés : docs/MULTI_HUB_GOVERNANCE.md

- [ ] **T0039 — Préparer la simulation du robot élu**
  - Ordre : 39
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0029, T0035
  - Description : Définir les scénarios de simulation, de création de hub autonome et les critères de réussite du robot élu.
  - Preuve requise : Plan de simulation du robot élu.
  - Validation requise : Revue stratégique.
  - Livrables attendus : docs/ROBOT_ELU_SIMULATION.md
  - Fichiers potentiellement impactés : docs/ROBOT_ELU_SIMULATION.md

- [ ] **T0040 — Préparer la V2 d’industrialisation**
  - Ordre : 40
  - Statut : `todo`
  - Obligatoire : `true`
  - Dépendances : T0036, T0037, T0038, T0039
  - Description : Planifier l’extension du système, l’augmentation du volume, les sous-hubs et l’automatisation supplémentaire.
  - Preuve requise : Feuille de route V2.
  - Validation requise : Revue stratégique et technique.
  - Livrables attendus : docs/V2_ROADMAP.md
  - Fichiers potentiellement impactés : docs/V2_ROADMAP.md
