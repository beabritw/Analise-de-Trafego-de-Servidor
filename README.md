# 📊 Dashboard de Análise de Tráfego de Servidor em Tempo Real

Este projeto consiste em um sistema completo para captura, processamento e visualização de tráfego de rede de um servidor-alvo em tempo real. A aplicação utiliza Scapy para a captura de pacotes, FastAPI para a exposição dos dados via API RESTful e React para a construção de um dashboard web interativo.

## Features

  * **Captura de Pacotes:** Escuta em uma interface de rede específica para capturar pacotes de e para um IP alvo.
  * **Agregação em Tempo Real:** Processa e agrega os dados de tráfego (bytes de entrada/saída) em janelas de tempo discretas de 5 segundos.
  * **Agrupamento por Cliente:** Os dados são agrupados por cliente (endereço IP de origem/destino).
  * **API RESTful:** Um backend robusto com FastAPI serve os dados agregados para qualquer cliente web.

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

  * Python 3.12 ou superior
  * Privilégios de `sudo` / administrador (necessário para a captura de pacotes com Scapy)

### Instalação [linux]

Siga o passo a passo abaixo. Todos os comandos devem ser executados no seu terminal.

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

### ⚙️ Configuração

A aplicação precisa saber qual endereço IP do servidor ela deve monitorar. Esta configuração é feita através de um arquivo de ambiente.

1.  **Crie seu arquivo de configuração local** a partir do exemplo fornecido:

    ```bash
    # Este comando copia o template para o seu arquivo de configuração local
    cp .env.example .env
    ```

2.  **Abra o arquivo `.env`** com seu editor de código.

3.  **Altere o valor da variável `SERVER_IP`** para o endereço IP da sua máquina na sua rede local.

    ```dotenv
    # Exemplo de como o .env deve ficar:
    SERVER_IP="000.000.0.00"
    TIME_WINDOW_SECONDS=5
    ```


### Instalação e configuração [windows]

   ```bash
    git clone https://github.com/beabritw/Analise-de-Trafego-de-Servidor.git
    cd Analise-de-Trafego-de-Servidor
    
    python -m venv venv
    
    .\venv\Scripts\activate

   ```
mude para a pasta backend

   ```bash
    cd backend
    pip install --upgrade pip
    pip install -r requirements.txt
    
    copy .env.example .env
    [edite o SERVER_IP com o ip da sua maquina, verifique com o comando ipconfig]
   ```

Vá para o site oficial do Npcap, baixe o instalador mais recente.
Durante a instalação, certifique-se de marcar a opção "Install Npcap in WinPcap API-compatible Mode"

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    ```

Teste no navegador (aparecera no terminal a endpoint)


## 💻 Uso

Com o ambiente configurado, você pode agora executar o servidor e os testes.

### Rodando o Servidor Backend

O servidor web é iniciado com o Uvicorn. Como a captura de pacotes requer privilégios elevados, o comando deve ser executado com `sudo`.

```bash
# Estando na pasta 'backend/' e com o ambiente virtual (venv) ativo:
PYTHONPATH=. sudo venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# No Windows, use:

```

  * `PYTHONPATH=.` é necessário para garantir que o Python encontre os módulos do seu projeto corretamente.
  * O servidor estará disponível em `http://0.0.0.0:8000`.
  * A documentação interativa da API estará disponível em `http://127.0.0.1:8000/docs`.

### Gerando Tráfego para Testes

Para ver o sistema em ação, você precisa gerar tráfego para o `SERVER_IP` que você configurou.

1.  **Abra um novo terminal** na mesma máquina.
2.  Inicie um servidor web simples na porta 8080:
    ```bash
    python3 -m http.server 8080
    ```
3.  Use **outro dispositivo** (como seu celular) na mesma rede Wi-Fi e acesse `http://<SEU_SERVER_IP>:8080` no navegador.
4.  Consulte o endpoint `GET /api/traffic` na documentação (`/docs`) para ver os dados capturados.

### Executando os Testes Automatizados

Para garantir a qualidade e a integridade da lógica de negócio, execute a suíte de testes com Pytest.

```bash
# Estando na pasta 'backend/' e com o ambiente virtual (venv) ativo:
python3 -m pytest -v
```

## 👥 Autores
- Beatriz Brito - 2312130227
- Gabriel Alves - 2312082030

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.
