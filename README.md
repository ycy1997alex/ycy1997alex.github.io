# 尤俊硯 — 個人網站

**繁體中文** ｜ [English](README.en.md)

個人網站的原始碼，網站為中英雙語，線上位置：**<https://ycy1997alex.github.io>**。

以 [Hugo](https://gohugo.io/) 搭配 [hugo-coder](https://github.com/luizdepra/hugo-coder)
主題建置，透過 GitHub Actions 自動部署到 GitHub Pages。

## 網站內容

- **關於（About）** — 個人背景、學歷、專長與著作
- **專案（Projects）** — 研究與工程專案
- **部落格（Blog）** — 文章與互動工具
- **聯絡資訊（Contact）**

所有頁面皆提供**繁體中文**與**英文**，可從導覽列切換語言。

## 技術架構

| | |
|---|---|
| 靜態網站產生器 | Hugo（extended） |
| 主題 | hugo-coder |
| 主機 | GitHub Pages |
| 部署 | GitHub Actions — push 到 `main` 自動建置 |
| 網站分析 | Google Analytics 4 |

本 repo 存放的是 Hugo **原始碼**（Markdown 內容 + 主題）。發布用的 HTML 由 Hugo
在部署時產生、並由 GitHub Pages 提供，不會 commit 進本 repo。

## 致謝

主題：[hugo-coder](https://github.com/luizdepra/hugo-coder)，作者 Luiz de Prá，
採 MIT 授權。
