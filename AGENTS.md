# AGENTS.md

給 coding agent 的專案說明。本 repo 是雙語（en / zh-tw）Hugo 網站，使用 vendored 的 `hugo-coder` 主題，部署到 GitHub Pages。Claude Code 透過 `CLAUDE.md` 裡的 `@AGENTS.md` 匯入讀取本檔。

## 建置與執行

- Hugo extended v0.163.3（版本鎖定在 `.github/workflows/hugo.yml`）。
- 本機預覽：`hugo server`
- 正式建置（與 CI 相同）：`$env:HUGO_ENVIRONMENT='production'; hugo --gc --minify`。CI 另外用 `--baseURL` 帶入 Pages 網址，但它和 `hugo.toml` 的 `baseURL` 相同，本機不必加。
- 驗證變更時不要動到 `public/`：用 `hugo -d <dir>` 建置到暫存目錄（Claude Code 用 scratchpad），再檢查或 diff 輸出的 HTML。
- 部署：push 到 `main`，GitHub Actions 會建置並發布。`public/` 與 `resources/` 不進版控。

## 雙語內容

每個頁面都是一組兩個檔案：`<name>.md`（英文，預設語言）與 `<name>.zh-tw.md`（繁體中文）。新增或修改頁面時，兩個語言版本都要處理。

## 互動頁 fragment（`{{< webapp >}}`）

- `layouts/shortcodes/webapp.html` 會把 `assets/fragments/<file>` 原封不動嵌進文章頁，所以 fragment 沒有 `<html>` / `<head>`，只有 `<style>`、markup 與 `<script>`。
- 有的 fragment 由兩種語言共用一個檔案（如 `2026-jeju.html`），有的分成 `<name>.html`（中文）與 `<name>.en.html`（英文）。
- `2026-jeju.html` 與 `2026-setouchi.html` 是產生出來的檔案，來源分別是 `tools/make_jeju_fragment.py` 與 `tools/make_setouchi_fragment.py`（只用標準函式庫，執行 `python tools/<script>.py`）。要修改時改腳本再重新產生；直接改 HTML，下次產生時就會被覆蓋。其餘 fragment 是手寫的。
- 寫 fragment 樣式的兩個前提：主題把 `html` 設成 `font-size: 62.5%`，所以 `1rem = 10px`；深色模式由主題掛在 `body` 上的 `.colorscheme-dark` 控制，不是 `prefers-color-scheme`。

## 社群分享圖（og:image / twitter:image）

名片卡 `static/images/og-card.jpg` 只在分享首頁或 About 頁時出現。它由 `tools/make_og_card.py` 產生，這支腳本需要 Pillow，字型直接讀 `C:\Windows\Fonts`，所以只能在 Windows 上執行。

- 不要在 `hugo.toml` 的 `[params]` 底下設 `images`。Hugo 內建的 `opengraph.html` / `twitter_cards.html` 在頁面沒有自己的圖時會退回 `site.Params.images`，設了就會讓每篇文章都顯示名片卡。
- 名片卡逐頁寫在 front matter（`images: ["images/og-card.jpg"]`），而且只寫在這四個檔案：`content/_index.md`、`content/_index.zh-tw.md`（首頁）、`content/about.md`、`content/about.zh-tw.md`。`_index.md` 這兩個檔只有 front matter（這張圖，加上從 About 頁複製過來的首頁 `description`）；首頁版型不會讀它們的內文。
- 文章預設不出圖（`twitter:card` 退回 `summary`）。要給文章代表圖，就把圖放進 `static/images/`，並在兩個語言版本的 front matter 都加上 `images: ["images/<file>"]`。文章絕對不要用 `og-card.jpg`。
- 修改後的驗證：重新建置一次，應該只有上述四頁含有 `<meta ... og:image>` 標籤。grep 時要搜 meta 標籤，不能只搜 `og:image` 字串，因為 `how-to-build-hugo-pages` 的內文提到了這個字。
