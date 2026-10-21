// api.js — a ÚNICA parte do front que fala com o servidor (as chamadas fetch).
// Centralizar aqui evita repetir "fetch" espalhado pelas telas e deixa um lugar
// só para tratar erros e anexar o token do admin.

import { pegarToken, limparToken } from "./auth.js";

// Monta os cabeçalhos. Se houver token salvo, envia no formato "Bearer <token>",
// que é o que o back-end espera nas rotas protegidas.
function montarCabecalhos(temCorpo) {
  const cabecalhos = {};
  if (temCorpo) cabecalhos["Content-Type"] = "application/json";
  const token = pegarToken();
  if (token) cabecalhos["Authorization"] = `Bearer ${token}`;
  return cabecalhos;
}

// Função única que faz a requisição e já trata os casos comuns de erro.
async function requisitar(metodo, caminho, corpo) {
  const resposta = await fetch(caminho, {
    method: metodo,
    headers: montarCabecalhos(corpo !== undefined),
    body: corpo !== undefined ? JSON.stringify(corpo) : undefined,
  });

  // 401 = sessão expirou ou token inválido: limpa o token e manda relogar.
  if (resposta.status === 401) {
    limparToken();
    throw new ErroApi("Sessão expirada. Faça login novamente.", 401);
  }

  // 204 = sucesso sem conteúdo (ex.: exclusão). Não há JSON para ler.
  if (resposta.status === 204) return null;

  const dados = await resposta.json().catch(() => ({}));

  if (!resposta.ok) {
    // A API devolve {"detail": "mensagem"}. Mostramos essa mensagem ao usuário.
    const mensagem = extrairMensagem(dados);
    throw new ErroApi(mensagem, resposta.status);
  }
  return dados;
}

// O erro de validação do FastAPI (422) vem como lista; os nossos erros vêm como
// string. Esta função normaliza os dois para uma frase legível.
function extrairMensagem(dados) {
  if (typeof dados.detail === "string") return dados.detail;
  if (Array.isArray(dados.detail)) {
    return dados.detail.map((e) => e.msg).join("; ");
  }
  return "Ocorreu um erro inesperado.";
}

// Erro próprio que carrega também o código HTTP, útil para as telas decidirem o que fazer.
export class ErroApi extends Error {
  constructor(mensagem, status) {
    super(mensagem);
    this.status = status;
  }
}

// Atalhos usados pelas telas. Lê-se "api.categorias.listar()", etc.
export const api = {
  login: (usuario, senha) =>
    requisitar("POST", "/api/auth/login", { usuario, senha }),

  categorias: {
    listar: () => requisitar("GET", "/api/categorias"),
    obter: (id) => requisitar("GET", `/api/categorias/${id}`),
    criar: (dados) => requisitar("POST", "/api/categorias", dados),
    atualizar: (id, dados) => requisitar("PUT", `/api/categorias/${id}`, dados),
    excluir: (id) => requisitar("DELETE", `/api/categorias/${id}`),
  },

  pratos: {
    listarPorCategoria: (categoriaId) =>
      requisitar("GET", `/api/categorias/${categoriaId}/pratos`),
    criar: (categoriaId, dados) =>
      requisitar("POST", `/api/categorias/${categoriaId}/pratos`, dados),
    obter: (id) => requisitar("GET", `/api/pratos/${id}`),
    atualizar: (id, dados) => requisitar("PUT", `/api/pratos/${id}`, dados),
    excluir: (id) => requisitar("DELETE", `/api/pratos/${id}`),
  },
};
