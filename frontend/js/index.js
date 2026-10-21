// index.js — monta o cardápio público (somente leitura).
// Para cada categoria, busca seus pratos e lista apenas os disponíveis.
import { api } from "./api.js";
import { mostrarMensagem, formatarPreco, escapar } from "./ui.js";

const cardapio = document.getElementById("cardapio");
const mensagem = document.getElementById("mensagem");

async function carregar() {
  try {
    const categorias = await api.categorias.listar();
    if (categorias.length === 0) {
      cardapio.innerHTML = '<p class="vazio">Cardápio em preparação. Volte em breve!</p>';
      return;
    }
    // Busca os pratos de todas as categorias em paralelo (mais rápido).
    const porCategoria = await Promise.all(
      categorias.map((c) => api.pratos.listarPorCategoria(c.id))
    );
    cardapio.innerHTML = categorias
      .map((categoria, i) => montarCategoria(categoria, porCategoria[i]))
      .join("");
  } catch (erro) {
    mostrarMensagem(mensagem, "Não foi possível carregar o cardápio.", "erro");
  }
}

function montarCategoria(categoria, pratos) {
  // No cardápio público mostramos só os pratos disponíveis.
  const disponiveis = pratos.filter((p) => p.disponivel);
  const itens = disponiveis.length
    ? disponiveis.map(montarPrato).join("")
    : '<p class="vazio">Sem pratos disponíveis nesta categoria no momento.</p>';
  return `
    <section>
      <h2>${escapar(categoria.nome)}</h2>
      ${categoria.descricao ? `<p>${escapar(categoria.descricao)}</p>` : ""}
      ${itens}
    </section>`;
}

function montarPrato(prato) {
  return `
    <div class="cartao">
      <h3>${escapar(prato.nome)}</h3>
      ${prato.descricao ? `<p>${escapar(prato.descricao)}</p>` : ""}
      <span class="preco">${formatarPreco(prato.preco)}</span>
    </div>`;
}

carregar();
