---
title: "如何建立Hugo靜態網頁"
date: 2023-07-23
lastmod: 2026-08-31
authors: ["Alex Yu"]
series: ["Web"]
tags: ["hugo", "Github Pages", "個人網頁", "靜態網頁", "部落格"]
summary: "這個網站從選主題到上線的完整過程，以及 2026 年用 Claude 重寫的那一輪。"
description: "這個網站從選主題到上線的完整過程，以及 2026 年用 Claude 重寫的那一輪。"
# 這篇原本在 /posts/ 底下，搬到新 section 後留一個轉址頁給舊連結
aliases: ["/posts/how-to-build-hugo-pages/"]
---

> **This post is in Traditional Chinese Only.**

> 這篇是大綱，內容之後會再補完整。

建這個網站的過程其實比想像中簡單，大致分成五個階段。

## 1. 選一個 Hugo 主題

Hugo 官方的 [Themes](https://themes.gohugo.io/) 頁面可以直接預覽。這個網站用的是
[hugo-coder](https://github.com/luizdepra/hugo-coder)，理由是版面乾淨、內建深色模式，
而且原生支援多語系。

## 2. 照模板填入自己的內容後佈署

主題本身已經把版型做完了，實際要動的只有 `hugo.toml` 的設定與 `content/` 底下的
Markdown。寫完之後推上 GitHub，由 GitHub Actions 建置並發布到 GitHub Pages。

## 3. 申請 Google 收錄

網站上線不等於搜尋得到。要到 Google Search Console 驗證網域所有權，
把 sitemap 提交上去，Google 才會開始爬。

## 4. 設定 SEO

包含中英雙語的 hreflang 標記、每頁的 description 與 og:image、
sitemap 分語言輸出，還有 Google Analytics 4 的流量追蹤。

## 5. 2026 年重新以 Claude 改寫

隔了兩年回頭看，內容與結構都有不少該修的地方。這一輪用 Claude 做了一次完整的
健檢與重寫，也順手補上了幾個互動頁面。
