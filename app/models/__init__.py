"""Importar os models aqui garante que o SQLAlchemy os registre na Base."""

from app.models.categoria import Categoria
from app.models.prato import Prato

__all__ = ["Categoria", "Prato"]
