# Modèle de preuve et d'audit

> Référence canonique pour T0023.  
> Ce document définit ce qui constitue une preuve valide dans AI10101IA et comment
> l'audit s'appuie sur le modèle de preuve.

---

## 1. Définition

Une preuve est un enregistrement immuable et traçable qui démontre qu'un événement,
une décision, une validation ou une action a réellement eu lieu dans le système.
Les preuves sont la garantie d'auditabilité d'AI10101IA.

---

## 2. Types de preuves

| Type                   | Code                   | Description                                                |
|------------------------|------------------------|------------------------------------------------------------|
| Exécution de règle     | `execution_regle`      | Déclenchement d'une règle du moteur                        |
| Exécution de commande  | `execution_commande`   | Traitement d'une commande slash                            |
| Validation de tâche    | `validation_tache`     | Clôture ou validation d'une tâche                          |
| Modification d'entité  | `modification_entite`  | Changement structurel dans le registre                     |
| Décision humaine       | `decision_humaine`     | Arbitrage ou décision prise par un humain                  |
| Attribution de points  | `attribution_points`   | Attribution ou retrait de points                           |
| Opération d'index      | `operation_index`      | Reconstruction ou recalcul du multi-index                  |
| Revue documentaire     | `revue_documentaire`   | Validation d'un document ou d'une politique                |
| Alerte de sécurité     | `alerte_securite`      | Incident ou anomalie détectée                              |
| Événement système      | `evenement_systeme`    | Événement interne non lié à une action utilisateur         |

---

## 3. Structure d'une preuve

```yaml
id: PREUVE-00142                        # identifiant canonique, séquence globale
type_preuve: validation_tache           # type (vocabulaire contrôlé §2)
version: 1                              # version de la fiche preuve

# Origine et horodatage
origine: bus_slash                      # voir §4
date_preuve: "2026-03-11T22:00:00Z"    # ISO 8601 UTC, immuable
auteur: Topbrutus                       # identifiant de l'agent émetteur (voir §5)
auteur_type: humain                     # humain | robot | systeme

# Rattachements
tache_id: T0019                         # tâche associée (null si non applicable)
regle_id: null                          # règle associée (null si non applicable)
commande: /tache.clore                  # commande à l'origine (null si non applicable)
entite_id: TACHE-T0019                  # entité directement concernée

# Contenu de la preuve
contenu:
  statut_avant: todo
  statut_apres: done
  motif: "Définition documentaire du registre central effectuée."
  artefacts:
    - docs/CENTRAL_REGISTRY.md

# Confiance et validation
niveau_confiance: eleve                 # voir §10
validation: automatique                 # automatique | humaine | mixte (voir §11)
validee_par: null                       # identifiant du validateur humain si applicable
validee_le: null

# Métadonnées d'audit
immuable: true                          # les preuves ne peuvent pas être modifiées
archive: false                          # true après la période de rétention active
```

---

## 4. Origine

L'`origine` précise le mécanisme qui a généré la preuve :

| Valeur           | Description                                  |
|------------------|----------------------------------------------|
| `bus_slash`      | Générée lors d'une exécution de commande     |
| `moteur_regles`  | Générée lors d'un déclenchement de règle     |
| `agent_humain`   | Produite manuellement par un humain          |
| `systeme`        | Générée par un processus interne automatique |
| `ci_cd`          | Générée par un pipeline de validation        |

---

## 5. Auteur ou source

L'`auteur` est l'identifiant de l'agent ayant initié l'événement :

- Pour un humain : son identifiant GitHub ou système
- Pour un robot : son identifiant canonique (`ROBOT-0001`)
- Pour le système : `systeme` (réservé)
- Pour un pipeline : `ci_cd/{nom_workflow}`

L'auteur est immuable une fois la preuve créée.

---

## 6. Rattachement à une tâche

`tache_id` : identifiant de la tâche de référence du registre projet (ex : `T0019`).

- Une preuve sans tâche associée doit justifier l'absence de rattachement.
- Les preuves de validation de tâche ont obligatoirement un `tache_id`.

---

## 7. Rattachement à une règle

`regle_id` : identifiant canonique d'une règle du moteur (ex : `REGLE-0001`).

- Les preuves de type `execution_regle` ont obligatoirement un `regle_id`.
- Les autres types peuvent inclure un `regle_id` si une règle a influencé l'événement.

---

## 8. Rattachement à une commande

`commande` : commande slash à l'origine de la preuve (ex : `/tache.clore`).

- Les preuves de type `execution_commande` ont obligatoirement ce champ renseigné.

---

## 9. Rattachement à une entité

`entite_id` : identifiant canonique de l'entité principale concernée.

- Toute preuve doit être rattachée à au moins une entité du registre central.
- Plusieurs entités peuvent être concernées (liste `entites_secondaires`).

---

## 10. Niveau de confiance

| Niveau     | Description                                               |
|------------|-----------------------------------------------------------|
| `faible`   | Preuve informelle, non vérifiée                           |
| `moyen`    | Preuve automatique sans validation humaine                |
| `eleve`    | Preuve automatique validée ou preuve humaine structurée   |
| `certifie` | Preuve double-validée (humain + automatique)              |

Le niveau de confiance est attribué à la création et peut être réhaussé par une validation.

---

## 11. Validation humaine ou automatique

| Valeur        | Description                                        |
|---------------|----------------------------------------------------|
| `automatique` | Validée par le système sans intervention humaine   |
| `humaine`     | Validée par un agent humain désigné                |
| `mixte`       | Requiert les deux validations                      |

Les preuves de niveau `certifie` requièrent une validation mixte.

---

## 12. Auditabilité

- Toutes les preuves sont accessibles via `/audit.consulter --preuve <id>`.
- Une liste de preuves par entité est accessible via `/audit.lister --entite <id>`.
- Les preuves d'une plage temporelle : `/audit.lister --depuis <date> --jusqu <date>`.
- Le journal d'audit global est accessible via `/audit.exporter`.
- Aucune preuve ne peut être supprimée de l'index de preuve (T0022).

---

## 13. Rétention

| Niveau de confiance | Rétention active | Archive |
|---------------------|------------------|---------|
| `faible`            | 30 jours         | 1 an    |
| `moyen`             | 1 an             | 5 ans   |
| `eleve`             | 5 ans            | 10 ans  |
| `certifie`          | 10 ans           | perpétuel|

Après la période de rétention active, `archive: true` est positionné.
Les preuves archivées restent lisibles mais ne sont plus dans le flux courant.

---

## 14. Archivage

- L'archivage est automatique à l'expiration de la rétention active.
- L'archivage manuel est possible par un administrateur avec motif obligatoire.
- Une preuve archivée ne peut pas revenir en statut actif.
- L'archivage lui-même génère une preuve de type `evenement_systeme`.

---

## 15. Consultation

- Les preuves actives sont accessibles à tout agent authentifié.
- Les preuves archivées sont accessibles aux modérateurs et administrateurs uniquement.
- Les preuves de type `alerte_securite` sont réservées aux administrateurs.
- L'export massif est réservé aux administrateurs.

---

## 16. Critères de rejet d'une preuve

Une preuve est rejetée (statut `rejetee`) si :

| Critère                          | Code d'erreur           |
|----------------------------------|-------------------------|
| Identifiant dupliqué             | `ID_DUPLIQUE`           |
| Type de preuve inconnu           | `TYPE_INCONNU`          |
| Auteur non identifiable          | `AUTEUR_INVALIDE`       |
| Date absente ou invalide         | `DATE_INVALIDE`         |
| Entité cible inexistante         | `ENTITE_INCONNUE`       |
| Contenu vide ou insuffisant      | `CONTENU_INSUFFISANT`   |
| Signature invalide (si requise)  | `SIGNATURE_INVALIDE`    |
| Tâche référencée inexistante     | `TACHE_INCONNUE`        |

Une preuve rejetée est conservée avec le motif de rejet. Elle n'est pas supprimée.

---

## 17. Modèle d'audit

L'audit est la capacité à répondre aux questions :

1. **Qui** a fait quoi ?
2. **Quand** ?
3. **Pourquoi** (motif) ?
4. **Quel résultat** ?
5. **Quelle preuve** ?

Le modèle d'audit d'AI10101IA garantit ces cinq dimensions pour toute action
critique passant par le bus slash (T0021) ou le moteur de règles (T0020).

---

## 18. Dépendances

Ce document s'appuie sur :
- `docs/CENTRAL_REGISTRY.md` : registre des entités (T0019)
- `docs/EVIDENCE_POLICY.md` : politique de preuve générale

Il est utilisé par :
- `docs/RULE_ENGINE_CONTRACT.md` (T0020)
- `docs/SLASH_BUS_CONTRACT.md` (T0021)
- `docs/MULTI_INDEX.md` : index de preuve (T0022)
- `templates/evidence_record_template.md`
