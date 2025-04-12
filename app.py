
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Event
from forms import LoginForm, RegisterForm, EventForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///calendar.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def calendar():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('calendar.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('calendar'))
        flash('Usuário ou senha inválidos.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('calendar'))
    return render_template('event_form.html', form=form, title='Novo Evento')

@app.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash('Acesso negado.')
        return redirect(url_for('calendar'))
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        db.session.commit()
        return redirect(url_for('calendar'))
    return render_template('event_form.html', form=form, title='Editar Evento')

@app.route('/event/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('calendar'))

if __name__ == '__main__':
    app.run(debug=True)
