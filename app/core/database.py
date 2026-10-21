"""Conexão com o PostgreSQL (Neon): engine, sessão e base dos models."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Classe base de todos os models."""


# pool_pre_ping: o Neon suspende o banco quando ocioso; testa a conexão antes de
# usar, evitando erro na primeira chamada depois de um período parado.
# pool_recycle: recicla conexões antigas, também por causa do "sono" do Neon.
engine = create_engine(
    get_settings().database_url,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """Dependência do FastAPI: abre uma sessão por requisição e a fecha ao final."""
    with SessionLocal() as sessao:
        yield sessao
