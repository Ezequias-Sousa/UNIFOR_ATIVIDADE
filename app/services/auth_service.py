"""Serviço de autenticação: a regra de negócio do login.

Mantém o padrão das outras camadas: a regra fica no serviço, e o endpoint (router)
só repassa. Aqui a regra é: conferir usuário e senha do admin e, se baterem,
emitir um token.
"""

from app.core.config import Settings
from app.core.seguranca import conferir_senha, criar_token, gerar_hash_senha
from app.exceptions import CredenciaisInvalidas


class AuthService:
    def __init__(self, config: Settings) -> None:
        self.config = config

    def autenticar(self, usuario: str, senha: str) -> str:
        """Confere as credenciais e devolve um token. Erra se forem inválidas."""
        if usuario != self.config.admin_usuario or not self._senha_confere(senha):
            # Mensagem genérica de propósito: não revela se errou o usuário ou a
            # senha, para não ajudar quem tenta adivinhar credenciais.
            raise CredenciaisInvalidas("Usuário ou senha inválidos.")
        return criar_token(usuario)

    def _senha_confere(self, senha: str) -> bool:
        # Preferimos o hash (admin_senha_hash). Se só houver a senha em texto no
        # .env, geramos o hash na hora e comparamos — assim o código é o mesmo.
        if self.config.admin_senha_hash:
            return conferir_senha(senha, self.config.admin_senha_hash)
        if self.config.admin_senha:
            return conferir_senha(senha, gerar_hash_senha(self.config.admin_senha)) or (
                senha == self.config.admin_senha
            )
        # Nenhuma credencial configurada: por segurança, ninguém entra.
        return False
