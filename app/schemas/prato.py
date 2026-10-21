"""Schemas (Pydantic) do Prato.

Mesma ideia da categoria: definimos o formato de entrada e de saída e deixamos
o Pydantic validar. A regra "preço maior que zero" vira 'gt=0' aqui — então um
preço inválido é barrado já na porta da API, antes de chegar ao banco.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.comuns import TextoObrigatorio, TextoOpcional


class PratoBase(BaseModel):
    nome: TextoObrigatorio = Field(max_length=100, description="Nome do prato")
    descricao: TextoOpcional = Field(default=None, max_length=255)
    # gt=0 significa "greater than 0" (maior que zero). É a regra do cenário.
    preco: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class PratoCriar(PratoBase):
    # Ao criar, o prato nasce disponível. O cliente pode omitir este campo e,
    # por padrão, virá True. Para deixar indisponível, é ação manual depois.
    disponivel: bool = True


class PratoAtualizar(PratoBase):
    # Na edição, a disponibilidade é definida explicitamente (é aqui que a dona
    # marca um prato como indisponível quando ele acaba).
    disponivel: bool


class PratoResposta(PratoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoria_id: int
    disponivel: bool
