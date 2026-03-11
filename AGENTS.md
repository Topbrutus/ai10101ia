# Règles d’or pour tous les agents

## Lecture avant action

Toujours lire, dans cet ordre :

1. `docs/MASTER_TODO.md`
2. `project/todo_registry.yaml`
3. `docs/WORKFLOW_RULES.md`
4. `project/project_policy.yaml`
5. `docs/GOVERNANCE.md`

## Règles absolues

- ne pas agir sans identifiant de tâche
- respecter l’ordre des phases et des dépendances
- signaler immédiatement toute dépendance manquante
- produire des modifications minimales, traçables et justifiées
- ne jamais sortir du périmètre demandé
- toujours laisser une piste de preuve
- ne jamais renuméroter le registre sans décision formelle
- ne jamais supprimer une tâche obligatoire sans arbitrage versionné
- ne jamais réécrire manuellement la checklist maître sans la régénérer depuis le registre machine

## Comportement attendu

- proposer de petites PR cohérentes
- citer les fichiers touchés
- décrire les risques
- documenter le rollback
- préférer le correctif localisé à la refonte opportuniste

## Fichiers critiques

Les fichiers suivants demandent une vigilance renforcée :

- `project/todo_registry.yaml`
- `project/project_policy.yaml`
- `docs/MASTER_TODO.md`
- `docs/WORKFLOW_RULES.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/*.yml`
