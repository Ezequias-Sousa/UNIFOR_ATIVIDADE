// admin-categorias.js — tela de administração das categorias (CRUD completo).
import { api, ErroApi } from "./api.js";
import { exigirLogin, limparToken } from "./auth.js";
import { mostrarMensagem, esconderMensagem, escapar } from "./ui.js";

exigirLogin(); // bloqueia a página se não houver token

const form = document.getElementById("form-categoria");
const campoId = document.getElementById("categoria-id");
const campoNome = document.getElementById("nome");
const campoDescricao = document.getElementById("descricao");
const btnSalvar = document.getElementById("btn-salvar");
const btnCancelar = document.getElementById("btn-cancelar");
const lista = document.getElementById("lista-categorias");
const mensagem = document.getElementById("mensagem");

// Botão "Sair": limpa o token e volta ao login.
document.getElementById("link-sair").addEventListener("click", (e) => {
  e.preventDefault();
  limparToken();
  window.location.href = "login.html";
});

// Carrega e desenha a tabela de categorias.
async function carregar() {
  try {
    const categorias = await api.categorias.listar();
    lista.innerHTML = categorias.length
      ? categorias.map(montarLinha).join("")
      : '<tr><td colspan="3" class="vazio">Nenhuma categoria cadastrada.</td></tr>';
  } catch (erro) {
    tratarErro(erro);
  }
}

function montarLinha(categoria) {
  // As ações ficam com data-id para o clique saber qual categoria é.
  return `
    <tr>
      <td>${escapar(categoria.nome)}</td>
      <td>${escapar(categoria.descricao) || "—"}</td>
      <td class="acoes">
        <a class="botao" href="admin-pratos.html?categoria=${categoria.id}">Pratos</a>
        <button data-acao="editar" data-id="${categoria.id}"
                data-nome="${escapar(categoria.nome)}"
                data-descricao="${escapar(categoria.descricao) || ""}">Editar</button>
        <button class="botao-perigo" data-acao="excluir" data-id="${categoria.id}">Excluir</button>
      </td>
    </tr>`;
}

// Um único "ouvinte" na tabela cuida de editar e excluir (delegação de eventos).
lista.addEventListener("click", async (evento) => {
  const botao = evento.target.closest("button");
  if (!botao) return;
  const id = Number(botao.dataset.id);

  if (botao.dataset.acao === "editar") {
    entrarEmModoEdicao(id, botao.dataset.nome, botao.dataset.descricao);
  } else if (botao.dataset.acao === "excluir") {
    if (!confirm("Excluir esta categoria?")) return;
    try {
      await api.categorias.excluir(id);
      mostrarMensagem(mensagem, "Categoria excluída.", "sucesso");
      await carregar();
    } catch (erro) {
      tratarErro(erro); // mostra o 409 "possui pratos", por exemplo
    }
  }
});

// Preenche o formulário para edição.
function entrarEmModoEdicao(id, nome, descricao) {
  campoId.value = id;
  campoNome.value = nome;
  campoDescricao.value = descricao;
  btnSalvar.textContent = "Salvar alterações";
  btnCancelar.hidden = false;
  campoNome.focus();
}

function sairDoModoEdicao() {
  form.reset();
  campoId.value = "";
  btnSalvar.textContent = "Adicionar categoria";
  btnCancelar.hidden = true;
}

btnCancelar.addEventListener("click", sairDoModoEdicao);

// Envio do formulário: cria (sem id) ou atualiza (com id).
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  esconderMensagem(mensagem);
  const dados = { nome: campoNome.value, descricao: campoDescricao.value || null };
  try {
    if (campoId.value) {
      await api.categorias.atualizar(Number(campoId.value), dados);
      mostrarMensagem(mensagem, "Categoria atualizada.", "sucesso");
    } else {
      await api.categorias.criar(dados);
      mostrarMensagem(mensagem, "Categoria criada.", "sucesso");
    }
    sairDoModoEdicao();
    await carregar();
  } catch (erro) {
    tratarErro(erro); // mostra o 409 "nome já existe", por exemplo
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

carregar();
