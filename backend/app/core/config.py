from pydantic_settings import BaseSettings, SettingsConfigDict

# Define quais variáveis de ambiente nosso programa precisa para funcionar
class Settings(BaseSettings):
    # O Pydantic garante que estas variáveis existam no .env e tenham o tipo certo.
    
    SERVER_IP: str # O endereço IP do servidor que queremos monitorar. Deve ser um texto (string).
    TIME_WINDOW_SECONDS: int # O intervalo de tempo em segundos para cada janela de agregação. Deve ser um número inteiro
    SNIFF_INTERFACE: str # O nome da interface de rede para a captura de pacotes (ex: "Wi-Fi" ou "wlo1")
    model_config = SettingsConfigDict(env_file=".env") # Esta linha instrui o Pydantic a procurar e ler as variáveis de um arquivo chamado ".env"

# Esta é a linha que efetivamente "liga" tudo.
# Ela cria uma instância da nossa classe `Settings`, fazendo com que o Pydantic
# leia o arquivo .env, valide os dados e os armazene no objeto 'settings'.
# Agora, podemos acessar as configurações em qualquer outro lugar do código
# de forma fácil, como: settings.SERVER_IP
settings = Settings()