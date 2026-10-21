"""Rotas (endpoints) de Categoria — a camada de interface do serviço Web.

A rota é bem "magrinha" de propósito: ela só recebe o pedido HTTP, repassa para o
serviço e devolve a resposta. Nenhuma regra de negócio mora aqui. Isso deixa claro
quem faz o quê (separação em camadas) e facilita a leitura.

Também incluímos aqui a listagem e a criação de pratos DE UMA categoria, porque
essas rotas penduram embaixo de /categorias/{id}/pratos.
"""

from fastapi import APIRouter, status

from app.routers.dependencias import AdminDep, CategoriaServiceDep, PratoServiceDep
from app.schemas.categoria import CategoriaAtualizar, CategoriaCriar, CategoriaResposta
from app.schemas.prato import PratoCriar, PratoResposta

router = APIRouter(prefix="/api/categorias", tags=["Categorias"])


@router.get("", response_model=list[CategoriaResposta])
def listar_categorias(servico: CategoriaServiceDep):
    """Lista todas as categorias."""
    return servico.listar()


@router.post("", response_model=CategoriaResposta, status_code=status.HTTP_201_CREATED)
def criar_categoria(dados: CategoriaCriar, servico: CategoriaServiceDep, _admin: AdminDep):
    """Cria uma categoria. Devolve 409 se o nome já existir. Exige admin."""
    return servico.criar(dados)


@router.get("/{categoria_id}", response_model=CategoriaResposta)
def obter_categoria(categoria_id: int, servico: CategoriaServiceDep):
    """Detalha uma categoria. Devolve 404 se não existir."""
    return servico.obter(categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaResposta)
def atualizar_categoria(
    categoria_id: int,
    dados: CategoriaAtualizar,
    servico: CategoriaServiceDep,
    _admin: AdminDep,
):
    """Atualiza uma categoria. Exige admin."""
    return servico.atualizar(categoria_id, dados)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_categoria(categoria_id: int, servico: CategoriaServiceDep, _admin: AdminDep):
    """Exclui uma categoria. Devolve 409 se ela ainda tiver pratos. Exige admin."""
    servico.excluir(categoria_id)


# --- Pratos de uma categoria (relação 1:N na URL) ---


@router.get("/{categoria_id}/pratos", response_model=list[PratoResposta], tags=["Pratos"])
def listar_pratos_da_categoria(categoria_id: int, servico: PratoServiceDep):
    """Lista os pratos de uma categoria."""
    return servico.listar_por_categoria(categoria_id)


@router.post(
    "/{categoria_id}/pratos",
    response_model=PratoResposta,
    status_code=status.HTTP_201_CREATED,
    tags=["Pratos"],
)
def criar_prato_na_categoria(
    categoria_id: int, dados: PratoCriar, servico: PratoServiceDep, _admin: AdminDep
):
    """Cria um prato dentro de uma categoria. O prato nasce disponível. Exige admin."""
    return servico.criar(categoria_id, dados)
