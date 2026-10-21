"""Serviço da Categoria: é aqui que moram as REGRAS DE NEGÓCIO.

O serviço é o "gerente": ele decide o que pode e o que não pode, usando o
repositório (o almoxarife) para mexer no banco. Quando uma regra é quebrada,
ele levanta um erro de domínio (ConflitoDeRegra, RecursoNaoEncontrado), que
depois vira o código HTTP certo.

Regras do cenário tratadas aqui:
- nome de categoria sem repetição;
- não excluir categoria que ainda tenha pratos.
"""

from app.exceptions import ConflitoDeRegra, RecursoNaoEncontrado
from app.models import Categoria
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria import CategoriaAtualizar, CategoriaCriar


class CategoriaService:
    def __init__(self, repo: CategoriaRepository) -> None:
        self.repo = repo

    def listar(self) -> list[Categoria]:
        return self.repo.listar()

    def obter(self, categoria_id: int) -> Categoria:
        # Busca e, se não achar, já avisa com um erro claro (vira 404).
        categoria = self.repo.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado(f"Categoria {categoria_id} não encontrada.")
        return categoria

    def criar(self, dados: CategoriaCriar) -> Categoria:
        # Regra: nome não pode repetir (ignorando maiúsculas/minúsculas).
        # O nome já chega limpo (sem espaços nas bordas) do schema.
        self._garantir_nome_unico(dados.nome)
        categoria = Categoria(nome=dados.nome, descricao=dados.descricao)
        return self.repo.salvar(categoria)

    def atualizar(self, categoria_id: int, dados: CategoriaAtualizar) -> Categoria:
        categoria = self.obter(categoria_id)
        # Só checa duplicidade se o nome realmente mudou. Isso evita um "falso
        # conflito" da categoria com ela mesma.
        if dados.nome.lower() != categoria.nome.lower():
            self._garantir_nome_unico(dados.nome)
        categoria.nome = dados.nome
        categoria.descricao = dados.descricao
        return self.repo.salvar(categoria)

    def excluir(self, categoria_id: int) -> None:
        categoria = self.obter(categoria_id)
        # Regra: não dá para excluir categoria que ainda tem pratos.
        if self.repo.contar_pratos(categoria_id) > 0:
            raise ConflitoDeRegra(
                "Não é possível excluir: a categoria possui pratos cadastrados."
            )
        self.repo.excluir(categoria)

    def _garantir_nome_unico(self, nome: str) -> None:
        # Método auxiliar (o "_" indica uso interno). Centraliza a checagem de
        # nome repetido para não duplicar código entre criar e atualizar.
        if self.repo.buscar_por_nome(nome) is not None:
            raise ConflitoDeRegra(f"Já existe uma categoria com o nome '{nome}'.")
