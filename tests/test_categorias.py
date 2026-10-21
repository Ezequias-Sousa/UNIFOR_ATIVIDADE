"""Testes da entidade Categoria: o CRUD e as regras do cenário.

Cada teste recebe o 'client' (a API ligada ao banco em memória) e verifica um
comportamento. O nome do teste descreve o que ele garante.
"""


def test_criar_e_listar_categoria(client):
    # Começa vazio.
    assert client.get("/api/categorias").json() == []

    resposta = client.post("/api/categorias", json={"nome": "Carnes", "descricao": "Pratos com carne"})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] > 0
    assert corpo["nome"] == "Carnes"

    # Agora a lista tem uma categoria.
    lista = client.get("/api/categorias").json()
    assert len(lista) == 1


def test_nome_obrigatorio_rejeita_vazio(client):
    # Nome só com espaços deve ser tratado como vazio -> 422 (regra: obrigatório).
    resposta = client.post("/api/categorias", json={"nome": "   "})
    assert resposta.status_code == 422


def test_nome_sem_repeticao(client):
    client.post("/api/categorias", json={"nome": "Bebidas"})
    # Mesmo nome com outra caixa deve ser recusado -> 409 (regra: sem repetição).
    resposta = client.post("/api/categorias", json={"nome": "bebidas"})
    assert resposta.status_code == 409
    assert "já existe" in resposta.json()["detail"].lower()


def test_atualizar_categoria(client):
    criada = client.post("/api/categorias", json={"nome": "Sobremesa"}).json()
    resposta = client.put(f"/api/categorias/{criada['id']}", json={"nome": "Sobremesas"})
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Sobremesas"


def test_atualizar_mantendo_mesmo_nome_nao_da_conflito(client):
    # Editar a categoria sem trocar o nome não pode acusar "nome repetido".
    criada = client.post("/api/categorias", json={"nome": "Saladas"}).json()
    resposta = client.put(
        f"/api/categorias/{criada['id']}",
        json={"nome": "Saladas", "descricao": "atualizada"},
    )
    assert resposta.status_code == 200


def test_obter_categoria_inexistente_retorna_404(client):
    assert client.get("/api/categorias/99999").status_code == 404


def test_excluir_categoria_vazia(client):
    criada = client.post("/api/categorias", json={"nome": "Vazia"}).json()
    assert client.delete(f"/api/categorias/{criada['id']}").status_code == 204
    assert client.get(f"/api/categorias/{criada['id']}").status_code == 404


def test_nao_excluir_categoria_com_pratos(client):
    categoria = client.post("/api/categorias", json={"nome": "Massas"}).json()
    client.post(f"/api/categorias/{categoria['id']}/pratos", json={"nome": "Lasanha", "preco": "30.00"})
    # Regra: não dá para excluir categoria que ainda tem pratos -> 409.
    resposta = client.delete(f"/api/categorias/{categoria['id']}")
    assert resposta.status_code == 409
