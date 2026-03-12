# Consignes Copilot — AI10101IA

## Règles essentielles

- Lire dans cet ordre : `docs/MASTER_TODO.md`, `project/todo_registry.yaml`, `docs/WORKFLOW_RULES.md`, `project/project_policy.yaml`, `docs/GOVERNANCE.md`.
- Ne jamais agir sans identifiant de tâche valide issu du registre.
- Vérifier dépendances, phase active et gates avant toute modification.
- Limiter les changements au périmètre demandé et maintenir une trace explicite.

## Fichiers sous vigilance renforcée

- `project/todo_registry.yaml`, `project/project_policy.yaml`, `docs/MASTER_TODO.md`, `docs/WORKFLOW_RULES.md`
- `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/*.yml`, `docs/RELEASE_GATES.md`, `docs/GOVERNANCE.md`
- Justifier toute modification critique dans la PR correspondante.

## Interdictions

- Pas de contournement des workflows CI ni des gates de release.
- Pas de renumérotation ou suppression de tâches obligatoires.
- Pas de modification de `docs/MASTER_TODO.md` sans `make sync-write`.

## Bonnes pratiques

- Préférer les correctifs localisés et traçables.
- Documenter preuves, validations (`make validate`, `make test`, `make validate-domain`, `make sync-check`) et plan de rollback.
- Rester en français pour les documents et messages.
