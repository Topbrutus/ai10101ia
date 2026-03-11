# Contrat du moteur de règles

> Référence canonique pour T0020.  
> Ce document définit la structure, les contrats et les invariants du moteur de règles
> d'AI10101IA. Il ne constitue pas une implémentation complète mais le contrat que
> toute implémentation doit respecter.

---

## 1. Définition d'une règle

Une règle est une unité de logique conditionnelle versionnée, identifiable et auditable
qui produit une ou plusieurs actions lorsque ses conditions d'entrée sont satisfaites.

```yaml
id: REGLE-0001
nom: attribuer_points_validation
version: 1
statut_regle: active           # voir §9
priorite: 10                   # entier, plus bas = évalué en premier
categorie: points
description: "Attribue des points à un robot lorsqu'une tâche est validée."
entrees:
  - nom: tache_id
    type: string
    obligatoire: true
  - nom: robot_id
    type: string
    obligatoire: true
conditions:
  - expression: "tache.statut == 'done'"
  - expression: "robot.actif == true"
exceptions:
  - expression: "robot.suspendu == true"
    message: "Robot suspendu : règle ignorée."
actions:
  - type: attribuer_points
    cible: robot_id
    valeur: 10
    motif: "validation de tâche"
preuve_produite: true
journalisation: complete        # voir §10
dependances: []                 # liste d'IDs de règles dont celle-ci dépend
liens:
  dieux: []
  academies: []
  robots: []
  lignees: []
```

---

## 2. Entrées

Les entrées (`entrees`) définissent les données requises pour évaluer la règle :

| Champ         | Type     | Description                           |
|---------------|----------|---------------------------------------|
| `nom`         | string   | Nom de la variable d'entrée           |
| `type`        | string   | Type attendu (string, int, bool, etc.)|
| `obligatoire` | boolean  | Bloque l'évaluation si manquant       |
| `defaut`      | any      | Valeur par défaut si non obligatoire  |

Une entrée manquante et obligatoire produit une erreur de type `ENTREE_MANQUANTE`
et interrompt l'évaluation de la règle.

---

## 3. Conditions

Les conditions (`conditions`) sont des expressions booléennes évaluées dans l'ordre.
Toutes les conditions doivent être vraies pour déclencher les actions (ET logique par défaut).

```yaml
conditions:
  - expression: "entite.statut == 'actif'"
    operateur: ET          # ET (défaut) ou OU
```

- Une condition fausse arrête l'évaluation et aucune action n'est déclenchée.
- Les expressions utilisent des variables d'entrée et des fonctions utilitaires
  définies par le runtime (préfixe `fn:`).

---

## 4. Priorités

- La priorité est un entier positif (1 = plus haute priorité).
- Les règles sont évaluées dans l'ordre croissant de priorité.
- En cas d'égalité, l'ordre d'insertion dans le registre est utilisé.
- La priorité peut être modifiée uniquement par le propriétaire de la règle
  avec justification tracée.

---

## 5. Exceptions

Les exceptions (`exceptions`) sont des conditions qui court-circuitent
l'application des actions même si les conditions normales sont satisfaites :

```yaml
exceptions:
  - expression: "robot.statut == 'suspendu'"
    message: "Robot suspendu : règle ignorée."
    code: ROBOT_SUSPENDU
```

- Une exception active génère une entrée de journal de type `REGLE_IGNOREE`.
- Les exceptions ne comptent pas comme un échec de règle.

---

## 6. Actions

Les actions (`actions`) définissent les effets produits si la règle est déclenchée :

```yaml
actions:
  - type: attribuer_points        # type d'action (vocabulaire contrôlé)
    cible: "{robot_id}"           # identifiant canonique de la cible
    valeur: 10
    motif: "validation de tâche"
  - type: mettre_a_jour_statut
    cible: "{tache_id}"
    valeur: done
```

Types d'actions autorisés (vocabulaire contrôlé) :

| Type                  | Description                                  |
|-----------------------|----------------------------------------------|
| `attribuer_points`    | Ajoute des points à une entité               |
| `retirer_points`      | Retire des points                            |
| `mettre_a_jour_statut`| Change le statut d'une entité               |
| `creer_entite`        | Crée une nouvelle entité dans le registre    |
| `archiver_entite`     | Archive une entité                           |
| `emettre_evenement`   | Publie un événement sur le bus               |
| `notifier`            | Envoie une notification                      |
| `journaliser`         | Produit une entrée d'audit forcée            |

---

## 7. Validation d'une règle

Avant d'être activée, une règle doit passer la validation structurelle :

- présence de tous les champs obligatoires
- identifiant unique non dupliqué
- expressions syntaxiquement valides
- types des entrées connus
- types des actions connus
- dépendances déclarées existantes et actives

Une règle invalide reste en statut `brouillon` et n'est pas évaluée.

---

## 8. Preuve produite

Si `preuve_produite: true`, chaque évaluation réussie de la règle génère
une entrée de preuve dans le modèle d'audit (voir `docs/AUDIT_MODEL.md`) :

```yaml
type_preuve: execution_regle
regle_id: REGLE-0001
entrees: {tache_id: "T0019", robot_id: "ROBOT-0001"}
resultat: declenche
actions_executees:
  - type: attribuer_points
    cible: ROBOT-0001
    valeur: 10
date_preuve: "2026-03-11T22:00:00Z"
auteur: moteur_de_regles
```

---

## 9. Statut d'une règle

| Statut      | Description                                      |
|-------------|--------------------------------------------------|
| `brouillon` | En cours de définition, non évaluée             |
| `active`    | Évaluée normalement                              |
| `suspendue` | Désactivée temporairement, non évaluée          |
| `retirée`   | Retirée définitivement, non évaluée (archivée)  |

---

## 10. Journalisation

Chaque évaluation de règle produit une entrée de journal :

| Niveau         | Cas                                              |
|----------------|--------------------------------------------------|
| `INFO`         | Règle évaluée, conditions non satisfaites        |
| `SUCCESS`      | Règle déclenchée, actions exécutées              |
| `WARN`         | Exception activée, règle ignorée                 |
| `ERROR`        | Erreur d'entrée ou d'action                      |

La journalisation `complete` enregistre les entrées, conditions et résultats.
La journalisation `minimale` n'enregistre que le déclenchement ou le non-déclenchement.

---

## 11. Conflits entre règles

Un conflit est détecté lorsque deux règles actives produisent des actions
contradictoires sur la même cible dans le même contexte.

Stratégies de résolution (ordre de priorité) :

1. Priorité explicite (règle de priorité inférieure gagne)
2. Version (règle de version plus récente gagne)
3. Ordre d'enregistrement (première règle gagne)

Les conflits non résolus automatiquement déclenchent un événement `CONFLIT_REGLE`
et suspendent les deux règles concernées jusqu'à arbitrage humain.

---

## 12. Ordre d'évaluation

1. Trier les règles actives par priorité croissante
2. Évaluer les dépendances inter-règles (les règles dépendantes attendent leurs prérequis)
3. Évaluer les conditions
4. Appliquer les exceptions
5. Exécuter les actions
6. Produire la preuve si activée
7. Journaliser le résultat

---

## 13. Promotion, retrait et désactivation

| Opération     | Transition          | Autorisation requise  |
|---------------|---------------------|-----------------------|
| Promotion     | brouillon → active  | Propriétaire + revue  |
| Suspension    | active → suspendue  | Propriétaire          |
| Réactivation  | suspendue → active  | Propriétaire          |
| Retrait       | active → retirée    | Propriétaire + preuve |

Chaque opération génère une entrée d'historique et une preuve d'audit.

---

## 14. Dépendances entre règles

```yaml
dependances:
  - REGLE-0002   # doit être évaluée avant la présente règle
  - REGLE-0003
```

- Une règle dont une dépendance n'est pas active est automatiquement suspendue.
- Les dépendances circulaires sont interdites et détectées à la validation.

---

## 15. Liens avec le registre central

Chaque règle peut déclarer des liens explicites vers des entités du registre :

```yaml
liens:
  dieux: [DIEU-001]
  academies: [ACADEMIE-003]
  robots: []
  lignees: []
```

Ces liens permettent au multi-index (T0022) de retrouver toutes les règles
applicables à une entité donnée.

---

## 16. Dépendances

Ce contrat s'appuie sur :
- `docs/CENTRAL_REGISTRY.md` : registre des entités (T0019)
- `docs/AUDIT_MODEL.md` : modèle de preuve (T0023)
- `project/schemas/` : schémas métier (T0018)

Il est utilisé par :
- `docs/SLASH_BUS_CONTRACT.md` (T0021)
- `docs/MULTI_INDEX.md` (T0022)
