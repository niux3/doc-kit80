from fastapi import status

# Préfixe global défini dans create_app()
BASE_URL = "/api/v1/languages"


def test_create_language_invalid_payload(client):
    # Manque "name" et "abbr"
    response = client.post(f"{BASE_URL}/", json={"name": "Python"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_delete_language_success(client):
    created = client.post(
        f"{BASE_URL}/", json={"name": "JavaScript", "abbr": "js"}
    ).json()
    lang_id = created["id"]

    delete_res = client.delete(f"{BASE_URL}/{lang_id}")
    assert delete_res.status_code == status.HTTP_204_NO_CONTENT

    get_res = client.get(f"{BASE_URL}/{lang_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_get_language_not_found(client):
    # Non-existent resource -> 404 Not Found
    response = client.get(f"{BASE_URL}/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Language 999 not found"


def test_create_language_success(client):
    response = client.post(
        f"{BASE_URL}/", json={"name": "Python", "abbr": "py"}
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "Python"
    assert data["abbr"] == "py"
    assert "id" in data


def test_get_language_success(client):
    # 1. Création préalable
    created = client.post(
        f"{BASE_URL}/", json={"name": "Rust", "abbr": "rs"}
    ).json()
    lang_id = created["id"]

    # 2. Récupération par ID
    response = client.get(f"{BASE_URL}/{lang_id}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == lang_id
    assert data["name"] == "Rust"
    assert data["abbr"] == "rs"
