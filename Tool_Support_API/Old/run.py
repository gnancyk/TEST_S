import requests
from requests_ntlm import HttpNtlmAuth 
from ldap3 import Server, Connection, ALL, NTLM
from flask import Flask, request,jsonify
import pyodbc
from ping3 import ping, verbose_ping
from flask_cors import CORS
import base64
import re
from requests.auth import HTTPBasicAuth
import subprocess
import socket

from databases.db import DatabaseConnection 

app = Flask(__name__)
CORS(app)

def server_available(hostname):
    reponse = ping(hostname)
    if reponse is not None:
        return True
    else:
        return False


def check_port_open(host, port=5986):
    try:
        # Tentative de connexion au port
        with socket.create_connection((host, port), timeout=5):
            print(f"Le port {port} est ouvert sur {host}.")
            return True
    except (socket.timeout, socket.error):
        print(f"Le port {port} est fermé sur {host}.")
        return False





def check_service_windows_status_remote_powershell(server, username, password,query):
    # Créer une chaîne d'informations d'identification PowerShell
    creds_command = f"$username = '{username}'; $password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential($username, $password)"
    
    
    ps_command = f"""
    $session = New-PSSession -ComputerName {server} -Credential $cred;
    Invoke-Command -Session $session -ScriptBlock {{ {query} }};
    Remove-PSSession -Session $session
    """

    # Exécuter la commande PowerShell avec la connexion distante
    result = subprocess.run(
        ["powershell", "-Command", creds_command + ps_command],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        output = result.stdout.strip()
        st = output[output.find("------  -------------- ----------") + len("------  -------------- ----------"):output.find(server)] 
        print (st)
        return st.strip()
    else:
        return 'N/A'
        


def get_sql_server_catalogs(server, username, password, database="master"):
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={server};'
                              f'UID={username};'
                              f'PWD={password};'
                              f'DATABASE={database}')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        catalogs = cursor.fetchall()
        cursor.close()
        conn.close()
        return [catalog[0] for catalog in catalogs]
    
    except Exception as e:
        print(f"Erreur lors de la connexion ou de l'exécution de la requête : {e}")
        return []

def avoir_version_crm(crm_url, domaine, username, password):
    
    
    web_api_url = f"{crm_url}/api/data/v8.0/"
    username = "Univers\\AdminSaphirV3PP"
    password = "$pecial@ccountpp02"

    # Authentification NTLM
    auth = HttpNtlmAuth(username, password)
    
    # Appel Web API
    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Test de connexion à l'API
    response = requests.get(web_api_url, headers=headers, auth=auth, verify=False)  # verify=False si tu as un certif self-signed
    if response.status_code == 200:
        print("Connexion à l'API OK")
        
        # Appel de la fonction RetrieveVersion
        version_url = f"{web_api_url}RetrieveVersion()"
        response2 = requests.get(version_url, headers=headers, auth=auth, verify=False)

        if response2.status_code == 200:
            version_info = response2.json()
            print("Version Dynamics CRM :", version_info.get('Version'))
            return version_info.get('Version')
        else:
            print("Erreur lors de la récupération de la version :", response2.status_code)
            return 'N/A'
    else:
        print("Erreur de connexion à l'API :", response.status_code)
        return 'N/A'
        
        

def check_service_status_remote_powershell(server, service_name, username, password):
    # Créer une chaîne d'informations d'identification PowerShell
    creds_command = f"$username = '{username}'; $password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential($username, $password)"

    ps_command = f"""
    $session = New-PSSession -ComputerName {server} -Credential $cred;
    Invoke-Command -Session $session -ScriptBlock {{ Get-Service | Where-Object {{ $_.Name -like '*{service_name}*' }}  | Select-Object Status }};
    Remove-PSSession -Session $session
    """

    # Exécuter la commande PowerShell avec la connexion distante
    result = subprocess.run(
        ["powershell", "-Command", creds_command + ps_command],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        output = result.stdout.strip()
        # print(len(output))
        # print(result.stdout.strip()[120:127])
        return output[120:127]  # L'état du service (Running, Stopped, etc.)
    else:
        print(f"Erreur lors de la récupération de l'état du service : {result.stderr.strip()}")
        return f"Erreur lors de la récupération de l'état du service : {result.stderr.strip()}"
    
    
    
def check_system_status_remote_powershell(server, username, password):
    # Créer une chaîne d'informations d'identification PowerShell
    creds_command = f"$username = '{username}'; $password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential($username, $password)"

    ps_command = f"""
    $session = New-PSSession -ComputerName {server} -Credential $cred;
    Invoke-Command -Session $session -ScriptBlock {{ systeminfo }};
    Remove-PSSession -Session $session
    """

    # Exécuter la commande PowerShell avec la connexion distante
    result = subprocess.run(
        ["powershell", "-Command", creds_command + ps_command],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        output = result.stdout.strip()
        # print(len(output))
        # print(result.stdout.strip()[120:127])
        return output  # L'état du service (Running, Stopped, etc.)
    else:
        print(f"Erreur lors de la récupération de l'état du service : {result.stderr.strip()}")
        return f"Erreur lors de la récupération de l'état du service : {result.stderr.strip()}"




def recuperer_ps_and_function(instance_sql,username,password,database):
    
    query = """
    SELECT ROUTINE_NAME, ROUTINE_DEFINITION, SPECIFIC_CATALOG, ROUTINE_TYPE
    FROM INFORMATION_SCHEMA.ROUTINES
    WHERE ROUTINE_TYPE IN ('PROCEDURE','FUNCTION')
    """
   
    procedures = executer_sql_instance(instance_sql, database, username, password,query)
    
    procedures_list = []
    for proc in procedures:
        procedures_list.append({
            'source':proc.SPECIFIC_CATALOG,
            'nom': proc.ROUTINE_NAME,
            'type': proc.ROUTINE_TYPE,
            # 'definition': proc.ROUTINE_DEFINITION
        })
    
    return procedures_list
    
def se_connecter_sql(server, database, user, password):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn

def executer_sql_instance(instance_sql, database, username, password,query):
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={instance_sql};'
                              f'UID={username};'
                              f'PWD={password};'
                              f'DATABASE={database}')
    cursor = conn.cursor()

    cursor.execute(query)
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return resultats

def analyser_catalogues(proc_definition):
    # Rechercher les occurrences de catalogues (ex : database.schema.table)
    catalogues_utilises = set()
    # catalogues_utilises = []
    
    # Chercher des patterns de catalogues typiques : base.schema.table
    # Cela peut varier en fonction de la convention utilisée dans ta base de données

    pattern = r'([a-zA-Z0-9_]+)\.([a-zA-Z]+)\.([a-zA-Z0-9_]+)'
    # pattern = r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)'
    matches = re.findall(pattern, proc_definition)
    
    for match in matches:
        base, schema, table = match
        # catalogues_utilises.add(f'{base}.{schema}')
        # catalogues_utilises.add({'base':f'{base}', 'table':table, 'schema':schema})
        catalogues_utilises.add(f'{base}')
    
    return catalogues_utilises



def verification_catalogues_ps_function(instance_sql, database, username, password):
    
    query = """
            SELECT 
            ROUTINE_NAME, ROUTINE_DEFINITION, SPECIFIC_CATALOG, ROUTINE_TYPE
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE IN ('PROCEDURE','FUNCTION')
            """
    resultats = executer_sql_instance(instance_sql, database, username, password,query)
    
    all_catalogues = get_sql_server_catalogs(instance_sql, username, password, database="master")
    all_catalogues.append('dbo')
    all_catalogues.append('A')
    all_catalogues.append('T')
    all_catalogues.append('AdventureWorks')
    
    func = []
    ps   = []
    
    procedures_et_function_list = []
    for proc in resultats:
        procedures_et_function_list.append({
            'source':proc.SPECIFIC_CATALOG,
            'nom': proc.ROUTINE_NAME,
            'definition': proc.ROUTINE_DEFINITION,
            'type': proc.ROUTINE_TYPE,
        })
        
        if type(proc.ROUTINE_DEFINITION) is str:
            catalogues = analyser_catalogues(proc.ROUTINE_DEFINITION)
        
        if catalogues:
            for cat in catalogues:
                 if cat not in all_catalogues:
                    if proc.ROUTINE_TYPE == 'PROCEDURE':
                        ps.append({
                            'source': proc.SPECIFIC_CATALOG,
                            'nom':proc.ROUTINE_NAME,
                            'catalogue_detecte':cat
                        })
                    elif  proc.ROUTINE_TYPE == 'FUNCTION':
                        func.append({
                            'source': proc.SPECIFIC_CATALOG,
                            'nom':proc.ROUTINE_NAME,
                            'catalogue_detecte':cat
                        })
                    print( proc.ROUTINE_NAME, proc.SPECIFIC_CATALOG, proc.ROUTINE_TYPE, cat)
    
    return procedures_et_function_list, ps, func

    
def execute_sql(query):
    my_request = DatabaseConnection(server="GSECRMS1T\SQL2016", 
                            database="PackageManager", 
                            username="sa", 
                            password="Operating0")
    my_request.connect()
    resultats = my_request.execute_query(f"{query}") 
    my_request.close()
    return  resultats

def entite_avec_organisation_id(server, username,password,database):
    query = f"""
                SELECT DISTINCT i.TABLE_NAME, i.TABLE_SCHEMA
                FROM INFORMATION_SCHEMA.COLUMNS i
                INNER JOIN Entity e WITH (NOLOCK)
                ON e.BaseTableName = i.TABLE_NAME
                WHERE COLUMN_NAME = 'OrganizationId'
                AND e.BaseTableName NOT IN ('OrganizationBase')
                order by i.TABLE_NAME asc; 
            """
    resultats = executer_sql_instance(server, database, username, password,query)
    
    return resultats

def verifier_trigger(server, username,password,database):
    
    query = f"""
                SELECT 
                    name,
                    parent_id,
                    type_desc,
                    is_disabled
                FROM 
                    sys.triggers 
            """
    return executer_sql_instance(server, database, username, password,query)
    
    # return resultats
    
    
    
    
def verification_organisationId(server, username,password,database,tables):
    
    
    soucis = []
 
    for table in tables:
        query = f"select  distinct(OrganizationId) from {table} where OrganizationId  !=  (SELECT OrganizationId FROM OrganizationBase WITH (NOLOCK))"
        resultat = executer_sql_instance(server, database, username, password,query)
        if(resultat):
            soucis.append(table)
            # print(table)
            
    return soucis
        

def check_web_ressource(server, username,password,database,lien_crm,serveur_batch,nom_ressource="gs2e_fonctionsGenerales"):
    
    # query = f"""
    # select Content from WebResourceBase
    # where name like '%{nom_ressource}%'
    # """
    query = f"""
    select w.Content, w.ModifiedOn, o.Name  from WebResourceBase w
    inner join OwnerBase o on w.ModifiedBy = o.OwnerId
    where w.Name like '%{nom_ressource}%'
    """
    resultats = executer_sql_instance(server, database, username, password,query)
    
    try:            
        
        content = [column[0] for column in resultats]
        ModifiedOn = [column[1] for column in resultats]
        ModifiedBy = [column[2] for column in resultats]
        
        # print(content[0])
        decoded_bytes = base64.b64decode(content[0])
        decoded_string = decoded_bytes.decode('utf-8')
        
        # print('Recupération de la fonction générale')
        
        debut = "//#region Parametres"
        fin = " //Url web service de requetage"
        portion = decoded_string[decoded_string.find(debut) + len(debut):decoded_string.find(fin)]
        
        # print('Portion de code à vérifier')
        # print(portion)
        
        
        debut_catalogue = "var nomBaseDeDonnees = \""
        fin_catalogue = ".dbo."
        catalogue = portion[portion.find(debut_catalogue) + len(debut_catalogue):portion.find(fin_catalogue)] 
        # print(catalogue)
        # print(parametre)
        # print('\n Récupération du catalogue: \n')
        bd = { 'message':'', 'status':False}
        lien = { 'message':'', 'status':False}
        service ={ 'message':'', 'status':False}
        
        # print('\n')
        if catalogue != database :
            # print (f"Le catalogue {catalogue} dans la fonction générale n'est pas correct à {database}")
            bd['message'] = f"Le catalogue {catalogue} dans la fonction générale n'est pas correct à {database}"
            bd['status'] = False,
        else:
            # print("Catalogue : OK")
            bd['message'] = "Catalogue : OK"
            bd['status'] = True,
            
            
        if (lien_crm+'/').lower()  not in portion.lower():
            # print (f"Le lien CRM dans la fonction générale n'est pas conforme au paramètre du Help : {lien_crm}")
            lien['message'] = f"Le lien CRM dans la fonction générale n'est pas conforme au paramètre du Help : {lien_crm}"
            lien['status'] = False,
        else:
            # print("Lien CRM : OK")
            lien['message'] = "Lien CRM : OK"
            lien['status'] = True,
            
        if serveur_batch.lower() not in portion.lower(): #parametre['serveur_batch'].lower() not in portion.lower()
            # print(f"Merci de vérifier le lien du service ExecutionPS; serveur batch : {serveur_batch}")
            service['message'] = f"Merci de vérifier le lien du service ExecutionPS; serveur batch : {serveur_batch}"
            service['status'] = False,
        else:
            # print('Lien du service ExecutionPs semble être bon')
            service['message'] = 'Lien du service ExecutionPs semble être bon'
            service['status'] = True,
        # print('\n')
        
        message = ''
        
        if bd['status'][0]:
            message = message + " Le catalogue semble être correct, "
        else:
            message =  message + " Le catalogue semble être incorrect, "
        
        if lien['status'][0] :
            message =   message + "Le lien CRM semble être correct"
        else:
            message =  message + "Le lein CRM semble être incorrect"
            
        if service['status'][0] :
            message =  message + "Le lien du service semble être correct"
        else:
            message =  message + " Le lien du service semble être incorrect"
        
        
        # if (bd['status'] == True and serveur_batch['status'] == True and lien['status'] == True):
        #     message = "Tous les paramètres sont apparamment corrects"
        # elif 
        return {'bd':bd,'crm':lien,'service':service, 'portion':portion,'status':200, 'catalogue':catalogue, 'message': message,'ModifiedBy':ModifiedBy,'ModifiedOn': ModifiedOn}
    except:  # noqa: E722
        # print (f"Pas de ressource {nom_ressource} trouvée sur le catalogue {database}")
        return {'message':f"Pas de ressource {nom_ressource} trouvée sur le catalogue {database}",'status':400,'catalogue':database,'ModifiedBy':'N/A','ModifiedOn': 'N/A'}
    # finally:
    #     conn.close()
        
        

@app.route('/organisations', methods=['GET'])
def get_utilisateurs():
    
    organistions = execute_sql(f"SELECT * FROM Organisation ORDER BY Nom")
    return jsonify({'status':200,'message':'','response':organistions})

# Lire une organisation par ID
@app.route('/organisation/<int:id>', methods=['GET'])
def get_organisation(id):
    try:
        organisation =  execute_sql(f"SELECT * FROM Organisation where OrganisationId = {id}")
        organisation_name = organisation[0]['Nom']
        parametres    =  execute_sql(f"SELECT * FROM Parametre where OrganisationId = {id}")
        if not parametres:
            return jsonify({'message': "Paramètre de l'organisation  non trouvée", "response":"","status":404}), 404
        return jsonify({'status':200,'message':f"Liste des paramètres de l'organisation {organisation_name}",'response':{'organisation':organisation,'parametres':parametres}})
    except Exception as e:
        return jsonify({'message': "Il y a eu une souci lors de la recuperation des paramètres", "response":"","status":404}), 404

@app.route('/organisation/<int:id>/verification/serveur', methods=['GET'])
def get_organisation_check_server(id):
    try:
        organisation =  execute_sql(f"SELECT * FROM Organisation where OrganisationId = {id}")
        organisation_name = organisation[0]['Nom']
        liste_parametres    =  execute_sql(f"SELECT * FROM Parametre where OrganisationId = {id}")
        # print(liste_parametres)
        if not liste_parametres:
            return jsonify({'message': "Paramètre de l'organisation  non trouvée", "response":"","status":404}), 404
        
        filtre_hostname_serveur = {key: value for key, value in liste_parametres[0].items() if 'serveur' in key.lower()}
        etat_serveur = []
        
        # print(filtre_hostname_serveur)
        for key, value in filtre_hostname_serveur.items():
            # print(hostname.key)
            # print(value != '[{}]'  and value != 'null')
            # print (value)
            winrm_port = check_port_open(host=value)
            winrm = False
                
            if(winrm_port):
                winrm = True
                
                
            if value is not None and value != 'null' and server_available(value) == True:
                # print(value)
                # print(value.split("\\")[0])
                systemInfo =  check_system_status_remote_powershell(value.split("\\")[0], liste_parametres[0]['login_crm'],liste_parametres[0]['password_crm'])

                os_name  = systemInfo[systemInfo.find("OS Name:") + len("OS Name: "):systemInfo.find("OS Version:")] 
                os_version  = systemInfo[systemInfo.find("OS Version:") + len("OS Version:"):systemInfo.find("OS Manufacturer:")] 
                # print(systemInfo)
                # etat_serveur.append({'serveur':value,'role':key,'etat':'Disponible'})
                etat_serveur.append({'serveur':value,'role':key,'etat':'En ligne','os_name':os_name,'os_version':os_version,'port_winrm':winrm})
            else:
                etat_serveur.append({'serveur':value,'role':key,'etat':'Pas disponible','os_name':'N/A','os_version':'N/A','port_winrm':winrm})
                
        # print(flitre_hostname_serveur)
            
        return jsonify({'r':filtre_hostname_serveur,'status':200,'message':f"Disponiblité des serveurs {organisation_name}",'response':etat_serveur})
    except Exception as e:
        return jsonify({'message': "Il y a eu une souci lors de la recuperation des paramètres", "response":"","status":404}), 404



@app.route('/organisation/compte-utilisateur', methods=['GET'])
def check_user_in_ad():
    ad_server = "ldap://univers.ci:389"  # Remplace par l'adresse de ton serveur AD
    domain = "univers"
    # print(request.args.get())
    
    username =  request.args.get('username')
    password =  request.args.get('password')
    
    # print(username, password)
    try:
        server = Server(ad_server, get_info=ALL)
        user_dn = f"{domain}\\{username}"  # Remplace "DOMAIN" par ton domaine AD
        connection = Connection(server, user=user_dn, password=password, authentication=NTLM)

        if connection.bind():
            return jsonify({'status':200,'message':"L'utilisateur est sur le domaine",'response':True})
        else:
            return jsonify({'status':400,'message':f"Échec de l'authentification pour {username}.",'response':''})
            # print(f"Échec de l'authentification pour {username}.", level='ERROR')

        connection.unbind()
    except Exception as e:
        return jsonify({'status':500,'message':f"Erreur lors de la tentative de connexion à AD : {e}",'response':False})
        # print(f"Erreur lors de la tentative de connexion à AD : {e}")


@app.route('/organisation/disponibilite/frontend-crm', methods=['GET'])
def check_crm_avaibility():
    username =  request.args.get('username')
    password =  request.args.get('password')
    crm_url  =  request.args.get('crm_url')    
    domain   = 'univers'
    
    
    try:
        # Utilisation de l'authentification NTLM pour accéder à Dynamics CRM
        auth = HttpNtlmAuth(f'{domain}\\{username}', password)
        response = requests.get(crm_url, auth=auth, timeout=10)
        if response.status_code == 200:
            version = avoir_version_crm(crm_url=crm_url,domaine=domain,username=username,password=password)
            print (version)
            return jsonify({'status':200,'message':f"Dynamics CRM est disponible à {crm_url}. l'utilisateur {username} s'est connecté avec succès",'response':True, 'version': version})
        else:
            return jsonify({'status':response.status_code,'message':"Impossible de se connecter au crm",'response':False})

            # print(f"Erreur : Code {response.status_code} reçu pour {crm_url}.")
            # print(f"Erreur : Code {response.status_code} reçu pour {url}.", level='ERROR')
    except requests.exceptions.RequestException as e:
        return jsonify({'status':response.status_code,'message':f"Erreur de connexion à {crm_url}: {e}",'response':False})
        # print(f"Erreur de connexion à {url}: {e}", level='ERROR')


@app.route('/organisation/disponibilite/crm/fonction_generale', methods=['GET'])
def check_function_general():
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql')  
    database  =  request.args.get('database')  
    lien_crm  =  request.args.get('lien_crm')  
    serveur_batch  =  request.args.get('serveur_batch')  
    
    analyse = check_web_ressource(server=instance_sql,database=database,username=username,password=password,lien_crm=lien_crm,serveur_batch=serveur_batch)
    print (analyse)
    return jsonify({'status':analyse['status'],'message':analyse['message'],'response':analyse})
    # return jsonify({'status':analyse['status'],'message':f"Analyse de la fonction générale sur  '{database}' est disponible.",'response':analyse})
    

@app.route('/organisation/disponibilite/serveur-sql', methods=['GET'])
def check_server_sql_avaibility():
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql')  
    database = 'master'
    
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={instance_sql};DATABASE={database};UID={username};PWD={password}'

    
    try:
        # Chaîne de connexion pour SQL Server avec l'instance spécifiée
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={instance_sql};UID={username};PWD={password}'
        
        # Essayer de se connecter à la base de données
        connection = pyodbc.connect(conn_str)
        
        # Si la connexion réussit, l'instance est disponible
        # print(f"L'instance '{instance_sql}' est disponible.")
        connection.close()
        
        
        
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Exécution de la requête pour obtenir la version de SQL Server
        cursor.execute("SELECT @@VERSION")
        
        # Récupération du résultat
        version = cursor.fetchone()[0]
        
        
       
        
        conn.close()
       
        return jsonify({'status':200,'message':f"L'instance '{instance_sql}' est disponible.",'response':True, 'version':version})
        # return True
    except pyodbc.Error as e:
        # Si la connexion échoue, afficher l'erreur
        # print(f"Échec de la connexion à l'instance '{instance_sql}'. Erreur : {e}")
        return jsonify({'status':400,'message':f"Échec de la connexion à l'instance '{instance_sql}'. Erreur : {e}",'response':False, 'version':'N/A'})

@app.route('/organisation/recuperation/service/windows', methods=['GET'])
def get_windows_service():
    username =  request.args.get('username')
    password =  request.args.get('password')
    server  =  request.args.get('server')  
    role  =  request.args.get('role')  
    
    print(server)
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
            "SAPHIRV3 - NMPFIntegrationFichierV2Service"
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
        print('Batch : \n')
        for service in liste_services:
            state = check_service_status_remote_powershell(server, service, username, password)
            # print(service)
            services.append({
                'service': service,
                'status':state
            })
    
    elif role == 'backend':
        liste_services = [
                            {
                                'name' :  "MSCRMAsyncService",
                                'display_name': 'Service de traitement asynchrone Microsoft Dynamics CRM',
                                'description':"Gère le traitement des événements asynchrones en attente"
                            },
                            {
                                'name' :  "MSCRMAsyncService$maintenance",
                                'display_name': 'Service de traitement asynchrone Microsoft Dynamics CRM (maintenance)',
                                'description': "Gère le traitement des événements asynchrones en attente"
                            },    
                            {
                                'name' :  "MSCRMSandboxService",
                                'display_name': 'Service de traitement Bac à sable (sandbox) Microsoft Dynamics CRM',
                                'description': "Gère le traitement des plugins isolés"
                            }
                        ]
        print('backend')
        for serv in liste_services:
            service_name = serv['name']
            query = f"Get-Service | Where-Object {{ $_.Name -like '*{service_name}*' }}  | Select-Object Status"
            state = check_service_windows_status_remote_powershell(server=server,  username=username, password= password, query=query)
            # print(service_name, serv,server)
            # print(service)
            services.append({
                'service': serv,
                'status':state
            })
    elif role == 'bd':
        print('bd')
        server = server.split("\\")[0]
        liste_services = [
                            {
                                'name' :  "MSSQLFDLauncher",
                                'display_name': 'SQL Full-text Filter Daemon Launcher ',
                                'description':"Service to launch full-text filter daemon process which will perform document filtering and word breaking for SQL Server full-text search. Disabling this service will make full-text search features of SQL Server unavailable."
                            },
                            {
                                'name' :  "MSSQL",
                                'display_name': 'SQL Server',
                                'description': "Provides storage, processing and controlled access of data, and rapid transaction processing."
                            },    
                            {
                                'name' :  "SQLAgent",
                                'display_name': 'SQL Server Agent',
                                'description': "Executes jobs, monitors SQL Server, fires alerts, and allows automation of some administrative tasks"
                            }
                        ]
        for serv in liste_services:
            service_name = serv['name']
            query = f"Get-Service | Where-Object {{ $_.Name -like '*{service_name}*' }}  | Select-Object  Status"
            state = check_service_windows_status_remote_powershell(server=server,  username=username, password= password, query=query)
            # print(service_name, serv,server)
            print(serv)
            services.append({
                'service': serv,
                'status':state
            })
    return jsonify({'status':200,'message':f"Liste des services sur {role} sur'{server}'",'response':services})     


@app.route('/organisation/disponibilite/serveur-sql/recuperation/catalogue', methods=['GET'])
def check_sql_server_catalogue():
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql') 
    catalogues = get_sql_server_catalogs(instance_sql, username, password, database="master")
    
    return jsonify({'status':200,'message':f"Liste des catalogues disponibles sur'{instance_sql}'",'response':catalogues})

@app.route('/organisation/disponibilite/serveur-sql/recuperation/triggers', methods=['GET'])
def check_sql_server_triggers():
    print('Trigger')
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql') 
    database  =  request.args.get('database') 
    print(instance_sql,username,database)
    
    
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                            f'SERVER={instance_sql};'
                            f'UID={username};'
                            f'PWD={password};'
                            f'DATABASE={database}')
    cursor = conn.cursor()
    cursor.execute("SELECT name, parent_id, type_desc, is_disabled FROM sys.triggers ")
    triggers = cursor.fetchall()
    cursor.close()
    conn.close()
    # return [catalog[0] for catalog in catalogs]
    
    liste_triggers = {}
    # triggers = verifier_trigger(server= instance_sql, username=username,password=password, database=database)[0]
    for elt in triggers:
        print (elt)
        liste_triggers['nom']= elt[0]
        liste_triggers['status']= elt[3]
         
    # triggers = {}
    print(liste_triggers)
    return jsonify({'status':200,'message':f"Liste des triggers disponibles sur'{instance_sql}'",'response':liste_triggers})

@app.route('/organisation/disponibilite/serveur-sql/recuperation/organisation-id', methods=['GET'])
def check_sql_organisationId():
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql') 
    database  =  request.args.get('database') 
    resultats = entite_avec_organisation_id(instance_sql, username, password, database)
    entities = [column[0] for column in resultats]
    retour = verification_organisationId(instance_sql, username, password, database,entities)
    # retour =  [column[0] for column in  verification_organisationId(instance_sql, username, password, database,entities)]
    # print (entities)
    print(retour)
    return jsonify({'status':200,'message':f"Liste des tables qui ont des soucis d\'organisationID sur'{instance_sql}'",'response':retour})

@app.route('/organisation/disponibilite/serveur-sql/recuperation/ps-functions', methods=['GET'])
def check_sql_server_list_ps():
    username =  request.args.get('username')
    password =  request.args.get('password')
    instance_sql  =  request.args.get('instance_sql') 
    database = request.args.get('database') 
    
    procedures_list =  recuperer_ps_and_function(instance_sql,username,password,database)
    # func = []
    # ps   = []
    # for elt in procedures_list:
    #     # print (elt)
    #     if elt['type'] == 'FUNCTION':
    #         func.append(elt)
    #     else:
    #         ps.append(elt)
    
    # print(len(ps))
    liste, ps, func = verification_catalogues_ps_function(instance_sql,database,username,password)
    liste_func = []
    liste_ps   = []
    for elt in procedures_list:
        # print (elt)
        if elt['type'] == 'FUNCTION':
            liste_func.append(elt)
        else:
            liste_ps.append(elt)
        
    # func =   {elt for elt in procedures_list if elt['type'] == 'FUNCTION'}
    # ps =   {elt for elt in procedures_list } # if item['type'] == 'PROCEDURE'}
    # func =   {item for item in procedures_list if item.type == 'FUNCTION'}
    # print(len(liste), len(ps), len(func))
    return jsonify({'status':200,'catalogue':database,'message':f"Liste des catalogues disponibles sur'{instance_sql}'",'response':{'ps':len(liste_ps),'fonction':len(liste_func),'liste_ps':liste_ps,'liste_fonction':liste_func ,'liste':liste, 'ps_probleme':ps, 'func_probleme':func}})
    

if __name__ == '__main__':
    app.run(debug=True)
