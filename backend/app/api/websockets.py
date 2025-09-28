from fastapi import WebSocket
from typing import List
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Aceita uma nova conexão WebSocket e a adiciona à lista."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nova conexão WebSocket. Total de conexões: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove uma conexão WebSocket da lista."""
        self.active_connections.remove(websocket)
        logger.info(f"Conexão WebSocket fechada. Total de conexões: {len(self.active_connections)}")

    async def broadcast_json(self, data: dict):
        """Envia dados JSON para todas as conexões ativas."""
        if not self.active_connections:
            return # Não faz nada se não houver ninguém conectado

        # Prepara uma lista de tarefas de envio para executar em paralelo
        tasks = [connection.send_json(data) for connection in self.active_connections]
        # Executa todas as tarefas
        await asyncio.gather(*tasks)

# Criamos uma instância única do gerenciador que será usada em toda a aplicação
manager = ConnectionManager()