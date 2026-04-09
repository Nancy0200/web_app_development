# 系統與使用者流程圖 - 線上算命系統

本文件根據 PRD 與系統架構文件，視覺化使用者在「線上算命系統」中的操作路徑與系統內部的資料流動。

## 1. 使用者流程圖（User Flow）

以下圖表展示使用者從進入網站開始，如何操作各項主要功能（生成八字、算命、占卜、歷史紀錄檢視、分享）。

```mermaid
flowchart LR
    A([進入網站首頁]) --> B{選擇服務項目}
    
    %% 八字與算命流程
    B -->|算命/八字排盤| C[填寫出生資料表單]
    C --> D[提交表單資料]
    D --> E[顯示生辰八字與命格解析結果]
    E -->|回首頁| B
    E -->|分享| F[產生分享連結或卡片]
    
    %% 占卜流程
    B -->|線上占卜| G[進入占卜頁面]
    G --> H[心中默想疑惑並點擊抽籤]
    H --> I[顯示籤詩與解惑指引]
    I -->|回首頁| B
    I -->|分享| F
    
    %% 歷史紀錄流程
    B -->|檢視歷史紀錄| J[進入歷史紀錄頁面]
    J --> K[瀏覽儲存的算命/占卜紀錄列表]
    K --> |點擊單筆紀錄| E
    K --> |點擊單筆紀錄| I
```

## 2. 系統序列圖（Sequence Diagram）

以下圖表描述「使用者提交出生日期進行算命」到「系統產生結果並記錄」的完整系統互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask 路由
    participant Model as 領域模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫出生年/月/日/時並送出
    Browser->>Flask: POST /calculate (提交資料)
    
    Flask->>Model: 呼叫八字運算與命理解析邏輯
    Note over Model: 執行核心算命演算法
    
    Model->>DB: INSERT INTO history (結合 session 儲存算命紀錄)
    DB-->>Model: 儲存成功並回傳紀錄 ID
    
    Model-->>Flask: 回傳計算結果與紀錄 ID
    
    Flask->>Browser: 重新導向至 GET /result/{id} 渲染畫面
    Browser-->>User: 呈現算命結果頁面
```

## 3. 功能清單對照表

下表列出系統各主要功能、預期的對應 URL 路徑及其 HTTP 操作方法：

| 功能模組 | 功能描述 | URL 路徑 | HTTP 方法 |
| --- | --- | --- | --- |
| **首頁** | 進入系統的第一個頁面，展示服務選項 | `/` | GET |
| **算命服務** | 提交使用者的出生時間進行計算 | `/calculate` | POST |
| **算命服務** | 顯示與呈現八字/算命分析結果 | `/result/<id>` | GET |
| **占卜服務** | 進入抽籤/占卜頁面 | `/divination` | GET |
| **占卜服務** | 執行抽籤邏輯並產生結果 | `/divination/draw` | POST |
| **占卜服務** | 顯示與呈現籤詩/占卜回答 | `/divination/<id>` | GET |
| **歷史紀錄** | 列出當前 Session 保存的測算紀錄 | `/history` | GET |
| **分享功能** | 公開檢視特定結果 (與查看本人結果共用) | `/share/<type>/<id>` | GET |
