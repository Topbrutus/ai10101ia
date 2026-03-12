# Gates de release — Fondation AI10101IA

> Référence : T0039 — Durcissement final et gates de release

## Objet

Ce document définit les conditions strictes et actionnables à satisfaire avant tout tag de release,
toute livraison ZIP ou toute ouverture de la phase suivante du projet.

---

## Principes généraux

- Un **gate bloquant** doit passer à zéro avant tout merge ou release.
- Un **prérequis recommandé** améliore la qualité mais ne bloque pas le merge.
- Tout échec de gate bloquant déclenche un **gel temporaire** (voir section Gel et rollback).
- Les gates sont vérifiables localement (`make validate`) et en CI.

---

## Checklist de release de la fondation

### Gates bloquants (obligatoires avant tag ou ZIP)

- [ ] `make validate` passe sans erreur (`validate_todo_registry` + `sync_checklist`)
- [ ] `make test` passe sans échec
- [ ] `make validate-domain` passe sans erreur
- [ ] `docs/MASTER_TODO.md` est synchronisé avec `project/todo_registry.yaml`
- [ ] Toutes les tâches obligatoires T0001 à T0033 ont le statut `done`
- [ ] T0039 et T0040 ont le statut `done`
- [ ] Aucun fichier critique modifié sans trace dans une PR référencée
- [ ] Le PR template de release est rempli et signé
- [ ] Les workflows CI sont verts sur la branche principale
- [ ] Aucune violation de dépendance (`check_dependencies.py`)

### Prérequis recommandés (fortement conseillés)

- [ ] Une revue humaine du diff complet a été effectuée
- [ ] Le runbook local de restauration a été testé
- [ ] Les rulesets GitHub sont activés sur `main`
- [ ] La documentation est cohérente entre tous les fichiers `docs/`
- [ ] Le rapport d'audit a été généré et sauvegardé

---

## Politique de modification des fichiers critiques

Les fichiers suivants sont **sous protection renforcée** :

| Fichier | Niveau de protection | Justification requise |
|---|---|---|
| `project/todo_registry.yaml` | Renforcé | Source de vérité machine |
| `project/project_policy.yaml` | Renforcé | Politique du dépôt |
| `docs/MASTER_TODO.md` | Renforcé | Vue humaine synchronisée |
| `docs/WORKFLOW_RULES.md` | Renforcé | Règles de workflow |
| `.github/PULL_REQUEST_TEMPLATE.md` | Renforcé | Contrôle des PR |
| `.github/workflows/*.yml` | Renforcé | Automatisation CI |
| `docs/RELEASE_GATES.md` | Renforcé | Ce document |
| `docs/GOVERNANCE.md` | Renforcé | Gouvernance du dépôt |

**Règle** : toute modification de ces fichiers doit :
1. être justifiée dans la description de la PR ;
2. référencer la tâche concernée ;
3. être accompagnée d'une preuve de validation ;
4. passer `make validate` en CI.

---

## Politique de modification des catalogues, schémas, registre et preuves

### Catalogues de commandes et de règles

- Toute modification doit être couverte par un test de régression.
- Le numéro de version de la règle ou commande modifiée doit être incrémenté.
- La PR doit mentionner l'impact métier.

### Schémas

- Toute modification de schéma est **bloquante** jusqu'à ce que le dataset bootstrap soit validé.
- Un schéma ne peut pas être supprimé sans décision formelle enregistrée.

### Registre (`todo_registry.yaml`)

- Le registre est la source de vérité. Toute divergence avec `MASTER_TODO.md` bloque le merge.
- Les numéros de tâches ne doivent jamais être réutilisés.
- Le changement de statut d'une tâche doit être accompagné de la preuve associée.

### Preuves (`project/bootstrap_proofs.yaml`, `records/`)

- Une preuve engagée ne peut être supprimée sans décision formelle.
- Les preuves doivent rester cohérentes avec les entités du bootstrap.

---

## Politique de gel temporaire

### Conditions déclenchant un gel

- Échec de `make validate` sur la branche principale
- Divergence détectée entre `todo_registry.yaml` et `MASTER_TODO.md`
- Merge accidentel sans passage des gates bloquants
- Corruption détectée d'un fichier critique

### Procédure de gel

1. **Aucun nouveau merge** n'est autorisé sur `main` jusqu'à résolution.
2. Ouvrir une issue de type `gel-fondation` avec l'état détaillé.
3. Identifier la cause racine.
4. Appliquer le rollback si nécessaire (voir section suivante).
5. Relancer `make validate` + `make test` jusqu'à passage complet.
6. Lever le gel via PR dédiée après validation.

---

## Politique de rollback

### Rollback sur commit récent (< 24h)

```bash
git log --oneline -5       # identifier le dernier commit sain
git revert <sha_commit>    # créer un commit de revert propre
# ou
git reset --hard <sha_commit>  # uniquement si la branche n'est pas partagée
git push --force-with-lease    # ne faire qu'en cas de nécessité absolue
```

### Rollback sur fichiers critiques isolés

```bash
git checkout <sha_sain> -- project/todo_registry.yaml
git checkout <sha_sain> -- docs/MASTER_TODO.md
make validate               # vérifier que le rollback restaure l'intégrité
```

### Rollback sur release/tag

1. Rétrograder le tag dans GitHub (Settings → Releases).
2. Rétablir la branche `main` à l'état pré-release.
3. Documenter l'incident dans `records/`.
4. Relancer la procédure de release complète.

---

## Procédure de validation finale avant tag ou livraison ZIP

1. Créer une branche `release/fondation-vX.Y`.
2. Exécuter :
   ```bash
   make validate
   make test
   make validate-domain
   make audit
   ```
3. Vérifier que toutes les cases de la checklist de release ci-dessus sont cochées.
4. Ouvrir une PR de release avec le PR template rempli.
5. Faire relire par au moins un mainteneur.
6. Merger seulement si tous les gates bloquants sont verts.
7. Poser le tag (`git tag -a vX.Y -m "Release fondation vX.Y"`).
8. Générer le ZIP (`make zip`).
9. Archiver le rapport d'audit dans `records/`.

---

## Vue consolidée des prérequis avant phase suivante

Avant d'engager la **phase d'industrialisation** (post-fondation), tous les éléments suivants
doivent être satisfaits :

| Prérequis | Vérification | Bloquant |
|---|---|---|
| T0001–T0033 tous `done` | `make validate` | Oui |
| T0039–T0040 tous `done` | `make validate` | Oui |
| `make test` vert | CI | Oui |
| `make validate-domain` vert | CI | Oui |
| Aucune divergence registre/checklist | `make validate` | Oui |
| PR template renforcé en place | Présence du fichier | Oui |
| Rulesets GitHub activés sur `main` | Vérification manuelle | Recommandé |
| Rapport d'audit archivé | `records/` | Recommandé |
| Runbook de restauration testé | Exercice | Recommandé |

---

## Références croisées

- `docs/VALIDATION_POLICY.md` — politique de validation des tâches
- `docs/EVIDENCE_POLICY.md` — politique de preuve
- `docs/WORKFLOW_RULES.md` — règles de workflow
- `docs/GITHUB_RULESET_SETUP.md` — configuration des rulesets GitHub
- `docs/GOVERNANCE.md` — gouvernance et arbitrage
- `docs/INDUSTRIALIZATION_ROADMAP.md` — feuille de route post-fondation
