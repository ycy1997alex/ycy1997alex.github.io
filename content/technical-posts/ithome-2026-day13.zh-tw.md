---
title: "Day 13｜少講的需求會自己浮出來，踩過的坑留給下一版當規則"
date: 2026-08-27T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10405513)。

> 本篇階段：Prj#1 暖身專案

> 使用介面：Claude Code（via VS Code）

---

## 今天的內容簡介

[Day 11](https://ithelp.ithome.com.tw/articles/10405148) 把 `~/.claude` 底下的東西分成「圍欄」和「提示」兩類，[Day 12](https://ithelp.ithome.com.tw/articles/10405357) 替後面的股票專案鋪路。今天做三個小工具，都是我自己實際會用到的：把圖片轉成 `.ico`、把 `.webp` 轉成圖片、把 PDF 壓縮小一點好寄 Email 出去。三個全部是在 VS Code 裡開 Claude Code 做的，所以在家目錄設定好的 `~/.claude/CLAUDE.md` 與 `skills`、`rules`、`agents` 都有套用。

一開始只簡單講了需求：要能轉成 `.ico`、要把 `.webp` 轉成圖片檔、要能把 `.pdf` 壓到指定大小，流程上先寫 `測試 script` 再寫 `執行程式`，順便把環境需要的 `requirements.txt` 列出來。

image to ico 是直接把需求丟出去的。程式可以動，但沒有軟體工程架構的概念，整體看起來滿亂，不管我自己維護還是交給 AI 維護都容易出事，所以後來補上了「用 `MVP` 架構」這句提示詞。輪到 webp to image，它做出來的 UI 實在令人不忍直視，我請它重想一次，並引入 Claude 原生的指令 `/design` 幫忙設計，終於看起來順眼一些。最後是 pdf compression：指定了 `MVP` 也用 `/design` 要求先想過，結果做出來的視窗直接超出螢幕，於是又補「先讀取螢幕解析度再設計版面」，視窗範圍由左到右 3%～50%、由上到下 3%～87%，這條後來也回頭加到前面兩個工具。

三個工具都是用 Python + ttk 寫的，再用 `pyinstaller` 打包，各自搭一份 `.spec` 檔案。`.ico` 則是拿來讓程式圖示顯示在標題列、工作列，以及檔案總管和桌面上。

> 三個工具的原始碼與 `.spec` 檔請參考我的 GitHub 對應的[專案連結](https://github.com/ycy1997alex/ycy1997alex-oss-projects/tree/main/iThome-2026-Ironman/Prj_1)

---

## 1. 為什麼是這三個，而且是這個順序

| 順序 | 工具 | 功能 | 為什麼要做？ |
|---|---|---|---|
| 1 | `image2ico` | 圖片轉多尺寸 `.ico` | 方便後面打包的應用程式用 |
| 2 | `webp2image` | `.webp` 轉 PNG／JPEG／BMP／TIFF | 手上的 `.webp` 圖片可以轉成常用格式 |
| 3 | `pdf_compression` | PDF 內嵌圖片重新編碼壓縮 | 工作上常因為 Email 附件大小上限寄不出去 |

實務上後面兩個小工具的 App 圖示，的確都是拿 `image2ico` 轉出來的。

---

## 2. image2ico：第一版不給專案規則

第一句話大致是這樣：

> 我要一個 Windows 桌面小程式，把圖片轉成 `.ico`，有 GUI。先寫測試，再寫主程式。

沒講架構、沒講用哪個 GUI 套件、沒講檔案怎麼放。唯一講的是「先寫測試」，它直接生出一個 `.py`，外加一份 `test_convert.py`。所以這一版等於在全域規則底下裸奔，沒給這個專案自己的規則，但已經做出基本上能用的東西了！

### 2.1 先寫測試，因為用眼睛驗不出來

程式跑完，跳出「轉換成功」，桌面上多了一個 `.ico`，圖示看起來也對。到這裡沒有任何地方看得出問題。但那個 `.ico` 裡面有幾種尺寸、每一種是不是正方形，得把檔案打開來數才知道。

測試檔開頭就把驗收標準寫死：不論來源圖的尺寸、長寬比、色彩模式為何，輸出的 `.ico` 都必須包含 16／32／48／64／128／256 六種正方形尺寸。最後寫了六個案例，涵蓋正方形大圖、小於 256px 的小圖、非正方形長圖、調色盤模式的 GIF／PNG、根本不是圖片的檔案，以及隨附的 App 圖示。

驗尺寸時只看 `ico.sizes()` 宣告了什麼是不夠的，因為非正方形來源做出來的檔案會宣告 256 卻存成 256×128。所以測試裡多了一步，把每個 frame 真的取出來確認 `frame.width == frame.height`。這種宣告跟實際不一致的東西，最需要用測試卡住。

### 2.2 測試立刻抓到一個看不出來的錯

Pillow 寫 `.ico` 有兩個會靜默出錯的行為。一是大於原圖的尺寸會被丟掉：拿一張 100×100 的來源指定六種尺寸，實際只會寫進 16／32／48／64，`save()` 不報錯，UI 於是跟著謊報成功。二是非正方形來源會產生非正方形 frame，Windows 顯示時會變形。

修法是不要偷懶把原圖直接丟給 Pillow。Model 先把來源整理成「至少 256px 的正方形 RGBA」（EXIF 轉正、統一轉 RGBA、非正方形置中補透明邊、太小的用 LANCZOS 放大），再對每個尺寸各做一次 resize，最後重新讀回檔案驗證尺寸真的都在。

補透明邊還是裁切、放大還是直接拒絕，這是有取捨的。它給了三個選項讓我選，我選了「補透明邊 ＋ 放大」，並且要求兩種情況都要在 UI 上明講做了什麼處理。

### 2.3 MVP 不是架構潔癖

和 Claude、ChatGPT、Gemini、Grok 討論以後，決定用 Python + ttk 寫的桌面程式一律走 `MVP`，跟 Python 原生就支援的東西也比較搭（但這沒有絕對，用別種框架也沒有不行）。在 MVP 架構中，有 Model／View／Presenter 三個類別，全部寫在同一個 `image2ico.py` 裡，三百多行。單看規模是有點小題大作，但好處是 Model 不 import tkinter，所以測試可以直接拿 `IconConverterModel` 來測，不用開視窗；第 6 節那次 UI 大改，動到的只有 View 的 `_setup_ui()`，測試一個字沒改，跑完照樣六個 PASS。

---

## 3. 打包：三個專案共用的骨架

程式本體 `*.py`、打包設定 `*.spec`、應用程式圖示 `*.ico`，加上 `requirements.txt` 鎖版本和 `test_*.py` 當驗收，一個可以交出去的小工具原始碼就這五種檔案。

`.spec` 只有三段：`Analysis` 掃相依決定收哪些檔案，`PYZ` 把純 Python 模組壓成一包，`EXE` 產出執行檔。三個工具都選 onefile，啟動慢個兩三秒換「拖到隨身碟就能跑」是權衡後覺得划算的。

有一段是三個專案都必須寫的：

```python
from PyInstaller.utils.hooks import collect_data_files
ttkbootstrap_datas = collect_data_files('ttkbootstrap')
```

ttkbootstrap 2.x 的字型與圖示資產是執行時才讀的檔案，PyInstaller 的靜態分析看不到它，也沒有現成的 hook。少了這段，開發環境完全正常，打包出來的 exe 一啟動就 `FileNotFoundError` 閃退。這個坑 AI 重複踩過，所以我先把它加進我的 LESSONS.md 檔案中。

圖示則要在三個位置各自生效：標題列靠程式裡呼叫 `root.iconbitmap()`，工作列靠在建立 root 視窗之前呼叫 `SetCurrentProcessExplicitAppUserModelID()`，檔案總管裡的 `.exe` 靠 `.spec` 的 `icon=`。第二個最容易漏，不設的話 Windows 會把這支程式歸到 Python 直譯器底下，工作列上出現的是 Python 的圖示。另外 onefile 會把資源解壓到暫存目錄 `sys._MEIPASS`，所以 `.ico` 必須同時列在 `icon=` 和 `datas` 裡，程式端再判斷現在是不是 frozen 狀態：

```python
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
```

這裡刻意不用 `os.path.abspath(".")`，改用「本檔案所在目錄」，從別的工作目錄啟動也不會有找不到圖示的問題。這一段我也把它加進我的 LESSONS.md 檔案中，之後應該會透過更新 skills 或 rules 的方式避免 AI 再度踩坑。

最後，那個 `.ico` 本身必須是多尺寸的，只放一張 256px 進去，工作列的小圖示會由系統即時縮，糊得很明顯。這件事繞回上一節：所以 `image2ico` 才是三個裡最先做的那一個。

---

## 4. webp2image：背景執行緒不能碰 widget

第二個工具的第一句 prompt 就長多了，因為 image2ico 那些教訓我不想再講一次：一樣的 MVP 架構、一樣先寫測試、`.spec` 要記得 `collect_data_files`、圖示三個位置都要。

這一輪我還多加了一個動作：**先想設計，不要急著寫**。上一個工具是講完就直接開始生程式碼，這次我要求它還要先把 UI 給我看，我親眼確認過以後才動手。

這個小工具遇到的問題是：如果批次轉幾百個檔案，在 UI 執行緒裡跑，視窗會整個凍住；但 tkinter 的 widget 又不能從非主執行緒碰。Claude 給的解法是加一層佇列：

```
工作執行緒  --post(callback)-->  queue.Queue  --after 50ms 輪詢-->  UI 執行緒執行
```

這個安排順便處理「轉到一半關視窗」的狀況：先取消 `after` 輪詢，再通知執行緒停止，最後才 `destroy()`。少了第一步，視窗都關了輪詢還在跑，就會噴 tkinter callback 例外。驗收條件也把這件事寫進去：轉換途中關掉視窗必須沒有例外、沒有殘留執行緒。這條目前只能手動測。

過程中有幾個地方是它問我、我來決定的：若 `.webp` 是動畫，就只取第一幀、JPEG／BMP 的透明區域壓平成白底、單一檔案毀損只標「失敗」並繼續處理其餘的。測試從六個變成十一個，多出來的幾乎都不是「功能對不對」，而是「邊界情況會不會炸」。第一版的測試只是在確認它會動，第二版多出來的那幾個，是在確認它不會在奇怪的地方壞掉。（雖然我覺得它事後加測試，有點違反我原本預期的行為）

---

## 5. pdf_compression：檔案終於拆開了

第三個工具我講了 `MVP`，但沒講要拆成幾個檔案，結果它自己就拆了：`main.py` 組裝三層、`model.py` 放壓縮邏輯、`view.py` 處理畫面、`presenter.py` 管事件轉接與背景執行緒，測試也跟著拆成兩份。

拆開後有個顯而易見的好處：`test_presenter.py` 用 FakeView／FakeModel 取代真的 UI 與壓縮流程，完全不用開視窗就能測輸入驗證、輸出路徑組法、關閉時的取消流程。裡面有個設計很聰明：把 `schedule()` 換成只記錄不執行的假物件，測試自己手動呼叫 `_poll_queue()` 推進佇列，等於把「時間」也變成可控的變數。

功能上有一段自動收斂：輸入一個目標檔案大小，壓完還是超標就自動調降縮放比例與 JPEG 品質重試，最多八次。畫面上真正給使用者調的參數只有五個，其中「最小圖片邊長」是我後來才要求加的。第一版把頁面裡所有點陣圖一視同仁地壓，結果類似公司 logo 這種本來只有幾 KB 的小圖被壓成馬賽克，檔案大小卻幾乎沒變，壓錯對象。設一個下限之後，壓縮只會動到真正佔空間的大圖。

在打包這個小工具的時候，踩到一個大坑：打包成功，但一執行就閃退，錯誤是 `ImportError: DLL load failed while importing pyexpat`。原因是 conda 環境把原生 DLL 放在 `<env>\Library\bin`，那個目錄不在 PyInstaller 的預設搜尋路徑上，解法是在 `.spec` 的 `Analysis` 之前把它手動加進 `PATH`。除錯的關鍵動作是：`console=False` 的 exe 閃退時什麼都看不到，把 `.spec` 複製一份改成 `console=True` 再打包，錯誤訊息就整段出來了。

還有個體積問題。第一次打包出來一百多 MB，查下去發現 `pymupdf` 裡有個沒用到、以 try/except 保護的 `Table.to_pandas()`，PyInstaller 看不懂 try/except，照樣把 pandas／matplotlib／scipy 整條相依鏈收進去，在 `excludes` 排掉之後降到約 52 MB。同樣的道理在 `image2ico` 上也驗證過：乾淨環境打包是 20.5 MB，裝了 numpy 的環境則是 28.1 MB。

---

## 6. 後來追加的兩個條件

三個工具都能跑之後，我又補了兩條。UI 那條 image2ico 當初沒提，視窗大小那條則是三支都要求了。

**UI 要好看一點。** 第一版的介面很像 2005 年的東西：粗框的 `Labelframe`、標題 18 級粗體置中、按鈕是綠色的 SUCCESS 樣式。我補一句「介面再現代一點」，它調過之後是有好一點，但還是醜。最近剛好 Claude 的指令 `/design` 在社群上滿多人討論，我就把這個指令也加進需求裡，現在的介面就是這樣來的。

三支工具現在打開來的樣子：

＊image2ico 打開後的初始畫面＊
![image2ico 打開後的初始畫面](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Prj_1/image2ico/image2ico_app-view.png)

＊webp2image 打開後的初始畫面＊
![webp2image 打開後的初始畫面](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Prj_1/webp2image/webp2image_app-view.png)

＊pdf_compression 打開後的初始畫面＊
![pdf_compression 打開後的初始畫面](https://raw.githubusercontent.com/ycy1997alex/ycy1997alex-oss-projects/main/iThome-2026-Ironman/Prj_1/pdf_compression/pdf_compression_app-view.png)

**視窗大小統一。** 起因很實際：三個工具開起來大小都不一樣，有的太小要拉、有的超出螢幕下緣。我給的規格是一個比例而不是像素值：讀取螢幕解析度後，初始視窗由左到右佔 3%～50%、由上到下佔 3%～87%。

```python
sw = self.winfo_screenwidth()
sh = self.winfo_screenheight()
x = int(sw * 0.03)
y = int(sh * 0.03)
width = int(sw * 0.50) - x
height = int(sh * 0.87) - y
self.geometry(f"{width}x{height}+{x}+{y}")
```

`3%` 同時是左上角座標，視窗不貼齊邊緣；下緣停在 87% 而不是 100%，是為了避開工作列。這樣可以解決幾乎全部的超出畫面問題（用比例的好處是換一台螢幕不用改程式），不過如果螢幕真的太小，大概字還是會擠在一起。如此調整過幾輪之後，三個工具開起來用的時候終於都順我的眼了。~~雖然使用者只有我一個，我的莫名要求 xD~~

---

## 小結

三個小工具，用了不到一個小時就收工，這效率可真的是可怕，照以前的實作經驗來說，沒有個幾天是很難做好的⋯⋯

這三個小工具技術難度沒有到特別了不起，但今天讓我對 vibe coding 的想法具體了一點。比較不像是「什麼都不管讓 AI 生」，也不是「一開始就把規格寫死」，而是靠討論一輪一輪收斂：第一版因為少講，問題自己浮出來；每浮出一個就補一些條件；補到某個程度之後，這些條件穩定下來，就變成下一個專案的起手式（或是像我加入待辦的 LESSONS.md 中，有一天再來整理）。這些條件大多是過程中被問題逼出來的，事前根本想不到。與其一開始就寫一份完美的 prompt，不如接受第一版一定會爛，然後把每個踩到的坑變成下一輪的預設值。

而這個過程中，能收斂的關鍵點是：要有辦法知道自己錯了。所以「先寫測試再寫主程式」是一個重要的條件，可以在程式定案前先把明顯的錯誤攔下來。

## 參考資料

Anthropic 官方文件

- Claude Code — Extend Claude with skills — https://code.claude.com/docs/zh-TW/skills

套件與工具文件

- PyInstaller — Using Spec Files — https://pyinstaller.org/en/stable/spec-files.html
- PyInstaller — Run-time Information（`sys._MEIPASS`） — https://pyinstaller.org/en/stable/runtime-information.html
- Pillow — ICO 檔案格式支援 — https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#ico
- ttkbootstrap 官方文件 — https://ttkbootstrap.readthedocs.io/
- PyMuPDF 官方文件 — https://pymupdf.readthedocs.io/
- Python 官方文件 — tkinter — https://docs.python.org/3/library/tkinter.html

---

> 註一：本文描述的產品與套件行為以 2026 年 8 月 27 日為準。

> 註二：本文提到的「先寫測試再寫主程式」是對這三個專案的實際做法，不是對所有專案的都該這樣做。一次性的腳本不建議這樣處理。

> 註三：文中貼出的程式片段皆節錄自實際檔案，為了閱讀省略了部分註解與例外處理，完整版請看前面附的 GitHub 鏡像連結。
