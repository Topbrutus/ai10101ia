# Feuille de route d'industrialisation — AI10101IA

> Référence : T0040 — Préparation de la suite industrielle

## Objet

Ce document décrit la feuille de route structurée de la phase d'industrialisation
qui suit la fondation. Il ne démarre pas cette phase — il la prépare proprement.

---

## État de la fondation à la clôture

### Ce qui est terminé (T0001–T0040)

- Structure du dépôt, gouvernance, registre machine et checklist humaine
- Contrôles GitHub : PR gate, workflows CI, instructions agents
- Modélisation métier : taxonomie, schémas, catalogues commandes/règles
- Architecture technique : noyau registre, règles, commandes, multi-index
- Fonctionnel pilote : dataset bootstrap, validation métier, CLI, audit, flux pilote
- Hub minimal, vues opérateur, observabilité de base
- Packaging/staging local
- Durcissement final : gates de release, politiques de gel et rollback
- Préparation de la suite : ce document et les documents associés

### Ce qui n'est PAS encore fait

- Déploiement en production → interdit dans cette phase
- Reproduction réelle activée → dépend de T0034+
- Élection réelle du robot élu → dépend de plusieurs prérequis industriels
- Hub final complet → phase suivante
- Multi-hub → phase ultérieure
- Tests avancés à grande échelle → phase ultérieure

---

## Blocs logiques de la phase d'industrialisation

### Bloc I1 — Staging, sauvegarde et restauration (T0034)

**Objectif** : rendre le système exploitable dans un environnement staging réel.

**Prérequis** :
- Fondation complète (T0001–T0033, T0039–T0040)
- `make validate` + `make test` + `make validate-domain` verts

**Livrables attendus** :
- `docs/OPERATIONS.md` : runbooks d'installation, staging, sauvegarde, restauration
- Scripts d'automatisation de sauvegarde/restauration
- Exercice de restauration documenté

**Gate de sortie** : exercice de restauration exécuté et validé.

---

### Bloc I2 — Readiness production initiale (T0035)

**Objectif** : valider les checks finaux avant toute mise en service.

**Prérequis** :
- Bloc I1 complet
- Rulesets GitHub activés
- Rapport d'audit archivé
- Runbook de restauration testé

**Livrables attendus** :
- `docs/PRODUCTION_READINESS.md` : checklist go/no-go production
- Workflows CI renforcés
- Go/no-go formel documenté

**Gate de sortie** : go/no-go formel validé par mainteneur principal.

---

### Bloc I3 — Exploitation quotidienne (T0036)

**Objectif** : permettre la maintenance et le support courant.

**Prérequis** : Bloc I2 complet.

**Livrables attendus** :
- `docs/RUNBOOKS.md` : procédures opérateur, support, maintenance courante
- Procédures d'escalade documentées

**Gate de sortie** : runbooks relus et validés par un opérateur.

---

### Bloc I4 — Tests avancés (T0037)

**Objectif** : valider la robustesse et la sécurité à grande échelle.

**Prérequis** : Blocs I2 et I1 complets.

**Livrables attendus** :
- `docs/ADVANCED_QA_PLAN.md` : plan de tests de charge, sécurité, chaos, non-régression

**Gate de sortie** : plan de tests approuvé en revue QA.

---

### Bloc I5 — Gouvernance multi-hub (T0038)

**Objectif** : préparer l'extension à plusieurs hubs gouvernés.

**Prérequis** : Bloc I2 complet.

**Livrables attendus** :
- `docs/MULTI_HUB_GOVERNANCE.md` : charte multi-hub, synchronisation, audit

**Gate de sortie** : charte relue en revue architecture et gouvernance.

---

## Prérequis avant montée en charge

| Prérequis | Détail | Gate |
|---|---|---|
| Staging fonctionnel | T0034 complet | Bloquant |
| Sauvegarde/restauration testée | Exercice réel | Bloquant |
| CI verte sur staging | Tous workflows | Bloquant |
| Documentation exploitant disponible | T0036 complet | Bloquant |
| Plan de tests avancés approuvé | T0037 complet | Bloquant |

---

## Prérequis avant hub étendu

| Prérequis | Détail |
|---|---|
| Bloc I1 complet | T0034 |
| Bloc I2 complet | T0035 |
| Charte multi-hub disponible | T0038 |
| Architecture hub étendu documentée | Nouveau bloc à définir |
| Tests d'intégration multi-hub | Nouveau bloc à définir |

---

## Prérequis avant académies exécutables complètes

| Prérequis | Détail |
|---|---|
| Dataset bootstrap validé | T0029 (done) |
| Workflows d'académie pilote validés | T0027 (done) |
| Staging fonctionnel | T0034 |
| Tests de charge académies | T0037 |
| Documentation académie complète | Nouveau bloc à définir |

---

## Prérequis avant reproduction réelle

| Prérequis | Détail |
|---|---|
| Workflow reproduction pilote validé | T0028 (done) |
| Staging fonctionnel | T0034 |
| Go/no-go production | T0035 |
| Quotas et garde-fous validés sous charge | T0037 |
| Audit de reproduction documenté | Records disponibles |

---

## Prérequis avant élection réelle du robot élu

| Prérequis | Détail |
|---|---|
| Reproduction réelle activée | T0028 + T0034 + T0035 |
| Crédit social validé sous charge | T0026 + T0037 |
| Critères d'élection formalisés | Nouveau bloc à définir |
| Plan de simulation validé | Nouveau bloc à définir |
| Gouvernance du robot élu documentée | Nouveau bloc à définir |

---

## Limites actuelles de la fondation

- La fondation est locale : aucun déploiement cloud ou serveur actif.
- La reproduction et l'élection sont simulées sur dataset bootstrap.
- Le hub est minimal : un seul hub pilote.
- Le volume de données est celui du bootstrap : non représentatif de la production.
- Les tests avancés (charge, sécurité, chaos) ne sont pas encore exécutés.
- L'automatisation CI couvre la fondation mais pas l'industrialisation.

---

## Dettes assumées et contrôlées

| Dette | Justification | Résolution prévue |
|---|---|---|
| Pas de déploiement cloud | Fondation locale délibérée | T0035 |
| Tests de charge absents | Hors périmètre fondation | T0037 |
| Runbooks opérateur absents | Hors périmètre fondation | T0036 |
| Multi-hub non gouverné | Trop tôt | T0038 |
| Robot élu non implémenté | Trop tôt | Nouveau bloc post-T0038 |
| Académies partiellement exécutables | Pilote suffisant | Nouveau bloc |

---

## Points à surveiller pour l'industrialisation

1. **Dérive du registre** : surveiller toute divergence entre `todo_registry.yaml` et `MASTER_TODO.md`.
2. **Explosion du volume** : les schémas et validations doivent être testés sous charge avant production.
3. **Gouvernance multi-contributeurs** : les rulesets GitHub doivent être activés avant l'élargissement.
4. **Sécurité des preuves** : les preuves engagées ne doivent pas être altérées rétroactivement.
5. **Compatibilité des schémas** : toute évolution de schéma doit être rétrocompatible ou versionnée.
6. **Traçabilité des reproductions** : chaque reproduction réelle doit générer une preuve archivée.

---

## Références croisées

- `docs/RELEASE_GATES.md` — gates de release et conditions de passage
- `docs/NEXT_PHASE_ARCHITECTURE.md` — architecture cible de la phase suivante
- `docs/PROJECT_PHASES.md` — phases officielles du projet
- `docs/GOVERNANCE.md` — gouvernance et arbitrage
- `project/todo_registry.yaml` — registre machine des tâches
