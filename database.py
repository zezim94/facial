
import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Conexão com o banco de dados estabelecida com sucesso!")
        return connection
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None
