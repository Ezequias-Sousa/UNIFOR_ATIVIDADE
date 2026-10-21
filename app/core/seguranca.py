"""Funções de segurança: hash de senha e geração/validação do token JWT.

Isolamos aqui a parte "criptográfica" para o resto do código não precisar saber
como o hash ou o token funcionam por dentro. Quem precisa só chama estas funções.

Escolhas:
- bcrypt para a senha: guardar senha em texto é perigoso. O bcrypt transforma a
  senha num hash do qual não dá para voltar ao original.
- JWT para o token: depois do login, o servidor devolve um "crachá" assinado.
  O navegador apresenta esse crachá nas próximas chamadas, e o servidor confia
  nele porque a assinatura bate com a chave secreta.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


def gerar_hash_senha(senha: str) -> str:
    """Transforma uma senha em texto num hash bcrypt (para guardar com segurança)."""
    hash_bytes = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def conferir_senha(senha: str, hash_armazenado: str) -> bool:
    """Confere se a senha digitada corresponde ao hash guardado."""
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), hash_armazenado.encode("utf-8"))
    except ValueError:
        # Hash malformado: trata como senha incorreta, sem quebrar a aplicação.
        return False


def criar_token(usuario: str) -> str:
    """Cria o token JWT que identifica o admin logado, com prazo de validade."""
    config = get_settings()
    agora = datetime.now(timezone.utc)
    conteudo = {
        "sub": usuario,  # "subject": de quem é o token
        "iat": agora,  # emitido em
        "exp": agora + timedelta(hours=config.jwt_expira_horas),  # expira em
    }
    return jwt.encode(conteudo, config.jwt_secret, algorithm="HS256")


def ler_token(token: str) -> str:
    """Valida o token e devolve o usuário. Lança erro se for inválido/expirado."""
    config = get_settings()
    dados = jwt.decode(token, config.jwt_secret, algorithms=["HS256"])
    return dados["sub"]
