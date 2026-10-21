"""Rotas de autenticação.

Só uma rota: o login. Ela repassa para o AuthService e devolve o token.
A proteção das rotas de escrita fica na dependência 'exigir_admin' (ver dependencias.py).
"""

from fastapi import APIRouter

from app.routers.dependencias import AuthServiceDep
from app.schemas.auth import LoginRequisicao, TokenResposta

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResposta)
def login(dados: LoginRequisicao, servico: AuthServiceDep):
    """Recebe usuário e senha. Se baterem, devolve um token. Senão, 401."""
    token = servico.autenticar(dados.usuario, dados.senha)
    return TokenResposta(access_token=token)
