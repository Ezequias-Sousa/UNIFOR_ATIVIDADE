# Design: Cardápio Digital da Marmitaria Sabor de Casa

Data: 2026-10-20 | Disciplina: Desenvolvimento Web | Cenário 3 (Marmitaria)

## 1. Objetivo

Sistema Web para manter o cardápio da marmitaria organizado por categorias.
A aplicação oferece criar, listar, atualizar e excluir (CRUD) para duas entidades
relacionadas: **Categoria** e **Prato** (1 categoria : N pratos).

Prazos: commits válidos até **27/11**; app e repositório no ar até **10/12**.

## 2. Decisões de stack (validadas)

| Item | Decisão | Motivo |
|---|---|---|
| Linguagem / API | Python + FastAPI | Domínio da equipe; documentação automática em `/docs` |
| Validação | Pydantic | Regras do cenário com mensagens claras |
| Acesso a dados | SQLAlchemy 2.0 (ORM) | Equipe novata; relação 1:N declarada no código |
| Banco | PostgreSQL no Neon | Nuvem, plano grátis sem prazo; maior nota em rigor técnico |
| Front-end | HTML + CSS + JS puro (`fetch`) + Bootstrap 5 via CDN | Telas separadas, fácil dividir tarefas |
| Hospedagem | Render (API + front no mesmo serviço) | Um único link público |

## 3. Modelo de dados

**categoria**
- `id` PK
- `nome` obrigatório, até 60 caracteres, único sem diferenciar maiúsculas de minúsculas
- `descricao` opcional

**prato**
- `id` PK
- `categoria_id` FK obrigatória, `ON DELETE RESTRICT`
- `nome` obrigatório, até 100 caracteres
- `descricao` opcional
- `preco` `NUMERIC(10,2)`, obrigatório, maior que zero
- `disponivel` booleano, `DEFAULT TRUE` (muda para falso manualmente)

## 4. Regras do cenário e onde são aplicadas

| Regra | API (Pydantic / serviço) | Banco (2ª barreira) |
|---|---|---|
| Campos obrigatórios | 422 com mensagem por campo | `NOT NULL` |
| Preço maior que zero | `Field(gt=0)` | `CHECK (preco > 0)` |
| Nome de categoria sem repetição | serviço devolve 409 | índice único em `lower(nome)` |
| Não excluir categoria com pratos | serviço devolve 409 | FK `ON DELETE RESTRICT` |

## 5. Arquitetura em camadas

```
app/
  main.py            # cria a aplicação, registra rotas e arquivos estáticos
  core/              # configuração (.env) e conexão com o banco
  models/            # tabelas SQLAlchemy
  schemas/           # validação Pydantic (entrada e saída)
  repositories/      # acesso ao banco (única camada que fala com a sessão)
  services/          # regras de negócio
  routers/           # endpoints HTTP (camada de interface do serviço)
  exceptions.py      # erros de domínio + handlers HTTP
frontend/
  categorias.html    # lista + cadastro/edição de categoria
  pratos.html        # pratos de uma categoria (?categoria=ID) + cadastro/edição
  css/style.css
  js/api.js          # chamadas HTTP (única camada que usa fetch)
  js/ui.js           # alertas e mensagens de erro
  js/categorias.js
  js/pratos.js
```

Fluxo: `router` → `service` (regras) → `repository` (ORM) → Neon.
Erros de domínio sobem como exceções e um handler os converte em resposta JSON
`{"detail": "mensagem clara"}` com o status HTTP adequado (404, 409, 422).

## 6. API REST

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/categorias` | Lista categorias |
| POST | `/api/categorias` | Cria categoria |
| GET | `/api/categorias/{id}` | Detalha categoria |
| PUT | `/api/categorias/{id}` | Atualiza categoria |
| DELETE | `/api/categorias/{id}` | Exclui (409 se houver pratos) |
| GET | `/api/categorias/{id}/pratos` | Lista pratos da categoria |
| POST | `/api/categorias/{id}/pratos` | Cria prato na categoria |
| GET | `/api/pratos/{id}` | Detalha prato |
| PUT | `/api/pratos/{id}` | Atualiza prato (inclui `disponivel`) |
| DELETE | `/api/pratos/{id}` | Exclui prato |

## 7. Telas

1. **Categorias**: tabela com ações (editar, excluir, ver pratos) e formulário de cadastro/edição.
2. **Pratos da categoria**: tabela com preço e situação (disponível/indisponível), botão para alternar
   disponibilidade, formulário de cadastro/edição. Novo prato já vem marcado como disponível.

Erros do servidor aparecem como alerta na tela (ex.: "Não é possível excluir: a categoria
possui pratos cadastrados").

## 8. Plano de sprints (20/10 a 27/11)

1. Stack, repositório e planejamento
2. Modelagem de dados e conexão com o Neon
3. Back-end: CRUD em camadas
4. Validação e tratamento de erros
5. Front-end: telas e navegação
6. Integração, revisão de clean code e testes manuais
7. Deploy (Render + Neon) e testes no link público
8. Documentação: PDF no modelo oficial, declaração de IA, reflexão
9. Buffer e conferência final (capa, links, prazos)

## 9. Pontos de atenção para a nota

- Declarar uso de IA generativa no PDF (tópico 11): sem isso, -2,0.
- Capa com nome completo e matrícula de todos os integrantes.
- Commits distribuídos entre os integrantes, até 27/11.
- Render grátis dorme após 15 min sem acesso: abrir o link antes da avaliação.
