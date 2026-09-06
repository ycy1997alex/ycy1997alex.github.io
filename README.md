# 尤俊硯 — 個人網站

**繁體中文** ｜ [English](README.en.md)

個人網站的原始碼，網站為中英雙語，線上位置：**<https://ycy1997alex.github.io>**。

以 [Hugo](https://gohugo.io/) 搭配 [hugo-coder](https://github.com/luizdepra/hugo-coder)
主題建置，透過 GitHub Actions 自動部署到 GitHub Pages。

## 網站內容

- **關於（About）** — 履歷：個人背景、工作經歷、學歷、專長、著作與聯絡方式
- **專案（Projects）** — 個人、工作與學術專案
- **技術貼文（Technical-Posts）** — 技術文章
- **日常貼文（Casual-Posts）** — 旅遊、清單等日常文章與互動工具
- **分析（Analysis）** — 分析相關的儲存庫

導覽列可切換**繁體中文**與**英文**。關於、專案、分析與部分貼文兩種語言都有；
少數以中文寫成的貼文尚未翻譯，英文版頁首會標示 “This post is in Traditional
Chinese Only”。

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

## 互動示範頁

文章用到的密碼保護示範頁已移到
[ycy1997alex-oss-projects](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/demo)
集中管理。本 repo 的 `static/demo/` 只留轉址頁，讓已發布文章裡的舊網址繼續有效。

## 授權

內容與程式碼分開授權，詳見 [LICENSE](LICENSE)：內容採 CC BY-NC 4.0，
建站程式碼採 MIT，人像照片保留所有權利。

## 致謝

主題：[hugo-coder](https://github.com/luizdepra/hugo-coder)，作者 Luiz de Prá，
採 MIT 授權。
