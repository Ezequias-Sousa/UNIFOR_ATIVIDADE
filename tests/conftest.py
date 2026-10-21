"""Configuração compartilhada dos testes (fixtures do pytest).

A ideia: rodar os testes contra um banco SQLite em memória, descartável e rápido,
em vez de bater no Neon. Assim os testes são isolados (cada um começa com o banco
vazio), não dependem de internet e não sujam o banco de verdade.

Fixture = um "preparo" que o pytest injeta nos testes que pedirem por ele.
"""

import os
from collections.abc import Iterator

# Define credenciais de teste ANTES de importar a aplicação, pois a config é
# lida na inicialização. Assim o login funciona de forma previsível nos testes.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ["ADMIN_USUARIO"] = "admin"
os.environ["ADMIN_SENHA"] = "senha-de-teste"
os.environ["JWT_SECRET"] = "chave-de-teste"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, event  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.core.config import get_settings  # noqa: E402
from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

get_settings.cache_clear()  # garante que a config use as variáveis acima


@pytest.fixture
def engine():
    # SQLite em memória. StaticPool + check_same_thread=False fazem todas as
    # conexões compartilharem o MESMO banco em memória durante o teste.
    motor = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # O SQLite não aplica chave estrangeira por padrão. Este gancho liga a
    # verificação em cada conexão, para o teste refletir o banco real (Postgres).
    @event.listens_for(motor, "connect")
    def _ligar_fk(conexao, _registro):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Cria as tabelas a partir dos models e as remove ao final do teste.
    Base.metadata.create_all(motor)
    yield motor
    Base.metadata.drop_all(motor)


@pytest.fixture
def db(engine) -> Iterator[Session]:
    # Uma sessão ligada ao banco em memória, usada tanto pela API quanto pelas
    # verificações diretas dentro dos testes.
    SessaoTeste = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with SessaoTeste() as sessao:
        yield sessao


@pytest.fixture
def client_publico(db) -> Iterator[TestClient]:
    # Cliente SEM login: representa o visitante do cardápio. Usado para testar
    # que as rotas de escrita são bloqueadas (401) sem token.
    def _get_db_teste():
        yield db

    app.dependency_overrides[get_db] = _get_db_teste
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()


@pytest.fixture
def client(client_publico) -> TestClient:
    # Cliente JÁ LOGADO como admin: faz login e passa a enviar o token em todas
    # as requisições. A maioria dos testes usa este, pois exercita o CRUD.
    resposta = client_publico.post(
        "/api/auth/login", json={"usuario": "admin", "senha": "senha-de-teste"}
    )
    token = resposta.json()["access_token"]
    client_publico.headers.update({"Authorization": f"Bearer {token}"})
    return client_publico
