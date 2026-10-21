"""Validadores reutilizáveis dos schemas.

Reunir aqui o tratamento de texto evita repetir a mesma lógica em cada schema
(princípio de não duplicar código). Os schemas de categoria e prato usam estes
tipos prontos.
"""

from typing import Annotated

from pydantic import AfterValidator


def _limpar_texto_obrigatorio(valor: str) -> str:
    # Remove espaços das bordas ANTES de validar o tamanho. Assim um texto só com
    # espaços ("   ") vira "" e é rejeitado como campo obrigatório vazio.
    limpo = valor.strip()
    if not limpo:
        raise ValueError("não pode ficar em branco")
    return limpo


def _limpar_texto_opcional(valor: str | None) -> str | None:
    # Para descrição: tira espaços; se sobrar vazio, trata como "sem descrição".
    if valor is None:
        return None
    limpo = valor.strip()
    return limpo or None


# Tipos prontos para usar nos schemas:
# - TextoObrigatorio: já chega limpo e garantido não-vazio.
# - TextoOpcional: já chega limpo, ou None.
TextoObrigatorio = Annotated[str, AfterValidator(_limpar_texto_obrigatorio)]
TextoOpcional = Annotated[str | None, AfterValidator(_limpar_texto_opcional)]
