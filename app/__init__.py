
from flask import Flask
from db import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adm:bdunwFc6lvwAotvqDdKvRX4eDjHspy4a@dpg-cvskeq9r0fns73cbad20-a/facialdb_fj3i'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    from .views import main
    app.register_blueprint(main)

    return app
