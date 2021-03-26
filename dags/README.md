# Drugs Data Pipeline [DAGs]

## I. Description

Le répertoire DAGS contient l'implémentation du DAG Drugs Data Pipeline, ainsi que des modules génériques destinés à réutiliser pour d'autres cas d'usage.

## II. Structure du répertoire

Ce répertoire est structuré ainsi :

    .

    ├──  common                  # Modules communs réutilisables pour d'autres DAGs
        ├── plugins              # Modules Airflow génériques (Operators) destinés pour du reuse
        ├── utils                # Fonctions utilitaires génériques
    ├──  drugs_data_pipeline     # Code source de la Data Pipeline
        ├── config               # Fichier de configuration du DAG
        ├── data                 # Données input et output du DAG
        ├── sql                  # Requêtes SQL utilisées pour interagir avec PostgreSQL
        ├── tests                # Répertoire de tests (unitaires et intégration)
        ├── dag.py               # Entrypoint du DAG

## III. Structure du graphe (DAG)

Le DAG contient un ensemble de tâches regroupées par type sous forme de Task Groups. L'image ci-dessous représente une vue d'ensemble du DAG :

![DAG overview](../img/dag-overview.PNG)

Comme illustré, le DAG contient 3 tâches principales :
1- ```create_tables``` : Ce Task Group crée les tables qui seront par la suite alimentées par des fichiers CSV et JSON. Les sous-tâches de ce Task Group utilisent l'opérateur [***PostgresOperator***](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html)

2- ```insert_into_tables``` : Ce Task Group a pour objectif de récupérer les fichiers, de les traiter en fonction de leurs types (CSV ou JSON) et de stocker le résultat dans les tables créés précédemment. Les sous-tâches de ce Task Group utilisent l'opérateur custom disponible dans le répertoire common : [***FileToPostgresOperator***](common/plugins/postgres/operators/file_to_postgres.py)

3- ```export_drugs_json``` : Cette tâche récupère les données aggrégées à partir des tables créées précédemment, puis construit le graphe de liaisonqui sera finalement exporté  sous format JSON. Cette tâche utilise l'opérateur custom disponible dans le répertoire common : [***PostgresToJSONOperator***](common/plugins/postgres/operators/postgres_to_json.py)

Le graphe complet (en faisant apparaitre les sous-tâches) a la forme suivante :

![DAG subtasks](../img/dag-subtasks.PNG)

On peut constater à travers ce schéma les liens qui existent entre les sous-tâches des Task Groups.
En effet, si l'on prend comme exemple la table ```pubmed```, son alimentation se fait à travers 2 types de fichiers (JSON et CSV), d'où le lien de dépendance entre la sous-tâche **create_pubmed_table** et les 2 sous-tâches **insert_csv_into_pubmed_table** et **insert_json_into_pubmed_table**.

## IV. Schéma de sortie JSON

L'exécution du DAG renvoie un fichier JSON en sortie qui représente les liens entre chaque médicament, les publications qui le mentionnent ainsi que les journaux associés.
Le fichier est créé suivant les règles de gestion suivantes :

- Un médicament est considéré comme mentionné dans un article PubMed ou un essai clinique s’il est mentionné dans le titre de la publication.

- Un drug est considéré comme mentionné par un journal s’il est mentionné dans une publication émise par ce journal.

Le schéma du fichier JSON est donc le suivant :

```json
{
  "drug1": {
    "pubmed": [
        {
            "title": "title1",
            "date": "mm/jj/aaaa"
        },
        {
            "title": "title2",
            "date": "mm/jj/aaaa"
        }
    ],
    "clinical_trial": [
        {
            "title": "title3",
            "date": "mm/jj/aaaa"
        }
    ],
    "journals": [
        {
            "title": "title1",
            "date": "mm/jj/aaaa"
        },
        {
            "title": "title2",
            "date": "mm/jj/aaaa"
        },
        {
            "title": "title3",
            "date": "mm/jj/aaaa"
        }
    ]
  },
  "drug2": {...},
  ...
}
```

## V. Bonnes pratiques

- Tous les fichiers (code et configuration) sont **commentés en anglais**, soit par ligne ou par bloc d'instructions.

- Les classes, méthodes et fonctions implémentées sont munis de **docstrings** qui contiennent :

  - Une **description générale**
  - Un listing des **paramètres** en entrée et des **valeurs** en sortie
  - Une **description par paramètre** / valeur
  - Le **type de valeur** en sortie

- Le code suit les principales règles définies dans le guide [***PEP 8***](https://www.python.org/dev/peps/pep-0008/). ```Exemple :``` Les lignes ne dépassent pas 79 caractères.

- Le code et la configuration son **séparés** dans des fichiers distincts. Aucune configuration n'est incluse directement dans le code.
