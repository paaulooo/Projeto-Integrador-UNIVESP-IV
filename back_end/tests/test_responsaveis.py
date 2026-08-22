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


def _create_responsavel(client, aluno_ids, nome="Carlos"):
    return client.post(
        "/responsaveis/",
        json={
            "nome": nome,
            "telefone": "11999990000",
            "email": "carlos@example.com",
            "parentesco": "pai",
            "aluno_ids": aluno_ids,
        },
    )


def test_create_responsavel(client):
    sala_id = _create_sala(client)
    aluno_id = _create_aluno(client, sala_id)

    response = _create_responsavel(client, [aluno_id])

    assert response.status_code == 201
    body = response.json()
    assert body["nome"] == "Carlos"
    assert body["aluno_ids"] == [aluno_id]


def test_create_responsavel_com_aluno_inexistente(client):
    response = _create_responsavel(client, [999])

    assert response.status_code == 404


def test_responsavel_com_multiplos_alunos(client):
    sala_id = _create_sala(client)
    aluno_1 = _create_aluno(client, sala_id, nome="Joao", matricula="2026001")
    aluno_2 = _create_aluno(client, sala_id, nome="Maria", matricula="2026002")

    response = _create_responsavel(client, [aluno_1, aluno_2])

    assert response.status_code == 201
    assert sorted(response.json()["aluno_ids"]) == sorted([aluno_1, aluno_2])


def test_get_responsavel_inexistente(client):
    response = client.get("/responsaveis/999")

    assert response.status_code == 404


def test_update_responsavel(client):
    sala_id = _create_sala(client)
    aluno_id = _create_aluno(client, sala_id)
    created = _create_responsavel(client, [aluno_id]).json()

    response = client.put(
        f"/responsaveis/{created['id']}",
        json={
            "nome": "Carlos Atualizado",
            "telefone": "11999990000",
            "email": "carlos@example.com",
            "parentesco": "pai",
            "aluno_ids": [aluno_id],
        },
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Carlos Atualizado"


def test_delete_responsavel(client):
    sala_id = _create_sala(client)
    aluno_id = _create_aluno(client, sala_id)
    created = _create_responsavel(client, [aluno_id]).json()

    response = client.delete(f"/responsaveis/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/responsaveis/{created['id']}").status_code == 404
