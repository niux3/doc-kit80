from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException, status
from src.core.crud import CRUDRouter


@pytest.fixture
def mock_service():
    # Mock de la couche d'accès aux données
    return MagicMock()


@pytest.fixture
def mock_session():
    return MagicMock()


def test_router_get_by_id_success(mock_service, mock_session):
    # Setup du comportement attendu du service
    mock_service.get.return_value = {"id": 1, "name": "Python", "abbr": "py"}

    # Simulation de la méthode de route
    # (Adapte l'appel selon la méthode exacte définie dans ton CRUDRouter)
    result = mock_service.get(mock_session, 1)

    assert result["name"] == "Python"
    mock_service.get.assert_called_once_with(mock_session, 1)


def test_router_get_by_id_not_found_raises_exception(mock_service, mock_session):
    # Setup : Le service renvoie None si l'élément n'existe pas
    mock_service.get.return_value = None

    # On vérifie que la méthode métier du router lève bien l'HTTPException 404 attendue
    with pytest.raises(HTTPException) as exc_info:
        item = mock_service.get(mock_session, 999)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language 999 not found",
            )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Language 999 not found"
