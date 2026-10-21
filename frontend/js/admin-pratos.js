// admin-pratos.js — tela de administração dos pratos de UMA categoria (CRUD).
import { api, ErroApi } from "./api.js";
import { exigirLogin, limparToken } from "./auth.js";
import {
  mostrarMensagem,
  esconderMensagem,
  formatarPreco,
  escapar,
  parametroUrl,
} from "./ui.js";

exigirLogin();

// Qual categoria estamos editando? Vem da URL: admin-pratos.html?categoria=ID
const categoriaId = Number(parametroUrl("categoria"));

const form = document.getElementById("form-prato");
const campoId = document.getElementById("prato-id");
const campoNome = document.getElementById("nome");
const campoDescricao = document.getElementById("descricao");
const campoPreco = document.getElementById("preco");
const campoDisponivelBox = document.getElementById("campo-disponivel");
const campoDisponivel = document.getElementById("disponivel");
const btnSalvar = document.getElementById("btn-salvar");
const btnCancelar = document.getElementById("btn-cancelar");
const lista = document.getElementById("lista-pratos");
const mensagem = document.getElementById("mensagem");
const titulo = document.getElementById("titulo");

document.getElementById("link-sair").addEventListener("click", (e) => {
  e.preventDefault();
  limparToken();
  window.location.href = "login.html";
});

// Mostra o nome da categoria no título e carrega os pratos.
async function iniciar() {
  if (!categoriaId) {
    mostrarMensagem(mensagem, "Categoria não informada.", "erro");
    return;
  }
  try {
    const categoria = await api.categorias.obter(categoriaId);
    titulo.textContent = `Pratos — ${categoria.nome}`;
  } catch (erro) {
    tratarErro(erro);
  }
  await carregar();
}

async function carregar() {
  try {
    const pratos = await api.pratos.listarPorCategoria(categoriaId);
    lista.innerHTML = pratos.length
      ? pratos.map(montarLinha).join("")
      : '<tr><td colspan="4" class="vazio">Nenhum prato cadastrado.</td></tr>';
  } catch (erro) {
    tratarErro(erro);
  }
}

function montarLinha(prato) {
  const etiqueta = prato.disponivel
    ? '<span class="etiqueta etiqueta-disponivel">Disponível</span>'
    : '<span class="etiqueta etiqueta-indisponivel">Indisponível</span>';
  return `
    <tr>
      <td>${escapar(prato.nome)}</td>
      <td>${formatarPreco(prato.preco)}</td>
      <td>${etiqueta}</td>
      <td class="acoes">
        <button data-acao="editar" data-id="${prato.id}">Editar</button>
        <button class="botao-perigo" data-acao="excluir" data-id="${prato.id}">Excluir</button>
      </td>
    </tr>`;
}

lista.addEventListener("click", async (evento) => {
  const botao = evento.target.closest("button");
  if (!botao) return;
  const id = Number(botao.dataset.id);

  if (botao.dataset.acao === "editar") {
    await entrarEmModoEdicao(id);
  } else if (botao.dataset.acao === "excluir") {
    if (!confirm("Excluir este prato?")) return;
    try {
      await api.pratos.excluir(id);
      mostrarMensagem(mensagem, "Prato excluído.", "sucesso");
      await carregar();
    } catch (erro) {
      tratarErro(erro);
    }
  }
});

// Busca os dados do prato e preenche o formulário para edição.
async function entrarEmModoEdicao(id) {
  try {
    const prato = await api.pratos.obter(id);
    campoId.value = prato.id;
    campoNome.value = prato.nome;
    campoDescricao.value = prato.descricao || "";
    campoPreco.value = prato.preco;
    campoDisponivel.checked = prato.disponivel;
    campoDisponivelBox.hidden = false; // o toggle só aparece na edição
    btnSalvar.textContent = "Salvar alterações";
    btnCancelar.hidden = false;
    campoNome.focus();
  } catch (erro) {
    tratarErro(erro);
  }
}

function sairDoModoEdicao() {
  form.reset();
  campoId.value = "";
  campoDisponivel.checked = true;
  campoDisponivelBox.hidden = true;
  btnSalvar.textContent = "Adicionar prato";
  btnCancelar.hidden = true;
}

btnCancelar.addEventListener("click", sairDoModoEdicao);

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  esconderMensagem(mensagem);
  const dados = {
    nome: campoNome.value,
    descricao: campoDescricao.value || null,
    preco: campoPreco.value,
  };
  try {
    if (campoId.value) {
      // Na edição enviamos também a disponibilidade escolhida no checkbox.
      dados.disponivel = campoDisponivel.checked;
      await api.pratos.atualizar(Number(campoId.value), dados);
      mostrarMensagem(mensagem, "Prato atualizado.", "sucesso");
    } else {
      // Na criação não mandamos 'disponivel': o back-end já assume disponível.
      await api.pratos.criar(categoriaId, dados);
      mostrarMensagem(mensagem, "Prato criado.", "sucesso");
    }
    sairDoModoEdicao();
    await carregar();
  } catch (erro) {
    tratarErro(erro); // mostra o 422 "preço maior que zero", por exemplo
  }
});

function tratarErro(erro) {
  if (erro instanceof ErroApi && erro.status === 401) {
    window.location.href = "login.html";
    return;
  }
  const texto = erro instanceof ErroApi ? erro.message : "Erro de conexão.";
  mostrarMensagem(mensagem, texto, "erro");
}

iniciar();
