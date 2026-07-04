# Backend

Python + FastAPI バックエンド。

## 前提

- [uv](https://docs.astral.sh/uv/)
- Docker（PostgreSQL）

## 初回セットアップ

```bash
# リポジトリルートで
cp .env.example .env
# .env を開き、プレースホルダーを実際の値に置き換える（DATABASE_URL は必須）

docker compose up -d db

cd backend
uv sync
uv run alembic upgrade head
```

## 開発サーバー起動

```bash
cd backend
uv run uvicorn app.main:app --reload
```

`GET http://localhost:8000/health` で `{"status":"ok","db":"connected"}` が返れば正常。

## 品質チェック

```bash
cd backend
uv run ruff check .
uv run mypy .
uv run pytest
```
