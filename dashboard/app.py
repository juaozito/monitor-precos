import streamlit as st
import pandas as pd
from backend.database.config import obter_conexao

# Configuração da Página
st.set_page_config(page_title="Monitor de Preços KaBuM!", layout="wide")

def carregar_dados():
    try:
        conn = obter_conexao()
        # Query para pegar os produtos mais recentes da KaBuM
        query = "SELECT nome, preco_atual, preco_antigo, url_produto, url_imagem, data_registro FROM produtos WHERE loja = 'KaBuM!' ORDER BY data_registro DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return pd.DataFrame()

# --- TÍTULO ---
st.title("🚀 Monitor de Ofertas: KaBuM!")
st.markdown("Acompanhamento de preços em tempo real.")

# Botão de atualização manual
if st.button('🔄 Atualizar Dados'):
    st.rerun()

df = carregar_dados()

if not df.empty:
    # --- MÉTRICAS GERAIS ---
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Total de Produtos", len(df))
    with col_m2:
        # Conta quantos produtos tiveram queda de preço
        promocoes = df[df['preco_atual'] < df['preco_antigo']].shape[0] if 'preco_antigo' in df else 0
        st.metric("Promoções Detectadas", promocoes)

    st.divider()

    # --- LISTAGEM DE PRODUTOS EM CARDS ---
    # Criamos uma grade de 4 colunas
    cols = st.columns(4)
    
    for i, row in df.iterrows():
        with cols[i % 4]:
            # Container visual para cada produto
            with st.container(border=True):
                # Imagem do Produto
                if row['url_imagem']:
                    st.image(row['url_imagem'], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150", caption="Sem Imagem")
                
                # Nome (limitado para não quebrar o layout)
                st.subheader(f"{row['nome'][:50]}...")
                
                # Lógica de Preço
                preco_atual = row['preco_atual']
                preco_antigo = row['preco_antigo']
                
                if preco_antigo and preco_atual < preco_antigo:
                    st.success(f"🔥 R$ {preco_atual:,.2f}")
                    st.caption(f"~~De: R$ {preco_antigo:,.2f}~~")
                else:
                    st.info(f"R$ {preco_atual:,.2f}")
                
                # Botão para abrir o site
                st.link_button("Ver na Loja", row['url_produto'])

else:
    st.warning("Nenhum produto encontrado no banco. Rode o scraper da KaBuM primeiro!")

# --- RODAPÉ ---
st.divider()
st.caption("Desenvolvido para monitoramento automático de Hardware.")