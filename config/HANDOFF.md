# 農業日報管理アプリ ― 実装仕様書（HANDOFF）

本書はデザイン（`農業日報アプリ デザイン案.dc.html`）を実装に落とし込むための仕様書です。
デザインで確定したレイアウト・カラー・フォント・寸法・アニメーション・BEMクラス設計を記載します。
バックエンド連携の手順は `implement.md` を参照してください。

---

## 0. 技術スタック前提（requirements.md より）

| 領域 | 採用技術 |
|---|---|
| サーバ | FastAPI + uvicorn（ローカル起動） |
| DB | SQLite |
| テンプレート | Jinja2（`src/templates/`） |
| 部分更新 | HTMX（ダイアログを `components/` から取得し `innerHTML` で差し込む） |
| クライアント状態 | Alpine.js（ダイアログ開閉、トースト表示） |
| 画像保存 | `src/imgs/`（`{date}_{ulid}` 形式） |

- 認証なし（デモ版）。**PCブラウザ専用**。
- AI要約はダミーテキスト（`src/utils/demo_data.py`）。センサーデータは固定ダミー。

> デザインは React ベースのプロトタイプですが、本実装は **Jinja + HTMX + Alpine** で再現します。
> 本書のクラス名・トークン・寸法をそのまま CSS（`src/static/css/app.css` 等）へ移植してください。

---

## 1. 全体構成

### 1.1 レイアウト

```
┌──────────────────────────────────────────────┐
│  page (背景 #e4e9df / 上下30px・左右24pxパディング)  │
│   ┌────────────────────────────────────────┐   │
│   │ app shell（最大幅1180px / 角丸28px / 中央寄せ）│   │
│   │ ┌────────────────────────────────────┐ │   │
│   │ │ topbar（白背景・ロゴ＋アプリ名）          │ │   │
│   │ ├────────────────────────────────────┤ │   │
│   │ │ screen area（一覧 / 作成 / 閲覧を切替）   │ │   │
│   │ └────────────────────────────────────┘ │   │
│   │  ※ ダイアログ・トーストは shell 内に重ねる   │   │
│   └────────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

- アプリ全体を1枚の**角丸シェル**（`max-width:1180px` / `min-height:780px` / `border-radius:28px` / `overflow:hidden`）に収める。
- シェルは `position:relative`。**ダイアログ（オーバーレイ）とトーストはシェル内に絶対配置**で重ねる。
- 画面（一覧・作成・閲覧）は**シェル内で1画面ずつ切替**（HTMXのコンテンツ差し替え or 別ルートのフルページ）。

### 1.2 カラーパレット

#### ブランドグリーン
| 用途 | HEX |
|---|---|
| プライマリ（ボタン・ロゴ・FAB・選択） | `#6fae6b` |
| プライマリ hover | `#5e9d5a` |
| 濃グリーン（見出し強調・トースト背景） | `#3f5e3a` |
| アクセントグリーン（テキスト・アウトライン文字） | `#4f8d52` |
| ステップ点灯（中間） | `#cfe6cb` / 枠 `#a8d3a2` |
| スライダー塗り | `linear-gradient(90deg,#9bcf97,#6fae6b)` |

#### 背景・面
| 用途 | HEX |
|---|---|
| ページ背景 | `#e4e9df` |
| アプリシェル背景 | `#eef5ec` |
| カード・パネル・トップバー | `#ffffff` |
| 薄グリーン面（バッジ・選択カード等） | `#e8f2e4` / `#eaf5e6` / `#f1f8ee` |
| 入力欄背景 | `#f6faf4`（focus時 `#fff`） |
| 読取専用入力背景 | `#eef1ec` |
| ゴーストボタン背景 | `#f1f4ee`（hover `#e6efe1`） |
| AIまとめカード | `linear-gradient(180deg,#f1f8ee,#e8f3e3)` |

#### 枠線
| 用途 | HEX |
|---|---|
| シェル枠 | `#dce8d5` |
| カード枠（薄） | `#ecf2e8` |
| パネル枠 | `#e7eee1` |
| 入力枠 | `#dfe9d8` / `#e2ecdc` |
| 破線区切り | `#e6ede1` |
| AIカード枠 | `#d4e6cd` |

#### テキスト
| 用途 | HEX |
|---|---|
| メイン | `#2e3a2c` |
| 本文 | `#3a4736` |
| サブ（強調・品種名） | `#5a6b56` |
| ミュート | `#8a9786` |
| ミュート（ラベル） | `#9aa896` |
| ミュート（ボタン文字） | `#7c8a78` |
| ヒント（任意・補足） | `#b9c6b3` |

#### 状態色
| 用途 | HEX |
|---|---|
| 削除（danger）文字 / 背景 | `#d36a52` / `#fdeeec`（hover `#fbe3e0`） |
| 評価ドット（点灯 / 消灯） | `#6fae6b` / `#dde7d6` |

### 1.3 フォント

```html
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
```

| 役割 | フォント | ウェイト |
|---|---|---|
| 見出し・数値・ロゴ（`--font-display`） | `'Zen Maru Gothic'` | 700 / 800 / 900 |
| 本文・UI・ボタン（`--font-body`） | `'M PLUS Rounded 1c'` | 400 / 500 / 700 / 800 |

#### タイプスケール
| トークン | サイズ / ウェイト / フォント | 用途 |
|---|---|---|
| display-xl | 26px / 800 / display | 閲覧画面のロットID |
| display-lg | 25px / 800 / display | 画面タイトル（ロット一覧） |
| display-md | 24px / 800 / display | カードのロットID |
| display-sm | 23px / 800 / display | 作成画面のロットID |
| number | 34px / 800 / display | センサー数値 |
| title | 19–20px / 800 / display | アプリ名・ダイアログ見出し |
| body | 14px / 500 / body | 本文・コメント |
| label | 13–13.5px / 500–700 / body | 補助ラベル |
| section | 12px / 700 / body（`letter-spacing:.05em`） | セクション見出し |
| micro | 11.5–12px / 500 / body | カウンタ・タグ・補足 |

### 1.4 デザイントークン（CSS変数）

```css
:root{
  /* color */
  --c-primary:#6fae6b;        --c-primary-hover:#5e9d5a;
  --c-primary-deep:#3f5e3a;   --c-accent:#4f8d52;
  --c-page:#e4e9df;           --c-shell:#eef5ec;
  --c-surface:#ffffff;
  --c-tint:#e8f2e4;           --c-tint-soft:#f1f8ee;  --c-tint-card:#eaf5e6;
  --c-input:#f6faf4;          --c-input-ro:#eef1ec;
  --c-ghost:#f1f4ee;          --c-ghost-hover:#e6efe1;
  --c-border-shell:#dce8d5;   --c-border-card:#ecf2e8;
  --c-border-panel:#e7eee1;   --c-border-input:#dfe9d8;
  --c-dash:#e6ede1;
  --c-text:#2e3a2c;           --c-text-body:#3a4736;
  --c-text-sub:#5a6b56;       --c-muted:#8a9786;
  --c-muted-2:#9aa896;        --c-muted-3:#7c8a78;  --c-hint:#b9c6b3;
  --c-danger:#d36a52;         --c-danger-bg:#fdeeec; --c-danger-bg-hover:#fbe3e0;
  --c-dot-on:#6fae6b;         --c-dot-off:#dde7d6;
  --grad-slider:linear-gradient(90deg,#9bcf97,#6fae6b);
  --grad-ai:linear-gradient(180deg,#f1f8ee,#e8f3e3);

  /* radius */
  --r-shell:28px; --r-dialog:24px; --r-card:22px; --r-fab:20px;
  --r-panel:18px; --r-photo:16px; --r-input:12px; --r-btn:13px;
  --r-btn-sm:10px; --r-pill:99px;

  /* shadow */
  --sh-shell:0 28px 70px rgba(55,80,50,.22);
  --sh-card:0 4px 16px rgba(70,95,60,.06);
  --sh-card-hover:0 22px 42px rgba(70,105,60,.18);
  --sh-fab:0 12px 26px rgba(111,174,107,.55);
  --sh-btn:0 8px 20px rgba(111,174,107,.4);
  --sh-toast:0 14px 32px rgba(40,60,35,.38);
  --sh-dialog:0 30px 70px rgba(30,45,28,.4);

  /* font */
  --font-display:'Zen Maru Gothic',sans-serif;
  --font-body:'M PLUS Rounded 1c',sans-serif;

  /* motion */
  --ease-pop:cubic-bezier(.2,.9,.3,1.2);
  --dur-screen:.4s; --dur-dialog:.42s; --dur-toast:.4s;
  --toast-life:2600ms;
}
```

### 1.5 共通コンポーネント（ボタン等）

| 種別 | クラス | スタイル要点 |
|---|---|---|
| プライマリ | `.btn .btn--primary` | bg `--c-primary` / 文字白 / `--r-btn` / hover `--c-primary-hover` |
| アウトライン | `.btn .btn--outline` | bg白 / 文字 `--c-accent` / 枠 `1.5px #bcdcb6` / hover bg `--c-tint-soft` |
| ゴースト | `.btn .btn--ghost` | bg `--c-ghost` / 文字 `--c-muted-3` / hover bg `--c-ghost-hover` 文字 `--c-accent` |
| 中立（キャンセル） | `.btn .btn--neutral` | bg白 / 文字 `--c-muted-3` / 枠 `1.5px #dde7d6` |
| 危険（削除） | `.btn .btn--danger` | bg `--c-danger-bg` / 文字 `--c-danger` / hover bg `--c-danger-bg-hover` |
| 小サイズ | `.btn--sm` | `padding:8–9px 14–15px` / `font-size:12.5px` |

- ボタン共通：`font-weight:700` / `font-family:var(--font-body)` / `cursor:pointer` / `transition:background .2s` または `transform .2s`。

---

## 2. 画面別仕様

### 2.1 ルーティング

| 画面 | パス |
|---|---|
| ロット一覧 | `GET /` |
| 日報作成 | `GET /lots/{lot_id}/report/new` |
| 日報閲覧 | `GET /lots/{lot_id}/report/{report_id}` |
| 登録ダイアログ（部分HTML） | `GET /lots/dialog/new` |
| 編集ダイアログ（部分HTML） | `GET /lots/{lot_id}/dialog/edit` |

---

### 2.2 ロット一覧画面（`/`）

**構成**：画面タイトル＋件数 → 3カラムのロットカードグリッド → 右下にFAB（＋）。

**ロットカード（`.lot-card`）の表示順**
1. 右上に **「編集」ボタン**（`.lot-card__edit`、`position:absolute; top:16px; right:16px`）
2. **ロットID**を大きく表示（`.lot-card__id` / 24px / display / 800）
3. その下に **作物・品種**（`.lot-card__crop` / 14px / 700 / `--c-text-sub`）。例：`トマト・シンディー`
4. 破線区切り（`--c-dash`）の下に明細：農場 / 棟番号 / 定植本数（ラベル左・値右）
5. 下部に2ボタン：**日報を書く**（primary）／ **日報を見る**（outline）

| 項目 | 値 |
|---|---|
| グリッド | `display:grid; grid-template-columns:repeat(3,1fr); gap:22px` |
| カード | `padding:24px 22px 22px` / `--r-card` / 枠 `--c-border-card` / `--sh-card` |
| カード hover | `translateY(-7px)` ＋ `--sh-card-hover`（`transition:.28s`） |
| FAB | `60×60` / `--r-fab` / bg `--c-primary` / `--sh-fab` / 文字「＋」32px |
| FAB hover | `translateY(-3px) rotate(90deg)`（`transition:.3s`） |

- **作物アイコン（絵文字）・画面右上の年月日・「作」アイコンは表示しない**（デザイン確定）。
- 操作：日報を書く→作成画面、日報を見る→閲覧画面、編集→編集ダイアログ、FAB→登録ダイアログ。
- 当日レポートの有無は作成画面側で判定（§2.3 備考）。

---

### 2.3 日報作成画面（`/lots/{lot_id}/report/new`）

**構成**：戻るリンク → ロット情報バナー → 評価スライダー2枚 → 写真 → コメント → 操作ボタン。

| ブロック | 仕様 |
|---|---|
| 戻るリンク `.back-link` | 「← ロット一覧へもどる」。左に30px角丸の戻るアイコン。 |
| ロットバナー `.lot-banner` | 左：**ロットIDを大きく**（23px）＋下に作物・品種・農場・棟。右：日付（`2026.06.28`）。**作物アイコンなし**。 |
| 評価スライダー `.rating` | 「植物の状態」「病害虫の状況」を**1〜5の5段階**で選択。下端に「悪い／良い」。**「良好」「問題なし」等のステータスバッジは表示しない**。 |
| 写真 `.photos` | 最大3枚。サムネ128px角丸16px、右上に削除「×」。空きスロットは破線「＋ 写真を追加」。 |
| コメント `.textarea` | `maxlength=200`、右下に `{n} / 200` カウンタ。 |
| 操作 | 右寄せで **キャンセル**（neutral）／ **保存する**（primary）。 |

#### 5段階スライダー（`.rating`）詳細
- トラック：`height:6px`、ベース `#e7ede2`、塗り `--grad-slider`、塗り幅 `= (value-1)/4*100%`。
- ステップ：`30×30` の円を5個（`justify-content:space-between`）。クリックで値確定（`transition:transform .15s`、hover `scale(1.12)`）。

| ステップ状態 | 背景 | 枠 | 文字色 |
|---|---|---|---|
| 選択中（`--selected`） | `#6fae6b` | `3px solid #5e9d5a` | `#fff` |
| 点灯（`--on`、選択値以下） | `#cfe6cb` | `2px solid #a8d3a2` | `#4f8d52` |
| 消灯 | `#fff` | `2px solid #e1ebdb` | `#b7c3b1` |

#### 操作・ビジネスロジック
- **「保存する」押下でロット一覧へリダイレクト**し、トースト「日報を保存しました」を表示（§4.3）。
- 1ロット1日1レポート。画面アクセス時に**当日レポートの存在を確認**し、あれば登録済み内容を初期表示、なければ新規フォーム。
- 現在日時は `src/utils/datetime_utils.py` の関数で取得。写真は `src/imgs/` に `{date}_{ulid}` で保存（最大3枚・個別削除可）。

---

### 2.4 日報閲覧画面（`/lots/{lot_id}/report/{report_id}`）

**構成**：戻るリンク → ヘッダ → 2カラム（左：本体 / 右：日報タイムライン）。

| ブロック | 仕様 |
|---|---|
| ヘッダ | 左：**ロットIDを大きく**（26px）＋作物・品種・農場・棟。右：日報の日付。**曜日は表示しない**（例：`2026年6月28日`）。**作物アイコンなし**。 |
| センサーデータ `.sensor-grid` | 気温・湿度の2カード。数値34px。**固定ダミー**（温度・湿度）。 |
| 作業者の入力 `.worker-input` | 植物の状態 / 病害虫の状況を**ドット5個＋「n / 5」**で表示。**「良好」「問題なし」等のステータス文言は表示しない**。写真サムネ、コメント。 |
| AIまとめ `.ai-summary` | グラデ面のカード。`✦ AIまとめ` バッジ＋「作業者の入力をもとに自動生成」。本文は `src/utils/demo_data.py` の固定テキスト。 |
| 日報タイムライン `.report-timeline` | 右カラム。**このロットに紐づく他日報を時系列の小カードで一覧**。クリックで該当日報の詳細に切替。 |

- レイアウト：`grid-template-columns:1.15fr .85fr; gap:18px; align-items:start`。
- **「ロット一覧へ」ボタンは廃止**（戻るリンクのみ）。

#### タイムラインカード（`.timeline-card`）
| 状態 | 背景 | 枠 | タグ |
|---|---|---|---|
| 表示中（`--active`） | `#eaf5e6` | `1.5px solid #6fae6b` | `表示中`（白文字 / bg `#6fae6b`） |
| 非選択 | `#fff` | `1px solid #e7eee1` | `見る`（`#7c8a78` / bg `#f1f4ee`） |
- 中身：日付（`6月28日`、15px display）＋「植物 n ・ 病害虫 n」。hover `translateY(-2px)` ＋ 影。

---

### 2.5 ロット登録・編集ダイアログ

**新規登録・編集でダイアログを共通化**（`src/templates/components/lot_registration_dialog.html`）。
HTMXで `components/` から取得し `innerHTML` で差し込む。開閉は Alpine.js。

| 取得 | エンドポイント | 中身 |
|---|---|---|
| 新規登録 | `GET /lots/dialog/new` | **全項目空欄**のダイアログ |
| 編集 | `GET /lots/{lot_id}/dialog/edit` | DBから取得し**各項目に初期表示**したダイアログ |

**共通レイアウト**：オーバーレイ（`rgba(40,55,38,.42)`）＋中央のカード（`width:460px` / `--r-dialog` / `--sh-dialog`）。

**入力項目**（縦並び。農場名/棟番号、栽培品目/栽培品種は2カラム）
1. ロットID（`例: DEMO_LOT4`）
2. 農場名 / 棟番号
3. 栽培品目 / 栽培品種（任意）
4. 定植本数（任意）

| モード差分 | 新規登録 | 編集 |
|---|---|---|
| 見出し | `ロットを登録` | `ロットを編集` |
| ロットID | 入力可（bg `#f6faf4`） | **`readonly`**・グレー表示（bg `#eef1ec` / 文字 `#9aa896`）・ラベルに「（変更不可）」 |
| フッター | キャンセル / **登録** | **削除**（左） ／ キャンセル / **保存** |
| 完了トースト | 「ロットを登録しました」 | 「ロットを保存しました」 |

- **ロットIDの南京錠（🔒）アイコンは表示しない**（テキスト「（変更不可）」のみ）。
- 削除時は該当ロットに紐づく Reports と画像ファイル（`src/imgs/`）も削除。
- 登録/保存の押下で**完了トーストを表示**（§4.3）。
- **JSON埋め込みは `<script>`タグ＋windowオブジェクト経由**で行うこと（`x-data` 属性内にJSON直書きしない）。

```html
<!-- 例：編集ダイアログの初期値受け渡し -->
<script>window.__lotForm = {{ lot | tojson }};</script>
<div x-data="lotDialog()" x-init="init()"> … </div>
```

---

## 3. コンポーネント構造

```
App (.app)
├─ Topbar (.app__topbar)           … ロゴ＋アプリ名（全画面共通）
├─ Screen: LotList (.lot-list)     … GET /
│   ├─ ListHeader (.lot-list__header)
│   ├─ LotCard (.lot-card) ×N
│   │   ├─ EditButton (.lot-card__edit)
│   │   ├─ LotId / Crop (.lot-card__id / __crop)
│   │   ├─ Meta (.lot-card__meta)
│   │   └─ Actions (.lot-card__actions → .btn--primary / .btn--outline)
│   └─ Fab (.fab)
├─ Screen: ReportForm (.report-form) … GET /lots/{id}/report/new
│   ├─ BackLink (.back-link)
│   ├─ LotBanner (.lot-banner)
│   ├─ Rating (.rating) ×2          … 植物 / 病害虫（5段階）
│   ├─ Photos (.photos → .photo / .photo-add)
│   ├─ CommentField (.field → .textarea + .char-count)
│   └─ FormActions (.form-actions → .btn--neutral / .btn--primary)
├─ Screen: ReportView (.report-view) … GET /lots/{id}/report/{rid}
│   ├─ BackLink (.back-link)
│   ├─ ViewHeader (.report-view__header)
│   ├─ Left
│   │   ├─ SensorGrid (.sensor-grid → .sensor-card ×2)
│   │   ├─ WorkerInput (.worker-input → .rating-readout ×2 / 写真 / コメント)
│   │   └─ AiSummary (.ai-summary)
│   └─ Right: ReportTimeline (.report-timeline → .timeline-card ×N)
├─ Overlay: LotDialog (.modal → .lot-dialog)  … components/ から差込
└─ Toast (.toast)                  … 保存・登録・編集の完了通知
```

- **共通子コンポーネント**：`.btn`（modifierで種別分岐）、`.rating`（作成）、`.rating-readout`（閲覧）、`.lot-dialog`（新規/編集共通）。
- ロットカードとタイムラインカードは繰り返し要素。Jinjaの `{% for %}` で出力。

---

## 4. アニメーション仕様

```css
@keyframes fadeIn   { from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none} }
@keyframes pop      { 0%{transform:scale(.92)} 60%{transform:scale(1.02)} 100%{transform:scale(1)} }
@keyframes toastIn  { 0%{transform:translate(-50%,16px)} 100%{transform:translate(-50%,0)} }
@keyframes aiCaret  { 0%,49%{opacity:1} 50%,100%{opacity:0} }     /* タイピング用カーソル */
@keyframes spin     { to{transform:rotate(360deg)} }              /* 要約中スピナー */
@keyframes dotPulse { 0%,80%,100%{opacity:.2; transform:scale(.8)} 40%{opacity:1; transform:scale(1)} }
```

### 4.1 画面遷移フェードイン
- 画面（一覧/作成/閲覧）の表示時に `animation: fadeIn var(--dur-screen) ease;`。
- **実装上の注意**：`opacity:0` のまま固定されるのを防ぐため、要素の**基準 opacity は 1**にし、`animation-fill-mode` に `forwards/both` を使わない（HTMXの差し替えコンテンツに付与する場合も同様）。フェードはあくまで装飾で、未再生でも内容が必ず見える状態にする。
- HTMX利用時：`htmx:afterSwap` で対象に `fadeIn` を付与、または差し込むコンテナに直接付与。

### 4.2 AI要約生成時のタイピングアニメーション
保存→閲覧遷移直後に、AIまとめを「生成中→タイプ表示」で演出する。

**フェーズ**
1. **ローディング**（約1.9s）：スピナー（`spin .8s linear infinite`）＋「AIが日報を要約中…」＋3点パルス（`dotPulse 1.2s`、`.2s`ずつ遅延）。
2. **タイピング**：確定テキスト（`src/utils/demo_data.py`）を**1文字ずつ**追記（約40ms/字）。末尾に点滅カーソル `.ai-summary__caret`（`aiCaret 1s step-end infinite`、`width:2.5px; height:19px; bg:var(--c-primary)`）。
3. **完了**：カーソル消灯。

**実装メモ（Alpine.js 例）**
```js
function aiSummary(full){
  return {
    phase:'loading', shown:'',
    init(){
      setTimeout(()=>{ this.phase='typing'; let i=0;
        const iv=setInterval(()=>{ this.shown=full.slice(0,++i);
          if(i>=full.length){ clearInterval(iv); this.phase='done'; } }, 40);
      }, 1900);
    }
  }
}
```
- 既読の日報を再表示する場合はアニメ無し（全文即時表示）。**新規保存直後のみ**演出する。

### 4.3 保存完了時のトースト通知
- 位置：シェル下端中央（`position:absolute; left:50%; bottom:28px; transform:translateX(-50%)`）。
- 背景 `--c-primary-deep` / 白文字 / `--r-btn+1` / `--sh-toast` / 先頭に丸チェック（bg `--c-primary`）。
- 出現：`animation: toastIn var(--dur-toast) var(--ease-pop) both;`。
- **自動消去：2600ms**（`--toast-life`）。
- メッセージ分岐：
  - 日報保存 → **「日報を保存しました」**
  - ロット登録 → **「ロットを登録しました」**
  - ロット編集保存 → **「ロットを保存しました」**

**実装メモ（Alpine + HTMXイベント）**
```js
// 各保存処理の成功後に発火
window.dispatchEvent(new CustomEvent('toast', { detail:{ msg:'日報を保存しました' } }));
```
```html
<div x-data="{show:false,msg:''}"
     @toast.window="msg=$event.detail.msg; show=true; clearTimeout(t); t=setTimeout(()=>show=false,2600)">
  <div class="toast" x-show="show" x-transition>
    <span class="toast__icon">✓</span><span x-text="msg"></span>
  </div>
</div>
```

### 4.4 その他のマイクロインタラクション
| 要素 | 効果 |
|---|---|
| ロットカード hover | `translateY(-7px)` ＋影（`.28s`） |
| FAB hover | `translateY(-3px) rotate(90deg)`（`.3s`） |
| プライマリボタン hover | `translateY(-2px)` ＋影 |
| スライダーのステップ hover | `scale(1.12)`（`.15s`） |
| スライダー塗り | `transition: width .25s` |
| タイムラインカード hover | `translateY(-2px)` ＋影 |
| ダイアログ出現 | `animation: pop var(--dur-dialog) var(--ease-pop) both` |

---

## 5. CSSクラス設計（BEM）

> 命名規則：`block`、`block__element`、`block--modifier`。色・寸法は §1.4 トークンを参照。

### 5.1 アプリ・トップバー
```
.app
.app__topbar
.app__brand            .app__brand-logo   .app__brand-name
.app__screen           /* 画面切替コンテナ。fadeIn付与先 */
```

### 5.2 ロット一覧
```
.lot-list
.lot-list__header   .lot-list__title   .lot-list__count
.lot-list__grid
.lot-card
.lot-card__edit
.lot-card__id
.lot-card__crop
.lot-card__meta   .lot-card__meta-row   .lot-card__meta-label   .lot-card__meta-value
.lot-card__actions
.fab
```

### 5.3 ボタン（共通）
```
.btn
.btn--primary   .btn--outline   .btn--ghost   .btn--neutral   .btn--danger
.btn--sm
```

### 5.4 日報作成
```
.report-form
.back-link   .back-link__icon
.lot-banner   .lot-banner__id   .lot-banner__sub   .lot-banner__date   .lot-banner__date-label
.rating
.rating__head   .rating__title
.rating__track   .rating__fill
.rating__steps   .rating__step   .rating__step--on   .rating__step--selected
.rating__scale
.photos   .photos__head
.photo   .photo__remove   .photo__name
.photo-add   .photo-add__icon
.field   .field__label   .textarea   .char-count
.form-actions
```

### 5.5 日報閲覧
```
.report-view
.report-view__header   .report-header__id   .report-header__sub   .report-header__date
.sensor-grid
.sensor-card   .sensor-card__label   .sensor-card__value   .sensor-card__unit
.section-label
.worker-input
.rating-readout   .rating-readout__label   .rating-readout__dots   .rating-readout__value
.dot   .dot--filled
.ai-summary
.ai-summary__badge   .ai-summary__note
.ai-summary__text   .ai-summary__text--typing   .ai-summary__caret
.ai-loading   .ai-loading__spinner   .ai-loading__text   .ai-loading__dots
.report-timeline   .report-timeline__label
.timeline-card   .timeline-card--active
.timeline-card__date   .timeline-card__meta
.timeline-card__tag   .timeline-card__tag--active
```

### 5.6 ダイアログ・トースト
```
.modal   .modal__overlay
.lot-dialog
.lot-dialog__header   .lot-dialog__title   .lot-dialog__close
.lot-dialog__body
.field   .field__label   .field__hint
.input   .input--readonly
.lot-dialog__grid          /* 2カラム入力行 */
.lot-dialog__footer
.toast   .toast__icon
```

### 5.7 主要要素の参考CSS（抜粋）

```css
.app__screen{ animation:fadeIn var(--dur-screen) ease; }   /* §4.1の注意参照 */

.lot-card{
  position:relative; background:var(--c-surface);
  border:1px solid var(--c-border-card); border-radius:var(--r-card);
  padding:24px 22px 22px; box-shadow:var(--sh-card);
  transition:transform .28s, box-shadow .28s;
}
.lot-card:hover{ transform:translateY(-7px); box-shadow:var(--sh-card-hover); }
.lot-card__edit{ position:absolute; top:16px; right:16px; }
.lot-card__id{ font:800 24px/1 var(--font-display); margin-bottom:6px; }

.btn--primary{ border:none; background:var(--c-primary); color:#fff;
  font:700 13.5px var(--font-body); border-radius:var(--r-btn); cursor:pointer;
  transition:background .2s; }
.btn--primary:hover{ background:var(--c-primary-hover); }

.rating__step{ width:30px; height:30px; border-radius:50%;
  background:#fff; border:2px solid #e1ebdb; color:#b7c3b1;
  display:flex; align-items:center; justify-content:center;
  font:700 12px var(--font-body); cursor:pointer; transition:transform .15s; }
.rating__step--on{ background:#cfe6cb; border-color:#a8d3a2; color:var(--c-accent); }
.rating__step--selected{ background:var(--c-primary); border:3px solid var(--c-primary-hover); color:#fff; }
.rating__step:hover{ transform:scale(1.12); }

.toast{ position:absolute; left:50%; bottom:28px; transform:translateX(-50%);
  display:flex; align-items:center; gap:10px;
  background:var(--c-primary-deep); color:#fff; font:700 14px var(--font-body);
  padding:14px 26px; border-radius:14px; box-shadow:var(--sh-toast);
  white-space:nowrap; z-index:30;
  animation:toastIn var(--dur-toast) var(--ease-pop) both; }
```

---

## 6. データ構造（参考 / requirements.md より）

### Lots（`src/models/lot.py`）
| カラム | 型 | 備考 |
|---|---|---|
| id | String | 主キー（例 `DEMO_LOT1`） |
| farm_name | String | 農場名 |
| house_number | String | 棟番号 |
| crop_type | String | 栽培品目 |
| crop_variety | String? | 栽培品種（任意） |
| plant_count | Integer? | 定植本数（任意） |

### Reports（`src/models/report.py`）
| カラム | 型 | 備考 |
|---|---|---|
| id | String(ULID) | 主キー |
| lot_id | String | 外部キー → Lots.id |
| date | String | `YYYY-MM-DD` |
| plant_condition | Integer | 植物の状態 1〜5 |
| pest_condition | Integer | 病害虫の状況 1〜5 |
| photo_path | String? | 写真パス（最大3枚・カンマ区切り等） |
| comment | Text? | 200文字以内 |
| ai_summary | Text? | AIまとめ |
| created_at | DateTime | 作成日時 |

**デモロット初期データ**
| id | 農場 | 棟 | 品目 | 品種 | 本数 |
|---|---|---|---|---|---|
| DEMO_LOT1 | KAISHI農場 | 1号棟 | トマト | シンディー | 540 |
| DEMO_LOT2 | KAISHI農場 | 2号棟 | メロン | アールス | 320 |
| DEMO_LOT3 | KAISHI農場 | 3号棟 | トマト | フルティカ | 480 |

---

## 7. 実装チェックリスト

- [ ] デザイントークン（§1.4）を CSS 変数として定義
- [ ] Google Fonts（Zen Maru Gothic / M PLUS Rounded 1c）読み込み
- [ ] アプリシェル＋トップバーの共通レイアウト
- [ ] ロット一覧：カード（ID大表示・編集右上・アイコン/日付なし）＋FAB
- [ ] 日報作成：5段階スライダー・写真3枚・コメント200字・保存→一覧リダイレクト
- [ ] 日報閲覧：ID大表示・曜日なし・ステータス文言なし・日報タイムライン・戻るリンクのみ
- [ ] ダイアログ：新規/編集共通化・編集時IDは readonly（錠なし）・HTMXで `components/` から差込・Alpineで開閉
- [ ] アニメーション：画面フェードイン / AI要約タイピング / 完了トースト（3種メッセージ・2600ms）
- [ ] BEMクラス名（§5）で実装
