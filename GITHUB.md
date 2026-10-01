# GitHub 上傳與 GitHub Pages／Actions 指令

本專案遠端儲存庫：

```text
https://github.com/vicabon/BankDeposit.git
```

以下指令請在專案根目錄執行：

```bash
cd /home/vwei/workspace/agy/BankDeposit
```

## 一、第一次將目前資料夾連結到 GitHub

若目前資料夾尚未是 Git repository，執行：

```bash
git init
git branch -M main
git remote add origin https://github.com/vicabon/BankDeposit.git
```

若已存在 `origin`，不要重複 `git remote add`，改用：

```bash
git remote set-url origin https://github.com/vicabon/BankDeposit.git
```

確認遠端設定：

```bash
git remote -v
git branch --show-current
```

## 二、上傳本次實作檔案

```bash
git status --short
git diff -- README.md PLAN.html GITHUB.md
git add README.md PLAN.html GITHUB.md
git add src data site scripts docs .github
git status
git diff --cached --stat
git diff --cached --check
git commit -m "建立新台幣定存資料更新與 GitHub Pages 架構"
```

## 三、推送到 GitHub

第一次推送 `main` 分支：

```bash
git push -u origin main
```

之後每次有新的 commit：

```bash
git push
```

推送前確認遠端狀態：

```bash
git fetch origin
git status
git log --oneline --decorate -5
```

## 四、GitHub 驗證方式

若使用 HTTPS，GitHub 不接受帳號密碼作為 Git 驗證；需要使用 Personal Access Token（PAT）或 Git Credential Manager。不要把 Token 寫入程式、HTML、README、Actions workflow 或 commit。

若本機已安裝 GitHub CLI，可先登入：

```bash
gh auth login
gh auth status
gh repo view vicabon/BankDeposit
```

## 五、GitHub Actions 手動執行

推送 `.github/workflows/update-data.yml` 後，可用 GitHub CLI 手動觸發：

```bash
gh workflow list --repo vicabon/BankDeposit
gh workflow run "更新新台幣定存資料網站" --repo vicabon/BankDeposit
```

只驗證、不部署 Pages：

```bash
gh workflow run "更新新台幣定存資料網站" \
  --repo vicabon/BankDeposit \
  -f dry_run=true
```

查看最近執行結果：

```bash
gh run list --repo vicabon/BankDeposit --workflow update-data.yml
gh run view RUN_ID --repo vicabon/BankDeposit
```

將 `RUN_ID` 替換為實際執行編號。

## 六、GitHub Pages 設定

在 GitHub 網頁操作：

```text
Repository → Settings → Pages → Build and deployment → Source → GitHub Actions
```

確認 Pages 部署狀態：

```bash
gh api repos/vicabon/BankDeposit/pages
gh api repos/vicabon/BankDeposit/deployments
```

## 七、建議的日常更新流程

```bash
git status --short
git add README.md PLAN.html GITHUB.md
git add src data site scripts docs .github
git diff --cached --check
git commit -m "描述本次變更"
git push origin main
gh run list --repo vicabon/BankDeposit --limit 5
```

## 八、發生推送衝突時

```bash
git fetch origin
git status
git log --oneline --decorate --graph --all -10
git pull --rebase origin main
```

解決衝突後：

```bash
git status
git add CONFLICTED_FILE
git rebase --continue
git push origin main
```

不要在未確認內容前使用 `git push --force`。若確實需要改寫遠端歷史，優先使用：

```bash
git push --force-with-lease origin main
```

## 九、上傳前安全檢查

```bash
git diff --cached --check
git status --short
git ls-files | sort
```

確認沒有加入：

- GitHub Token、Personal Access Token 或其他密鑰
- `.env`、瀏覽器 Cookie、登入資訊
- 銀行帳號、個人資料或私人 API 金鑰
- Python 快取、虛擬環境與暫存檔

## 十、目前專案的資料限制

目前 workflow 會驗證並部署現有靜態資料，但尚未擷取五家銀行官方網站，也尚未填入任何利率、額度、活動期間或官方方案網址。空白資料不得解讀為「目前沒有方案」。

實際更新方式與限制請參閱：

- [README.md](README.md)
- [PLAN.html](PLAN.html)
- [docs/USAGE.md](docs/USAGE.md)
