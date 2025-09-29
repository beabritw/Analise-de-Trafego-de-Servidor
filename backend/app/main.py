import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Importa a função de configuração do nosso módulo de gerenciamento
from app.core.configurar_server import configurar_ambiente

# --- Bloco de Verificação e Carregamento da Configuração ---
# Este código executa ANTES de qualquer coisa do FastAPI.
path_env = Path(__file__).resolve().parents[1] / ".env"

# Se o arquivo .env não existir, o script de configuração interativa é chamado.
if not path_env.exists():
    print("Arquivo .env não encontrado. Iniciando configuração do servidor...")
    configurar_ambiente()
    print("\nConfiguração concluída. O servidor irá recarregar com as novas configurações.")
    # Encerra este processo. O Uvicorn com --reload irá reiniciar o servidor automaticamente.
    sys.exit(0)

# Se o .env já existe, suas variáveis são carregadas no ambiente.
load_dotenv(dotenv_path=path_env)

# Opcional: Imprime o conteúdo do .env para verificação
try:
    print("\n--- Conteúdo do arquivo .env carregado ---")
    with open(path_env, "r", encoding="utf-8") as f:
        print(f.read().strip())
    print("-----------------------------------------\n")
except IOError as e:
    print(f"Não foi possível ler o arquivo .env: {e}")
# -------------------------------------------------------------

# --- Imports da Aplicação FastAPI ---
# Estes imports só acontecem se a configuração já estiver carregada.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Importa as partes necessárias de outros módulos
from app.api.endpoints import router as api_router
from app.trafego.trafego import inicia_captura, gerenciador_janelas
from app.core.config import settings  # Configurações carregadas do .env


# Configuração básica de logging para ativar logs no console ([info], [error])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Cria a aplicação principal FastAPI
app = FastAPI(
    title="Dashboard de Tráfego de Rede",
    version="1.0.0",
    description="Backend para análise de tráfego em tempo real"
)

# Adiciona middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todas as rotas definidas em endpoints.py ficam disponíveis em /api/....
app.include_router(api_router, prefix="/api")

# ---------- Ciclo de vida da aplicação ----------
@app.on_event("startup")
async def startup_event():
    """
    Função chamada automaticamente quando o backend é iniciado.
    Inicia captura de pacotes e agregação em segundo plano.
    """
    logger.info("Inicializando captura e agregação de tráfego...")
    logger.info(f"Servidor configurado para rodar no IP: {settings.SERVER_IP}:{settings.SERVER_PORT}")
    logger.info(f"Modo de captura de interface: {settings.MODO}")
    logger.info("Para acessar a documentação da API, vá para http://127.0.0.1:8000/docs")

#Executa quando o servidor fecha
@app.on_event("shutdown")
async def shutdown_event():
    """
    Função chamada automaticamente no encerramento da aplicação.
    Pode ser expandida para liberar recursos.
    """
    logger.info("Encerrando aplicação...")

# ---------- Rotas auxiliares ----------
#util para testar rapidamente se backend está de pé (antes de usar /api/traffic)
@app.get("/", tags=["Root"])
def read_root():
    """
    Health-check: confirma se o backend está operacional.
    """
    return {"status": "Backend do Dashboard de Tráfego está operacional"}