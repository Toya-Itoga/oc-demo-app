# CLAUDE.md

## アーキテクチャ
- レイヤードアーキテクチャ

## レンダリング方式
- サーバーサイドレンダリング

## ディレクトリ・ファイル構成
- `.venv/`                                                - 仮想環境
- `src/main.py`                                           - アプリ本体
- `src/routers/`                                          - ルータ層
- `src/services/`                                         - サービス層
- `src/repositories/`                                     - リポジトリ層
- `src/templates/lots_show.html`                          - ロット一覧画面HTML
- `src/templates/report_show.html`                        - 日報表示画面HTML
- `src/templates/report_registration.html`                - 日報登録画面HTML
- `src/templates/components/lot_registration_dialog.html` - ロット登録ダイアログHTML
- `src/static/js/lots_show.js`                            - ロット一覧画面JaveScript
- `src/static/js/report_show.js`                          - 日報表示画面JavaScript
- `src/static/js/report_registration.js`                  - 日報登録画面JavaScript
- `src/static/js/lot_registration_dialog.js`              - ロット登録ダイアログJavaScript
- `src/static/css/lots_show.css`                          - ロット一覧画面CSS
- `src/static/css/report_show.css`                        - 日報表示画面CSS
- `src/static/css/report_registration.css`                - 日報登録画面CSS
- `src/static/css/lot_registration_dialog.css`            - ロット登録ダイアログCSS
- `src/schema/lot_schema.py`                              - ロットデータバリデーション(Pydantic)
- `src/schema/report_schema.py`                           - レポートデータバリデーション(Pydantic)
- `src/utils/`                                            - ユーティリティ関数定義
- `src/utils/demo_data.py`                                - ダミーデータ集約
- `src/utils/datetime_utils.py`                           - 日時取得ユーティリティ関数定義
- `src/database.py`                                       - データベース接続設定定義(SQLite)
- `src/models/lot.py`                                     - Lotsテーブルスキーマ定義
- `src/models/report.py`                                  - Reportsテーブルスキーマ定義
- `src/imgs/`                                             - 写真保存
- `config/`                                               - 設定・ドキュメント
- `scripts/`                                              - 開発補助スクリプト
- `tests/`                                                - テストコード
- `.claude/commands/`                                     - コマンド

## コーディング規約
- コメントを書くこと
- コードを機能単位のブロックで分割すること
- 生成するコードはsrc/に配置すること
- config/のファイルは読み取り専用とすること
- 機能を実装する際は必ずtests/にテストを作成すること
- HTMLのクラス名はBEM記法を遵守すること
- 変更理由を説明すること
- 既存コードは壊さない
- 変更は必ずdiff形式で出力すること

## データベース
- 環境ごとにDBを分けること
- 本番環境とテスト環境のDBを分けること

## 禁止事項
- .envファイルの参照
- any型の乱用禁止
- ハードコードされたダミーデータを本番コードに含めないこと
- TODOコメントを残したまま実装を完了しないこと
- import文にsrc.プレフィックスを含めないこと

## Lambda対応
- 静的ファイルのパスはsrc/を含めないこと
  - StaticFiles(directory="static")
  - Jinja2Templates(directory="templates")
- import文はsrc.を含めないこと

## 更新ポリシー
- 機能追加時はREADME.mdを更新すること
- AIが間違った動作をしたらここに反映すること

## 技術スタック
- Python3.12
- FastAPI
- Pydantic
- uvicorn
- HTMX
- Alpine.js
- SQLAlchemy
- Jinja2
- SQLite