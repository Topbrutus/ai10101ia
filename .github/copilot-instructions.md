# Instructions Copilot — AI10101IA

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

## Interdictions absolues

- Ne jamais contourner les workflows CI.
- Ne jamais faire de commit direct sur `main`.
- Ne jamais modifier `docs/MASTER_TODO.md` manuellement sans `make sync-write`.
- Ne jamais démarrer une phase dont les dépendances ne sont pas satisfaites.
- Ne jamais déclarer la production active ou le robot élu implémenté sans preuve (T0035).
- Ne jamais renuméroter les tâches du registre.
- Ne jamais supprimer une tâche obligatoire.

## Comportement attendu

- Proposer de petites PR cohérentes.
- Citer les fichiers touchés.
- Décrire les risques.
- Documenter le rollback.
- Préférer le correctif localisé à la refonte opportuniste.
- Référencer l'identifiant de tâche dans chaque PR.
