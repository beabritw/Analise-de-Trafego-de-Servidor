# 📊 Dashboard de Análise de Tráfego de Servidor em Tempo Real

Este projeto consiste em um sistema completo para captura, processamento e visualização de tráfego de rede de um servidor-alvo em tempo real. A aplicação utiliza Scapy para a captura de pacotes, FastAPI para a exposição dos dados via API RESTful e React para a construção de um dashboard web interativo.


## Features
- Captura de pacotes de/para um servidor alvo (via porta espelhada ou interface da máquina) com Scapy
- Processa e agrega os dados de tráfego (bytes de entrada/saída) em janelas de tempo de 5 segundos (configurável no `.env`)
- Agrupamento por cliente (endereço IP de origem/destino) e detalhamento por protocolo  
- API RESTful (`/api/traffic`) retorna dados prontos para o frontend com FastAPI 
- Visualização planejada (frontend com drill down de protocolos)  


## Tecnologias 

  * **Backend:**
      * **Linguagem:** Python 3.12+
      * **Captura de Rede:** Scapy
      * **Framework Web/API:** FastAPI
      * **Servidor ASGI:** Uvicorn
      * **Gerenciamento de Ambiente:** Venv
      * **Testes:** Pytest


### Pré-requisitos

O que você precisa ter instalado para rodar este projeto:
- Python 3.12 ou superior
- Privilégios de administrador (`sudo` no Linux ou Npcap no Windows) necessário para a captura de pacotes com Scapy
- Git


## Instalação

Siga o passo a passo abaixo. Todos os comandos devem ser executados no seu terminal.

### [Linux/macOS]

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/beabritw/Analise-de-Trafego-de-Servidor.git
    ```

2.  **Navegue até o diretório do backend:**

    ```bash
    cd Analise-de-Trafego-de-Servidor/backend
    ```

3.  **Crie e ative o ambiente virtual:**

    ```bash
    # Cria a pasta 'venv'
    python3 -m venv venv
    
    # Ativa o ambiente (Linux/macOS)
    source venv/bin/activate
    ```

4.  **Instale as dependências do projeto:**

    ```bash
    # Instala as bibliotecas de produção e desenvolvimento
    python3 -m pip install -r requirements.txt
    python3 -m pip install -r requirements-dev.txt
    ```

### [Windows]

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/beabritw/Analise-de-Trafego-de-Servidor.git
    ```

2.  **Navegue até o diretório do backend:**

    ```bash
    cd Analise-de-Trafego-de-Servidor/backend
    ```

3.  **Crie e ative o ambiente virtual:**

    ```bash
    # Cria a pasta 'venv'
    python -m venv venv
    
    # Ativa o ambiente (Linux/macOS)
    .\venv\Scripts\activate
    ```

4.  **Instale as dependências do projeto:**

    ```bash
    # Instala as bibliotecas de produção e desenvolvimento
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

    
## Configuração

A aplicação precisa saber qual endereço IP do servidor ela deve monitorar. Esta configuração é feita através de um arquivo de ambiente.


### [Linux/macOS]

1.  **Crie seu arquivo de configuração local** a partir do exemplo fornecido:

    ```bash
    # Este comando copia o template para o seu arquivo de configuração local
    cp .env.example .env
    ```

2.  **Abra o arquivo `.env`** com seu editor de código.

3.  **Altere o valor da variável `SERVER_IP`** para o endereço IP da sua máquina na sua rede local. Verifique seu IP com o comando ipconfig
4.  **e o valor da variável 'SNIFF_INTERFACE' para wlo1**.


### [Windows]

1.  **Crie seu arquivo de configuração local** a partir do exemplo fornecido:

    ```bash
    # Este comando copia o template para o seu arquivo de configuração local
    copy .env.example .env
    ```
2.  **Abra o arquivo `.env`** com seu editor de código.

3.  **Altere o valor da variável `SERVER_IP`** para o endereço IP da sua máquina na sua rede local. Verifique seu IP com o comando ipconfig
4.  **e o valor da variável 'SNIFF_INTERFACE' para Wi-Fi**.


5. Vá para o site oficial do [Npcap](https://npcap.com/#download) e baixe o instalador mais recente.
   Durante a instalação, certifique-se de marcar a opção **"Install Npcap in WinPcap API-compatible Mode"**


## Uso

Com o ambiente configurado, você pode agora executar o servidor e os testes.

### Rodando o Servidor Backend

O servidor web é iniciado com o Uvicorn. Como a captura de pacotes requer privilégios elevados, o comando deve ser executado com `sudo`.

#### [Linux/macOS]
```bash
# Estando na pasta 'backend/' e com o ambiente virtual (venv) ativo:
PYTHONPATH=. sudo venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

  * `PYTHONPATH=.` é necessário para garantir que o Python encontre os módulos do seu projeto corretamente.
  * O servidor estará disponível em `http://0.0.0.0:8000`.
  * A documentação interativa da API estará disponível em `http://127.0.0.1:8000/docs`.

#### [WIndows]

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


### Gerando Tráfego para Testes

Para ver o sistema em ação, você precisa gerar tráfego para o `SERVER_IP` que você configurou.

1.  **Abra um novo terminal** na mesma máquina.

#### [Linux/macOS]
2.  Inicie um servidor web simples na porta 8080:
    ```bash
    python3 -m http.server 8080
    ```
    
#### [Windows]
2.  Inicie um servidor web simples na porta 8080:
    ```bash
    python -m http.server 8080
    ```

3.  Use **outro dispositivo** (como seu celular) na mesma rede Wi-Fi e acesse `http://<SEU_SERVER_IP>:8080` no navegador.
4.  Consulte o endpoint `GET /api/traffic` na documentação (`/docs`) para ver os dados capturados.


### Execução dos Testes Automatizados

```bash
# Estando na pasta 'backend/' e com o ambiente virtual (venv) ativo:
python3 -m pytest -v #linux
python -m pytest -v #windows

```

## Autores

- Beatriz Brito - 2312130227
- Gabriel Alves - 2312082030

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.
