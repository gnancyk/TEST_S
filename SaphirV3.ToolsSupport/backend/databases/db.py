import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password):
        """
        Initialise la connexion à la base de données avec les paramètres fournis.
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Se connecte à la base de données SQL Server en utilisant pyodbc.
        """
        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password}'
        )

        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            # print("Connexion réussie à la base de données !")
        except Exception as e:
            print("Erreur de connexion :", e)
# 
    def fetch_as_dict(self):
        """Transforme les résultats de la requête en dictionnaires."""
        columns = [column[0] for column in self.cursor.description]  # Obtenir les noms des colonnes
        rows = self.cursor.fetchall()  # Récupérer toutes les lignes
        result = [dict(zip(columns, row)) for row in rows]  # Convertir chaque ligne en dictionnaire
        return result
    
    
    def execute_query(self, query, params=None):
        """
        Exécute une requête SQL, par exemple une requête SELECT.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            # return self.cursor.fetchall()
            return self.fetch_as_dict()
        except Exception as e:
            print("Erreur lors de la requête :", e)
            return None

    def insert_data(self, query, params):
        """
        Exécute une requête INSERT pour insérer des données dans la base.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()  # Validation de la transaction
            print("Données insérées avec succès.")
        except Exception as e:
            print("Erreur lors de l'insertion :", e)

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()