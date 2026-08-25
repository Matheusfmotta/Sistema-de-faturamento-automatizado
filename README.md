Objetivo:

Percebi que no meu trabalho atual, o sistema de faturamento é muito manual e poderia ser automatizado reduzindo muito o tempo de faturamento

O que iremos desenvolver:

A ideia é reproduzir uma parte do fluxo do sistema de faturamento do meu trabalho porém de forma automatizada, mais clara e simples.
Para isso, teremos dois pontos importante, primeiro é o banco de dados armazenando informações, uma API REST com fastapi no backend, um frontend. O segundo ponto importante são as regras do sistema para automatizar que estaram em outro tópico mais abaixo 

O que eu fiz até agora:
Criei uma venv, iniciei o git e fiz o primeiro commit antes de começar usar o claude, já criei o banco de dados com as informações necessárias e adicionei valores dentro dele(no script, ainda não rodei esse código). Eu criei um arquivo sistema_faturamento aonde iria começar aplicar as regras e endpoints da API

Seu papel:
Me ajudar a construir esse sistema já utilizando partes do meu código, esse sistema não é profissional, então não precisamos ter um código como se fosse feito por senior, vamos trabalhar de forma simples e certeira, seu papel também é entender minha encessidade com esse projeto e minhas especificações, caso haja dúvidas, sempre me pergunte antes

tecnologias:
vamos usar slite3 para o banco de dados com persistencia em arquivos, nada de temporario. Iremos utilizar o framework fastapi, python para o backend e javascript, html e css para o frontend(não domino frontend, caso tenha opções melhores e novas ideias me avise antes)

segurança:
Não vamos usar chaves de API ou algo assim, todo conteúdo no banco de dados reflete um exemplo somente, não se preocupe com segurança de informações

frontend da aplicação: 
A aplicação original é um frontend bem antigo e legado, o design é velho e com muitas informações. Iremos aprimorar tudo isso em design, o fundo deve permanecer branco e a frente deve abrir um forms com cores em degrade, de forma suave e simples, para saber o que implementar no forms, leia "segundo ponto, as regras do sistema para automatizar:"

segundo ponto, as regras do sistema para automatizar:
o frontend deve conter uma aba de login de usuario e senha(Sem JWT no momento, isso irei estudar para implementar sozinho depois) a forma de autenticar o usuário pode ser uma forma padrão(verificar o nome dele e a senha no banco de dados batem com as informações do login). Após isso abrirá a tela de fundo branco com o forms centralizado no meio. O título do forms deve tá escrito como (movimentação de comandas)

abaixo segue cada campo, seguido com seu título e a informação que deve conter:

campo um, número da comanda, id aleatório entre 1000 a 3000 já gerado em def gerar_id_faturament, não há problema se repetir o id, faturamentos não devem ser salvos
campo dois, tipo de comanda, preencher como honorário logo após gerar o número de comanda no campo um

campo tres, leito do paciente, escrever o leito que o paciente está e automaticamente essa informação deve preencher o nome completo do paciente, o id no paciente

campo quatro do paciente
campo cinco, nome completo
campo seis convenio do paciente
campo sete, data, irá puxar o dia atual na função def data_hora_atual():
campo oito, hora, irá puxar a hora atual na função def data_hora_atual():

ATENÇÃO(clicar em gerar número de comanda erá preencher o campo 1 e automaticamente o campo 2. Escrever o leito e dar ok deve preencher automaticamente os campos 4,5,6,7,8)

ainda no formulário, porém um pouco mais abaixo, deve conter em uma única linha:

campo 8, produtos, está relacionado com a tabela produtos, deve aparecer para selecionar os produtos que tem na lista, o usuário clica no produto que quer e no campo 8 aparece o id do produto
campo 9, nome do produto que será preenchido automaticamente após preencher o campo 8 pois eles se relacionam
campo 10, quantidade, esse campo deve ser para o usuário colocar o número de vezes que o produto foi ofertado, pode ser um campo com setinhas pra cima e para baixo aonde se clica para aumentar ou para diminuir

na linha abaixo uma opção para adicionar um novo produto, caso seja clicado em adicionar um novo produto irá abrir uma nova linha identica aos campos 8,9,10

mais abaixo, quase no final, deve aparecer:
campo11, código médico, aqui deve conter o id da pessoa que fez o login, deve ser preencido automaticamente logo após o login
campo 12, ato, esse campo deve ser preenchido com o cargo do usuário que fez login, exemplo, se quem fez login foi matheus ferraz, esse campo deve aparecer escrito fisioterapia(será preenchido automaticamente ao fazer o login)

no final do forms deve conter dois botões, um escrito confirmar e outro cancelar.
botão confirmar -> animação de tela dizendo que a comanda do faturamento foi salva com sucesso -> em seguida abre um novo forms para preencher
botão cancelar -> reseta as informações escritas no forms, para começar a escrever de novo

no topo do forms deve ter um X que serve para fechar e voltar para tela de login
