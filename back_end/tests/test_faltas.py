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


def _create_falta(client, aluno_id, data="2026-09-21", presente=False, justificada=False):
    return client.post(
        "/faltas/",
        json={"aluno_id": aluno_id, "data": data, "presente": presente, "justificada": justificada},
    )


def test_create_falta(client):
    aluno_id = _create_aluno(client, _create_sala(client))

    response = _create_falta(client, aluno_id, data="2026-09-21")

    assert response.status_code == 201
    body = response.json()
    assert body["aluno_id"] == aluno_id
    assert body["data"] == "2026-09-21"
    assert body["presente"] is False
    assert "id" in body


def test_create_falta_com_aluno_inexistente(client):
    response = _create_falta(client, aluno_id=999, data="2026-09-21")

    assert response.status_code == 404


def test_create_falta_em_sabado_ou_domingo_falha(client):
    aluno_id = _create_aluno(client, _create_sala(client))

    response = _create_falta(client, aluno_id, data="2026-09-19")

    assert response.status_code == 422


def test_create_falta_duplicada_para_o_mesmo_dia_falha(client):
    aluno_id = _create_aluno(client, _create_sala(client))
    _create_falta(client, aluno_id, data="2026-09-21")

    response = _create_falta(client, aluno_id, data="2026-09-21")

    assert response.status_code == 409


def test_list_faltas(client):
    aluno_id = _create_aluno(client, _create_sala(client))
    _create_falta(client, aluno_id, data="2026-09-21")
    _create_falta(client, aluno_id, data="2026-09-22")

    response = client.get("/faltas/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_falta_inexistente(client):
    response = client.get("/faltas/999")

    assert response.status_code == 404


def test_update_falta(client):
    aluno_id = _create_aluno(client, _create_sala(client))
    created = _create_falta(client, aluno_id, data="2026-09-21").json()

    response = client.put(
        f"/faltas/{created['id']}",
        json={"aluno_id": aluno_id, "data": "2026-09-21", "presente": False, "justificada": True},
    )

    assert response.status_code == 200
    assert response.json()["justificada"] is True


def test_delete_falta(client):
    aluno_id = _create_aluno(client, _create_sala(client))
    created = _create_falta(client, aluno_id, data="2026-09-21").json()

    response = client.delete(f"/faltas/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/faltas/{created['id']}").status_code == 404
