from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import json
import os
from app.utils.constants import LIWC_DICTIONARY_PATH

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    
    with open(LIWC_DICTIONARY_PATH) as f:
        app.config['LIWC_DICTIONARY'] = json.load(f)

    with app.app_context():
        from app.models import user, journal
        db.create_all()

        # Load LIWC dictionary
        with open(os.path.join(os.path.dirname(__file__), '../liwc_dictionary.json')) as f:
            app.config['LIWC_DICTIONARY'] = json.load(f)

        # Register blueprints
        from app.routes.auth import auth_bp
        from app.routes.journal import journal_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(journal_bp)

    return app
