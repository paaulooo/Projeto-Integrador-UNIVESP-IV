from app.api import faltasController


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


def _create_responsavel(client, aluno_id, email="resp@example.com"):
    client.post(
        "/responsaveis/",
        json={
            "nome": "Maria",
            "telefone": "11999999999",
            "email": email,
            "parentesco": "mae",
            "aluno_ids": [aluno_id],
        },
    )


def test_falta_dispara_notificacao_para_responsaveis(client, monkeypatch):
    chamadas = []

    async def fake_notificar(aluno_nome, responsaveis, registros):
        chamadas.append((aluno_nome, responsaveis, registros))

    monkeypatch.setattr(faltasController, "notificar_responsaveis_falta", fake_notificar)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": False, "justificada": False},
    )

    assert response.status_code == 201
    assert len(chamadas) == 1
    nome, responsaveis, registros = chamadas[0]
    assert nome == "Joao"
    assert responsaveis == [
        {
            "nome": "Maria",
            "email": "resp@example.com",
            "telefone": "11999999999",
            "whatsapp_apikey": None,
        }
    ]
    assert len(registros) == 1


def test_presenca_nao_dispara_notificacao(client, monkeypatch):
    chamadas = []

    async def fake_notificar(aluno_nome, responsaveis, registros):
        chamadas.append((aluno_nome, responsaveis, registros))

    monkeypatch.setattr(faltasController, "notificar_responsaveis_falta", fake_notificar)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)

    response = client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": True, "justificada": False},
    )

    assert response.status_code == 201
    assert chamadas == []


def test_update_falta_para_ausente_dispara_notificacao(client, monkeypatch):
    chamadas = []

    async def fake_notificar(aluno_nome, responsaveis, registros):
        chamadas.append((aluno_nome, responsaveis, registros))

    monkeypatch.setattr(faltasController, "notificar_responsaveis_falta", fake_notificar)

    aluno_id = _create_aluno(client, _create_sala(client))
    _create_responsavel(client, aluno_id)
    created = client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": True, "justificada": False},
    ).json()
    assert chamadas == []

    response = client.put(
        f"/faltas/{created['id']}",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": False, "justificada": False},
    )

    assert response.status_code == 200
    assert len(chamadas) == 1


def test_falta_atualiza_contador_de_faltas_do_aluno(client):
    aluno_id = _create_aluno(client, _create_sala(client))

    client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": False, "justificada": False},
    )
    client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": "2026-09-22", "presente": True, "justificada": False},
    )

    aluno = client.get(f"/alunos/{aluno_id}").json()

    assert aluno["faltas"] == 1
    assert aluno["perc_presenca"] == 50.0
