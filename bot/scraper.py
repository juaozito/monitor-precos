import requests
from bs4 import BeautifulSoup

def rastrear_preco():
    url_produto = "https://www.mercadolivre.com.br/apple-iphone-15-128-gb-preto/p/MLB27393220"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        print(f"Buscando informações no site...")
        resposta = requests.get(url_produto, headers=headers)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # 1. Título (com verificação)
        tag_titulo = sopa.find('h1', class_='ui-pdp-title')
        titulo = tag_titulo.text.strip() if tag_titulo else "Título não encontrado"

        # 2. Preço (Busca mais inteligente)
        # Procuramos o container principal do preço primeiro
        container_preco = sopa.find('span', class_='andes-money-amount__main-container')
        
        if container_preco:
            # Pegamos a parte inteira do preço
            valor = container_preco.find('span', class_='andes-money-amount__fraction').text
            print("-" * 30)
            print(f"Produto: {titulo}")
            print(f"Preço: R$ {valor}")
            print("-" * 30)
        else:
            print("Putz! Não consegui encontrar o preço. O Mercado Livre pode ter mudado o layout.")
            # Dica: salve o html para analisar o que o robô está vendo
            # with open("erro.html", "w", encoding='utf-8') as f: f.write(resposta.text)

    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    rastrear_preco()