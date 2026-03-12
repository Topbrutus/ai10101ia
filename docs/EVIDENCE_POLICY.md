# Politique de preuve

## Définition

Une preuve est un élément traçable qui démontre qu’une tâche, une validation ou un changement a réellement eu lieu.

## Exemples recevables

- sortie de commande de validation
- journal d’exécution pertinent
- capture ciblée, si nécessaire
- lien vers un fichier de `records/`
- rapport de test
- diff commenté ou décision formelle

## Exemples insuffisants

- “ça marche chez moi”
- commentaire sans trace
- capture floue sans contexte
- affirmation non reliée à la tâche

## Règles

- la preuve doit être liée à l’identifiant de tâche
- la preuve doit être lisible ou reproductible
- la preuve doit être référencée dans la PR
- la preuve doit survivre à la relecture

## Preuves de release (T0039)

Pour une release ou un tag de la fondation, les preuves suivantes sont requises :

| Preuve | Format attendu | Bloquant |
|---|---|---|
| Sortie de `make validate` | Texte console ou log CI | Oui |
| Sortie de `make test` | Résultat pytest | Oui |
| Sortie de `make validate-domain` | Texte console ou log CI | Oui |
| Rapport d'audit | Fichier Markdown dans `records/` | Recommandé |
| Revue humaine | Approbation dans la PR | Oui |

## Conservation des preuves

- Les preuves engagées dans `records/` ne peuvent pas être supprimées
  sans décision formelle enregistrée.
- Les preuves de release sont à archiver dans `records/` après chaque tag.
- Les preuves doivent rester cohérentes avec les entités du bootstrap.
