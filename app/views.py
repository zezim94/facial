
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from db import db
from models import User
from camera import capture_face_encoding_and_image, match_face
import bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
        role = request.form.get('role') or 'user'
        encoding, face_image = capture_face_encoding_and_image()
        if encoding:
            user = User(name=name, email=email, password=password, role=role, encoding=encoding, image=face_image)
            db.session.add(user)
            db.session.commit()
            return "Usuário cadastrado com sucesso!"
        else:
            return "Rosto não detectado."
    return "Página de cadastro"

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user and match_face(user.encoding):
        return f"Login facial realizado com sucesso para {user.name}!"
    return "Falha no reconhecimento facial ou e-mail inválido."
