import time
from threading import Lock, Thread
from scapy.all import sniff, IP, TCP, UDP

# Esta é a estrutura de dados central que será compartilhada.
dados_agregados = {
    "janela_atual": {},
    "janela_pronta": None,
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

def inicia_captura(server_ip: str):
    """Inicia o processo de sniffing, usando uma função parcial para passar o server_ip."""
    print(f"Iniciando captura de pacotes para o servidor: {server_ip}...")
    # Usamos uma função anônima (lambda) para passar o IP para o callback
    sniff(iface="wlo1",prn=lambda pkt: _processa_pacote(pkt, server_ip), store=0)

def gerenciador_janelas(time_window_seconds: int):
    """A cada X segundos, chama a função de rotação de janelas."""
    print("Gerenciador de janelas iniciado.")
    while True:
        time.sleep(time_window_seconds)
        _rotacionar_janela()

def _rotacionar_janela():
    """
    Função pura que contém a lógica de mover os dados de uma janela para outra.
    É FACILMENTE TESTÁVEL de forma isolada.
    """
    with dados_agregados["lock"]:
        dados_agregados["janela_pronta"] = dados_agregados["janela_atual"]
        dados_agregados["janela_atual"] = {}