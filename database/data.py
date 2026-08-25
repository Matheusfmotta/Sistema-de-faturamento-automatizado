import sqlite3

con = sqlite3.connect('faturamento.db')
cur = con.cursor()

cur.execute(
    " CREATE TABLE IF NOT EXISTS usuarios(" \
    " id INTERGER PRIMARY KEY," \
    " usuario TEXT," \
    " cargo TEXT)")
con.commit()
con.close()

cur.execute(
    " CREATE TABLE IF NOT EXISTS cliente(" \
    " id INTERGER PRIMARY KEY," \
    " paciente TEXT," \
    " leito INTERGER" \
    " convenio TEXT)")
con.commit()
con.close()

cur.execute(
    " CREATE TABLE IF NOT EXISTS produtos(" \
    " id INTERGER," \
    " nome_produto TEXT)")
con.commit()
con.close()

lista_usuario = [
    (1, 'matheus ferraz', 'fisioterapia'),
    (2, 'ricardo alves motta', 'enfermagem'),
    (3, 'mariana fernandes', 'medico')
]

lista_cliente = [
    (1, 'lucas da silva', 1201, 'bradesco seguros'),
    (2, 'ana beatriz de souza filho', 507, 'amil'),
    (3, 'marcos antonio', 1111, 'sulamerica'),
    (4, 'fernanda ribeiro da silva', 302, 'bradesco seguros'),
    (5, 'carlos bruno batista', 707, 'porto seguro saúde')
]

lista_produto = [
    (1, 'fisioterapia respiratória'),
    (2, 'fisioterapia cinesioterapia')
]

cur.executemany('INSERT OR IGNORE INTO usuarios VALUES(?,?,?)', lista_usuario)
con.commit()
con.close()

cur.executemany('INSERT OR IGNORE INTO cliente VALUES(?,?,?,?)', lista_cliente)
con.commit()
con.close()

cur.executemany('INSERT OR IGNORE INTO produtos VALUES(?,?)', lista_produto)
con.commit()
con.close()

#PAREI AQUI
def get_usuario(login_usuario):
    cur.execute('SELECT usuario FROM usuarios WHERE usuario == login_usuario')
    resultado = cur.fetchone()
   
    