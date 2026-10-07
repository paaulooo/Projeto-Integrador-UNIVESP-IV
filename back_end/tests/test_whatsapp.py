from app.models.whatsapp import _normalizar_telefone


def test_normaliza_telefone_sem_ddi_assume_padrao():
    assert _normalizar_telefone("11999990001") == "5511999990001"


def test_normaliza_telefone_com_mascara():
    assert _normalizar_telefone("(11) 99999-0001") == "5511999990001"


def test_normaliza_telefone_ja_com_mais():
    assert _normalizar_telefone("+5511999990001") == "5511999990001"


def test_normaliza_telefone_ja_com_ddi_sem_mais():
    assert _normalizar_telefone("5511999990001") == "5511999990001"
