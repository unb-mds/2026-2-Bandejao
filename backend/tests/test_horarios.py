from datetime import date, datetime, time, timezone

import pytest

from app.core.config import AMOSTRA_MINIMA_ESTIMATIVA, HORARIOS_INICIO_REFEICAO
from app.core.tempo import FUSO_BRASILIA, avaliacao_esta_aberta
from app.models.enums import TipoRefeicao


@pytest.mark.parametrize(
    ("tipo_refeicao", "horario"),
    [
        (TipoRefeicao.CAFE_DA_MANHA, time(7, 0)),
        (TipoRefeicao.ALMOCO, time(11, 0)),
        (TipoRefeicao.JANTAR, time(17, 0)),
    ],
)
def test_horarios_de_inicio_seguem_a_fonte_oficial(tipo_refeicao, horario):
    assert HORARIOS_INICIO_REFEICAO[tipo_refeicao.value] == horario


def test_amostra_minima_e_definida_na_configuracao():
    assert AMOSTRA_MINIMA_ESTIMATIVA == 10


@pytest.mark.parametrize(
    ("instante", "esperado"),
    [
        (datetime(2026, 10, 15, 10, 59, 59, 999999, tzinfo=FUSO_BRASILIA), False),
        (datetime(2026, 10, 15, 11, 0, tzinfo=FUSO_BRASILIA), True),
        (datetime(2026, 10, 15, 23, 59, 59, 999999, tzinfo=FUSO_BRASILIA), True),
        (datetime(2026, 10, 16, 0, 0, tzinfo=FUSO_BRASILIA), False),
    ],
)
def test_limites_da_janela_de_avaliacao(instante, esperado):
    assert (
        avaliacao_esta_aberta(TipoRefeicao.ALMOCO, date(2026, 10, 15), instante) is esperado
    )


def test_instante_e_convertido_para_o_fuso_de_brasilia():
    instante_utc = datetime(2026, 10, 15, 14, 0, tzinfo=timezone.utc)

    assert avaliacao_esta_aberta(TipoRefeicao.ALMOCO, date(2026, 10, 15), instante_utc)


def test_refeicao_sem_horario_configurado_permanece_fechada():
    assert not avaliacao_esta_aberta(
        TipoRefeicao.JANTAR,
        date(2026, 10, 15),
        datetime(2026, 10, 15, 18, 0, tzinfo=FUSO_BRASILIA),
        horarios_inicio={},
    )


def test_instante_sem_fuso_e_rejeitado():
    with pytest.raises(ValueError, match="deve informar o fuso"):
        avaliacao_esta_aberta(
            TipoRefeicao.ALMOCO,
            date(2026, 10, 15),
            datetime(2026, 10, 15, 11, 0),
        )
