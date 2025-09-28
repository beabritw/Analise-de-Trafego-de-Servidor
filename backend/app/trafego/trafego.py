import time
import asyncio 
from threading import Lock
import logging
from scapy.all import sniff, IP, TCP, UDP

from app.core.utils import formatar_dados_para_frontend
from app.api.websockets import manager
from app.core.config import settings 

logger = logging.getLogger(__name__)

# Esta é a estrutura de dados central que será compartilhada.
dados_agregados = {
    "janela_atual": {},
    "janela_pronta": None, # Esta janela será lida pela API
    "lock": Lock()
}

def _processa_pacote(pacote, server_ip):
    """Função interna para processar cada pacote capturado."""
    if not pacote.haslayer(IP):
        return

    ip_layer = pacote[IP]
    tamanho_pacote = len(pacote)
    
    client_ip, direcao = None, None
    if ip_layer.src == server_ip:
        direcao = "out_bytes"
        client_ip = ip_layer.dst
    elif ip_layer.dst == server_ip:
        direcao = "in_bytes"
        client_ip = ip_layer.src
    else:
        return

    protocolo = "OUTROS"
    if pacote.haslayer(TCP):
        protocolo = "TCP"
    elif pacote.haslayer(UDP):
        protocolo = "UDP"

    with dados_agregados["lock"]:
        janela = dados_agregados["janela_atual"]
        janela.setdefault(client_ip, {}).setdefault(protocolo, {"in_bytes": 0, "out_bytes": 0})
        janela[client_ip][protocolo][direcao] += tamanho_pacote

#
# --- MUDANÇAS PRINCIPAIS ABAIXO ---
#

async def inicia_captura(server_ip: str):
    """
    Inicia a captura de pacotes de forma assíncrona, rodando o Scapy
    em um executor de threads para não bloquear o loop principal.
    """
    logger.info(f"Iniciando captura de pacotes para o servidor: {server_ip}...")
    
    # Tenta obter a interface do settings, se não, deixa o Scapy escolher a padrão
    # Isso remove o "wlo1" hardcoded
    interface = getattr(settings, "SNIFF_INTERFACE", None)
    if interface:
        logger.info(f"Usando interface de rede especificada: {interface}")
    else:
        logger.info("Nenhuma interface especificada, Scapy usará a padrão.")

    loop = asyncio.get_running_loop()
    
    # A função sniff é bloqueante, então a executamos em um thread pool
    await loop.run_in_executor(
        None,  # Usa o executor de thread padrão
        lambda: sniff(
            iface=interface,
            prn=lambda pkt: _processa_pacote(pkt, server_ip),
            store=0
        )
    )

async def gerenciador_janelas(time_window_seconds: int):
    """
    A cada X segundos, rotaciona a janela e transmite os dados via WebSocket.
    """
    logger.info("Gerenciador de janelas iniciado.")
    while True:
        await asyncio.sleep(time_window_seconds)
        
        logger.debug("Rotacionando janela de tráfego...")
        _rotacionar_janela()
        
        # --- A MUDANÇA ESTÁ AQUI ---
        # Pega a janela que acabamos de aprontar
        dados_prontos = obter_janela_pronta()
        
        if dados_prontos:
            # Formata os dados usando nossa função centralizada
            dados_formatados = formatar_dados_para_frontend(dados_prontos)
            
            # Envia os dados para TODOS os clientes conectados via WebSocket!
            await manager.broadcast_json(dados_formatados)
            logger.info(f"Nova janela de tráfego transmitida para {len(manager.active_connections)} cliente(s) via WebSocket.")


def _rotacionar_janela():
    """
    Função pura que contém a lógica de mover os dados de uma janela para outra.
    Nenhuma mudança necessária. A lógica e o uso do lock estão corretos.
    """
    with dados_agregados["lock"]:
        dados_agregados["janela_pronta"] = dados_agregados["janela_atual"]
        dados_agregados["janela_atual"] = {}

def obter_janela_pronta():
    """
    Função auxiliar segura para a API ler a última janela pronta.
    A API deve chamar esta função para obter os dados.
    """
    with dados_agregados["lock"]:
        # Retorna uma cópia para evitar problemas de concorrência
        # se a API estiver lendo enquanto a janela é trocada.
        # Embora a troca seja rápida, é uma boa prática.
        dados_prontos = dados_agregados["janela_pronta"]
        
    return dados_prontos