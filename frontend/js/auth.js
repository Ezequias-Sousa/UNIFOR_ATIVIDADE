// auth.js — guarda e recupera o token do admin no navegador.
// Usamos o localStorage: o token fica salvo mesmo se a aba for recarregada,
// até o admin sair (logout) ou a sessão expirar.

const CHAVE = "marmitaria_token";

export function salvarToken(token) {
  localStorage.setItem(CHAVE, token);
}

export function pegarToken() {
  return localStorage.getItem(CHAVE);
}

export function limparToken() {
  localStorage.removeItem(CHAVE);
}

export function estaLogado() {
  return Boolean(pegarToken());
}

// Protege as páginas de admin: se não houver token, manda para o login.
export function exigirLogin() {
  if (!estaLogado()) {
    window.location.href = "login.html";
  }
}
