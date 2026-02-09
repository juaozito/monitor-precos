import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza o .env na raiz do projeto
raiz = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=raiz / '.env')

def obter_conexao():
    """Retorna uma conexão ativa com o MySQL"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def inicializar_banco():
    try:
        # Conexão inicial para garantir que o banco existe
        conexao_inicial = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conexao_inicial.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
        conexao_inicial.close()

        # Conecta para criar a tabela
        db = obter_conexao()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                preco_atual DECIMAL(10, 2) NOT NULL,
                preco_antigo DECIMAL(10, 2),
                url_produto TEXT,
                url_imagem TEXT,
                loja VARCHAR(50),
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.close()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    if inicializar_banco():
        print("✅ Banco pronto para receber imports!")