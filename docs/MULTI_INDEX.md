# Multi-index initial

> Référence canonique pour T0022.  
> Ce document définit la structure initiale du multi-index universel d'AI10101IA,
> les règles de reconstruction, de cohérence et d'audit.

---

## 1. Définition

Le multi-index est la couche de consultation rapide du registre central.
Il maintient plusieurs index spécialisés qui permettent de retrouver et croiser
les entités sans parcourir l'intégralité du registre.

Le multi-index est dérivé du registre central (T0019) : il ne constitue pas
une source de vérité indépendante. En cas de divergence, le registre central
fait foi.

---

## 2. Index d'identité

**Objectif** : retrouver immédiatement n'importe quelle entité par son identifiant canonique.

```yaml
index_identite:
  ROBOT-0001:
    type: ROBOT
    statut: actif
    version: 3
    localisation: registre_central
  DIEU-001:
    type: DIEU
    statut: actif
    version: 1
    localisation: registre_central
```

- Clé : identifiant canonique (ex : `ROBOT-0001`)
- Valeur : type, statut, version, pointeur vers l'entrée complète
- Reconstruction : balayage séquentiel du registre central

---

## 3. Index de type

**Objectif** : lister toutes les entités d'un type donné.

```yaml
index_type:
  ROBOT:
    - ROBOT-0001
    - ROBOT-0042
  DIEU:
    - DIEU-001
  ACADEMIE:
    - ACADEMIE-003
```

- Clé : type d'entité (CODE_TYPE)
- Valeur : liste ordonnée des identifiants canoniques

---

## 4. Index de filiation

**Objectif** : naviguer dans les arbres généalogiques entre robots et lignées.

```yaml
index_filiation:
  LIGNEE-001:
    fondateur: ROBOT-0001
    membres:
      - ROBOT-0003
      - ROBOT-0007
      - ROBOT-0012
  ROBOT-0001:
    parent: null
    enfants:
      - ROBOT-0003
```

- Clé : identifiant de lignée ou de robot
- Valeur : fondateur, membres directs, liens parent/enfant
- Règle : un robot ne peut appartenir qu'à une seule lignée

---

## 5. Index de fonction

**Objectif** : retrouver les entités par rôle ou domaine fonctionnel.

```yaml
index_fonction:
  gouvernance:
    - DIEU-001
    - ACADEMIE-001
  enseignement:
    - ACADEMIE-003
    - ACADEMIE-007
  production:
    - ROBOT-0001
    - ROBOT-0042
```

- Clé : fonction ou domaine (vocabulaire contrôlé)
- Valeur : liste des identifiants des entités exerçant cette fonction

---

## 6. Index d'état

**Objectif** : retrouver rapidement les entités par statut.

```yaml
index_etat:
  actif:
    - ROBOT-0001
    - DIEU-001
    - ACADEMIE-003
  suspendu:
    - ROBOT-0042
  brouillon: []
  archive:
    - ROBOT-0010
```

- Clé : statut (`actif`, `suspendu`, `brouillon`, `archive`)
- Valeur : liste des identifiants dans cet état

---

## 7. Index temporel

**Objectif** : retrouver les entités créées ou modifiées dans une plage de dates.

```yaml
index_temporel:
  "2026-03-11":
    crees:
      - ROBOT-0001
      - REGLE-0001
    modifies:
      - TACHE-T0019
```

- Clé : date (ISO 8601, résolution journalière)
- Valeur : listes `crees` et `modifies`
- Usage : audit quotidien, rapports d'activité

---

## 8. Index de score

**Objectif** : consulter et classer les entités par score cumulé.

```yaml
index_score:
  - id: ROBOT-0001
    score_total: 450
    score_academie: 120
    score_taches: 330
  - id: ROBOT-0042
    score_total: 210
    score_academie: 90
    score_taches: 120
```

- Trié par `score_total` décroissant
- Mis à jour à chaque attribution/retrait de points (via bus slash T0021)
- Ne contient que les entités de type ROBOT et DIEU (porteurs de scores)

---

## 9. Index de réputation

**Objectif** : suivre le score de réputation (distinct du score de points).

```yaml
index_reputation:
  - id: ROBOT-0001
    reputation: 92
    tendance: hausse     # hausse | stable | baisse
    derniere_maj: "2026-03-11"
  - id: ACADEMIE-003
    reputation: 78
    tendance: stable
    derniere_maj: "2026-03-10"
```

- Couverture : ROBOT, DIEU, ACADEMIE, LIGNEE
- Mis à jour lors des validations et des sanctions

---

## 10. Index de validation

**Objectif** : retrouver les entités en attente ou ayant été validées récemment.

```yaml
index_validation:
  en_attente:
    - REGLE-0002
    - ROBOT-0050
  validees_recentes:
    - {id: TACHE-T0019, date: "2026-03-11", validateur: Topbrutus}
```

---

## 11. Index de preuve

**Objectif** : retrouver toutes les preuves rattachées à une entité ou une tâche.

```yaml
index_preuve:
  TACHE-T0019:
    - PREUVE-00142
    - PREUVE-00143
  ROBOT-0001:
    - PREUVE-00100
  REGLE-0001:
    - PREUVE-00101
```

- Clé : identifiant canonique de l'entité, tâche ou règle
- Valeur : liste des identifiants de preuves associés
- Voir `docs/AUDIT_MODEL.md` pour le modèle des preuves

---

## 12. Règles de reconstruction

- La reconstruction complète du multi-index s'effectue depuis le registre central
  via la commande `/index.reconstruire`.
- La reconstruction est idempotente : appeler deux fois produit le même résultat.
- La reconstruction peut être totale (tous les index) ou partielle (un index donné).
- Une reconstruction complète génère une preuve de type `reconstruction_index`.
- La durée estimée de reconstruction est proportionnelle au nombre d'entités.

---

## 13. Règles de cohérence

- Un identifiant présent dans un index secondaire doit exister dans l'index d'identité.
- Un identifiant dans l'index d'état doit avoir le statut correspondant dans le registre.
- Les index de score et de réputation ne couvrent que les types autorisés.
- Toute incohérence détectée déclenche une alerte `INCOHERENCE_INDEX`.

---

## 14. Règles de recalcul

- Les index de score et de réputation sont recalculés à chaque événement
  d'attribution ou retrait via le bus slash (T0021).
- L'index temporel est mis à jour en temps réel à chaque modification du registre.
- Les autres index sont mis à jour de manière asynchrone après chaque opération.
- Un recalcul forcé est possible via `/index.recalculer --type score`.

---

## 15. Règles de suppression logique

- La suppression physique d'une entrée d'index n'est jamais effectuée.
- Les entités archivées sont déplacées dans la liste `archive` de l'index d'état.
- Les entrées obsolètes sont marquées `obsolete: true` mais conservées.
- L'index de preuve est immuable (les preuves ne peuvent pas être effacées de l'index).

---

## 16. Règles d'audit de l'index

Toute opération de reconstruction ou de recalcul génère une preuve d'audit :

```yaml
type_preuve: operation_index
operation: reconstruction_complete
declencheur: Topbrutus
horodatage: "2026-03-11T22:00:00Z"
entites_indexees: 142
incoherences_detectees: 0
```

Les opérations d'audit de l'index sont accessibles via `/audit.index`.

---

## 17. Dépendances

Ce document s'appuie sur :
- `docs/CENTRAL_REGISTRY.md` : registre des entités (T0019)
- `docs/AUDIT_MODEL.md` : modèle de preuve (T0023)

Il est utilisé par :
- `docs/RULE_ENGINE_CONTRACT.md` : pour les liens entre règles et entités (T0020)
- `docs/SLASH_BUS_CONTRACT.md` : mise à jour après commandes (T0021)
