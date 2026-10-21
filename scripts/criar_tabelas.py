"""Cria as tabelas no banco (idempotente: não altera tabelas que já existem).

Uso: python -m scripts.criar_tabelas
"""

from app.core.database import Base, engine
import app.models  # noqa: F401  (registra os models na Base)


def criar_tabelas() -> None:
    Base.metadata.create_all(engine)
    print("Tabelas criadas/verificadas:", ", ".join(Base.metadata.tables))


if __name__ == "__main__":
    criar_tabelas()
