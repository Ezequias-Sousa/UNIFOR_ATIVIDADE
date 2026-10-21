"""Repositório da Categoria: a ÚNICA camada que conversa com o banco.

Pense no repositório como o "almoxarife": ele sabe guardar e buscar coisas no
estoque (o banco), mas não decide regras de negócio. Quem decide é o serviço.
Essa separação é uma das técnicas de clean code que o trabalho pede.
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Categoria


class CategoriaRepository:
    def __init__(self, db: Session) -> None:
        # Recebe a sessão do banco já aberta para esta requisição.
        self.db = db

    def listar(self) -> list[Categoria]:
        # Busca todas as categorias em ordem alfabética.
        return list(self.db.scalars(select(Categoria).order_by(Categoria.nome)))

    def buscar_por_id(self, categoria_id: int) -> Categoria | None:
        # Retorna a categoria ou None (quem decide o que fazer com o None é o serviço).
        return self.db.get(Categoria, categoria_id)

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        # Compara ignorando maiúsculas/minúsculas, igual à regra de unicidade do banco.
        # Serve para avisar o usuário com clareza ANTES de o banco recusar.
        consulta = select(Categoria).where(func.lower(Categoria.nome) == nome.strip().lower())
        return self.db.scalars(consulta).first()

    def contar_pratos(self, categoria_id: int) -> int:
        # Conta quantos pratos pertencem à categoria. Usado para impedir exclusão.
        from app.models import Prato

        consulta = select(func.count()).select_from(Prato).where(Prato.categoria_id == categoria_id)
        return self.db.scalar(consulta) or 0

    def salvar(self, categoria: Categoria) -> Categoria:
        # Insere (se for novo) ou atualiza (se já existe) e confirma no banco.
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)  # recarrega para pegar o id gerado
        return categoria

    def excluir(self, categoria: Categoria) -> None:
        self.db.delete(categoria)
        self.db.commit()
