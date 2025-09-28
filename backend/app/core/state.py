from threading import Lock

# Esta estrutura guardará os dados da última janela processada.
# Usamos um Lock para garantir que a escrita e a leitura sejam seguras entre threads/tasks.
latest_traffic_data = {"data": None, "timestamp": None}
data_lock = Lock()