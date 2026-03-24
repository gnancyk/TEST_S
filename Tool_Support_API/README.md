/app : Ce répertoire contient tous les composants de l'application Flask.

/controllers : Contient les fichiers pour les routes et les contrôleurs API. Chaque fichier gère un groupe de routes lié à un concept spécifique (par exemple, users.py, auth.py, etc.). Les contrôleurs reçoivent les requêtes et appellent les services nécessaires pour les traiter.

/services : Contient la logique métier. Les services sont responsables du traitement des données, de l'interaction avec la base de données, ou d'autres opérations complexes. Par exemple, tu pourrais avoir user_service.py ou auth_service.py.

/models : Contient les modèles pour interagir avec la base de données. Si tu utilises SQLAlchemy, tu y trouveras les classes qui définissent la structure de tes tables.

/schemas : Si tu utilises des bibliothèques comme Marshmallow ou Pydantic pour la validation et la sérialisation des données, les schémas y seront. Les schémas permettent de transformer les données (ex. convertir un objet en JSON et inversement).

/utils : Contient des fonctions utilitaires qui peuvent être réutilisées dans tout le projet (par exemple, des fonctions de gestion des erreurs, de manipulation de dates, etc.).

config.py : Ce fichier contient la configuration de ton application, comme la configuration de la base de données, les clés secrètes, etc.

**init**.py : Ce fichier permet de créer l'objet Flask, d’enregistrer les blueprints, et d’ajouter la configuration au projet.

/migrations : Si tu utilises une base de données relationnelle avec des migrations, ce répertoire contiendra les fichiers générés par Flask-Migrate.

/tests : Un dossier pour tes tests. Tu peux organiser les tests pour chaque partie de l'application (par exemple, tests des routes dans /tests/routes, tests des services dans /tests/services, etc.).

run.py : Le fichier principal pour démarrer l'application Flask. Il importe l'application et l'exécute.

requirements.txt : Contient toutes les dépendances de ton projet. Tu peux les générer avec la commande pip freeze > requirements.txt.

pip freeze > requirements.txt
pip install -r requirements.txt
