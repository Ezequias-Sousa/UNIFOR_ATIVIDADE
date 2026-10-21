"""Ponto de entrada da aplicação.

Aqui a gente:
1. cria a aplicação FastAPI;
2. registra os "handlers" que traduzem nossos erros de domínio em respostas HTTP;
3. pendura as rotas (routers) de categorias e pratos.

Manter este arquivo enxuto é de propósito: a lógica fica nas camadas, e aqui só
acontece a "montagem" final.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.exceptions import ConflitoDeRegra, CredenciaisInvalidas, RecursoNaoEncontrado
from app.routers import auth, categorias, pratos

app = FastAPI(
    title="Sabor de Casa - Cardápio Digital",
    description="API para gerenciar categorias e pratos da marmitaria.",
    version="0.1.0",
)


# --- Tradução de erros de domínio para HTTP ---
# Quando um serviço levanta RecursoNaoEncontrado, o FastAPI chama esta função e
# devolve 404 com uma mensagem clara. O mesmo vale para ConflitoDeRegra (409).
# Assim, as camadas internas nunca precisam saber o que é "status 404".


@app.exception_handler(RecursoNaoEncontrado)
def tratar_nao_encontrado(request: Request, erro: RecursoNaoEncontrado) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": erro.mensagem})


@app.exception_handler(ConflitoDeRegra)
def tratar_conflito(request: Request, erro: ConflitoDeRegra) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": erro.mensagem})


@app.exception_handler(CredenciaisInvalidas)
def tratar_credenciais(request: Request, erro: CredenciaisInvalidas) -> JSONResponse:
    # 401 = não autenticado. O cabeçalho WWW-Authenticate é a convenção para
    # avisar o cliente que a rota usa token do tipo Bearer.
    return JSONResponse(
        status_code=401,
        content={"detail": erro.mensagem},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/api/saude", tags=["Infraestrutura"])
def verificar_saude() -> dict[str, str]:
    """Confirma que a API está no ar."""
    return {"status": "ok"}


# Pendura as rotas da API na aplicação.
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(pratos.router)

# Serve o front-end (HTML/CSS/JS) na raiz do site. html=True faz "/" abrir o
# index.html automaticamente. Fica por último para não "engolir" as rotas /api.
_pasta_frontend = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=_pasta_frontend, html=True), name="frontend")
