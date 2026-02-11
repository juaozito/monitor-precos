import sys
import os
import ssl
import cloudscraper
import urllib3
from bs4 import BeautifulSoup

# Ajuste de caminho para o banco
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.database.config import obter_conexao

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def rodar_monitor_kabum():
    # URL de Placas de Vídeo
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga"
    
    contexto = ssl.create_default_context()
    contexto.check_hostname = False
    contexto.verify_mode = ssl.CERT_NONE
    
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
        ssl_context=contexto
    )
    
    print(f"🚀 Iniciando varredura visual na KaBuM!...")
    
    try:
        response = scraper.get(url, timeout=30, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Na KaBuM, os produtos ficam dentro de tags <article> ou <main>
        # Vamos buscar por qualquer elemento que tenha 'productCard' na classe
        produtos_html = soup.find_all('article', class_=lambda x: x and 'productCard' in x)
        
        if not produtos_html:
            # Tentativa 2: Buscar por links que pareçam ser de produtos
            produtos_html = soup.select('a[class*="productLink"]')

        if not produtos_html:
            print("❌ Falha: O site bloqueou o acesso ou o layout mudou drasticamente.")
            # Salva o HTML para você ver o que está vindo (ajuda no debug)
            with open("debug_kabum.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("💡 Verifique o arquivo 'debug_kabum.html' para ver o que o Python está recebendo.")
            return

        conn = obter_conexao()
        cursor = conn.cursor()
        contador = 0

        for item in produtos_html:
            try:
                # Buscando Nome
                nome_tag = item.find('span', class_=lambda x: x and 'nameCard' in x)
                nome = nome_tag.text.strip() if nome_tag else None
                
                # Buscando Preço
                preco_tag = item.find('span', class_=lambda x: x and 'priceCard' in x)
                if not preco_tag: continue
                
                # Limpando o preço: "R$ 1.200,00" -> 1200.00
                preco_texto = preco_tag.text.replace('R$', '').replace('.', '').replace(',', '.').strip()
                preco_final = float(preco_texto)
                
                # Link e Imagem
                link_tag = item if item.name == 'a' else item.find('a', href=True)
                url_produto = "https://www.kabum.com.br" + link_tag['href']
                
                img_tag = item.find('img', class_=lambda x: x and 'imageCard' in x)
                img_url = img_tag.get('src') or img_tag.get('data-src') if img_tag else ""

                if nome and preco_final:
                    sql = """
                        INSERT INTO produtos (nome, preco_atual, url_produto, url_imagem, loja) 
                        VALUES (%s, %s, %s, %s, 'KaBuM!') 
                        ON DUPLICATE KEY UPDATE 
                        preco_antigo = preco_atual,
                        preco_atual = VALUES(preco_atual)
                    """
                    cursor.execute(sql, (nome, preco_final, url_produto, img_url))
                    contador += 1
            except Exception:
                continue

        conn.commit()
        conn.close()
        print(f"✅ SUCESSO! {contador} produtos encontrados e salvos.")

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    rodar_monitor_kabum()
    