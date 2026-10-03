---
title: "Day 10｜每次都要重講的話，寫成檔案；這次沒做完的事，寫成一封信"
date: 2026-08-24T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10404921)。

> 本篇階段：基礎說明

> 使用介面：Claude Code（終端機 CLI ＋ VS Code 擴充套件）

---

## 前情

[Day 09](https://ithelp.ithome.com.tw/articles/10404684) 整理了 Skill：一個按需要才載入的內容，平常只有 name 和 description 待在 context 裡，符合條件才把本體叫進來。那篇最後留了一句「明天再來聊聊 CLAUDE.md」，因為 CLAUDE.md 剛好是它的反面，是每次都會載入的。

今天分三段。先把 Claude Code 裝起來，終端機和 VS Code 兩條路，順便講一個很多人第一次會誤會的地方。再來是我的家目錄那份 `~/.claude/CLAUDE.md` 到底寫了什麼、為什麼要寫，以及它跟專案自己的 CLAUDE.md 怎麼分工。

最後一段是我猶豫要不要寫的：**一封寫給下一個 session 的信。** 它跟前面兩段的性質不一樣，前面兩段講的是規則，這封信講的是狀態。規則可以一直放著，狀態放到明天就過期了。

從高中開始碰程式語言到現在，我很清楚每次做同一件事都要重新交代一遍，不是一個好習慣。LLM 時代除了記憶機制以外，還可以直接把規範寫成檔案，而在 Claude Code 裡，這件事就是 CLAUDE.md。

我的 CLAUDE.md 完整內容，可於我的 github 專案資料夾 [dotclaude](https://github.com/ycy1997alex/dotclaude) 看到。

---

## 1. 兩種安裝，而且它們不是同一件事

### 1.1 終端機 CLI

Windows 11 上最快的一條是官方安裝腳本，開 PowerShell 跑：

```powershell
irm https://claude.ai/install.ps1 | iex
```

裝完的位置是 `%USERPROFILE%\.local\bin\claude.exe`，我的電腦就是這樣安裝的，跑 `claude --version` 現在回報 `2.1.241 (Claude Code)`。另一條路是走 npm 全域安裝，需要先有 Node.js：

```powershell
npm install -g @anthropic-ai/claude-code
```

兩條擇一就好。裝完在終端機，在任何一個路徑中打 `claude` 就會進到互動模式。

### 1.2 VS Code 擴充套件

前置條件是 [VS Code 最新版本](https://code.visualstudio.com/download)，加上一個 [Anthropic 帳號](https://www.anthropic.com/)。付費訂閱（Pro、Max、Team、Enterprise）或 Claude Console 帳號都可以，準備 API key 也行。

`Ctrl+Shift+X` 打開 Extensions 面板，搜尋[「Claude Code」](vscode:extension/anthropic.claude-code)，按 Install，要注意發布者是 **Anthropic**。Cursor 這個 IDE 也可以裝同一個套件。

裝完沒出現的話，Command Palette 跑一次 `Developer: Reload Window`。第一次打開面板會出現登入畫面，點 Sign in，瀏覽器授權完會回到原本視窗。

### 1.3 一個容易誤會的地方

**裝了擴充套件不等於終端機裡有 `claude` 指令。** 擴充套件自己帶了一份私有的 CLI 給聊天面板用，但要在終端機打 `claude`，得另外裝上面 1.1 那個 standalone CLI。`claude mcp add`、`claude --resume` 這些指令也是裝完 CLI 才用得到。

反過來也一樣：先裝了 CLI 不會自動出現 VS Code 面板。兩邊各裝各的。

裝了之後兩邊是通的。在 VS Code 裡用 Ctrl 加上重音符號那個鍵開整合終端機、跑 `claude`，它會自動接上 IDE，diff 檢視和診斷資訊共享都還在，只是介面從側邊面板換成終端機。

---

## 2. 在 VS Code 裡實際會用到的東西

### 2.1 入口不只一個

擴充套件用一個 Spark 圖示代表自己，在 VS Code 各處都是同一個圖示：

1. 編輯器右上角的 Spark 圖示最快，但要有檔案打開才會出現。
2. 左側 Activity Bar 的 Spark 圖示永遠在，點開是 session 列表。
3. `Ctrl+Shift+P` 輸入 Claude Code，選 Open in New Tab 會開成一個編輯器分頁。
4. 右下角狀態列的「✱ Claude Code」在完全沒開檔案的時候也能用。
5. 按編輯器右上角的 Codex Sidebar，再選到 Claude Code 也行。

### 2.2 三個天天會用到的鍵

選一段程式碼，Claude 自動看得到，輸入框下緣會顯示選了幾行。按 `Alt+K` 可以把 `@app.ts#5-10` 這種帶行號的參照直接塞進 prompt，指得更精確。

用 `@` 開頭提及檔案或資料夾支援模糊比對，打 `@auth` 就能命中 `AuthService.ts`，資料夾記得加斜線。

`Shift+Enter` 換行不送出。prompt 會寫得長的時候很需要。

### 2.3 改動要經過同意

Claude 要改檔案的時候會開一個左右對照的 diff，然後停下來問：接受、拒絕、或者直接告訴它該怎麼改。也可以在 diff 裡先把它的內容改掉再接受，這時候 Claude 會被告知檔案被動過，不會繼續假設內容是它原本提議的樣子。

輸入框底部的模式指示器控制它有多自由：

| 模式 | 行為 |
|---|---|
| Manual | 改檔和大部分指令都要問 |
| Plan | 先講計畫、等批准才動手；VS Code 會把計畫開成一份 Markdown 讓我寫 inline comment 回饋 |
| Edit automatically | 自動編輯，不再逐次問 |
| Auto | 安全檢查通過就自動執行，有風險的事情停下來問 |

我大部分時間掛在 Auto，讓 Claude 自己選。而且這不是每次開視窗手動點的，我在 `settings.json` 裡寫了 `"defaultMode": "auto"`，開起來就是這個模式。

但「有風險就停下來問」這句話能不能算數，取決於風險的定義寫在哪裡。預設模式只決定它敢不敢自己動手，沒有決定哪些事情不准動手。

---

## 3. 為什麼需要一份全域規範

如果每一次新對話，模型都是一個沒有記憶的新同事，它讀得懂現在的程式碼，卻不知道這裡有什麼規範或慣例，那大概我會先瘋掉。

用 Claude Code 這段時間，我重複交代過的事情包含但不限於：

1. 它會寫出 bash 語法，而我在 Windows。（而且看它在那邊 retry 很耗 token）
2. 在 git 專案裡，它有時候會在做完事情之後想要 `git commit` 收尾。（這有點可怕，我得先知道它改了什麼）
3. 改一個函式的時候，把附近三個函式的命名一起「改好」。（但這常常違反我當下的要求）
4. 直接 `pip install` 進 base 環境。（然後環境就亂到不行）

這些都不是 bug，是預設值和我的習慣不一致。糾正一次的成本很低，糾正一百次我可能會想殺死自己。

`~/.claude/CLAUDE.md` 就是把「每次都要講的話」寫成檔案，每個 session 開頭自動載入。全域規範每個 session 都要付 token，所以它不能什麼都放，旁邊還有幾個鄰居分擔：按檔案類型載入的 `rules/`、按任務載入的 `skills/`、被呼叫才載入的 `agents/`，還有一個永遠不載入的收集桶。今天先把最中間那份講完，其他幾層明天一起攤開。

---

## 4. 我這份 CLAUDE.md 的章節導覽

主體結構參考了 [multica-ai/andrej-karpathy-skills 的 CLAUDE.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md)。第 1 到 4 節我幾乎原樣照抄，因為那比較像是通用的、需要給 LLM 的慣例；第 5 節之後是我自己補的安全邊界和使用習慣。

檔案開頭我先寫了一行免責：這份指引偏向謹慎而非速度，瑣碎任務用判斷力就好，第 4 節有豁免條款。還有一行更重要的，**這個檔案只由我手動修改，模型不准編輯，包含追加**，要改的話在對話裡提。

底下我用編號帶路，是為了寫文章方便。但實際上在其他規則檔裡互相引用的時候，我一律用**章節名稱**而不是編號，因為編號會在檔案被編輯的時候整排位移。

### 第 0 節：語言與環境

對話回覆用台灣繁體中文，技術名詞保留英文；程式碼註解中文或英文皆可；identifier、檔名、commit message、rule 和 skill 檔案一律英文。

一個例外寫在條文裡：當一份 skill 的主題本身就是某個自然語言（例如 `humanizer-zh-tw`，它每一條 pattern 和每個例子都是中文），那份檔案就用它處理的語言寫。

這節最後一行是「這台電腦是 Windows 11，所以不要用 Bash 指令，用 PowerShell」，直接對應第 3 節列的第一個坑。

### 第 1 到 4 節：來自 Karpathy 那份的四條

**Think Before Coding。** 不要假設，不要藏起困惑，把 tradeoff 講出來。有多種解讀就攤開來問，不要默默挑一個。

**Simplicity First。** 解決問題的最少程式碼，不要投機。沒人要求的彈性和可設定性不要加，單一用途的程式碼不要抽象。寫了 200 行而其實 50 行做得完，就重寫。

**Surgical Changes。** 只碰非碰不可的地方，只清自己弄出來的髒東西。不要順手「改善」旁邊的程式碼、註解或排版，沒壞的東西不要重構，就算它自己會用別的寫法，也照現有風格走。驗收標準很直接：每一行改動都要能追溯到我的要求。無關的 dead code 提一下就好，不要刪；但因為這次改動而變成孤兒的 import、變數、函式，要自己收掉。這節後來還補了一句：進行大量或有風險的編輯前，在 git 專案裡要先請我 commit 或 stash，不准在 repo 裡開 `.bak` 檔（會被誤 commit 進去）；不在版控裡的目錄才用 `<name>.bak`。

**Goal-Driven Execution。** 「修這個 bug」要先寫一個會失敗的測試重現它，再讓它通過；「重構 X」要求同一組測試在前後都通過。多步驟的工作要先把計畫講出來，一步一行，格式是 `1. [步驟] → verify: [檢查]`。「完成」的意思是檢查跑過而且過了，不是「程式碼看起來對」。這節有個豁免條款：單一檔案、五行以內、不影響邏輯的改動（錯字、註解、文件文字）不用寫測試，看結果就好。

### 第 5 節：什麼時候該停下來問我

資料會被刪掉或覆蓋而沒有備份路徑。兩條指令互相衝突，例如 Surgical Changes 對上一個必須動三十個檔案的需求。驗收標準沒辦法具體化（「弄好一點」），這種要跟我要一個可量測的目標；但「讓測試通過」本身已經夠具體，不用問，直接做。同一個方法失敗兩次。

最後一條我覺得最有用：**同一個方法失敗兩次，第三次不是努力不夠，是方法錯了。**

還有一條是關於品味的。命名、UX 用字、取捨這種沒有技術上贏家的決定，列出選項和代價給我看，不要自己決定。

### 第 6 節：安全與環境

不寫死、不 commit 任何密鑰。log、錯誤訊息、匯出檔、debug 輸出不能含 PII/PHI，要用匿名 ID 或遮蔽值。交付前把 debug print 移掉或用 logging level 關掉。

環境相關的三條：先確認 OS 和 shell 再組指令，Windows 就假設 PowerShell（PowerShell 5.1 的編碼陷阱另外放在 `rules/powershell.md`，只有動到 `.ps1` 才載入）。先確認 conda/venv 環境再裝東西，不要預設是 base。一個專案的 build/test/lint/run 指令第一次弄清楚的時候，就記進那個專案自己的 CLAUDE.md。

### 第 7 節：委派

為了隔離 context 才委派，不是預設行為；而且 subagent 預設在背景跑，結果會晚一點以通知的形式回來。掃很多檔案、讀長 log、跑整套測試、批次編輯，這些會把大量內容倒進主 context 的工作適合丟出去。

反過來，如果那件事需要的正是「這一輪對話累積下來的脈絡」，那就用 fork（`/subtask`）：它繼承完整歷史，又共用 prompt cache，比開一個全新的 subagent 便宜。要隔離、或要限制它只能用哪些工具的時候，才叫具名的 subagent。

三件實務上的注意事項。內建的 Explore 和 Plan agent 不會載入 CLAUDE.md 和 git status，所以關鍵限制要在委派的 prompt 裡重講一次。每一次委派要交代三件事：目標和它為什麼重要、具體的驗收標準（測試通過／檔案裡要有 X 和 Y 兩節／grep 出來零筆），還有回報格式——只要結論加 `file:line`，長輸出寫成檔案再回傳路徑。以及**驗證永遠不是自我驗證**：檔案要自己讀回來，程式碼要自己跑，高風險的判斷要找一個乾淨 context 的 agent 給第二意見。

### 第 8 節：Git

`git add`、`git commit`、`git push`、`git tag`、`git merge`、`git rebase` 這六個絕對不能自己跑。不是任務做完可以跑，不是 diff 看起來乾淨可以跑，也不是它自己提的計畫最後一步可以跑。這六個同時寫在 `settings.json` 的強制確認清單裡，不管在哪一種權限模式下都會跳出來問，所以這節還多寫一句：預期會跳，不要想辦法繞過。唯讀的 `status`、`diff`、`log`、`show`、`branch --list` 隨時可以跑。

看起來該 commit 的時候，講一句話然後停下來。跑 `/git-commit` 那個 skill 是允許也是預期內的，它負責把訊息寫好，再把 `add` → `push` 的指令原樣列出來給我看——列出來是它的交付物，跑是我的事。

這節的由來值得單獨講，放在本篇後面章節。

### 第 9 節：記憶與維護

Auto memory（`~/.claude/projects/<project>/memory/`）預設開啟，放專案範圍的學習，邊做邊維護，我用 `/memory` 稽核，這裡的東西不要在別處重複記一次。`LESSONS.md` 放在這份檔案旁邊，是這個目錄裡唯一允許模型追加的檔案，只收跨專案才成立的教訓，格式一行一條：`- [YYYY-MM-DD] symptom → proposed global rule`，檔案不在就自己開一份；當一條專案範圍的教訓後來發現換個專案也成立，就提上來這裡。它**永遠不會被載入任何 session**，超過大約十行要提醒我。skill、rule、agent 檔案（`~/.claude/skills/*/SKILL.md`、`~/.claude/rules/<topic>.md`、`~/.claude/agents/*.md`）模型可以提修改建議，但要我在對話裡明確同意才准動手。

最後一條是：**context 快耗盡的時候要立刻停止產出**，把沒做完的事寫成一封信交給下一個 session。包含 3 到 5 件我沒問過但它認為這個環境最重要的事，加上它判斷這套設定最可能怎麼跑歪、要怎麼防。這封信只在 5 小時額度快撞到 context 上限的時候才寫，平常工作不觸發。

---

## 5. 全域 vs 專案：同一個機制的兩層

`~/.claude/CLAUDE.md` 管的是「我這個人怎麼工作」，專案根目錄的 `CLAUDE.md` 管的是「這個專案是什麼」。載入順序是 user 先、project 後，所以專案規則優先權比較高。

分界線我用一個問題判斷：**換一個專案，這句話還成立嗎？**

- 「Windows，用 PowerShell」，換專案還成立，放全域。
- 「這個資料夾不是 git repo」，只有這裡成立，放專案。

順帶一提，還有第三層：`~/.claude/projects/<project>/memory/`，那是 Claude 自己寫給自己的。CLAUDE.md 是我寫給它的規範，auto memory 是它整理出來的專案知識。

---

## 6. 第一條規則是怎麼長出來的

第 8 節那條「不准自己 commit」不是抄來的，是撞來撞去撞出來的。

實際發生的是：模型做完一個修改，覺得應該收個尾，就 commit 了。那個 commit 訊息不是我要的寫法，而且內容也不是我認為到了該 commit 的節點。要補救不難，重點是它每次都還會再這樣搞。

所以我學到的第一件事是：**要把「為什麼」寫進規則，而不只是寫「不要 commit」。** 一條帶著代價說明的規則，在壓力或限制下還會被遵守；一條光禿禿的 MUST，只會被遵守到它變得不方便為止。第 8 節因此不是一句禁令，而是把三種它會自我合理化的情境（任務做完了、diff 很乾淨、這是我自己計畫的最後一步）逐一堵掉。

第二件事是：**不要只靠文字。** `settings.json` 裡的 `permissions.ask` 是 harness 層級的攔截，不管模型怎麼想都會跳確認。文字管的是它的意圖，設定管的是它的權限，兩層都要設計。這部分明天會整個攤開。

### LESSONS.md 這個緩衝層

不是每次踩到的坑都值得寫進全域 CLAUDE.md。全域規範每個 session 都在燒 token，什麼都往裡面塞，重要的規則就被稀釋了。

我的做法是在中間放一個 `~/.claude/LESSONS.md`，它是這個目錄裡唯一允許模型自己 append 的檔案，而且只能寫跨專案會成立的教訓。格式一行一條：

```
- [YYYY-MM-DD] symptom → proposed global rule
```

關鍵在於：**這個檔案不會被載入任何 session。**

所以往裡面寫東西，行為上什麼都不會改變。它是一個零風險的收集桶，模型可以隨時丟進觀察到的問題，不會意外改變自己的行為，也不會偷偷佔掉我每個 session 的 context 預算。

真正的改變時機是我隔一陣子讀一次 LESSONS.md，然後決定每一條要升級成 CLAUDE.md 的規則、寫成一個 skill、變成一份 rules、或者刪掉（那其實只是那次的巧合）。規則裡還寫了超過大約十行 Claude 就要提醒我，免得它默默長成一份沒人讀的雜記，~~比深宮怨婦還可憐~~。

這個流程解決的其實是一個信任問題。我不想讓模型自己改那份每個 session 都會載入的規範，但我也不想因為這樣就把它觀察到的東西丟掉。把「記錄」和「生效」拆成兩個步驟，是我目前想到最低風險的作法，也順便迴避了網路上常見的那個問題：CLAUDE.md 無止盡地越寫越長。每次更新的時候我也會回頭查，看看有沒有哪幾條現在可以刪掉，**CLAUDE.md 不是只會增加，它也需要減少。**

---

## 7. 寫給下一個 session 的一封信

### 7.1 規則管不到的那一類東西

前面講的都是規則：這台是 Windows、不准自己 commit、改動要外科手術式。規則的特性是它一直成立，所以適合放進每個 session 都會載入的檔案。

但還有一類東西不是規則，是**狀態**：這件事做到哪、下一步是什麼、為什麼上一個決定是那樣決定的。狀態放到明天就過期了，寫進 CLAUDE.md 只會變成錯誤資訊。

而 session 一定會斷。長對話會 `/compact`，視窗會被關掉，額度會用完，或者單純是今天太晚了明天再說。斷掉之後，Claude 手上那份「我們現在進行到哪」就沒了。

**在 session 有可能中斷之前，讓它把現況寫成一份落地的檔案**，檔名 `LETTER_TO_FUTURE_SESSIONS.md`，放在專案根目錄。

### 7.2 這跟 auto memory 不一樣

這點值得說清楚，因為兩者很容易混：

| | auto memory | 交接信 |
|---|---|---|
| 誰寫 | Claude 自己 | Claude 寫，但由我指定時機與格式 |
| 位置 | `~/.claude/projects/<專案>/memory/` | 專案根目錄，跟程式碼放一起 |
| 何時載入 | 每個 session 自動 | 我叫它讀才讀 |
| 內容性質 | 長期成立的**知識** | 有時效的**狀態** |
| 過期後 | 應該更新或刪掉 | 直接被下一封覆蓋 |

「這個專案的評分規則以 Pseudocode 那份文件為唯一真相來源」是知識，該進 memory。「第 15 項文件更新還沒做，因為使用者說要等他驗收完」是狀態，該進交接信。

### 7.3 實際長什麼樣

那封信的骨架是這樣（以某次為例）：

```markdown
# LETTER TO FUTURE SESSIONS

> 2026-07-31｜Statistics Analysis Tool — 14 項潛在問題修正

## 現況：程式碼修改已全部完成並驗證通過，只剩「3 份文件更新」未做
（使用者明確指示先不要更新文件，等他驗收測試後再說。所以下一步不是繼續改程式，而是等使用者回報驗收結果。）

## 已完成（14/14，皆已實跑驗證）
| # | 內容 | 主要檔案 |

## 第二輪修正（同日，使用者驗收後回報的 6 項）
## 第三輪修正（同日，第二次驗收後回報的 5 項）

## 未完成：第 15 項 — 三份文件更新（等使用者驗收後才做）
（列出每一份文件要改的具體段落）

## 環境與驗證方式
（conda 環境路徑、兩條實際可跑的指令、GUI 為何無法在無頭環境測試）

## 備份
（修改前的完整原始碼備份在哪個資料夾）
```

有幾個段落是我覺得建議要寫的：

**「現況」放在最前面，而且第一句要講下一步不是什麼。** 那次的第一句是「下一步不是繼續改程式，而是等使用者回報驗收結果」。接手的 session 最容易做錯的事情就是熱心地繼續往前做，先把煞車寫上去比較安全。

**「未完成」要跟「已完成」一樣詳細。** 已完成的部分其實 git log 也看得出來，未完成的部分才是只存在於上一段對話裡的東西。

**要寫「為什麼」，不只是「做了什麼」。** 那封信裡有一段標題叫〈為什麼第 1 項不能只靠「每類 ≥ 折數+1」的算式〉，講的是 sklearn 的 `train_test_split(stratify=)` 會先對測試集總筆數取 ceil、再用 `_approximate_mode` 分配名額，餘數會多塞給某一類，於是實測 4 類各 6 筆時測試集是 5 筆而非 4 筆。結論是**算式判定可行、實際不可行**。

這一段是整封信裡最值錢的。沒有它，下一個 session 幾乎一定會提議「用算式判斷就好了啊，何必實際跑一次」，然後把那個 bug 再帶回來一次。

**「環境與驗證方式」直接給可以複製貼上的指令。** 那封信裡是兩條：一條跑訓練（約 10 分鐘），一條跑推論。還有一句「GUI 無法在無頭環境測試（會開真實視窗並卡住），Presenter 邏輯改用 stub View 測試」。少了這句，接手的 session 大概會先在無頭環境裡卡上一輪，才發現那個視窗根本開得起來、只是不會結束。

### 7.4 什麼時候寫

我的觸發時機有四個：

1. 對話快要 compact 之前（context 剩下不多的時候）
2. 一個階段做完、要等我驗收的時候
3. 收工前
4. 任何我準備要換一個新 session 繼續的時候

寫的成本很低，就一句「把現在的狀態寫成 LETTER_TO_FUTURE_SESSIONS.md」。它會被下一封整份覆蓋，所以不需要維護，也不會像 CLAUDE.md 那樣越長越肥。

---

## 小結

今天做完的事情其實只有三件：把 Claude Code 從終端機和 VS Code 兩邊裝起來，把「每次都要重講的話」變成一個檔案，把「這次沒做完的事」變成另一個檔案。

裝的部分唯一要記住的是擴充套件和 CLI 是兩份東西，各裝各的，裝完會互通。

檔案的部分，同樣是「寫給未來的 Claude」，載入時機差很多：

| 檔案 | 何時載入 | 放什麼 |
|---|---|---|
| `~/.claude/CLAUDE.md` | 每個 session | 我這個人怎麼工作 |
| `<專案>/CLAUDE.md` | 在該專案的每個 session | 這個專案是什麼、環境長什麼樣 |
| `~/.claude/projects/<專案>/memory/` | 每個 session（它自己寫的） | Claude 整理出來的專案知識 |
| `LETTER_TO_FUTURE_SESSIONS.md` | 我叫它讀的時候 | 有時效的進度與狀態 |
| `~/.claude/LESSONS.md` | 永不載入 | 還沒決定要放哪的觀察 |

如果要給一個寫 CLAUDE.md 的起手式：**不要一開始就抄一份長的。** 我建議先拿第 1 到 4 節那四條通用原則，然後等到發現自己第三次~~絕對不是我的耐心有限 (?)~~在打同樣的提醒，那句話就是第五條規則。

今天欠了兩筆帳：`settings.json` 那層真正的圍欄，還有那些「不是每次都要載入」的檔案到底怎麼分工。明天會把家目錄那個 `.claude` 整個拆開，裡面除了 skill 資料夾、還有 rules 和 agent 資料夾。

## 參考資料

Anthropic 官方文件

- Claude Code — Set up Claude Code — https://code.claude.com/docs/zh-TW/setup
- Claude Code — Claude Code in VS Code — https://code.claude.com/docs/zh-TW/vs-code
- Claude Code — Manage Claude's memory — https://code.claude.com/docs/zh-TW/memory
- Claude Code — Extend Claude with skills — https://code.claude.com/docs/zh-TW/skills
- Claude Code — Settings — https://code.claude.com/docs/zh-TW/settings

其他參考

- multica-ai/andrej-karpathy-skills 的 CLAUDE.md — https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md
- VS Code 下載頁 — https://code.visualstudio.com/download

---

> 註一：本文對 Claude Code 的功能描述以 2026 年 8 月 24 日的產品行為為準，CLI 版本為 2.1.241。安裝路徑、擴充套件介面、模式名稱與各項預設值日後都可能改變，以官方文件為準。

> 註二：第 1.1 節的兩條安裝指令中，我實際使用的是 PowerShell 安裝腳本那條，`.local\bin\claude.exe` 的位置是在我這台機器上確認的；npm 那條我沒有實際跑過，僅依官方文件列出。

> 註三：第 4 節是我自己那份 `~/.claude/CLAUDE.md` 的導覽，不是官方建議的模板。它是照著我踩過的坑長出來的，直接照抄到別人的環境不一定有意義。

> 註四：第 6 節「模型自己 commit」是我遇到的單次經驗與後續的重複發生，屬定性觀察，不代表所有模型或所有版本都會如此。

> 註五：第 7 節的交接信範例來自另一個專案於 2026 年 7 月 31 日的實際檔案，內容經過節錄，環境路徑已略去。它是我自己的作法，不是官方機制，官方沒有名為「交接信」的功能。
