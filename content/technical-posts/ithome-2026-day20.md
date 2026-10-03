---
title: "Day 20｜盤點個人網頁：清單由 Claude 列、權衡我自己扛"
date: 2026-09-03T00:00:00+08:00
authors: ["Alex Yu"]
series: ["iThome 2026 Ironman"]
tags: ["Claude", "iThome"]
---

> **This post is in Traditional Chinese Only.**

> Originally published on [iThome 2026 Ironman Contest](https://ithelp.ithome.com.tw/articles/10407372).

> 本篇階段：Prj#4 個人網頁

> 使用介面：Claude Code（via VS Code）

---

## 前情

[Day 19](https://ithelp.ithome.com.tw/articles/10407096) 把手環那條線收掉了，Prj#3 結束。今天換一個完全不同的題目：把三年前自己弄出來的個人網站，交給 Claude Code 從頭檢查一次。

個人網站可以把履歷、專案清單、做過的小東西都收在同一個網址底下，格式自己決定，要放互動頁就放互動頁。這件事對一個履歷上寫著跨領域的人特別有用，因為跨領域這三個字在制式表格裡幾乎沒有欄位可以填。呈現方式也完全自己掌握，不用配合別人平台的排版跟規則。

再說為什麼是現在來做這件事。我不是寫網頁的，這點沒有變過。2023 年第一次架的時候，光是搞懂 Hugo 的目錄結構、front matter 怎麼寫、GitHub Actions 要怎麼設，就翻了不知道多少篇教學跟別人的 repo，東拼西湊弄出一個能動的版本 ~~，弄完就再也不敢亂動，深怕動一下哪裡就壞了~~ 。弄好以後就一直擺著，中間幾乎沒加什麼東西；直到今年才零星動了幾次：換了頭像、調過版面、補了幾篇貼文，加著加著自己也覺得有點亂，索性趁這次把當年那套從建置到部署的流程重新走一遍，順便盤點現在到底是什麼狀況。現在的差別不在於我變會了，而在於可以直接問「這個網站有什麼問題？」「要怎麼改？」「直接幫我改」~~三年前要是像現在這麼方便，就不用搞個一個禮拜，可能只需要半天。~~

讓 Claude Code 檢查一波下來，最有感的是好幾項問題其實都藏在螢幕上完全看不出來的「一切正常」底下。

> 這一輪的完整健檢報告（十二項發現的逐項處理結果與驗證數字）在這裡，瀏覽器可以直接開：[Alex Yu 個人網站健檢.html](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day20_20260903/Alex%20Yu%20個人網站健檢.html)，相關檔案在同一個[專案連結](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day20_20260903)底下。

---

## 1. 先要清單，不要修改

第一件事不是叫它動手，是叫它盤點。讓 Claude Code 把整個 repo 讀過一遍，包含所有檔案、跑一次完整建置、連產出的 HTML 也一起看，然後列出問題，先不要改。

這個順序有差。直接說「幫我優化網站」會拿到一堆改動，而我根本沒有能力判斷哪些該收哪些不該收。先拿清單的話，每一項都可以獨立看：這是真的問題嗎、嚴重到什麼程度、修了會動到什麼。

回來十二項，按嚴重度排：

| | 項目 | 判定 |
|---|---|---|
| 1 | 英文站的貼文其實是中文 | 需修正 |
| 2 | 履歷頁有七個 h1 | 需修正 |
| 3 | 2023 年的一句話殘稿還公開掛著 | 需修正 |
| 4 | 兩張重複的圖，而且沒人引用 | 待改善 |
| 5 | 互動示範頁在站內沒有任何入口 | 待改善 |
| 6 | 512 像素的圖示佔 343 KB | 待改善 |
| 7 | 分享到社群的預覽圖是一隻貓 | 待改善 |
| 8 | 兩篇貼文各有兩個 h1 | 待改善 |
| 9 | 一個示範頁目錄命名不一致 | 待改善 |
| 10 | 升 Hugo 版本時建置會斷的 API | 待改善 |
| 11 | 部署設定裡指向不存在目錄的註解 | 待改善 |
| 12 | 沒有授權聲明 | 待改善 |

有預期中的，像是沒有 LICENSE、有兩張重複的圖沒人用；也有幾項是我完全沒想過要往那個方向看的。上面只是標題，每一項底下還有證據、影響範圍跟建議做法，完整的那份在[健檢報告](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day20_20260903/Alex%20Yu%20個人網站健檢.html)裡。

清單裡沒有的東西同樣有用。網站上那幾個密碼保護的示範頁，檢查結果說內容是真的加密，AES-GCM-256 加上 PBKDF2-SHA256 跑 250,000 輪導出金鑰，不是那種把內容藏起來、用 JS 比對字串的假保護。多語系的 hreflang 三組齊全、每頁 canonical 都在、GA4 只注入一份，有些在 2023 年設好之後就再也沒看過的東西，也都還活著。 ~~手刻 Code 萬歲 (?)~~

---

## 2. 沒有症狀的那幾項

這幾項的共通點是：網站畫面正常，建置成功，沒有任何錯誤訊息。壞掉的東西通常會跳出問題，這幾項不會。

### 2.1 英文站其實是中文站

網站是中英雙語，導覽列可以切換語言。

實際上 `content/posts/` 底下五對雙語檔案，「英文版」除了 `authors` 欄位從「尤俊硯」換成「Alex Yu」之外，標題、摘要、內文一個字都沒改：

```
/posts/  （英文列表頁實際輸出）
  2026瀨戶內海五日跟團遊
  教召攜帶物品推薦清單
  教召攜帶物品清單
  旅遊確認清單
  2026東京近郊自駕
  First Post          ← 唯一真正的英文標題
```

而 README 裡還寫著「Every page is available in English and Traditional Chinese」，但實際上不完全是這樣。(也跟我在建置後的這幾年沒有特別去維護有關係)

會這樣是因為當初做雙語的時候，我先照著模板把檔案複製成 `xxx.md` 跟 `xxx.zh-tw.md` 兩份，先大致留位給這個功能。切換功能是真的會動，只是切過去看到的還是中文，當時先著重在功能切換正常的這個部分。

檢查抓到這一項的線索是頁數對不起來：建置報表顯示英文 40 頁、中文 50 頁。有一篇談建站過程的貼文只有中文版，英文站那邊根本不存在，以此類推。

比較需要思考的是這一頁的讀者是誰。個人網站的英文版，多半是有人從 LinkedIn 點進來時才會看到（而那個人多半是招聘方），結果看到的卻是一頁中文標題。

處理方式是把某些內容整份同步翻成英文，另外一些中文限定的則是在英文版頁首標上中文限定的說明，同時把 README 那句話改掉。翻譯的部分不只換標題，是把互動頁的內容整份重做一份英文版。

### 2.2 履歷頁有七個 h1

這個很難自己發現，因為畫面上完全正常。`about.md` 裡我用 `#` 當作區塊標題（WORK EXPERIENCE、EDUCATION、SKILLS），底下直接接 `####`。Hugo 本身已經輸出過一次頁面標題的 `h1`，加起來變成：

```
/about/ 的標題序列
  h1 h1 h4 h1 h4 h4 h1 h3 h3 h3 h3 h3 h3 h1 h4 h4 h4 h1 h1 h4 h4 h4
     └─ h2 完全缺席，h1 出現 7 次
```

螢幕閱讀器是靠標題階層建立目錄跳轉的。七個並列的 `h1` 等於告訴它這頁有七個同等重要的主題，而且中間跳過 h2 直接到 h4，階層是斷的。這頁是履歷頁，是整個網站最需要被讀懂的一頁。（有點久沒更新了，預計也會來更新一下）

修法是純 Markdown 的尋找取代，`#` 降成 `##`、`####` 降成 `###`，四個檔案，版型一行沒動。改完 `/about/` 跟 `/projects/` 都是一個 `h1`。

### 2.3 一段 2063 字元的 meta description

搜尋結果底下那行摘要，是從 `description` 這個欄位來的。`about.md` 跟 `projects.md` 沒有寫，主題於是退而求其次，抓內文開頭去填：

```
                              修正前        修正後
  /zh-tw/about/            2063 字元  →    57 字元
  /about/                   782 字元  →   143 字元
  /zh-tw/projects/          503 字元  →    46 字元
  /projects/                485 字元  →   153 字元
```

搜尋結果只會顯示前面一小段，剩下全部截掉，等於整個欄位白白浪費。而這又剛好是履歷頁：別人搜到我的名字，第一眼看到的那行字，是我的自我介紹被砍在半句中間。

補上四段一百多字元的描述就解決了。

這一項是掃描建置後約一百個頁面才抓到的。基礎設定其實都對，壞掉的是後來新增內容時沒有跟著補的那一格。三年前設定的骨架撐住了，後來長出來的肉沒跟上。

### 2.4 現在沒事，下次升級才會壞

第四項嚴格說不算「看不出來」，是「還沒發生」。

建置跑起來零錯誤，只有一行警告，來自主題裡的一個呼叫：`.Language.LanguageName` 這個屬性在 Hugo 0.158 就被標記為 deprecated，官方說明是未來版本會移除。移除的那天，建置不是繼續跑帶個警告，是直接失敗。

麻煩的地方在於錯誤訊息會指向主題的樣板檔案，而那個檔案我從來沒打開過，是三年前 clone 進來就沒再動的。真的那天出事，我大概會先懷疑自己剛剛改的內容，再懷疑 GitHub Actions，最後才會想到去看主題。~~老實說我覺得現在實務上會靠 LLM 處理，應該會方便很多的。~~ 解決方式是換一個屬性名稱，這種問題基本上不太會主動去找，因為它能動，而軟體工程時常講求一個能正常運作就好，警告訊息就只是個警告，直到變成錯誤的那天XD

---

## 3. 檔案很大，不等於有成本

清單裡有一項是我自己補上去的：`android-chrome-512x512.png` 佔 343 KB，一張 512 像素的圖示不該這麼大。

Claude 實際查下去才發現方向錯了。那三張大圖只被 `site.webmanifest` 和 `rel="apple-touch-icon"` 參照，一般人打開網頁，瀏覽器根本不會去抓：

```
一次頁面瀏覽實際請求的圖片
  favicon-16x16.png      736 B
  favicon-32x32.png      2.3 KB
  首頁頭像               173 KB   ←

只在「加到主畫面／安裝」時才會抓
  android-chrome-512x512.png   343 KB
  android-chrome-192x192.png    60 KB
  apple-touch-icon.png          53 KB
```

Claude 當成效能問題的那 343 KB，從來沒有花過任何一個訪客的流量。更麻煩的是，唯一能省下六成的做法是 PNG-8 調色盤量化，而那張圖是一隻異色瞳的貓（我今年稍早時加的），量化之後琥珀色那隻眼睛會被壓成黃綠色。把兩個版本並排在實際顯示尺寸下比對，差異看得出來。所以這一項最後是不改。

真正在花流量的，是表裡標了箭頭的那張首頁頭像。原圖 1024×1024、173 KB，版面上卻只畫成 200px，等於每次打開首頁都多下載了約五倍的像素。這張就值得處理，而且做法跟那顆圖示不一樣：圖示要縮檔得靠 PNG-8 調色盤量化，會毀掉眼睛顏色；頭像則是把原圖縮成 400px（200px 的兩倍，留給高解析螢幕），再轉成 WebP，完全沒動到調色盤，貓還是那隻貓、琥珀色也還在，檔案卻從 173 KB 掉到 20.9 KB。同樣一隻貓，一個留著大檔也沒差、一個值得縮，差別只在前者沒人下載、後者每次都下載。

同一輪還抓到一件跟圖有關、但跟效能無關的事：分享到社群的預覽圖也是那隻貓。設定裡 `og:image` 指向的就是首頁頭像，所以把網址貼到 LinkedIn，跳出來的預覽卡片是一張貓的照片。首頁放貓當頭像是刻意的，我沒打算改；但預覽卡片是別人在動態牆上滑過去時唯一會看到的東西，那個位置放貓，跟這個網站另一半是履歷的定位對不起來。這一項後來另外做了一張帶姓名跟專長的卡片給它用，首頁的貓維持不動。

---

## 4. 閱讀寬度：主題原本就設好了，是我拿掉的

這一項要從三年前講起。

hugo-coder 這個主題原本就有設內容欄寬度，`.container` 是 `max-width: 90rem`。我在今年稍早某一次改版把它放寬了，改成幾乎滿版，理由現在想起來很單純：買了大螢幕，覺得兩側留那麼多空白很浪費，內容當然是塞滿比較好。

後來查資料才知道那個寬度不是主題作者隨手填的，背後是人因工程。

讀一行字的時候，視線並不是平滑滑過去的，是一小段一小段跳（saccade），跳完一行再整個掃回下一行的開頭，這個動作叫 return sweep。回掃的落點靠的是行首那一側的空間關係，行愈長，回掃要跨越的距離愈大，落點就愈容易偏掉。偏掉的結果是重讀同一行或跳過一行，然後得回頭確認，一整篇累積起來就是「讀完很累但說不出哪裡累」。

排版上一般建議每行 45 到 75 個西文字元，WCAG 1.4.8 則把 80 字元列為上限。主題原本那個 90rem，換算下來就落在這個區間裡。我改成滿版之後，在 27 吋螢幕上一行可以跑到一百多個字元，早就超出上限。

知道原理之後回頭看自己的網站，才對上了另一件事。我自己在大螢幕上讀那幾篇長文，確實讀得很吃力，會不自覺想把瀏覽器視窗拉窄。當時只覺得是字太小或自己不專心，從來沒把它跟版面寬度連在一起，畢竟那是我自己調的，而且調的時候覺得很合理。原理跟體感對上之後就沒什麼好猶豫了，請 Claude 改回來。

改的時候有個小插曲值得記一下。48rem 這個常見數字是在 16px 的根字級下算出來的 768px，但 hugo-coder 把 `html` 設成 `font-size: 62.5%`，這個專案裡 1rem 等於 10px。照字面寫 `48rem` 會得到 480px，比手機視窗還窄，要拿到 768px 得寫 `76.8rem`。

最後整個檔案只剩一條規則：

```css
.container {
  max-width: 76.8rem;
}
```

導覽列、文章、列表頁、footer、互動頁共用同一個 `.container`，改這裡整站一致。扣掉容器自帶的左右 padding，實際文字寬約 728px，在本站 18px 的內文下大約是一行四十個中文字。

這一項跟前面幾項不一樣。前面那些是我不清楚所以弄錯，這一項是我知道有個設定、但以為那是可以照喜好調的參數，於是把一個有依據的預設值改成了個人偏好。

主題作者沒有在程式碼旁邊寫下理由，只留一個數字。這次改回去的時候，有請 claude 把理由跟換算過程寫成註解留在 CSS 裡，包含那個 1rem 等於 10px 的陷阱，下次不管是誰想動它，至少會先看到為什麼是這個值。

---

## 5. 搬家的時候，已經發出去的連結還在

網站上有四個密碼保護的互動示範頁，是前面幾天文章用到的，這次想搬到作品集 repo 集中管理。

檢查的時候先攔下一件事：Day 04 跟 Day 05 已經發布的文章裡，有四條連結指向現在的網址。文章已經公開，讀者隨時可能點進去，直接搬走那四條當場 404。解法是在原位置留轉址頁，`meta refresh` 加 `canonical` 加 `location.replace()`，再放一個可以點的備援連結。四頁加起來大約 6 KB，換到已發布的文章一個字都不用改。

這種「動作本身沒問題，但會波及外面」的狀況，是我指定 Claude 要特別注意的情況，而他的確處理了這個問題。

---

## 小結

十二項全部處理完，另外還追加了三項：重壓首頁頭像、補上四頁的 meta description、把閱讀寬度改回主題原本的值。整輪下來，建置從一個警告變成零警告，兩個語言的貼文數對齊，履歷頁的標題階層修好了，首頁載入的圖片也從 173 KB 降到 20.9 KB。

Claude Code 幫得上的，是「把整個 repo 讀一遍然後列出問題」。這需要同時看 Markdown、看 Hugo 設定、看主題的 SCSS、看建置後的 HTML，一個人做要來回切換很久，而且很容易看不出來。

它幫不上的，是判斷那 343 KB 值不值得壓：得先知道那張圖是異色瞳的貓、知道琥珀色那隻眼睛是重點。清單是它列的，權衡還是得自己做，而這一輪最大的兩個轉折都發生在權衡的時候。

回到開頭那個問題：不會寫網頁的人能不能維護一個像樣的個人網站？可以。差別不是我突然學會了什麼，而是現在可以直接問「這裡有什麼問題」再讓它動手，省掉當年翻遍教學、自己慢慢摸的那一大段路。

那個閱讀寬度大概是這一輪最好的例子。三年前主題作者已經幫我設好了，我沒問為什麼就改掉，然後在大螢幕前面讀得很累卻沒把兩件事連起來。這次改回去，順手也把「為什麼是這個數字」查清楚了，不再只是照抄一個值。

## 參考資料

Hugo 官方文件

- Hugo — Image Processing — https://gohugo.io/content-management/image-processing/
- Hugo — Multilingual Mode — https://gohugo.io/content-management/multilingual/
- Hugo — Configure Markup — https://gohugo.io/getting-started/configuration-markup/

無障礙與人因

- W3C — Understanding SC 1.3.1: Info and Relationships — https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html
- W3C — Understanding SC 1.4.8: Visual Presentation — https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html
- MDN — The HTML Section Heading elements — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements
- Butterick's Practical Typography — Line length — https://practicaltypography.com/line-length.html

網頁效能與圖片

- web.dev — Optimize Cumulative Layout Shift — https://web.dev/articles/optimize-cls
- MDN — Responsive images — https://developer.mozilla.org/en-US/docs/Web/HTML/Responsive_images
- MDN — WebP image format — https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types#webp

SEO 與多語系

- Google Search Central — Localized versions of your page — https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Search Central — Control your title links — https://developers.google.com/search/docs/appearance/title-link

其他參考

- hugo-coder（本站使用的主題，作者 Luiz de Prá，MIT 授權） — https://github.com/luizdepra/hugo-coder
- GitHub Docs — Configuring a publishing source for your GitHub Pages site — https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

---

> 註一：第 3 節那張「一次頁面瀏覽實際請求的圖片」是從建置後的 HTML 逐一比對參照關係得到的，不是用瀏覽器的網路面板實測。實際行為會受瀏覽器與作業系統對 manifest 圖示的處理策略影響，Claude 建議標記為待確認。

> 註二：第 4 節提到的每行 45 到 75 個西文字元是排版上的通則，來源是排版文獻而非針對本站的閱讀實驗；WCAG 1.4.8 的 80 字元上限則是明文規範。中文的最適行長不能從西文直接換算，文中的「約四十個中文字」是依字寬推算，沒有做過閱讀測試。第 4 節提到自己在大螢幕上讀得吃力，那是個人感受，不是實驗結果。

> 註三：本篇提到的健檢報告是一份自包含的 HTML，透過 GitHub Pages 直接在瀏覽器開啟：[Alex Yu 個人網站健檢.html](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day20_20260903/Alex%20Yu%20個人網站健檢.html)，沒有外部相依。相關檔案在同一個[專案連結](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day20_20260903)底下；個人網站本身的原始碼在 https://github.com/ycy1997alex/ycy1997alex.github.io 。
