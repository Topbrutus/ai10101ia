# Contribution

## Règle générale

Aucune contribution ne doit commencer sans référence explicite à une ou plusieurs tâches du registre.

## Ordre de travail obligatoire

1. Lire `docs/MASTER_TODO.md`.
2. Lire `project/todo_registry.yaml`.
3. Lire `docs/WORKFLOW_RULES.md`.
4. Vérifier les dépendances de la tâche ciblée.
5. Créer une branche conforme.
6. Effectuer des modifications minimales et traçables.
7. Fournir preuves, validations et plan de rollback dans la PR.

## Nommage des branches

- tâche unique : `task/T0001-slug`
- lot exceptionnel validé : `batch/T0001-T0002-slug`
- maintenance transverse : `maintenance/slug`

## Règles de pull request

- toujours citer les identifiants de tâches `Txxxx`
- ne jamais modifier `project/todo_registry.yaml` sans justification explicite
- ne jamais modifier `docs/MASTER_TODO.md` manuellement sans repasser par `scripts/sync_checklist.py --mode write`
- ne jamais supprimer une tâche obligatoire sans arbitrage formel documenté
- ne jamais fusionner plusieurs tâches dans une seule sans justification claire

## Preuves obligatoires

Les preuves doivent être décrites dans la PR et, si nécessaire, déposées sous `records/` à l’aide des gabarits de `templates/`.

## Validations obligatoires avant PR

```bash
make validate
make test
```

## Quand une tâche change de statut

- la justification doit apparaître dans la PR
- le registre doit être mis à jour proprement
- la checklist doit être régénérée
- le changement doit être relu
