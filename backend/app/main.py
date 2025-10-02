from fastapi import FastAPI #para apis
from fastapi.middleware.cors import CORSMiddleware #libera o acesso do frontend (senão o navegador bloqueia).
import asyncio # gerencia tarefas assíncronas em paralelo (substitui threads)
import logging #para gerenciar logs

# Importa as partes necessárias de outros módulos
from app.api.endpoints import router as api_router
from app.trafego.trafego import inicia_captura, gerenciador_janelas
from app.core.config import settings  # Configurações carregadas do .env


# Configuração básica de logging para ativar logs no console ([info], [error])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Cria a aplicação principal FastAPI. a avriavel "app" é o nosso servidor
app = FastAPI(
    # Estes dados geram a documentação automática em /docs
    title="Dashboard de Tráfego de Rede",
    version="1.0.0",
    description="Backend para análise de tráfego em tempo real"
)

# Adiciona middleware de CORS (para permitir q o frontend consiga acessar a API no navegador sem bloquieos (cors policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # significa q qualquer origem pode acessar, obs: em produção, configure com domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todas as rotas definidas em endpoints.py ficam disponíveis em /api/....
app.include_router(api_router, prefix="/api")



# ---------- Ciclo de vida da aplicação ----------

# Define uma função que será executada uma única vez, assim que o servidor iniciar
@app.on_event("startup")
async def startup_event():
    """
    Função chamada automaticamente quando o backend é iniciado.
    Inicia captura de pacotes e agregação em segundo plano.
    """
    logger.info("Inicializando captura e agregação de tráfego...")

    try:
        # Cria tasks assíncronas para rodar em paralelo
        asyncio.create_task(gerenciador_janelas(settings.TIME_WINDOW_SECONDS)) #roda continuamente, agrupando pacotes por janela de tempo
        asyncio.create_task(inicia_captura(settings.SERVER_IP)) #escuta pacotes que envolvem o SERVER_IP
    except Exception as e:
        logger.error(f"Erro ao iniciar serviços de monitoramento: {e}")
        raise


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
