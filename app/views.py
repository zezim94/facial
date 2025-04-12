
from flask import Blueprint, request, session
from db import db
from models import User
from camera import capture_face_encoding_and_image, match_face
import bcrypt

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
    role = request.form.get('role', 'user')
    encoding, face_image = capture_face_encoding_and_image()
    if encoding:
        user = User(name=name, email=email, password=password, role=role, encoding=encoding, image=face_image)
        db.session.add(user)
        db.session.commit()
        return "Usuário cadastrado com sucesso!"
    return "Rosto não detectado."

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user and match_face(user.encoding):
        session['user_id'] = user.id
        return f"Login facial realizado com sucesso para {user.name}!"
    return "Falha no reconhecimento facial ou e-mail inválido."
