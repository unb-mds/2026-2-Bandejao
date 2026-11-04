"""D05/#78: comando explícito, dados identificados e remoção seletiva."""

import json
import runpy
import sys
from datetime import UTC, date, datetime
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.db import simular_intencoes as simulacao
from app.models import (
    Avaliacao, Campus, Cardapio, CategoriaReclamacao, Intencao, Reclamacao, TipoRefeicao,
)
from tests.test_cardapio_api import criar_cardapio_de_teste


@pytest.fixture()
def refeicao(db_session, definir_agora):
    definir_agora(2026, 9, 15, 9)
    return criar_cardapio_de_teste(db_session)


def argumentos(refeicao, operacao='criar'):
    return [operacao, '--campus-id', str(refeicao.campus_id),
            '--data', '2026-09-15', '--refeicao', 'almoco']


def test_gera_so_intencoes_simuladas_para_a_refeicao_escolhida(db_session, refeicao):
    quantidade = simulacao.criar_simuladas(
        db_session, refeicao.campus_id, refeicao.data, refeicao.tipo_refeicao, 10,
    )
    assert quantidade == 10
    registros = db_session.query(Intencao).all()
    assert len(registros) == 10
    assert all(r.simulada and r.ativa and r.cardapio_id == refeicao.id for r in registros)
    assert len({r.identidade for r in registros}) == 10
    assert all(r.identidade.version == 4 for r in registros)


def test_remocao_preserva_dados_reais_cancelados_e_outros_recortes(db_session, refeicao):
    outro = Cardapio(campus_id=refeicao.campus_id, data=date(2026, 9, 16),
                     tipo_refeicao=TipoRefeicao.ALMOCO)
    db_session.add(outro)
    db_session.flush()
    reais = [Intencao(cardapio_id=refeicao.id, identidade=uuid4(), ativa=ativa)
             for ativa in (True, False)]
    outro_simulado = Intencao(cardapio_id=outro.id, identidade=uuid4(), simulada=True)
    avaliacao = Avaliacao(cardapio_id=refeicao.id, identidade=uuid4(), nota=4)
    reclamacao = Reclamacao(
        cardapio_id=refeicao.id, identidade=uuid4(), categoria=CategoriaReclamacao.OUTROS,
        descricao='Relato preservado', criado_em=datetime(2026, 9, 15, 15, tzinfo=UTC),
    )
    db_session.add_all([*reais, outro_simulado, avaliacao, reclamacao])
    db_session.commit()
    simulacao.criar_simuladas(db_session, refeicao.campus_id, refeicao.data,
                             refeicao.tipo_refeicao, 11)
    assert simulacao.remover_simuladas(db_session, refeicao.campus_id, refeicao.data,
                                      refeicao.tipo_refeicao) == 11
    assert db_session.query(Intencao).count() == 3
    assert db_session.query(Intencao).filter_by(simulada=False).count() == 2
    assert db_session.get(Intencao, outro_simulado.id) is not None
    assert db_session.query(Avaliacao).count() == 1
    assert db_session.query(Reclamacao).count() == 1
    assert db_session.query(Cardapio).count() == 2
    assert db_session.query(Campus).count() == 1
    assert simulacao.remover_simuladas(db_session, refeicao.campus_id, refeicao.data,
                                      refeicao.tipo_refeicao) == 0


@pytest.mark.parametrize('quantidade', [0, -1, 10001, True, 1.5])
def test_quantidade_invalida_nao_grava(db_session, refeicao, quantidade):
    with pytest.raises(ValueError, match='quantidade'):
        simulacao.criar_simuladas(db_session, refeicao.campus_id, refeicao.data,
                                 refeicao.tipo_refeicao, quantidade)
    assert db_session.query(Intencao).count() == 0


@pytest.mark.parametrize('operacao', ['criar_simuladas', 'remover_simuladas'])
def test_refeicao_inexistente_nao_cria_campus_ou_cardapio(db_session, operacao):
    args = [db_session, 999, date(2026, 9, 15), TipoRefeicao.ALMOCO]
    if operacao == 'criar_simuladas':
        args.append(10)
    with pytest.raises(ValueError, match='Refeição não encontrada'):
        getattr(simulacao, operacao)(*args)
    assert db_session.query(Campus).count() == 0
    assert db_session.query(Cardapio).count() == 0
    assert db_session.query(Intencao).count() == 0


def test_gerar_de_novo_acrescenta_registros_marcados_sem_duplicar_identidade(db_session, refeicao):
    for _ in range(2):
        simulacao.criar_simuladas(db_session, refeicao.campus_id, refeicao.data,
                                 refeicao.tipo_refeicao, 10)
    registros = db_session.query(Intencao).all()
    assert len(registros) == len({r.identidade for r in registros}) == 20


@pytest.mark.parametrize('outro_campus', [False, True])
def test_remocao_preserva_outros_campi_e_refeicoes(db_session, refeicao, outro_campus):
    campus_id = refeicao.campus_id
    if outro_campus:
        campus = Campus(nome='Outro campus')
        db_session.add(campus)
        db_session.flush()
        campus_id = campus.id
    outro = Cardapio(
        campus_id=campus_id, data=refeicao.data,
        tipo_refeicao=TipoRefeicao.ALMOCO if outro_campus else TipoRefeicao.JANTAR,
    )
    db_session.add(outro)
    db_session.flush()
    registro = Intencao(cardapio_id=outro.id, identidade=uuid4(), simulada=True)
    db_session.add(registro)
    db_session.commit()
    seletores = (db_session, refeicao.campus_id, refeicao.data, refeicao.tipo_refeicao)
    simulacao.criar_simuladas(*seletores, 1)
    assert simulacao.remover_simuladas(*seletores) == 1
    assert db_session.query(Intencao).one().id == registro.id


def test_remocao_tambem_exclui_simuladas_canceladas(db_session, refeicao):
    db_session.add(Intencao(
        cardapio_id=refeicao.id, identidade=uuid4(), ativa=False, simulada=True,
    ))
    db_session.commit()
    assert simulacao.remover_simuladas(
        db_session, refeicao.campus_id, refeicao.data, refeicao.tipo_refeicao,
    ) == 1
    assert db_session.query(Intencao).count() == 0


def test_falha_de_escrita_reverte_o_lote_inteiro(db_session, refeicao, monkeypatch):
    original = db_session.commit
    def falhar():
        db_session.flush()
        raise SQLAlchemyError('credencial=segredo-nao-pode-aparecer')
    monkeypatch.setattr(db_session, 'commit', falhar)
    with pytest.raises(SQLAlchemyError):
        simulacao.criar_simuladas(db_session, refeicao.campus_id, refeicao.data,
                                 refeicao.tipo_refeicao, 10)
    monkeypatch.setattr(db_session, 'commit', original)
    assert db_session.query(Intencao).count() == 0


def test_cli_cria_e_remove_sem_imprimir_identidades(db_session, refeicao, monkeypatch, capsys):
    # Session.close não destrói a sessão de teste; o banco descartável segue acessível.
    criar = [*argumentos(refeicao), '--quantidade', '10']
    remover = argumentos(refeicao, 'remover')
    monkeypatch.setattr(simulacao, 'SessionLocal', lambda: db_session)
    assert simulacao.main(criar) == 0
    saida = capsys.readouterr()
    resumo = json.loads(saida.out)
    assert resumo['dados_simulados'] is True
    assert resumo['quantidade'] == 10
    assert set(resumo) == {
        'operacao', 'campus_id', 'data', 'refeicao', 'quantidade', 'dados_simulados',
    }
    assert 'identidade' not in saida.out
    assert simulacao.main(remover) == 0
    assert json.loads(capsys.readouterr().out)['quantidade'] == 10
    assert db_session.query(Intencao).count() == 0


@pytest.mark.parametrize('extras', [
    ['--quantidade', '0'], ['--quantidade', '10001'], ['--quantidade', '1.5'],
    ['--quantidade', '10', '--data', '2026-02-30'],
    ['--quantidade', '10', '--data', '20260915'],
    ['--quantidade', '10', '--refeicao', 'lanche'],
    ['--quantidade', '10', '--campus-id', '0'],
])
def test_cli_recusa_argumentos_antes_de_abrir_sessao(refeicao, monkeypatch, extras):
    def proibida():
        raise AssertionError('Não deveria conectar ao banco')
    monkeypatch.setattr(simulacao, 'SessionLocal', proibida)
    with pytest.raises(SystemExit) as erro:
        simulacao.main([*argumentos(refeicao), *extras])
    assert erro.value.code == 2


@pytest.mark.parametrize('args', [
    [], ['criar'], ['remover'],
    ['criar', '--campus-id', '1', '--data', '2026-09-15', '--refeicao', 'almoco'],
    ['remover', '--campus-id', '1', '--data', '2026-09-15', '--refeicao', 'almoco',
     '--quantidade', '1'],
])
def test_cli_exige_seletores_e_quantidade_apenas_na_criacao(monkeypatch, args):
    def proibida():
        raise AssertionError('Não deveria conectar ao banco')
    monkeypatch.setattr(simulacao, 'SessionLocal', proibida)
    with pytest.raises(SystemExit) as erro:
        simulacao.main(args)
    assert erro.value.code == 2


def test_cli_trata_refeicao_ausente_sem_traceback(db_session, monkeypatch, capsys):
    monkeypatch.setattr(simulacao, 'SessionLocal', lambda: db_session)
    assert simulacao.main(['criar', '--campus-id', '999', '--data', '2026-09-15',
                           '--refeicao', 'almoco', '--quantidade', '10']) == 1
    assert 'Refeição não encontrada' in capsys.readouterr().err


def test_cli_falha_de_banco_nao_expoe_credenciais(monkeypatch, capsys):
    def falhar():
        raise SQLAlchemyError('senha=nao-imprimir')
    monkeypatch.setattr(simulacao, 'SessionLocal', falhar)
    assert simulacao.main(['remover', '--campus-id', '1', '--data', '2026-09-15',
                           '--refeicao', 'almoco']) == 1
    texto = capsys.readouterr().err
    assert 'banco' in texto.lower()
    assert 'senha' not in texto


def test_dados_gerados_aparecem_so_na_estimativa_simulada(client, db_session, refeicao):
    simulacao.criar_simuladas(db_session, refeicao.campus_id, refeicao.data,
                             refeicao.tipo_refeicao, 11)
    params = {'campus_id': refeicao.campus_id, 'data_inicio': '2026-09-15',
              'data_fim': '2026-09-15'}
    [real] = client.get('/estimativas/', params=params).json()
    [simulada] = client.get('/estimativas/', params={**params, 'dados_simulados': True}).json()
    assert real['status'] == 'dados_insuficientes'
    assert 'contagem' not in real
    assert simulada['contagem'] == 11 and simulada['dados_simulados'] is True
    simulacao.remover_simuladas(db_session, refeicao.campus_id, refeicao.data,
                              refeicao.tipo_refeicao)
    [vazia] = client.get('/estimativas/', params={**params, 'dados_simulados': True}).json()
    assert vazia['status'] == 'dados_insuficientes'


@pytest.mark.parametrize('quantidade', [1, 10000])
def test_limites_de_quantidade_sao_aceitos(db_session, refeicao, quantidade):
    assert simulacao.criar_simuladas(
        db_session, refeicao.campus_id, refeicao.data, refeicao.tipo_refeicao, quantidade,
    ) == quantidade
    assert db_session.query(Intencao).count() == quantidade


def test_falha_de_remocao_preserva_o_lote(db_session, refeicao, monkeypatch):
    seletores = (db_session, refeicao.campus_id, refeicao.data, refeicao.tipo_refeicao)
    simulacao.criar_simuladas(*seletores, 10)

    def falhar():
        raise SQLAlchemyError('postgresql://usuario:senha@host/banco')

    monkeypatch.setattr(db_session, 'commit', falhar)
    with pytest.raises(SQLAlchemyError):
        simulacao.remover_simuladas(*seletores)
    assert db_session.query(Intencao).count() == 10


def test_modulo_executa_main_e_devolve_codigo_de_saida(db_session, refeicao, monkeypatch, capsys):
    from app.db import session

    args = [*argumentos(refeicao), '--quantidade', '1']
    monkeypatch.setattr(session, 'SessionLocal', lambda: db_session)
    monkeypatch.setattr(sys, 'argv', ['app.db.simular_intencoes', *args])
    monkeypatch.delitem(sys.modules, 'app.db.simular_intencoes')
    with pytest.raises(SystemExit) as erro:
        runpy.run_module('app.db.simular_intencoes', run_name='__main__')
    assert erro.value.code == 0
    assert json.loads(capsys.readouterr().out)['quantidade'] == 1
