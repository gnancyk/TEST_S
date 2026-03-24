import pyodbc

def executer_sql_instance(instance_sql, username, password,query, database="master"):
    conn = pyodbc.connect(
                            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                            f'SERVER={instance_sql};'
                            f'UID={username};'
                            f'PWD={password};'
                            f'DATABASE={database}'
                        )
    cursor = conn.cursor()

    cursor.execute(query)
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return resultats