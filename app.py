
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import base64
import os
from database import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM avisos ORDER BY data_criacao DESC")
    avisos = c.fetchall()
    conn.close()
    return render_template('index.html', avisos=avisos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    data_criacao = datetime.now()

    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO avisos (titulo, descricao, data_criacao) VALUES (%s, %s, %s)",
              (titulo, descricao, data_criacao))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/capturar', methods=['GET', 'POST'])
def capturar():
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

        # Salvar imagem
        os.makedirs('dataset', exist_ok=True)
        with open(f'dataset/user_{user_id}_web.jpg', 'wb') as f:
            f.write(imagem_bin)

        return redirect('/painel')
    return render_template('captura.html')

@app.route('/painel')
def painel():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    c.execute("SELECT * FROM avisos ORDER BY data_criacao DESC")
    avisos = c.fetchall()
    conn.close()
    return render_template('painel.html', usuarios=usuarios, avisos=avisos)

if __name__ == '__main__':
    app.run(debug=True)
