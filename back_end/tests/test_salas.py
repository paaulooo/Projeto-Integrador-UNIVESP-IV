def _create_sala(client, nome="Sala A", capacidade=30, turno="manha"):
    return client.post("/salas/", json={"nome": nome, "capacidade": capacidade, "turno": turno})


def test_create_sala(client):
    response = _create_sala(client)

    assert response.status_code == 201
    body = response.json()
    assert body["nome"] == "Sala A"
    assert body["capacidade"] == 30
    assert "id" in body


def test_list_salas(client):
    _create_sala(client, nome="Sala A")
    _create_sala(client, nome="Sala B")

    response = client.get("/salas/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_sala(client):
    created = _create_sala(client).json()

    response = client.get(f"/salas/{created['id']}")

    assert response.status_code == 200
    assert response.json()["nome"] == "Sala A"


def test_get_sala_inexistente(client):
    response = client.get("/salas/999")

    assert response.status_code == 404


def test_update_sala(client):
    created = _create_sala(client).json()

    response = client.put(
        f"/salas/{created['id']}",
        json={"nome": "Sala Renomeada", "capacidade": 40, "turno": "tarde"},
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Sala Renomeada"
    assert response.json()["capacidade"] == 40


def test_delete_sala(client):
    created = _create_sala(client).json()

    response = client.delete(f"/salas/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/salas/{created['id']}").status_code == 404
