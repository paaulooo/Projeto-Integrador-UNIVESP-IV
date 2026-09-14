from datetime import date, timedelta

import pytest

from app.models.regra_res_falta import regra_faltas_consecutivas, regra_perc_falta


def _registro(dias_atras, presente=True, justificada=False, hoje=None):
    hoje = hoje or date.today()
    return {"data": hoje - timedelta(days=dias_atras), "presente": presente, "justificada": justificada}


def test_perc_falta_sem_registros_recentes():
    registros = [_registro(100, presente=False)]

    resultado = regra_perc_falta(registros, dias=30)

    assert resultado.disparada is False


def test_perc_falta_abaixo_do_limite():
    registros = [_registro(d, presente=True) for d in range(20)]

    resultado = regra_perc_falta(registros, dias=30, lim=0.5)

    assert resultado.disparada is False
    assert resultado.peso == 0.0


def test_perc_falta_igual_ou_acima_do_limite():
    registros = [_registro(d, presente=(d % 2 == 0)) for d in range(10)]

    resultado = regra_perc_falta(registros, dias=30, lim=0.5)

    assert resultado.disparada is True
    assert resultado.peso == pytest.approx(0.5)


def test_perc_falta_ignora_registros_fora_da_janela():
    registros = [_registro(d, presente=False) for d in range(40, 50)]
    registros += [_registro(d, presente=True) for d in range(5)]

    resultado = regra_perc_falta(registros, dias=30, lim=0.1)

    assert resultado.disparada is False
    assert "5 aulas" in resultado.detalhe


def test_perc_falta_nao_conta_falta_justificada():
    registros = [_registro(d, presente=False, justificada=True) for d in range(5)]
    registros += [_registro(d, presente=True) for d in range(5, 15)]

    resultado = regra_perc_falta(registros, dias=30, lim=0.1)

    assert resultado.disparada is False
    assert resultado.peso == 0.0


def test_faltas_consecutivas_dispara_com_sequencia_ate_o_ultimo_registro():
    registros = [_registro(d, presente=False) for d in range(3)]

    resultado = regra_faltas_consecutivas(registros, lim=3)

    assert resultado.disparada is True
    assert "3 faltas consecutivas" in resultado.detalhe


def test_faltas_consecutivas_nao_dispara_com_sequencia_curta():
    registros = [_registro(d, presente=False) for d in range(2)]

    resultado = regra_faltas_consecutivas(registros, lim=3)

    assert resultado.disparada is False


def test_faltas_consecutivas_justificada_interrompe_sequencia():
    registros = [
        _registro(4, presente=False),
        _registro(3, presente=False),
        _registro(2, presente=False, justificada=True),
        _registro(1, presente=False),
        _registro(0, presente=False),
    ]

    resultado = regra_faltas_consecutivas(registros, lim=3)

    assert resultado.disparada is False


def test_faltas_consecutivas_lista_vazia_nao_quebra():
    resultado = regra_faltas_consecutivas([], lim=3)

    assert resultado.disparada is False
