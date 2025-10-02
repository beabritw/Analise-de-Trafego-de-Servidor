from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .websockets import manager
from app.trafego.trafego import obter_janela_pronta
from app.core.utils import formatar_dados_para_frontend

router = APIRouter()
    
@router.get("/traffic")
def get_traffic_data():
    """Endpoint que retorna os dados da última janela de tempo completa."""
    # Pega os dados brutos da última janela processada pelo módulo de tráfego
    dados_brutos = obter_janela_pronta()
    return formatar_dados_para_frontend(dados_brutos)


#endpoint websocket pro frontend se conectar e recebr atualizacoes em tempo real
@router.websocket("/ws/traffic")
async def websocket_endpoint(websocket: WebSocket):
    # Aceita e registra a nova conexão
    await manager.connect(websocket)
    try:
        # Mantém a conexão viva, esperando por mensagens (não faremos nada com elas)
        # ou até o cliente desconectar.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Quando o cliente desconecta (fecha a aba), removemos ele da lista.
        manager.disconnect(websocket)