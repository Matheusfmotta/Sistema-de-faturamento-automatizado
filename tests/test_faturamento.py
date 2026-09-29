import pytest

from backend.sistema_faturamento import gerar_id_faturamento
from database import data


@pytest.fixture(autouse=True)
def banco_temporario(tmp_path, monkeypatch):
    # cada teste usa um banco novo em pasta temporária, sem tocar no faturamento.db real
    monkeypatch.setattr(data, 'DB_PATH', str(tmp_path / 'teste.db'))
    data.iniciar_banco()


def test_setor_encontrado_pelo_leito():
    assert data.get_setor(101)['nome'] == 'CTI geral'


def test_leito_do_11_andar_nao_tem_setor():
    assert data.get_setor(1101) is None


def test_login_ignora_espacos_e_maiusculas():
    usuario = data.get_usuario('  Matheus Ferraz ', '1234')
    assert usuario['cargo'] == 'fisioterapia'


def test_login_com_senha_errada():
    assert data.get_usuario('matheus ferraz', 'errada') is None


def test_paciente_encontrado_pelo_leito():
    assert data.get_cliente_por_leito(507)['convenio'] == 'amil'


def test_numero_da_comanda_fica_na_faixa():
    assert 1000 <= gerar_id_faturamento() <= 3000
