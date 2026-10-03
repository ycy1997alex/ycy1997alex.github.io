---
title: "Day 12｜開始寫程式之前，先去把幾個帳號辦一辦"
date: 2026-08-26T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10405357)。

## 要解決的

[Day 11](https://ithelp.ithome.com.tw/articles/10405148) 把 settings、skills、rules、agents 各自的內容處理好，有關 CLAUDE 加目錄設定就告一段落了。接下來要進實際的專案來測試看看，而排在最後面的專案是總體經濟與股票相關的，並要嘗試接上 GitHub Pages 的自動更新。

而這個專案需要串接外部 API，其中有些需事先申請，而且**其中申請證券戶要花上幾天**，不是當天想到當天就有。

所以今天不寫程式。今天只做一件事：把該辦的帳號辦一辦，該申請的金鑰申請下來，約十天後會用到（想要跟著做的話，現在就得動手）。

先給結論，約十天後的範例會用到：**永豐金 Shioaji（台股）＋ yfinance（美股與跨市場）＋ FRED（總體經濟）**。另外還需要一個 GitHub 個人帳號。

---

## 1. 今天要辦的四件事

| 要辦的 | 前提 | 要等多久 | 費用 |
|---|---|---|---|
| 永豐金 Shioaji API | **必須先有永豐金證券帳戶** | 開戶需幾個工作天，API Key 當下就給 | 免費 |
| FRED API Key | 一個 email | 註冊完當下就給 | 免費 |
| yfinance | 無 | 不用申請 | 免費 |
| GitHub 個人帳號 | 一個 email | 當下 | 免費 |

順序上唯一有卡點的是第一項。**沒有永豐金證券的戶頭，就拿不到 Shioaji 的 API Key**，而開戶審核不是即時的。打算跟著後面幾天做的話，這一項要先去辦。

---

## 2. 永豐金 Shioaji：先要有證券戶

### 2.1 前提：永豐金證券帳戶

Shioaji 是永豐金證券提供給自家客戶的程式交易 API，不是公開資料服務。**要用它，必須是永豐金證券的客戶。**

沒有戶頭的話，永豐金有線上開戶：備妥雙證件（身分證 + 健保卡或駕照）、本人名下的銀行帳戶資料，在手機或電腦上完成身分驗證與問卷，送出後等審核，開戶本身不收費。

開戶完成後會拿到帳號與密碼，這兩個是接下來每一步的基礎。

### 2.2 申請 API Key 與 Secret Key

有戶頭之後，剩下的都在網頁上點：

1. 搜尋「永豐金證券 API 管理頁」並進入 **(要確認是正確的 www.sinotrade.com.tw 並有類似 PythonAPIKey 字眼的網址)**
2. 按「新增 API KEY」
3. 做一次雙因素驗證（手機或 email）
4. 設定這把金鑰的**到期日、權限（行情／帳務／下單／正式環境）、綁定帳號、IP 限制**
5. 建立成功，畫面上給出 API Key 與 Secret Key

第 5 步有一個不能忘記的地方：**Secret Key 只在建立當下顯示一次**，關掉頁面就再也看不到，只能刪掉重辦。當場複製起來。

至於權限，如果只是要抓資料做評分、暫時不打算下單，第 4 步可以先不勾「下單」。少一項權限就少一個出事的面向。

### 2.3 金鑰要放哪裡

官方建議寫進 `.env`，用 `python-dotenv` 讀進來：

```
SJ_API_KEY=...
SJ_SEC_KEY=...
SJ_CA_PATH=...
SJ_CA_PASSWD=...
```

這裡要提醒的是 [Day 11](https://ithelp.ithome.com.tw/articles/10405148) 講過同一件事：`.env` 和 `.pfx` 都要進 `.gitignore`，而且要在第一次 commit **之前**就進去。金鑰一旦被推上 GitHub，就算馬上刪 commit 也要當作已經外洩，回頭重辦一組比較安全。

### 2.4 流量與次數限制，先看一眼

Shioaji 有明確的用量上限，而且級距是綁交易量的：

| 近 30 日成交金額（證券／現貨整股） | 每日流量 |
|---|---|
| 0 元 | 500 MB |
| 1 元 – 1 億元 | 2 GB |
| > 1 億元 | 10 GB |

期貨那邊一樣是這三階，級距換成近 30 日成交口數（0 口／大台 1,000 或小台 4,000 口以內／超過）。流量在開盤日早上 8:00 重置。

其他幾條限制：同一身分證字號最多 **5 個連線**、行情查詢 10 秒 50 次、帳務查詢 5 秒 25 次、委託操作 10 秒 250 次、訂閱上限 200 個、登入一天上限 1,000 次。超過流量時行情查詢會回空值，超過次數則暫停服務一分鐘，屢次違規會被停掉 IP 與 ID 的使用權。

對只是每天抓一次盤後資料的用途來說，**500 MB 綽綽有餘**。會撞到牆的通常不是資料量太大，而是迴圈寫錯、斷線重連沒退避、或是錯誤重試沒有上限，這幾種寫法會在幾分鐘內把一天的額度燒光。

~~想當初我就是因為想知道自己燒掉多少，順手寫了一個查用量的小工具。~~ 這個工具我放在 [shioaji-usage](https://github.com/ycy1997alex/shioaji-usage)。

---

## 3. FRED API Key：上網填一頁就好

FRED 是聖路易聯準銀行的經濟資料庫。總經那一整層的資料，包括利差、CPI、失業率、高收益債利差、聯準會資產負債表、OECD 各國出口，都從這裡拿。

申請流程比 Shioaji 短很多，**不需要任何帳戶或身分證明**：

1. 到 <https://fredaccount.stlouisfed.org/> 註冊一個免費帳號（email 驗證）
2. 登入後進 API Keys 頁面，按 Request API Key
3. 填一句用途說明（寫個人研究、學習用途就可以）
4. 同意使用條款，送出
5. 金鑰當下就出現在頁面上

額度方面：帶 API Key 的請求速率上限是**每分鐘 120 次**，沒帶金鑰只有 30 次。官方沒有公布每日總量。對每天更新一次、一次抓十幾條序列的用法，這個額度完全不是問題。

存放方式跟上一節一樣，環境變數 `FRED_API_KEY` 或一個被 gitignore 的檔案，二選一。

---

## 4. yfinance：不用申請，但要知道它的代價

yfinance 完全不需要申請，`pip install yfinance` 就能用。它拿的是 Yahoo Finance 公開端點上的資料，涵蓋美股、ETF、指數、外匯、部分台股代號，而且有很長的歷史資料，回測要拉十幾年的價格，這是最省事的來源。

- 套件首頁：<https://github.com/ranaroussi/yfinance>
- 文件：<https://ranaroussi.github.io/yfinance/>
- PyPI：<https://pypi.org/project/yfinance/>

有個部分要講清楚：**yfinance 不是 Yahoo 的官方 API，也沒有得到 Yahoo 的背書。** 它是社群套件，靠著呼叫 Yahoo 前端在用的端點運作，官方定位是研究與教學用途、個人使用。這代表三件事：

1. **會壞。** Yahoo 改端點的時候套件就會壞，通常幾天內社群會修好，但那幾天是真的抓不到。
2. **沒有 SLA，也沒有客服。** 出事只能自己讀 issue。
3. **資料品質要自己驗。** 特別是台股代號、除權息調整、以及成交量欄位，偶爾會出現明顯不合理的值。

所以用法預計是：**yfinance 負責「長歷史 + 廣度」，不負責「準確 + 即時」**。真的要精確到單一台股的當日資料，要靠 Shioaji。

---

## 5. 台灣其他券商的 API

會選永豐是因為它的 Python 套件最單純，`pip install shioaji` 之後就是一般的 Python 物件，不用裝 COM 元件、不用綁 Windows。但台灣提供程式交易 API 的券商不只一家，有些的語言生態跟永豐差很多，開戶之前值得先看一眼。

> 以下是 CLAUDE 整理的

### 5.1 對照表

| 券商 | API 名稱 | 主要語言 | 作業系統 | 功能範圍 | 申請門檻 | 額度／限制 |
|---|---|---|---|---|---|---|
| **永豐金** | Shioaji | **Python** | Windows／macOS／Linux | 行情、歷史 K 線、下單、帳務、期權 | 永豐金證券戶 → 網頁自助申請 API Key + 憑證，免營業員 | 每日流量 500 MB／2 GB／10 GB（依近 30 日成交金額三階）；5 連線；行情 10 秒 50 次；訂閱 200 個 |
| **富邦** | Neo API | Python、C#、Node.js | Windows／macOS／Linux | 行情、下單、帳務 | 富邦證券戶 → 簽署 API 協議 + 連線測試 + 憑證 | 未公開 |
| **元大** | SPARK API | Python、C#（另有舊的 COM／Delphi／WPF 元件） | Windows／macOS／Linux | 行情、下單（含雲端條件單）、帳務、庫存損益 | 元大證券戶，**無財力或交易量門檻**；簽風險預告書 + API 測試 | 未公開 |
| **凱基** | SUPER PY | Python 3.9–3.13（64 位元） | Windows（需 VC++ 2015–2022 Redistributable） | 台股、美股行情與下單 | 凱基證券戶 + 數位憑證 + 簽署風險預告書 + 測試軟體驗證 | 未公開 |
| **群益** | 策略王 API | C#、Python（以 COM 元件為底） | Windows | 國內外證期選行情、下單、回報 | 群益戶 → **需向營業員申請並簽約** | 未公開 |
| **元富** | MasterTradePy（下單）＋ SolPYAPI（行情） | Python | Windows | 行情與下單分成兩個元件 | 元富戶 + 數位憑證 + 線上簽署風險預告書 + 線上驗證 | 未公開 |
| **統一期貨** | 統一 API | Python、C#、Excel VBA | Windows | 期貨為主 | 統一期貨戶 → 洽營業員，免費 | 未公開 |
| **玉山（富果）** | Fugle 行情 API／交易 API | Python、Node.js（REST + WebSocket） | 跨平台 | 日內行情、歷史行情、技術指標、盤後籌碼、下單 | 行情 API 註冊富果會員即可；交易 API 需玉山證券富果帳戶，**開戶次日**可申請 token | 分級收費，見 5.2 |

### 5.2 三個值得單獨講的差異

**第一，「跨平台」在這裡差很多。** 群益和元富是以 Windows COM 元件為基礎的，套件裝好之後仍然綁在 Windows，Linux 上的排程機器跑不了。永豐、富邦、元大、富果是真的跨平台。

**第二，自助 vs. 找營業員。** 永豐、元大、凱基、元富都是網頁上自己走完流程；群益要向營業員申請並簽約，統一期貨也是洽營業員。

**第三，富果是唯一把「行情」和「券商戶」拆開賣的。** 沒有玉山證券帳戶也可以註冊富果會員拿免費行情 token，甚至有 demo token 可以先試，是唯一一個能在完全不開戶的情況下先玩玩看的選項。它的行情方案是這樣分的：

| 方案 | 價格 | 台股日內行情 | 歷史行情 | 技術指標／盤後籌碼 | WebSocket |
|---|---|---|---|---|---|
| 基本用戶 | 免費 | 60 次／分 | 60 次／分 | 不支援 | 5 訂閱／1 連線 |
| 開發者 | NT$1,499／月 | 600 次／分 | 60 次／分 | 60、30 次／分 | 300 訂閱／2 連線 |
| 進階用戶 | NT$2,999／月 | 2,000 次／分 | 60 次／分 | 60、30 次／分 | 2,000 訂閱／2 連線 |

免費那一層的「不支援技術指標」值得注意：打算讓別人幫忙算指標的話，免費方案不夠；打算自己從 K 線算，免費方案夠用。

### 5.3 那為什麼是永豐

三個理由，按重要性排：

1. **Python 是第一等公民。** 不是「附了 Python 範例的 C# 元件」，是原生的 Python 套件，而且跨平台。
2. **申請全程自助。** 網頁上點一點就有 Key，憑證也是網頁下載，不用約時間、不用打電話。
3. **限制寫得清楚。** 流量分級、各種次數上限、超限的後果，官方文件一條一條列出來。這在後面設計更新頻率時，是可以直接拿來算的數字。

反過來說，本來就是元大或富邦的客戶的話，那兩家的 API 也都跨平台、也都免費，沒有必要為了跟這個系列而多開一個戶。**後面幾天的重點是資料怎麼流、評分怎麼設計，換一家券商要改的只有取資料那一層。**

~~但依照我目前查詢到的內容，套件 Shioaji 的 document 是真的很完整，推推。~~

---

## 6. 記得還要有一個 GitHub 帳號

約十天後的那個專案要把結果推上 GitHub Pages，並且用排程做定期更新，所以需要一個 **GitHub 個人帳號**。

這裡先提需求就好：免費帳號足夠，到 <https://github.com/> 用 email 註冊，順手把兩步驟驗證打開。

---

## 小結

今天沒寫半行程式，但這是整個系列裡「不做完就沒辦法往下走」的一天。

三個來源的分工大概是：**FRED 管總體經濟、yfinance 管長歷史與廣度、Shioaji 管台股的準確與即時。** 三個都免費，兩個要申請，一個要先開證券戶。

開戶審核那幾天，不管手上的程式寫得多好都沒有辦法縮短。而這種前置作業在專案裡通常不會被排進時程，因為它看起來不像工作，直到某個週六下午想開始動手，才發現什麼都做不了。

約十天後才會真正用到，但審核時間不會等人，所以先辦起來放著。

## 參考資料

券商官方文件

- 永豐金 Shioaji — 金鑰與憑證申請 — https://sinotrade.github.io/zh/tutor/prepare/token/
- 永豐金 Shioaji — 使用限制 — https://sinotrade.github.io/zh/tutor/limit/
- 永豐金證券 Python API — https://ai.sinotrade.com.tw/python/Main/index.aspx
- Shioaji GitHub — https://github.com/Sinotrade/Shioaji
- 富邦 Neo API 文件 — https://www.fbs.com.tw/TradeAPI/
- 元大 SPARK API — https://www.yuanta.com.tw/file-repository/content/API/page/index.html
- 凱基 SUPER PY — https://superpy.kgieworld.com.tw/kgipythonapi/
- 元富數位 API 專區 — https://mlapi.masterlink.com.tw/web_api/service/home
- 統一期貨 API — https://www.pfcf.com.tw/software/detail/1223
- Fugle Developer Docs — 台股行情方案及價格 — https://developer.fugle.tw/docs/pricing/
- Fugle Developer Docs — 富果交易 API — https://developer.fugle.tw/docs/trading/intro/

資料源官方文件

- FRED API 文件 — https://fred.stlouisfed.org/docs/api/fred/
- FRED 帳號與 API Key — https://fredaccount.stlouisfed.org/
- yfinance GitHub — https://github.com/ranaroussi/yfinance
- yfinance 文件 — https://ranaroussi.github.io/yfinance/
- FinMind 登入說明 — https://finmind.github.io/login/
- FinMind API 使用次數 — https://finmind.github.io/api_usage_count/

---

> 註一：本文所有申請流程、額度數字與方案價格以各家官方頁面為準。券商 API 的規格、收費與限制改動頻繁，實際申請前請以官方公告為準。

> 註二：第 5.1 節對照表中標示「未公開」的欄位，代表該券商的公開文件未揭露流量或呼叫額度，不代表沒有限制；實際上限請洽該券商。表中富邦、元大、凱基、群益、元富、統一期貨六家的資訊來自官方頁面與公開技術文章的整理，我本人只實際申請並使用過永豐金 Shioaji，其餘六家屬**文件引述而非實測**，細節（特別是群益的 Python 支援程度、元富行情與下單元件的實際相依性）**待確認**。

> 註三：本文為個人學習與工具建置紀錄，所有提及的券商、資料源與方案均非業配，也不代表推薦。**本文不構成任何投資建議，亦不構成開立特定券商帳戶之建議。投資有風險，任何投資決策請自行評估並自負盈虧。**
