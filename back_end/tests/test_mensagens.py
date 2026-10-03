from datetime import date, timedelta

from app.services.mensagens import (
    LIMITE_SEGURO_WHATSAPP,
    formatar_mensagem_whatsapp,
    montar_mensagem_falta,
)


def _registro(dias_atras, presente=False, justificada=False, hoje=None):
    hoje = hoje or date.today()
    return {"data": hoje - timedelta(days=dias_atras), "presente": presente, "justificada": justificada}


def test_mensagem_padrao_para_uma_ou_duas_faltas():
    registros = [_registro(0)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert msg.titulo == "Aviso de falta"
    assert "Joao" in msg.mensagem
    assert "AVISO IMPORTANTE" not in msg.mensagem


def test_mensagem_acompanhamento_com_tres_faltas():
    registros = [_registro(d) for d in range(3)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert msg.titulo == "Aviso de frequência"
    assert "3 faltas" in msg.mensagem


def test_mensagem_situacao_critica_com_quatro_faltas():
    registros = [_registro(d) for d in range(4)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert msg.titulo == "Aviso importante de frequência"
    assert "AVISO IMPORTANTE" in msg.mensagem


def test_mensagem_cancelamento_de_vaga_com_quinze_faltas():
    registros = [_registro(d) for d in range(15)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert msg.titulo == "Comunicado oficial"
    assert "cancelada" in msg.mensagem


def test_mensagem_inclui_aviso_de_faltas_consecutivas():
    registros = [_registro(d) for d in range(3)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert "consecutivas" in msg.mensagem


def test_mensagem_de_cancelamento_nao_duplica_aviso_de_consecutivas():
    registros = [_registro(d) for d in range(15)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert "padrão preocupante" not in msg.mensagem


def test_mensagem_falta_justificada_nao_conta():
    registros = [_registro(0, justificada=True)]

    msg = montar_mensagem_falta("Joao", "Maria", registros)

    assert msg.titulo == "Contato da escola"
    assert "faltou" not in msg.mensagem


def test_mensagem_sem_faltas_nao_afirma_que_aluno_faltou():
    msg = montar_mensagem_falta("Joao", "Maria", [])

    assert msg.titulo == "Contato da escola"
    assert "faltou" not in msg.mensagem


def test_whatsapp_tem_estrutura_de_alerta():
    registros = [_registro(0)]
    msg = montar_mensagem_falta("Joao", "Maria", registros)

    texto = formatar_mensagem_whatsapp(msg)

    assert texto.startswith("⚠️ *AVISO DE FALTA*")
    assert "*Joao*" in texto
    assert "📋 *Descrição:*" in texto
    assert "📌 *O que fazer:*" in texto
    assert "💡 Você recebeu esta mensagem" in texto
    assert "Observação" not in texto


def test_whatsapp_inclui_bloco_de_observacao_quando_informado():
    registros = [_registro(0)]
    msg = montar_mensagem_falta("Joao", "Maria", registros)

    texto = formatar_mensagem_whatsapp(msg, observacao="Favor comparecer amanhã.")

    assert "📝 *Observação do(a) professor(a):*" in texto
    assert "Favor comparecer amanhã." in texto


def test_whatsapp_emoji_varia_por_tier():
    sem_faltas = formatar_mensagem_whatsapp(montar_mensagem_falta("Joao", "Maria", []))
    uma_falta = formatar_mensagem_whatsapp(
        montar_mensagem_falta("Joao", "Maria", [_registro(0)])
    )
    cancelamento = formatar_mensagem_whatsapp(
        montar_mensagem_falta("Joao", "Maria", [_registro(d) for d in range(15)])
    )

    assert sem_faltas.startswith("💬")
    assert uma_falta.startswith("⚠️")
    assert cancelamento.startswith("🚨")


def test_whatsapp_nunca_ultrapassa_o_limite_seguro():
    casos = [
        [],
        [_registro(0)],
        [_registro(d) for d in range(3)],
        [_registro(d) for d in range(4)],
        [_registro(d) for d in range(15)],
    ]
    for registros in casos:
        msg = montar_mensagem_falta("Gabriel Santos", "Roberto Santos", registros)
        for observacao in (None, "obs curta", "x" * 2000):
            texto = formatar_mensagem_whatsapp(msg, observacao=observacao)
            assert len(texto) <= LIMITE_SEGURO_WHATSAPP


def test_whatsapp_preserva_acao_mesmo_truncando_descricao():
    registros = [_registro(d) for d in range(4)]
    msg = montar_mensagem_falta("Gabriel Santos", "Roberto Santos", registros)

    texto = formatar_mensagem_whatsapp(msg, observacao="x" * 2000)

    assert "📌 *O que fazer:*" in texto
    assert msg.acao in texto
