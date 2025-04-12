
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import base64, os
import psycopg2
import os

def get_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

app = Flask(__name__)
app.secret_key = 'segredo_seguro_para_sessao'

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM administradores WHERE usuario = %s AND senha = %s", (usuario, senha))
        admin = c.fetchone()
        conn.close()
        if admin:
            session['admin'] = usuario
            return redirect('/painel')
        else:
            erro = "Usuário ou senha inválidos"
    return render_template("login.html", erro=erro)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

@app.route('/painel')
def painel():
    if 'admin' not in session:
        return redirect('/login')
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    c.execute("SELECT * FROM avisos ORDER BY data_criacao DESC")
    avisos = c.fetchall()
    conn.close()
    return render_template("painel.html", usuarios=usuarios, avisos=avisos)

@app.route('/capturar', methods=['GET', 'POST'])
def capturar():
    if 'admin' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nome = request.form['nome']
        imagem_data = request.form['imagem']
        if imagem_data.startswith('data:image'):
            imagem_data = imagem_data.split(',')[1]
        imagem_bin = base64.b64decode(imagem_data)
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (nome) VALUES (%s) RETURNING id", (nome,))
        user_id = c.fetchone()[0]
        conn.commit()
        conn.close()
        os.makedirs('dataset', exist_ok=True)
        with open(f'dataset/user_{user_id}_web.jpg', 'wb') as f:
            f.write(imagem_bin)
        return redirect('/painel')
    return render_template("captura.html")

@app.route('/excluir_usuario/<int:id>')
def excluir_usuario(id):
    if 'admin' not in session:
        return redirect('/login')
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/painel')

@app.route('/excluir_aviso/<int:id>')
def excluir_aviso(id):
    if 'admin' not in session:
        return redirect('/login')
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM avisos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/painel')

@app.route('/')
def index():
    if 'admin' not in session:
        return redirect('/login')
    return redirect('/painel')

if __name__ == '__main__':
    app.run(debug=True)
