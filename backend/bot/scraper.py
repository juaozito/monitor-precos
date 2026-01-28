import requests
from bs4 import BeautifulSoup
import urllib3

# Isso desativa o aviso chato de "conexão insegura" que vai aparecer no terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def extrair_mercado_livre(sopa):
    titulo = sopa.fin('h1', class_='ui-pdp-title')
    preco = sopa.find('meta', itemprop='price')
    img = sopa.find('img', class_='ui-pdp-image')
    return {
        "titulo": titulo.text.strip() if titulo else "N/A",
        "preco": preco['content'] if preco else "N/A",
        "imagem": img.get('data-zoom') or img.get('src') if img else ""
    }

def extrair_amazon(sopa):
    titulo = sopa.find('span', id='productTtile')
    preco_inteiro = sopa.find('span', class_='a-price-whole')
    preco_fracao = sopa,find('span', class_='a-price-fraction')
    img = sopa.find('img', id='landingImage')

    preco = f"{preco_inteiro.text.replace(',', '')}.`{preco-fracao.text}" if preco_inteiro else "N/A"
    return {
        "titulo": titulo.text.strip() if titulo else "N/A",
        "preco": preco,
        "imagem": img.get('src') if img else ""
    }


def rastrear_produto(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # ADICIONADO: verify=False para ignorar o erro de certificado SSL
        resposta = requests.get(url, headers=headers, timeout=10, verify=False)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        if "mercadolivre.com" in url:
            dados = extrair_mercado_livre(sopa)
        elif "amazon.com" in url:
            dados = extrair_amazon(sopa)
        else:
            return {"titulo": "Loja não suportada", "preco": "---", "imagem": ""}
        
        return dados
    except Exception as e:
        print(f"Erro: {e}")
        return {"titulo": "Erro ao buscar", "preco": "---", "imagem": ""}

       