import pytest
from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)
from pydantic import SecretStr

from backend.config import get_settings, Settings
from backend.main import create_app


@pytest.fixture
def mock_env(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("DB_HOST", "localhost")


@pytest.fixture
def mock_settings() -> Settings:
    return get_settings(
        db_host="localhost",
        db_port=5432,
        db_name="app",
        db_user="app",
        db_password=SecretStr("secret"),
        auth_host="localhost",
        auth_port=8080,
        auth_http_schema="http",
        auth_realm="app",
        auth_client_id="app"
    )


def test_root(mock_settings: Settings) -> None:
    # Arrange
    app = create_app(settings=mock_settings)
    client = TestClient(app)

    # Act
    r = client.get("/backend/")

    # Assert
    assert r.status_code == HTTP_200_OK
    assert r.json() == {"msg": "Hello (no auth required for this endpoint)"}
