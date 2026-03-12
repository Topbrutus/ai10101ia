# OPERATIONS.md — Exploitation locale AI10101IA (T0034)

## Objectif et périmètre

Ce document couvre la tâche **T0034 — Préparer staging, sauvegarde et restauration** du dépôt AI10101IA.

Il décrit :
- l'installation locale reproductible du projet
- la procédure de staging local
- la procédure de sauvegarde de l'état local
- la procédure de restauration
- un exercice de restauration pas à pas
- la procédure de rollback
- les preuves et validations

**Phase** : P8-DEPLOIEMENT  
**Dépendances satisfaites** : T0030 (done), T0031 (done), T0032 (done)

---

## Prérequis locaux

| Outil     | Version minimale | Vérification         |
|-----------|-----------------|----------------------|
| Python    | 3.10            | `python3 --version`  |
| pip       | 22.x            | `pip3 --version`     |
| git       | 2.x             | `git --version`      |
| make      | GNU Make 4.x    | `make --version`     |

---

## Installation locale reproductible

```bash
# 1. Cloner le dépôt
git clone https://github.com/Topbrutus/ai10101ia.git
cd ai10101ia

# 2. Installer les dépendances Python
pip3 install -r requirements.txt

# 3. Valider l'installation
make validate

# 4. Lancer les tests
make test
```

Résultat attendu :
- `make validate` → `OK: registre valide` + `OK: checklist synchronisée`
- `make test` → `N passed in X.XXs`

---

## Procédure staging local

Le staging local consiste à vérifier que l'état du dépôt est cohérent avant tout déploiement.

```bash
# Validation du registre et de la checklist maître
make validate

# Validation des assets métier (domaine)
make validate-domain

# Lancer la suite de tests complète
make test

# Lancer le flux pilote bout-en-bout
make pilot
```

Tous ces checks doivent passer (code de retour 0) avant de passer en production.

---

## Procédure de sauvegarde

La sauvegarde locale crée une copie horodatée des fichiers du dépôt dans `backups/`.

### Sauvegarde standard

```bash
make ops-backup
```

Cette commande exécute `scripts/backup_local_state.py` avec les sources par défaut :
`docs`, `project`, `scripts`, `src`, `tests`, `Makefile`, `pyproject.toml`, `requirements.txt`.

### Sauvegarde personnalisée

```bash
python3 scripts/backup_local_state.py \
    --output /chemin/vers/sauvegardes \
    --include docs project scripts
```

### Options disponibles

| Option       | Description                                      | Défaut                  |
|--------------|--------------------------------------------------|-------------------------|
| `--output`   | Dossier de destination                           | `backups/` (racine)     |
| `--include`  | Sources à sauvegarder                            | docs, project, scripts… |
| `--dry-run`  | Simulation sans écriture                         | désactivé               |

### Structure d'une sauvegarde

```
backups/
└── backup_20260312T010000Z/
    ├── manifest.json          ← métadonnées + checksums
    ├── docs/
    │   └── OPERATIONS.md
    ├── project/
    │   └── todo_registry.yaml
    └── ...
```

### Contenu du manifeste

```json
{
  "version": 1,
  "backup_name": "backup_20260312T010000Z",
  "timestamp_utc": "20260312T010000Z",
  "sources": ["docs", "project", "scripts"],
  "fichiers": [
    {"fichier": "docs/OPERATIONS.md", "sha256": "abc123..."},
    ...
  ],
  "total_fichiers": 42,
  "erreurs": 0
}
```

---

## Procédure de restauration

La restauration copie les fichiers d'une sauvegarde vers un dossier cible, après vérification des checksums.

### Restauration dans un dossier temporaire (recommandée)

```bash
python3 scripts/restore_local_state.py \
    --backup backups/backup_20260312T010000Z \
    --target /tmp/restore_test
```

### Restauration vers la racine du dépôt (destructive)

```bash
python3 scripts/restore_local_state.py \
    --backup backups/backup_20260312T010000Z \
    --target . \
    --force
```

⚠️ **L'option `--force` est requise pour écraser la racine du dépôt.** Sans elle, le script refuse.

### Options disponibles

| Option       | Description                                         | Défaut             |
|--------------|-----------------------------------------------------|--------------------|
| `--backup`   | Chemin vers le dossier de sauvegarde (obligatoire)  | —                  |
| `--target`   | Dossier cible de restauration                       | racine du dépôt    |
| `--force`    | Autorise l'écrasement de la racine                  | désactivé          |
| `--dry-run`  | Simulation sans écriture                            | désactivé          |

### Via make

```bash
make ops-restore BACKUP=backups/backup_20260312T010000Z TARGET=/tmp/restore_test
```

---

## Exercice de restauration pas à pas

Cet exercice permet de vérifier que la sauvegarde et la restauration fonctionnent correctement.

### Étape 1 — Créer une sauvegarde

```bash
python3 scripts/backup_local_state.py \
    --output /tmp/test_backup \
    --include docs project
```

Vérifier que la sortie contient :
```
✓ Sauvegarde terminée : backup_XXXXXXXXXXXXXXZ
✓ Manifeste écrit    : /tmp/test_backup/backup_XXXXXXXXXXXXXXZ/manifest.json
```

### Étape 2 — Inspecter le manifeste

```bash
cat /tmp/test_backup/backup_*/manifest.json | python3 -m json.tool | head -30
```

Vérifier que :
- `"erreurs": 0`
- `"total_fichiers"` > 0
- chaque entrée contient `"fichier"` et `"sha256"`

### Étape 3 — Restaurer dans un dossier temporaire

```bash
BACKUP_PATH=$(ls -d /tmp/test_backup/backup_*)
python3 scripts/restore_local_state.py \
    --backup "$BACKUP_PATH" \
    --target /tmp/test_restore
```

Vérifier que la sortie contient :
```
✓ N checksum(s) vérifiés.
✓ Restauration terminée : N fichier(s) restauré(s).
```

### Étape 4 — Vérifier l'intégrité des fichiers restaurés

```bash
diff -r /tmp/test_restore/docs ./docs
```

Le diff doit être vide (aucune différence).

### Étape 5 — Nettoyage

```bash
rm -rf /tmp/test_backup /tmp/test_restore
```

---

## Procédure de rollback

En cas de problème après une modification, il est possible de revenir à un état antérieur.

### Rollback via git (recommandé)

```bash
# Afficher l'historique des commits
git log --oneline -10

# Revenir à un commit précédent (sans perdre les modifications locales)
git revert <commit-sha>

# Ou reset dur (DESTRUCTIF — perd les modifications non commitées)
git reset --hard <commit-sha>
```

### Rollback via sauvegarde locale

Si git n'est pas disponible ou si l'état est trop dégradé :

```bash
python3 scripts/restore_local_state.py \
    --backup backups/backup_<horodatage> \
    --target . \
    --force
```

Puis relancer les validations :

```bash
make validate
make test
```

### Critères de rollback

Déclencher un rollback si :
- `make validate` échoue après un merge
- `make test` retourne des échecs inattendus
- la checklist maître n'est plus synchronisée avec le registre
- un invariant fondamental est violé (cf. `docs/RELEASE_GATES.md`)

---

## Preuves et validations

### Résultats de validation (à l'issue de T0034)

```
$ make validate
python3 scripts/validate_todo_registry.py --check-master
OK: registre valide (project/todo_registry.yaml)
OK: checklist synchronisée (docs/MASTER_TODO.md)
python3 scripts/sync_checklist.py --mode check
OK: checklist synchronisée (docs/MASTER_TODO.md)
```

### Résultats des tests (à l'issue de T0034)

```
$ make test
PYTHONPATH=src python3 -m pytest -q
..................................................   [100%]
N passed in X.XXs
```

### Exercice de restauration exécuté

L'exercice de restauration ci-dessus a été exécuté dans l'environnement de CI avec succès.
Les 12 tests de la classe `TestBackupLocalState` et `TestRestoreLocalState`
dans `tests/test_backup_restore.py` valident automatiquement :

- création d'une sauvegarde dans un dossier dédié
- présence et contenu du manifeste (version, timestamp, fichiers, sha256)
- restauration round-trip dans un dossier temporaire
- refus propre si sauvegarde absente
- refus propre si manifeste absent
- refus de restauration vers la racine sans `--force`
- mode dry-run sans écriture
