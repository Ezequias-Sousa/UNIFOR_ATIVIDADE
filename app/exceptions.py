"""Erros de domínio da aplicação.

A ideia aqui é simples: as camadas de serviço não sabem o que é HTTP. Quando algo
dá errado por uma regra de negócio (ex.: "essa categoria já existe"), o serviço
levanta uma destas exceções. Lá no main.py, um "handler" traduz cada uma delas
para o código HTTP certo (404, 409, etc.) com uma mensagem clara para o usuário.

Isso mantém as camadas separadas: regra de negócio de um lado, detalhe de HTTP do outro.
"""


class ErroDeDominio(Exception):
    """Classe-mãe de todos os nossos erros de regra de negócio."""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class RecursoNaoEncontrado(ErroDeDominio):
    """Quando o item pedido não existe no banco (vira HTTP 404)."""


class ConflitoDeRegra(ErroDeDominio):
    """Quando a ação fere uma regra de negócio (vira HTTP 409).

    Exemplos: nome de categoria repetido, ou excluir categoria que ainda tem pratos.
    """


class CredenciaisInvalidas(ErroDeDominio):
    """Quando o login falha: usuário ou senha incorretos (vira HTTP 401)."""
