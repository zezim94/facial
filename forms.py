
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Registrar')

class EventForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    start_time = DateTimeField('Início', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField('Fim', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Salvar')
