## Tâches liées

- Identifiants de tâches concernés (ex: T0008, T0009) :

## Objectif

Décrire le but de la PR et le résultat attendu.

## Portée

Quelles parties du dépôt sont modifiées ? Qu’est-ce qui reste hors scope ?

## Risques

Lister les risques ou régressions possibles et les garde-fous prévus.

## Preuves

Sorties de commandes, liens vers `records/`, captures pertinentes prouvant le travail.

## Validations

- [ ] `make validate` passe sans erreur
- [ ] `make test` passe sans échec
- [ ] `make validate-domain` passe sans erreur (si applicable)
- [ ] `make sync-check` confirme la synchronisation checklist ↔ registre

## Impacts fichiers

Fichiers modifiés, en particulier les fichiers critiques s’il y en a.

## Justification des modifications critiques

Obligatoire si des fichiers critiques sont modifiés (registre, policies, workflows, template PR, etc.).

## Plan de rollback

Étapes pour revenir à l’état précédent si nécessaire.

## Déclaration et confirmations

- [ ] Je confirme avoir lu docs/MASTER_TODO.md, project/todo_registry.yaml et docs/WORKFLOW_RULES.md.
- [ ] Je confirme ne pas avoir contourné la checklist maître.
- [ ] Je confirme que les dépendances des tâches référencées sont satisfaites ou explicitement levées.
