from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sys
from pathlib import Path

# Ajuste de caminhos
raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(raiz))

from backend.database.config import obter_conexao
from bot.scrapers.mercado_livre import extrair_ml
from bot.scrapers.ml_search import buscar_links_games

app = FastAPI(title="Monitor API + Scraper")

# --- ROTA: PEGAR TODOS OS PRODUTOS (JSON) ---
@app.get("/produtos")
def listar_produtos():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos ORDER BY data_registro DESC")
    dados = cursor.fetchall()
    conn.close()
    
    for d in dados:
        d['preco_atual'] = float(d['preco_atual'])
        if d['preco_antigo']: d['preco_antigo'] = float(d['preco_antigo'])
    return dados

# --- ROTA: DISPARAR O SCAPER MANUALMENTE ---
@app.post("/scraper/scan-games")
def disparar_scraper(background_tasks: BackgroundTasks):
    """
    Aciona a varredura de games em segundo plano para não travar a API.
    """
    def tarefa_pesada():
        # Aqui chamamos a lógica que estava no seu engine.py
        links = buscar_links_games()
        conn = obter_conexao()
        cursor = conn.cursor()
        
        for link in links[:10]: # Limitando a 10 para teste rápido
            dados = extrair_ml(link)
            if dados:
                sql = "INSERT INTO produtos (nome, preco_atual, url_produto, url_imagem, loja) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE preco_atual = VALUES(preco_atual)"
                cursor.execute(sql, (dados['nome'], dados['preco'], dados['url'], dados['imagem'], dados['loja']))
                conn.commit()
        conn.close()

    background_tasks.add_task(tarefa_pesada)
    return {"status": "Processamento iniciado em segundo plano!", "msg": "Os produtos aparecerão no banco em instantes."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)