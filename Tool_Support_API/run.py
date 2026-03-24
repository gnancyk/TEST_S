from app import create_app
from app.models import db

app = create_app()

# Initialiser la base de données au démarrage
with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès")

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask...")
    print("📍 API disponible sur http://127.0.0.1:5000")
    print("📍 Testez avec: curl http://localhost:5000/users/")
    app.run(debug=True)
