// ---------- estado ----------
let usuarioLogado = null;   // { codigo_medico, usuario, ato }
let produtos = [];          // lista vinda do banco

// ---------- atalhos ----------
const $ = (id) => document.getElementById(id);

async function api(caminho, opcoes) {
  const resposta = await fetch(caminho, opcoes);
  const corpo = await resposta.json();
  if (!resposta.ok) throw new Error(corpo.detail || 'Erro no servidor');
  return corpo;
}

// ================= LOGIN =================
$('form-login').addEventListener('submit', async (evento) => {
  evento.preventDefault();
  $('erro-login').textContent = '';

  try {
    usuarioLogado = await api('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        usuario: $('login-usuario').value,
        senha: $('login-senha').value,
      }),
    });

    produtos = await api('/produtos');

    $('tela-login').classList.add('escondido');
    $('tela-forms').classList.remove('escondido');
    $('usuario-logado').textContent = `${usuarioLogado.usuario} - ${usuarioLogado.ato}`;

    novoFormulario();
  } catch (erro) {
    $('erro-login').textContent = erro.message;
  }
});

// botão X: fecha o forms e volta para o login
$('btn-fechar').addEventListener('click', () => {
  usuarioLogado = null;
  $('form-login').reset();
  $('erro-login').textContent = '';
  $('tela-forms').classList.add('escondido');
  $('tela-login').classList.remove('escondido');
});

// ================= CAMPOS 1 e 2 =================
$('btn-gerar').addEventListener('click', async () => {
  const comanda = await api('/comanda/nova');
  $('numero-comanda').value = comanda.numero_comanda;
  $('tipo-comanda').value = comanda.tipo_comanda;
});

// ================= CAMPO 3 -> preenche 4,5,6,7,8 =================
$('btn-ok-leito').addEventListener('click', buscarLeito);

$('leito').addEventListener('keydown', (evento) => {
  if (evento.key === 'Enter') {
    evento.preventDefault();
    buscarLeito();
  }
});

async function buscarLeito() {
  $('erro-leito').textContent = '';
  const leito = $('leito').value;

  if (!leito) {
    $('erro-leito').textContent = 'Informe o leito';
    return;
  }

  try {
    const paciente = await api(`/paciente/${leito}`);
    $('setor').value = paciente.setor;
    $('id-paciente').value = paciente.id_paciente;
    $('nome-paciente').value = paciente.paciente;
    $('convenio').value = paciente.convenio;
    $('data').value = paciente.data;
    $('hora').value = paciente.hora;
  } catch (erro) {
    limparPaciente();
    $('erro-leito').textContent = erro.message;
  }
}

function limparPaciente() {
  ['setor', 'id-paciente', 'nome-paciente', 'convenio', 'data', 'hora']
    .forEach((id) => { $(id).value = ''; });
}

// ================= CAMPOS 8, 9 e 10 (produtos) =================
function adicionarLinhaProduto() {
  const linha = $('modelo-produto').content.firstElementChild.cloneNode(true);
  const seletor = linha.querySelector('.produto-select');

  produtos.forEach((produto) => {
    const opcao = document.createElement('option');
    opcao.value = produto.id;
    opcao.textContent = produto.nome_produto;
    seletor.appendChild(opcao);
  });

  // ao escolher o produto, preenche o id (campo 8) e o nome (campo 9)
  seletor.addEventListener('change', () => {
    const produto = produtos.find((p) => String(p.id) === seletor.value);
    linha.querySelector('.produto-id').value = produto ? produto.id : '';
    linha.querySelector('.produto-nome').value = produto ? produto.nome_produto : '';
  });

  linha.querySelector('.btn-remover').addEventListener('click', () => {
    const linhas = document.querySelectorAll('.linha-produto');
    if (linhas.length > 1) linha.remove();
  });

  $('lista-produtos').appendChild(linha);
}

$('btn-add-produto').addEventListener('click', adicionarLinhaProduto);

// ================= CONFIRMAR =================
$('form-comanda').addEventListener('submit', async (evento) => {
  evento.preventDefault();
  $('erro-comanda').textContent = '';

  if (!$('numero-comanda').value) {
    $('erro-comanda').textContent = 'Gere o número da comanda';
    return;
  }

  if (!$('id-paciente').value) {
    $('erro-comanda').textContent = 'Informe um leito válido';
    return;
  }

  const itens = [];
  document.querySelectorAll('.linha-produto').forEach((linha) => {
    const id = linha.querySelector('.produto-id').value;
    if (id) {
      itens.push({
        produto_id: Number(id),
        quantidade: Number(linha.querySelector('.produto-qtd').value),
      });
    }
  });

  if (itens.length === 0) {
    $('erro-comanda').textContent = 'Selecione ao menos um produto';
    return;
  }

  try {
    const resultado = await api('/comanda/confirmar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        numero_comanda: Number($('numero-comanda').value),
        tipo_comanda: $('tipo-comanda').value,
        leito: Number($('leito').value),
        setor: $('setor').value,
        itens: itens,
        codigo_medico: usuarioLogado.codigo_medico,
        ato: usuarioLogado.ato,
      }),
    });

    mostrarSucesso(resultado.mensagem);
  } catch (erro) {
    $('erro-comanda').textContent = erro.message;
  }
});

function mostrarSucesso(mensagem) {
  $('mensagem-sucesso').textContent = mensagem;
  $('overlay-sucesso').classList.remove('escondido');

  // depois da animação, abre um novo formulário em branco
  setTimeout(() => {
    $('overlay-sucesso').classList.add('escondido');
    novoFormulario();
  }, 1800);
}

// ================= CANCELAR =================
$('btn-cancelar').addEventListener('click', novoFormulario);

function novoFormulario() {
  $('form-comanda').reset();
  $('numero-comanda').value = '';
  $('tipo-comanda').value = '';
  limparPaciente();
  $('erro-leito').textContent = '';
  $('erro-comanda').textContent = '';

  $('lista-produtos').innerHTML = '';
  adicionarLinhaProduto();

  // campos 11 e 12 vêm do login
  $('codigo-medico').value = usuarioLogado ? usuarioLogado.codigo_medico : '';
  $('ato').value = usuarioLogado ? usuarioLogado.ato : '';
}
