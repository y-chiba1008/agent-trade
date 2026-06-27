# ディレクトリ構成・アーキテクチャ方針

## 1. 全体構成（モノレポ）

```
agent-trade/
  docs/
  backend/
  frontend/
```

## 2. 設計思想

バックエンド・フロントエンドともに、以下の記事で紹介されている「LLMフレンドリーアーキテクチャ」の考え方を採用する。

参照: [LLMフレンドリーアーキテクチャ（Zenn）](https://zenn.dev/yosugi/articles/llm-friendly-architecture)

- **コンテキストの最小化**: 1つの修正で見る範囲を小さくする
- **純粋関数の最大化**: 副作用のないロジックとI/Oを分離する
- **Package by Feature**: 技術的役割（controller/service/repository）ではなく、業務機能単位でディレクトリを切る

## 3. 命名規則の原則

**言語・フレームワークの標準的な慣習に従う**ことを大原則とする。

| 対象 | ファイル名 | ディレクトリ名 | 根拠 |
|---|---|---|---|
| Python（バックエンド） | スネークケース | スネークケース | PEP 8 / Pythonコミュニティ標準 |
| TypeScript（フロントエンド） | キャメルケース | キャメルケース | React/TypeScriptコミュニティ標準 |

### バックエンド: 処理の種類ごとのファイル接尾辞

| 接尾辞 | 役割 |
|---|---|
| `*_pure.py` | 副作用のない純粋ロジック（計算等） |
| `*_io.py` | 副作用のある処理（DBアクセス、外部API呼び出し） |
| `*_usecase.py` | オーケストレーション（pure/ioの呼び出しを束ねる） |

### フロントエンド: TanStack Queryフックの命名

| 接尾辞 | 役割 |
|---|---|
| `use*Query.ts` | データ取得（`useQuery`のラップ） |
| `use*Mutation.ts` | データ更新（`useMutation`のラップ。関連キャッシュの無効化処理も含む） |

バックエンドの`*_usecase.py`とフロントエンドの`use*Query.ts`/`use*Mutation.ts`は、それぞれの言語・フレームワークの慣習に従った「オーケストレーション層」として対応する関係にある。

## 4. デュアルエントリポイント（WebAPI層 / MCP層）

バックエンドはWebAPI層とMCP層という2つの入口を持つが、いずれも共通のusecase層を呼び出す薄いラッパーとして実装する（NFR-003）。

```
api/order_router.py  ─┐
                       ├─→ features/order/.../xxx_usecase.py
mcp/order_tools.py   ─┘
```

各エントリポイントは「リクエスト/レスポンスの変換」のみを担当し、業務ロジックを持たない。

## 5. ORMモデルとドメインEntityの扱い

- `common/`: 業務に依存しない共通要素のみを置く（ORMモデルは含まない）
- `db/models/`: SQLAlchemyのORMモデル（テーブル定義）
- `db/migrations/`: Alembicのマイグレーション

**Phase 1時点の方針**: ORMモデルとドメインEntityは分離せず、ORMモデルを直接usecase/pureで使用する。各featureの`shared/`にEntity定義（例: `order_entity.py`）を置く構成は将来の拡張ポイントとして用意するが、ロジックが肥大化した時点で導入を検討する（YAGNI）。

## 6. バックエンドディレクトリ構成

```
backend/
  app/
    main.py                      # FastAPIエントリポイント（起動時リカバリ呼び出し等）
    api/                         # WebAPI層（フレームワーク接続層）
      __init__.py
      router.py
      account_router.py
      order_router.py
      price_router.py
    mcp/                         # MCP層（フレームワーク接続層）
      __init__.py
      server.py
      account_tools.py
      order_tools.py
      price_tools.py
    features/                   # Package by Feature
      common/                   # 業務非依存の共通要素（ORMモデル含まない）
        money.py
        datetime_utils.py
      account/
        shared/
          account_status.py
        create/
          create_account_usecase.py
          create_account_io.py
        delete/
          delete_account_usecase.py
          delete_account_io.py
        list/
          list_accounts_usecase.py
          list_accounts_io.py
      price/
        shared/
          price_source_adapter.py   # PriceSourceAdapterインターフェース
        ingest/
          ingest_price_usecase.py
          ingest_price_io.py
          bitflyer_realtime_io.py
        get_current/
          get_current_price_usecase.py
          get_current_price_io.py
        recover/                    # Phase 3: 停止期間リカバリ
          recover_price_history_usecase.py
          recover_price_history_io.py
      order/
        shared/
          order_status.py
          order_entity.py           # 将来の拡張ポイント（Phase 1では未使用）
        place_market/
          place_market_order_usecase.py
          place_market_order_pure.py
          place_market_order_io.py
        list/
          list_orders_usecase.py
          list_orders_io.py
      execution/
        shared/
        list/
          list_executions_usecase.py
          list_executions_io.py
    db/
      session.py
      models/                      # ORMモデル（SQLAlchemy）
        account_model.py
        order_model.py
        execution_model.py
        system_status_model.py
      migrations/                  # Alembic
        env.py
        versions/
    config.py
  tests/
    features/
      account/
      order/
      price/
  pyproject.toml
  alembic.ini
  .env.example
```

## 7. フロントエンドディレクトリ構成

```
frontend/
  src/
    main.tsx
    App.tsx
    router.tsx
    api/                          # APIクライアント（フレームワーク接続層）
      client.ts
      accountApi.ts
      orderApi.ts
      priceApi.ts
    features/                    # Package by Feature
      common/
        money.ts
        dateFormat.ts
      account/
        shared/
          accountTypes.ts
        list/
          useAccountsQuery.ts
          accountListPage.tsx
        create/
          useCreateAccountMutation.ts
          createAccountForm.tsx
          createAccountSchema.ts    # Zod schema
        delete/
          useDeleteAccountMutation.ts
      price/
        shared/
          priceTypes.ts
        display/
          usePriceQuery.ts
          priceDisplay.tsx
      order/
        shared/
          orderTypes.ts
        placeMarket/
          usePlaceMarketOrderMutation.ts
          marketOrderForm.tsx
          marketOrderSchema.ts
        list/
          useOrdersQuery.ts
          orderHistoryTable.tsx
    components/
      ui/                         # shadcn/uiの生成物（業務ロジックを含まない共通UI）
    store/                        # Zustand（必要になった時点で導入）
    lib/
      utils.ts
  index.html
  vite.config.ts
  tsconfig.json
  package.json
  .env.example
```

## 8. 既知の注意点・未決事項

- **`api/`の名称の重複**: バックエンドの`api/`は「WebAPIのルーター（提供側）」、フロントエンドの`api/`は「APIクライアント（呼び出し側）」を指す。同名だが役割が異なる点に注意する。
- **Alembicのパス設定**: `db/migrations/`をリポジトリ構成に合わせて配置する際、`alembic.ini`内のパス設定を調整する必要がある（Phase 0の作業項目として追加予定）。
- **`order`機能の肥大化対応**: Phase 4でOCO/IFD注文を追加する際、注文間の関連性（親子関係・グルーピング）を`order`配下に置くか、別機能として切り出すかは現時点では未決定。実装時に再検討する。
