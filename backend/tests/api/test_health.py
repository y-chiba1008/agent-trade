from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


def test_health_db_connected(client: TestClient) -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'db': 'connected'}


@patch('app.api.router.check_db_connection', new_callable=AsyncMock)
def test_health_db_disconnected(
    mock_check: AsyncMock,
    client: TestClient,
) -> None:
    mock_check.return_value = False
    response = client.get('/health')
    assert response.status_code == 503
    assert response.json() == {'status': 'degraded', 'db': 'disconnected'}
