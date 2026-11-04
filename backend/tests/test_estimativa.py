"""RF07/D05: contagens separadas e limites de amostra 0, 9, 10 e 11."""

from datetime import date
from uuid import uuid4

import pytest

from app.core import config
from app.models import Campus, Cardapio, Intencao, TipoRefeicao
from tests.test_cardapio_api import criar_cardapio_de_teste


@pytest.fixture()
def refeicao(db_session, definir_agora):
    definir_agora(2026, 9, 15, 9)
    return criar_cardapio_de_teste(db_session)


def adicionar(db, cardapio, quantidade, *, simulada=False, ativa=True):
    for _ in range(quantidade):
        db.add(Intencao(
            cardapio_id=cardapio.id, identidade=uuid4(), ativa=ativa, simulada=simulada,
        ))
    db.commit()


def consultar(client, cardapio, **filtros):
    return client.get('/estimativas/', params={
        'campus_id': cardapio.campus_id,
        'data_inicio': '2026-09-15',
        'data_fim': '2026-09-15',
        **filtros,
    })


@pytest.mark.parametrize('quantidade', [0, 9, 10, 11])
def test_limites_da_amostra(client, db_session, refeicao, quantidade):
    adicionar(db_session, refeicao, quantidade)

    resposta = consultar(client, refeicao)

    assert resposta.status_code == 200
    assert resposta.headers['cache-control'] == 'no-store'
    [resultado] = resposta.json()
    assert resultado['cardapio_id'] == refeicao.id
    assert resultado['campus_id'] == refeicao.campus_id
    assert resultado['data'] == '2026-09-15'
    assert resultado['tipo_refeicao'] == 'almoco'
    assert resultado['data_inicio'] == resultado['data_fim'] == '2026-09-15'
    assert resultado['calculado_em'] == '2026-09-15T09:00:00-03:00'
    assert resultado['dados_simulados'] is False
    assert resultado['amostra_minima'] == config.AMOSTRA_MINIMA_ESTIMATIVA
    assert 'fila real' in resultado['mensagem']
    if quantidade < 10:
        assert resultado['status'] == 'dados_insuficientes'
        assert 'contagem' not in resultado
    else:
        assert resultado['status'] == 'disponivel'
        assert resultado['contagem'] == quantidade
    assert 'identidade' not in resposta.text


def test_canceladas_nao_contam(client, db_session, refeicao):
    adicionar(db_session, refeicao, 9)
    adicionar(db_session, refeicao, 30, ativa=False)
    [resultado] = consultar(client, refeicao).json()
    assert resultado['status'] == 'dados_insuficientes'
    assert 'contagem' not in resultado


def test_reais_e_simuladas_nunca_se_misturam(client, db_session, refeicao):
    adicionar(db_session, refeicao, 11)
    adicionar(db_session, refeicao, 15, simulada=True)
    adicionar(db_session, refeicao, 7, simulada=True, ativa=False)
    [reais] = consultar(client, refeicao).json()
    [simuladas] = consultar(client, refeicao, dados_simulados=True).json()
    assert reais['contagem'] == 11
    assert reais['dados_simulados'] is False
    assert simuladas['contagem'] == 15
    assert simuladas['dados_simulados'] is True


def test_amostras_pequenas_nao_se_somam(client, db_session, refeicao):
    adicionar(db_session, refeicao, 9)
    adicionar(db_session, refeicao, 9, simulada=True)
    for simulados in [False, True]:
        [resultado] = consultar(client, refeicao, dados_simulados=simulados).json()
        assert resultado['status'] == 'dados_insuficientes'
        assert 'contagem' not in resultado


def test_usa_a_constante_unica_da_configuracao(client, db_session, refeicao, monkeypatch):
    adicionar(db_session, refeicao, 10)
    monkeypatch.setattr(config, 'AMOSTRA_MINIMA_ESTIMATIVA', 11)
    [resultado] = consultar(client, refeicao).json()
    assert resultado['status'] == 'dados_insuficientes'
    assert resultado['amostra_minima'] == 11
    assert 'contagem' not in resultado


def test_isola_campus_data_e_refeicao(client, db_session, refeicao):
    outro_campus = Campus(nome='Ceilândia')
    db_session.add(outro_campus)
    db_session.flush()
    outros = [
        Cardapio(campus_id=outro_campus.id, data=refeicao.data,
                 tipo_refeicao=TipoRefeicao.ALMOCO),
        Cardapio(campus_id=refeicao.campus_id, data=date(2026, 9, 16),
                 tipo_refeicao=TipoRefeicao.ALMOCO),
        Cardapio(campus_id=refeicao.campus_id, data=refeicao.data,
                 tipo_refeicao=TipoRefeicao.JANTAR),
    ]
    db_session.add_all(outros)
    db_session.commit()
    for outra in outros:
        adicionar(db_session, outra, 11)
    [resultado] = consultar(client, refeicao, tipo_refeicao='almoco').json()
    assert resultado['cardapio_id'] == refeicao.id
    assert resultado['status'] == 'dados_insuficientes'
    assert 'contagem' not in resultado


def test_lista_refeicoes_sem_intencoes_e_preserva_empates(client, db_session, refeicao):
    jantar = Cardapio(campus_id=refeicao.campus_id, data=refeicao.data,
                     tipo_refeicao=TipoRefeicao.JANTAR)
    db_session.add(jantar)
    db_session.commit()
    vazio = consultar(client, refeicao).json()
    assert len(vazio) == 2
    assert all(r['status'] == 'dados_insuficientes' for r in vazio)
    adicionar(db_session, refeicao, 10)
    adicionar(db_session, jantar, 10)
    resultados = consultar(client, refeicao).json()
    assert [r['contagem'] for r in resultados] == [10, 10]
    assert [r['cardapio_id'] for r in resultados] == [refeicao.id, jantar.id]


def test_marcacao_idempotente_e_cancelamento_repercutem_na_estimativa(client, refeicao):
    identidades = [str(uuid4()) for _ in range(10)]
    url = f'/cardapios/{refeicao.id}/intencao/'
    for identidade in identidades:
        cabecalho = {'X-Identidade': identidade}
        assert client.put(url, headers=cabecalho).status_code == 200
        assert client.put(url, headers=cabecalho).status_code == 200
    assert consultar(client, refeicao).json()[0]['contagem'] == 10
    assert client.delete(url, headers={'X-Identidade': identidades[0]}).status_code == 200
    [resultado] = consultar(client, refeicao).json()
    assert resultado['status'] == 'dados_insuficientes'
    assert 'contagem' not in resultado
    assert all(identidade not in str(resultado) for identidade in identidades)


@pytest.mark.parametrize('filtros', [
    {'data_inicio': '2026-09-16'},
    {'data_inicio': 'invalida'},
    {'tipo_refeicao': 'lanche'},
    {'campus_id': 0},
    {'dados_simulados': 'invalido'},
])
def test_recusa_filtros_invalidos(client, refeicao, filtros):
    assert consultar(client, refeicao, **filtros).status_code == 422


def test_campus_inexistente_404_e_sem_refeicoes_lista_vazia(client, db_session, refeicao):
    assert consultar(client, refeicao, campus_id=999).status_code == 404
    vazio = Campus(nome='Sem publicação')
    db_session.add(vazio)
    db_session.commit()
    assert consultar(client, refeicao, campus_id=vazio.id).json() == []


def test_recorte_explicito_obrigatorio(client):
    assert client.get('/estimativas/').status_code == 422


def test_preflight_ja_permite_as_chamadas_do_planejamento(client, refeicao):
    resposta = client.options(f'/cardapios/{refeicao.id}/intencao/', headers={
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'PUT',
        'Access-Control-Request-Headers': 'X-Identidade',
    })
    assert resposta.status_code == 200
    assert resposta.headers['access-control-allow-origin'] == 'http://localhost:5173'
    assert 'PUT' in resposta.headers['access-control-allow-methods']
