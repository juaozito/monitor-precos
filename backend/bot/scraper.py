import requests
from bs4 import BeautifulSoup

def rastrear_produto():
    # URL do produto monitorado
    url = "https://www.mercadolivre.com.br/apple-iphone-15-128-gb-preto/p/MLB27393220"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

    try:
        resposta = requests.get(url, headers=headers)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # --- 1. BUSCA O TÍTULO ---
        tag_titulo = sopa.find('h1', class_='ui-pdp-title')
        titulo = tag_titulo.text.strip() if tag_titulo else "Produto não encontrado"

        # --- 2. BUSCA A IMAGEM (Versão Blindada) ---
        # Tenta várias classes conhecidas do Mercado Livre
# --- 2. BUSCA A IMAGEM (Versão Ultra-Compatível) ---
        # Tenta capturar de diferentes lugares onde o ML guarda o link da foto
        img_tag = sopa.find('img', class_='ui-pdp-image') or \
                  sopa.find('img', class_='poly-component__picture') or \
                  sopa.find('img', {'data-zoom': True})
        
        link_imagem = ""
        if img_tag:
            # Pega o link real, mesmo que esteja "escondido" em atributos de zoom
            link_imagem = img_tag.get('data-zoom') or \
                          img_tag.get('src') or \
                          img_tag.get('data-src')

        # --- 3. BUSCA O PREÇO ---
        meta_preco = sopa.find('meta', itemprop='price')
        if meta_preco:
            preco = meta_preco['content']
        else:
            container_preco = sopa.find('span', class_='andes-money-amount__fraction')
            preco = container_preco.text.strip() if container_preco else "Não encontrado"

        return {
            "titulo": titulo, 
            "preco": preco, 
            "imagem": link_imagem
        }

    except Exception as e:
        print(f"Erro ao capturar dados: {e}")
        return {"titulo": "Erro de conexão", "preco": "---", "imagem": ""}