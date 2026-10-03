from app.api import mensagensController


def _create_sala(client):
    response = client.post("/salas/", json={"nome": "Sala A", "capacidade": 30, "turno": "manha"})
    return response.json()["id"]


def _create_aluno(client, sala_id, nome="Joao", matricula="2026001"):
    response = client.post(
        "/alunos/",
        json={
            "nome": nome,
            "data_nascimento": "2015-04-10",
            "matricula": matricula,
            "sala_id": sala_id,
        },
    )
    return response.json()["id"]


def _create_responsavel(
    client,
    aluno_id,
    email="resp@example.com",
    nome="Maria",
    telefone="11999999999",
    whatsapp_apikey="123456",
):
    client.post(
        "/responsaveis/",
        json={
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "parentesco": "mae",
            "whatsapp_apikey": whatsapp_apikey,
            "aluno_ids": [aluno_id],
        },
    )


def _mock_canais(monkeypatch, email_ok=True, whatsapp_ok=True):
    chamadas_email = []
    chamadas_whatsapp = []

    async def fake_send_email(**kwargs):
        chamadas_email.append(kwargs)
        if not email_ok:
            raise RuntimeError("SMTP indisponivel")

    async def fake_send_whatsapp(mensagem):
        chamadas_whatsapp.append(mensagem)
        if not whatsapp_ok:
            raise RuntimeError("Twilio indisponivel")

    monkeypatch.setattr(mensagensController, "sendTemplateEmail", fake_send_email)
    monkeypatch.setattr(mensagensController, "sendWhatsApp", fake_send_whatsapp)
    return chamadas_email, chamadas_whatsapp


def test_envio_manual_com_sucesso(client, monkeypatch):
    chamadas_email, chamadas_whatsapp = _mock_canais(monkeypatch)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(
        f"/alunos/{aluno_id}/mensagens", json={"observacao": "Favor comparecer amanhã."}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["destinatarios_email"] == ["resp@example.com"]
    assert body["falhas_email"] == []
    assert body["destinatarios_whatsapp"] == ["11999999999"]
    assert body["falhas_whatsapp"] == []
    assert len(chamadas_email) == 1
    assert chamadas_email[0]["context"]["observacao"] == "Favor comparecer amanhã."
    assert len(chamadas_whatsapp) == 1
    assert "Favor comparecer amanhã." in chamadas_whatsapp[0].mensagem


def test_envio_manual_sem_observacao(client, monkeypatch):
    _mock_canais(monkeypatch)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(f"/alunos/{aluno_id}/mensagens", json={})

    assert response.status_code == 201


def test_envio_manual_aluno_inexistente(client):
    response = client.post("/alunos/999/mensagens", json={})

    assert response.status_code == 404


def test_envio_manual_sem_responsavel_cadastrado(client):
    aluno_id = _create_aluno(client, _create_sala(client))

    response = client.post(f"/alunos/{aluno_id}/mensagens", json={})

    assert response.status_code == 422


def test_envio_manual_retorna_502_se_todos_os_envios_falharem(client, monkeypatch):
    _mock_canais(monkeypatch, email_ok=False, whatsapp_ok=False)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(f"/alunos/{aluno_id}/mensagens", json={})

    assert response.status_code == 502


def test_envio_manual_sucesso_parcial_quando_so_whatsapp_funciona(client, monkeypatch):
    _mock_canais(monkeypatch, email_ok=False, whatsapp_ok=True)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(f"/alunos/{aluno_id}/mensagens", json={})

    assert response.status_code == 201
    body = response.json()
    assert body["falhas_email"] == ["resp@example.com"]
    assert body["destinatarios_whatsapp"] == ["11999999999"]
