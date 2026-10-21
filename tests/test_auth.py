"""Testes de autenticação: login e proteção das rotas de escrita.

Aqui garantimos as duas pontas da regra:
- quem tem credencial certa recebe token e consegue editar;
- quem não tem token NÃO consegue editar (mas ainda pode ler o cardápio).
"""


def test_login_com_credenciais_corretas(client_publico):
    resposta = client_publico.post(
        "/api/auth/login", json={"usuario": "admin", "senha": "senha-de-teste"}
    )
    assert resposta.status_code == 200
    assert resposta.json()["access_token"]  # token não vazio


def test_login_com_senha_errada_retorna_401(client_publico):
    resposta = client_publico.post(
        "/api/auth/login", json={"usuario": "admin", "senha": "errada"}
    )
    assert resposta.status_code == 401


def test_leitura_e_publica(client_publico):
    # O visitante (sem token) consegue listar o cardápio normalmente.
    assert client_publico.get("/api/categorias").status_code == 200


def test_escrita_sem_token_e_bloqueada(client_publico):
    # Sem token, criar categoria é recusado com 401 (proteção da área admin).
    resposta = client_publico.post("/api/categorias", json={"nome": "Invasor"})
    assert resposta.status_code == 401


def test_escrita_com_token_funciona(client):
    # 'client' já está logado; a mesma operação agora passa.
    resposta = client.post("/api/categorias", json={"nome": "Autorizado"})
    assert resposta.status_code == 201


def test_token_invalido_e_recusado(client_publico):
    client_publico.headers.update({"Authorization": "Bearer token-falso"})
    resposta = client_publico.post("/api/categorias", json={"nome": "Falso"})
    assert resposta.status_code == 401
