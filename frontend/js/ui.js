// ui.js — pequenas ajudas visuais reaproveitadas por todas as telas.
// Reunir aqui evita repetir o mesmo código de alerta/formatação em cada página.

// Mostra uma mensagem colorida (verde = sucesso, vermelho = erro) num elemento.
export function mostrarMensagem(elemento, texto, tipo = "erro") {
  elemento.textContent = texto;
  elemento.className = `alerta alerta-${tipo}`;
  elemento.hidden = false;
}

export function esconderMensagem(elemento) {
  elemento.hidden = true;
}

// Formata um número como preço em reais (ex.: 49.9 -> "R$ 49,90").
export function formatarPreco(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

// Escapa texto antes de jogar no HTML, evitando que um nome com "<" quebre a
// página (boa prática simples de segurança contra injeção de HTML).
export function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

// Lê o parâmetro da URL (ex.: pratos em "?categoria=3").
export function parametroUrl(nome) {
  return new URLSearchParams(window.location.search).get(nome);
}
