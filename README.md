#Project9

Développez une application Web en utilisant Django

## Objet.  
Se référer aux spécifications données sur la page https://openclassrooms.com/fr/paths/518/projects/837/assignment

## Installation

Pour installer l'application à partir de zéro.

- cloner les sources avec 

    git clone https://github.com/jsoques1/litreview

- se déplacer dans le sous répertoire de travail litreview

    cd litreview

- créer un environnement virtuel python, venv

    python -m venv venv

- activer un environnement virtuel python, venv

    venv\scripts\activate.bat

5. installer les paquets requis

    pip install -r requirements.txt

6. exécuter la migration des modèles (non nécessaire si le fichier DB db.sqlite3 n'est pas supprimé)

    python manage.py migrate

7. lancer le serveur

    python manage.py runserver

8. accéder à l'application LitReview servie via le WEB à l'URL :
9. 
    http://127.0.0.1:8000/


Comme requis un exemple de travail du fichier DB db.sqlite3 est livré et permet de démarrer sans effectuer la migration des modèles. 
Si vous souhaitez débuter avec une base de donnée vierge, il vous suffit de supprimer le fichier db.sqlite3 ; 
l'application en créera un nouveau à la première connexion.

Plusieurs comptes ont été créés :
user/us3r

toto/t0t0

titi/t1t1

tata/t@t@
...

9. flake8

     le résultat se trouve sous litreview/flake. 

      Pour le relancer, aller sous litreview et lancer dans l'environnement virtuel de python :
      flake8