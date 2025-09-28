def formatar_dados_para_frontend(dados_brutos: dict | None) -> list:
    """
    Converte o dicionário de agregação bruto para a lista de clientes
    que o frontend espera receber.
    """
    if not dados_brutos:
        return []

    resposta_formatada = []
    for ip, protocolos in dados_brutos.items():
        total_in = sum(p["in_bytes"] for p in protocolos.values())
        total_out = sum(p["out_bytes"] for p in protocolos.values())
        
        resposta_formatada.append({
            "client_ip": ip,
            "total_in": total_in,
            "total_out": total_out,
            "protocols": protocolos
        })
    return resposta_formatada