import os
import sqlite3

# caminho fixo do banco: sempre database/faturamento.db, não importa de onde rodar
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faturamento.db')


def conectar():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS usuarios("
        " id INTEGER PRIMARY KEY,"
        " usuario TEXT,"
        " senha TEXT,"
        " cargo TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS cliente("
        " id INTEGER PRIMARY KEY,"
        " paciente TEXT,"
        " leito INTEGER,"
        " convenio TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS produtos("
        " id INTEGER PRIMARY KEY,"
        " nome_produto TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS setores("
        " codigo INTEGER PRIMARY KEY,"
        " nome TEXT)")

    con.commit()
    con.close()


lista_usuario = [
    (1, 'matheus ferraz', '1234', 'fisioterapia'),
    (2, 'ricardo alves motta', '1234', 'enfermagem'),
    (3, 'mariana fernandes', '1234', 'médico')
]

lista_cliente = [
    (1, 'lucas da silva', 1201, 'bradesco seguros'),
    (2, 'ana beatriz de souza filho', 507, 'amil'),
    (3, 'marcos antônio', 905, 'sulamérica'),
    (4, 'fernanda ribeiro da silva', 302, 'bradesco seguros'),
    (5, 'carlos bruno batista', 707, 'porto seguro saúde')
]

lista_produto = [
    (1, 'fisioterapia respiratória'),
    (2, 'fisioterapia cinesioterapia'),
    (3, 'fisioterapia motora'),
    (4, 'aspiração traqueal'),
    (5, 'ventilação mecânica não invasiva')
]

# cada setor comeca no seu codigo e vai ate codigo + 17 (18 leitos no total).
# ex: 1301 atende do leito 1301 ao 1318.
LEITOS_POR_SETOR = 18

lista_setor = [
    (101, 'CTI geral'),
    (201, 'pediatria'),
    (301, 'internação'),
    (401, 'pediatria'),
    (501, 'pós operatório'),
    (601, 'cuidados especiais'),
    (701, 'cardio intensiva'),
    (801, 'semi intensiva'),
    (901, 'semi intensiva'),
    (1001, 'internação'),
    (1201, 'internação vip'),
    (1301, 'internação')
]


def popular_tabelas():
    con = conectar()
    cur = con.cursor()
    cur.executemany('INSERT OR IGNORE INTO usuarios VALUES(?,?,?,?)', lista_usuario)
    cur.executemany('INSERT OR IGNORE INTO cliente VALUES(?,?,?,?)', lista_cliente)
    cur.executemany('INSERT OR IGNORE INTO produtos VALUES(?,?)', lista_produto)
    cur.executemany('INSERT OR IGNORE INTO setores VALUES(?,?)', lista_setor)
    con.commit()
    con.close()


# ---------- consultas usadas pela API ----------

def get_usuario(login_usuario, login_senha):
    """Retorna o usuário se nome e senha baterem, senão None."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        'SELECT id, usuario, cargo FROM usuarios WHERE usuario = ? AND senha = ?',
        (login_usuario.strip().lower(), login_senha))
    resultado = cur.fetchone()
    con.close()
    return dict(resultado) if resultado else None


def get_cliente_por_leito(leito):
    """Retorna o paciente daquele leito, senão None."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        'SELECT id, paciente, leito, convenio FROM cliente WHERE leito = ?',
        (leito,))
    resultado = cur.fetchone()
    con.close()
    return dict(resultado) if resultado else None


def get_setor(leito):
    """Descobre o setor pelo numero do leito, senão None.

    Nao olha os digitos iniciais de proposito: compara o leito com a faixa
    de cada setor (codigo ate codigo + 17). Assim nao existe confusao entre
    o 1o andar e os andares 10, 12 e 13, porque as faixas nao se cruzam
    (101-118, 1001-1018, 1201-1218, 1301-1318).
    """
    con = conectar()
    cur = con.cursor()
    cur.execute(
        'SELECT codigo, nome FROM setores WHERE ? BETWEEN codigo AND codigo + ?',
        (leito, LEITOS_POR_SETOR - 1))
    resultado = cur.fetchone()
    con.close()
    return dict(resultado) if resultado else None


def listar_setores():
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT codigo, nome FROM setores ORDER BY codigo')
    resultado = cur.fetchall()
    con.close()
    return [dict(linha) for linha in resultado]


def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT id, nome_produto FROM produtos ORDER BY id')
    resultado = cur.fetchall()
    con.close()
    return [dict(linha) for linha in resultado]


def get_produto(produto_id):
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT id, nome_produto FROM produtos WHERE id = ?', (produto_id,))
    resultado = cur.fetchone()
    con.close()
    return dict(resultado) if resultado else None


def iniciar_banco():
    criar_tabelas()
    popular_tabelas()


if __name__ == '__main__':
    iniciar_banco()
    print(f'Banco criado em: {DB_PATH}')
    print(f'usuários: {len(lista_usuario)} | clientes: {len(lista_cliente)} | produtos: {len(listar_produtos())}')
