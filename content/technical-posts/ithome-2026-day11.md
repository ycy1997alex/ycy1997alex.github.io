---
title: "Day 11｜規則擋不住的交給圍欄，每次用不到的別讓它進來"
date: 2026-08-25T00:00:00+08:00
authors: ["Alex Yu"]
series: ["iThome 2026 Ironman"]
tags: ["Claude", "iThome"]
summary: "拆開 ~/.claude：settings.json 是唯一真正擋得住操作的圍欄，Skills、Rules、Agents 則是依需要才載入的 context，各自該放什麼。"
description: "拆開 ~/.claude：settings.json 是唯一真正擋得住操作的圍欄，Skills、Rules、Agents 則是依需要才載入的 context，各自該放什麼。"
---

> **This post is in Traditional Chinese Only.**

> Originally published on [iThome 2026 Ironman Contest](https://ithelp.ithome.com.tw/articles/10405148).

> 本篇階段：基礎說明

> 使用介面：Claude Code（終端機 CLI ＋ VS Code 擴充套件）

---

## 前情

[Day 10](https://ithelp.ithome.com.tw/articles/10404921) 把 `~/.claude/CLAUDE.md` 攤開講了一遍，也欠了兩筆帳：`settings.json` 那層真正的攔截，還有那些「不是每次都要載入」的檔案怎麼分工。

今天把家目錄那個 `.claude` 整個拆開。裡面除了昨天講的 CLAUDE.md，還有 skill、rules、agent，以及一份 `settings.json`。它們常常被混在一起討論，但**生效方式完全不同**。

先說結論：這四樣東西只有一樣真的擋得住事情，其他三樣都只是很強的建議。

---

## 1. 先把這些東西分成兩類

Claude Code 的文件對 rules 有一句話講得很直白：

> 這些是 **context，不是被強制執行的設定**（context, not enforced configuration）。

CLAUDE.md 和 rules 都是以 **system prompt 之後的 user message** 形式送進對話的，不是 system prompt 本身。所以它沒有嚴格遵循的保證，只是很強的建議。

我把家目錄裡的東西擺成兩個軸來看：

| | 我寫的 | Claude 寫的 |
|---|---|---|
| **提示（可能不被遵守）** | `CLAUDE.md`、`rules/*.md`、`agents/*.md` 的 prompt、`skills/*/SKILL.md` | auto memory |
| **圍欄（無論如何都擋）** | `settings.json` 的 `permissions`、hooks | 無 |

昨天那條「不准自己 commit」我寫在 CLAUDE.md 第 8 節，同時也寫進 `settings.json` 的 `permissions.ask`。當時說「文字管的是它的意圖，設定管的是它的權限」，今天先從擋得住的那一層開始。

**判定標準很簡單：需要無條件擋下某個動作時，一定要寫在 `settings.json` 的權限規則或 hook。寫在 CLAUDE.md 裡是擋不住的。**

---

## 2. settings.json：唯一擋得住事情的那一層

### 2.1 它不是必要檔案

`~/.claude/settings.json` 完全選用，沒有它 Claude Code 一樣正常運作，所有設定走預設值，多數欄位其實是跑 `/config` 由 CLI 自動寫入的，不一定要手刻。

### 2.2 作用域與優先序

| 作用域 | 位置 | 影響範圍 | 進 git |
|---|---|---|---|
| Managed | 系統層 `managed-settings.json` | 整個組織或整台機器 | 由公司 IT 部署 |
| User | `~/.claude/settings.json` | 我，跨所有專案 | 否 |
| Project | `.claude/settings.json` | 此 repo 所有協作者 | 是 |
| Local | `.claude/settings.local.json` | 我，僅此 repo | 否（自動 gitignore） |

優先序由高到低是 Managed、命令列參數、Local、Project、User。

**但 `permissions` 是例外：它跨作用域合併，不是覆蓋。** 各層的 `allow` / `deny` 會疊加生效，而且 `deny` 優先於 `allow`。權限規則的評估順序是 deny → ask → allow，第一個命中的規則決定結果，與規則的精確度無關。

還有一個嚴格度差異值得記：Managed 設定「寬容解析」，單一壞條目被丟棄並記警告，其餘照常執行；User / Project / Local 設定則是**驗證失敗整份拒絕**。所以手改自己的 settings.json 打錯一個逗號，是整個檔案不生效，不是那一行不生效。

### 2.3 我的 settings.json

不長，全文如下：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "cleanupPeriodDays": 21,
  "attribution": { "commit": "", "pr": "" },
  "permissions": {
    "defaultMode": "auto",
    "allow": [
      "Bash(git status)", "Bash(git status *)",
      "Bash(git diff)", "Bash(git diff *)",
      "Bash(git log)", "Bash(git log *)",
      "Bash(git show *)",
      "Bash(git branch --list)", "Bash(git branch --list *)"
    ],
    "ask": [
      "Bash(git add)", "Bash(git add *)",
      "Bash(git commit)", "Bash(git commit *)",
      "Bash(git push)", "Bash(git push *)",
      "Bash(git tag)", "Bash(git tag *)",
      "Bash(git merge)", "Bash(git merge *)",
      "Bash(git rebase)", "Bash(git rebase *)"
    ]
  },
  "model": "opus",
  "effortLevel": "high",
  "autoUpdatesChannel": "latest",
  "theme": "dark",
  "agentPushNotifEnabled": true
}
```

幾個說明：

`$schema` 那行讓 VS Code 幫我做自動完成和即時驗證。已發布的 schema 更新有延遲，最新版 CLI 的新欄位可能被誤報警告，那不代表設定無效。

`defaultMode` 設成 `auto`，就是昨天第 2.3 節那個模式指示器的預設值。它管的是「沒有規則命中的時候，Claude 敢不敢自己動手」，而不是「哪些事情不准做」。這兩件事分開很重要：把預設模式調鬆並不會讓下面的 `ask` 失效，反過來，把預設模式調到最嚴，遇到沒被列進 `allow`／`ask`／`deny` 的動作也只是多跳一次確認，不是永久擋死，真的要無條件擋住，還是得靠 `deny`。

`allow` 和 `ask` 兩個清單，就是昨天第 8 節那條規則的另一半。唯讀的 git 指令進 allow，不跳確認；寫入操作進 ask，**在每一種權限模式下都會跳確認**，包含我平常掛的 Auto。

這份清單裡最後補進來的是 `git add`。它本身不會產生 commit，我原本覺得寫成禁令太重，只放在 `settings.json` 就好：**不是不准做，是做之前讓我看一眼。** 但它會改變 index，而 index 一旦被動過，我下一次看 `git status` 的 mindset 就跟事實對不起來了，所以後來 CLAUDE.md 第 8 節也把它列進去。**現在兩邊是同一組六個動作**，第 8 節甚至直接寫明這六個在每一種權限模式下都會跳確認，預期會跳，不要想辦法繞過。讓提示層和圍欄層講同一句話，比刻意留一格落差好記。

我用的是 `ask` 而不是 `deny`，因為我要的不是把路徑整條封死，而是「動手前讓我看一眼」，在 `/git-commit` 印出指令之後，是我自己貼上去執行，`ask` 剛好卡在這個節點上，不擋流程，只擋自動執行。連這個機會都不想留，才用 `deny`。

`attribution` 兩個空字串是把 commit 和 PR 的自動署名關掉。`model` 和 `effortLevel` 是我預設 model 與 effort，注意 `effortLevel` 接受 `low` / `medium` / `high` / `xhigh`，**不接受 `max`**。

### 2.4 一個很常見的地雷

有幾個鍵**不屬於 `settings.json`**，寫進去會觸發 schema 驗證錯誤，它們住在 `~/.claude.json`：

`autoConnectIde`、`autoInstallIdeExtension`、`externalEditorContext`、`permissionExplainerEnabled`、`teammateDefaultModel`、`workflowSizeGuideline`。

`~/.claude.json` 同時也存放 OAuth session、user/local 範圍的 MCP server 設定、各專案狀態與快取。專案層的 MCP server 則獨立放在 `.mcp.json`。

搞不清楚哪個設定生效的時候，`/doctor` 或 `claude doctor` 會列出解析後的設定、被丟棄的條目，以及它們來自哪個檔案的哪個欄位。

必須在特定時間點執行的事（每次 commit 前、每次編輯後）也不該寫在 CLAUDE.md，那要寫成 **hook**，同樣是 harness 層級。

---

## 3. 剩下的都是 context，所以它們比的是「什麼時候才進來」

圍欄講完了，剩下三樣（skills、rules、agents）加上昨天的 CLAUDE.md，全部都只是 context。既然約束強度都一樣，它們真正的差別就只剩一個：**什麼時候被載入，以及那個時機要付多少代價。**

### 3.1 四層載入機制

| 層級 | 檔案 | 載入時機 | 代價 |
|---|---|---|---|
| 永遠在 context | `CLAUDE.md` | 每個 session、每個專案，開場即載入 | 每次對話都付 token |
| 命中檔案類型才載入 | `rules/*.md` | 該次任務碰到符合 `paths:` glob 的檔案時 | 只在相關時付費 |
| 命中任務才載入 | `skills/*/SKILL.md` | `description` 與請求相符，或我打 `/<name>` | 只有 description 常駐，body 按照需求載入 |
| 被呼叫才載入 | `agents/*.md` | 主 session 用 Agent tool 指定 `subagent_type` | 獨立 context，不污染主對話 |

skill 的觸發方式其實有兩種：預設靠 description，但也可以像 rules 一樣加 `paths:`，改成碰到符合的檔案才載入。

skill 內部另外還有一層：`references/`。SKILL.md 的 body 在任務命中時整份載入，`references/` 只有在 body 明確指示「什麼時候該讀它」的時候才被讀進來。我目前的 skill 裡只有 `officecli` 用到，它把 elements、watch-marks、batch-raw 三份參考拆出去。

### 3.2 後來我把它整個變成一個 repo

一開始這些檔案就是散在家目錄裡，改到後來我發現一件事：**我在維護它的方式，跟維護一個專案沒兩樣。** 有目錄結構、有分類原則、有改完要跑的檢查、還有中英文兩份。所以乾脆把它抽成一個 repo，要部署的話就是把檔案複製回家目錄。

對應關係長這樣：

```
dotclaude/                      ~/.claude/
├── CLAUDE.md          ──────►  ├── CLAUDE.md       全域準則，一律載入
├── settings.json      ──────►  ├── settings.json   權限 / 模型 / 清理週期
├── rules/             ──────►  ├── rules/          paths: glob 命中才載入
├── skills/            ──────►  ├── skills/         description 命中或 /<name>
│   └── synced/        ──╳───►  │                   （帳號端備份，不部署）
└── agents/            ──────►  └── agents/         subagent_type 指定才載入
```

部署時只搬 `rules/`、`skills/`（可排除 `synced/`）、`agents/` 與根目錄那幾個檔案。

覆蓋 `settings.json` 的時候要特別小心，它是**整份覆蓋不是合併**，`permissions` 區塊先手動比對過再蓋。

### 3.3 改完之後要跑的檢查

這是把它當專案維護之後才長出來的東西。既然沒有測試框架也沒有 lint，檢查就得自己列：

1. **格式** 依 `rules/markdown.md`：每個段落一個實體行、每個區塊前後各空一行、檔尾有換行、無 BOM、無行尾空白。
2. **章節引用**：檔案裡每個 `(global: X)`（指回 CLAUDE.md 某一節的寫法，第 6.5 節有實例）都要對得上 CLAUDE.md 現有的章節名稱。這是為什麼引用一律用名稱不用編號，編號被改了不會有人發現，名稱被改了這個檢查會抓到。
3. **frontmatter 逐欄對照**：人工檢查。
4. **實際觸發**：用「使用者真的會怎麼打」的兩三句 prompt 試跑。
5. **設定生效**：跑 `/status`、`/model`、`/effort` 核對是否與 `settings.json` 一致。

第 3 條為什麼是人工檢查，值得單獨拉出來講。`claude plugin validate --strict` 通過**不能**證明欄位有效：它只型別檢查 `description`、`name`、`allowed-tools`、`metadata`、`shell` 五項，對不認得的欄位一律靜默忽略，而且完全不掃 `rules/`。

換句話說，**一個拼錯或放錯位置的 frontmatter 欄位，會坐在那裡看起來一副設定好的樣子，然後什麼事都不做。** 而且驗證工具會跟我說沒問題。這比報錯難查得多。

---

## 4. Skills：八個資料夾，只有兩個帶額外欄位

Day 09 講了 Skill 的機制，這裡補上實物。`~/.claude/skills/` 底下是我自己寫的八個，加一個 `synced/`。

| Skill | 觸發方式 | 額外 frontmatter |
|---|---|---|
| `git-commit` | description 命中，或手動 `/git-commit` | 無 |
| `humanizer` | description 命中（編修英文文稿） | 無 |
| `humanizer-zh-tw` | description 命中，或手動 `/humanizer-zh-tw` | `argument-hint`、`context: fork`、`background: false`、`model: sonnet`、`effort: high` |
| `officecli` | description 命中（Office 檔案） | 無；含 `references/` |
| `python-plot` | description 命中（畫圖、存圖、調圖） | 無 |
| `python-ui` | `paths: **/*.py`、`**/*.spec` | `paths` |
| `readme` | description 命中（寫或更新 README） | 無 |
| `ui-project` | description 命中（UI_README / 使用者指引 / 打包） | 無 |

八個裡面只有兩個帶額外欄位，其餘一律只有 `name` 和 `description`。這不是懶，是規則：**省略就是繼承 session 設定，寫一個跟預設一樣的值只會多一行要讀的字。** 要覆寫就得在同一份檔案裡寫下理由。

### 4.1 覆寫的代價在 fork 與 inline 之間差很多

`humanizer-zh-tw` 是唯一一個五個欄位一次上的。它的理由寫在檔案裡：改寫文字是量大但判斷單純的工作，模式清單就在那裡，逐條比對後重寫，不需要跨模組推理，所以 `model: sonnet` 加 `effort: high` 用較低的單位成本換足夠的文字判斷力。

真正關鍵的是後半句：**因為它是 `context: fork`，這組覆寫只作用在 fork 內部。**

這件事我很晚才想通。inline skill 的 `model:` 覆寫會改掉**整輪對話**的模型，包含 skill 步驟前後那些跟它無關的工作；forked skill 的覆寫只影響 fork 自己。所以同樣一句 `model: sonnet`，在 fork 上很便宜，在 inline 上很貴。

推論很直接：**與其把一整輪降級，不如把那個 skill 改成 fork。** 我現在的做法是，只要一個 skill 想覆寫模型，就先問它能不能 fork。

`background: false` 也是刻意的。這個欄位**只在 `context: fork` 下有效**，inline skill 上它是個無效欄位，卻會讓人以為設定了某個從來沒生效的行為（就是第 3.3 節那個「看起來設定好了其實什麼都沒做」的實例）。設 `false` 是讓呼叫端等結果並直接顯示在對話裡，而不是丟回一則任務通知，因為潤稿的產出是要當場看的。

還有一個坑：forked skill 看不到主對話歷史。所以 `humanizer-zh-tw` 的 body 第一句就寫明「待處理的文字必須由參數直接帶入，或給一個檔案路徑讓它自己讀」。純指引型的 skill 被 fork 之後會空手而回，它必須自己說清楚輸入從哪來。

### 4.2 `python-plot` 為什麼刻意不用 `paths:`

`python-ui` 帶 `paths: **/*.py` 和 `**/*.spec`，`python-plot` 沒有，兩個都是 Python 相關的 skill，這個不對稱是想過的。

帶 `paths:` 的 skill 多一道限制：**它只有在模型實際碰到符合的檔案之後才會載入**，開場的 skill 清單裡根本看不到它。這適合「一定是從既有檔案開始」的任務，改 tkinter 視窗一定有一個 `.py` 在手上，所以 `python-ui` 用 `paths:` 沒問題。

但畫圖不是。「幫我畫一張折線圖」這句話出口的時候，手邊常常一個檔案都還沒有。如果 `python-plot` 帶了 `paths:`，這種請求永遠不會觸發它。所以它改靠 description 觸發，把「畫一張圖」「圖太醜幫我調一下」「存成圖檔」這些人真的會打的字直接寫進 description 裡。

### 4.3 三組成對關係

**`readme` 和 `ui-project` 原本是同一個 skill，後來拆開。** README 規則適用於每一個專案，UI_README.html 和 PyInstaller 打包只適用於 App 專案。觸發條件不同卻綁在一起，結果是寫一份 README 也要被迫載入整套打包規則。

**`python-ui` 是下位層，`ui-project` 是上位層。** `.ico`、`sys._MEIPASS` 這些規則只寫在 `ui-project`，`python-ui` 指過去而不重抄，並且在開頭要求兩個一起載入。

**`humanizer` 處理英文、`humanizer-zh-tw` 處理中文，兩邊的 description 互相指路。** 這是為了避免同一個請求兩邊都半觸發。規則裡有一條寫得很重：兩個 skill 覆蓋同一塊地，比一個長 skill 更糟，因為兩個都會半觸發。

### 4.4 `git-commit` 只印指令，不執行

這個 skill 的定位寫在它 description 的最後一句：組出訊息並印出指令是它的產出，**指令由使用者親自來跑**。

規則裡寫死：skill 永遠不指示 `commit`、`push`、`tag`、`merge`、`rebase`，不能當收尾步驟，不能當清理動作，它可以準備好一則 commit 訊息然後停在那裡。

所以昨天那條規則現在有三層：CLAUDE.md 第 8 節說服它的意圖，skill 的授權設計限制它的產出形態，`settings.json` 的 `ask` 收掉它的執行權限。三層都指向同一件事。

### 4.5 那個我沒建立的 `synced/` 資料夾

`~/.claude/skills/` 底下有一個我沒有建立過的 `synced/`，裡面七個資料夾（`docx`、`pdf`、`pptx`、`xlsx`、`skill-creator`、`import-memory`、`morning`），還有一份 `manifest.json`。

打開 manifest 看，每一筆都帶著 `source` 欄位，值是 `anthropic` 或 `anthropic-example`，另外還有各自的 `updatedAt`。換句話說，這些是從我的 Claude 帳號同步下來的官方 Skill，不是我放的，也不是隨 CLI 一起裝的。

這裡要很小心地跟 Day 09 的結論對齊，因為它們看起來像是矛盾的。Day 09 我寫過，「Skill 會跨介面同步」是誤解。這個判斷現在依然成立，但要補一個限定詞：**不會同步的，只限我自己寫的 Skill。** 官方掛在帳號上的那批會下來，我自己那八個資料夾，claude.ai 那邊還是看不到，要用還是得自己上傳。

所以同步是單向而且只涵蓋官方那批。對我的實際影響有兩個。第一，本機的 skill 清單不是只由我決定的，它會自己長出東西來，所以 CLAUDE.md 裡我從來沒有寫死「我有哪幾個 skill」，寫死了就會過期。第二，那個 repo 部署的時候要主動排除 `synced/`，那不是我維護的內容，蓋回去只會製造衝突。

那 skill 和 CLAUDE.md 到底怎麼分？我的判定標準是：**CLAUDE.md 寫事實，skill 寫特定操作步驟。** 「這台是 Windows」是事實，每次都要知道；「怎麼寫一則 commit message」是特定操作步驟，只有真的要 commit 的時候才需要。當 CLAUDE.md 的某一節從一句事實長成一串步驟，那就是該把它抽成 skill 的時候了。

---

## 5. Rules：按檔案類型才載入的那一層

### 5.1 它不是另一套機制

`rules` 屬於 CLAUDE.md 家族，同樣是我寫的持久指令、同樣在 session 載入。差別只在它可以按檔案類型分批載入。位置與範圍：

| Scope | 位置 | 範圍 |
|---|---|---|
| Managed policy | Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | 全機器，無法被個人設定排除 |
| **User rules** | **`~/.claude/rules/*.md`** | **本機所有專案** |
| User instructions | `~/.claude/CLAUDE.md` | 本機所有專案 |
| Project rules | `<project>/.claude/rules/*.md` | 該專案（可進版控共享） |
| Project instructions | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 該專案 |
| Local instructions | `./CLAUDE.local.md` | 只有我、只有該專案（要進 .gitignore） |

上面這張表是依作用域範圍由大到小排列，不是優先序。優先序是反過來的。Windows 下的 `~/.claude` 會解析成 `%USERPROFILE%\.claude`。載入順序是 user 先、project 後，所以**專案規則優先權比較高**。目錄下的 `.md` 會遞迴探索，可以用子資料夾分組。

### 5.2 `paths:` 才是重點

沒有 `paths:` 的 rule 會在啟動時無條件載入，優先權等同 `.claude/CLAUDE.md`，那等於是把 CLAUDE.md 拆成好幾個檔案而已，context 一點都沒省到。

有 `paths:` 的才是真正的按照需求載入。寫法：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

觸發條件是 **Claude 實際「讀到」符合 pattern 的檔案時**，不是每次 tool use 都檢查。這個區別很重要：規則不會因為我在對話裡提到 PowerShell 就載入，要等它真的去讀一個 `.ps1`。

### 5.3 兩個 glob 陷阱

**Brace expansion 會相乘。** `{a,b}/{c,d}/*.{ts,tsx}` 會展開成 8 個 pattern，整個 `paths` 清單共用 1,000 個展開 pattern 或 4 MiB 的預算。超出預算的 pattern 會被原封不動使用，字面大括號配不到任何檔案，那條等於失效。

**中括號會被當成 bracket expression。** `photos [2024/**` 這種無法解讀的 pattern 視為無效，該條配不到檔，但同一份 rule 的其他 pattern 仍正常運作。要匹配字面的 `[` 得跳脫成 `photos \[2024/**`。

我的三份 rules 都只用最單純的 pattern，沒有大括號。

### 5.4 我實際放了哪三份

`~/.claude/rules/` 底下只有三個檔案。

**`markdown.md`**（`paths: **/*.md`）管的是 markdown 原始碼而不是渲染結果，只有兩條：段落不要硬換行，每個區塊前後各留一個空行。

理由都不在美觀。單一換行在 CommonMark 是軟換行，但在 GitHub-flavored markdown 會變成 `<br>`，所以折行過的原始碼會在句子中間、剛好折到的那一欄爆出斷行。清單緊貼下一段則會被解析成清單的延續，那個段落會默默變成最後一個項目的一部分。**兩條的代價都是「渲染出來才發現壞掉」**，所以值得放 rules，而不是靠當下想起來。

**`powershell.md`**（`paths: **/*.ps1`、`**/*.psm1`、`**/*.psd1`）是三份裡最實用的一份，寫了九節。它的開場白就把賭注講清楚：這台跑的是 Windows PowerShell 5.1 而不是 7，從 PowerShell 7 的答案複製過來的片段常常是 **parse error 而不是 runtime error**，意思是整個腳本在第一行執行之前就死了，`try/catch` 救不到。

最花錢的是編碼那一節。`.ps1` 一律存成 UTF-8 with BOM，否則 5.1 會用 ANSI code page（我這台是 cp950）解碼，中文註解變成亂碼，腳本通常死在 `"the string is missing the terminator"`，而那個錯誤指的是一個引號，不是真正的原因。輸出編碼更亂，三個預設值互相不同意：

| 寫法 | 5.1 的預設編碼 |
|---|---|
| `Set-Content` / `Add-Content` | ANSI code page（我這台是 cp950） |
| `Out-File`、`>`、`>>` | UTF-16LE with BOM |
| `[System.IO.File]::WriteAllText` | UTF-8 without BOM |

還有一條我覺得最有價值：**要跑在工作排程器裡的腳本必須自己設 `[Console]::OutputEncoding`，而且必須用真正的排程執行驗證，手動在終端機跑不會重現這個失敗。** 互動式主控台的 code page 通常跟排程器交給電腦程式的那個不一樣。

這種「連驗證方式本身都是錯的」的知識，只能記錄下來。

**`skill-authoring.md`**（`paths: **/SKILL.md`、`**/.claude/skills/**`）是三份裡最長的，內容是寫 SKILL.md 的整套慣例：什麼該做成 skill、frontmatter 怎麼填、body 保持 500 行以內、`model:` / `effort:` 省略就是繼承、以及一份出貨前檢查清單。這篇第 3.3 節和第 4 節那些判斷，來源都是它。

它裡面有一條規則我很喜歡：

> 如果某條指引已經在全域 CLAUDE.md 裡了，不要重述。用**章節名稱**指過去，永遠不要用章節編號，編號會在檔案被編輯時漂移。

還有一條是給我自己的煞車：**建立一個與現有 skill 重疊的 skill 之前要先停下來問。**

以及一條關於 description 的觀察，跟直覺相反：**常見的失敗是「不觸發」，不是「過度觸發」。** 所以 description 要寫得明確而且有點強勢，要寫出請求實際會長成的樣子（副檔名、工具名、人真的會打的字），不要寫抽象類別。`python-plot` 那串「畫一張圖」「圖太醜幫我調一下」就是照這條寫的。

### 5.5 三個會咬人的細節

**`/compact` 之後不會全部回來。** 頂層的 CLAUDE.md (`~/.claude/CLAUDE.md`) 和專案根目錄的 CLAUDE.md 都算，而會在 compact 之後從磁碟重讀並重新注入；**巢狀 CLAUDE.md 與帶 `paths:` 的 rules 不會**，要等下次讀到符合的檔案才重載。所以某條指令在長對話中途「消失」，通常就是這個原因。

**用 `@import` 拆檔省不了 context。** import 進來的檔案一樣在啟動時全部展開。要省 context 只有 path-scoped rules 這條路。官方對單一 CLAUDE.md 的建議上限是 200 行。

**寫得可驗證。** 官方給的對照是「Use 2-space indentation」勝過「Format code properly」，「Run `npm test` before committing」勝過「Test your changes」。

除錯的話有三個工具：`/context` 看實際載入了哪些 memory 檔、`/memory` 列出並開啟各範圍的 memory 檔、`InstructionsLoaded` hook 記錄哪些指令檔在什麼時候為什麼被載入。

---

## 6. Agents：委派的時機、代價、與那個沒人提醒的坑

### 6.1 檔案格式與位置

Subagent 定義檔是 Markdown：YAML frontmatter 是設定，Markdown body 成為它的 system prompt。

```markdown
---
name: code-improver
description: 掃描檔案並提出可讀性、效能與最佳實務的改善建議。寫完或改完程式後使用。
tools: Read, Grep, Glob
model: sonnet
---

You are a code improvement specialist. For each issue you find, explain the problem, show the current code, and provide an improved version.
```

**只有 `name` 與 `description` 是必填。** 位置的優先序由高到低：managed settings、`--agents` CLI flag、`.claude/agents/`（專案）、`~/.claude/agents/`（家目錄，跨所有專案）、plugin 的 `agents/`。

`description` 是 Claude 判斷「何時要委派給它」的唯一依據，跟 skill 的 description 是同一回事，第 5.4 節那條「常見的失敗是不觸發」在這裡一樣成立。

### 6.2 會被靜默略過的四種檔案

這是我覺得最該先知道的踩雷點。以下情況會被跳過，而且**不會在 session 裡提示**，只寫進 debug log：

- 沒有 `name` → 被視為放在 agents 旁邊的說明文件
- `name` 以 `-` 開頭或含 `:` → 跳過並寫 log
- 有 `name` 但沒有 `description` → 跳過並寫 log
- YAML 無法解析 → 整個檔案不讀取

排查用 `claude --debug` 看 log，或 `claude plugin validate ~/.claude/agents` 檢查 frontmatter 是否可解析。注意 `plugin validate` **不會**標記「可解析但缺 `name`」的檔案，那種只能靠 debug log，這跟第 3.3 節那個「驗證工具說沒問題不等於沒問題」是同一件事。

另外，同時有多個檔案宣告相同 `name` 時，只會載入其中一個，由檔案系統讀取順序決定，沒有文件化的優先規則。所以保持 `name` 全域唯一，還是得靠自己把關，比較實在。

### 6.3 subagent 啟動時到底載入了什麼

非 fork 的 subagent 一律是**全新的獨立 context window**，看不到主對話歷史、已載入的 skill、已讀過的檔案。它拿到的是：自己的 system prompt 加環境資訊、Claude 委派時寫的任務描述、**CLAUDE.md 階層**（主對話載入的每一層都會載入）、git status 快照、`skills:` 欄位列出的 skill 全文。

不會傳遞過去的：output style、主對話的 auto memory、父層的 context window 大小。

**唯二的例外是內建的 Explore 與 Plan，它們跳過 CLAUDE.md 與 git status，而且沒有任何欄位或設定可以改變這一點。** 這就是昨天導覽過的 CLAUDE.md 第 7 節那條「委派給 Explore / Plan 時要在 prompt 裡重講關鍵限制」的來源。我第一次踩到的時候，是 Explore 回報了一串 bash 指令，而我在 Windows。

有個小技巧：在 `~/.claude/agents/` 建立一個 `name: Explore` 的定義就能覆寫內建版本。

### 6.4 工具權限有兩層過濾

第一道對所有 subagent 生效，一律移除 `AskUserQuestion`、`EndConversation`、`EnterPlanMode`、`ExitPlanMode`、`ScheduleWakeup`、`TaskOutput` 等，即使寫在 `tools` 裡也一樣。

第二道只對**背景執行**的 subagent 生效，而背景執行是預設值。這一層只保留一組內建工具白名單（Read、Grep、Glob、Bash、PowerShell、Edit、Write、WebFetch、WebSearch、Skill、SendMessage 等，MCP 工具全保留）。

結論是：**同一份定義在前景與背景可能解析出不同的工具集。** 如果一個 agent 在前景好好的、丟到背景就怪怪的，先查這個。

白名單和黑名單並用時（agent frontmatter 裡 `tools` 與 `disallowedTools` 兩個欄位一起寫），先套 `disallowedTools`，再用 `tools` 對剩下的 pool 內容解析，兩邊都列到的工具會被移除。

### 6.5 我唯一一個自訂 agent

`~/.claude/agents/` 底下只有一個檔案：`doc-verifier.md`。它的 frontmatter 是這樣：

```yaml
---
name: doc-verifier
description: Read-only auditor for a project's documentation set (README.md, README.en.md, UI_README.html, 使用者指引.html). Checks required sections, cross-document sync, and drift against the actual code. Use after writing or updating any of these docs, or before packaging a release. Reports problems only — never edits files.
tools: Read, Grep, Glob, PowerShell
skills:
  - readme
  - ui-project
model: sonnet
effort: medium
---
```

四個設計決定，每一個都對應前面某一節：

**`tools` 只給四個唯讀工具，沒有 Edit / Write。** 這個 agent 的定位是稽核員，稽核員不改檔。這裡的 `PowerShell` 不是筆誤，body 裡寫死了「這台是 Windows 11、shell 是 PowerShell，這裡沒有可用的 Bash」，並且加註 `(global: Security & Environment)` 指回 CLAUDE.md 的章節名稱。這件事其實已經在 CLAUDE.md 裡，照第 5.4 節那條「別重述」的規則不該再寫一次，但這裡我還是重複了：這個 agent 常被塞進更長的委派鏈，我不想賭它每次都把整層 CLAUDE.md 讀完再動作，寧可多花這一句。同一句 body 還限制 `PowerShell` 只能做唯讀檢查（`git log`、`git status`、`Get-ChildItem`），永遠不要跑會寫入、暫存、提交或安裝的指令。因為 shell 本身是萬用的，光靠工具清單擋不住。

**`skills:` 預載 `readme` 和 `ui-project` 兩個 skill 的全文。** 這樣它不必自己去猜規則，body 裡直接寫「必要章節與內容規則來自預載的 skill，不要自己重新推導，照著那份文字稽核」。這是 `skills:` 欄位最好用的地方：把判斷基準跟判斷者綁在一起。而且第 4.3 節那個「`readme` 和 `ui-project` 拆成兩份」的決定在這裡剛好回收，兩份都要用的時候，列兩個名字就好。

**`model: sonnet` / `effort: medium` 是刻意覆寫，理由寫在 body 裡：** 稽核是清單工作，所以跑 Sonnet 就好，有哪個發現需要深度判斷再由呼叫端往上升。也印證第 4.1 節那條：覆寫在隔離的 context 裡很便宜。

**輸出格式寫成一個確定的模板，而不是一段描述。** 每一條發現都是 `[FILE] path:line` 加上哪裡錯了、一行修法，按嚴重度排序，最後必須恰好一行結論（`PASS` 加審了幾份文件，或 `FAIL` 加幾個發現、其中幾個是阻擋級）。發現超過 30 條就寫成檔案，只回傳前 15 條加檔案路徑。

最後一條是委派最實際的價值：**subagent 的產出必須是可以塞回主對話的體積。** 如果一個 agent 會回吐三千行，那委派並沒有隔離 context，只是把倒進來的時機延後而已。

### 6.6 什麼時候不要委派

官方的建議：需要頻繁來回、需要多階段共享大量 context、或者只是小改動的時候，留在主對話比較好。

還有一種情況不是「不要委派」，而是「委派錯對象」：那件事需要的正是這一輪對話累積下來的脈絡。這時候該用 fork（`/subtask`）而不是具名 subagent。fork 繼承完整歷史，又共用 prompt cache，比讓一個全新 context 從零把前因後果讀回來便宜。CLAUDE.md 第 7 節就是這樣分的：要脈絡就 fork，要隔離或要限制工具才叫具名 subagent。

同一節還規定了每次委派要交代的三件事：目標和它為什麼重要、具體的驗收標準（測試通過／檔案裡要有 X 和 Y 兩節／grep 出來零筆）、以及回報格式—只要結論加 `file:line`，長輸出寫成檔案再回傳路徑。

另外有兩個上限值得知道：預設 subagent 可以再往下生成 3 層，同時執行的上限預設 20 個。要讓某個 subagent 不能再往下生成，就從它的 `tools` 移除 `Agent`。

---

## 7. 一句話該放哪

三天下來整套東西是這樣分的：

| 一句話要放哪 | 判定標準 | 何時生效 |
|---|---|---|
| `settings.json` | 這件事必須被無條件擋下 | 永遠，harness 層級 |
| `~/.claude/CLAUDE.md` | 換個專案還成立的工作習慣 | 每個 session |
| `<專案>/CLAUDE.md` | 只在這個專案成立的事實與環境 | 該專案的每個 session |
| `~/.claude/rules/*.md` | 每次碰到某類**檔案**就必須套用 | 讀到符合 `paths:` 的檔案時 |
| `~/.claude/skills/*/` | 可重複的多步驟**特定操作步驟** | 任務符合 description 時 |
| `~/.claude/agents/*.md` | 需要隔離 context 的**角色** | 被委派時，全新 context |
| auto memory | Claude 自己整理出的專案知識 | 每個 session |
| `LETTER_TO_FUTURE_SESSIONS.md`（交接信） | 有時效的進度與狀態 | 我叫它讀的時候 |
| `LESSONS.md` | 還沒決定要放哪的觀察 | 永不載入 |

一個實務上的自檢問題，我覺得比整張表都好用：**這句話如果沒被遵守，代價是什麼？**

- 代價是資料不見或東西被 commit 出去 → `settings.json` 或 hook。
- 代價是我要再講一次 → CLAUDE.md 或 rules。
- 代價是它要多花十分鐘重新摸索 → 交接信或 memory。
- 代價是零 → 那就不要寫，它只會稀釋其他規則。

---

## 小結

三天下來（Day 09 的 Skill、Day 10 的 CLAUDE.md 與交接信、今天的 settings / skills / rules / agents），其實一直在回答同一個問題：一段知識該寫成哪一種檔案，才會在需要的時候在場、不需要的時候不佔 context。

我目前的答案有兩條軸。第一條是**約束強度**：只有 `settings.json` 和 hook 是圍欄，其他全部是提示。第二條是**載入時機**：每次載入、按檔案載入、按任務載入、被呼叫才載入、永不載入。第一條決定它擋不擋得住，第二條決定它會耗費多少 token 資源。

如果只能記一句：**CLAUDE.md 和 rules 是 context，不是設定。它們影響模型的意圖，擋不住模型的行為。**

從後天起會開始進實際的專案，第一個是暖身用的小工具。

## 參考資料

Anthropic 官方文件

- Claude Code — Manage Claude's memory（含 rules 與 `paths:` 規格） — https://code.claude.com/docs/zh-TW/memory
- Claude Code — Subagents — https://code.claude.com/docs/zh-TW/sub-agents
- Claude Code — Settings — https://code.claude.com/docs/zh-TW/settings
- Claude Code — Hooks — https://code.claude.com/docs/zh-TW/hooks
- Claude Code — Extend Claude with skills — https://code.claude.com/docs/zh-TW/skills

其他參考

- Claude Code settings JSON Schema — https://json.schemastore.org/claude-code-settings.json

---

> 註一：本文對 Claude Code 的功能描述以 2026 年 8 月 25 日的產品行為為準，CLI 版本為 2.1.241。設定欄位、frontmatter 欄位、內建 subagent 清單與各項預設值日後都可能改變，以官方文件為準。

> 註二：部分規格內容整理自官方文件，其中 brace expansion 的 1,000 pattern／4 MiB 預算、bracket expression 的失效行為、背景 subagent 的工具白名單、`Set-Content`／`Out-File`／`[System.IO.File]::WriteAllText` 三種寫法的預設編碼、`ask` 在所有權限模式下都會跳確認、以及 inline skill 的 `model:` 覆寫會影響整輪對話模型，我沒有逐項實測，屬文件引述而非實驗結果。

> 註三：第 2.3 節貼出的是我自己的 `~/.claude/settings.json` 全文，第 3 節到第 6 節描述的檔案結構、frontmatter 與 rules 內容，都以 2026 年 8 月 25 日我這台電腦上的實際檔案為準，不是官方建議的模板。`ask` 而非 `deny` 是我個人的取捨，不見得適合每個人。

> 註四：第 4.5 節的 `synced/` 資料夾內容以我這台電腦上的 `manifest.json` 為觀察樣本，`source` 欄位值為 `anthropic` 與 `anthropic-example`。「只同步官方 Skill、不同步自訂 Skill」這點已另行查閱官方文件確認；同步的觸發時機仍以這份 manifest 為準。

> 註五：第 6.3 節「Explore 回報 bash 指令」是我遇過的單次情況，屬定性觀察。
