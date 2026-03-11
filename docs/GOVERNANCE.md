# Gouvernance

## But

Empêcher la dérive du dépôt, protéger les tâches obligatoires et rendre les changements traçables.

## Rôles

### Mainteneur principal

- valide les modifications critiques
- arbitre les conflits de priorités
- approuve les changements de règles et de politiques

### Contributeur

- travaille uniquement via branche et PR
- respecte la checklist maître
- documente preuves, validations et rollback

### Agent IA / Copilot

- lit la documentation obligatoire avant de proposer
- ne contourne jamais l’ordre des tâches
- ne modifie pas les fichiers critiques sans justification

## Qui peut changer quoi

### Peut être modifié par PR ordinaire

- code applicatif non critique
- documentation non critique
- tests liés à une tâche valide

### Nécessite justification renforcée

- `project/todo_registry.yaml`
- `project/project_policy.yaml`
- `docs/MASTER_TODO.md`
- `docs/WORKFLOW_RULES.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/*.yml`

### Nécessite arbitrage explicite

- suppression d’une tâche obligatoire
- réordonnancement des tâches
- changement du système de numérotation
- changement des phases
- changement des règles de merge ou de sécurité

## Différences entre types de changement

### Ajout

Créer une nouvelle tâche sans casser l’ordre logique ni renuméroter arbitrairement le registre existant.

### Correction

Corriger une erreur factuelle, de formulation ou de dépendance tout en documentant la raison.

### Suppression

Interdite pour les tâches obligatoires sans décision formelle enregistrée.

### Replanification

Autorisée seulement si les impacts sur les dépendances sont explicitement documentés.

## Décision formelle requise

Une décision formelle doit exister si l’on touche à l’ordre, au caractère obligatoire ou à la politique du dépôt.
