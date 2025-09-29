from pathlib import Path
import sys

def configurar_ambiente():
    """
    Função principal para configurar o arquivo .env do servidor.
    Permite uma configuração manual ou padrão.
    """
    try:
        # Define o caminho para o arquivo .env no diretório pai do script atual.
        # Esta é uma forma robusta de encontrar o arquivo, não importa de onde o script seja executado.
        path_env = Path(__file__).resolve().parents[2] / ".env"
        print(f"O arquivo .env será criado ou modificado em: {path_env}\n")
    except IndexError:
        print("Erro: Não foi possível determinar o diretório pai. Certifique-se de que o script não está no diretório raiz.")
        sys.exit(1)
    # Loop infinito que só será quebrado quando uma opção válida for escolhida e executada com sucesso.
    # 'while True:' é a forma mais idiomática em Python para um loop infinito.
    while True:
        configuracao_servidor = input("Escolha uma das opções:\n 1. Configuração Manual\n 2. Configuração Padrão\nSua escolha: ")

        match configuracao_servidor:
            case "1":
                ip = input("Digite o IP do servidor: ")
                port = input("Digite a PORTA do servidor (ex: 8000): ")
                try:
                    with open(path_env, "w", encoding="utf-8") as f:
                        f.write(f"SERVER_IP={ip}\n")
                        # CORREÇÃO: Usando SERVER_PORT para compatibilidade com o Pydantic.
                        f.write(f"SERVER_PORT={port}\n")
                        f.write(f"TIME_WINDOW_SECONDS=5\n")
                        # NOVO: Adicionando o modo de captura (interface de rede).
                        f.write(f"MODO=wlo1\n") # CORREÇÃO: Adicionada quebra de linha.
                    print("\n✅ Arquivo .env configurado com sucesso!")
                    break
                except IOError as e:
                    print(f"\n❌ Erro ao escrever no arquivo: {e}")

            case "2":
                try:
                    with open(path_env, "w", encoding="utf-8") as f:
                        f.write("SERVER_IP=127.0.0.1\n")
                        f.write("SERVER_PORT=8000\n")
                        f.write("TIME_WINDOW_SECONDS=5\n")
                        # NOVO: Adicionando o modo de captura (loopback).
                        f.write("MODO=lo\n") # CORREÇÃO: Adicionada quebra de linha.
                    print("\n✅ Arquivo .env criado com a configuração padrão!")
                    break
                except IOError as e:
                    print(f"\n❌ Erro ao escrever no arquivo: {e}")
            case _:
                print("\nOpção inválida. Por favor, digite 1 ou 2.\n")

