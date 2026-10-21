"""Serviço do Prato: regras de negócio da entidade Prato.

Um prato sempre pertence a uma categoria existente. Por isso o serviço de prato
conversa também com o serviço de categoria, reaproveitando a regra "a categoria
precisa existir" em vez de repeti-la aqui (evitar código duplicado).
"""

from app.exceptions import RecursoNaoEncontrado
from app.models import Prato
from app.repositories.prato_repository import PratoRepository
from app.schemas.prato import PratoAtualizar, PratoCriar
from app.services.categoria_service import CategoriaService


class PratoService:
    def __init__(self, repo: PratoRepository, categoria_service: CategoriaService) -> None:
        self.repo = repo
        self.categoria_service = categoria_service

    def listar_por_categoria(self, categoria_id: int) -> list[Prato]:
        # obter() dispara 404 se a categoria não existir — reaproveitamos a regra.
        self.categoria_service.obter(categoria_id)
        return self.repo.listar_por_categoria(categoria_id)

    def obter(self, prato_id: int) -> Prato:
        prato = self.repo.buscar_por_id(prato_id)
        if prato is None:
            raise RecursoNaoEncontrado(f"Prato {prato_id} não encontrado.")
        return prato

    def criar(self, categoria_id: int, dados: PratoCriar) -> Prato:
        # Garante que a categoria existe antes de criar o prato nela.
        self.categoria_service.obter(categoria_id)
        prato = Prato(
            categoria_id=categoria_id,
            nome=dados.nome.strip(),
            descricao=dados.descricao,
            preco=dados.preco,
            disponivel=dados.disponivel,  # vem True por padrão na criação
        )
        return self.repo.salvar(prato)

    def atualizar(self, prato_id: int, dados: PratoAtualizar) -> Prato:
        prato = self.obter(prato_id)
        prato.nome = dados.nome.strip()
        prato.descricao = dados.descricao
        prato.preco = dados.preco
        prato.disponivel = dados.disponivel  # aqui a dona pode marcar indisponível
        return self.repo.salvar(prato)

    def excluir(self, prato_id: int) -> None:
        prato = self.obter(prato_id)
        self.repo.excluir(prato)
