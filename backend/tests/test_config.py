from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings, validate_startup_settings
from app.main import app


def test_resolved_database_url_raises_when_unset() -> None:
    settings = Settings(database_url=None)
    with pytest.raises(RuntimeError, match='DATABASE_URL'):
        _ = settings.resolved_database_url


def test_resolved_database_url_returns_value_when_set() -> None:
    settings = Settings(
        database_url='postgresql+asyncpg://user:pass@localhost:5432/db',
    )
    assert settings.resolved_database_url == settings.database_url


def test_validate_startup_settings_raises_when_unset() -> None:
    with patch('app.config.get_settings', return_value=Settings(database_url=None)):
        with pytest.raises(RuntimeError, match='DATABASE_URL'):
            validate_startup_settings()


def test_app_startup_raises_when_database_url_unset() -> None:
    with patch('app.config.get_settings', return_value=Settings(database_url=None)):
        with pytest.raises(RuntimeError, match='DATABASE_URL'):
            with TestClient(app):
                pass


def test_get_settings_cache_can_be_cleared() -> None:
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.database_url is not None
