from datetime import date, datetime, timezone

import pytest

from app.core.tempo import limites_da_semana


@pytest.mark.parametrize(
    ("referencia", "inicio", "fim"),
    [
        (date(2026, 10, 12), date(2026, 10, 12), date(2026, 10, 18)),
        (date(2026, 10, 18), date(2026, 10, 12), date(2026, 10, 18)),
        (date(2026, 9, 30), date(2026, 9, 28), date(2026, 10, 4)),
        (date(2027, 1, 1), date(2026, 12, 28), date(2027, 1, 3)),
    ],
)
def test_limites_da_semana_para_datas(referencia, inicio, fim):
    assert limites_da_semana(referencia) == (inicio, fim)


def test_instante_e_convertido_para_data_de_brasilia():
    instante_utc = datetime(2026, 10, 12, 1, 30, tzinfo=timezone.utc)

    assert limites_da_semana(instante_utc) == (date(2026, 10, 5), date(2026, 10, 11))


def test_instante_sem_fuso_e_rejeitado():
    with pytest.raises(ValueError, match="deve informar o fuso"):
        limites_da_semana(datetime(2026, 10, 12, 1, 30))


def test_referencia_com_tipo_invalido_e_rejeitada():
    with pytest.raises(TypeError, match="data ou um instante"):
        limites_da_semana("2026-10-12")


def test_agora_devolve_o_instante_atual_em_brasilia():
    from app.core.tempo import FUSO_BRASILIA, agora

    instante = agora()

    assert instante.tzinfo is FUSO_BRASILIA
    assert abs((datetime.now(timezone.utc) - instante).total_seconds()) < 5
