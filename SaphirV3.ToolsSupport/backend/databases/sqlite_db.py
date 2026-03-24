import sqlite3

def get_sqlite_connection():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('db.sqlite')
    return conn

