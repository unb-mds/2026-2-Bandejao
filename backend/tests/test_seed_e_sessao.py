import runpy

from sqlalchemy.orm import Session

from app.db import seed
from app.db import session as session_module
from app.models import Avaliacao, Campus, Cardapio, ItemCardapio


def test_get_db_fecha_a_sessao(monkeypatch):
    class SessaoFalsa:
        fechada = False

        def close(self):
            self.fechada = True

    sessao = SessaoFalsa()
    monkeypatch.setattr(session_module, "SessionLocal", lambda: sessao)

    gerador = session_module.get_db()

    assert next(gerador) is sessao
    gerador.close()
    assert sessao.fechada


def test_seed_popula_dados_e_eh_idempotente(
    db_session: Session, monkeypatch, capsys
):
    monkeypatch.setattr(seed, "SessionLocal", lambda: db_session)

    seed.seed()
    # A segunda execução não pode duplicar o campus e seus dados dependentes.
    seed.seed()

    assert db_session.query(Campus).count() == 1
    assert db_session.query(Cardapio).count() == 1
    assert db_session.query(ItemCardapio).count() == 6
    assert db_session.query(Avaliacao).count() == 1
    assert "Campus: Gama" in capsys.readouterr().out


def test_seed_executa_como_modulo(db_session: Session, monkeypatch):
    monkeypatch.setattr(session_module, "SessionLocal", lambda: db_session)

    # Garante que o atalho `python -m app.db.seed` também permanece funcional.
    runpy.run_module("app.db.seed", run_name="__main__")

    assert db_session.query(Campus).filter_by(nome="Gama").one_or_none() is not None
