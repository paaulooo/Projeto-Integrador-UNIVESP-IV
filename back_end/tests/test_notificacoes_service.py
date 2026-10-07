import asyncio
from datetime import date

from app.services import notificacoes


def test_notifica_email_e_whatsapp_por_responsavel(monkeypatch):
    chamadas_email = []
    chamadas_whatsapp = []

    async def fake_email(**kwargs):
        chamadas_email.append(kwargs)

    async def fake_whatsapp(mensagem):
        chamadas_whatsapp.append(mensagem)

    monkeypatch.setattr(notificacoes, "sendTemplateEmail", fake_email)
    monkeypatch.setattr(notificacoes, "sendWhatsApp", fake_whatsapp)

    responsaveis = [
        {
            "nome": "Maria",
            "email": "maria@example.com",
            "telefone": "11999990001",
            "whatsapp_apikey": "123456",
        },
        {
            "nome": "Carlos",
            "email": "carlos@example.com",
            "telefone": "11999990002",
            "whatsapp_apikey": "654321",
        },
    ]
    registros = [{"data": date(2026, 9, 21), "presente": False, "justificada": False}]

    asyncio.run(notificacoes.notificar_responsaveis_falta("Joao", responsaveis, registros))

    assert len(chamadas_email) == 2
    assert len(chamadas_whatsapp) == 2
    assert chamadas_whatsapp[0].telefone == "11999990001"
    assert chamadas_whatsapp[0].apikey == "123456"


def test_nao_envia_whatsapp_sem_telefone_cadastrado(monkeypatch):
    chamadas_whatsapp = []

    async def fake_email(**kwargs):
        return None

    async def fake_whatsapp(mensagem):
        chamadas_whatsapp.append(mensagem)

    monkeypatch.setattr(notificacoes, "sendTemplateEmail", fake_email)
    monkeypatch.setattr(notificacoes, "sendWhatsApp", fake_whatsapp)

    responsaveis = [
        {"nome": "Maria", "email": "maria@example.com", "telefone": None, "whatsapp_apikey": None}
    ]
    registros = [{"data": date(2026, 9, 21), "presente": False, "justificada": False}]

    asyncio.run(notificacoes.notificar_responsaveis_falta("Joao", responsaveis, registros))

    assert chamadas_whatsapp == []


def test_nao_envia_whatsapp_sem_opt_in_no_callmebot(monkeypatch):
    chamadas_whatsapp = []

    async def fake_email(**kwargs):
        return None

    async def fake_whatsapp(mensagem):
        chamadas_whatsapp.append(mensagem)

    monkeypatch.setattr(notificacoes, "sendTemplateEmail", fake_email)
    monkeypatch.setattr(notificacoes, "sendWhatsApp", fake_whatsapp)

    responsaveis = [
        {
            "nome": "Maria",
            "email": "maria@example.com",
            "telefone": "11999990001",
            "whatsapp_apikey": None,
        }
    ]
    registros = [{"data": date(2026, 9, 21), "presente": False, "justificada": False}]

    asyncio.run(notificacoes.notificar_responsaveis_falta("Joao", responsaveis, registros))

    assert chamadas_whatsapp == []


def test_falha_no_email_nao_impede_envio_do_whatsapp(monkeypatch):
    chamadas_whatsapp = []

    async def fake_email(**kwargs):
        raise RuntimeError("SMTP indisponivel")

    async def fake_whatsapp(mensagem):
        chamadas_whatsapp.append(mensagem)

    monkeypatch.setattr(notificacoes, "sendTemplateEmail", fake_email)
    monkeypatch.setattr(notificacoes, "sendWhatsApp", fake_whatsapp)

    responsaveis = [
        {
            "nome": "Maria",
            "email": "maria@example.com",
            "telefone": "11999990001",
            "whatsapp_apikey": "123456",
        }
    ]
    registros = [{"data": date(2026, 9, 21), "presente": False, "justificada": False}]

    asyncio.run(notificacoes.notificar_responsaveis_falta("Joao", responsaveis, registros))

    assert len(chamadas_whatsapp) == 1
