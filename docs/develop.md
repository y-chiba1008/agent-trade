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

## 利用可能なスクリプト

### backend（uv）

| コマンド | 説明 |
|---|---|
| `uv run uvicorn app.main:app --reload` | 開発サーバーを起動 |
| `uv run pytest` | テストを実行 |
| `uv run ruff check .` | Lintチェック |
| `uv run alembic upgrade head` | DBマイグレーションを適用 |

### frontend（pnpm）

| コマンド | 説明 |
|---|---|
| `pnpm dev` | 開発サーバーを起動 |
| `pnpm build` | 本番用ビルドを作成 |
| `pnpm lint` | ESLintでコードをチェック |
| `pnpm preview` | ビルド結果をプレビュー |

> 上記スクリプト名・内容はPhase 0実装時に確定する（[implementation_plan.md](implementation_plan.md) のPhase 0参照）。確定後は本表を実際の`pyproject.toml`/`package.json`の内容に合わせて更新する。

## 設定ファイル

価格データソースのURL、ハートビート間隔等の調整可能な値は、実装時に `backend/app/config.py`（環境変数経由）にまとめる予定。詳細未確定（[implementation_plan.md](implementation_plan.md) のPhase 0/1参照）。

外部APIキー等のシークレットは環境変数で管理し、コード・DBにハードコードしない（[requirements.md](requirements.md) NFR-011）。

## テスト

- バックエンド: pytest
- フロントエンド: テストランナー未確定（Phase 2以降で導入検討）
- テストファイルの配置: `backend/tests/features/` 配下に、対象featureと対応する構成で配置（[architecture.md](architecture.md) 参照）

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