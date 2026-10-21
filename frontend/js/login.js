// login.js — lógica da tela de login.
import { api, ErroApi } from "./api.js";
import { salvarToken } from "./auth.js";
import { mostrarMensagem } from "./ui.js";

const form = document.getElementById("form-login");
const mensagem = document.getElementById("mensagem");

form.addEventListener("submit", async (evento) => {
  evento.preventDefault(); // impede o recarregamento padrão do formulário
  try {
    const usuario = document.getElementById("usuario").value;
    const senha = document.getElementById("senha").value;
    const resposta = await api.login(usuario, senha);
    salvarToken(resposta.access_token); // guarda o token e entra na área admin
    window.location.href = "admin-categorias.html";
  } catch (erro) {
    const texto = erro instanceof ErroApi ? erro.message : "Falha ao conectar.";
    mostrarMensagem(mensagem, texto, "erro");
  }
});
