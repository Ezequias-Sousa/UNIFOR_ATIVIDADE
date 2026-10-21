"""Schemas do login: o que o cliente envia e o que a API devolve."""

from pydantic import BaseModel, Field


class LoginRequisicao(BaseModel):
    usuario: str = Field(min_length=1)
    senha: str = Field(min_length=1)


class TokenResposta(BaseModel):
    # "bearer" é o tipo padrão de token enviado no cabeçalho Authorization.
    access_token: str
    token_type: str = "bearer"
