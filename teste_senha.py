import os
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv("DB_PASSWORD")
print(f"Senha lida do .env: {senha}")