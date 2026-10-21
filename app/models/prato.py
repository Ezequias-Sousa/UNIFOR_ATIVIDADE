"""Model da tabela prato."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.categoria import Categoria


class Prato(Base):
    __tablename__ = "prato"
    __table_args__ = (CheckConstraint("preco > 0", name="ck_prato_preco_positivo"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id", ondelete="RESTRICT"), index=True
    )
    nome: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str | None] = mapped_column(String(255))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # Todo prato nasce disponível; passa a indisponível apenas por ação manual.
    disponivel: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )

    categoria: Mapped[Categoria] = relationship(back_populates="pratos")
