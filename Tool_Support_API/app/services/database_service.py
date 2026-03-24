import pyodbc
from ..utils.execution_requete_sql import executer_sql_instance
from ..utils.bd_tools import analyser_catalogues

def se_connecter_sql(server, database, user, password):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn


def avoir_version(serveur,username,password):
    query = "SELECT @@VERSION"
    retour = executer_sql_instance(serveur,username,password,query)
    return retour



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


def get_sql_server_catalogs(instance_sql, username, password, database="master"):
    
    query = """
    SELECT ROUTINE_NAME, ROUTINE_DEFINITION, SPECIFIC_CATALOG, ROUTINE_TYPE
    FROM INFORMATION_SCHEMA.ROUTINES
    WHERE ROUTINE_TYPE IN ('PROCEDURE','FUNCTION')
    """
    retour = executer_sql_instance(instance_sql,username,password,query)
    return retour




def verification_organisationId(server, username,password,database,tables):
    
    
    soucis = []
    for table in tables:
       
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                                f'SERVER={server};'
                                f'UID={username};'
                                f'PWD={password};'
                                f'DATABASE={database}')
        cursor = conn.cursor()
        cursor.execute(f"select  distinct(OrganizationId) from {table} where OrganizationId  !=  (SELECT OrganizationId FROM OrganizationBase WITH (NOLOCK))")
        resultats = cursor.fetchall()
        cursor.close()
        if(resultats):
            soucis.append(table)
            # print(table)
            
    return soucis

def entite_avec_organisation_id(server, username,password,database):
    
    
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                                f'SERVER={server};'
                                f'UID={username};'
                                f'PWD={password};'
                                f'DATABASE={database}')
    cursor = conn.cursor()
    cursor.execute("""
                         SELECT DISTINCT i.TABLE_NAME, i.TABLE_SCHEMA
                FROM INFORMATION_SCHEMA.COLUMNS i
                INNER JOIN Entity e WITH (NOLOCK)
                ON e.BaseTableName = i.TABLE_NAME
                WHERE COLUMN_NAME = 'OrganizationId'
                AND e.BaseTableName NOT IN ('OrganizationBase')
                order by i.TABLE_NAME asc; 
                    """)
    resultats = cursor.fetchall()
    cursor.close()
    
    return resultats


def liste_catalogues(server, username, password, database="master"):
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                                f'SERVER={server};'
                                f'UID={username};'
                                f'PWD={password};'
                                f'DATABASE={database}')
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT name FROM sys.databases
                        where name not in ('master','model','msdb','tempdb')
                    """)
        catalogs = cursor.fetchall()
        cursor.close()
        conn.close()
        return [catalog[0] for catalog in catalogs]
    
    except Exception as e:
        print(f"Erreur lors de la connexion ou de l'exécution de la requête : {e}")
        return []



def verification_catalogues_ps_function(instance_sql, username, password):
    
    query = """
            SELECT 
            ROUTINE_NAME, ROUTINE_DEFINITION, SPECIFIC_CATALOG, ROUTINE_TYPE
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE IN ('PROCEDURE','FUNCTION')
            """
    resultats = executer_sql_instance(instance_sql, username, password,query)
    
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
                    # print( proc.ROUTINE_NAME, proc.SPECIFIC_CATALOG, proc.ROUTINE_TYPE, cat)
    
    return procedures_et_function_list, ps, func


