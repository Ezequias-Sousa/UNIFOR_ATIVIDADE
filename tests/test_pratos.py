"""Testes da entidade Prato: o CRUD, a regra de preço e a disponibilidade."""

import pytest


@pytest.fixture
def categoria_id(client) -> int:
    # Preparo comum: cria uma categoria e devolve o id, para os testes de prato.
    return client.post("/api/categorias", json={"nome": "Carnes"}).json()["id"]


def test_criar_prato_nasce_disponivel(client, categoria_id):
    resposta = client.post(
        f"/api/categorias/{categoria_id}/pratos",
        json={"nome": "Picanha", "preco": "49.90"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    # Regra combinada: todo prato nasce disponível.
    assert corpo["disponivel"] is True
    assert corpo["preco"] == "49.90"


def test_preco_deve_ser_maior_que_zero(client, categoria_id):
    # Regra do cenário: preço maior que zero -> 422.
    assert client.post(
        f"/api/categorias/{categoria_id}/pratos",
        json={"nome": "Grátis", "preco": "0"},
    ).status_code == 422
    # Preço negativo também é recusado.
    assert client.post(
        f"/api/categorias/{categoria_id}/pratos",
        json={"nome": "Negativo", "preco": "-5"},
    ).status_code == 422


def test_criar_prato_em_categoria_inexistente_retorna_404(client):
    assert client.post(
        "/api/categorias/99999/pratos",
        json={"nome": "Fantasma", "preco": "10"},
    ).status_code == 404


def test_listar_pratos_da_categoria(client, categoria_id):
    client.post(f"/api/categorias/{categoria_id}/pratos", json={"nome": "Frango", "preco": "25"})
    client.post(f"/api/categorias/{categoria_id}/pratos", json={"nome": "Costela", "preco": "40"})
    lista = client.get(f"/api/categorias/{categoria_id}/pratos").json()
    assert len(lista) == 2


def test_tornar_prato_indisponivel(client, categoria_id):
    prato = client.post(
        f"/api/categorias/{categoria_id}/pratos",
        json={"nome": "Peixe", "preco": "38"},
    ).json()
    # Ação manual: marcar como indisponível na edição.
    resposta = client.put(
        f"/api/pratos/{prato['id']}",
        json={"nome": "Peixe", "preco": "38", "disponivel": False},
    )
    assert resposta.status_code == 200
    assert resposta.json()["disponivel"] is False


def test_excluir_prato(client, categoria_id):
    prato = client.post(
        f"/api/categorias/{categoria_id}/pratos",
        json={"nome": "Arroz", "preco": "12"},
    ).json()
    assert client.delete(f"/api/pratos/{prato['id']}").status_code == 204
    assert client.get(f"/api/pratos/{prato['id']}").status_code == 404


def test_obter_prato_inexistente_retorna_404(client):
    assert client.get("/api/pratos/99999").status_code == 404
