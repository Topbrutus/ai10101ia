# Politique de validation

## Définition

Une validation est le mécanisme qui confirme qu’un changement est acceptable au regard des règles du dépôt.

## Types de validation

- validation automatique
- validation humaine
- validation sécurité
- validation exploitation
- validation gouvernance

## Règles

- toute tâche doit déclarer une validation requise dans le registre
- la PR doit mentionner explicitement les validations réalisées
- les validations manquantes doivent bloquer le merge

## Exemples

- tests unitaires passés
- revue documentaire
- revue sécurité
- exercice de restauration
- revue d’architecture

## Validation métier (T0030)

La validation métier couvre les assets du domaine AI10101IA :

- **Schémas** : cohérence des entités avec les modèles définis (T0018, T0019)
- **Relations** : chaque relation inter-entité pointe vers une entité existante
- **Scores** : points, prestige, crédit social sont des entiers positifs ou nuls
- **Preuves** : chaque preuve référence une entité valide et a un type connu
- **Événements** : chaque événement référence une preuve valide et un hub existant

### Commande de validation métier

```bash
make validate-domain
# ou
python scripts/validate_domain_assets.py
```

Retourne 0 si tout est valide, 1 sinon avec messages d'erreur explicites sur stderr.

### Périmètre couvert

| Fichier | Validation appliquée |
|---|---|
| `project/bootstrap_entities.yaml` | Structure, relations, scores |
| `project/bootstrap_proofs.yaml` | Format, types, références |
| `project/bootstrap_events.yaml` | Format, références, cohérence |
