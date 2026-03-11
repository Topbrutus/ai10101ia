# Registre central des entités

> Référence canonique pour T0019.  
> Ce document définit la structure, les règles et les contrats du registre central
> de toutes les entités principales du système AI10101IA.

---

## 1. Périmètre

Le registre central est la source de vérité unique pour toutes les entités du système.
Il couvre les types d'entités suivants :

| Type          | Code interne | Description courte                               |
|---------------|--------------|--------------------------------------------------|
| Dieu          | `DIEU`       | Entité divine du panthéon (108 dieux canoniques) |
| Académie      | `ACADEMIE`   | Institution d'enseignement et de cursus          |
| Robot         | `ROBOT`      | Agent autonome issu d'une lignée                 |
| Lignée        | `LIGNEE`     | Filiation généalogique entre robots              |
| Tâche         | `TACHE`      | Unité de travail du registre projet              |
| Règle         | `REGLE`      | Contrat de comportement du moteur de règles      |
| Commande      | `COMMANDE`   | Instruction slash du bus de commandes            |
| Preuve        | `PREUVE`     | Enregistrement d'audit ou de validation          |

---

## 2. Identifiant canonique

Chaque entité possède un identifiant unique selon le schéma :

```
{CODE_TYPE}-{SEQUENCE_ZERO_PAD}
```

Exemples :
- `DIEU-001` (premier dieu)
- `ROBOT-0042`
- `TACHE-T0019`

Règles :
- l'identifiant est immuable une fois créé
- la séquence commence à 1 (zéro padding à 3 ou 4 chiffres selon le type)
- les alias humains sont autorisés en plus de l'identifiant canonique mais ne remplacent pas l'ID

---

## 3. Structure d'une entrée de registre

Chaque entité enregistrée possède les champs obligatoires suivants :

```yaml
id: ROBOT-0001                      # identifiant canonique
type: ROBOT                         # type d'entité
version: 1                          # version de la fiche (entier, incrémental)
statut: actif                       # voir §4
proprietaire: Topbrutus             # responsable de l'entité
cree_le: "2026-03-11T22:00:00Z"     # date de création (ISO 8601 UTC)
modifie_le: "2026-03-11T22:00:00Z"  # date de dernière mise à jour
relations: []                       # voir §6
metadonnees: {}                     # voir §7
historique: []                      # voir §8
```

Les champs additionnels dépendent du type d'entité et sont définis dans les schémas
métier (`project/schemas/`).

---

## 4. États d'une entité

| Statut     | Description                                         | Transitions autorisées              |
|------------|-----------------------------------------------------|-------------------------------------|
| `brouillon`| Entité créée mais non validée                       | → `actif`, → `archive`              |
| `actif`    | Entité pleinement opérationnelle                    | → `suspendu`, → `archive`           |
| `suspendu` | Entité temporairement inactive                      | → `actif`, → `archive`              |
| `archive`  | Entité retirée du fonctionnement courant            | aucune transition (état terminal)   |

---

## 5. Versionnement

- la `version` est un entier incrémenté à chaque modification structurelle
- une modification de métadonnée non structurelle n'incrémente pas obligatoirement la version
- chaque changement de version génère une entrée dans `historique`
- le rollback vers une version antérieure est possible mais doit être tracé comme une entrée d'historique

---

## 6. Relations entre entités

Le champ `relations` est une liste d'objets :

```yaml
relations:
  - type: appartient_a      # type sémantique de la relation
    cible: ACADEMIE-003     # identifiant canonique de la cible
    depuis: "2026-01-01"    # date de début de la relation
    jusqu: null             # date de fin (null = toujours active)
    notes: ""
```

Types de relations autorisés :

| Type de relation  | Sens                                      |
|-------------------|-------------------------------------------|
| `appartient_a`    | entité membre d'un groupe ou type parent  |
| `gouverne`        | entité A supervise entité B               |
| `issu_de`         | filiation directe (lignée)               |
| `reference`       | lien informationnel sans hiérarchie       |
| `depend_de`       | dépendance fonctionnelle                  |

---

## 7. Métadonnées obligatoires

Selon le type d'entité, les métadonnées minimales obligatoires sont :

**DIEU** : `nom`, `domaine`, `rang`, `attributs[]`  
**ACADEMIE** : `nom`, `type_cursus`, `capacite`  
**ROBOT** : `nom`, `classe`, `lignee_id`, `scores{}`  
**LIGNEE** : `nom`, `fondateur_id`, `generation`  
**TACHE** : `titre`, `phase`, `statut`, `obligatoire`  
**REGLE** : `nom`, `priorite`, `statut_regle`  
**COMMANDE** : `slash`, `categorie`, `niveau_risque`  
**PREUVE** : `type_preuve`, `source`, `date_preuve`

---

## 8. Historique minimal

Le champ `historique` conserve les événements significatifs :

```yaml
historique:
  - version: 1
    action: creation
    auteur: Topbrutus
    date: "2026-03-11T22:00:00Z"
    note: "Création initiale."
  - version: 2
    action: modification
    auteur: Topbrutus
    date: "2026-03-12T10:00:00Z"
    note: "Mise à jour du statut."
```

Règles :
- toute modification de statut est tracée
- toute modification de relation est tracée
- toute suppression logique est tracée avec le motif

---

## 9. Règles d'unicité

- deux entités du même type ne peuvent pas avoir le même identifiant canonique
- deux entités du même type ne peuvent pas avoir le même alias humain (nom)
- un doublon détecté à l'insertion déclenche une erreur bloquante

---

## 10. Règles d'archivage

- une entité ne peut être archivée que par son propriétaire ou un administrateur
- l'archivage est irréversible (état terminal)
- l'entité archivée reste consultable en lecture seule
- les relations actives d'une entité archivée sont marquées `jusqu` avec la date d'archivage

---

## 11. Règles de consultation

- toute entité active ou suspendue est lisible par tous les agents autorisés
- les entités archivées sont lisibles en lecture seule
- les brouillons ne sont lisibles que par leur propriétaire et les administrateurs

---

## 12. Règles de mise à jour

- seul le propriétaire ou un agent délégué peut modifier une entité
- toute modification incrémente la version et ajoute une entrée d'historique
- un champ immuable (`id`, `type`, `cree_le`) ne peut jamais être modifié
- une modification de statut requiert une preuve associée (voir docs/AUDIT_MODEL.md)

---

## 13. Règles de cohérence inter-entités

- une entité ne peut référencer comme cible de relation une entité archivée
- une lignée ne peut exister sans un fondateur valide (ROBOT ou DIEU actif)
- un robot ne peut appartenir qu'à une seule académie à la fois
- la suppression logique d'une entité cascade sur les relations dépendantes
- les identifiants de tâches (T0001…) ne doivent pas être dupliqués entre le registre projet et le registre central

---

## 14. Dépendances

Ce registre s'appuie sur :
- `project/schemas/` : définitions de schémas métier (T0018)
- `docs/AUDIT_MODEL.md` : modèle de preuve (T0023)
- `docs/MULTI_INDEX.md` : index de consultation rapide (T0022)

Il est utilisé par :
- `docs/RULE_ENGINE_CONTRACT.md` (T0020)
- `docs/SLASH_BUS_CONTRACT.md` (T0021)
