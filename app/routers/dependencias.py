"""Montagem das camadas (injeção de dependência).

O FastAPI consegue "montar" os objetos que cada rota precisa. Aqui dizemos como
empilhar as camadas: a sessão do banco entra no repositório, o repositório entra
no serviço, e a rota recebe o serviço pronto para usar.

Vantagem: a rota não precisa saber COMO o serviço é construído. E nos testes dá
para trocar qualquer camada por uma versão falsa com facilidade.
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.core.seguranca import ler_token
from app.exceptions import CredenciaisInvalidas
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.prato_repository import PratoRepository
from app.services.auth_service import AuthService
from app.services.categoria_service import CategoriaService
from app.services.prato_service import PratoService

# "Annotated[... , Depends(...)]" é a forma do FastAPI de dizer:
# "para preencher este parâmetro, chame esta função".
SessaoDep = Annotated[Session, Depends(get_db)]
ConfigDep = Annotated[Settings, Depends(get_settings)]


def obter_categoria_service(db: SessaoDep) -> CategoriaService:
    return CategoriaService(CategoriaRepository(db))


CategoriaServiceDep = Annotated[CategoriaService, Depends(obter_categoria_service)]


def obter_prato_service(
    db: SessaoDep, categoria_service: CategoriaServiceDep
) -> PratoService:
    return PratoService(PratoRepository(db), categoria_service)


PratoServiceDep = Annotated[PratoService, Depends(obter_prato_service)]


def obter_auth_service(config: ConfigDep) -> AuthService:
    return AuthService(config)


AuthServiceDep = Annotated[AuthService, Depends(obter_auth_service)]


# --- Proteção das rotas de escrita ---
# HTTPBearer lê o cabeçalho "Authorization: Bearer <token>" da requisição.
# auto_error=False: em vez de deixar o FastAPI responder sozinho, tratamos a
# ausência do token aqui, devolvendo sempre a mesma mensagem de 401.
_esquema_bearer = HTTPBearer(auto_error=False)


def exigir_admin(
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)],
) -> str:
    """Guarda das rotas protegidas: só deixa passar quem traz um token válido.

    As rotas de leitura (GET) NÃO usam esta dependência, então seguem públicas.
    As de escrita (POST/PUT/DELETE) a usam e, sem token válido, recebem 401.
    """
    if credenciais is None:
        raise CredenciaisInvalidas("Autenticação necessária.")
    try:
        return ler_token(credenciais.credentials)
    except Exception as erro:  # token inválido, expirado ou malformado
        raise CredenciaisInvalidas("Sessão inválida ou expirada.") from erro


# Usada apenas pelo seu efeito colateral (validar o token). Quem a declara numa
# rota está dizendo "esta rota exige admin".
AdminDep = Annotated[str, Depends(exigir_admin)]
