from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SERVER_IP: str
    TIME_WINDOW_SECONDS: int

    # Agora o .env está dois níveis acima (../..), mas Pydantic é esperto
    # e o encontrará subindo a árvore de diretórios.
    # Para ser explícito, você poderia usar:
    # model_config = SettingsConfigDict(env_file="../../.env")
    # Mas o padrão de busca geralmente já resolve.
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()