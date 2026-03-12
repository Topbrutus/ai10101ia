# Phases du projet

## Ordre officiel des phases

### 01. Cadrage (`P1-CADRAGE`)

- **Gate de sortie** : Mission, périmètre, vocabulaire et critères d’acceptation validés.
- **Règle** : aucune phase suivante ne doit être engagée sans ce socle.

### 02. Fondation du dépôt (`P2-FONDATION`)

- **Gate de sortie** : Dépôt, structure, registre machine et checklist humaine validés.
- **Règle** : tant que le dépôt n’est pas stable, aucune industrialisation sérieuse ne doit partir.

### 03. Contrôles GitHub (`P3-CONTROLES-GITHUB`)

- **Gate de sortie** : PR gate, issue forms, instructions agents et workflows actifs.
- **Règle** : les contrôles doivent précéder l’augmentation du volume de contribution.

### 04. Modélisation métier (`P4-MODELISATION`)

- **Gate de sortie** : Taxonomie, schémas et catalogues métier approuvés.

### 05. Architecture technique (`P5-ARCHITECTURE`)

- **Gate de sortie** : Noyau registre, règles, commandes et multi-index implémentés.

### 06. Fonctionnel (`P6-FONCTIONNEL`)

- **Gate de sortie** : Scores, académies, reproduction, élection et hub minimal opérationnels.

### 07. Qualité et sécurité (`P7-QUALITE`)

- **Gate de sortie** : Observabilité, sécurité et performance vérifiées.

### 08. Déploiement (`P8-DEPLOIEMENT`)

- **Gate de sortie** : Staging, sauvegardes, restauration et readiness production validés.

### 09. Évolutions (`P9-EVOLUTIONS`)

- **Gate de sortie** : Feuille de route, multi-hub et robot élu préparés.

---

## État actuel de la fondation (après T0034)

Le socle validé couvre T0001–T0034, T0039 et T0040. Le bloc T0035–T0038 reste à construire (phase d'industrialisation).

| Bloc | Tâches | État |
|---|---|---|
| Cadrage | T0001–T0002 | Terminé |
| Fondation du dépôt | T0003–T0007 | Terminé |
| Contrôles GitHub | T0008–T0015 | Terminé |
| Modélisation métier | T0016–T0022 | Terminé |
| Architecture technique | T0023–T0033 | Terminé |
| Fonctionnel pilote | T0024–T0028 | Terminé |
| Dataset bootstrap | T0029–T0033 | Terminé |
| Durcissement final | T0039 | Terminé |
| Préparation industrialisation | T0040 | Terminé |
| Staging, sauvegarde, restauration | T0034 | Terminé |
| Production initiale | T0035 | À faire |
| Exploitation quotidienne | T0036 | À faire |
| Tests avancés | T0037 | À faire |
| Gouvernance multi-hub | T0038 | À faire |

## Transition vers l'industrialisation

La phase suivante est décrite dans :
- `docs/INDUSTRIALIZATION_ROADMAP.md` — feuille de route
- `docs/NEXT_PHASE_ARCHITECTURE.md` — architecture cible
- `docs/RELEASE_GATES.md` — gates de passage

**Condition de passage** : tous les gates bloquants de `docs/RELEASE_GATES.md` doivent être satisfaits.
