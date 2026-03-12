---
applyTo: "**"
---

# Instructions d'application des tâches — AI10101IA

## Règle fondamentale

Tout changement dans ce dépôt doit être tracé à une tâche du registre
`project/todo_registry.yaml`. Aucune modification sérieuse ne peut exister
sans identifiant de tâche valide.

## Avant de proposer un changement

1. Lire `docs/MASTER_TODO.md` pour identifier la tâche à traiter.
2. Vérifier que les dépendances de la tâche ont le statut `done` dans `project/todo_registry.yaml`.
3. Vérifier que la phase de la tâche est active ou autorisée.
4. Vérifier les gates bloquants dans `docs/RELEASE_GATES.md` si applicable.

## Vérifications obligatoires

- `make validate` doit passer avant tout merge.
- `make test` doit passer avant tout merge.
- `make validate-domain` doit passer si des assets métier sont modifiés.
- `make sync-check` doit confirmer la synchronisation de `docs/MASTER_TODO.md`.

## Modifications du registre

Si `project/todo_registry.yaml` est modifié :
- Justifier explicitement dans la PR.
- Ne jamais renuméroter les tâches.
- Ne jamais supprimer une tâche obligatoire.
- Mettre à jour `docs/MASTER_TODO.md` via `make sync-write` après modification.

## Modifications des fichiers critiques

Les fichiers suivants nécessitent une justification renforcée dans la PR :
- `project/todo_registry.yaml`
- `project/project_policy.yaml`
- `docs/MASTER_TODO.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RELEASE_GATES.md`
- `docs/GOVERNANCE.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/*.yml`

## Preuves obligatoires

Chaque PR doit inclure des preuves traçables :
- Sortie de commande de validation
- Résultat de tests
- Lien vers fichier dans `records/`
- Rapport d'audit si applicable

## Interdictions

- Ne jamais contourner les workflows CI.
- Ne jamais faire de commit direct sur `main`.
- Ne jamais modifier `docs/MASTER_TODO.md` manuellement sans `make sync-write`.
- Ne jamais démarrer une phase dont les dépendances ne sont pas satisfaites.
- Ne jamais déclarer la production active sans go/no-go formel (T0035).
