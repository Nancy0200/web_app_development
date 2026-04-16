# API 與路由設計 - 線上算命系統

根據架構與 UI 流程規劃，本專案將後端路由拆分為幾個主要的模組。所有的網頁渲染均透過 Jinja2 處理。

## 1. 路由總覽表

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁** | GET | `/` | `index.html` | 網站首頁，顯示進入算命或占卜的選項 |
| **歷史紀錄** | GET | `/history` | `history.html` | 從 Session 取得所有算命與占卜歷史列表並顯示 |
| **算命(八字)** | GET | `/bazi` | `bazi/form.html` | 顯示生辰資料表單 |
| **算命(八字)** | POST | `/bazi/calculate` | — | 接收表單資料，計算八字，儲存紀錄，重導向至結果頁 |
| **算命(八字)** | GET | `/bazi/result/<id>`| `bazi/result.html` | 取得單筆算命結果並渲染頁面 |
| **占卜(抽籤)** | GET | `/divination` | `divination/draw.html` | 顯示心中默念對象的占卜頁面 |
| **占卜(抽籤)** | POST | `/divination/draw` | — | 接收疑惑，抽籤並儲存，重導向至結果頁 |
| **占卜(抽籤)** | GET | `/divination/result/<id>` | `divination/result.html` | 取得單筆占卜測算紀錄並渲染頁面 |

---

## 2. 每個路由詳細說明

### `main.py` (共用與主要頁面)

1. **`GET /` (首頁)**
   - 輸入：無
   - 處理邏輯：渲染系統首頁。
   - 輸出：`index.html`

2. **`GET /history` (歷史紀錄)**
   - 輸入：無（從 cookie 的 `session` 中取得 session_id）
   - 處理邏輯：呼叫 `BaziHistory.get_all_by_session` 與 `DivinationHistory.get_all_by_session`，組合列表。
   - 輸出：`history.html`

### `bazi.py` (八字算命模組)

1. **`GET /bazi`**
   - 處理邏輯：渲染填表頁面。
   - 輸出：`bazi/form.html`

2. **`POST /bazi/calculate`**
   - 輸入：表單欄位 (`birth_year`, `birth_month`, `birth_day`, `birth_time`, `gender`)
   - 處理邏輯：
     1. 確保或產生 `session_id`。
     2. 驗證資料是否合法。
     3. 呼叫八字運算模型進行排盤。
     4. 呼叫 `BaziHistory.create` 將結果存入 SQLite。
   - 輸出：成功後重導向至 `GET /bazi/result/<id>`。

3. **`GET /bazi/result/<id>`**
   - 輸入：URL 參數 `id`
   - 處理邏輯：檢查紀錄是否存在，如果有，透過 `BaziHistory.get_by_id(id)` 撈出資料反序列化。
   - 輸出：`bazi/result.html` 或遇到 404 回傳錯誤頁面。

### `divination.py` (占卜測算模組)

1. **`GET /divination`**
   - 處理邏輯：渲染抽籤介面。
   - 輸出：`divination/draw.html`

2. **`POST /divination/draw`**
   - 輸入：表單欄位 (`question`)
   - 處理邏輯：
     1. 確保或產生 `session_id`。
     2. 呼叫隨機抽籤演算法。
     3. 呼叫 `DivinationHistory.create` 存入 SQLite。
   - 輸出：重導向至 `GET /divination/result/<id>`。

3. **`GET /divination/result/<id>`**
   - 輸入：URL 參數 `id`
   - 處理邏輯：透過 `DivinationHistory.get_by_id(id)` 撈出籤詩結果。
   - 輸出：`divination/result.html`

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 中：
- `base.html`：**(共用版型)** 包含 `<head>`、Navbar、Footer 等共用元件。
- `index.html`：**(繼承 base.html)** 主要落地頁面。
- `history.html`：**(繼承 base.html)** 列出過往測算的卡片清單。
- `bazi/`
  - `form.html`：**(繼承 base.html)** 八字資料輸入頁面。
  - `result.html`：**(繼承 base.html)** 詳盡展現命盤的頁面。
- `divination/`
  - `draw.html`：**(繼承 base.html)** 充滿神秘感，允許使用者輸入問題跟點擊籤筒的頁面。
  - `result.html`：**(繼承 base.html)** 籤詩解析與吉凶說明。
