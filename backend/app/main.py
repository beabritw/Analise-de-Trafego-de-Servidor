from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import contextlib

# Importa as partes que precisamos de outros módulos
from app.api.endpoints import router as api_router
from app.trafego.trafego import inicia_captura, gerenciador_janelas
from app.core.config import settings # Importa as configurações do .env

# Dicionário para manter referências às nossas threads
background_tasks = {}

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que roda na inicialização da aplicação
    print("Iniciando serviços de monitoramento em segundo plano...")
    
    # Cria e inicia a thread do gerenciador de janelas
    background_tasks["aggregator_thread"] = Thread(
        target=gerenciador_janelas, 
        args=(settings.TIME_WINDOW_SECONDS,), 
        daemon=True
    )
    
    # Cria e inicia a thread do sniffer de pacotes
    background_tasks["sniffer_thread"] = Thread(
        target=inicia_captura, 
        args=(settings.SERVER_IP,), 
        daemon=True
    )
    
    background_tasks["aggregator_thread"].start()
    background_tasks["sniffer_thread"].start()
    
    yield
    
    # Código que roda no encerramento (se necessário)
    print("Aplicação encerrando.")

# Cria a aplicação principal FastAPI e associa o 'lifespan'
app = FastAPI(title="Dashboard de Tráfego de Rede", version="1.0.0", lifespan=lifespan)

# Adiciona o middleware de CORS para permitir que o frontend se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o roteador da API no aplicativo principal
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Backend do Dashboard de Tráfego está operacional"}