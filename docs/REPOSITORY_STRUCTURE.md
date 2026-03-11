# Structure du dépôt

## Règle générale

Chaque dossier existe pour une contrainte réelle. Aucun vrac à la racine.

## Dossiers

### `/docs`

Documentation versionnée, lisible par humains, imprimable et exploitable en revue.

### `/project`

Source de vérité machine et politiques de dépôt.

### `/.github`

Contrôles GitHub, templates, instructions Copilot et workflows d’automatisation.

### `/scripts`

Scripts opérationnels appelés localement ou par GitHub Actions.

### `/templates`

Gabarits de preuves, décisions et enregistrements normalisés.

### `/records`

Traces déposées volontairement, conservées avec historique Git.

### `/src`

Code Python du noyau outillage.

### `/tests`

Tests unitaires et de non-régression pour les scripts critiques.

## Interdictions

- ne pas déposer des documents critiques hors de `docs/`
- ne pas déposer des fichiers machine hors de `project/`
- ne pas déposer des scripts opératoires hors de `scripts/`
- ne pas créer de nouveaux dossiers racine sans justification documentée
