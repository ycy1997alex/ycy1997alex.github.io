# Case A：Hugo + hugo-coder（復刻現有外觀）

以 Hugo 重建的網站「原始專案」。theme 沿用線上網站現在使用的
[hugo-coder](https://github.com/luizdepra/hugo-coder)，因此外觀與現有網站幾乎相同，
且所有舊網址（`/posts/travel-checklist/`、`/zh-tw/about/` 等）在新站都有對應頁面。

## 本機預覽

```powershell
cd Case_A
..\_tools\hugo.exe server
# 瀏覽 http://localhost:1313/
```

正式建置（輸出到 `public/`，不進版控）：

```powershell
..\_tools\hugo.exe --gc --minify
```

## 目錄結構

```text
Case_A/
├── hugo.toml                  # 全站設定：標題、選單、社群連結、GA4、雙語
├── content/                   # ★ 內容都在這裡，發文只動這個資料夾
│   ├── about.md               # 英文版（網址 /about/）
│   ├── about.zh-tw.md         # 中文版（網址 /zh-tw/about/），檔名加 .zh-tw 即成對翻譯
│   ├── contact.md / projects.md（同上規則）
│   └── posts/
│       ├── first-post.md / first-post.zh-tw.md
│       ├── how-to-build-hugo-pages.zh-tw.md   # 只有中文版 → 只出現在中文站
│       ├── travel-checklist.md / .zh-tw.md    # 互動頁：內容只有一行 shortcode
│       ├── call-up-list.md / .zh-tw.md
│       └── 2026-tokyo-drive.md / .zh-tw.md
├── assets/fragments/          # ★ 互動 Web App 的 HTML+CSS+JS（單一原始檔，雙語共用）
│   ├── travel-checklist.html
│   ├── call-up-list.html
│   └── 2026-tokyo-drive.html
├── layouts/shortcodes/webapp.html   # webapp shortcode 的實作
├── static/images/             # 大頭貼、favicon（會原樣複製到網站根目錄）
├── themes/hugo-coder/         # theme（純複製，見下方「更新 theme」）
└── .github/workflows/hugo.yml # GitHub Actions 自動部署（正式採用時搬到 repo 根目錄）
```

## 發新文

### 一般文章（Markdown）

新增 `content/posts/我的文章.md`：

```markdown
---
title: "文章標題"
date: 2026-07-04
authors: ["Alex Yu"]        # 中文版用 ["尤俊硯"]
tags: ["標籤1", "標籤2"]
---

內文直接寫 Markdown。
```

存檔即完成。列表頁、RSS、sitemap、tags 全部自動更新。
要有中文版就再加一個 `我的文章.zh-tw.md`；只想發某一種語言就只放那一個檔。

### 互動 Web App 型貼文（像東京自駕、checklist）

1. 把整頁互動內容（HTML + `<style>` + `<script>`）存成 `assets/fragments/新頁面.html`
   （不含 `<html>`、`<head>`、`<body>` 外殼，也不用放導覽列與 footer，theme 會包好）
2. 新增 `content/posts/新頁面.md`，內文只需要一行：

```markdown
---
title: "頁面標題"
date: 2026-07-04
summary: "一句話描述"       # 沒有這行的話，列表卡片摘要會抓到 App 的原始文字
description: "一句話描述"
---

{{< webapp "新頁面.html" >}}
```

fragment 只有一份，en 與 zh-tw 兩個 .md 可以共用它。

## 正式採用的步驟

1. 先備份現狀：`git branch legacy-static`（舊的靜態輸出永遠找得回來）
2. 把 `Case_A/` 的內容移到 repo 根目錄（並刪除根目錄的舊 generated HTML）
3. 把 `.github/workflows/hugo.yml` 放到 repo 的 `.github/workflows/`
4. 到 GitHub repo → Settings → Pages → Build and deployment → Source 改成 **GitHub Actions**
5. push 之後 Actions 會自動建置與發布，之後發文只要 push Markdown

## 更新 theme

目前 `themes/hugo-coder/` 是純複製（沒有 .git）。要更新時：

```powershell
# 於 repo 根目錄
Remove-Item -Recurse -Force themes/hugo-coder
git clone --depth 1 https://github.com/luizdepra/hugo-coder themes/hugo-coder
Remove-Item -Recurse -Force themes/hugo-coder/.git
```

（正式採用後也可改成 git submodule 管理，但純複製最不容易出錯。）

## 相較舊站已修正的問題

- GA4 追蹤碼只注入一次（舊站 head/body 重複兩份）
- favicon / apple-touch-icon 補齊（舊站全是 404）
- 中文站補上兩個 checklist 頁（舊站只掛在英文樹）
- footer 年份自動產生（舊站 2023/2026 不一致）
- theme 範例殘留的 demo/測試 分類仍在（來自 first-post 的 front matter，
  想拿掉就編輯 `content/posts/first-post*.md` 刪掉 categories/series 兩行）
