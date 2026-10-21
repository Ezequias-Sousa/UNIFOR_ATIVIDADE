# Sabor de Casa - Cardápio Digital

Projeto acadêmico de Desenvolvimento Web (Cenário 3: Marmitaria).
Sistema para manter o cardápio organizado por categorias, com CRUD de **Categoria** e **Prato**.

## Stack

Python + FastAPI + SQLAlchemy + PostgreSQL (Neon) + HTML/CSS/JS + Bootstrap 5.
Detalhes e decisões em [docs/plans/2026-10-20-marmitaria-design.md](docs/plans/2026-10-20-marmitaria-design.md).

## Como rodar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env   # depois preencha DATABASE_URL com a string do Neon
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/api/saude
- Documentação interativa: http://127.0.0.1:8000/docs

## Uso de IA generativa

Este projeto usou IA generativa (Kiro) como apoio ao desenvolvimento. A equipe revisa,
entende e responde por todo o código entregue. A declaração completa consta no PDF (tópico 11).

# UNIFOR_ATIVIDADE
