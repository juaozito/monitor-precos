import sys
import time
from pathlib import Path

# Resolve caminhos para importar os outros arquivos
raiz = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(raiz))

from backend.database.config import obter_conexao
from bot.scrapers.mercado_livre import extrair_ml
from bot.scrapers.ml_search import buscar_links_games

def monitorar_categoria_completa():
    # 1. Busca todos os links da primeira página de Games
    links = buscar_links_games()
    
    if not links:
        print("⚠️ Nenhum link encontrado para processar.")
        return

    # 2. Conecta ao banco uma única vez para ser mais rápido
    conn = obter_conexao()
    cursor = conn.cursor()

    print("🚀 Iniciando extração de detalhes...")

    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Analisando produto...")
        
        # Usa o scraper que você já validou para pegar Nome, Preço e Imagem
        dados = extrair_ml(link)
        
        if dados and dados['preco'] > 0:
            try:
                # Salva ou Atualiza no MySQL
                sql = """
                    INSERT INTO produtos (nome, preco_atual, url_produto, url_imagem, loja)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    preco_antigo = preco_atual, 
                    preco_atual = VALUES(preco_atual),
                    data_registro = CURRENT_TIMESTAMP
                """
                valores = (dados['nome'], dados['preco'], dados['url'], dados['imagem'], dados['loja'])
                cursor.execute(sql, valores)
                conn.commit()
                print(f"✅ Salvo: {dados['nome'][:40]}... | R$ {dados['preco']}")
            except Exception as e:
                print(f"❌ Erro ao salvar no banco: {e}")
        
        # PAUSA DE SEGURANÇA (2 segundos)
        # Isso impede que o Mercado Livre ache que você é um ataque e bloqueie seu IP
        time.sleep(2)

    conn.close()
    print("\n✨ Varredura concluída! Verifique seu Dashboard.")

if __name__ == "__main__":
    monitorar_categoria_completa()