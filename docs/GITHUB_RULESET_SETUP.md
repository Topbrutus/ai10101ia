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

## Gates de release renforcés (T0039)

### Avant tout merge sur `main`

Les status checks suivants doivent être **bloquants** :

| Check | Job | Bloquant |
|---|---|---|
| Validation du registre | `validate_todo_registry` / `validate` | Oui |
| PR gate | `pr_gate` / `gate` | Oui |
| Synchronisation checklist | `sync_checklist` / `sync` | Oui |
| Tests unitaires | `test` | Oui |

### Avant tout tag de release

1. Vérifier que tous les status checks bloquants sont verts sur la branche source.
2. Protéger les tags dans **Settings → Rules → Tags** pour empêcher les suppressions accidentelles.
3. Exiger une revue d'approbation sur la PR de release.

### Fichier CODEOWNERS recommandé

Créer `.github/CODEOWNERS` pour affecter des reviewers obligatoires aux fichiers critiques :

```
project/todo_registry.yaml    @Topbrutus
project/project_policy.yaml   @Topbrutus
docs/MASTER_TODO.md           @Topbrutus
docs/RELEASE_GATES.md         @Topbrutus
docs/GOVERNANCE.md            @Topbrutus
.github/                      @Topbrutus
```

### Vérification de la configuration

Après activation, vérifier :
- [ ] Aucun commit direct possible sur `main`
- [ ] Les status checks bloquants apparaissent dans les PR
- [ ] Les tags ne peuvent pas être supprimés sans autorisation
- [ ] CODEOWNERS est pris en compte dans les revues
