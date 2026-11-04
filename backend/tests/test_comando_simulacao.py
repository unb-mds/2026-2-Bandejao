import json
import os
import subprocess
import sys
from datetime import date
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.session import Base
from app.models import Campus, Cardapio, Intencao, TipoRefeicao


def test_comando_de_simulacao_tem_ajuda():
    resultado = subprocess.run(
        [sys.executable, "-m", "app.db.simular_intencoes", "--help"],
        capture_output=True, text=True, check=False,
    )
    assert resultado.returncode == 0, resultado.stderr
    assert "criar" in resultado.stdout and "remover" in resultado.stdout


def test_comando_cria_e_remove_em_banco_isolado_preservando_reais(tmp_path):
    url = f"sqlite:///{(tmp_path / 'simulacao.db').as_posix()}"
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        campus = Campus(nome='Gama')
        db.add(campus)
        db.flush()
        cardapio = Cardapio(campus_id=campus.id, data=date(2026, 11, 4),
                            tipo_refeicao=TipoRefeicao.ALMOCO)
        db.add(cardapio)
        db.flush()
        campus_id, cardapio_id = campus.id, cardapio.id
        identidades = [uuid4(), uuid4()]
        db.add_all([
            Intencao(cardapio_id=cardapio_id, identidade=identidade, ativa=ativa)
            for identidade, ativa in zip(identidades, (True, False), strict=True)
        ])
        db.commit()

    seletores = ['--campus-id', str(campus_id), '--data', '2026-11-04',
                 '--refeicao', 'almoco']
    ambiente = {**os.environ, 'DATABASE_URL': url, 'PYTHONIOENCODING': 'utf-8'}
    for operacao in ('criar', 'remover'):
        args = [operacao, *seletores]
        if operacao == 'criar':
            args.extend(['--quantidade', '10'])
        resultado = subprocess.run(
            [sys.executable, '-m', 'app.db.simular_intencoes', *args],
            env=ambiente, capture_output=True, text=True, encoding='utf-8', check=False,
        )
        assert resultado.returncode == 0, resultado.stderr
        assert json.loads(resultado.stdout) == {
            'operacao': operacao, 'campus_id': campus_id, 'data': '2026-11-04',
            'refeicao': 'almoco', 'quantidade': 10, 'dados_simulados': True,
        }
        assert not resultado.stderr
        with Session(engine) as db:
            assert db.query(Intencao).filter_by(simulada=True).count() == (
                10 if operacao == 'criar' else 0
            )
            reais = db.query(Intencao).filter_by(simulada=False).all()
            assert {registro.identidade for registro in reais} == set(identidades)
            assert {registro.ativa for registro in reais} == {True, False}
            assert db.query(Campus).count() == db.query(Cardapio).count() == 1
    engine.dispose()
