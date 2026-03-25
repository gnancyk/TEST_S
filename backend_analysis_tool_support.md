# Analyse Détaillée du Backend (Tool_Support_API)

Ce document explique en détail le fonctionnement du code de la nouvelle API Flask située dans le dossier `Tool_Support_API`. 

L'application suit une architecture moderne de type **Modèle-Vue-Contrôleur (MVC) étendu avec des Services**. Cette structure sépare bien les responsabilités pour que le code soit lisible et maintenable.

## 1. La Racine de l'Application

*   **[run.py](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/Tool_Support_API/run.py)** : C'est le point d'entrée. 
    *   Il importe la fonction [create_app()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/Tool_Support_API/app/__init__.py#7-24) pour fabriquer l'application Flask.
    *   Il crée les tables de base de données (SQLite) au démarrage (`db.create_all()`).
    *   Il lance le serveur web sur le port `5000` (`app.run(debug=True)`).
*   **[app/__init__.py](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/Tool_Support_API/app/__init__.py)** : C'est l'usine de l'application.
    *   Il charge la configuration.
    *   Il initialise CORS (pour autoriser le frontend Vue.js à lui parler).
    *   Il enregistre les **Blueprints** (les contrôleurs qui définissent les URLs de l'API comme `/users`, `/infra`, `/database`, etc.).
*   **`app/config.py`** : Définit les variables de configuration (comme `SQLALCHEMY_DATABASE_URI = 'sqlite:///mon_db.db'` et la clé secrète).

---

## 2. Les Contrôleurs (`app/controllers/`)
Les contrôleurs sont les points de contact de l'API. Ils reçoivent les requêtes HTTP (ex: POST, GET) du Frontend, extraient les données (les paramètres envoyés en JSON), appellent les **Services** pour faire le vrai travail, puis renvoient la réponse en format JSON.

*   **`infra_controller.py`** (`/infra`): 
    *   `/disponibilite/serveur` : Prend une liste de serveurs et vérifie s'ils répondent au ping en appelant `server_disponible`.
    *   `/caracteristiques/serveur` : Récupère les infos du système d'exploitation de chaque serveur (Version de l'OS, Uptime, CPU).
    *   `/performances/serveur` : Récupère les statistiques d'utilisation (RAM, Disque, Charge processeur).
    *   `/antivirus` : Vérifie l'état de l'antivirus (Windows Defender, McAfee, Kaspersky) sur les serveurs cibles via PowerShell.
*   **`database_controller.py`** (`/database`):
    *   `/disponibilite` : Vérifie que le serveur SQL Server est disponible et renvoie sa version exacte.
    *   `/statistique` : Compte le nombre de Procédures Stockées (PS), de Fonctions et de Catalogues dans les bases de données.
    *   `/verification/catalogue` : Vérifie que le code SQL des PS/Fonctions fait appel à des catalogues (bases) qui existent bien.
    *   `/verification/organisation_id` : Liste les tables où la valeur `OrganizationId` ne correspond pas à celle de la table d'organisation de base (très spécifique à Dynamics CRM).
*   **`central_param_controller.py`** (`/central_param`):
    *   Appelé pour discuter avec un service externe SOAP appelé "CentralisationParam".
    *   `/controle` : Vérifie qu'une URL donnée est bien un service SOAP valide.
    *   `/parametres` et `/parametre` : Interrogent le service SOAP (avec la bibliothèque `zeep`) pour récupérer les valeurs des paramètres CRM.
*   **`batch_controller.py`** (`/batch`):
    *   `/services/windows` : Liste les services Windows tournant sur une machine distante.
    *   `/services/windows/verification/config` : Lit directement le fichier `.config` (XML) des services batch Windows (ceux contenant "SAPHIRV3" dans leur nom) pour vérifier si leur endpoint `CentralisationParamEndPoint` est configuré vers la bonne machine.
*   **`user_controller.py`** (`/users`):
    *   C'est un contrôleur de test ou basique pour créer et lister des utilisateurs dans la petite base de données locale SQLite (`mon_db.db`). 

---

## 3. Les Services (`app/services/`)
Les services contiennent toute la **"Logique Métier"** et la "Mécanique". C'est ici que se trouvent les scripts PowerShell, les requêtes SQL, et les pings.

*   **`verification_infra_service.py`** : Le mécanicien du réseau et des serveurs Windows.
    *   `server_disponible(hostname)` : Utilise la bibliothèque `ping3` pour pinguer la machine.
    *   `verification_antivirus(...)` : Envoie une requête PowerShell distante (`Get-Service`) pour voir si les services McAfee, Kaspersky ou Defender sont actifs.
    *   `performances_serveur(...)` : Utilise `wmi` (Windows Management Instrumentation) et `pythoncom` pour se connecter au cœur de la machine distante et récupérer les disques (`Win32_LogicalDisk`), la RAM (`Win32_OperatingSystem`), le CPU (`Win32_Processor`), le réseau et le BIOS.
    *   `recuperation_os_information(...)` : Envoie la commande `systeminfo` en PowerShell et découpe le texte pour trouver la l'OS, la version, etc.
*   **`database_service.py`** : Le spécialiste de la Base de Données SQL Server.
    *   `se_connecter_sql(...)` : Crée une connexion avec `pyodbc` et le pilote `ODBC Driver 17 for SQL Server`.
    *   `recuperer_ps_and_function(...)` : Exécute des requêtes sur `INFORMATION_SCHEMA.ROUTINES` pour lister le code SQL des procédures stockées et fonctions.
    *   `verification_catalogues_ps_function(...)` : Utilise des expressions régulières (Regex) via la fonction `analyser_catalogues` pour trouver "database.schema.table" dans le texte des requêtes SQL et s'assurer que les bases appelées existent.
*   **`central_param_service.py`** : Le traducteur SOAP.
    *   Utilise `requests` pour valider que le lien répond à un WSDL.
    *   Utilise la bibliothèque `zeep` pour créer un client SOAP, parser le WSDL et invoquer la méthode distante `GetParameter()`.
*   **`verification_serveur_service.py`** : L'inspecteur des services Windows (SaphirV3).
    *   `service_windows(...)` : Utilise `wmi` (`Win32_Service`) pour lister tous les services de la machine. Si un service contient "SAPHIRV3" dans son nom, il récupère l'emplacement de son fichier `.exe` sur le disque dur, et déduit que son fichier de configuration s'appelle `.exe.config`. C'est grâce à ça que le contrôleur Batch peut aller lire le code source XML des configurations.
*   **`user_service.py`** : Basique, fait de simples ajouts (`db.session.add`) dans la table utilisateur.

---

## 4. Les Outils (`app/utils/` - supposés d'après les imports)
*   **`powershell_scripting.py`** : Exécute de manière invisible des arguments PowerShell sur d'autres serveurs du réseau.
*   **`extraction_texte.py`** : Fonctions servant à découper un long bloc de texte pour extraire la valeur entre deux mots-clés (utilisé pour lire le résultat de `systeminfo`).
*   **`bd_tools.py`** : Fonctions partagées pour analyser le code source SQL.

## Conclusion
Le **Backend Tool_Support_API** est une application spécialisée d'**Audit de Parc Informatique**. 
Lorsqu'elle reçoit une requête du site Web (Frontend Vue.js), elle contacte les serveurs Windows de ton architecture (Active Directory / CRM) en coulisses en utilisant du WMI, des requêtes PowerShell, des pings réseaux et du SQL (ODBC), pour s'assurer que les bases de données sont cohérentes, que les services tournent, que la RAM n'est pas saturée et que les URLs de fichiers de configuration pointent vers les bons endroits.
