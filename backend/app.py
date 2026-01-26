from flask import Flask, render_template
import os
import sys

# Caminho para o sistema encontrar a pasta 'bot'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from bot.scraper import rastrear_produto

# AQUI ESTÁ O SEGREDO: Avisamos ao Flask onde estão as pastas do frontend
# O '../' serve para sair da pasta backend e entrar na frontend
app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

@app.route('/')
def home():
    produto_info = rastrear_produto()
    return render_template('index.html', produto=produto_info)

if __name__ == "__main__":
    app.run(debug=True)