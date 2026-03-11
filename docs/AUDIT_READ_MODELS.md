# Modèles de lecture pour l'audit AI10101IA

> Référence canonique pour T0032.  
> Ce document définit les vues de lecture d'audit disponibles,
> leur structure et la façon de les interpréter.

---

## 1. Objectif

Les vues d'audit permettent à tout humain de comprendre l'état du système
sans accéder directement aux fichiers YAML bruts.
Elles sont générées par `scripts/build_audit_report.py` et suivent les
modèles définis ici.

---

## 2. Vue synthétique du registre bootstrap

**Source** : `project/bootstrap_entities.yaml`

Contient :

- l'identifiant du hub actif
- le nombre d'entités par type
- le total de preuves et d'événements

**Exemple** :

```
Hub    : HUB-001
Total entités  : 13
Total preuves  : 6
Total événements : 6

| Type       | Nombre |
|------------|--------|
| Dieux      | 3      |
| Academies  | 2      |
| Robots     | 4      |
| Lignees    | 3      |
| Regles     | 2      |
| Commandes  | 3      |
```

---

## 3. Vue des relations de filiation

**Source** : champ `relations[type=descendant_de]` des robots

Liste chaque paire enfant → parent observée dans le registre.

**Exemple** :

```
| Enfant      | Parent      |
|-------------|-------------|
| ROBOT-0002  | ROBOT-0001  |
```

Interprétation :

- `ROBOT-0002` est un descendant direct de `ROBOT-0001`
- Les deux appartiennent à `LIGNEE-001`

---

## 4. Vue des preuves par entité

**Source** : `project/bootstrap_proofs.yaml`

Associe chaque entité connue à la liste de ses preuves.

**Exemple** :

```
| Entité      | Preuves                        |
|-------------|--------------------------------|
| HUB-001     | PREUVE-00002, PREUVE-00006     |
| ROBOT-0001  | PREUVE-00003, PREUVE-00004     |
| ROBOT-0002  | PREUVE-00005                   |
```

Interprétation :

- si une entité n'a aucune preuve, elle est non auditée
- les preuves de type `validation_tache` prouvent la clôture d'une tâche
- les preuves de type `execution_regle` prouvent l'application d'une règle

---

## 5. Vue des incohérences détectées

**Source** : analyse croisée entités / preuves / événements

Liste toutes les anomalies trouvées dans le registre :

- score négatif
- référence d'entité manquante (lignée, académie, dieu tuteur, parent)
- preuve avec `entite_id` introuvable
- événement avec `preuve_id` introuvable

**Exemple sans incohérence** :

```
Aucune incohérence détectée.
```

**Exemple avec incohérence** :

```
⚠️  Robot ROBOT-0999 : lignee_id 'LIGNEE-999' introuvable.
⚠️  Preuve PREUVE-99999 : entite_id 'ROBOT-9999' introuvable.
```

---

## 6. Vue de synthèse exportable

**Fichier de sortie** : `/tmp/audit_report.md` (par défaut) ou chemin personnalisé.

Structure complète :

1. En-tête avec date de génération et statut global (`OK` / `ATTENTION`)
2. Section 1 : synthèse du registre
3. Section 2 : relations de filiation
4. Section 3 : preuves par entité
5. Section 4 : incohérences
6. Section 5 : bilan

**Commande** :

```bash
python scripts/build_audit_report.py --output /tmp/audit_ai10101ia.md
```

ou via make :

```bash
make audit
```

---

## 7. Format JSON

Le rapport est également disponible en JSON pour traitement automatique :

```bash
python scripts/build_audit_report.py --format json --output /tmp/audit.json
```

Structure JSON :

```json
{
  "synthese": {
    "generated_at": "...",
    "hub": "HUB-001",
    "entites_par_type": {...},
    "total_entites": 13,
    "total_preuves": 6,
    "total_evenements": 6
  },
  "filiation": [
    {"enfant": "ROBOT-0002", "parent": "ROBOT-0001"}
  ],
  "preuves_par_entite": {
    "HUB-001": ["PREUVE-00002", "PREUVE-00006"],
    ...
  },
  "incoherences": [],
  "statut": "OK"
}
```

---

## 8. Politique d'interprétation

| Statut | Signification | Action attendue |
|---|---|---|
| `OK` | Aucune incohérence détectée | Aucune action requise |
| `ATTENTION` | Incohérences présentes | Corriger avant merge |

Un rapport avec statut `ATTENTION` doit être analysé et les incohérences
corrigées avant toute validation de PR.

---

## 9. Dépendances

Ce document s'appuie sur :

- `docs/AUDIT_MODEL.md` (T0023) : définition du modèle de preuve
- `docs/PILOT_DATASET.md` (T0029) : description du dataset bootstrap
- `docs/VALIDATION_POLICY.md` (T0030) : politique de validation métier
- `scripts/build_audit_report.py` : génération automatique du rapport
