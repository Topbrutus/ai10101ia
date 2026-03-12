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

## Répertoires réservés pour la phase d'industrialisation

Les répertoires suivants sont réservés pour la phase suivante.
Ils ne doivent pas être créés avant que les prérequis soient satisfaits.

### `/records`

Archivage des preuves formelles, décisions, rapports d'audit de release.
À créer lors de la première release officielle (T0035).

### `/staging`

Configuration et scripts spécifiques à l'environnement staging.
À créer lors du déploiement staging (T0034).

## Règles de placement pour la phase d'industrialisation

- Tout nouveau module applicatif va dans `/src/foundation_tools/`.
- Tout nouveau script opérationnel va dans `/scripts/`.
- Toute nouvelle documentation va dans `/docs/`.
- Les runbooks opérateur volumineux peuvent aller dans `/docs/runbooks/` si nécessaire.
- Aucun répertoire nouveau à la racine sans décision formelle.
