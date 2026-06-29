# 農業日報管理アプリ

農場作業者がロット単位で日報を作成・閲覧できる Web アプリ。  
作業者の入力内容をもとに AI が日報要約を自動生成する。

---

## 画面構成と機能

### ロット一覧画面 `/`

登録されている栽培ロットをカード形式で一覧表示する。

| 表示項目 | 内容 |
|---|---|
| ロットID | 一意の識別子（例: `DEMO_LOT1`） |
| 栽培品目・品種 | 例: `トマト・シンディー` |
| 農場名 / 棟番号 / 定植本数 | ロットの詳細情報 |

**操作**

- `日報を書く` — 日報作成画面へ遷移
- `日報を見る` — 最新日報の閲覧画面へ遷移
- `編集` — ロット編集ダイアログを開く
- `＋`（右下 FAB） — ロット登録ダイアログを開く

起動時にデモロット 3 件（DEMO_LOT1〜3）が自動登録される。

---

### 日報作成画面 `/lots/{lot_id}/report/new`

ロット単位で当日の日報を作成する。1 ロット 1 日 1 レポート（アップサート）。

| 入力項目 | 内容 |
|---|---|
| 植物の状態 | 1〜5 の 5 段階スライダー |
| 病害虫の状況 | 1〜5 の 5 段階スライダー |
| 写真 | 最大 3 枚アップロード（`src/imgs/` に保存） |
| コメント | 200 文字以内のテキスト |

**保存時の動作**

1. センサーデータ（気温・湿度）をランダム生成して DB に保存
2. AI まとめテキストを生成（`src/utils/demo_data.py` の固定テキスト）
3. 日報閲覧画面へリダイレクト
4. 閲覧画面でタイピングアニメーションと保存完了トーストを表示

当日の日報が既に存在する場合は、登録済み内容をフォームに初期表示する。

---

### 日報閲覧画面 `/lots/{lot_id}/report/{report_id}`

作成済み日報を閲覧する。

| 表示項目 | 内容 |
|---|---|
| センサーデータ | 気温・湿度（保存時のランダム値） |
| 植物の状態 / 病害虫の状況 | ドット 5 個で評価を表示 |
| 写真 | アップロード済み画像のサムネイル |
| コメント | 作業者の入力テキスト |
| AI まとめ | 自動生成された日報要約 |
| 日報タイムライン（右カラム） | このロットの過去日報一覧 |

保存直後のアクセス時のみ AI まとめをタイピングアニメーションで表示する。

---

### ロット登録・編集ダイアログ

新規登録と編集でダイアログを共通化（`src/templates/components/lot_registration_dialog.html`）。  
HTMX で取得し `innerHTML` に差し込む。Alpine.js で開閉を管理。

| モード | エンドポイント | ボタン |
|---|---|---|
| 新規登録 | `GET /lots/dialog/new` | 登録 / キャンセル |
| 編集 | `GET /lots/{lot_id}/dialog/edit` | 保存 / 削除 / キャンセル |

編集時はロット ID を `readonly` にして変更不可にする。  
削除時は紐づく日報・画像ファイルもカスケード削除する。

---

## ディレクトリ・ファイル構成

```
.
├── requirements.txt                                  # Python 依存パッケージ
├── src/
│   ├── main.py                                       # FastAPI エントリポイント
│   ├── database.py                                   # DB 接続設定（SQLite / SQLAlchemy）
│   ├── models/
│   │   ├── lot.py                                    # Lots テーブルスキーマ
│   │   └── report.py                                 # Reports テーブルスキーマ
│   ├── repositories/
│   │   ├── lot_repository.py                         # Lots の CRUD
│   │   └── report_repository.py                      # Reports の CRUD
│   ├── services/
│   │   ├── lot_service.py                            # ロットのビジネスロジック（カスケード削除等）
│   │   └── report_service.py                         # 日報のビジネスロジック（アップサート等）
│   ├── routers/
│   │   ├── lots.py                                   # ロット関連ルータ
│   │   └── reports.py                                # 日報関連ルータ
│   ├── schema/
│   │   ├── lot_schema.py                             # Pydantic バリデーション（ロット）
│   │   └── report_schema.py                          # Pydantic バリデーション（日報）
│   ├── utils/
│   │   ├── demo_data.py                              # デモ用ロット・AI まとめ・センサーデータ生成
│   │   └── datetime_utils.py                         # 日時取得ユーティリティ
│   ├── templates/
│   │   ├── lots_show.html                            # ロット一覧画面
│   │   ├── report_registration.html                  # 日報作成画面
│   │   ├── report_show.html                          # 日報閲覧画面
│   │   └── components/
│   │       └── lot_registration_dialog.html          # ロット登録・編集ダイアログ
│   ├── static/
│   │   ├── css/
│   │   │   ├── app.css                               # 共通スタイル・デザイントークン
│   │   │   ├── lots_show.css                         # ロット一覧画面 CSS
│   │   │   ├── report_registration.css               # 日報作成画面 CSS
│   │   │   ├── report_show.css                       # 日報閲覧画面 CSS
│   │   │   └── lot_registration_dialog.css           # ダイアログ CSS
│   │   └── js/
│   │       ├── lots_show.js                          # ロット一覧画面 Alpine.js コンポーネント
│   │       ├── report_registration.js                # 日報作成画面 Alpine.js コンポーネント
│   │       ├── report_show.js                        # 日報閲覧画面 Alpine.js コンポーネント
│   │       └── lot_registration_dialog.js            # ダイアログ Alpine.js コンポーネント
│   └── imgs/                                         # アップロード写真の保存先
├── tests/                                            # テストコード
├── config/
│   ├── requirements.md                               # 機能要件定義
│   ├── implement.md                                  # 実装タスク管理
│   └── HANDOFF.md                                    # デザインハンドオフ仕様書
└── .claude/
    └── commands/                                     # Claude Code カスタムコマンド
```

## 技術スタック

| 領域 | 採用技術 |
|---|---|
| サーバ | Python 3.12 / FastAPI / uvicorn |
| DB | SQLite（SQLAlchemy ORM） |
| テンプレート | Jinja2（サーバーサイドレンダリング） |
| 部分更新 | HTMX 2.0 |
| クライアント状態 | Alpine.js 3.x |
| バリデーション | Pydantic |
| ID 生成 | python-ulid |
