# Règles de workflow

## Ordre officiel des opérations

1. identifier la tâche
2. vérifier ses dépendances
3. vérifier la phase
4. créer une branche conforme
5. modifier uniquement le périmètre nécessaire
6. produire preuves et validations
7. ouvrir une PR conforme
8. laisser les checks s’exécuter
9. faire relire
10. fusionner seulement si tout est vert

## Interdictions

- démarrer une tâche dont les dépendances ne sont pas satisfaites
- renuméroter le registre sans décision formelle
- modifier `docs/MASTER_TODO.md` à la main sans régénération
- supprimer une tâche obligatoire sans arbitrage
- fusionner une PR sans références de tâches
- fusionner une PR sans preuves ni validations
- contourner les workflows par commit direct sur la branche protégée

## Modifications des tâches

### Autorisé avec justification

- correction de description
- ajout de livrables attendus
- enrichissement des preuves et validations

### Renforcé

- changement de statut
- correction de dépendance
- ajout de tâche

### Interdit sans décision formelle

- suppression de tâche obligatoire
- changement d’ordre
- fusion de plusieurs tâches en une seule

## Exceptions

Les exceptions doivent être documentées via une issue de type décision et une PR justifiée.

## Gates de release et durcissement final

### Avant tout merge sur `main`

- `make validate` doit passer sans erreur
- `make test` doit passer sans échec
- La PR doit référencer au moins un identifiant de tâche valide
- Les dépendances des tâches citées doivent être satisfaites

### Avant tout tag ou livraison ZIP

- Suivre la procédure complète définie dans `docs/RELEASE_GATES.md`
- Toutes les cases bloquantes de la checklist de release doivent être cochées

### Gel temporaire

- Si `make validate` échoue sur `main`, aucun nouveau merge n'est autorisé
- Appliquer la procédure de gel et rollback de `docs/RELEASE_GATES.md`

## Transition vers la phase d'industrialisation

- La fondation doit être complète (T0001–T0040 tous `done`) avant d'engager l'industrialisation
- La feuille de route de la phase suivante est dans `docs/INDUSTRIALIZATION_ROADMAP.md`
- L'architecture cible est dans `docs/NEXT_PHASE_ARCHITECTURE.md`
- Ne pas démarrer un bloc d'industrialisation sans en avoir validé les prérequis
