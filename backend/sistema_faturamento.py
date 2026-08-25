import os
import random
import sys
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# permite importar a pasta database mesmo rodando de dentro de backend/
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(RAIZ)

from database import data

FRONTEND = os.path.join(RAIZ, 'frontend')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # cria as tabelas e insere os dados de exemplo quando a API sobe
    data.iniciar_banco()
    yield


app = FastAPI(title='Sistema de Faturamento Automatizado', lifespan=lifespan)


# ---------- funções do sistema ----------

def gerar_id_faturamento():
    return random.randint(1000, 3000)


def data_hora_atual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ---------- modelos ----------

class Login(BaseModel):
    usuario: str
    senha: str


class ItemComanda(BaseModel):
    produto_id: int
    quantidade: int


class Comanda(BaseModel):
    numero_comanda: int
    tipo_comanda: str
    leito: int
    setor: str
    itens: list[ItemComanda]
    codigo_medico: int
    ato: str


# ---------- endpoints ----------

@app.post('/login')
def login(dados: Login):
    usuario = data.get_usuario(dados.usuario, dados.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail='Usuário ou senha inválidos')
    # codigo_medico = id do usuário | ato = cargo do usuário
    return {
        'codigo_medico': usuario['id'],
        'usuario': usuario['usuario'],
        'ato': usuario['cargo'],
    }


@app.get('/comanda/nova')
def nova_comanda():
    """Campo 1 e campo 2: gera o número e já define o tipo como honorário."""
    return {
        'numero_comanda': gerar_id_faturamento(),
        'tipo_comanda': 'honorário',
    }


@app.get('/paciente/{leito}')
def paciente_por_leito(leito: int):
    """Preenchidos a partir do leito: setor, paciente, convênio, data e hora."""
    setor = data.get_setor(leito)
    if not setor:
        raise HTTPException(
            status_code=404,
            detail=f'Leito {leito} não pertence a nenhum setor cadastrado')

    cliente = data.get_cliente_por_leito(leito)
    if not cliente:
        raise HTTPException(status_code=404, detail=f'Nenhum paciente no leito {leito}')

    data_hora = data_hora_atual()
    dia, hora = data_hora.split(' ')
    return {
        'setor': setor['nome'],
        'id_paciente': cliente['id'],
        'paciente': cliente['paciente'],
        'convenio': cliente['convenio'],
        'data': dia,
        'hora': hora,
    }


@app.get('/setores')
def setores():
    """Lista os setores e a faixa de leitos de cada um."""
    return [
        {
            'codigo': setor['codigo'],
            'nome': setor['nome'],
            'faixa': f"{setor['codigo']} a {setor['codigo'] + data.LEITOS_POR_SETOR - 1}",
        }
        for setor in data.listar_setores()
    ]


@app.get('/produtos')
def produtos():
    return data.listar_produtos()


@app.post('/comanda/confirmar')
def confirmar_comanda(comanda: Comanda):
    """Valida a comanda e devolve sucesso. Nada é gravado no banco."""
    if not comanda.itens:
        raise HTTPException(status_code=400, detail='Adicione ao menos um produto')

    if not data.get_cliente_por_leito(comanda.leito):
        raise HTTPException(status_code=400, detail='Leito inválido')

    # o setor vem preenchido pela tela, mas conferimos de novo aqui
    setor = data.get_setor(comanda.leito)
    if not setor or setor['nome'] != comanda.setor:
        raise HTTPException(status_code=400, detail='Setor não confere com o leito')

    for item in comanda.itens:
        if not data.get_produto(item.produto_id):
            raise HTTPException(status_code=400, detail=f'Produto {item.produto_id} não existe')
        if item.quantidade < 1:
            raise HTTPException(status_code=400, detail='Quantidade deve ser no mínimo 1')

    return {
        'mensagem': f'Comanda {comanda.numero_comanda} faturada com sucesso!',
        'confirmado_em': data_hora_atual(),
    }


# ---------- frontend ----------

@app.get('/')
def index():
    return FileResponse(os.path.join(FRONTEND, 'index.html'))


app.mount('/static', StaticFiles(directory=FRONTEND), name='static')
