import requests
from bs4 import BeautifulSoup

def rastrear_preco():
    # 1. O LINK DO PRODUTO: Vamos usar um exemplo real
    url_produto = "https://www.mercadolivre.com.br/apple-iphone-15-128-gb-preto/p/MLB27393220"

    # 2. O DISFARCE (Headers): Isso diz ao site que somos um navegador humano
    # Sem isso, sites como Mercado Livre e Amazon bloqueiam o robô na hora.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        # 3. ACESSANDO O SITE: Enviamos o link e o nosso disfarce
        print(f"Buscando informações no site...")
        resposta = requests.get(url_produto, headers=headers)

        # 4. CRIANDO A "SOPA": Traduzindo o HTML para o Python
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # 5. EXTRAINDO O TÍTULO:
        # No Mercado Livre, o título geralmente fica em uma classe chamada 'ui-pdp-title'
        titulo = sopa.find('h1', class_='ui-pdp-title').text.strip()

        # 6. EXTRAINDO O PREÇO:
        # Aqui é onde a mágica acontece. Buscamos a parte inteira e os centavos.
        # Nota: As classes do Mercado Livre podem mudar, mas hoje são essas:
        preco_inteiro = sopa.find('span', class_='andes-money-amount__main-container').text.strip()

        print("-" * 30)
        print(f"Produto Encontrado: {titulo}")
        print(f"Preço Atual: {preco_inteiro}")
        print("-" * 30)

    except Exception as e:
        print(f"Ops! Ocorreu um erro ao tentar rastrear: {e}")

# Executa a função que criamos acima
if __name__ == "__main__":
    rastrear_preco()