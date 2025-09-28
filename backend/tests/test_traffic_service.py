from app.trafego.trafego import _rotacionar_janela, dados_agregados
from fastapi.testclient import TestClient
from app.main import app
from app.trafego.trafego import dados_agregados

def test_rotacao_de_janela_move_dados_corretamente():
    """
    Este teste segue o padrão Arrange-Act-Assert (AAA).
    que verifica se a função _rotacionar_janela funciona como esperado
    """
    # 1. Arrange (Prepara o Cenário)
    # Colocamos dados de teste na 'janela_atual' e garantimos que a 'janela_pronta' está limpa
    dados_iniciais = {
        "1.1.1.1": {"TCP": {"in_bytes": 100, "out_bytes": 50}},
        "2.2.2.2": {"UDP": {"in_bytes": 200, "out_bytes": 150}}
    }
    with dados_agregados["lock"]:
        dados_agregados["janela_atual"] = dados_iniciais
        dados_agregados["janela_pronta"] = None

    # 2. Act (Executa a Ação)
    # Chamamos a função que queremos testar
    _rotacionar_janela()

    # 3. Assert (Verificar / Garantir o Resultado)
    # Verifica se o estado final da nossa estrutura de dados está correto
    with dados_agregados["lock"]:
        # Garantimos que a 'janela_pronta' agora contém os dados iniciais
        assert dados_agregados["janela_pronta"] is not None
        assert dados_agregados["janela_pronta"] == dados_iniciais
        
        # Garantimos que a 'janela_atual' foi limpa e está pronta para novos dados.
        assert dados_agregados["janela_atual"] == {}


def test_rotacao_de_janela_com_dados_vazios():
    """
    Testa o caso de borda: o que acontece se a janela atual estiver vazia?
    """
    # Arrange
    with dados_agregados["lock"]:
        dados_agregados["janela_atual"] = {}
        dados_agregados["janela_pronta"] = {"algum_dado_antigo": 123}

    # Act
    _rotacionar_janela()

    # Assert
    with dados_agregados["lock"]:
        # A 'janela_pronta' deve agora estar vazia, e a 'janela_atual' também.
        assert dados_agregados["janela_pronta"] == {}
        assert dados_agregados["janela_atual"] == {}

client = TestClient(app)

def test_get_traffic_data_endpoint():
    """
    Testa se o endpoint /api/traffic retorna dados no formato correto.
    """
    # Arrange: prepara dados fictícios na janela_pronta
    with dados_agregados["lock"]:
        dados_agregados["janela_pronta"] = {
            "1.1.1.1": {"TCP": {"in_bytes": 100, "out_bytes": 50}},
            "2.2.2.2": {"UDP": {"in_bytes": 200, "out_bytes": 150}}
        }

    # Act: faz a requisição para o endpoint
    response = client.get("/api/traffic")

    # Assert: verifica resposta
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["client_ip"] == "1.1.1.1"
    assert "total_in" in data[0]
    assert "total_out" in data[0]
    assert "protocols" in data[0]