import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from dotenv import load_dotenv
import urllib3

# 1. Desativa avisos de certificado (evita poluição no terminal devido ao verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. Configuração de Caminho para carregar o .env da raiz
# Caminho: bot/scrapers/mercado_livre.py -> sobe 3 níveis -> raiz/.env
raiz = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=raiz / '.env')

def extrair_ml(url):
    """Entra no Mercado Livre e extrai Nome, Preço, Imagem e Loja."""
    
    # O User-Agent disfarça o bot como um navegador real
    headers = {"User-Agent": os.getenv("USER_AGENT")}
    
    try:
        # verify=False ignora erros de SSL/Certificado comuns em redes locais
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Erro ao acessar site: Status {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- EXTRAÇÃO DO NOME ---
        # Tenta o seletor de catálogo OU o seletor de anúncio normal
        nome_tag = soup.find('h1', class_='ui-pdp-title') or soup.find('h1', class_='ui-item__title')
        nome = nome_tag.text.strip() if nome_tag else "Nome não encontrado"

        # --- EXTRAÇÃO DA IMAGEM ---
        # Busca a imagem principal da galeria
        img_tag = soup.find('img', class_='ui-pdp-image ui-pdp-gallery__figure__image')
        link_imagem = img_tag['src'] if img_tag else ""

        # --- EXTRAÇÃO DO PREÇO ---
        # O ML usa uma estrutura de meta-tags ou containers para o preço
        preco_final = 0.0
        preco_container = soup.find('span', class_='andes-money-amount__main-container')
        
        if preco_container:
            # Pega apenas o texto, remove 'R$' e espaços
            preco_texto = preco_container.text.replace('R$', '').replace('\xa0', '').strip()
            # Converte formato brasileiro (1.200,50) para float (1200.50)
            preco_limpo = preco_texto.replace('.', '').replace(',', '.')
            try:
                preco_final = float(preco_limpo)
            except ValueError:
                preco_final = 0.0

        return {
            "nome": nome,
            "preco": preco_final,
            "imagem": link_imagem,
            "url": url,
            "loja": "Mercado Livre"
        }

    except Exception as e:
        print(f"❌ Erro crítico na extração: {e}")
        return None

# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    # Link de um Mouse Gamer G305 (Anúncio oficial mais estável que o anterior)
    url_teste = "https://www.mercadolivre.com.br/mouse-gamer-sem-fio-logitech-g305-lightspeed-12000-dpi-preto/p/MLB12271351"
    
    print(f"🕵️ Iniciando coleta de teste...")
    resultado = extrair_ml(url_teste)
    
    if resultado and resultado['preco'] > 0:
        print(f"\n✅ SUCESSO NA EXTRAÇÃO!")
        print(f"📦 Produto: {resultado['nome']}")
        print(f"💰 Preço: R$ {resultado['preco']}")
        print(f"🖼️ Imagem: {resultado['imagem']}")
        print(f"🏪 Loja: {resultado['loja']}")
    else:
        print("\n❌ Falha ao capturar os dados. Verifique o link ou a conexão.")