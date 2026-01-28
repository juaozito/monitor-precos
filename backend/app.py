from flask import Flask, render_template, request # Adicionamos o 'request' aqui
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

@app.route('/', methods=['GET', 'POST'])
def home():
    url_padrao = 'https://www.mercadolivre.com.br/apple-iphone-15-128-gb-preto/p/MLB27393220'

    if request.method == 'POST':
        url_usuario = request.form.get('url_produto')
        if url_usuario:
            url_padrao = url_usuario

    produto_info = rastrear_produto(url_padrao)
    return render_template('index.html', produto=produto_info)

if __name__ == "__main__":
    app.run(debug=True)
