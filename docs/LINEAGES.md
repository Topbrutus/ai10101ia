# Classes de robots et lignées — AI10101IA

> Document généré pour T0017. Source de vérité : `project/robot_classes.yaml`.

## Classes de robots

Chaque robot appartient à une **classe** qui définit ses permissions, son cycle de vie
et ses scores initiaux.

| ID | Nom | Quota max/hub | Niveau requis |
|----|-----|---------------|---------------|
| CLASSE-VALIDATEUR | Validateur | 20 | 1 |
| CLASSE-ARCHIVISTE | Archiviste | 10 | 1 |
| CLASSE-EXECUTEUR | Exécuteur | 30 | 1 |
| CLASSE-GARDIEN | Gardien | 5 | 2 |
| CLASSE-SCOREUR | Scoreur | 8 | 1 |
| CLASSE-REPRODUCTEUR | Reproducteur | 3 | 2 |

---

## Détail des classes

### Validateur

Spécialisé dans la validation des règles métier et la détection des incohérences.

- **Permissions** : lecture entités, écriture règles, exécution validation, émission alertes
- **Formation** : Académie de Logique Appliquée
- **Score initial** : 50 pts, 5 prestige, 70 crédit social
- **Retraite** : après 500 cycles ou prestige < 5

### Archiviste

Spécialisé dans la conservation des preuves et la production des rapports d'audit.

- **Permissions** : lecture/écriture preuves, écriture rapports, exécution audit
- **Formation** : Académie de la Mémoire Structurée
- **Score initial** : 80 pts, 8 prestige, 80 crédit social
- **Retraite** : après 600 cycles ou prestige < 8

### Exécuteur

Spécialisé dans l'exécution des workflows et l'optimisation des performances.

- **Permissions** : lecture entités, écriture événements, exécution workflows et commandes
- **Formation** : Académie de l'Exécution Optimale
- **Score initial** : 30 pts, 2 prestige, 65 crédit social
- **Retraite** : après 400 cycles ou performance < 60% de référence

### Gardien

Spécialisé dans la sécurité, le contrôle des accès et la détection des anomalies.

- **Permissions** : lecture entités/logs, écriture alertes, exécution blocage et audit sécurité
- **Formation** : Académie de la Sécurité et de l'Intégrité (niveau 2 requis)
- **Score initial** : 100 pts, 10 prestige, 85 crédit social
- **Retraite** : après 700 cycles ou 3 failles non détectées

### Scoreur

Spécialisé dans le calcul et la gestion des systèmes de points, prestige et crédit social.

- **Permissions** : lecture entités, écriture scores, exécution calculs et barèmes
- **Formation** : Académie de la Valeur et des Scores
- **Score initial** : 60 pts, 6 prestige, 75 crédit social
- **Retraite** : après 300 cycles ou erreur de calcul répétée

### Reproducteur

Spécialisé dans la création de nouvelles lignées et robots avec contrôle des quotas.

- **Permissions** : lecture entités, écriture lignées/robots, exécution reproduction et contrôle quotas
- **Formation** : Académie de la Reproduction et des Lignées (niveau 2 requis)
- **Score initial** : 120 pts, 12 prestige, 80 crédit social
- **Retraite** : après 5 violations de quotas

---

## Lignées

Chaque lignée est une famille de robots partageant des **attributs héréditaires** et
placée sous la tutelle d'un dieu.

| ID | Nom | Classe dominante | Dieu tuteur | Quota max |
|----|-----|-----------------|-------------|-----------|
| LIGNEE-AXIOM | Lignée Axiom | Validateur | Anaxis (DIEU-001) | 10 |
| LIGNEE-MNEMO | Lignée Mnemo | Archiviste | Orialys (DIEU-002) | 8 |
| LIGNEE-EXEC | Lignée Exec | Exécuteur | Vortex (DIEU-003) | 15 |
| LIGNEE-SENTINEL | Lignée Sentinel | Gardien | Securix (DIEU-010) | 5 |
| LIGNEE-SCALA | Lignée Scala | Scoreur | Valura (DIEU-009) | 6 |
| LIGNEE-GENESIS | Lignée Genesis | Reproducteur | Genitor (DIEU-012) | 3 |

---

## Règles de filiation communes

1. Un robot doit atteindre le niveau de maîtrise requis avant de pouvoir initier une reproduction.
2. Le robot descendant hérite d'une fraction des scores du parent (variable selon la lignée).
3. La création d'un robot requiert l'accord implicite du dieu tuteur de la lignée.
4. Tout dépassement de quota de lignée déclenche une alerte auprès du dieu Genitor.
5. Un robot ne peut appartenir qu'à **une seule lignée** à la fois.

## Cycle de vie d'un robot

```
[Création] → [Formation académique] → [Activité] → [Retraite] → [Archivage]
```

- **Création** : le robot est instancié avec les scores initiaux de sa classe.
- **Formation** : inscription dans une académie, progression par niveaux.
- **Activité** : exécution des tâches, accumulation des scores.
- **Retraite** : conditions de retraite atteintes (âge en cycles ou critères de performance).
- **Archivage** : le robot est désactivé et ses preuves sont conservées.
