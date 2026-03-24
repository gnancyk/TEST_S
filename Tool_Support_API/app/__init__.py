from flask import Flask
from .models import db
from .controllers import user_controller, central_param_controller, infra_controller, database_controller, batch_controller
from .config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)

    # Initialisation de SQLAlchemy
    db.init_app(app)

    # Enregistrer les blueprints
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(central_param_controller.bp)
    app.register_blueprint(infra_controller.bp)
    app.register_blueprint(batch_controller.bp)
    app.register_blueprint(database_controller.bp)

    return app
