# agent-trade

個人用デモトレードアプリ（BTC-JPY）。詳細は [docs/requirements.md](docs/requirements.md) を参照。

## クイックスタート（Phase 0）

```bash
cp .env.example .env
# .env のプレースホルダーを実際の値に置き換える
docker compose up -d db

cd backend
uv sync
uv run alembic upgrade head
uv run dev
```

ヘルスチェック:

```bash
curl -s http://localhost:8000/health
```

## ドキュメント

- [docs/develop.md](docs/develop.md) — 開発手順・スクリプト一覧
- [docs/implementation_plan.md](docs/implementation_plan.md) — フェーズ別実装計画
