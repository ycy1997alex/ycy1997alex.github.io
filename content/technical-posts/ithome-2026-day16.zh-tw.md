---
title: "Day 16｜格式定好不用動，資料變變變也沒關係"
date: 2026-08-30T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10406251)。

> 本篇階段：應用程式

> 使用介面：Claude Code（via VS Code）

---

## 前情

[Day 15](https://ithelp.ithome.com.tw/articles/10406015) 那支統計分析程式跑完，輸出裡有一份 `Analysis_Report.docx`。那份 Word 是程式自己寫的，連格式也是程式自己定的。但實務上更常遇到的是反過來：模板早就存在，公司的、老師的、客戶指定的，欄位順序、字級、色票、表格框線都不能動，真正會變的只有裡面的數字和圖。

今天三件事都繞著 Office 打轉：

- **Word**：手上有一份現成的模板，資料修正以後，能不能只換內容和圖，其他一律不動。
- **Excel**：Day 15 用的 Bolasso，中間那段 bootstrap 只花 0.07 秒就跑完，過程完全看不到。想把它攤在儲存格上，按 F9 就重抽一次。
- **PPT**：把一整疊文字檔讀完、整理成一份簡報。這件事在工作上最直接的用途是績效考核前翻半年份的週報。

三件事的共同點是：格式與規則都是既有的，會變的只有資料。

> 今天的程式碼、示範檔案可以在[今日的專案資料夾](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day16_20260830) 中獲得

---

## 1. Word：模板不動，只換資料與圖

### 1.1 先弄一份會出錯的資料

要示範「資料錯了」，得先有一份錯的資料。

拿的是 scikit-learn 內建的 Diabetes 資料集，442 位患者的年齡、BMI、血壓與六項血液指標，預測一年後的疾病進展指標。sklearn 內建的是標準化過的版本，我讓 Claude 直接抓原始未標準化的那一份，抓下來以後套進 Day 15 那支程式吃的資料格式，成為 [`Diabetes_Data_Origin.xlsx`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Diabetes_Data_Origin.xlsx)（抓取與轉檔的腳本是 [`fetch_diabetes_to_template.py`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/fetch_diabetes_to_template.py)）。

錯的那一份 [`Diabetes_Data_Wrong.xlsx`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Diabetes_Data_Wrong.xlsx) 是複製一份之後，把 `age`、`bmi`、`glu` 三欄各自獨立重排。重點在「各自獨立」：每一欄的最大值、最小值、平均數、直方圖全部原封不動，壞掉的只有「這一列的 BMI 是不是這一列的人」。

```
bmi 與 target 的相關係數：+0.586（原始） → -0.004（打亂後）
```

敘述統計看不出任何異常，開起來也是一份長得很正常的 Excel。~~這種錯誤在真實世界的成因通常叫做 VLOOKUP，但不是說不要用，只是用的時候不要弄錯造成資料整欄亂掉。絕對沒有偷臭同事 xD~~

### 1.2 用錯的資料跑一次

Bolasso 對 9 個候選變項各做 200 次 bootstrap，結果 9 個全部通過 90% 的門檻被選入，接著配適 OLS（[完整輸出資料夾](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day16_20260830/Output_Wrong)）：

- 樣本內 R² = 0.425、交叉驗證 R² = 0.404
- 只有 4 個變項達統計顯著
- `bmi` 的標準化係數 0.057、`glu` 0.046，兩個都 n.s.
- `tc` 的 VIF 是 59.5、`ldl` 39.1、`hdl` 15.5

R² 0.4 不算難看，模型整體的 F 檢定 p 值是 9.4e-47，看起來很有說服力。但 BMI 與血糖在糖尿病文獻裡是最主要的兩個預測因子，在這份報告裡卻雙雙失去解釋力，這是露出馬腳的地方，而且要先有這個背景知識才能發現。

### 1.3 資料更正，同一支程式重跑

換成沒被打亂的那份，同樣的流程再跑一次（[完整輸出資料夾](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day16_20260830/Output_Origin)），結果差很多：

| | 打亂的資料 | 更正後的資料 |
|---|---|---|
| Bolasso 選入 | 9 / 9 | 4 / 9（`bmi`、`bp`、`hdl`、`ltg`） |
| 樣本內 R² | 0.425 | 0.491 |
| 交叉驗證 R² | 0.404 | 0.483 |
| 達顯著的變項 | 4 個 | 4 個（全部） |
| 最高 VIF | 59.5 | 1.46 |
| 條件數 | 7552 | 1460 |

Bolasso 的懲罰強度 α，從 0.0436 變成 1.1186，差了 25 倍。資料錯位的時候變項之間的訊號被打散，交叉驗證挑出來的懲罰只好放到很輕，於是什麼都留下來；資料正確的時候訊號集中，懲罰可以下得很重，最後只留四個。

「選入 9 個」看起來比「選入 4 個」豐收，實際上是模型分不出誰有用。

### 1.4 模板重用

這一步是今天真正想確認的：我給 Claude 的是一份現成的 Word 模板，裡面已經有完整的排版。

它的做法是把模板檔本身當底，開檔之後清掉 body 裡的所有內容、只留 `sectPr`（頁面設定那一段），再往裡面填新的東西。這樣做的好處是頁面邊界、Heading 樣式、表格樣式都還在原地，不需要重新定義一次。圖片則是直接指向那一次分析輸出資料夾裡的 png，換一次資料就換一組圖。

比較有意思的是文字敘述的部分。第一版我讓它照著錯的資料寫，「綜合建議」那一段有三條：共線性、選入但不顯著、資料品質可疑。換成正確資料以後，這三條理應要消失兩條，所以敘述不能寫死，得由數字推導出來：

```python
if high_vif:
    bullets.append("• 共線性：...VIF 超過警戒線 10...")
else:
    bullets.append("• 共線性：所有進入模型的特徵 VIF 皆低於警戒線 10...")
```

換成正確資料重跑，那一段自己變成：

> • 共線性：所有進入模型的特徵 VIF 皆低於警戒線 10（最高 1.46），係數可各自解讀。

> • 本報告全部為相關性分析，不能解讀為因果關係。

「資料品質」那條也自己不見了，因為判斷條件是 `bmi` 與 `glu` 同時不顯著，正確的資料裡 `bmi` 是最強的那一個。

整個過程[模板檔](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Statistical%20Analysis%20Report%20%5BTemplate(FILENAME)%5D.docx)一個位元組都沒有被改到，改的只有那支填資料的程式（[`make_report.py`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/make_report.py)）。要再換一份資料，指令是 `make_report.py Origin` 換成別的名字而已。兩份報告的成品在這裡：[打亂資料版](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Statistical%20Analysis%20Report%20%5BDiabetes_Data_Wrong%5D.docx)、[更正資料版](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Statistical%20Analysis%20Report%20%5BDiabetes_Data_Origin%5D.docx)。

---

## 2. Excel：把 bootstrap 攤在儲存格上

### 2.1 為什麼想做這個

Day 15 那支程式的變項篩選是 Bolasso，中間那個 boot 就是 bootstrap：從原始樣本裡抽出一筆、記下來、再放回去，重複到湊滿一組，然後拿這一組去算一次結果；做兩百次，看哪些變項每次都活下來。

這件事在程式裡跑，看不到過程，所以拿 Excel 做一個看得見的版本：複製 `Diabetes_Data_Origin.xlsx`，加上第三個分頁 `Boostrapping`，成品是 [`Diabetes_Data_Origin_Bootstrapping.xlsx`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Diabetes_Data_Origin_Bootstrapping.xlsx)。

### 2.2 這張表在做什麼

母體是 `Data` 分頁的 442 筆資料。每一列就是一次抽樣：隨機挑一個 1 到 442 的列號，把那一筆的**整列**抄過來，然後放回去。抽 N 次，得到 N 筆重抽出來的樣本。

表格左邊兩欄是第 i 次與抽中第幾筆，右邊十一欄是那一筆的 `age`、`sex`、`bmi`⋯⋯到 `target`：

| 第 i 次 | 抽中第幾筆 | age | sex | bmi | bp | tc | … | target |
|---|---|---|---|---|---|---|---|---|
| 1 | 263 | 44 | 2 | 38.2 | 123 | 201 | … | 308 |
| 2 | 364 | 35 | 2 | 24.1 | 94.67 | 155 | … | 58 |
| 3 | 396 | 32 | 1 | 26.5 | 86 | 184 | … | 258 |

「抽中第幾筆」那欄是重點，它會出現重複的號碼，1000 次裡有列號被抽中八次。這就是「抽出放回」四個字的樣子。整列一起抄過來還有另一個意義：bootstrap 重抽的單位是「一筆樣本」而不是「一個數字」，欄與欄之間的關係會被完整保留下來，所以重抽後的資料還能拿去跑迴歸。這正是 Day 15 那支程式在 Bolasso 裡做的事。

上方是每一欄的抽樣結果與母體對照，兩兩擺在一起：

| | age | bmi | bp | tc | target |
|---|---|---|---|---|---|
| N 次抽樣平均 | 48.41 | 26.36 | 94.68 | 191.67 | 151.50 |
| 母體平均 | 48.52 | 26.38 | 94.65 | 189.14 | 152.13 |
| N 次抽樣標準差 | 13.22 | 4.38 | 13.63 | 35.75 | 75.81 |
| 母體標準差 | 13.11 | 4.42 | 13.83 | 34.61 | 77.09 |

每一欄都貼著母體跑，但兩邊永遠不會完全相等。按 F9 重算，抽樣那兩列會換一組，母體那兩列不動。「每次結果略微不同，但不會亂跑」這件事，用講的很抽象，看表格自己跳一遍就懂了。

`N` 預設 1000，右邊一顆微調按鈕可以改，範圍 100 到 2000。調小到 100，抽樣與母體的差距明顯變大；調回 2000，又貼回去，抽越多次越準，這件事跟統計上的中央極限定理有關，這邊不細講。

### 2.3 兩個實作上的取捨

**沒有用巨集。** 微調按鈕是 Excel 的表單控制項（Form control），綁一個儲存格就會動，不需要 VBA，檔案也還是 `.xlsx`，打開不會跳巨集安全性警告。代價是沒辦法做一顆「重新抽樣」按鈕，那需要巨集，所以改用 F9，反正效果一樣。

**沒有用 openpyxl。** 這個檔案是複製既有的分析檔再加分頁，原本 `Definition` 與 `Data` 兩張表的字型、填色、凍結窗格都要留著，openpyxl 存檔會掉一部分；而且表單控制項它也放不進去。所以整支腳本走 Excel COM，從 PowerShell 驅動（[`make_bootstrapping_sheet.ps1`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/make_bootstrapping_sheet.ps1)）。公式用 `FormulaR1C1` 一次填一整塊，不是一格一格寫。

還有一個地方非拆開不可：列號要獨立成一欄。如果把 `RANDBETWEEN` 直接寫進 `INDEX` 裡，十一個資料欄會各抽各的號碼，同一列拼出來的會是十一個不同人的資料，整列抄過來的意義就沒了。所以是 B 欄先抽一次號碼，右邊十一欄都照著 B 欄查值。

---

## 3. PPT：把讀過的東西變成簡報

### 3.1 先講一個工作場景

每年績效考核最花時間的通常不是寫，是回憶做了什麼。半年前那個專案到底是幾月結案的、當時擋在哪裡、後來怎麼解的，全都散在週報裡，一份一份翻回去看，一個下午就沒了。

這件事很適合丟給 Claude Code：週報就在本機資料夾裡，讓它整份讀完，抓出時間軸、關鍵決策、量化成果，直接產一份績效回顧簡報。不用一個一個上傳，不用擔心公司文件離開這台電腦，不管是二十份或兩百份，也都是同一個指令、同樣的做法。

### 3.2 今天實際跑的例子

不方便拿真的週報示範，所以換一批性質相同的檔案：[`Stock_Summary/`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day16_20260830/Stock_Summary) 裡 8/24 到 8/28 五個交易日的財經節目摘要，加上週末節目一份，每份都是當天多支節目的彙整，目標是一份 PPT，用途是上週回顧與下週判斷。

規則直接沿用 [Day 3](https://ithelp.ithome.com.tw/articles/10403572)、[Day 4](https://ithelp.ithome.com.tw/articles/10403715) 那份摘要規則書，那份規則書當初是寫給 NotebookLM 讀 YouTube 影片用的，核心幾條是：只寫來源明確講過的內容、每一條都要標明是哪位分析師講的、態度只能用「看多／偏多／中性／偏空／看空」五個詞、查不到的股名與代號一律標「待確認」、不准加入自己的判斷與建議。

這幾條原封不動拿來用，只換掉輸出載體：規則書輸出的是可以貼進 LINE 的純文字，這次輸出的是 pptx。

產出九頁：上週指數軌跡、總體環境、一週共識看多、看空與風險標的、貫穿整週的分歧、下週關鍵時程、下週判斷、資料來源與整理原則。成品是 [`Stock_Weekly_Review_20260824-0828.pptx`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Stock_Weekly_Review_20260824-0828.pptx)，另存了一份 [PDF](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/Stock_Weekly_Review_20260824-0828.pdf) 方便直接手機下載閱讀。

### 3.3 跨日比對才看得出來的東西

> 以下說明不構成投資建議，僅是對財經節目摘要的內容

單日摘要看不到的，是同一件事在六份檔案之間怎麼變的。整理完最有意思的四個：

**利率預期一週轉了兩次向。** 週初美債殖利率高檔壓抑科技股，週三財政部擴大回購、殖利率下滑，週四週五還在講「9 月大機率按兵不動」；結果週末華許在央行年會放鷹，升息機率從 35% 跳到 60%，兩年期美債殖利率跳升 11 個基點。前面四天建立起來的前提，被最後一份檔案推翻。

**貨櫃航運一週內翻面。** 8/24、8/25 林漢偉、張林忠、老王都看多，理由是塞港短期無解、低本益比高殖利率；郭哲榮同期一路看空，認為與 AI 無關。8/26 萊茵河水位回升、歐線期貨大跌，林漢偉當天「全數出清」轉為看空，跟郭哲榮、容逸燊變成一致看空。8/28 老王補上收尾：成交量從 20 萬張乾涸到 4.5 萬張、融券連四天大回補，三檔全數看空。

**欣興從單向看空長出分歧。** 8/28 兩名副總與一名會計被檢調帶走時，三位分析師一致看空，黃豐凱預估跌到 900 至 1,000 元。週末釐清是「原產地標示不實」而非做假帳，陳昆仁當場改口說週一跌停很可能是相對低點、打開跌停反而是買點；蔡明翰不同意，認為仍涉公司治理與財報可靠度。同一個事件，資訊補齊之後結論完全岔開。

**分界線是同一個數字。** 下週判斷那頁，偏多的林漢偉說跌破 46,000 點沒有破壞多方結構、拉回是低接買點；偏空的鍾國忠說指數高於 46,000 點就該把持股降到 4 成。兩個人講的是同一個位置，只是站在線的兩邊。

### 3.4 家目錄那幾個檔案有跟著生效

這是我想確認的另一件事。網頁版的 Claude 也能讀檔案做簡報，但 Claude Code 是在本機跑的，家目錄底下那些設定會一起套用：

- `~/.claude/CLAUDE.md` 的語言規則，所以簡報內文與腳本註解都是繁體中文，識別字與檔名是英文，我沒有另外交代。
- `~/.claude/rules/powershell.md` 在寫 `.ps1` 的時候自己載入了。上一節那支 Excel COM 腳本存成 UTF-8 帶 BOM，不是我提醒的。
- 專案的 `CLAUDE.md` 裡寫著 python-pptx 只裝在 `office` 這個 conda 環境，所以它直接用絕對路徑呼叫那顆 python，沒有去 `conda activate`。

最後成品 Claude 有實際看過：用 PowerPoint COM 把九頁匯出成 PNG 檢查排版，不是產完就當作好了。

### 3.5 順手抓到的一個錯，跟一個沒跑成的指令

彙整的時候發現，同一位分析師在 08/25 的來源檔裡叫「蔡明漢」、08/26 變成「蔡明翰」。這不是節目講錯，是產生那份摘要的模型自己打錯字。第一版簡報被 Claude 列成「是否為同一人待確認」，後來由我確認是同一人、正確是蔡明「翰」。

這個錯單獨看任何一天都看不出來，是把六份檔案攤在一起做跨日比對時才浮現。用弱模型產出的東西，錯誤通常不會出現在單筆結果裡，而是出現在筆與筆之間對不起來之處。

至於排版，用 Claude Code 的 `/design` 把簡報做成設計稿（九張 16:9 的 artboard，深藍主色、台股紅漲綠跌、數字走等寬字），再把同一套視覺規則直接寫進產生 pptx 的程式（[`make_weekly_ppt.py`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day16_20260830/make_weekly_ppt.py)）：每頁一條深藍標題列、白底卡片、表格深藍表頭、漲跌數字上色。設計稿檔案留在 [`design/`](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Day16_20260830/design) 底下。

---

## 討論

[Day 08](https://ithelp.ithome.com.tw/articles/10404489) 做的也是 Word、Excel、PPT 這三件事，只是那天比的是 claude.ai 和 Claude Desktop 的 Cowork mode。隔了八天，同樣三種格式換成 Claude Code 在本機再做一次，剛好可以拿來對照。

### 一次性的產出，與可以重跑的產生器

Day 08 的成品是三個檔案，這一天的成品是三支程式，檔案只是它們吐出來的東西。

Day 08 最後有一句是「真正省下的是從零排版的時間，不是檢查的時間」。這件事到今天沒有被推翻，只是位置移動了：第一次的成本反而更高，因為要多寫一支產生器；省下來的是第二次以後，資料換一份，指令只換一個字。而「綜合建議」那段敘述由數字推導、不寫死，等於把一部分檢查也塞進程式裡。

### 一邊在做模板，一邊在用模板

Day 08 那個「拿出模板」，整件事唯一需要判斷力的地方是分辨哪些內容是這趟旅行的、哪些是每趟旅行都會用到的：instance 清掉，pattern 留著。今天反過來，模板已經在手上，判斷題不存在，剩下的只有「一個位元組都不要動到它」。

兩天剛好是同一條流程的兩端。Day 08 產出的 `.dotx` 如果真的拿去用，接下來要做的就是今天第 1 節這件事。

### 同樣的坑，不同的躲法

| | Day 08（claude.ai／Claude Desktop） | Day 16（Claude Code） |
|---|---|---|
| Word | 解壓改 XML 再重打包／`python-docx` 就地改 | 以模板檔為底，清 body 只留 `sectPr` |
| Excel | `openpyxl`，公式沒有快取值 → 補一步 LibreOffice 全量重算 | Excel COM，樣式與表單控制項都留得住 |
| PPT | `pptxgenjs`（Node） | `python-pptx` |
| 目視驗證 | `soffice` 轉 PDF → `pdftoppm` 轉圖 | PowerPoint COM 直接匯出 PNG |

三個轉折其實是同一個原因：本機裝著 Office，Sandbox 裡沒有。

Excel 那格最明顯。Day 08 兩邊都踩到 `openpyxl` 寫出去的公式沒有快取值，所以流程裡非得多一步 LibreOffice 重算；今天不用 `openpyxl` 的理由不同（要保住既有分頁的字型填色，還要放表單控制項），但 COM 這條路能走，前提是這台機器上真的有 Excel。

PPT 那格是反過來的。Day 08 兩邊都避開 `python-pptx`，理由是它無法複製投影片、`text_frame.text = ` 會把段落塌成單一無樣式的 run。今天用了也沒事，因為九頁全部是程式從零建的，沒有哪一頁需要複製誰。限制還在原地，只是這次沒有走到它前面。~~不是它變好了，是我沒去碰~~

字型那件事更乾脆。Day 08 第 9 節列的「兩邊都沒解決的事」第一條就是字型算繪不可靠：Sandbox 裡只有 Noto Sans CJK，預覽看到的 fit 判斷不能信，非安全字型要多留一成空間。今天不需要解決這一條，因為匯出 PNG 的就是本機那套 PowerPoint，看到的字就是等一下會看到的字。不是被解掉的，是換了地方以後它不成立了。

### 環境知識是誰寫的

Day 08 最後一節寫兩個介面動手前都先去讀 `/mnt/skills/public/*/SKILL.md`，翻開來不是 API 教學，是這個容器的踩雷筆記，補的是環境知識，不是領域知識。

今天第 3.4 節那三件事是同一個東西的另一半。差別在誰寫的、對誰生效：`SKILL.md` 是 Anthropic 放在容器裡的，每個人開起來都一樣；家目錄和專案裡那幾份 `CLAUDE.md` 是我自己寫的，只在我這台機器上成立。前者讓 Claude 知道 Sandbox 的 LibreOffice 會怎麼壞，後者讓它知道 `python-pptx` 裝在哪個 conda 環境。

順帶把 Day 08 那個「先問，還是先做」的差異接下去：今天我沒有被問要用哪顆 python，因為答案早就寫在專案的 `CLAUDE.md` 裡。把答案寫成檔案，等於預先把題目做答完畢。

---

> 註一：本篇的分析全部是相關性分析，糖尿病資料集只用來示範報告流程，不構成任何醫療建議。

> 註二：兩次分析都是單次執行的結果，屬定性觀察；Bolasso 的選入頻率取決於 bootstrap 抽樣，換一組亂數種子接近門檻的變項可能進出。

> 註三：打亂的那份資料是我刻意做的，不是真實世界的錯誤樣本。

> 註四：第 3 節那份 PPT 的內容全部來自財經節目摘要文字檔，是節目講者說法的整理，不是我的看法，其中的指數、成交量與財務數字都沒有另外向公開資訊源查證。**本文與該份簡報均不構成投資建議。**

> 註五：「蔡明漢」與「蔡明翰」在不同日的來源裡寫法不一，經確認為同一人、正確是蔡明翰，簡報已統一。
