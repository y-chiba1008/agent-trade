import asyncio
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.session import dispose_engine
from app.main import app
from tests.fake_price_adapter import FakePriceSourceAdapter


@pytest.fixture
def fake_price_adapter() -> FakePriceSourceAdapter:
    return FakePriceSourceAdapter(price_jpy=10_000_000)


@pytest.fixture
def client(fake_price_adapter: FakePriceSourceAdapter) -> Generator[TestClient, None, None]:
    mock_task = MagicMock()
    mock_stop_event = MagicMock()

    with (
        patch('app.main.BitflyerRealtimeAdapter', return_value=fake_price_adapter),
        patch('app.main.start_heartbeat', return_value=(mock_task, mock_stop_event)),
    ):
        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture(autouse=True)
def reset_db_engine() -> Generator[None, None, None]:
    asyncio.run(dispose_engine())
    yield
    asyncio.run(dispose_engine())
