# Bienvenue sur notre projet d'intelligence artificielle 

## IE-IG-B3-NPCI3-Projet

Ce projet consiste en la création d'un jeu de plateau à l'aide du framework Django. Notre jeu est codé en Python, Javascript, HTML et CSS. La base de donnée est PostgreSQL.

Le but est simple, capturez un maximum de cases possible en jouant contre un ami ou une IA! 

### Découpe de notre projet

Notre projet est découpé en trois applications, connection, le jeu et l'intelligence artificielle. <br>
- Premièrement, l'application "connection" reprend le model, les vues et les templates utiles à la connexion <br>
- Ensuite, l'application "game" permet de s'occuper de la logique relative à une partie <br>
- Pour finir, l'application "ai", gère toute la logique de cette dernière <br>
<br>
Vous pouvez également trouver le schéma de base de données dans les fichier au dessus. (Schema-BD.png)


### Notre Intelligence Artificielle 

Notre IA est l'implémentation d'une méthode de Reinforcement Learning : la Q-Function. Celle ci est entrainée à la volée lors de sa création par un utilisateur sur l'application web. <br>

### Prérequis

Python3 <br>

*pip3* <br>

Django <br>

psycopg2 <br>

Une base de données PostgreSQL. Celle ci était hébergée sur une image Docker sur l'environnement de production, ce qui vous donne accès aux fichiers de configurations directement dans ce repo. <br>

*L'installation des prérequis peut se faire avec pip :*
`pip install -r requirements.txt` ou `pip3`

## Installation

Clonez le projet dans le dossier de votre choix

`git clone https://github.com/TurboMachina/ProjetDjangoIA_2020.git`

Si vous utilisez votre propre base de données, vérifiez que postgreSQL soit lancé sur votre environnement et que les paramètres s'accordent avec ceux du fichier `~/ProjetIA/settings.py`

### Si vous souhaitez utiliser Docker, vérifiez qu'il soit bien présent sur votre machine puis dans un terminal naviguez vers le dossier cloné. Pour télécharger l'image docker la première fois lancez 

`docker-compose run web python manage.py migrate`

L'image sera téléchargée. Ensuite pour lancer le container docker :

`docker-compose run web python manage.py migrate`

`docker-compose build`

`docker-compose up`

Les paramètres du lancement se trouvent dans les fichiers `~/docker-compose.yml` et `~/dockerfile`

Les paramètres de PostgreSQL doivent être ajouté à côté de ces fichiers dans `db.env`, voici un exemple de configuration :


```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=projetia
POSTGRES_DB=postgres
```

### Si vous n'utilisez pas docker et votre base de données PostgreSQL nativement 

*Ici `python` représente le chemin de votre executable python3.exe*

Naviguez jusqu'au dossier racine du projet

`python manage.py makemigrations`

`python manage.py migrate`

Et pour lancer le serveur

`python manage.py runserver`

Via ces deux méthodes le site est accessible via `http://url/connection:port-spécifié`

Pour plus d'information sur la gestion des containers de docker et de PostgreSQL :

https://docs.docker.com/compose/

https://www.postgresql.org/docs/

---
Toute autre information relative au projet se trouve dans le dossier d'analyse. <br>

---

Un grand merci à nos professeurs Mme Christine Charlier et Mme Anne Smal pour leur aide tout au long de la conception de ce projet.

Antoine B, Jordan S & Antoine H <br>



























