# 資本島：商戰人生（Bizwar Island）

![Bizwar Island](https://img.shields.io/badge/版本-v1.0.0-00d4aa)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-純前端靜態-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

**資本島：商戰人生**（Bizwar Island）是一款免費的線上台灣商戰模擬遊戲：純前端、單一 HTML 檔、免下載、免註冊、手機與電腦瀏覽器都能玩。

## 遊戲簡介

你創立一家公司，從夜市擺攤、科技新創或家族企業出發，逐年經歷融資、併購、上市、公關危機與股權爭奪——體驗充滿台灣味與時事梗的完整企業生涯。

| 特色 | 說明 |
| --- | --- |
| 種子化 RNG | 輸入任意種子碼即可重現同一場企業生涯 |
| 9 大經營階段 | 籌備期 → 夜市/天使 → 種子 → A/B/C 輪 → 上市 → 併購/壟斷 → 退休 |
| 8 大企業能力 | 產品、行銷、銷售、財務、管理、人脈、抗壓、遠見 |
| 100+ 商戰事件 | 融資、併購、股權爭奪、公關危機、台灣時事梗 |
| 雙軌目標 | 志向 × 成就，累計解鎖 50 項成就 |
| 結算評級 | 從 D 到 SSS 的企業生涯結算與 PNG 分享圖 |

## 檔案結構

| 檔案 | 說明 |
| --- | --- |
| `index.html` | 遊戲主程式（HTML + CSS + JS 單一檔案，約 1,500 行） |
| `news.html` | 更新公告頁面 |
| `robots.txt` / `sitemap.xml` | SEO 基礎檔案 |

## 本地開發

不需要任何建構工具，直接以任意靜態伺服器開啟 `index.html` 即可：

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```

然後用瀏覽器開啟 `http://localhost:8080/index.html`。

## 部署（GitHub Pages）

1. 開啟本儲存庫的 **Settings → Pages**
2. **Source** 選擇 `Deploy from a branch`（或留空，因為本 repo 僅含靜態檔案）
3. **Branch** 選擇 `main`、路徑 `/ (root)`，按 Save
4. 約 1–2 分鐘後即可透過 `https://{你的帳號}.github.io/Bizwar-Island/` 遊玩

> 注意：Manus 的 GitHub 整合 token 沒有 Pages / Actions 權限，啟用 Pages 需在 GitHub 介面上手動操作一次（30 秒）。

## 靈感來源

本遊戲靈感來自 [yakyulife 棒球人生模擬器](https://github.com/kai890707/Life-TW)，在其架構與玩法基礎上重製為商戰主題。所有事件純屬虛構娛樂，真實人物與品牌均以改編化名呈現。

## License

MIT
