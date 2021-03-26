# Drugs Data Pipeline [Appendix]

Ce répertoire contient les réponses aux questions du test.

**Question :**
Extraire depuis le json produit par la data pipeline le nom du journal qui mentionne le plus de médicaments différents
**Réponse :**
voir fichier [max_drugs_journal.py](max_drugs_journal.py)

**Question :** 
Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?
**Réponse :**
Les modifications à apporter au niveau du code :

- Modification du **connecteur de données** selon la source Big Data
- Soumettre le processing des données à un **moteur de calcul Spark** (via **SparkSubmitOperator**) -> car Airflow doit être utilisé comme orchestrateur de workflow et non comme un moteur de calcul.
- Utilisation de **base de données orientées graphes** pour ce type de use case, au lieu de PostgreSQL (Neo4J par exemple)

**Question :** Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?
**Réponse :**
Les modifications à apporter au niveau de l'infrastructure :

- Utisation d'une infrastructure **Big Data** pour **Stockage des données** (HDFS, solution Data Lake Cloud, ...)
- Utilisation d'un moteur de calcul distribué **Spark** pour le **processing** des données.
- Utilisation d'une **infrastructure robuste pour Airflow** (basée sur Kubernetes, les bases ont été réalisées dans ce projet) afin de gérer des charges plus importantes.

**SQL**
**Première partie du test**
Réponse dans [sql/select_chiffre_affaire.sql](sql/select_chiffre_affaire.sql)

**Deuxième partie du test**
Réponse dans [sql/select_ventes_meubles_deco.sql](sql/select_ventes_meubles_deco.sql)