
from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import db
from models import User
from camera import capture_face_encoding_and_image, match_face
import bcrypt
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://adm:bdunwFc6lvwAotvqDdKvRX4eDjHspy4a@dpg-cvskeq9r0fns73cbad20-a/facialdb_fj3i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
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
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for('login'))
        else:
            flash("Rosto não detectado. Tente novamente.", "danger")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user and match_face(user.encoding):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash("Rosto não reconhecido ou usuário inválido.", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = User.query.get(session.get('user_id'))
    if not user:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)

@app.route('/admin')
def admin():
    user = User.query.get(session.get('user_id'))
    if not user or user.role != 'admin':
        flash("Acesso negado.", "danger")
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
