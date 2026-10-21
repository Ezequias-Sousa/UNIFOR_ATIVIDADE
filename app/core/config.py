"""Configurações da aplicação, lidas das variáveis de ambiente ou do arquivo .env.

Centralizar tudo aqui evita espalhar os.getenv pelo código e deixa claro, num
lugar só, de que a aplicação precisa para rodar. Nada de segredo escrito no código:
senha e chave vêm do ambiente (.env no PC, variáveis de ambiente no deploy).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Conexão com o banco (Neon).
    database_url: str

    # Credenciais do administrador. A senha pode vir em texto puro (admin_senha)
    # OU já em hash bcrypt (admin_senha_hash). Preferimos o hash no deploy.
    admin_usuario: str = "admin"
    admin_senha: str | None = None
    admin_senha_hash: str | None = None

    # Chave usada para assinar o token JWT. Troque por um valor longo e aleatório
    # no deploy (ex.: gerado com 'openssl rand -hex 32').
    jwt_secret: str = "troque-esta-chave-no-deploy"
    jwt_expira_horas: int = 8

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
