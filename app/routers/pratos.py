"""Rotas (endpoints) de Prato que operam sobre um prato específico.

Criar e listar pratos vivem em /categorias/{id}/pratos (ver categorias.py), porque
dependem da categoria. Já detalhar, atualizar e excluir usam só o id do prato,
então ficam aqui em /pratos/{id}.
"""

from fastapi import APIRouter, status

from app.routers.dependencias import AdminDep, PratoServiceDep
from app.schemas.prato import PratoAtualizar, PratoResposta

router = APIRouter(prefix="/api/pratos", tags=["Pratos"])


@router.get("/{prato_id}", response_model=PratoResposta)
def obter_prato(prato_id: int, servico: PratoServiceDep):
    """Detalha um prato. Devolve 404 se não existir."""
    return servico.obter(prato_id)


@router.put("/{prato_id}", response_model=PratoResposta)
def atualizar_prato(
    prato_id: int, dados: PratoAtualizar, servico: PratoServiceDep, _admin: AdminDep
):
    """Atualiza um prato (inclui marcar como disponível/indisponível). Exige admin."""
    return servico.atualizar(prato_id, dados)


@router.delete("/{prato_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_prato(prato_id: int, servico: PratoServiceDep, _admin: AdminDep):
    """Exclui um prato. Exige admin."""
    servico.excluir(prato_id)
