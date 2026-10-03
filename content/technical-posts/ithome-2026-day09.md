---
title: "Day 09｜三個介面，一套 Skill？先看看它們各自預設帶了什麼"
date: 2026-08-23T00:00:00+08:00
authors: ["Alex Yu"]
series: ["iThome 2026 Ironman"]
tags: ["Claude", "iThome"]
---

> **This post is in Traditional Chinese Only.**

> Originally published on [iThome 2026 Ironman Contest](https://ithelp.ithome.com.tw/articles/10404684).

---

## 說明

在[Day 08](https://ithelp.ithome.com.tw/articles/10404489) 中，提到了 Claude 的 Skill 機制 (也是現在所有 LLM 模型幾乎都有的機制)，今天來探索一下何謂 Skill。

## 1. Skill 是什麼

官方稱 **Agent Skill** 是一個資料夾，裡面必須有一個 `SKILL.md`，可以再附加參考文件、範本、腳本。

範例結構模板：

```
my-skill/
├── SKILL.md          ← 必要：YAML frontmatter + Markdown 指令
├── reference.md      ← 選用：需要時才載入的詳細參考
├── examples.md       ← 選用：範例
└── scripts/
    └── helper.py     ← 選用：被執行，而不是被讀進 context
```

核心機制是 **漸進式載入（progressive disclosure）**：

- 平常 context 裡只有「名稱 + description」的清單
- 只有當 Claude 判斷任務符合 description，或輸入 `/skill-name` 時，才把 SKILL.md 本體載入
- 因此「長篇參考資料放進 Skill 幾乎不花錢，直到使用者真的需要它」

這是它跟 `CLAUDE.md` 最大的差別：`CLAUDE.md` 是**每次都載入的事實**，Skill 是**按需要才載入的程序**。當 `CLAUDE.md` 某一節從「事實」長成「流程」時，就是該把它抽成 Skill 的時候。（明天再來聊聊 CLAUDE.md）

Claude Code 的 Skill 遵循 [Agent Skills 開放標準](https://agentskills.io)，並在此之上加了自己的擴充（invocation 控制、subagent 執行、動態 context 注入）。

### 最小範例

```yaml
---
name: summarize-changes
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

用兩三個 bullet 摘要上面的變更，然後列出使用者注意到的風險：缺少錯誤處理、寫死的值、需要更新的測試。若 diff 為空，直接說沒有未提交的變更。
```

---

## 2. 各介面的「預設 Skill」對照

這是最容易混淆的部分。**不同介面的預設 Skill 完全不同，而且自訂 Skill 不會自動跨介面同步。**

### 2.1 總覽表

| 介面 | 預設 Skill | Skill 來源 | 支援 Claude Code 專屬 frontmatter |
|---|---|---|---|
| **claude.ai chat（網頁/App）** | pptx / xlsx / docx / pdf 四個文件類 | 帳號啟用的 Skill | ❌ 只支援標準 6 欄位 |
| **claude.ai Cowork（網頁/App）** | 同上四個 + Cowork 相關 | 帳號啟用的 Skill | ❌ |
| **Claude Desktop chat** | 同 claude.ai chat（同一個帳號設定） | 帳號啟用的 Skill | ❌ |
| **Claude Desktop Cowork** | 同上 | 帳號啟用的 Skill（session 啟動時同步） | ❌（且 `!` 指令被替換成佔位符） |
| **Claude Code（終端機原生）** | bundled skills：`/doctor` `/code-review` `/debug` `/batch` `/loop` `/claude-api` `/run` `/verify` `/run-skill-generator` … | 本機檔案系統 + plugin | ✅ 全部欄位 |
| **Claude Code in VS Code** | 同終端機原生（同一個 CLI 核心） | 同上 | ✅ |
| **Claude Cloud session / Routines** | bundled skills | claude.ai 帳號啟用的 Skill + repo 內 `.claude/skills/` | ✅（repo 內的） |

### 2.2 claude.ai / Desktop 的四個內建 Skill

這四個是 Anthropic 官方預建、**開箱即用、不需安裝**：

| Skill | 用途 |
|---|---|
| `pptx` | 建立簡報、編輯投影片、分析簡報內容 |
| `xlsx` | 建立試算表、資料分析、產生含圖表的報告 |
| `docx` | 建立文件、編輯內容、格式化文字 |
| `pdf` | 產生格式化的 PDF 文件與報告 |

這四個同時在 Claude API、AWS 上的 Claude Platform、Microsoft Foundry 與 claude.ai 提供。

### 2.3 Claude Code 的 bundled skills

Claude Code 有一整組隨附 Skill，性質跟上面四個不同，它們是**prompt-based**：給 Claude 詳細指令，讓它用自己的工具去編排工作（而多數 built-in command 是直接執行固定邏輯）。

常用的幾個：

| Skill | 用途 |
|---|---|
| `/doctor` | 環境健檢 |
| `/code-review` | 程式碼審查（v2.1.218 起以 forked subagent 執行） |
| `/debug` | 除錯 |
| `/batch` | 批次處理 |
| `/loop` | 迴圈執行 |
| `/claude-api` | 提供最新的 Anthropic API 參考資料 |
| `/run` | 啟動並驅動 app，實際看到改動生效 |
| `/verify` | 建置並執行 app 確認改動正確，只看測試或型別檢查 |
| `/run-skill-generator` | 把「怎麼建置與啟動這個專案」錄成 per-project skill，寫進 `.claude/skills/run-<name>/` |

幾個要點：

- 有些 bundled skill Claude 會自動觸發；`/verify` 這種比較耗時的**只有手動叫才會跑**，避免它自己花掉時間跟 token
- 想全部關掉：設定 `disableBundledSkills: true`（`/doctor` 除外）
- `/run` 與 `/verify` 免設定就能用，會從專案類型、README、`package.json`、`Makefile` 去推論怎麼啟動。但只要專案需要資料庫、env 檔、圖形化 session 或多步驟建置，推論就不可靠，這時可以透過跑一次 `/run-skill-generator` 把 recipe 錄下來

### 2.4 Cowork 的特殊之處（重要陷阱）

> **Cowork session 與 cloud session 不會讀取本機的 `~/.claude/skills/`。**

它們讀的是**使用者 claude.ai 帳號上啟用的 Skill**，在 session 啟動時同步。所以：

- 使用者在本機 `~/.claude/skills/` 寫的 Skill，Cowork **找不到**
- Routine（排程任務）每次都是全新的遠端 session，一樣找不到
- 要讓個人 Skill 在 Cowork 可用 → 必須把它**上傳到 claude.ai 帳號**並啟用
- Cloud session 另外還會載入 repo 內 committed 的 `.claude/skills/`

**唯一例外**：Desktop **scheduled tasks** 是在使用者本機跑的，載入位置跟一般本機 session 相同。

另外，Cowork 中 Claude Code 會把每個 `!` shell 注入指令替換成 `disableSkillShellExecution` 佔位符，而動態 context 注入在 Cowork **不會實際執行**。

### 2.5 名稱衝突的解析順序（Claude Code）

| 層級 | 路徑 | 適用範圍 |
|---|---|---|
| Enterprise | managed settings 目錄 | 全組織 |
| Personal | `~/.claude/skills/<name>/SKILL.md` | 個人所有專案 |
| Project | `.claude/skills/<name>/SKILL.md` | 該專案 |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | 啟用該 plugin 處 |

優先序：

- **Enterprise > Personal > Project**（注意：personal 蓋過 project，跟直覺相反）
- 上述任一層級的同名 skill 會蓋掉 bundled skill，但**不會蓋掉 bundled skill 的別名**（例如使用者自訂 `code-review`，輸入 `/review` 仍然跑內建的）
- Plugin skill 有 `plugin-name:skill-name` 命名空間，不會衝突
- 本機任何來源的 skill 都蓋過**從 claude.ai 同步下來的**同名 skill
- 同名時 skill 優先於 `.claude/commands/` 的檔案

Monorepo（單體式倉庫）補充：巢狀 `.claude/skills/` 在 Claude 讀寫該子目錄檔案時才載入，同名時以 `apps/web:deploy` 這種目錄限定名稱出現。

---

## 3. 如何在各介面加入自己的 Skill
 
### 3.1 claude.ai / Claude Desktop（chat 與 Cowork）
 
**方式 A：安裝現成的**
 
1. claude.ai / Claude Desktop：左側欄 **Customize** → **Skills** 分頁 → **Add skill** → **+**
2. claude.ai / Claude Desktop：對話框輸入 `/` 看目前可用 Skill；**add-files** 也可新增
3. 點 **Install**。安裝後預設啟用，Claude 會在任務符合 description 時自動套用，且可隨時關掉

**方式 B：上傳自訂 Skill**
 
- claude.ai / Claude Desktop：左側欄 **Customize** → **Skills** 分頁 → 右上角 **Add v** → 選擇要怎麼創立
- 若選擇 Upload 要是 zip 檔案，而 zip 的根目錄要直接是 skill 資料夾本身（不要多包一層），且資料夾名稱要與 skill 名稱一致
- **前提是開啟「Code execution and file creation」**
  - Skill 功能在 **Free、Pro、Max、Team、Enterprise 全方案皆可用**
  - Free / Pro / Max：自行到 **Settings → Capabilities** 開啟 code execution
  - Team：組織層級預設已啟用
  - Enterprise：需由 Owner 在 **Organization settings → Skills** 確認 code execution 與 Skills 皆為開啟
- 上傳的 Skill 為**個人帳號私有**；Team / Enterprise 的組織 Owner 可另外上傳並全組織佈署，這類 skill 會自動出現在所有成員的清單中

**方式 C：從 Claude Code 打包上傳**
 
用 [anthropics/skills](https://github.com/anthropics/skills) 的 `package_skill.py` 打包後上傳。
 
> ⚠️ **frontmatter 限制**：走 claude.ai 上傳、Skills API、`package_skill.py` 這三條路徑時，**只允許標準 6 個欄位**：
> `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`
>
> 放了 `argument-hint`、`context: fork`、`disable-model-invocation` 等 Claude Code 專屬欄位，會直接**打包/上傳失敗**（硬錯誤，不是忽略）：
>
> ```
> Unexpected key(s) in SKILL.md frontmatter: argument-hint.
> Allowed properties are: allowed-tools, compatibility, description, license, metadata, name
> ```
>
> 同樣地，`!` 動態注入這類 Claude Code body 專屬功能，在 claude.ai chat 與 API 中**不會運作**。
>
> 補充：把個人 Skill 啟用給 Cowork 與雲端 session（含 routines）使用時，等同上傳到 claude.ai，因此適用同一套欄位限制。
 
啟用在帳號上的 Skill 也會自動出現在 Claude for Excel / PowerPoint / Word / Outlook 外掛中，Claude 會在使用者工作時自動套用相關 Skill，不需另外呼叫。跨 app 作業時，各 app 會各自套用對應的 Skill。例如一個規範 Excel 建模慣例的 Skill 會在 Excel 生效，另一個對應簡報樣板的 Skill 會在 PowerPoint 生效。實際輸出形式仍取決於 Skill 本身怎麼寫，平台不會自動轉換格式。

### 3.2 Claude Code（終端機 / VS Code）

**個人 Skill（跨所有專案）：**

(PowerShell)
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills\my-skill" | Out-Null
notepad "$HOME\.claude\skills\my-skill\SKILL.md"
```

(Bash)
```bash
mkdir -p ~/.claude/skills/my-skill
$EDITOR ~/.claude/skills/my-skill/SKILL.md
```

**專案 Skill（提交進 git，團隊共用）：**

(PowerShell)
```powershell
New-Item -ItemType Directory -Force -Path ".claude\skills\my-skill" | Out-Null
```

(Bash)
```bash
mkdir -p .claude/skills/my-skill
```

**即時生效**：Claude Code 會監看 skill 目錄，新增／編輯／刪除在**當前 session 內就會生效，不用重啟**（僅限 SKILL.md 文字；plugin 型 skill 的 hooks/agents 變更需 `/reload-plugins`）。若建立了一個 session 啟動時還不存在的頂層 skills 目錄，才需要重啟。

**額外目錄**：`--add-dir` / `/add-dir` 會自動載入該目錄的 `.claude/skills/` 與 `.claude/commands/`（這是權限規則的例外）。但 `settings.json` 裡的 `permissions.additionalDirectories` **只給檔案存取，不載入 skill**。

**符號連結**：skill 目錄可以是 symlink，Claude Code 會跟隨並讀取目標目錄的 SKILL.md。

**用 plugin 安裝：**

```bash
claude plugins install <plugin-name>
# 或 session 內
/plugin install <plugin-name>
```

**把 claude.ai 的 Skill 同步到本機**（需要一次非互動式執行）：

(PowerShell)
```powershell
$env:CLAUDE_CODE_SYNC_SKILLS="1"; claude -p "List the skills you have available"
```

(Bash)
```bash
CLAUDE_CODE_SYNC_SKILLS=1 claude -p "List the skills you have available"
```

下載到 `~/.claude/skills/synced/`，之後每個本機 session 都會載入。`/skills` 選單會把它們標為 `claude.ai sync`。注意：`synced` 這個資料夾名稱是保留字。

> 同步下來的 Skill 在**本機一般 session** 中限制較多：`!` 指令不執行、`@` 引用不附加檔案、`${CLAUDE_PROJECT_DIR}` 等佔位符不替換，全部以字面文字送給 Claude。只有 cloud session（隔離容器）與 Cowork session 保有較接近本機 skill 的行為。

執行結果（我已經有自行新增了部分的 Skills，請參考 [ycy1997alex/dotclaude](https://github.com/ycy1997alex/dotclaude/)）：

```bash
內容開始↓↓↓
```

`(base) PS D:\> $env:CLAUDE_CODE_SYNC_SKILLS="1"; claude -p "List the skills you have available"`
以下是目前這個 session 可用的 skills（可用 `/<名稱>` 直接叫用）：

**文件處理**
| 名稱 | 用途 |
|---|---|
| `docx` | Word 文件（.docx / .dotx）建立、讀取、編輯 |
| `xlsx` | 試算表（.xlsx / .csv / .tsv）操作與清理 |
| `pptx` | 簡報（.pptx / .potx）建立與解析 |
| `pdf` | PDF 讀取、合併、拆分、OCR、表單填寫 |
| `officecli` | 透過 officecli CLI 建立／校對／修改 Office 檔案 |

**寫作與文件規範**
| 名稱 | 用途 |
|---|---|
| `humanizer` | 去除英文文字的 AI 生成痕跡 |
| `humanizer-zh-tw` | 去除中文文字的 AI 生成痕跡 |
| `readme` | README.md 及多語版本的章節與同步規範 |
| `ui-project` | UI_README.html／使用者指引.html 與 PyInstaller 打包規範 |
| `doc-verifier`（agent，非 skill） | 唯讀稽核專案文件集 |

**程式碼審查與開發**
| 名稱 | 用途 |
|---|---|
| `code-review` | 審查 diff／PR，可 `--fix`、`--comment`，或 `ultra` 雲端多 agent 審查 |
| `simplify` | 只做簡化／重用／效率清理，不抓 bug |
| `security-review` | 當前 branch 待提交變更的資安審查 |
| `run` | 啟動並操作專案 app 以驗證改動 |
| `init` | 產生新的 CLAUDE.md |
| `claude-api` | Claude API／SDK 參考（model id、定價、streaming、tool use…） |

**設定與環境**
| 名稱 | 用途 |
|---|---|
| `update-config` | 修改 settings.json：權限、env、hooks |
| `keybindings-help` | 自訂 keybindings.json 快捷鍵 |
| `fewer-permission-prompts` | 掃描歷程並產生 allowlist，減少權限提示 |
| `skill-creator` | 建立／改進／評測 skill |

**排程與自動化**
| 名稱 | 用途 |
|---|---|
| `loop` | 依間隔重複執行某個 prompt 或 slash command |
| `schedule` | 建立雲端 cron 排程 agent（含一次性排程） |
| `morning` | 早晨簡報 HTML artifact |

**其他**
| 名稱 | 用途 |
|---|---|
| `dataviz` | 任何圖表／儀表板繪製前的設計規範 |
| `import-memory` | 匯入其他 AI 助理的 memory 匯出檔 |

補充兩點：

1. `/ultrareview` 是 `/code-review ultra` 的舊別名，兩者相同；該指令由使用者觸發並計費，我無法自行啟動。
2. 這個 session 中的 claude.ai Gmail、Google Calendar、Google Drive 三個 MCP server 尚未授權，且此為非互動 session 無法跑 OAuth 流程。若要使用，需到 claude.ai 的 connector 設定中授權。

```bash
內容結束↑↑↑
```

### 3.3 移除 Skill

| 來源 | 移除方式 |
|---|---|
| Personal / Project | 刪掉該 skill 目錄 |
| Enterprise | 管理員從 managed settings 目錄刪除 |
| Plugin | `/plugin uninstall <plugin>@<marketplace>` 後 `/reload-plugins` |
| claude.ai 同步 | 在 claude.ai 帳號關閉該 skill（手動刪本機目錄會被下次同步抓回來） |
| Bundled | `disableBundledSkills: true` 或 `skillOverrides` 設 `"off"` |

不想刪、只想讓 Claude 不要自動觸發 → frontmatter 加 `disable-model-invocation: true`，或在 `skillOverrides` 設 `"user-invocable-only"`。

---

## 4. Frontmatter 關鍵欄位速查（Claude Code 專用）

```yaml
---
name: my-skill                    # 顯示名稱；指令名仍取自目錄名
description: 做什麼、什麼時候用    # 最重要，Claude 靠它決定是否載入
when_to_use: 觸發語句、範例請求    # 附加在 description 後
disable-model-invocation: true    # 只有使用者能叫（適合有副作用的：/deploy /commit）
user-invocable: false             # 只有 Claude 能叫（適合背景知識）
allowed-tools: Bash(git add *)    # 該回合免詢問的工具授權
disallowed-tools: AskUserQuestion # 該 skill 啟用時移除的工具
model: opus                       # 該 skill 啟用時切換模型
effort: high                      # 該 skill 啟用時的 effort 等級 ★
context: fork                     # 在獨立 subagent 中執行
agent: Explore                    # fork 時用哪種 subagent
background: false                 # fork 時是否等待結果
paths: "src/**/*.ts"              # 只在處理符合的檔案時自動載入
hooks: ...                        # 註冊 hooks
---
```

**誰能觸發的三種組合：**

| Frontmatter | 使用者能叫 | Claude 能叫 | context 載入時機 |
|---|---|---|---|
| （預設） | ✅ | ✅ | description 常駐，本體在被叫時載入 |
| `disable-model-invocation: true` | ✅ | ❌ | description **不在** context，本體在使用者叫時載入 |
| `user-invocable: false` | ❌ | ✅ | description 常駐，本體在被叫時載入 |

**字串替換**：`$ARGUMENTS`、`$0`/`$1`、`${CLAUDE_SKILL_DIR}`、`${CLAUDE_PROJECT_DIR}`、`${CLAUDE_SESSION_ID}`、`${CLAUDE_EFFORT}`。

**動態注入**：`` !`command` `` 或 ```` ```! ```` 區塊，會在送給 Claude 前先執行並把輸出貼進來。注入指令**永不詢問權限**：權限檢查沒過就直接中止整個 skill 呼叫。任何非零 exit code（搜尋類指令的 exit 1 除外）也會中止，預期會非零的指令記得加 `|| true`。

**Skill 生命週期**：被叫用後，渲染後的 SKILL.md 以單一訊息進入對話，**留在 context 直到 session 結束**。Claude Code 不會在後續回合重讀檔案，所以「整個任務都要遵守」的規則要寫成常駐指令，而不是一次性步驟。Auto-compaction 時會保留每個 skill 最近一次呼叫的前 5,000 tokens，總預算 25,000 tokens，從最近呼叫的往回填，呼叫過太多 skill 的話，舊的會被整個丟掉。

---

## 5. Marketplace：哪裡找額外的 Skill

除了自己寫，還有一整套 marketplace 機制可以安裝別人做好的 Skill。分三層。

### 5.1 官方 Marketplace：claude-plugins-official

Anthropic 維護的官方目錄，**首次啟動時自動註冊，不用手動加**。截至 2026 年 7 月收錄 **256 個項目**：36 個 Anthropic 內部 plugin + 220 個外部上架項目。

**瀏覽與安裝：**

```bash
/plugin                                    # 開啟面板瀏覽整個目錄
/plugin install <name>@claude-plugins-official
```

Claude Cowork **預設就內建**這個官方 marketplace。若在 Claude Code 中需要手動加：

```bash
/plugin marketplace add https://marketplace.anthropic.com
```

**內容分類：**

| 類別 | 例子 |
|---|---|
| 開發流程 | `code-review`、`security-guidance` |
| 設計 | `frontend-design` |
| Skill 工具 | `skill-creator`（寫、測、調校自己的 Skill） |
| Code Intelligence | 11 種語言的 Language Server（LSP 診斷與程式碼導航） |
| Output styles | 輸出風格 |
| 合作夥伴 MCP 整合 | GitHub、Supabase、Vercel、Figma、Linear、Sentry、Notion… |

### 5.2 官方社群 Marketplace：claude-community

Anthropic 另外經營的第二個 marketplace，收錄**經過審核的第三方 plugin**。定位介於「官方自製」與「完全野生」之間，屬於有通過自動化安全篩查，但不是 Anthropic 自己寫的。

### 5.3 自架 / 第三方 Marketplace

Plugin 透過 **git 分發**：一個 marketplace 本質上就是一個含 `.claude-plugin/marketplace.json` manifest 加上 plugin 內容的 git repo。所以任何能放上 GitHub / GitLab / Bitbucket 的地方都能當 marketplace。

```bash
/plugin marketplace add <git-repo-url 或 owner/repo>
```

知名社群目錄例如 `wshobson/agents`（94 個 plugin，涵蓋語言工具、外部整合、多 agent 編排）。**下一節要介紹的 `mattpocock/skills` 也是走這條路線。**

### 5.4 Plugin vs Skill：為什麼要有 Plugin

在 plugin 出現之前，這些東西要一個一個手動接：MCP server 設定寫進 `~/.claude/.mcp.json`、slash command 丟進 `~/.claude/commands/`、hooks 設進 `settings.json`、Skill 再裝到 session 看得到的地方。要分享給同事等於在四個設定檔之間做複製貼上巡禮。

**Plugin 把這些收斂成一道安裝指令。** 標準結構：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json    # plugin metadata（必要）
├── .mcp.json          # MCP server 設定（選用）
├── commands/          # slash commands（選用）
├── agents/            # agent 定義（選用）
├── skills/            # Skill 定義（選用）★
└── README.md
```

所以：**Skill 是單一能力，Plugin 是打包容器**，一個 plugin 可以同時帶 skills、commands、agents、hooks 和 MCP servers，安裝時 Claude Code 會自動把每個部分接到正確的 scope（user / project / local）。

### 5.5 ⚠️ 安全提醒

> **Marketplace 上架只是分發用的 metadata，不是沙箱，也不是安全保證。**

官方 repo 明文寫著外部 plugin 必須符合上架標準，但**同時警告 Anthropic 並不控管第三方所捆綁的 MCP server、檔案或其他軟體**。

實務原則：

- 把每個 plugin 都當成**會以使用者帳號權限執行的程式碼**
- 安裝前讀過它的每一個 skill、command、agent 定義
- 特別注意 `allowed-tools` ，如第 8 節所述，這個欄位**不受 workspace trust 把關**，一個 skill 可以自我授予廣泛的工具權限

### 5.6 跟 claude.ai chat 的關係

這套 `/plugin` marketplace 系統目前主要服務 **Claude Code 與 Cowork**。claude.ai chat 那邊安裝 Skill 走的是「Customize → Skills → 目錄」的圖形介面路徑。兩者背後的目錄有重疊（Cowork 內建官方 marketplace），但操作方式不同，別預期在網頁 chat 裡打 `/plugin install`。

---

## 6. mattpocock/skills：軟體工程架構 Skill

倉庫：<https://github.com/mattpocock/skills> ｜ MIT ｜ 226k stars

作者 Matt Pocock 的定位很明確：**「Skills for Real Engineers — 做真實工程，不是 vibe coding。」**

### 6.1 設計哲學

他對 GSD、BMAD、Spec-Kit 這類框架的批評是：**它們接管了整個流程，因而奪走使用者的控制權，並讓流程本身的 bug 難以排除。**

所以這組 skill 刻意做成 **小、易於改寫、可組合**，它們與模型無關，可在任何 agent 上跑，核心是「拿去改，變成使用者自己的」。

### 6.2 四大失敗模式 → 對應解方

這是整個架構的骨幹，每一層都對應一個真實的工程失敗模式：

#### #1 Agent 沒做出我要的東西（Misalignment）

> 「沒有人確切知道自己要什麼」— The Pragmatic Programmer

**問題**：軟體開發最常見的失敗是需求錯位。以為開發者懂需求者，看到成品才發現完全誤解，而這件事在 AI 時代一模一樣。

**解法**：**grilling session** — 讓 agent 反過來拷問需求者，逼出所有細節。

- `/grill-me` — 非程式用途
- `/grill-with-docs` — 同上，但額外建立領域模型

這是他最受歡迎的 skill，**每次要做改動前都該用。**

#### #2 Agent 太囉唆（缺乏共通語言）

> 「有了 ubiquitous language，開發者之間的對話與程式碼的表達都源自同一個領域模型」— Eric Evans, DDD

**問題**：agent 被丟進專案，得邊做邊猜行話，於是用 20 個字講 1 個字的事。

**解法**：一份 `CONTEXT.md`，幫 agent 解碼專案術語。

範例對照：

- **BEFORE**：「當一個 course 裡某個 section 裡的 lesson 被『實體化』（也就是在檔案系統中被分配位置）時會有問題」
- **AFTER**：「materialization cascade 有問題」

共通語言的連帶效益：變數／函式／檔案命名一致 → codebase 對 agent 更好導航 → **agent 花在思考上的 token 更少**，作者說這可能是整個 repo 裡最酷的技巧。

#### #3 程式碼不能跑（缺乏 feedback loop）

> 「永遠採取小而審慎的步伐。回饋速率就是需求者的速限。」— The Pragmatic Programmer

**解法**：靜態型別、瀏覽器存取、自動化測試三件套，其中 red-green-refactor 迴圈最關鍵。agent 先寫一個會失敗的測試，再把它修綠。

- `/tdd` — red-green-refactor，並給 agent 大量「什麼是好測試／壞測試」的指引
- `/diagnosing-bugs` — 把除錯最佳實踐包成一個逐階段設卡的紀律迴圈

#### #4 我們蓋出了一團爛泥（Ball of Mud）

> 「每天都投資在系統設計上」— Kent Beck
> 「最好的模組是深的：大量功能藏在簡單介面之後」— John Ousterhout, A Philosophy of Software Design

**問題**：agent 大幅加速寫程式，也就**同步加速了軟體熵增**。

**解法**：把「在意程式碼設計」內建進每一層。

- `/to-spec` — 建 spec 前先問需求者會動到哪些模組
- `/improve-codebase-architecture` — 掃描 codebase 找「可加深模組」的機會，做成視覺化 HTML 報告交給使用者挑。作者建議**每幾天跑一次**，他也誠實提醒：這是**普查而非救援**，老舊 codebase 上它會找出真候選，但不會幫使用者把爛泥解開

### 6.3 架構的關鍵切分：User-invoked vs Model-invoked

這是整個 repo 最值得學的設計決定：

| | User-invoked | Model-invoked |
|---|---|---|
| 誰能叫 | 只有使用者打 `/grill-me` | 使用者可以叫，agent 也會在任務合適時自己伸手拿 |
| 職責 | **編排（orchestrate）** | **持有可複用的紀律（discipline）** |
| 組合規則 | 可以呼叫 model-invoked skill | — |
| 禁止 | **不能呼叫另一個 user-invoked skill** | — |

這條「user-invoked 不能呼叫 user-invoked」的規則，讓整個系統維持單層編排、不會遞迴成黑箱 — 正好對應他對 GSD/BMAD 的批評。

### 6.4 Skill 清單

**Engineering / User-invoked**

| Skill | 說明 |
|---|---|
| `ask-matt` | 問「我這情境該用哪個 skill／流程」的 router |
| `grill-with-docs` | 拷問 + 建立領域模型，同步更新 `CONTEXT.md` 與 ADR |
| `triage` | 用 triage 角色的狀態機推進 issue |
| `improve-codebase-architecture` | 掃描可加深的模組機會 → HTML 報告 → 挑一個進去拷問 |
| `setup-matt-pocock-skills` | 每個 repo 跑一次的初始設定 |
| `to-spec` | 把當前對話變成 spec 並發布到 issue tracker（不面談，只綜整） |
| `to-tickets` | 把計畫拆成 tracer-bullet tickets，各自宣告 blocking 邊 |
| `implement` | 依 spec/tickets 施工，在預先約定的接縫驅動 `/tdd`，提交前跑 `/code-review` |
| `wayfinder` | 規劃超過單一 agent session 容量的大工程：在 tracker 上做成決策 ticket 地圖，逐一解決 |

**Engineering / Model-invoked**

| Skill | 說明 |
|---|---|
| `prototype` | 用完即丟的原型回答設計問題（單檔 HTML 或多種 UI 變體） |
| `diagnosing-bugs` | 紅燈 → 最小化 → 假設 → 埋點 → 修復 → 回歸測試 |
| `research` | 對高信任度一手來源調查，產出帶引用的 Markdown，背景 agent 執行 |
| `tdd` | red-green-refactor，一次一個垂直切片 |
| `domain-modeling` | 主動打磨領域模型：挑戰術語、用邊界案例壓力測試 |
| `codebase-design` | 設計深模組的共通紀律與詞彙：小介面、乾淨接縫、可透過介面測試 |
| `code-review` | 雙軸審查（Standards + Spec），以平行 subagent 執行避免互相污染 |
| `resolving-merge-conflicts` | 逐 hunk 依意圖解衝突，追溯到雙方一手來源，最後完成合併（絕不 `--abort`） |
| `wizard` | 產生互動式 bash wizard，帶人類走只有人能做的步驟 |

**Productivity**

| Skill | 類型 | 說明 |
|---|---|---|
| `grill-me` | User | 被無情面談直到設計樹每個分支都解決 |
| `handoff` | User | 把對話壓縮成交接文件，讓另一個 agent 接手 |
| `teach` | User | 跨 session 教學，用當前目錄當有狀態的教學工作區 |
| `to-questionnaire` | User | 把答不了的決策變成給對的人填的 Markdown 問卷 |
| `wait-what` | User | 訊息看不懂時立刻按，agent 用使用者的 `CONTEXT.md` 詞彙重新解釋 |
| `grilling` | Model | 面談原語，是 grill-me / grill-with-docs / triage / wayfinder 背後的共用元件 |
| `writing-for-agents` | Model | 怎麼寫給 agent 看的文件：skill、AGENTS.md / CLAUDE.md |

### 6.5 安裝：兩條路，兩種哲學

> **只選一條。兩個都裝會讓使用者每個 skill 都有兩份。**

**A. Claude Code plugin（訂閱式）**：整組以**唯讀託管套件**安裝，作者更新時自動同步。使用者是訂閱者，不是 fork 者。

```bash
claude plugins install mattpocock-skills
# 或 session 內
/plugin install mattpocock-skills
```

已在官方 marketplace，不用先加 marketplace。

**B. skills.sh（可改寫式）**：把可編輯的 skill 檔案複製進專案，變成個人擁有的普通檔案，可以隨意 hack。

```bash
npx skills@latest add mattpocock/skills
```

安裝器讓使用者選要哪些 skill、裝到哪些 agent（Codex 等也支援），**務必勾選 `setup-matt-pocock-skills`，** 想拉作者的最新變更時再手動 `npx skills update`。

**安裝後**：每個 repo 跑一次 `/setup-matt-pocock-skills`，它會問使用者三件事 (1) 用哪個 issue tracker（GitHub / Linear / 本地檔案） (2) triage 時貼什麼標籤 (3) 文件要存哪裡。

### 6.6 典型工作流

```
/grill-with-docs   ← 對齊需求 + 建立 CONTEXT.md 與 ADR
      ↓
/to-spec           ← 綜整成 spec，發到 issue tracker
      ↓
/to-tickets        ← 拆成 tracer-bullet tickets
      ↓
/implement         ← 施工，內部驅動 tdd → code-review
```

超大工程則從 `/wayfinder` 開始，先把決策點攤成地圖再逐一解。

---

## 7. Model 與 Effort 對 Skill 的適應性／遵從性

### 7.1 Effort 是什麼

Effort 控制模型在回應前投入多少內部推理。可用等級：`low` / `medium` / `high` / `xhigh` / `max`。

它**不只是思考深度的旋鈕，更是整體工作縝密度的旋鈕**：降低 effort 時，Claude 會減少工具呼叫次數、不寫前言直接開工、完成時只給簡短回報；提高 effort 時，會傾向先解釋計畫、詳細總結變更、寫更完整的程式碼註解。

### 7.2 各等級適用場景

| 等級 | 適用 |
|---|---|
| `low` | 只有一個明顯答案的工作：改名、一行修正、例行工具呼叫。輸出空間窄，多想無益 |
| `medium` | 速度／成本／效能的最佳平衡，適合大多數應用、agentic coding、tool-heavy workflow |
| `high` | 複雜推理、品質重於速度與成本；多數 intelligence-sensitive workload 的最低標準 |
| `xhigh` | coding 與 agentic 用途的建議起點 |
| `max` | 需要絕對最高能力、不在乎 token 花費時。**官方直言：多數 workload 上 max「增加顯著成本卻只換來相對小的品質提升」，某些結構化任務甚至會想太多** |

### 7.3 模型差異（重要）

**支援的等級因模型而異：**

| 模型 | 可用等級 |
|---|---|
| Opus 4.8 / Opus 4.7 | `low` `medium` `high` `xhigh` `max` |
| Opus 4.6 / Sonnet 4.6 | `low` `medium` `high` `max`（無 `xhigh`） |

設定了模型不支援的等級時，Claude Code 會**降到該模型支援的最高等級**（例如 `xhigh` 在 Opus 4.6 上跑成 `high`）。

**預設值：** 支援 effort 的模型預設都是 `high`，Opus 4.7 例外，預設 `xhigh`。首次執行 Fable 5 / Opus 4.8 / Opus 4.7 時，Claude Code 會套用該模型預設並保持，直到使用者明確用 `/effort` 或 `--effort` 選擇。Opus 5 沒有這個 hold，使用者先前設的等級會延續。

**遵從性差異（這點對 Skill 最關鍵）：**

> **Claude Opus 4.7 對 effort 等級的遵守比 Opus 4.6 更嚴格，尤其在 low 與 medium。低 effort 時，模型會把工作範圍限縮在「被要求的事情」，而不做超出要求的事。**（Opus 4.8 同樣適用）

這對 Skill 有直接影響：**一個要求多步驟紀律的 Skill（例如 `/tdd` 的 red-green-refactor、`/diagnosing-bugs` 的逐階段設卡），在 low/medium effort 下被「範圍限縮」而只執行表層的風險，在新模型上更高。**

官方建議：**如果在複雜問題上觀察到推理過淺，應該提高 effort，而不是用 prompt 繞過去。** 若因延遲考量必須維持低 effort，加上針對性指引如「This task involves multistep reasoning. Think carefully before responding.」

在 xhigh 或 max 執行 Opus 4.7/4.8 時，要把 `max_tokens` 設大，讓模型有空間跨 subagent 與工具呼叫思考，而**從 64k tokens 起跳是合理預設**。

### 7.4 Skill 的 effort 覆寫（Claude Code 專屬）

**設定優先序：** 環境變數 > 使用者設定的等級 > 模型預設。Skill/subagent frontmatter 的 `effort` 在該 skill 啟用時覆寫 session 等級，**但不覆寫環境變數**。

```yaml
---
name: diagnose-perf
description: 診斷效能回歸
effort: xhigh          # 這個 skill 跑的時候拉高推理
model: inherit         # 保持當前模型
---
```

**動態適應**：Skill 內容可用 `${CLAUDE_EFFORT}` 讀到當前等級（回傳 `low`/`medium`/`high`/`xhigh`/`max`；ultracode 回報為 `xhigh`），據此調整指令內容。這讓同一個 Skill 可以在低 effort 時給精簡步驟、高 effort 時展開完整檢查表。

**一次性深度推理**：在 Skill 內容任何地方寫入 `ultrathink`，即可在該 skill 執行時要求更深的推理。

**設定管道整理：**

| 方式 | 範圍 |
|---|---|
| `CLAUDE_CODE_EFFORT_LEVEL` 環境變數 | 最高優先，所有 session |
| `--effort` 啟動旗標 | 該 session |
| `/effort <level>` 或 `/effort auto` | 互動式切換，low~xhigh 會跨 session 保留 |
| `settings.json` 的 `effortLevel` | 接受 low/medium/high/xhigh，**不接受 max** |
| Skill / subagent frontmatter 的 `effort` | 該 skill/subagent 啟用期間 |

### 7.5 跨介面／跨模型的遵從性實務建議

| 情境 | 建議 |
|---|---|
| Skill 沒被觸發 | 檢查 description 是否含使用者會自然說出的關鍵字；問 Claude「What skills are available?」確認有載入；直接 `/skill-name` 叫它 |
| Skill 觸發後就失效 | 內容通常還在 context，是模型選擇了別的路徑。強化 description 與指令，或改用 **hooks** 做確定性強制 |
| Skill 太常觸發 | description 寫更具體，或加 `disable-model-invocation: true` |
| 多步驟紀律型 Skill | 提高 effort；不要靠 prompt 繞過淺推理 |
| Skill 很大或中間叫過很多別的 skill | compaction 後重新叫用一次，恢復完整內容 |
| description 被截斷 | 每個 entry 的 description + when_to_use 合計上限 1,536 字元，**把最關鍵用途寫在最前面**；listing 總預算為模型 context window 的 1%，可用 `skillListingBudgetFraction` 調高，或把低優先 skill 設為 `"name-only"` |
| 跨模型部署 Skill | 別假設 `xhigh` 一定存在；不支援時會自動降級 |
| 要在 Cowork 用 | 只能用標準 6 個 frontmatter 欄位，且 `!` 動態注入不會執行 |

### 7.6 用 skill-creator 做評估

「看到 skill 被觸發」只證明 Claude 找到了它，不證明它做了使用者要求的事。要分開量測兩件事：**Claude 是否在該觸發的 prompt 上觸發**，以及**觸發時輸出是否符合預期**。

方法是 baseline 比較：收集幾個真實 prompt，在**全新 session** 中分別在「有 skill」與「停用 skill」下各跑一次比對（全新 session 很重要，撰寫 skill 時殘留的 context 會掩蓋指令中的漏洞）。

```bash
/plugin install skill-creator@claude-plugins-official
```

它會幫使用者：把測試案例存進 skill 目錄的 `evals/evals.json`、為每個案例開獨立 subagent 保證乾淨 context、評分寫入 `grading.json`、把 with/without skill 的通過率與 token 成本彙整進 `benchmark.json`、對兩個版本做盲測 A/B、產生 should-trigger 與 should-not-trigger prompt 來調校 description、並開一份 HTML 報告讓使用者留下質性回饋供下一輪讀取。

---

## 8. 撰寫 Skill 的實務原則

1. **`description` 是最重要的一行**：它決定 Claude 會不會找到使用者的 skill。寫使用者會自然說出的關鍵字，把最關鍵用途放最前面
2. **`SKILL.md` 保持 500 行以內**：詳細參考資料拆到獨立檔案，並在 SKILL.md 說明「哪個檔案裝什麼、何時載入」
3. **本體要精簡**：一旦載入就跨回合留在 context，每一行都是重複的 token 成本。**只說要做什麼，不要敘述為什麼跟怎麼樣**
4. **寫成常駐指令而非一次性步驟**：Claude Code 不會在後續回合重讀檔案
5. **有副作用的加 `disable-model-invocation: true`**：因為不會希望 Claude 因為「程式碼看起來準備好了」就自己決定部署
6. **`context: fork` 只對有明確任務指令的 skill 有意義**：純指引型的 skill 被 fork 後，subagent 收到規範卻沒有可執行的 prompt，會空手而回
7. **腳本比 prompt 可靠**：需要確定性結果時（產生 HTML 報告、跑檢查），把工作放進 bundled script，讓 Claude 只負責編排
8. **審查來自 repo 的 skill**：`allowed-tools` **不受 workspace trust 把關**，一個 checked-in 的 skill 可以自己授予自己廣泛的工具權限。在陌生 repo 跑 Claude Code 前先看過

---

## 9. 三個常見誤解

| 誤解 | 實情 |
|---|---|
| 「Skill 會跨介面同步」 | ❌ 自訂 Skill **不會**自動跨介面同步。claude.ai 帳號的 Skill 與本機 `~/.claude/skills/` 是兩套 |
| 「Cowork 會讀電腦上的 skill」 | ❌ Cowork 與 cloud session 只讀 claude.ai 帳號啟用的 Skill。要上傳才行 |
| 「Skill = Plugin」 | ❌ Skill 是**單一能力**（一個含 SKILL.md 的資料夾）；Plugin 是**打包容器**，可以同時帶 skills、commands、agents、hooks、MCP servers |

---

## 參考連結

- [Claude Code — Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Claude Platform — Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic 支援中心 — Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Agent Skills 開放標準](https://agentskills.io)
- [anthropics/skills（官方開源 Skill）](https://github.com/anthropics/skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [Claude Platform — Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code — Model configuration](https://code.claude.com/docs/en/model-config)

---

> 註一：本文對 claude.ai 與 Claude Desktop 的功能描述以 2026 年 8 月 23 日的產品行為為準。關於內建 Skill 內容日後都可能改變。

> 註二：本文關於個人建立之 Skills 以 2026 年 8 月 23 日的更新為準。內容可能在日後都會有更新。
