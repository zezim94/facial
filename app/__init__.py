
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from db import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "default")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    from .views import main
    app.register_blueprint(main)
    return app
