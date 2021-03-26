# Drugs Data Pipeline [CI/CD]

## I. Description

Le répertoire cicd contient les **templates de CI/CD** (fichiers YAML principalement) qui permettent de **créer, tester et déployer** la solution dans **Google Cloud Platform** (GCP).

## II. Structure du répertoire

Ce répertoire est structuré ainsi :

    .

    ├──  build                  # Template Build dans Google Cloud Build
        ├── cloudbuild.yaml     # Fichier qui contient la déclaration des étapes de Build et de Deploy
    ├──  deploy                 # Templates de déploiement dans Google Kubernetes Engine (GKE)
        ├── kubernetes
            ├── namespace.yml   # Fichier de configuration du DAG
        ├── terraform           # Fonctions utilitaires génériques
            ├── *.tf            # Fichiers Terraform pour déployer l'infrastructure GKE
            ├── apply.sh        # Scripts Terraform pour l'automatisation de création des ressources GCP

## III. Architecture DevOps

Le schéma suivant illustre l'architecture DevOps de la solution :

![Architecture de déploiement](../img/devops-schema.PNG)

Ce schéma est décrit par le scénario ci-dessous :

1. Le développeur réalise un **push** dans une **branche** GitHub (dev, test, main)
2. Un **trigger** est déclenché dans **Cloud Build** qui va :
    - **Récupérer le code** depuis GitHub
    - **Construire une image Docker** pour Airflow
    - **Exécuter les tests** sur le container
    - **Push l'image** dans Container Registry
    - **Créer / Mettre à jour** le Cluster Kubernetes dans GKE (si besoin)
    - **Créer / Mettre à jour** la Helm Chart Airflow dans GKE
3. La mise à jour de la Helm Chart utilisera **l'image Docker Airflow** déployée précédemment dans Container Registry.

## IV. Mise en place

Afin de mettre en place la Pipeline de CI/CD, il faut suivre les étapes décrites ci-dessous.

### 1. Création d'un compte Google Cloud

La première étape est de **créer un compte** Google Cloud (ou utiliser un compte existant).
Pour créer il faut suivre les étapes décrites dans ce [```lien```](https://cloud.google.com/apigee/docs/hybrid/v1.1/precog-gcpaccount).

### 2. Création d'un projet

Il faut ensuite **créer un projet** dans GCP en suivant les étapes suivantes : [```lien```](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=fr&visit_id=637523311862389376-2913023992&rd=1).

### 3. Activation des services nécessaires

Pour le projet créé précedemment, il faut **activer les services** suivants :

- *Cloud Resource Manager API*
- *Compute Engine API*
- *Cloud Build API*
- *Kubernetes Engine API*

Pour activer un service, il faut suivre les étapes suivantes : [```lien```](https://cloud.google.com/service-usage/docs/enable-disable?hl=fr).

### 4. Création d'un Bucket dans Google Cloud Storage (GCS)

Un **Bucket GCS** est un espace de stockage d'objets dans Google Cloud.
Dans notre cas, le Bucket servira à **stocker l'état** (state) de **Terraform**, qui va servir de référence pour assurer la traçabilité des déploiements effectués.
Pour créer un Bucket dans GCP, il suffit de suivre les étapes suivantes : [```lien```](https://cloud.google.com/storage/docs/creating-buckets?hl=fr).``

### 5. Création d'un trigger dans Cloud Build

Afin de lancer les déploiements, il faut créer un **trigger** dans Cloud Build qui pointera sur le **référentiel GitHub**.

Voici un [lien](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers?hl=fr) qui explique comment créer un Trigger.

Au moment de la création du trigger, il faut spécifier la variable d'environnement ```TF_BUCKET_NAME``` qui a pour valeur le nom du Bucket GCS créé précédemment.

> **N.B. :** Les composants de déploiement étant variabilisés en fonction du nom de la branche, la création d'un seul trigger est suffisante. Cependant il faut restreindre les branches ciblées par Cloud Build à dev, test et main.

Après réalisation de ces étapes, le déploiement se fera de façon automatique dans GKE après chaque push dans les branches (dev, test, main).