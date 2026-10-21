"""Schemas (Pydantic) da Categoria.

Schema = o "formato" dos dados que entram e saem da API. O Pydantic valida
automaticamente o que o cliente envia. Se algo estiver errado (ex.: nome vazio),
o FastAPI já devolve um erro 422 com a explicação, sem a gente escrever nada.

Separamos em três classes de propósito:
- Base: campos comuns.
- CategoriaCriar / CategoriaAtualizar: o que o cliente PODE mandar.
- CategoriaResposta: o que a API DEVOLVE (inclui o id gerado pelo banco).
"""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.comuns import TextoObrigatorio, TextoOpcional


class CategoriaBase(BaseModel):
    # TextoObrigatorio remove espaços das bordas e recusa texto em branco.
    # max_length garante que o nome caiba na coluna do banco (60 caracteres).
    nome: TextoObrigatorio = Field(max_length=60, description="Nome da categoria")
    descricao: TextoOpcional = Field(default=None, max_length=255)


class CategoriaCriar(CategoriaBase):
    """Dados para criar uma categoria. Mesmos campos da base."""


class CategoriaAtualizar(CategoriaBase):
    """Dados para atualizar. Aqui exigimos o nome igual ao criar (edição completa)."""


class CategoriaResposta(CategoriaBase):
    # Esta configuração permite ao Pydantic ler os dados direto do objeto do
    # SQLAlchemy (o model), e não só de um dicionário.
    model_config = ConfigDict(from_attributes=True)

    id: int
