
from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='user')
    encoding = db.Column(db.PickleType, nullable=False)
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
