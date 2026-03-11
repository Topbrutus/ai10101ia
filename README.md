# AI10101IA — fondation de dépôt contrôlée par tâches

Ce dépôt impose une logique de production stricte :

1. la **source de vérité machine** vit dans `project/todo_registry.yaml` ;
2. la **vue humaine lisible et imprimable** vit dans `docs/MASTER_TODO.md` ;
3. aucune modification sérieuse ne doit contourner les tâches, les dépendances, les preuves et les validations ;
4. les pull requests sont censées être filtrées par les workflows GitHub Actions et le template de PR.

## Objectif du dépôt

Créer une base de dépôt GitHub robuste, immédiatement exploitable, pour un projet complexe piloté par checklist maître, avec traçabilité stricte entre :

- tâche → branche → PR → validation → preuve → merge

## Principe opératoire

- **Humain** : lit `docs/MASTER_TODO.md`, suit les cases et imprime si nécessaire.
- **Machine** : valide `project/todo_registry.yaml`, reconstruit `docs/MASTER_TODO.md`, vérifie le corps des PR et bloque les contournements évidents.
- **Copilot / agents** : doivent lire `AGENTS.md`, `.github/copilot-instructions.md`, `docs/WORKFLOW_RULES.md`, `docs/MASTER_TODO.md` et `project/todo_registry.yaml` avant toute proposition.

## Commandes utiles

```bash
make install
make validate
make test
make sync-check
make sync-write
make zip
```

## Fonctionnement des validations

### Validation du registre

- `scripts/validate_todo_registry.py`
- vérifie le schéma, les champs obligatoires, l’unicité, la continuité de numérotation et les dépendances.

### Synchronisation checklist ↔ registre

- `scripts/sync_checklist.py --mode check`
- échoue si `docs/MASTER_TODO.md` diverge du registre machine.

### Contrôle des PR

- `scripts/validate_pr_body.py`
- exige des sections complètes, des références de tâches valides et une branche traçable.

### Contrôle des dépendances

- `scripts/check_dependencies.py`
- bloque une PR si une tâche citée dépend d’une tâche non terminée dans le registre.

## Structure du dépôt

Voir `docs/REPOSITORY_STRUCTURE.md`.

## Réglages GitHub à activer

Voir `docs/GITHUB_RULESET_SETUP.md`.

## Récupérer le ZIP de fondation

### En local

```bash
make zip
```

### Depuis GitHub Actions

- exécuter le workflow `release_foundation_zip`
- télécharger l’artefact `foundation-zip`

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make validate
make test
```
