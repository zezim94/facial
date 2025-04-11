
from flask import Flask, render_template, request, redirect
from datetime import datetime
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

if __name__ == '__main__':
    app.run(debug=True)
