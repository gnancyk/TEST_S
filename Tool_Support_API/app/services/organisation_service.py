import pyodbc
import base64
import re
import socket
from ping3 import ping
from requests_ntlm import HttpNtlmAuth
from ldap3 import Server, Connection, ALL, NTLM
import requests
from ..utils.execution_requete_sql import executer_sql_instance

def get_all_organisations():
    """Récupère toutes les organisations depuis la base PackageManager"""
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=GSECRMS1T\\SQL2016;'
                              'DATABASE=PackageManager;'
                              'UID=sa;'
                              'PWD=Operating0')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Organisation ORDER BY Nom")
        resultats = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultats
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des organisations: {str(e)}")

def get_organisation_by_id(organisation_id):
    """Récupère une organisation par ID avec ses paramètres"""
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=GSECRMS1T\\SQL2016;'
                              'DATABASE=PackageManager;'
                              'UID=sa;'
                              'PWD=Operating0')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM Organisation WHERE OrganisationId = {organisation_id}")
        organisation = cursor.fetchall()

        cursor.execute(f"SELECT * FROM Parametre WHERE OrganisationId = {organisation_id}")
        parametres = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            'organisation': organisation[0] if organisation else None,
            'parametres': parametres
        }
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de l'organisation {organisation_id}: {str(e)}")

def check_user_in_ad(username, password):
    """Vérifie si un utilisateur existe dans Active Directory"""
    try:
        ad_server = "ldap://univers.ci:389"
        domain = "univers"

        server = Server(ad_server, get_info=ALL)
        user_dn = f"{domain}\\{username}"
        connection = Connection(server, user=user_dn, password=password, authentication=NTLM)

        if connection.bind():
            connection.unbind()
            return True
        else:
            connection.unbind()
            return False
    except Exception as e:
        return False

def check_crm_availability(crm_url, domaine, username, password):
    """Vérifie la disponibilité du frontend CRM"""
    try:
        auth = HttpNtlmAuth(f'{domaine}\\{username}', password)
        response = requests.get(crm_url, auth=auth, timeout=10)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def check_crm_function_general(instance_sql, database, username, password, lien_crm, serveur_batch):
    """Vérifie la fonction générale du CRM"""
    try:
        query = """
        SELECT w.Content, w.ModifiedOn, o.Name
        FROM WebResourceBase w
        INNER JOIN OwnerBase o ON w.ModifiedBy = o.OwnerId
        WHERE w.Name LIKE '%gs2e_fonctionsGenerales%'
        """

        resultats = executer_sql_instance(instance_sql, database, username, password, query)

        if not resultats:
            return {
                'message': f"Pas de ressource gs2e_fonctionsGenerales trouvée sur le catalogue {database}",
                'status': 400,
                'catalogue': database,
                'ModifiedBy': 'N/A',
                'ModifiedOn': 'N/A'
            }

        content = [column[0] for column in resultats]
        ModifiedOn = [column[1] for column in resultats]
        ModifiedBy = [column[2] for column in resultats]

        decoded_bytes = base64.b64decode(content[0])
        decoded_string = decoded_bytes.decode('utf-8')

        debut = "//#region Parametres"
        fin = " //Url web service de requetage"
        portion = decoded_string[decoded_string.find(debut) + len(debut):decoded_string.find(fin)]

        debut_catalogue = "var nomBaseDeDonnees = \""
        fin_catalogue = ".dbo."
        catalogue = portion[portion.find(debut_catalogue) + len(debut_catalogue):portion.find(fin_catalogue)]

        bd = {'message': '', 'status': False}
        lien = {'message': '', 'status': False}
        service = {'message': '', 'status': False}

        if catalogue != database:
            bd['message'] = f"Le catalogue {catalogue} dans la fonction générale n'est pas correct à {database}"
            bd['status'] = False
        else:
            bd['message'] = "Catalogue : OK"
            bd['status'] = True

        if (lien_crm + '/').lower() not in portion.lower():
            lien['message'] = f"Le lien CRM dans la fonction générale n'est pas conforme au paramètre du Help : {lien_crm}"
            lien['status'] = False
        else:
            lien['message'] = "Lien CRM : OK"
            lien['status'] = True

        if serveur_batch.lower() not in portion.lower():
            service['message'] = f"Merci de vérifier le lien du service ExecutionPS; serveur batch : {serveur_batch}"
            service['status'] = False
        else:
            service['message'] = 'Lien du service ExecutionPs semble être bon'
            service['status'] = True

        message = ''
        if bd['status']:
            message += "Le catalogue semble être correct, "
        else:
            message += "Le catalogue semble être incorrect, "

        if lien['status']:
            message += "Le lien CRM semble être correct"
        else:
            message += "Le lien CRM semble être incorrect"

        if service['status']:
            message += ", le lien du service semble être correct"
        else:
            message += ", le lien du service semble être incorrect"

        return {
            'bd': bd,
            'crm': lien,
            'service': service,
            'portion': portion,
            'status': 200,
            'catalogue': catalogue,
            'message': message,
            'ModifiedBy': ModifiedBy,
            'ModifiedOn': ModifiedOn
        }
    except Exception as e:
        return {
            'message': f"Erreur lors de l'analyse de la fonction générale: {str(e)}",
            'status': 500,
            'catalogue': database,
            'ModifiedBy': 'N/A',
            'ModifiedOn': 'N/A'
        }

def check_sql_server_availability(instance_sql, username, password):
    """Vérifie la disponibilité du serveur SQL et récupère la version"""
    try:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={instance_sql};UID={username};PWD={password}'

        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return True, version
    except pyodbc.Error as e:
        return False, 'N/A'

def get_windows_services(server, role, username, password):
    """Récupère les services Windows selon le rôle"""
    from ..utils.powershell_scripting import execution_powershell_hote_distant

    services = []

    if role == 'batch':
        liste_services = [
            "SAPHIRV3 - ClotureCaisseNMPFWinServ",
            "SAPHIRV3 - Compensation Automatique",
            "SAPHIRV3 - Comptabilisation",
            "SAPHIRV3 - Edition des factures",
            "SAPHIRV3 - Editions",
            "SAPHIRV3 - Editions des factures",
            "SAPHIRV3 - Facturation",
            "SAPHIRV3 - NMPFExtractionReglementsV2 Service",
            "SAPHIRV3 - NMPFExtractionService",
            "SAPHIRV3 - NMPFIntegrationFichierV2Service",
            "SAPHIRV3 - Planification",
            "SAPHIRV3 - Service de Reglement NMPF",
            "SAPHIRV3 - Service Windows De CompensationAuto",
            "SAPHIRV3 - Service Windows de PEPT",
            "SAPHIRV3 - Service Windows De Prelevement",
            "SAPHIRV3 - Service Windows De Recouvrement",
            "SAPHIRV3 - Service Windows De Ventilation",
            "SAPHIRV3 - Service Windows FileAttente",
            "SAPHIRV3 - Service Windows HR-Access",
            "SAPHIRV3 - Service Windows NMPFReglementAPI",
            "SAPHIRV3 - Service Windows SYGES"
        ]

        for service in liste_services:
            query = f"Get-Service | Where-Object {{ $_.Name -like '*{service}*' }} | Select-Object Status"
            state = execution_powershell_hote_distant(server, username, password, query)
            services.append({
                'service': service,
                'status': state
            })

    elif role == 'backend':
        liste_services = [
            {
                'name': "MSCRMAsyncService",
                'display_name': 'Service de traitement asynchrone Microsoft Dynamics CRM',
                'description': "Gère le traitement des événements asynchrones en attente"
            },
            {
                'name': "MSCRMAsyncService$maintenance",
                'display_name': 'Service de traitement asynchrone Microsoft Dynamics CRM (maintenance)',
                'description': "Gère le traitement des événements asynchrones en attente"
            },
            {
                'name': "MSCRMSandboxService",
                'display_name': 'Service de traitement Bac à sable (sandbox) Microsoft Dynamics CRM',
                'description': "Gère le traitement des plugins isolés"
            }
        ]

        for serv in liste_services:
            service_name = serv['name']
            query = f"Get-Service | Where-Object {{ $_.Name -like '*{service_name}*' }} | Select-Object Status"
            state = execution_powershell_hote_distant(server, username, password, query)
            services.append({
                'service': serv,
                'status': state
            })

    elif role == 'bd':
        server = server.split("\\")[0]
        liste_services = [
            {
                'name': "MSSQLFDLauncher",
                'display_name': 'SQL Full-text Filter Daemon Launcher',
                'description': "Service to launch full-text filter daemon process"
            },
            {
                'name': "MSSQL",
                'display_name': 'SQL Server',
                'description': "Provides storage, processing and controlled access of data"
            },
            {
                'name': "SQLAgent",
                'display_name': 'SQL Server Agent',
                'description': "Executes jobs, monitors SQL Server, fires alerts"
            }
        ]

        for serv in liste_services:
            service_name = serv['name']
            query = f"Get-Service | Where-Object {{ $_.Name -like '*{service_name}*' }} | Select-Object Status"
            state = execution_powershell_hote_distant(server, username, password, query)
            services.append({
                'service': serv,
                'status': state
            })

    return services

def get_sql_catalogs(instance_sql, username, password):
    """Récupère les catalogues SQL Server"""
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={instance_sql};'
                              f'UID={username};'
                              f'PWD={password};'
                              f'DATABASE=master')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        catalogs = cursor.fetchall()
        cursor.close()
        conn.close()
        return [catalog[0] for catalog in catalogs]
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des catalogues: {str(e)}")

def get_sql_triggers(instance_sql, database, username, password):
    """Récupère les triggers SQL Server"""
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={instance_sql};'
                              f'UID={username};'
                              f'PWD={password};'
                              f'DATABASE={database}')
        cursor = conn.cursor()
        cursor.execute("SELECT name, parent_id, type_desc, is_disabled FROM sys.triggers")
        triggers = cursor.fetchall()
        cursor.close()
        conn.close()

        liste_triggers = []
        for elt in triggers:
            liste_triggers.append({
                'nom': elt[0],
                'status': 'Activé' if not elt[3] else 'Désactivé'
            })

        return liste_triggers
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des triggers: {str(e)}")

def get_sql_organisation_id(instance_sql, database, username, password):
    """Vérifie les tables avec OrganizationId"""
    try:
        query = """
        SELECT DISTINCT i.TABLE_NAME, i.TABLE_SCHEMA
        FROM INFORMATION_SCHEMA.COLUMNS i
        INNER JOIN Entity e WITH (NOLOCK)
        ON e.BaseTableName = i.TABLE_NAME
        WHERE COLUMN_NAME = 'OrganizationId'
        AND e.BaseTableName NOT IN ('OrganizationBase')
        ORDER BY i.TABLE_NAME ASC;
        """

        resultats = executer_sql_instance(instance_sql, database, username, password, query)
        entities = [column[0] for column in resultats]

        soucis = []
        for table in entities:
            try:
                query_check = f"SELECT DISTINCT(OrganizationId) FROM {table} WHERE OrganizationId != (SELECT OrganizationId FROM OrganizationBase WITH (NOLOCK))"
                result = executer_sql_instance(instance_sql, database, username, password, query_check)
                if result:
                    soucis.append(table)
            except:
                continue

        return soucis
    except Exception as e:
        raise Exception(f"Erreur lors de la vérification OrganizationId: {str(e)}")

def get_sql_ps_functions(instance_sql, database, username, password):
    """Récupère les procédures et fonctions SQL"""
    try:
        query = """
        SELECT ROUTINE_NAME, ROUTINE_DEFINITION, SPECIFIC_CATALOG, ROUTINE_TYPE
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE ROUTINE_TYPE IN ('PROCEDURE','FUNCTION')
        """

        procedures = executer_sql_instance(instance_sql, database, username, password, query)

        procedures_list = []
        for proc in procedures:
            procedures_list.append({
                'source': proc.SPECIFIC_CATALOG,
                'nom': proc.ROUTINE_NAME,
                'type': proc.ROUTINE_TYPE
            })

        liste_func = [p for p in procedures_list if p['type'] == 'FUNCTION']
        liste_ps = [p for p in procedures_list if p['type'] == 'PROCEDURE']

        return {
            'ps': len(liste_ps),
            'fonction': len(liste_func),
            'liste_ps': liste_ps,
            'liste_fonction': liste_func
        }
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des procédures/fonctions: {str(e)}")