---
title: "Day 23｜Claude 幫我把個人網頁更新了，順便把履歷照片藏在刮刮樂底下"
date: 2026-09-06T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
summary: "重整個人網站的導覽與履歷，加上刮開才看得到的照片，並說明 hugo.toml 的設定與部署流程。"
description: "重整個人網站的導覽與履歷，加上刮開才看得到的照片，並說明 hugo.toml 的設定與部署流程。"
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10408212)。

> 本篇階段：Prj#4 個人網頁

> 使用介面：Claude Code（via VS Code）

---

## 前情

[Day 20](https://ithelp.ithome.com.tw/articles/10407372) 讓 Claude Code 把個人網站從頭檢查一次，拿回十二項問題；[Day 21](https://ithelp.ithome.com.tw/articles/10407692) 跟 [Day 22](https://ithelp.ithome.com.tw/articles/10407930) 則是把 Word 與 Excel 裡的清單和行程搬進網站，變成可以打勾、可以點地圖的頁面。三天下來內容多了不少，架子卻還是 2023 年那個。

導覽列四格，「貼文」底下混著旅遊行程、教召清單，還有一篇談這個網站怎麼架的技術文；「聯絡」點進去只有三行連結加一張照片。今天處理架子本身，順便把擺著三年沒動的履歷更新掉。

---

## 1. 舊版那四格

先看舊版長什麼樣子。視窗不夠寬的時候，導覽列會收成右上角那三條線：

![舊版首頁，中文、亮色主題，選單收成漢堡](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-Old-UI/old-home-zh-light-collapsed.png)

拉寬之後展開，四格是「關於、貼文、專案、聯絡」，最右邊是語言切換：

![舊版首頁，選單展開後的四格](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-Old-UI/old-home-zh-light.png)

英文版同一套骨架，暗色主題下是 About / Blog / Projects / Contact：

![舊版首頁，英文、暗色主題](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-Old-UI/old-home-en-dark.png)

窗一窄，英文暗色版一樣收成漢堡：

![舊版首頁，英文、暗色主題，選單收成漢堡](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-Old-UI/old-home-en-dark-collapsed.png)

問題不在格數，在分類跟內容對不起來。

「貼文」底下當時有五組雙語檔案：2026 瀨戶內海五日跟團遊、教召攜帶物品推薦清單、教召攜帶物品清單、旅遊確認清單、2026 東京近郊自駕，再加一篇談 Hugo 建站過程的文章跟一篇 first-post。旅遊跟教召是生活紀錄，Hugo 那篇是技術筆記，兩種東西的讀者根本不是同一批人。有人從 LinkedIn 點進來想看我做過什麼，結果第一眼是行李清單。

「聯絡」更尷尬。整頁只有 Email、LinkedIn、GitHub 三個連結加一張大頭照，等於為了三行字開一個頁面，而這三行字本來就該長在履歷上。

---

## 2. 新的五格導覽

改完之後是五格，順序由左而右：關於、專案、技術貼文、日常貼文、分析。中文版：

![新版首頁，中文、亮色主題，五格選單在同一行](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-New-UI/new-home-zh-light.png)

英文版，暗色主題，五格是 About / Projects / Tech-Posts / Casual-Posts / Analysis：

![新版首頁，英文、暗色主題，五格選單在同一行](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-New-UI/new-home-en-dark.png)

### 五個入口各裝什麼

「關於」現在就是完整履歷。頁面最上面是一張名片區塊：照片、姓名、應徵職務、所在地、三個聯絡連結，加三個標籤。往下依序是個人簡介、工作經驗、學歷、專業技能、專案經驗、研討會論文、證照與獲獎、學生社團經驗，中文版最後多一段自傳。舊版的「聯絡」整頁併進這張名片，順便在首頁社群圖示那排補了一顆信箱。

「專案」重新分成個人專案、工作專案、學術專案三塊，頁面頂端有一行錨點可以直接跳。這樣分的理由很現實：招募方要看的是工作專案，同行想看的多半是個人專案，混在一起誰都得自己找。

「技術貼文」跟「日常貼文」是原本那格「貼文」拆開的結果。技術貼文放建站、工具、工作流程；日常貼文放旅遊行程、攜帶物品清單那些。

「分析」是新開的一格，目前放三個外部儲存庫的連結：dotclaude、shioaji-usage，還有一個總體經濟分析的位置先留著。這格會是明天之後的主戰場。

---

## 3. 履歷更新

### 3.1 舊版停在 2023 年

舊版的「關於」開頭是三句話：曾任某公司研發工程師、陽明交大腦科所碩士、成大航太雙主修心理。工作經驗只有一段 2022 到 2023 年的，之後都沒寫。

### 3.2 改成八個區塊

新版工作經驗補到四段，履歷最上面的名片區塊長這樣，照片預設是蓋住的：

![新版履歷頁的名片區塊，照片被銀色刮刮遮罩蓋住](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-New-UI/new-about-card-covered.png)

---

## 4. 刮開才看得到的照片

履歷頁上那張照片，預設是蓋住的，要用滑鼠或手指刮開。

### 4.1 參考的原作，以及不能照抄的地方

起點是網路上一個叫「電腦版刮刮履歷」的作品。機制只有三個零件：兩張疊在一起的 canvas，上層畫 `before.jpg`、下層畫 `after.jpg`，然後在 `mousemove` 的時候用 `clearRect` 在上層挖一個 50×50 的洞。三十行做完一個效果，想法很乾淨。

問題全在細節。畫布寫死 3000×5000，一千五百萬像素，單層 RGBA 就要 57 MiB，兩層一百多 MiB；標題寫「電腦版」，大概就是知道這件事。事件只吃滑鼠，手機完全刮不動。`clearRect` 挖的是離散方塊，滑快一點兩次事件之間會留一段沒刮到，刮痕變虛線。`mouseup` 綁在畫布上，拖到畫布外放開就收不到，回來變成不用按也能刮。

最根本的是履歷本身是圖片。文字被壓成 jpg 之後不能選取、搜尋引擎讀不到、螢幕閱讀器讀不到、縮放會糊，雙語站還得維護兩套圖。我的履歷在 `content/about.md` 跟 `content/about.zh-tw.md` 裡，是 Markdown，走圖片這條路等於倒退回「要開設計軟體才能改一個字」。

### 4.2 我的版本：只蓋照片，不蓋履歷

結論是把範圍縮到最小：被蓋住的只有那張照片，履歷本文完全不動，還是 Markdown。

做成一個 Hugo shortcode，放在 `layouts/shortcodes/scratch-photo.html`，在 about.md 裡這樣叫：

```
{{</* scratch-photo
  src="/images/尤俊硯大頭貼-24.jpg"
  alt="尤俊硯 Alex Yu"
  w="402" h="555"
  width="240px"
  hint="刮開看照片"
  reveal="直接顯示照片" */>}}
```

輸出的 HTML 就是一個 `<img>`。遮罩那層 canvas 是 JS 跑起來之後才建立的，所以 JS 掛掉或被擋，看到的直接就是照片，不會變成一個空白的框。作業系統設了「減少動態」的話也一樣不蓋，底下藏的就是這張，一張再普通不過的畢業照：

![減少動態或沒有 JS 時，履歷頁直接顯示照片本身](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day23_20260906/Personal-Website-New-UI/new-about-card-revealed.png)

從原作那邊學到的坑，逐條處理掉：

畫布尺寸跟著容器走，乘上 `devicePixelRatio`，遮罩上那行提示字在高 DPI 螢幕才不會糊。遮罩不用圖片，用 `fillRect` 鋪底色再疊一道斜向漸層當銀漆，順便讀 body 上的主題 class 決定亮暗兩套顏色，切換主題時會重畫。筆刷改成圓頭線段，每次 `pointermove` 都從上一個點連過來，不留空隙。事件全部換成 Pointer Events，一套涵蓋滑鼠、觸控與手寫筆；按下去的時候 `setPointerCapture`，拖到畫布外放開也收得回來。

刮開的比例會算，超過一半就自動全開。`getImageData` 很貴，所以做了兩件事：最多每 250 毫秒算一次，而且每 64 個像素才抽一個 alpha 來看。旁邊固定放一顆「直接顯示照片」的按鈕，不想玩的一按就好；列印或存 PDF 的時候遮罩用 CSS 藏掉，拿到的一定是照片本身。

還有一個是重畫遮罩會把刮痕洗掉。解法是另外開一張離屏 canvas 專門記刮痕，重畫遮罩之後再拿它蓋回去挖掉；改視窗大小時，舊刮痕按新尺寸縮放搬過去，不用從頭刮。

---

## 5. hugo.toml 在管什麼

網站的設定全部集中在 repo 根目錄的 hugo.toml，就這一個檔案。

### 5.1 一個檔案管到哪些事

由上而下大致是這幾塊：站台基本資料（baseURL、標題、主題、預設語言）、分頁筆數、GA4 的追蹤 ID、Markdown 的處理方式、taxonomy 定義、params（作者、描述、關鍵字、首頁那兩行職稱、社群圖示、分享預覽圖、配色模式、要額外載入的 CSS），最後是兩個語言區塊，各自帶自己的標題、作者名、描述，以及那五格選單。

導覽列的順序就是這裡的 weight 決定的：

```toml
[[languages.zh-tw.menu.main]]
name = "技術貼文"
weight = 3
url = "technical-posts/"
```

改順序只要改數字。這也是為什麼第 2 節那個順序調整，設定檔上就是五個數字的事，麻煩的反而是連帶被擠出去的選單寬度。

### 5.2 兩個看不出來的開關

這兩個都是最近兩天補上的，共通點是不設也不會報錯，畫面也看不出異狀。

第一個是時區。

```toml
timeZone = "Asia/Taipei"
```

front matter 沒寫時區的日期，Hugo 預設當成 UTC。當天發的文，在台灣時間早上八點之前都會被算成未來日期，而 `buildFuture` 預設是 false，那篇會整篇不建置。本地測不一定看得出來，因為當下時間可能已經過了；CI 跑在 UTC，等於線上直接少一篇。

第二個是中文字數。

```toml
hasCJKLanguage = true
```

Hugo 預設按空白切詞算字數，而中文不寫空格，一整段中文只會被算成一個詞。當時實測，站上最長那頁 6187 個字只算到 1031 個詞，剩不到六分之一。閱讀時間是 WordCount 除以 213 再無條件進位算出來的，字數失真，閱讀時間就跟著失真，一篇要讀十幾分鐘的文章會標成五分鐘。

---

## 6. 部署流程

### 6.1 本地先跑起來

改完不會直接推。先在 repo 根目錄跑 `hugo server`，開 localhost 把每一頁點過一次：五格選單都在、順序對、中英文都切得過去、履歷頁的照片刮得開。hugo server 會監看檔案，存檔就重整；改到 hugo.toml 的話它會自己重啟。

### 6.2 commit 訊息交給 skill

本地沒問題才進 git。訊息我不自己編，交給 [Day 11](https://ithelp.ithome.com.tw/articles/10405148) 那個 git-commit skill：它讀 diff，寫成 Conventional Commits 的格式加上一顆表情符號前綴，然後把 add、commit、push 三行指令印出來讓我自己跑。

指令由我跑，這點是刻意的。Claude Code 在我的設定裡對 git 的寫入操作一律要確認，理由不是不信任，是 commit 一旦推上去就進了公開紀錄，決定權我想留在自己手上。

push 到 main 之後由 GitHub Actions 接手：裝 Hugo 0.163.3 extended、checkout、跑 `hugo --gc --minify --baseURL`，然後發布到 GitHub Pages。本地的 Hugo 版本要跟 workflow 裡寫死的那個對得起來，不然會是本地跑得動、CI 掛掉，或是更難查的那種：兩邊都成功，但產出不一樣。

上線之後再驗一次，這次驗的是本地驗不到的東西：正式網域下的絕對路徑對不對、轉址頁真的會跳、GA4 有沒有重複注入、社群分享抓到的預覽圖是名片卡而不是那隻貓。

---

## 小結

今天做的事，說穿了是把一個 2023 年設計給「一個人偶爾寫點東西」的架子，改成裝得下現在這些內容的樣子。

至於刮刮樂那張照片，跟履歷本身一點關係都沒有，純粹是覺得好玩。~~但至少我確保了不想玩的人一鍵就能跳過，而且列印出來絕對不會是一塊灰色。~~

## 參考資料

Hugo 官方文件

- Configure Hugo — https://gohugo.io/configuration/
- Aliases（舊網址轉址） — https://gohugo.io/content-management/urls/#aliases
- Shortcodes — https://gohugo.io/content-management/shortcodes/
- Host on GitHub Pages — https://gohugo.io/host-and-deploy/host-on-github-pages/

其他參考

- 電腦版刮刮履歷（lala870617） — https://lala870617.github.io/resume.github.io/
- hugo-coder 主題 — https://github.com/luizdepra/hugo-coder

---

> 註一：hasCJKLanguage 的字數比較（6187 字對 1031 詞）是那次改設定時站上最長頁面的單次實測，不同頁面的低估倍率不一樣。

> 註二：文中描述的 Claude Code 行為以 2026 年 9 月這段期間的實際操作為準，屬於單次操作的定性觀察，不是可重現的評測；產品行為會隨版本改變。

> 註三：刮刮卡遮罩在行動裝置上的畫布面積上限依裝置記憶體而定，實際門檻**待確認**，本文只在桌機與一般手機尺寸下測過。
