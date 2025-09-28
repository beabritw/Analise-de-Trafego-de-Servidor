from fastapi import WebSocket, WebSocketDisconnect
from .websockets import manager
from fastapi import APIRouter
from app.trafego.trafego import dados_agregados

# O 'APIRouter' funciona como um mini-aplicativo FastAPI, para organizar os endpoints
router = APIRouter()

@router.get("/traffic")
def get_traffic_data():
    """
    Endpoint que retorna os dados da última janela de tempo completa.
    """
    resposta_formatada = []
    with dados_agregados["lock"]:
        dados = dados_agregados["janela_pronta"]
        if not dados:
            return [] # Retorna uma lista vazia se não houver dados prontos
    
    # Formata os dados para um JSON amigável para o frontend
    for ip, protocolos in dados.items():
        total_in = sum(p["in_bytes"] for p in protocolos.values())
        total_out = sum(p["out_bytes"] for p in protocolos.values())
        
        resposta_formatada.append({
            "client_ip": ip,
            "total_in": total_in,
            "total_out": total_out,
            "protocols": protocolos
        })
    return resposta_formatada
    

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