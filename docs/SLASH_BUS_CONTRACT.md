# Contrat du bus de commandes slash

> Référence canonique pour T0021.  
> Ce document définit le format, les règles et les invariants du bus de commandes slash
> d'AI10101IA. Il constitue l'interface officielle d'action du système.

---

## 1. Définition

Le bus slash est le point d'entrée unique pour toutes les actions explicites
émises par des agents (humains ou robots) sur le système AI10101IA.
Toute modification d'état du système doit passer par une commande slash traçable.

---

## 2. Format canonique

```
/{categorie}.{action} [--arg1 valeur1] [--arg2 valeur2] [--contexte <id>]
```

Exemples :
```
/tache.clore --id T0019 --motif "Définition du registre central effectuée"
/robot.suspendre --id ROBOT-0042 --motif "Violation de règle REGLE-0007"
/points.attribuer --robot ROBOT-0001 --valeur 10 --motif "Validation T0019"
/regle.promouvoir --id REGLE-0001
```

---

## 3. Structure d'une commande

```yaml
slash: /tache.clore                 # commande (catégorie + action)
categorie: tache                    # catégorie principale
action: clore                       # action dans la catégorie
arguments:                          # arguments nommés
  id: T0019
  motif: "Définition du registre central effectuée"
contexte:                           # contexte d'exécution (optionnel)
  agent_id: Topbrutus
  session_id: "sess-20260311-001"
  horodatage: "2026-03-11T22:00:00Z"
```

---

## 4. Arguments

Les arguments sont toujours nommés (pas d'arguments positionnels).

| Champ       | Obligatoire | Type   | Description                               |
|-------------|-------------|--------|-------------------------------------------|
| `--id`      | Selon cmd   | string | Identifiant canonique de la cible         |
| `--motif`   | Selon cmd   | string | Justification humaine de l'action         |
| `--valeur`  | Selon cmd   | any    | Valeur à appliquer                        |
| `--contexte`| Non         | string | Identifiant de session ou de contexte     |
| `--preuve`  | Non         | string | Référence à une preuve existante          |
| `--dry-run` | Non         | bool   | Simule sans appliquer (niveau FAIBLE)     |

Les arguments propres à chaque commande sont définis dans le catalogue des commandes.

---

## 5. Permissions

Chaque commande déclare un niveau de permission minimum requis :

| Niveau       | Description                                              |
|--------------|----------------------------------------------------------|
| `PUBLIC`     | Accessible à tout agent authentifié                      |
| `MEMBRE`     | Réservé aux membres actifs                               |
| `MODERATEUR` | Réservé aux modérateurs et administrateurs               |
| `ADMIN`      | Réservé aux administrateurs                              |
| `SYSTEME`    | Réservé au moteur interne (non appelable manuellement)  |

Une commande appelée sans permission suffisante est rejetée avec code `PERMISSION_INSUFFISANTE`.

---

## 6. Validation

Avant exécution, chaque commande est soumise à une validation structurelle :

1. Présence du slash préfixe `/`
2. Format `{categorie}.{action}` valide
3. Catégorie et action reconnues dans le catalogue
4. Arguments obligatoires présents
5. Types des arguments corrects
6. Permission de l'agent suffisante
7. Entité cible existante et dans un état compatible

Toute validation échouée retourne un objet d'erreur avec :
```yaml
code: VALIDATION_ECHOUEE
commande: "/tache.clore"
message: "Argument --id manquant."
horodatage: "2026-03-11T22:00:00Z"
```

---

## 7. Preuve attendue

Toute commande de niveau MODÉRÉ ou ÉLEVÉ génère automatiquement une preuve d'audit :

```yaml
type_preuve: execution_commande
commande: /tache.clore
agent_id: Topbrutus
arguments: {id: T0019, motif: "..."}
resultat: succes
horodatage: "2026-03-11T22:00:00Z"
```

Voir `docs/AUDIT_MODEL.md` pour le modèle complet.

---

## 8. Résultat attendu

Chaque commande retourne un objet résultat :

```yaml
statut: succes            # succes | echec | simule | refuse
commande: /tache.clore
cible: T0019
actions_executees:
  - type: mettre_a_jour_statut
    cible: T0019
    valeur: done
preuve_id: PREUVE-00142   # si preuve générée
message: "Tâche T0019 clôturée."
```

---

## 9. Niveau de risque

Chaque commande est classée selon un niveau de risque :

| Niveau    | Code  | Description                                    | Confirmation requise |
|-----------|-------|------------------------------------------------|----------------------|
| Faible    | `F`   | Action réversible, impact limité               | Non                  |
| Modéré    | `M`   | Action partiellement réversible                | Non (mais journalisé)|
| Élevé     | `E`   | Action irréversible ou à fort impact           | Oui (confirmation)   |
| Critique  | `C`   | Action sur données critiques ou archivage      | Oui (double validation)|

Les commandes de niveau Critique nécessitent une seconde validation par un modérateur.

---

## 10. Contexte d'exécution

Chaque commande s'exécute dans un contexte qui précise :

```yaml
contexte:
  agent_id: Topbrutus          # qui émet la commande
  agent_type: humain           # humain | robot | systeme
  session_id: "sess-001"       # session de travail
  horodatage: "2026-03-11T22:00:00Z"
  ip: null                     # optionnel, pour traçabilité externe
  canal: web                   # web | api | script | interne
```

---

## 11. Catégories de commandes

| Catégorie  | Description                                      |
|------------|--------------------------------------------------|
| `tache`    | Gestion du cycle de vie des tâches               |
| `robot`    | Gestion des robots (création, suspension, etc.)  |
| `points`   | Attribution et retrait de points                 |
| `regle`    | Gestion du cycle de vie des règles               |
| `academie` | Gestion des académies et cursus                  |
| `dieu`     | Gestion des entités divines                      |
| `lignee`   | Gestion des filiations                           |
| `audit`    | Consultation et export d'audit                   |
| `index`    | Reconstruction et consultation du multi-index    |
| `systeme`  | Commandes réservées au moteur interne            |

---

## 12. Règles de nommage

- Format strict : `/{categorie}.{action}`
- Minuscules uniquement
- Séparateur catégorie/action : point `.`
- Pas d'espaces, pas de caractères spéciaux dans le nom de commande
- Les actions doivent être des verbes à l'infinitif (ex : `clore`, `suspendre`, `promouvoir`)
- Pas d'abréviations ambiguës

---

## 13. Interdictions

- il est interdit d'appeler une commande `SYSTEME` manuellement
- il est interdit d'omettre `--motif` sur toute commande de niveau Élevé ou Critique
- il est interdit d'utiliser `--dry-run` sur les commandes de niveau Critique
- il est interdit d'enchaîner plusieurs commandes Critiques sans preuve intermédiaire
- il est interdit de contourner le bus slash pour modifier directement l'état d'une entité

---

## 14. Événements générés

Chaque commande exécutée avec succès publie un événement sur le bus interne :

```yaml
evenement:
  type: commande_executee
  commande: /tache.clore
  cible: T0019
  agent_id: Topbrutus
  horodatage: "2026-03-11T22:00:00Z"
  preuve_id: PREUVE-00142
```

Ces événements peuvent déclencher des règles du moteur (T0020).

---

## 15. Liens avec le registre et le moteur de règles

- Avant exécution, le bus vérifie que la cible existe dans le registre central (T0019).
- L'exécution d'une commande peut déclencher des règles du moteur (T0020).
- Le moteur peut émettre des commandes de type `SYSTEME` en réponse à une règle.
- Toutes les preuves générées sont conformes au modèle d'audit (T0023).
- Le multi-index (T0022) est mis à jour après toute commande modifiant une entité.

---

## 16. Dépendances

Ce contrat s'appuie sur :
- `docs/CENTRAL_REGISTRY.md` : registre des entités (T0019)
- `docs/RULE_ENGINE_CONTRACT.md` : moteur de règles (T0020)
- `docs/AUDIT_MODEL.md` : modèle de preuve (T0023)

Il est utilisé par :
- `docs/MULTI_INDEX.md` (T0022)
