---
applyTo: "**"
---

# Garde-fous du dépôt — AI10101IA

## Objet

Ces instructions définissent les garde-fous que tout agent ou contributeur
doit respecter pour ne pas casser la fondation du dépôt.

## Fichiers protégés

Les fichiers suivants ne doivent jamais être modifiés sans justification
explicite dans une PR référencée :

- `project/todo_registry.yaml` — source de vérité machine
- `project/project_policy.yaml` — politique du dépôt
- `docs/MASTER_TODO.md` — vue humaine synchronisée (ne modifier qu'avec `make sync-write`)
- `docs/RELEASE_GATES.md` — gates de release
- `docs/WORKFLOW_RULES.md` — règles de workflow
- `docs/GOVERNANCE.md` — gouvernance
- `.github/PULL_REQUEST_TEMPLATE.md` — template de PR
- `.github/workflows/*.yml` — workflows CI

## Invariants à préserver

1. `project/todo_registry.yaml` et `docs/MASTER_TODO.md` doivent toujours être synchronisés.
2. Les numéros de tâches ne sont jamais réutilisés.
3. Les dépendances entre tâches doivent toujours être cohérentes.
4. Aucun statut `done` ne peut être régressé sans décision formelle.
5. `make validate` doit toujours passer sur la branche principale.

## Situations de gel

Si l'un des invariants ci-dessus est violé :
1. Stopper tout merge supplémentaire sur `main`.
2. Ouvrir une issue avec le label `gel-fondation`.
3. Identifier la cause et appliquer le rollback décrit dans `docs/RELEASE_GATES.md`.
4. Relancer `make validate` + `make test` jusqu'à passage complet.
5. Lever le gel via PR dédiée.

## Ce qu'un agent IA ne doit jamais faire

- Modifier `docs/MASTER_TODO.md` sans exécuter `make sync-write`.
- Renuméroter les tâches du registre.
- Supprimer une tâche obligatoire.
- Engager un commit direct sur `main`.
- Déclarer la production active ou le robot élu implémenté sans preuve.
- Contourner les workflows CI ou les gates bloquants.
- Ouvrir une phase future comme si elle était terminée.

## Ce qu'un agent IA doit toujours faire

- Lire `docs/MASTER_TODO.md`, `docs/WORKFLOW_RULES.md` et `project/todo_registry.yaml` avant de proposer.
- Vérifier les dépendances avant de traiter une tâche.
- Produire des modifications minimales, traçables et justifiées.
- Référencer l'identifiant de tâche dans chaque PR.
- Laisser une piste de preuve dans chaque PR.
- Respecter la langue française pour tous les documents.
