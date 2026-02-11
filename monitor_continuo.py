import time
import subprocess
import sys

def rodar_bot():
    print(f"\n[{time.strftime('%H:%M:%S')}] 🔄 Iniciando atualização automática...")
    try:
        # Executa o engine.py como se você estivesse digitando no terminal
        subprocess.run([sys.executable, "backend/core/engine.py"], check=True)
        print(f"✅ Atualização concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro na automação: {e}")

if __name__ == "__main__":
    print("🤖 Bot de Monitoramento Contínuo Ativado!")
    print("Pressione CTRL+C para parar.")
    
    while True:
        rodar_bot()
        print("😴 Aguardando 1 hora para a próxima verificação...")
        time.sleep(3600) # 3600 segundos = 1 hora