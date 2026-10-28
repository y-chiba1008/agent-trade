# 🔧 開発者向けドキュメント

## プロジェクト構造

モノレポ構成（`docs/` / `backend/` / `frontend/`）。各ディレクトリの詳細な構成（Package by Feature、命名規則等）は [architecture.md](architecture.md) を参照。

```
agent-trade/
├── docs/                  # ドキュメント
│   ├── requirements.md   # 要件定義書
│   ├── architecture.md   # ディレクトリ構成・アーキテクチャ方針
│   ├── implementation_plan.md  # 実装計画書（フェーズ計画）
│   ├── db_design.md      # DB設計
│   ├── other_information.md  # リポジトリ情報等
│   └── develop.md        # このファイル
├── backend/               # Python + FastAPI（WebAPI層 + MCP層）
└── frontend/               # React + Vite
```

## 初回セットアップ

```bash
# 環境変数の設定
## バックエンド・DB用
cp .env.example .env
# .env を開き、プレースホルダーを実際の値に置き換える（POSTGRES_* / DATABASE_URL 等）

## フロントエンド用
cd frontend
cp .env.example .env.development
cp .env.example .env.production
# 各ファイルの値を環境に合わせて設定する（詳細は「環境変数」節を参照）
cd ..

docker compose up -d db

cd backend
uv sync
uv run alembic upgrade head
uv run dev
```

別ターミナルでフロントエンドを起動する:

```bash
cd frontend
pnpm install   # 初回のみ
pnpm dev
```

`GET http://localhost:8000/health` が `{"status":"ok","db":"connected"}` を返せば Phase 0 の環境構築は完了。`http://localhost:5173` でフロントエンドが表示されれば Phase 2 の UI も利用可能。

## 利用可能なスクリプト

### backend（uv）

backend ディレクトリで実行:

| コマンド | 説明 |
|---|---|
| `uv run dev` | 開発サーバーを起動 |
| `uv run lint` | Lintチェック（`ruff check .`） |
| `uv run pytest` | テストを実行 |
| `uv run mypy .` | 型チェック |
| `uv run alembic upgrade head` | DBマイグレーションを適用 |

### frontend（pnpm）

| コマンド | 説明 |
|---|---|
| `pnpm dev` | 開発サーバーを起動 |
| `pnpm build` | 本番用ビルドを作成 |
| `pnpm lint` | ESLintでコードをチェック |
| `pnpm preview` | ビルド結果をプレビュー |

## 環境変数

環境変数は**ルート**（バックエンド・DB）と**フロントエンド**でファイルを分けて管理する。いずれもシークレットやローカル固有の値を含むため、原則として git にはコミットしない（テンプレートの `.env.example` のみコミット対象）。

### ファイル一覧

| ファイル | git | 用途 |
|---|---|---|
| `/.env` | 無視 | ルート設定の実値（DB 接続情報など） |
| `/.env.example` | コミット | ルート設定のテンプレート |
| `/frontend/.env.development` | 無視 | `pnpm dev` 用（development モード） |
| `/frontend/.env.production` | 無視 | `pnpm build` / `pnpm preview` 用（production モード） |
| `/frontend/.env.example` | コミット | フロントエンド設定のテンプレート |
| `**/.env.local` | 無視 | 個人の上書き用（任意） |

git の除外ルールはルート [`.gitignore`](../.gitignore) で定義している。

### ルート `.env`（バックエンド・DB・mise）

[mise](https://mise.jdx.dev/) の [`mise.toml`](../mise.toml) が `mise.file = ".env"` を指定しており、プロジェクトディレクトリではルート `.env` がシェル環境に読み込まれる。

バックエンドは [`backend/app/config.py`](../backend/app/config.py)（pydantic-settings）経由で `.env` および `../.env` を参照する。docker compose もルート `.env` の `POSTGRES_*` を使用する。

| 変数 | 説明 |
|---|---|
| `POSTGRES_*` | docker-compose 用（PostgreSQL コンテナの起動設定） |
| `ADMINER_PORT` | Adminer のホスト側ポート |
| `DATABASE_URL` | バックエンド・Alembic 用（**必須**）。未設定の場合、サーバ起動時にエラーで停止する |

セットアップ: `cp .env.example .env` のあと、プレースホルダーを実際の値に置き換える。

### フロントエンド `.env.*`（Vite）

Vite は `frontend/` 配下の `.env.[mode]` をモードに応じて読み込む。`VITE_` プレフィックス付きの変数のみクライアントコード（`import.meta.env`）に公開される。

| コマンド | モード | 読み込まれるファイル |
|---|---|---|
| `pnpm dev` | `development` | `.env.development`（および `.env`、`.env.local` 等） |
| `pnpm build` | `production` | `.env.production` |
| `pnpm preview` | — | **ビルド時**に `.env.production` の値が JS に埋め込まれる（実行時には再読み込みしない） |

セットアップ: `frontend/.env.example` をコピーして `.env.development` と `.env.production` を作成する。

| 変数 | 説明 |
|---|---|
| `VITE_API_BASE_URL` | API クライアントのベース URL（[`frontend/src/api/client.ts`](../frontend/src/api/client.ts)）。未設定時は `/api` |

**推奨値（ローカル開発）:**

| ファイル | `VITE_API_BASE_URL` | 理由 |
|---|---|---|
| `.env.development` | `/api` | Vite dev server の proxy（[`frontend/vite.config.ts`](../frontend/vite.config.ts)）経由でバックエンドへ中継。同一オリジンのため CORS 不要 |
| `.env.production` | `http://localhost:8000` | `pnpm preview` 時は proxy が無いためバックエンドへ直接接続。バックエンドの CORS 設定が必要 |

`pnpm build` 後に `.env.production` を変更した場合は、値を反映するために `pnpm build` を再実行する。

**注意:** `VITE_` 変数はビルド成果物に含まれる。シークレット（API キー、DB 接続文字列など）は `VITE_` 変数にしないこと。

### セキュリティ

外部 API キー等のシークレットは環境変数で管理し、コード・DB にハードコードしない（[requirements.md](requirements.md) NFR-011）。

## 設定ファイル

上記「環境変数」節を参照。バックエンドの設定読み込み実装は `backend/app/config.py`。

## テスト

- バックエンド: pytest
- フロントエンド: テストランナー未確定（Phase 2以降で導入検討）
- テストファイルの配置: `backend/tests/` 配下（Phase 1 以降は `tests/features/` に feature 対応構成を追加）

## コーディング規約

詳細な命名規則・アーキテクチャ方針は [architecture.md](architecture.md) を参照。要点のみ以下に記載する。

- 言語・フレームワークの標準的な慣習に従う（Python: スネークケース / TypeScript: キャメルケース）
- Package by Feature: 技術的役割ではなく業務機能単位でディレクトリを切る
- バックエンドの処理は `*_pure.py` / `*_io.py` / `*_usecase.py` に分離する
- フロントエンドのTanStack Queryフックは `use*Query.ts` / `use*Mutation.ts` で命名する
- WebAPI層・MCP層はusecase層への薄いラッパーとして実装し、業務ロジックを持たない
- 複雑なロジックや意図には日本語でコメントを追加する
- TypeScriptの型は明確に定義し、`any` の使用は避ける

## プロジェクト管理

- **リポジトリ**: [y-chiba1008/agent-trade](https://github.com/y-chiba1008/agent-trade)

## 関連ドキュメント

- [requirements.md](requirements.md): 要件定義書（機能要件・非機能要件）
- [architecture.md](architecture.md): ディレクトリ構成・アーキテクチャ方針の詳細
- [implementation_plan.md](implementation_plan.md): 実装計画書（フェーズごとのゴール・タスク）
- [db_design.md](db_design.md): DB設計（テーブル定義・ER図）
- [other_information.md](other_information.md): リポジトリ情報等