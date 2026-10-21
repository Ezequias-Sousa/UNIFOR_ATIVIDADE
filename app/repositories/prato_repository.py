"""Repositório do Prato: acesso ao banco para a entidade Prato.

Mesma função do repositório de categoria: só guarda e busca. Sem regras de negócio.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Prato


class PratoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_por_categoria(self, categoria_id: int) -> list[Prato]:
        # Lista os pratos de uma categoria, em ordem alfabética.
        consulta = (
            select(Prato)
            .where(Prato.categoria_id == categoria_id)
            .order_by(Prato.nome)
        )
        return list(self.db.scalars(consulta))

    def buscar_por_id(self, prato_id: int) -> Prato | None:
        return self.db.get(Prato, prato_id)

    def salvar(self, prato: Prato) -> Prato:
        self.db.add(prato)
        self.db.commit()
        self.db.refresh(prato)
        return prato

    def excluir(self, prato: Prato) -> None:
        self.db.delete(prato)
        self.db.commit()
