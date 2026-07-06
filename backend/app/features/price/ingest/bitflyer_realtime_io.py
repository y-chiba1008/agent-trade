import asyncio
import json
import logging
from datetime import UTC, datetime

import websockets
from websockets.asyncio.client import ClientConnection

from app.features.common.money import ltp_to_jpy
from app.features.price.ingest.price_store import PriceStore
from app.features.price.shared.price_source_adapter import PriceSnapshot

logger = logging.getLogger(__name__)

BITFLYER_WS_URL = 'wss://ws.lightstream.bitflyer.com/json-rpc'
BITFLYER_TICKER_CHANNEL = 'lightning_ticker_BTC_JPY'
PRODUCT_CODE_BTC_JPY = 'BTC_JPY'

MAX_RECONNECT_DELAY_SEC = 30


class BitflyerRealtimeAdapter:
    def __init__(self, price_store: PriceStore) -> None:
        self._price_store = price_store
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    def get_current_price(self, product_code: str) -> PriceSnapshot | None:
        return self._price_store.get(product_code)

    async def start(self) -> None:
        if self._task is not None:
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        self._stop_event.set()
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _run_loop(self) -> None:
        delay_sec = 1
        while not self._stop_event.is_set():
            try:
                await self._connect_and_listen()
                delay_sec = 1
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception('bitFlyer WebSocket接続エラー。再接続します。')
                if self._stop_event.is_set():
                    break
                await asyncio.sleep(delay_sec)
                delay_sec = min(delay_sec * 2, MAX_RECONNECT_DELAY_SEC)

    async def _connect_and_listen(self) -> None:
        async with websockets.connect(BITFLYER_WS_URL) as ws:
            await self._subscribe(ws)
            while not self._stop_event.is_set():
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=30)
                except TimeoutError:
                    continue
                self._handle_message(raw)

    async def _subscribe(self, ws: ClientConnection) -> None:
        subscribe_message = json.dumps(
            {
                'method': 'subscribe',
                'params': {'channel': BITFLYER_TICKER_CHANNEL},
                'id': None,
            }
        )
        await ws.send(subscribe_message)

    def _handle_message(self, raw: str | bytes) -> None:
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8')
        data = json.loads(raw)
        if data.get('method') != 'channelMessage':
            return
        params = data.get('params', {})
        message = params.get('message', {})
        ltp = message.get('ltp')
        if ltp is None:
            return
        timestamp_str = message.get('timestamp')
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        else:
            timestamp = datetime.now(UTC)
        snapshot = PriceSnapshot(
            product_code=PRODUCT_CODE_BTC_JPY,
            price_jpy=ltp_to_jpy(float(ltp)),
            timestamp=timestamp,
        )
        self._price_store.update(snapshot)
