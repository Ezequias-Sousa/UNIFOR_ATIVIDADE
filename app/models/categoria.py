"""Model da tabela categoria."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.prato import Prato


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(60))
    descricao: Mapped[str | None] = mapped_column(String(255))

    # passive_deletes="all": o ORM não mexe nos pratos; quem protege é o banco (RESTRICT).
    pratos: Mapped[list[Prato]] = relationship(
        back_populates="categoria", passive_deletes="all"
    )


# Nome único sem diferenciar maiúsculas de minúsculas ("Carnes" == "carnes").
Index("uq_categoria_nome_lower", func.lower(Categoria.nome), unique=True)
