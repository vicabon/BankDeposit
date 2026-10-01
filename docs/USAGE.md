# 第一階段使用說明

目前建立的是不抓取銀行網站的基礎架構。`data/latest.json` 與 `site/latest.json` 只包含五家指定銀行的空白狀態，不含利率、額度、活動或官方網址。

## 本機檢查

在專案根目錄執行：

```bash
PYTHONPATH=src python -m qgenie_deposit data/latest.json
python -m http.server 8000 --directory site
```

瀏覽 `http://localhost:8000/` 可查看靜態頁面。直接以 `file://` 開啟時，瀏覽器可能阻擋 JavaScript 讀取 JSON，因此建議使用 HTTP 伺服器。

## 資料限制

- GitHub Pages 頁面只讀取已發布的 `latest.json`，開啟頁面或按「重新載入資料」不會搜尋銀行網站。
- GitHub Actions 目前只有驗證骨架，不會抓取、解析或交叉驗證銀行資料。
- 空的方案清單代表「尚未取得資料」，不代表「目前沒有方案」。
- 只有完成官方資料校對、確認新台幣定存、非新客／新開戶限定且今日可承作的方案，才可加入主要結果。
- 官方未載明的欄位必須保留「官方資料未載明」，不得自行補值。

## GitHub Actions 手動／定時更新

`.github/workflows/update-data.yml` 已提供兩種觸發方式：

- 每日 08:30 台灣時間左右自動執行（GitHub Actions 排程可能延遲）。
- 在 GitHub Actions 頁面選擇「更新新台幣定存資料網站」後按 `Run workflow` 手動執行。
- 手動執行時可勾選 `dry_run`，只驗證資料，不部署 GitHub Pages。

目前更新流程會驗證 `data/latest.json`、同步至 `site/latest.json`、建立 `site/update-status.json`，再以 Pages artifact 部署；尚未擷取銀行官方網站，因此不會產生新的銀行方案資料。

若要啟用部署，儲存庫需在 GitHub Pages 設定中選擇 GitHub Actions 作為來源。公開網站訪客不能直接用此工作流程執行 Python；手動執行需要儲存庫相應權限。

## 後續實作前置條件

後續加入銀行資料擷取前，應先建立官方來源清單、證據摘錄、來源版本、失敗狀態與人工複核流程；本階段不會假設任何銀行網站的 HTML 結構或可抓取性。
