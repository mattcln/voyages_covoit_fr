# voyages_covoit_fr
Cet indicateur représente le nombre de trajets réalisés en covoiturage, incluant à la fois les trajets intermédiés par des plateformes et ceux réalisés de manière informelle.

# Contexte
Ce repos est créé dans le cadre d'un test technique pour un poste de Data Analyst au sein de l'[Ecolab](https://lannuaire.service-public.fr/gouvernement/b6441e59-9a83-4122-8c48-6e7e59ca6245).

# Objectif
Concevoir et implémenter un pipeline d'intégration d'un indicateur de voyages covoiturés en France.

# Plan 
Voici les étapes que je me donne à suivre : 
- Récupération des données jusqu'à juin 2022 (le format n'est plus le même avant)
- Exploration des données.
- Construire un script Python pour nettoyer les données et garder uniquement les quelques colonnes qui m'intéressent.
- Construire des tests confirmant le bon fonctionnement du script
- Construire un script Python d'output du nouvel indicateur (nombre de trajets par jour, en milliers)
- Construire des tests confirmant le bon fonctionnement du script

# Bonus
Si il me reste du temps :
- Visualisations
- Automatisations
- Récupération des données antérieures à Juin 2022 

Source : 
- [Trajets réalisés en covoiturage - Registre de Preuve de Covoiturage](https://www.data.gouv.fr/fr/datasets/trajets-realises-en-covoiturage-registre-de-preuve-de-covoiturage/#/resources)
- [Comprendre le covoiturage quotidien en France](https://observatoire.covoiturage.gouv.fr/observatoire/comprendre-covoiturage-quotidien/)
