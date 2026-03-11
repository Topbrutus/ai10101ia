# Mise en place des rulesets GitHub

## Objectif

Rendre les contrôles du dépôt réellement obligatoires côté GitHub.

## Réglages recommandés

### Branch protection sur `main`

Activer :

- Require a pull request before merging
- Require approvals
- Dismiss stale reviews when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict direct pushes
- Do not allow bypassing the above settings

### Status checks à rendre obligatoires

- workflow `validate_todo_registry` / job `validate`
- workflow `pr_gate` / job `gate`
- workflow `sync_checklist` / job `sync`
- tout job complémentaire de tests que vous rendez bloquant

### Recommandations supplémentaires

- activer CODEOWNERS
- activer conversation resolution before merge
- protéger les tags de release si vous en utilisez
- restreindre l’écriture sur les chemins critiques si votre plan GitHub le permet

## Procédure

1. ouvrir **Settings → Rules / Branches**
2. créer ou éditer la protection de `main`
3. cocher les options ci-dessus
4. sélectionner les status checks obligatoires après le premier passage réussi des workflows
5. enregistrer
