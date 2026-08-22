def _create_sala(client):
    response = client.post("/salas/", json={"nome": "Sala A", "capacidade": 30, "turno": "manha"})
    return response.json()["id"]


def _create_aluno(client, sala_id, nome="Joao", matricula="2026001"):
    return client.post(
        "/alunos/",
        json={
            "nome": nome,
            "data_nascimento": "2015-04-10",
            "matricula": matricula,
            "sala_id": sala_id,
        },
    )


def test_create_aluno(client):
    sala_id = _create_sala(client)

    response = _create_aluno(client, sala_id)

    assert response.status_code == 201
    body = response.json()
    assert body["nome"] == "Joao"
    assert body["sala_id"] == sala_id


def test_create_aluno_com_sala_inexistente(client):
    response = _create_aluno(client, sala_id=999)

    assert response.status_code == 404


def test_list_alunos(client):
    sala_id = _create_sala(client)
    _create_aluno(client, sala_id, nome="Joao", matricula="2026001")
    _create_aluno(client, sala_id, nome="Maria", matricula="2026002")

    response = client.get("/alunos/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_aluno_inexistente(client):
    response = client.get("/alunos/999")

    assert response.status_code == 404


def test_update_aluno(client):
    sala_id = _create_sala(client)
    created = _create_aluno(client, sala_id).json()

    response = client.put(
        f"/alunos/{created['id']}",
        json={
            "nome": "Joao Atualizado",
            "data_nascimento": "2015-04-10",
            "matricula": "2026001",
            "sala_id": sala_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Joao Atualizado"


def test_delete_aluno(client):
    sala_id = _create_sala(client)
    created = _create_aluno(client, sala_id).json()

    response = client.delete(f"/alunos/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/alunos/{created['id']}").status_code == 404
