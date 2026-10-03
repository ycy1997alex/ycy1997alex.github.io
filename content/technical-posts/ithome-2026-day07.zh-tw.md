---
title: "Day 07｜用 Claude Desktop 來做電腦的硬體診斷吧！"
date: 2026-08-21T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
summary: "用 Claude Desktop 診斷自己的電腦：Wi-Fi、電腦變慢與當機紀錄，我的假設怎麼被數據推翻，真正的原因又在哪裡。"
description: "用 Claude Desktop 診斷自己的電腦：Wi-Fi、電腦變慢與當機紀錄，我的假設怎麼被數據推翻，真正的原因又在哪裡。"
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10404285)。

> 本篇階段：網路與硬體、環境

> 使用介面：Claude Desktop（Cowork mode）

---

## 前情

[Day 06](https://ithelp.ithome.com.tw/articles/10404091) 的題目有明確規格，丟出去就知道要什麼。今天相反，起點是兩句對電腦的抱怨 ~~(記憶體漲成這樣只好先暫時客家一點不換電腦)~~：

- 家裡的 Wi-Fi 好像有點慢。
- 電腦好像也變慢了。

這種問題最麻煩的地方在於不知道要從哪裡查起...是網卡？是路由器？是 RAM 不夠？還是硬碟該清了？我對第二題甚至已經有一個算不上猜的答案：Chrome 開太多分頁，記憶體吃光了。

所以這天做的事情很單純：直接實測。兩次都是相同一套分工，結論也很像；最後也順手整理我 Anaconda 裡各個環境哪些有 Office 套件做為測試，之後某天會用到。

---

## 1. 先把 Claude Desktop 裝起來

前六天都在瀏覽器裡的 claude.ai 做事，從今天開始要碰本機的檔案和指令，所以先把桌面版裝起來。

下載頁只有一個：<https://claude.ai/download>。以 Windows 版來說，抓下來是一個 `.exe`，安裝過程沒有任何需要選的東西，一路下一步就結束了，也不用先裝 Python 之類的。裝完登入同一組帳號，之前在 claude.ai 上的對話就會自動同步了。

要留意的差別只有一個：**本機檔案存取和 Cowork mode 是桌面版才有的**，今天後面所有的診斷都靠這個，瀏覽器版做不到。實際權限長什麼樣子在第 2 節和第 9 節都會看到，它不是裝完就全開，而是每次用到才跳出來問。

> 如果在 claude.ai 使用的話，會說明「目前沒有連上電腦（沒有裝置橋接），所以以下是這個雲端沙箱環境的資訊。」

## 2. 兩次都先撞到同一道牆

第一句話丟出去，Claude 沒有開始給建議，而是先講自己碰不到什麼。

> 橋接給我的 `device_bash` 是跑在一個**獨立的 Linux VM** 裡，只有連結的資料夾會掛載進去，它沒辦法執行 Windows 指令，所以 `Get-Process`、`tasklist`、WMI 這些一律碰不到，連了資料夾也一樣。

後半句是我原本沒想到的：連資料夾只解決檔案存取，不解決指令執行，這是兩件事。~~我還一度以為把整顆 C 槽連上去就無敵了。~~

它給了三條路：排程器定時寫 JSON 快照、裝一個有 Windows shell 能力的本機 MCP、或是最「工人智慧」的一條路（它給腳本，我執行，把報告貼回去， ~~身為一個勞工楷模(?)~~ ）我選了第三條。

## 3. 編碼踩了兩次，第二次學乖了

Wi-Fi 那輪的 PowerShell 一次撈完介面、驅動、設定檔、鄰居 AP、網卡進階屬性，吐出來的檔案中文是壞的，UTF-16 混 Big5 的經典慘案。Claude 自己做了編碼轉換，把 cmdlet 那段原生 UTF-16 的中文還原，netsh 那段壞掉的直接靠英文欄位和數值判讀。**檔案髒掉沒有讓它卡住。**

到了效能那輪，同樣的坑換個樣貌又來一次，腳本訊息全是中文，下載過程 BOM 掉了，PowerShell 5.1 沒有 BOM 就用系統 ANSI 去讀：

```
+ if ($up.Days -ge 7) { W "  [!] 撌脰???7 憭拇??璈?閮擃???瘣拇?摰寞?蝝舐?嚗遣霅圈 ...
運算式或陳述式中有未預期的 '[!]' 語彙基元。
```

這次它沒有去凹更複雜的編碼參數，而是把腳本改成純 ASCII，報告全用英文輸出，中文的部分留在對話裡翻譯。

> 最乾淨的解法是把腳本改成純 ASCII，這樣不管用什麼編碼讀都不會出事。

上次是事後救壞掉的輸出，這次是事前避開。踩過一次之後選了更穩的路，我覺得這個轉變比原本的修復技巧更穩定。

## 4. Wi-Fi：訊號滿格、零干擾，然後呢

診斷資料回來是這樣：

| 項目 | 數值 |
|---|---| 
| 頻帶 | 2.4 GHz（通道 6） |
| 無線電類型 | 802.11n |
| 連線速率 | 接收 108 / 傳送 270 Mbps |
| 訊號強度 | 87%，RSSI −45 dBm |
| 網卡 | Intel Wireless-AC 9560 160MHz |
| 通道使用率 | 0% |

RSSI −45 dBm 是「幾乎貼在路由器旁邊」的等級，通道使用率 0% 代表鄰居完全沒在干擾。兩個最常見的嫌疑犯同時出局，箭頭就指向一個問題：為什麼跑在 2.4 GHz 的 802.11n？

掃描結果只有一個網路，就是我連線的 WiFi 本身，2.4 GHz 通道 6，沒有 5 GHz 的。我進一步提供路由器型號：TP-Link TL-WR840N 以後，在 Claude 查完規格後，前面所有「去把 5 GHz 打開」的建議當場作廢：

> TL-WR840N 是 2.4 GHz 單頻路由器，根本沒有 5 GHz 電波。

規格是 2.4 GHz 單頻、802.11n、300 Mbps，WAN 埠 10/100 Mbps。於是兩道硬體天花板同時浮出來：進來的流量被 100 Mbps 的 WAN 埠卡在約 94 Mbps 實際吞吐；無線端 270 Mbps 的連線速率已經接近這台機器的滿速，802.11n 實際吞吐約為連線速率的四到五成，換算下來大概 110～130 Mbps。

## 5. 中場：打開 Computer Use，撞到一張分層的權限表

做到效能評估時，研究了一下要如何打開 Claude Desktop 的 Computer Use 模式，如果它能直接操作電腦，前面那些來回不就都省了？

結果是兩層限制連續擋下來。

第一層，它去申請 PowerShell 和終端機的操作權限，系統直接回覆：

> Terminals and IDEs can only be granted in "click" mode — you can see and left-click, but cannot type, press keys, or paste.

終端機和 IDE 只能給「點擊」等級，看得到、可以左鍵點，但不能打字、不能按鍵、不能貼上。這是刻意的設計，想想也合理：能在終端機自由打字等於拿到整台機器。所以「開了 Computer Use 就能直接下指令」這個期待，從一開始就是錯的。

第二層，它改申請事件檢視器、控制台、電腦管理這些 GUI 程式，拿到的是完整權限。視窗確實開起來了，截圖也看得到內容，但滑鼠點擊和鍵盤輸入送出去之後畫面完全沒反應。工具回報「Clicked」「Key pressed」，選單不展開、視窗不最大化，連續試了七、八次都一樣。推測是 MMC 這類系統管理主控台擋掉了外部輸入注入，但無法確定。

過程中還有幾個插曲：事件檢視器的視窗是 `mmc.exe` 承載的，而 mmc 一開始不在允許清單裡，要單獨再申請一次；有一次點擊被擋，理由是「桌面 shell 在最前面」，但視覺上事件檢視器明明蓋在最上層；還意外開了一個空白的「主控台1」視窗。

![Computer Use 操作事件檢視器的畫面](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/Computer%20Use%20Mode.png)

然後它停手了：

> 先停下來，不要繼續空轉。

![Claude Desktop 主動停手並說明兩層阻礙的對話截圖](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/Computer%20Use%20Mode%20%5B%E9%99%84%E5%9C%96%5D.png)

沒有無限重試，也沒有假裝有進展，而是把哪些是設計使然、哪些是原因不明講清楚，然後回到腳本路線。連自己誤開的那個空白視窗都主動交代我關掉。

整理起來，Computer Use 的能力邊界是分層的：

| 程式類型 | 能做的事 |
|---|---|
| 一般 GUI 程式 | 看、點、打字 |
| 終端機 / IDE | 只能看和點，不能打字 |
| 桌面 shell（檔案總管、工作管理員） | 只能點，不能打字 |

而且就算拿到完整權限，實際推不推得動還要看那個程式吃不吃外部輸入。**權限拿到不等於操作得動**，事件檢視器就是完整權限卻完全推不動的例子。

> 說明：這是在單一電腦測試的結果，不確定在其他電腦是否有同樣情況，而且目前該模式還在 Beta 版，不確定未來的更新版本與內容如何。

## 6. 電腦變慢：我的假設在第三個數字就被推翻

回到腳本。[`perf-check.ps1`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day07_20260821/perf-check.ps1) 一次撈 11 個面向，關鍵數字：

| 項目 | 數值 |
|---|---|
| 開機至今 | 8 天 14 小時 |
| 實體記憶體 | 23.8 GB（8 + 16 混插） |
| 已使用 | 17.6 GB（73.9%） |
| 分頁檔峰值 | **2263 MB** |
| Memory Compression | 1852 MB |
| chrome | **12699 MB / 73 個行程** |

Claude 指出的關鍵證據不是使用率 73.9%，而是分頁檔峰值只有 2.2 GB：

> 如果記憶體真的不夠，這個數字會是 8 GB、10 GB 起跳，所以開機這 8 天以來，系統從來沒有嚴重缺過記憶體。

這個判讀方式值得好好記下來。當下使用率是會騙人的指標，Windows 本來就會拿閒置記憶體當快取；真正反映「曾經缺過」的是分頁檔的歷史峰值，因為那是系統被逼到把資料寫進硬碟的紀錄。

它也沒有直接宣告沒事，補了一個中間狀態：Memory Compression 佔了 1.85 GB，代表 Windows 已經在壓縮記憶體頁面擠空間，還沒換頁到硬碟之程度，但也不輕鬆。

接著是我覺得整次診斷最有價值的一段，而且我根本沒問：

> 這份快照是在 CPU 10%、磁碟 1% 時抓的，也就是機器很閒的時候。它證明了「閒置時 RAM 沒問題」，但沒有抓到覺得卡的那一刻，因為間歇性卡頓要在發作當下量才有意義。

報告有 11 個章節，並且把數值都列出，讓人容易直接接受結論，指出取樣時機等於削弱自己的產出，而這是真實的情境。

## 7. 當機史：真正的兇手在一個我沒想過的地方

[`crash-check.ps1`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day07_20260821/crash-check.ps1) 用系統管理員身分跑，查 15 個面向。半年只有兩次 Kernel-Power 41，但兩次的 BugcheckCode 都是 0，`C:\Windows\Minidump` 是空的，`MEMORY.DMP` 不存在，三樣證據同時缺席，代表一次藍當機都沒發生過。

那兩次是什麼？看時間差：6/13 斷電到開機隔 89 秒，2/20 隔 58 秒。然後是這句：

> 筆電不會因為停電而斷電，它有電池。

能造成 Kernel-Power 41 的就只剩長按電源鍵，而且一分半內就開回來，是「畫面卡死、長按、立刻重開」的節奏。那兩次不是當機，是完全凍結然後我自己按掉的。一個「筆電有電池」的常識，就把電源異常和使用者強制關機分開了。

硬體也全部乾淨：WHEA 錯誤零、磁碟與 NTFS 錯誤零、記憶體傾印檔不存在。

真正意外的在這裡：

```
30 x  EventID 37    (Kernel-Processor-Power)
處理器 0 中的處理器 4 的速度受到系統韌體的限制...371246 秒
```

Event 37 是 CPU 被系統韌體限制在降低的效能狀態。累計 371246 秒等於 103 小時；對照開機時間 190 小時，**開機以來有 54% 的時間 CPU 跑在被壓低的頻率，而且八個核心全中。**

這比 Chrome 更能解釋「感覺變慢」，因為Chrome 吃的是記憶體，CPU 降頻是每一個操作都變鈍。以 2019 年的 GL65（i7-9750H）加上台灣八月的室溫來看，散熱是最可能的原因，例如七年的積灰和乾掉的散熱膏影響非常直接。 ~~可惡！其實原本真的想換電腦的，無奈計畫不及記憶體的漲價速度...~~

順帶撈出來的還有一份當機排行：Dragon Center 180 天內掛了 10 次，`CrashDumps` 裡四個 38 MB 的傾印檔全是它的，它正好是負責風扇轉速和效能模式的那支軟體。Claude 提了假設，但明確標示是推測：

> 如果 Dragon Center 在背景反覆崩潰，風扇和效能設定檔可能沒有被正確套用，韌體就會退回保守的預設值，那正好會表現成 Event 37 的降速。這兩件事同時存在，但我沒有直接證據證明因果。

把「同時存在」和「有因果」分開講，這種地方最容易被含糊帶過。

## 8. 順手清了硬碟，然後被提醒這跟慢無關

第二個問題我要的是日後備用知識：硬碟該清的時候可以刪哪裡。Claude 給的分級是綠燈隨時可刪、黃燈確認後刪、紅燈千萬別碰。紅燈區特別值得記：`C:\Windows\WinSxS` 手動刪會讓系統無法更新，正確做法是 `DISM /Online /Cleanup-Image /StartComponentCleanup`；`%APPDATA%`（Roaming）是設定與資料不是快取；`pagefile.sys` 要關是用 `powercfg -h off`，不是直接刪檔。

我跑了預估量最大的兩項，結果差很多：

```
(base) PS D:\> conda clean --all
Will remove 28 (66.6 MB) tarball(s).

(base) PS D:\> pip cache purge
Files removed: 2449 (3618.2 MB)
```

pip 清了 3.6 GB，跟預估的 3.4 GB 對得上。conda 只清了 66.6 MB，而不是預期的 6.1 GB。

> `conda clean --all` 只會刪三種東西：壓縮的 tarball、索引快取，以及沒有任何環境在用的已解壓套件。那 6.1 GB 的 `anaconda3\pkgs` 裡，絕大部分是正在被環境硬連結引用的套件，刪掉環境就壞了，所以 conda 保護它們。

所以要再清，方向在環境不在快取，而且順序不能反：先 `conda env remove -n <環境名>`，把套件變成孤兒，第二次 `conda clean --all` 才有東西可刪。

最後它補了一句：

> 這些清理跟速度問題無關。C 槽本來就剩 61%，空間從來不是瓶頸。

## 9. Anaconda：把環境裡的 Office 套件先盤點起來

接著請他幫我做一張比較表，確認我現在的 conda 環境中，有哪一些有 Office 系列的 Word, Excel, PPT。

提示詞就一句：

```
幫我研究我現在的Anaconda環境中 (C:\Users\Alex\anaconda3\envs) 有哪些裝有
python ppt, word, excel 相關套件，請製表到 <指定路徑>。
```

送出之後跳的第一件事是授權對話框，一次要兩個資料夾（來源的 `envs` 和輸出的路徑），上面寫著它為什麼要：「掃描各 conda 環境已安裝的 Office 文件處理套件，並將製作好的表格存到輸出的路徑資料夾。」下面有一個「Don't ask again for these folders on this device」的勾選框，我沒有勾。

![授權對話框](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/1-%E8%A9%A2%E5%95%8F%E6%8E%88%E6%AC%8A.png)

第二件事是它反問我要什麼格式：Excel、Markdown、HTML 表格，或是其他。我選 .xlsx。

![詢問輸出格式](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/2-%E8%A9%A2%E5%95%8F%E8%BC%B8%E5%87%BA%E6%A0%BC%E5%BC%8F.png)

這兩個互動比結果本身更值得記。**它沒有假設輸出格式，也沒有假設可以直接翻我的家目錄**，兩件事都停下來問。前面第 5 節撞到的那些限制，換個角度看就是這個東西：權限是一次一個範圍、當場申請的。

跑完回來是一個三分頁的 xlsx。它沒有去 `conda list`（那要一個環境一個環境跑），而是直接讀每個環境 `Lib\site-packages` 底下的 dist-info 目錄，一次掃完九個環境。

![環境套件總表](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/EXCEL%E8%A1%A8%E7%B5%90%E6%9E%9C%E5%88%86%E9%A0%811-%E7%92%B0%E5%A2%83%E5%A5%97%E4%BB%B6%E7%B8%BD%E8%A1%A8.png)

總表長這樣（省略了幾個相依欄位）：

| 環境 | Python | python-pptx | python-docx | openpyxl | XlsxWriter | pywin32 |
|---|---|---|---|---|---|---|
| automl_gpu | 3.10.19 | — | 1.2.0 | 3.1.5 | — | 311 |
| fmri_bold | 3.11.15 | — | — | 3.1.5 | — | — |
| **stats** | **3.13.14** | **1.0.2** | **1.2.0** | **3.1.5** | **3.2.9** | — |
| stock_tw | 3.13.10 | — | — | 3.1.5 | — | — |
| fin / stock_rating | 3.13.10 | — | — | — | — | — |
| image2ico / webp2image / test | 3.12–3.13 | — | — | — | — | — |

結論很乾脆：**九個環境裡只有 `stats` 三大套件齊全**，PowerPoint、Word、Excel 都有。

另外兩個分頁分別是套件用途說明和逐環境的安裝明細，備註欄還把兩件容易誤會的事寫清楚：`et-xmlfile` 是 openpyxl 的相依不是獨立套件；`pywin32-ctypes` 和 `win32-setctime` 名字看起來很 Windows，實際是 keyring 和 loguru 的相依，跟 Office 無關，所以沒列進表。

![套件用途對照分頁](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/EXCEL%E8%A1%A8%E7%B5%90%E6%9E%9C%E5%88%86%E9%A0%812-%E5%A5%97%E4%BB%B6%E8%AA%AA%E6%98%8E.png)

![逐環境安裝明細分頁](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/EXCEL%E8%A1%A8%E7%B5%90%E6%9E%9C%E5%88%86%E9%A0%813-%E5%AE%89%E8%A3%9D%E6%98%8E%E7%B4%B0.png)

![完成與說明](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Day07_20260821/3-%E5%AE%8C%E6%88%90%E8%88%87%E8%AA%AA%E6%98%8E.png)

這件事本身不難，難的是「我自己一直懶得做」。九個環境手動查一輪大概要二十分鐘，而且查完還是會忘。現在它變成一個檔案，等哪天真的要挑環境，開來看就好。

## 小結

要分清楚會騙人的指標跟不會騙人的指標。記憶體使用率 73.9% 什麼都證明不了，分頁檔峰值 2.2 GB 才是證據；Kernel-Power 41 只說「非正常斷電」，斷電到開機隔 89 秒才指出是人為。原始事件不會給答案，事件之間的關係才會。

另外是 CLAUDE 對自己的產出保持懷疑。主動說快照抓在閒置時、主動把相關性和因果分開、試了七八次之後主動停手，這些都不是我問出來的。比多給幾條建議有用得多。

至於「找不到可以調的東西」算不算失敗，我現在覺得不算，診斷的意義從來不只是修好它，而是停止在錯的地方浪費時間，也能夠省下對著設定畫面瞎試的時間。

最後那張 Anaconda 對照表是唯一一件當天就有明確產出的事，不過它是放著備用的。

## 參考資料

**路由器與無線網路**

- TP-Link TL-WR840N 產品規格 — https://www.tp-link.com/tw/home-networking/wifi-router/tl-wr840n/
- Intel Wireless-AC 9560 產品規格 — https://www.intel.com/content/www/us/en/products/sku/99446/intel-wirelessac-9560/specifications.html
- Microsoft — netsh 指令參考 — https://learn.microsoft.com/windows-server/networking/technologies/netsh/netsh-contexts

**Windows 診斷**

- Microsoft — Event ID 41: The system has rebooted without cleanly shutting down first — https://learn.microsoft.com/troubleshoot/windows-client/performance/event-id-41-restart
- Microsoft — Configure system failure and recovery options（Minidump 與 MEMORY.DMP）— https://learn.microsoft.com/troubleshoot/windows-client/performance/configure-system-failure-and-recovery-options
- Microsoft — 清理 WinSxS 資料夾 — https://learn.microsoft.com/windows-hardware/manufacture/desktop/clean-up-the-winsxs-folder

**Anaconda**

- conda clean 指令文件 — https://docs.conda.io/projects/conda/en/stable/commands/clean.html

**Anthropic 官方文件**

- Claude Desktop 下載頁 — https://claude.ai/download
- Anthropic — Computer use — https://docs.anthropic.com/en/docs/build-with-claude/computer-use

> 註一：本文對 Claude Desktop 與 Computer Use 的功能描述以 2026 年 8 月 21 日的產品行為為準，權限分層與可授權的程式清單日後可能改變。

> 註二：所有數值取自單一台機器（MSI GL65 9SC / Windows 11 build 26200）的單次執行，屬定性觀察，不是統計證據。換一台機器、換一個時間點量，結論可能完全不同。

> 註三：「Dragon Center 反覆崩潰導致韌體降頻」是 Claude 提出的假設，屬待確認。

> 註四：Anaconda 套件對照表是 2026 年 8 月 21 日的掃描結果，只涵蓋 `C:\Users\Alex\anaconda3\envs` 底下的環境，未包含 base 環境。

> 註五：韌體相關內容只描述我這台 TL-WR840N v6 的情況。跨硬體版本刷韌體有變磚風險，請以自己機器後台顯示的硬體版本為準。
