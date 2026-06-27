# AGENTS.md

このファイルは、コーディングエージェントがプロジェクトの目的・技術スタック・コーディング規約を理解するための指示書です。

## 🤖 エージェントへの指示（重要）

- **コミュニケーション言語:** 提案・質問・結果の要約など、すべての対話は**必ず日本語**で行ってください。

## 🚀 プロジェクトの目的

人間がリスクなしに取引を体験でき、かつLLM（AI）による取引判断の有効性を検証できる、個人用のデモトレードアプリ。外部APIから暗号資産（BTC-JPY）の価格をリアルタイムに取得し、仮想的なデモ口座上で注文・約定をシミュレーションする。詳細な要件は [docs/requirements.md](docs/requirements.md) を参照。

## 🛠️ 技術スタック

- **バックエンド:** Python + FastAPI
- **データベース:** PostgreSQL
- **フロントエンド:** React + Vite（TypeScript）
- **クライアント状態管理:** Zustand
- **サーバ状態管理:** TanStack Query
- **UIコンポーネント:** shadcn/ui
- **フォーム:** React Hook Form + Zod
- **MCP実装方式:** バックエンドが直接MCPサーバとして動作（構成A）

詳細は [docs/requirements.md](docs/requirements.md) の「5. 技術スタック（確定事項）」を参照。

## 📏 コーディング規約

コーディング規約・プロジェクト構造・利用可能なスクリプトは [docs/develop.md](docs/develop.md) にまとめている。エージェントは作業前に必ずこちらを参照すること。

特に以下は厳格に守ること:

- WebAPI層・MCP層はusecase層への薄いラッパーとして実装し、業務ロジックを持たない
- Package by Feature（業務機能単位でのディレクトリ分割）に従う
- TypeScriptの型は明確に定義し、`any` の使用は避ける
- 複雑なロジックや意図には日本語でコメントを追加する

## 📐 設計・計画ドキュメント

重要機能や大規模改修を行う際は、着手前に以下の関連ドキュメントを確認すること。既存の設計方針（例: Package by Featureのレイヤリング、構成A/Bの分離方針）と矛盾する実装をしないよう注意する。

- [docs/architecture.md](docs/architecture.md): ディレクトリ構成・アーキテクチャ方針
- [docs/implementation_plan.md](docs/implementation_plan.md): フェーズごとの実装計画
- [docs/db_design.md](docs/db_design.md): DB設計

## ✅ 作業完了前のチェック

### backend

- `uv run ruff check .` でLintエラーがないことを確認する
- `uv run pytest` でテストが通ることを確認する

### frontend

- `pnpm lint` でエラーがないことを確認する
- `pnpm build` で型エラーがないことを確認する

コマンドの詳細は [docs/develop.md](docs/develop.md) を参照。