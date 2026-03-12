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

- [x] **T0015 — Définir la taxonomie canonique des 108 dieux**
  - Ordre : 15
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0001, T0002, T0004
  - Description : Compléter la liste des 108 dieux, leurs domaines, leurs responsabilités et leurs relations fonctionnelles.
  - Preuve requise : Registre canonique des dieux.
  - Validation requise : Revue métier + cohérence schéma.
  - Livrables attendus : project/gods_registry.yaml, docs/GODS_TAXONOMY.md
  - Fichiers potentiellement impactés : project/gods_registry.yaml, docs/GODS_TAXONOMY.md

- [x] **T0016 — Définir les académies et leurs cursus**
  - Ordre : 16
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0015
  - Description : Établir les académies, les examens, les niveaux de maîtrise et les relations avec les dieux et les robots.
  - Preuve requise : Registre des académies et cursus.
  - Validation requise : Revue métier + schémas.
  - Livrables attendus : project/academies_registry.yaml, docs/ACADEMIES.md
  - Fichiers potentiellement impactés : project/academies_registry.yaml, docs/ACADEMIES.md

- [x] **T0017 — Définir les classes de robots et les lignées**
  - Ordre : 17
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0015, T0016
  - Description : Décrire les classes de robots, leurs permissions, leur cycle de vie et les règles de filiation.
  - Preuve requise : Registre des classes et lignées.
  - Validation requise : Revue métier + validation d’intégrité.
  - Livrables attendus : project/robot_classes.yaml, docs/LINEAGES.md
  - Fichiers potentiellement impactés : project/robot_classes.yaml, docs/LINEAGES.md

- [x] **T0018 — Fixer les schémas métier détaillés**
  - Ordre : 18
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0015, T0016, T0017
  - Description : Étendre les schémas de base pour couvrir dieux, académies, robots, lignées, scores, preuves et élections.
  - Preuve requise : Jeu de schémas métier versionné.
  - Validation requise : Tests de validation de schéma.
  - Livrables attendus : project/schemas/
  - Fichiers potentiellement impactés : project/schemas/

## 05. Architecture technique (`P5-ARCHITECTURE`)

- **Gate de sortie** : Noyau registre, règles, commandes et multi-index implémentés.

- [x] **T0019 — Implémenter le registre central des entités**
  - Ordre : 19
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0018
  - Description : Créer la couche qui charge, valide, relie et expose l’ensemble des entités du système.
  - Preuve requise : Contrat documentaire du registre central validé.
  - Validation requise : Revue documentaire et cohérence inter-documents.
  - Livrables attendus : docs/CENTRAL_REGISTRY.md
  - Fichiers potentiellement impactés : docs/CENTRAL_REGISTRY.md

- [x] **T0020 — Implémenter le moteur de règles**
  - Ordre : 20
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019
  - Description : Construire l’évaluateur de règles, la résolution des dépendances et la production de preuves d’exécution.
  - Preuve requise : Contrat documentaire du moteur de règles validé.
  - Validation requise : Revue documentaire et cohérence inter-documents.
  - Livrables attendus : docs/RULE_ENGINE_CONTRACT.md
  - Fichiers potentiellement impactés : docs/RULE_ENGINE_CONTRACT.md

- [x] **T0021 — Implémenter le bus de commandes slash**
  - Ordre : 21
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019
  - Description : Créer le parseur, le routeur et le contrôle des commandes slash du hub.
  - Preuve requise : Contrat documentaire du bus slash validé.
  - Validation requise : Revue documentaire et cohérence inter-documents.
  - Livrables attendus : docs/SLASH_BUS_CONTRACT.md
  - Fichiers potentiellement impactés : docs/SLASH_BUS_CONTRACT.md

- [x] **T0022 — Implémenter le multi-index initial**
  - Ordre : 22
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0019
  - Description : Construire l’indexation par identité, phase, statut, filiation, scores et fichiers impactés.
  - Preuve requise : Contrat documentaire du multi-index validé.
  - Validation requise : Revue documentaire et cohérence inter-documents.
  - Livrables attendus : docs/MULTI_INDEX.md
  - Fichiers potentiellement impactés : docs/MULTI_INDEX.md

- [x] **T0023 — Implémenter la couche de preuves et d’audit**
  - Ordre : 23
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0019, T0020
  - Description : Journaliser les décisions, les validations, les preuves et les changements critiques.
  - Preuve requise : Modèle documentaire de preuve et d’audit validé.
  - Validation requise : Revue documentaire et cohérence inter-documents.
  - Livrables attendus : docs/AUDIT_MODEL.md, templates/evidence_record_template.md
  - Fichiers potentiellement impactés : docs/AUDIT_MODEL.md, templates/evidence_record_template.md

- [x] **T0029 — Créer le dataset bootstrap canonique**
  - Ordre : 29
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0019, T0020, T0021, T0022, T0023
  - Description : Construire un jeu pilote cohérent et versionné (hub, dieux, académies, robots, lignées, scores, preuves, événements) permettant de charger et tester le système sans données manuelles.
  - Preuve requise : Fichiers bootstrap YAML valides et cohérents avec les schémas et le registre central.
  - Validation requise : Tests de chargement et de cohérence des entités bootstrap.
  - Livrables attendus : project/bootstrap_entities.yaml, project/bootstrap_proofs.yaml, project/bootstrap_events.yaml, docs/PILOT_DATASET.md
  - Fichiers potentiellement impactés : project/bootstrap_entities.yaml, project/bootstrap_proofs.yaml, project/bootstrap_events.yaml, docs/PILOT_DATASET.md, tests/

- [x] **T0030 — Construire le pipeline de validation métier**
  - Ordre : 30
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0029
  - Description : Fournir un script de validation complet du domaine AI10101IA : schémas métier, relations inter-entités, références commandes/règles/preuves, cohérence scores, messages d'erreur lisibles.
  - Preuve requise : Script de validation exécutable sur les datasets bootstrap avec code de retour correct.
  - Validation requise : Tests unitaires et d'intégration sur la validation métier.
  - Livrables attendus : scripts/validate_domain_assets.py, docs/VALIDATION_POLICY.md, docs/CLI_USAGE.md
  - Fichiers potentiellement impactés : scripts/validate_domain_assets.py, docs/VALIDATION_POLICY.md, docs/CLI_USAGE.md, Makefile, tests/

- [x] **T0031 — Créer les commandes locales / CLI de pilotage**
  - Ordre : 31
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0029, T0030
  - Description : Fournir une couche CLI minimale pour charger le dataset bootstrap, valider le domaine, afficher/lister des entités, reconstruire le multi-index pilote et exporter une vue d'audit.
  - Preuve requise : CLI exécutable localement avec commandes stables et sortie lisible.
  - Validation requise : Tests des commandes CLI sur le dataset bootstrap.
  - Livrables attendus : scripts/run_registry_cli.py, docs/CLI_USAGE.md
  - Fichiers potentiellement impactés : scripts/run_registry_cli.py, src/foundation_tools/registry_tools.py, docs/CLI_USAGE.md, Makefile, tests/

- [x] **T0032 — Construire les vues d'audit lisibles**
  - Ordre : 32
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0029, T0030
  - Description : Générer des sorties structurées lisibles pour audit humain : vue synthétique du registre bootstrap, relations de filiation, preuves par entité, incohérences détectées, synthèse exportable.
  - Preuve requise : Script de rapport d'audit générant un fichier Markdown ou JSON exploitable.
  - Validation requise : Tests de génération et de contenu du rapport d'audit.
  - Livrables attendus : scripts/build_audit_report.py, docs/AUDIT_READ_MODELS.md
  - Fichiers potentiellement impactés : scripts/build_audit_report.py, docs/AUDIT_READ_MODELS.md, tests/

- [x] **T0033 — Assembler le flux bout-en-bout pilote**
  - Ordre : 33
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0029, T0030, T0031, T0032
  - Description : Démontrer un flux complet et traçable sur le jeu bootstrap : chargement, validation, consultation d'entités, rattachement de preuves, reconstruction du multi-index, génération d'audit, vérification de cohérence.
  - Preuve requise : Flux pilote rejouable avec tests automatisés et documentation claire.
  - Validation requise : Tests bout-en-bout sur le flux pilote complet.
  - Livrables attendus : docs/PILOT_FLOW.md, scripts/run_pilot_flow.py
  - Fichiers potentiellement impactés : docs/PILOT_FLOW.md, scripts/run_pilot_flow.py, Makefile, tests/

## 06. Fonctionnel (`P6-FONCTIONNEL`)

- **Gate de sortie** : Scores, académies, reproduction, élection et hub minimal opérationnels.

- [x] **T0024 — Implémenter le système de points**
  - Ordre : 24
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0018, T0019, T0023
  - Description : Calculer et tracer les points attribués aux entités et aux actions selon des règles versionnées.
  - Preuve requise : Calculateur de points et tests.
  - Validation requise : Tests unitaires.
  - Livrables attendus : src/foundation_tools/score_points.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_points.py, tests/

- [x] **T0025 — Implémenter le système de prestige**
  - Ordre : 25
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0024
  - Description : Ajouter le calcul de prestige et ses motifs d’attribution audités.
  - Preuve requise : Calculateur de prestige et barèmes versionnés.
  - Validation requise : Tests unitaires + revue métier.
  - Livrables attendus : src/foundation_tools/score_prestige.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_prestige.py, tests/

- [x] **T0026 — Implémenter le système de crédit social**
  - Ordre : 26
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0024, T0023
  - Description : Ajouter le calcul du crédit social, les causes, les effets et les recours.
  - Preuve requise : Calculateur de crédit social et politique appliquée.
  - Validation requise : Tests + revue gouvernance.
  - Livrables attendus : src/foundation_tools/score_social.py
  - Fichiers potentiellement impactés : src/foundation_tools/score_social.py, tests/

- [x] **T0027 — Implémenter les workflows d’académie**
  - Ordre : 27
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0016, T0017, T0020, T0023, T0024
  - Description : Créer les parcours d’entraînement, d’examen, de classement, de promotion et de sanction.
  - Preuve requise : Workflows d’académie démontrables.
  - Validation requise : Tests d’intégration.
  - Livrables attendus : src/foundation_tools/academy_workflows.py
  - Fichiers potentiellement impactés : src/foundation_tools/academy_workflows.py, tests/

- [x] **T0028 — Implémenter le workflow de reproduction contrôlée**
  - Ordre : 28
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0017, T0023, T0027
  - Description : Permettre la création de nouvelles lignées et robots avec contrôle des quotas et héritages.
  - Preuve requise : Workflow de reproduction avec garde-fous.
  - Validation requise : Tests d’intégration + revue sécurité.
  - Livrables attendus : src/foundation_tools/reproduction.py
  - Fichiers potentiellement impactés : src/foundation_tools/reproduction.py, tests/

## 07. Qualité et sécurité (`P7-QUALITE`)

- **Gate de sortie** : Observabilité, sécurité et performance vérifiées.

- [ ] Aucune tâche définie pour cette phase.

## 08. Déploiement (`P8-DEPLOIEMENT`)

- **Gate de sortie** : Staging, sauvegardes, restauration et readiness production validés.

- [x] **T0034 — Préparer staging, sauvegarde et restauration**
  - Ordre : 34
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0030, T0031, T0032
  - Description : Documenter et automatiser l’installation locale, le staging, les sauvegardes et les restaurations.
  - Preuve requise : Runbooks et scripts d’exploitation.
  - Validation requise : Exercice de restauration.
  - Livrables attendus : docs/OPERATIONS.md, scripts/backup_local_state.py, scripts/restore_local_state.py, tests/test_backup_restore.py
  - Fichiers potentiellement impactés : docs/OPERATIONS.md, Makefile, scripts/backup_local_state.py, scripts/restore_local_state.py, tests/test_backup_restore.py

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

- [x] **T0039 — Durcissement final et gates de release**
  - Ordre : 39
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0033
  - Description : Renforcer la fondation pour empêcher les contournements avant la suite du projet. Définir les gates de release, la politique de gel, de rollback et la procédure de validation finale avant tag ou livraison ZIP.
  - Preuve requise : docs/RELEASE_GATES.md créé, docs/WORKFLOW_RULES.md renforcé, docs/VALIDATION_POLICY.md et docs/EVIDENCE_POLICY.md mis à jour, .github/PULL_REQUEST_TEMPLATE.md et instructions agents créés.
  - Validation requise : make validate + make test verts.
  - Livrables attendus : docs/RELEASE_GATES.md, docs/VALIDATION_POLICY.md, docs/EVIDENCE_POLICY.md, docs/GITHUB_RULESET_SETUP.md, docs/WORKFLOW_RULES.md, .github/PULL_REQUEST_TEMPLATE.md, .github/instructions/task-enforcement.instructions.md, .github/instructions/repository-guard.instructions.md
  - Fichiers potentiellement impactés : docs/RELEASE_GATES.md, docs/VALIDATION_POLICY.md, docs/EVIDENCE_POLICY.md, docs/GITHUB_RULESET_SETUP.md, docs/WORKFLOW_RULES.md, .github/PULL_REQUEST_TEMPLATE.md, .github/instructions/task-enforcement.instructions.md, .github/instructions/repository-guard.instructions.md

- [x] **T0040 — Préparation de la suite industrielle**
  - Ordre : 40
  - Statut : `done`
  - Obligatoire : `true`
  - Dépendances : T0039
  - Description : Préparer proprement la transition entre la fondation et la phase d’industrialisation du projet AI10101IA. Documenter la feuille de route, les blocs logiques suivants, les prérequis, les limites et les dettes assumées.
  - Preuve requise : docs/INDUSTRIALIZATION_ROADMAP.md créé, docs/NEXT_PHASE_ARCHITECTURE.md créé, docs/PROJECT_PHASES.md et docs/GOVERNANCE.md mis à jour.
  - Validation requise : make validate + make test verts.
  - Livrables attendus : docs/INDUSTRIALIZATION_ROADMAP.md, docs/NEXT_PHASE_ARCHITECTURE.md, docs/PROJECT_PHASES.md, docs/GOVERNANCE.md, docs/REPOSITORY_STRUCTURE.md, README.md
  - Fichiers potentiellement impactés : docs/INDUSTRIALIZATION_ROADMAP.md, docs/NEXT_PHASE_ARCHITECTURE.md, docs/PROJECT_PHASES.md, docs/GOVERNANCE.md, docs/REPOSITORY_STRUCTURE.md, README.md
