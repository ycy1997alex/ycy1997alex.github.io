---
title: "Day 27｜從能跑到能發布：用測試守住架構，打造可部署的股票分析工具"
date: 2026-09-10T00:00:00+08:00
authors: ["Alex Yu"]
series: ["iThome 2026 Ironman"]
tags: ["Claude", "iThome"]
---

> **This post is in Traditional Chinese Only.**

> Originally published on [iThome 2026 Ironman Contest](https://ithelp.ithome.com.tw/articles/10409227).

> 本篇階段：Prj#5 股票分析

> 使用介面：Claude Code（via VS Code）

---

## 前情

前三天都在講資料跟評分。今天講把它裝起來的那些事：架構長什麼樣、界線靠什麼守、SQLite 為什麼在這裡、桌面程式怎麼做、相依與版本號怎麼固定，以及怎麼打包成一個可以發出去的 exe。

今天的主線是一個對比。這個專案裡幾乎每一條規矩都寫成了測試：分層界線、Port 抽象、CI 不准碰金鑰、輸出不准出現行動字眼等。

---

> ```重要說明：本文所有數字與敘述僅為個人技術實作紀錄，```**```不構成投資建議```**```。```

---

## 1. 架構：分層，表現層用 MVP

Day 24 講過那條界線（畫面層不准 import 儲存層），這裡講它實際長什麼樣。

```
   app/views + app/presenters + render/      ← 驅動側 adapter
                    │ 只認 Port（Protocol）
   ─────────────────▼─────────────────
   Domain Core：indicators / scoring / weighting / freshness
   定義 Port：PriceRepository、MacroRepository、
             ScoreHistoryRepository、ChipRepository
   ─────────────────┬─────────────────
                    │ 實作
   SqliteRepo / InMemoryRepo / YFinanceSource / Shioaji…
```

### 1.1 Port 就是一個 Protocol，沒有基底類別

「介面定義在內層、實作在外層」聽起來很抽象，實際上它就是一個 `Protocol`：

```python
@runtime_checkable
class PriceRepository(Protocol):
    def upsert_prices(self, bars: list[PriceBar]) -> int: ...

    def get_prices(
        self,
        symbol: str,
        start: dt.date | None = None,
        end: dt.date | None = None,
    ) -> list[PriceBar]: ...

    def last_price_date(self, symbol: str) -> dt.date | None: ...
```

用 `Protocol` 而不是 `ABC` 有一個具體差別：**實作不必 import 這個介面**。`SqliteRepo` 沒有繼承任何東西，長得對、型別檢查就過。這讓依賴方向真的是單向的：domain 定義形狀，storage 去符合它，而 storage 不需要反過來認識 domain。

`PriceBar` 這個 dataclass 上還釘了一條單位規則：`volume_shares` 一律是**股**。台股顯示成「張」是顯示層除以 1000 的事，資料層不做這個換算，也不存張。欄位名把單位寫進去，就沒有「這個欄位到底是哪個單位」的餘地。

### 1.2 界線是三個測試守著的，不是靠自律

```python
def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            ...
    return found
```

用 AST 走訪而不是字串比對，理由很實際：註解裡提到 `storage`、docstring 裡舉例寫了 `import storage`，都不該讓測試變紅。`ast.parse` 只看真正的 import 節點。相對 import（`from ..storage import x`）也要還原成完整模組名，不然 `node.module` 拿到的是半截字串，規則就漏了。

三個測試各守一個方向：

- **表現層不得 import `storage` / `datasources`**：畫面只能透過 Port 拿資料。
- **domain 不得 import 任何外層**（`storage`、`datasources`、`render`、`app`、`pipeline`）：核心不知道 SQLite 存在。
- **domain 零 I/O**：連 `sqlite3`、`requests`、`pathlib`、`os` 都在禁用清單上。

第三條最嚴格，而它也是最有用的。純函式加零 I/O 的直接後果是：指標與評分那幾個模組的測試全部離線、幾毫秒跑完，可以放心塞一堆邊界案例進去。

### 1.3 同一組測試餵兩個實作

Port 抽得對不對，光看程式碼看不出來，驗收的方式是拿同一組測試同時餵兩個實作：

```python
@pytest.fixture(params=["sqlite", "memory"])
def repo(request, tmp_path):
    if request.param == "sqlite":
        r = SqliteRepo(tmp_path / "test.db")
        r.init_schema()
        yield r
        r.close()
    else:
        yield InMemoryRepo()
```

`params` 讓底下每一個測試自動跑兩遍，兩邊都過，才證明「表現層拿到哪一個實作都沒有差別」這句話是真的，而不只是希望。

實際上這組測試抓到過幾個不對稱：排序、upsert 覆寫的語意、查不到的時候回空 list 還是 `None`。這些在單一實作底下永遠不會浮出來，因為呼叫端跟實作是同一個人寫的，會不自覺地配合。

目前 `src/` 6,236 行、`tests/` 3,364 行，測試大約是程式的一半。

---

## 2. SQLite 在這裡做什麼

### 2.1 它不是真相，是加速層

這套東西的真相在外部 API。SQLite 存的是快取與算出來的東西，把資料庫檔案刪掉，程式還是能跑，只是每次都要重抓。

「刪掉還能跑」不是一句自我安慰，它是有具體後果的設計立場：所有 schema 建立語句都寫成 `CREATE TABLE IF NOT EXISTS`，開檔的時候無條件跑一次；沒有任何一段程式碼假設某張表裡本來就有東西；查不到就是查不到，回空 list，由上層決定要不要去抓。反過來說，一旦有任何一個數字**只存在於這個 .db 檔裡**、外部再也拿不回來，這個定位就破了，而那正是 Day 28 要講的「補不回來的東西」。

第一行 `PRAGMA journal_mode = WAL` 也是為此，因為 WAL 讓讀跟寫可以同時進行，桌面程式在前景讀 `score_history` 的同時，背景那條管線可以照常寫入。用預設的 rollback journal 的話，寫入會鎖住整個檔案，畫面就會卡在那裡等。

### 2.2 七張扁平表，零 JOIN

```sql
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS price_daily (
    symbol        TEXT NOT NULL,
    date          TEXT NOT NULL,          -- ISO YYYY-MM-DD
    open          REAL,
    high          REAL,
    low           REAL,
    close         REAL,
    volume_shares REAL,                   -- 一律「股」，顯示層才換算成張
    source        TEXT NOT NULL,          -- shioaji / yfinance / yf_only / stale
    as_of         TEXT NOT NULL,
    stale         INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (symbol, date)
);

CREATE TABLE IF NOT EXISTS score_history (
    scope          TEXT NOT NULL,         -- macro_world / macro_tw / index / stock
    symbol         TEXT NOT NULL,
    as_of          TEXT NOT NULL,
    score          REAL NOT NULL,
    subscores_json TEXT NOT NULL,
    price_version  TEXT NOT NULL,         -- 用哪一版價格算的
    PRIMARY KEY (scope, symbol, as_of)
);
```

**日期存 ISO 字串不存 SQLite 的 date 型別**，因為 SQLite 根本沒有日期型別，存字串至少排序是對的，而且拿出來 `dt.date.fromisoformat()` 一行就還原。**複合主鍵直接當去重機制**：`(symbol, date)` 撞到就 upsert 覆寫，不必自己先查再決定 insert 還是 update。**`subscores_json` 直接塞 JSON**，因為分項的鍵會隨維度增減而變，開成欄位的話每加一個維度就要改 schema。

`price_version` 那一欄是後來補的，記著「這個分數是用哪一版價格算的」。價格會被回頭改寫（Yahoo 補一格缺值就會），沒有這一欄就分不出「分數變了」是因為程式改了還是因為價格改了。

### 2.3 後悔了嗎？

**沒後悔的**：評分歷史放 SQLite 是對的。桌面那兩個大盤分頁直接讀 `score_history` 不重算，沒有這張表的話桌面得自己算一次。

**代價是啥**：多了一個要維護的 schema。這三天加 `chip_daily` 一張表，連帶動了 Port 定義、兩個 adapter、合約測試四個地方。

**最務實的**：SQLite 的價值不在「存資料」，在「不用自己寫查詢邏輯」。`get_scores(scope, symbol)` 回一條排好序的序列，用 CSV 做要自己讀檔、排序、過濾。省下來的是那個。

---

## 3. 桌面程式

### 3.1 兩種更新，行為必須不同

程式有四個分頁：世界總經、台灣總經、台股大盤與 ETF、美股大盤與 ETF，跟網頁端一致。

**後面兩個分頁是我補要求的。** Claude 給的第一版桌面程式只有總經那兩頁，理由是「大盤評分已經在網頁上了」。但那等於要我為了看一個數字去開瀏覽器、輸入密碼、再關掉，而桌面程式本來就是為了省掉那些步驟才存在的。

補進去的做法是直接讀 `score_history`，不重算。真正花時間的是另一件事：Presenter 不能認得 SQLite，所以它拿的是 `ScoreHistoryRepository` 這個介面。分層的代價與好處在這裡同時出現，多繞了一層，但那一層的測試全部離線。

更新分成兩種：

- **到期自動更新**：背景每十分鐘檢查一次。**檢查本身不打網路**，它只讀本機快取的資料日期，跟各序列自己的公布頻率比，真的有東西到期才出去抓。
- **強制重抓**：一顆按鈕，按下去一定打網路，忽略快取重新掃一次。

「到期」按各序列自己的頻率算，不是固定間隔。CPI 每月出一次，每小時去問二十四次不會讓它早一點出現。而央行重貼現率沒有預期時間，那條用一週掃一次的慢節奏，不能永遠不抓，不然真的調息了也不會知道。

**切分頁一律只讀本機快取，一次網路都不打。**

這三種行為從畫面上完全看不出差別，都只是「畫面刷新了」。所以寫成三個測試：切分頁時假的 refresher 被呼叫零次、沒有東西到期時自動更新呼叫零次、強制重抓一定呼叫一次而且帶 `force=True`。

### 3.2 兩個 tkinter 的坑

**視窗尺寸不能寫死。** 按螢幕解析度算：由上到下 3% 到 87%、由左到右 3% 到 97%。下緣停在 87% 是留給工作列的。

**更新不能跑在主執行緒。** 一次 refresh 要打十幾個網路請求，跑在主執行緒上等於視窗凍住十幾秒，使用者只會覺得它當掉了。所以工作丟到 daemon 執行緒，結果走 `queue.Queue` 回傳，主執行緒用 `after()` 輪詢，**背景執行緒一律不碰任何 widget**。

關窗也要攔，而且順序不能換：先取消所有排程中的 `after` callback，再等背景執行緒 join，最後才 destroy。少了第一步，關窗後那些 callback 會炸 `invalid command name`；少了第二步，抓到一半的執行緒會變成孤兒。

---

## 4. 發布：本機加密，Actions 只部署

### 4.1 分工

```
本機：抓 → 交叉比對 → 算分 → 產明文 HTML → 加密
         ↓                                  ↓
   資料層（DB、CSV、明文、密碼）        docs/index.html（只有密文）
   完全不進任何 repo                          ↓ push
                                    GitHub Actions：只部署，不抓資料
```

**本機是唯一的寫入者，Actions 只是 renderer。**

### 4.2 一個很有意思的衝突（這部分我比較不清楚，是由 Claude 所提供的說明）

加密那邊有一條硬規定：**每次發布重新產生 salt、IV、內容金鑰**。AES-GCM 在同一把金鑰下重用 IV，機密性與完整性會同時崩掉，不是理論弱化，是可以直接還原明文。

而排程那邊也有一條硬規定：**資料沒變就不 commit**。不必維護交易日曆，颱風假、國定假日、資料延遲全自動處理掉。

這兩條正面對撞。因為每次都換隨機數，密文**每次都不一樣**，拿 `docs/index.html` 去比「有沒有變」永遠會說「變了」。結果就是每天多一筆內容完全相同、只有隨機數不同的 commit。

解法是把判斷移到加密**之前**：閘門比對的是**明文的指紋**，不是密文。明文一樣就整個跳過封裝，連 `docs/` 都不碰。

實測連跑兩次，第二次 `docs/index.html` 位元組沒動。兩條規定就都成立了：該換的隨機數在真的要發的時候還是每次都換，只是「要不要發」在那之前就決定了。

### 4.3 發布之後的驗收

`tools/verify_publish.py` 有十項檢查，每次發布後跑。其中最不能靠肉眼的是這一條：

> 連續兩次發布的 `content.iv`、每個 `keys[i].salt`、`keys[i].iv` 全都不同

沒有人能用眼睛比對 base64，這種檢查一定要寫成程式。

其他幾項：每組憑證逐一測過解得開、錯誤憑證只得到失敗、密文裡 grep 不到密碼、`docs/` 沒有資料檔、明文沒有行動字眼。

---

## 5. 什麼是 CI/CD，以及這個 repo 用到哪幾段

CI（持續整合）是每次推程式碼上去就自動跑一輪檢查，CD（持續交付／部署）是檢查過了就自動把成果送出去。兩個詞常被連在一起講，但它們是兩件事，而且可以只做其中一半。

### 5.1 兩條 workflow，各做一件事

這個 repo 只有兩個檔案：

| workflow | 觸發 | 做什麼 |
|---|---|---|
| `pages.yml` | push 到 main 且 `docs/**` 有變動 | 部署 GitHub Pages（純 CD） |
| `release.yml` | 打一個 `v*` tag | 跑測試 → 打包 exe → 掛上 Release（CI + CD） |

`pages.yml` 的觸發條件用 `paths` 限定在 `docs/**`，所以改程式碼、改測試、改文件都不會觸發部署。這一條跟第 4.2 節那個明文指紋閘門是同一件事的兩層：閘門決定「要不要產生新的 `docs/`」，`paths` 決定「`docs/` 沒變就不要跑部署」。

CI 的部分只有跑測試，而且是掛在打包那條流程裡順便跑的：`pip install pytest` 然後 `python -m pytest -q`，測試不綠就不會有 exe。

嚴格說這不算標準的 CI：真正的 CI 是**每一次 push 都跑**，早一點知道壞在哪；這裡只有打 tag 的時候才跑，等於把檢查延後到要發布的那一刻。會這樣配是因為本機每次收工都會跑一輪完整測試，Actions 那一遍的作用比較接近「發布前的最後一道閘」，而不是日常的回饋迴圈。

至於 CD，這個 repo 的兩條「交付」路徑其實形狀不同：Pages 那條是**內容部署**，把產好的靜態檔送上去；Release 那條是**產物交付**，把 exe 掛到一個可以下載的地方。兩者的觸發來源也不同：前者由資料驅動（`docs/` 變了），後者由人驅動（我打了 tag）。資料每天變，版本一年動幾次，把它們綁在同一條流程裡會讓其中一邊被另一邊的節奏拖著走。

刻意**沒有**做的：CI 裡不抓資料、不寫資料、不引用任何 secret。

### 5.2 CI 不需要金鑰，而且有一支測試守著

```python
@pytest.mark.parametrize("wf", WORKFLOWS, ids=lambda p: p.name)
def test_no_secret_references(wf: Path):
    """`secrets.GITHUB_TOKEN` 也不行 — 需要它就用 permissions，不用引用。"""
    text = wf.read_text(encoding="utf-8")
    offenders = [
        line.strip()
        for line in text.splitlines()
        if "secrets." in line and not line.strip().startswith("#")
    ]
    assert not offenders, f"{wf.name} 引用了 secret：\n  " + "\n  ".join(offenders)
```

這條規則看起來像廢話：沒有金鑰當然掃不到 `secrets.`。但它是整個架構決定的證據：因為排程放本機、CI 只做部署，所以 CI 不需要任何金鑰。

它真正的用途在未來。哪天有人（很可能是我自己，或是我叫來的 Claude）為了方便，在 Actions 裡加一支抓資料的 job，第一件要做的事就是往 workflow 裡塞 `secrets.FRED_KEY`。這支測試會在那一刻擋下來，而不是等到金鑰外洩才發現。

連 `secrets.GITHUB_TOKEN` 都不放行：Actions 要寫 Release，用 `permissions: contents: write` 宣告就好，不必引用那個變數。禁一個字串比禁「不好的用法」容易守得多。

同一支測試檔還守著另一條：workflow 裡不准出現 `yfinance`、`shioaji`、`run_macro` 這些字眼，**CI 不抓資料、不寫資料**。

### 5.3 Pages 怎麼開：五步，其中第四步最容易漏

`pages.yml` 寫得再對，Pages 沒開就什麼都不會發生。開的地方不在 repo 裡，在網頁介面上：

1. 進 repo 的 **Settings**（齒輪那排，不是帳號的 Settings），左邊側欄找 **Pages**。
2. **Build and deployment** 底下的 `Source` 下拉選單，改成 **GitHub Actions**。預設是 `Deploy from a branch`，這一格就是這一節的重點。
3. 選完不必按儲存，也不會立刻長出網站，它只是把「誰有權發布」交給 workflow。
4. **回去讓 workflow 真的跑一次。** 改設定不會回頭重發已經在線上的東西。這裡是 `on: push` 且限定 `docs/**`，所以要嘛推一次真的動到 `docs/` 的 commit，要嘛去 Actions 頁面手動 `Run workflow`（`pages.yml` 有留 `workflow_dispatch` 就是為了這個）。
5. 驗收看兩個地方：Actions 那頁的 `Deploy Pages` 是綠的，然後打開 `https://<帳號>.github.io/<repo>/` 看到的是自己的東西。

還有一件跟加密有關的事：**public repo 的 Pages 一定是公開的**，沒有「只有我看得到」這個選項（Private Pages 要付費方案）。所以這個系列的內容不是靠 Pages 的權限擋，是靠推上去的東西本身就是密文。

**兩個選項的差別不只是措辭。** 選 `Deploy from a branch`，GitHub 會用自己的邏輯處理那個分支：沒有 `.nojekyll` 就套 Jekyll，抓 README 產首頁，跟 repo 裡那條 workflow 完全無關。workflow 綠燈只代表它自己那幾個步驟跑完了，不代表網站照它的產物更新。這兩件事各自獨立地成立或失敗，中間沒有互相檢查的機制。

### 5.4 選錯的樣子

打開網站才看出問題：首頁卻是一份用 README 拼出來的說明頁，不是舊版內容，是完全不對的內容。

原因是 market-barometer 的 `Source` 那一格還停在 `Deploy from a branch: master /(root)`，從沒切過去。GitHub 因此用 Jekyll 處理 `master` 分支根目錄，把 README 當成首頁；工作流程確實把最新的密文推進了 `docs/`，但那份內容變成網站底下一個要打完整網址才進得去的子路徑，不是首頁本身。`pub_id` 對得上、內容也是新的，只是不在任何人會走到的那個網址上。

**Actions 列表裡其實有徵兆，只是要知道往哪看。** 選錯的那個 repo，每次 push 都會跑兩條流程：一條是 `Deploy Pages`，我自己寫的；另一條叫 `pages build and deployment`，我沒寫過這個檔案，是 GitHub 在分支模式下自己掛上去的。**列表裡出現一條自己沒寫過的 workflow，就是 `Source` 還停在分支模式的證據**，而且它比打開網站比對內容快得多。切成 `GitHub Actions` 之後，那一條就不再出現了。

這一格也是「測試守不到」的另一個實例。第 5.2 節那支測試掃得到 workflow 檔案裡的每一行，因為那是 repo 裡的檔案；`Source` 這一格不在 repo 裡，它是 GitHub 帳號底下的一筆設定，`git clone` 拿不到、`pytest` 看不到、換一個人 fork 過去還要自己再設一次。

雖然上面說了一堆失敗案例，不過 Claude 看得出錯誤也能告訴我怎麼改。 

---

## 6. 相依套件與環境怎麼固定

「相依固定」在這個專案裡分成三層，各解決不同的問題。

**第一層：`pyproject.toml` 把選配相依切出去。**

```toml
dependencies = [
    "yfinance>=1.2.0",
    "pandas>=2.2",
    "numpy>=2.0",
    "requests>=2.32",
    "cryptography>=42.0",
]

[project.optional-dependencies]
tw = ["shioaji>=1.3.2"]
dev = ["pytest>=8.0"]
```

`shioaji` 在 `[tw]` 裡，不在 base。這不是為了讓安裝快一點，是為了讓「要發出去的東西」跟「有下單能力的套件」在依賴圖上就分開。

**第二層：CI 只裝 base。**

```yaml
      - name: 安裝相依
        run: |
          python -m pip install --upgrade pip
          pip install .
          pip install pyinstaller==6.11.1
```

`pip install .` 裝的是 base，沒有 `[tw]`。所以就算 `.spec` 的 `excludes` 哪天寫錯，shioaji 也不可能被打包進去，它根本不在那台機器上。**兩層各自獨立地保證同一件事**，這種重複是划算的。

---

## 7. 版本號與釋出管理

版本號只有一個來源：**tag 本身**。

```yaml
on:
  push:
    tags: ['v*']
```

打一個 `v0.1.0`，Actions 就從那個 tag 推導出版本號 `0.1.0`，不另外維護一份版本檔。

理由是「同一個事實不要記兩次」。版本號如果同時寫在 `pyproject.toml`、`__init__.py` 跟 Release 標題上，遲早會有一份先改、另外兩份忘了跟。而這種不一致不會讓任何測試變紅，只會讓某一天有人下載到一個自稱 0.2.0、實際上是 0.1.9 的 exe。

代價是要記得打 tag，而且 tag 打錯了不能改：強行覆蓋一個已經推出去的 tag 等於改歷史，別人拉下來的版本會跟我這邊的不一樣。處置是往前補一個新的 patch tag，把錯的那個標成作廢，不回頭改。這個代價比「三個地方對不起來」小得多。

有一個更自動的做法是用 `setuptools-scm` 之類的工具，讓 `pyproject.toml` 裡的版本號直接從 git 描述推出來，連 `version = "0.1.0"` 那一行都不必寫。

釋出的內容也有一條規矩：Release 說明裡要寫清楚**這支 exe 不含什麼**：不含任何金鑰、不含 shioaji、資料根目錄走 `STOCKDATA_ROOT` 環境變數、第一次在新機器上跑會是空的。

---

## 8. 打包：三次「成功但跑不起來」

用 PyInstaller onefile 打包成單一 exe，最後 59.4 MB。

驗收條件**不是** `exit 0`、**不是**測試全綠，是：

1. 建置日誌裡零個 `Library not found`
2. **實際啟動 exe，確認視窗真的出現**
3. 出不來的時候，先去讀那個藏起來的錯誤對話框，不要急著重建

第三點省下的時間最多。讀對話框是幾秒鐘的事，重建一次是好幾分鐘，而且重建完看到的還是同一句話。

而第 1 點跟 CI 那個「產物存在檢查」是兩回事：workflow 裡那段 PowerShell 只確認檔案在、而且不是零位元組，它擋得住「打包整個失敗」，擋不住「打包成功但開不起來」。真正的啟動驗證要在一台沒裝開發環境的機器上做，那一項**待補**。

---

## 9. 本機跑 vs 上 GitHub Pages

| | 桌面程式 | GitHub Pages |
|---|---|---|
| 內容 | 四個分頁，跟網頁一致 | 四個分頁 |
| 能不能抓資料 | **可以**，按鈕會打網路 | 不行，純靜態 |
| 資料新鮮度 | 有到期判定、有自動更新 | 發布當下的靜態快照 |
| 走勢圖 | 沒有（純表格） | 有（inline SVG） |
| 誰看得到 | 有打包後檔案的人 | 有密碼的人 |

一句話：**桌面程式是操作台，網頁是發布出去的成果。**

部署上真正的差別在於：這是一個**資料型網站**。內容型網站改了文章才部署，一個月幾次；資料型網站每天都有新數字，不加限制就是每天一次部署、每天一筆 commit。

所以才有第 4.2 節那個閘門與第 5.1 節那個 `paths` 限定。**資料型網站的部署頻率必須由「資料有沒有變」決定，不是由「時間到了沒」決定。**

Pages 那邊的頁面在 https://ycy1997alex.github.io/market-barometer/ ，需要密碼才進得去。密碼與它擋得住什麼，明天講。

---

## 小結

今天最實在的一句話是第 8.3 節那個：**「完成」不是 `exit 0`，是視窗真的開出來。**

但更值得記的是那個對比。架構那一層的規矩全都寫成了測試：分層界線用 AST 掃、Port 抽象用同一組測試餵兩個實作、CI 不准碰金鑰用字串掃描，這些規矩守得住，因為它們的違反方式是「程式碼裡多了一行」，而那是測試看得見的東西。

## 參考資料

工具文件

- GitHub Actions：部署 Pages — https://github.com/actions/deploy-pages
- GitHub Actions 的 permissions — https://docs.github.com/actions/using-jobs/assigning-permissions-to-jobs
- GitHub Pages 官方說明 — https://docs.github.com/pages
- 設定 Pages 的發布來源（Deploy from a branch vs GitHub Actions） — https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

其他參考

- Ports and Adapters（Hexagonal Architecture） — https://alistair.cockburn.us/hexagonal-architecture/
- PEP 544：Protocols（結構型子型別） — https://peps.python.org/pep-0544/
- SQLite 官方文件 — https://www.sqlite.org/docs.html
- SQLite WAL 模式 — https://www.sqlite.org/wal.html

---

> 註一：文中的打包失敗、圖示問題與視窗行為，皆為 2026 年 9 月 7 日至 10 日在 Windows 11 + Python 3.13 + PyInstaller 6.11.1 環境下的**單次實測**，屬於定性觀察；不同版本組合的行為可能不同。

> 註二：exe 體積 59.4 MB 是 onefile 模式、含 numpy 與 ttkbootstrap 的結果，**未做體積最佳化**。

> 註三：`tag → CI 打包 → 掛上 Release` 這條流程，在 CI 目前只檢查產物存在且不是零位元組。

> 註五：第 5.3、5.4 節的操作步驟與畫面位置，是 2026 年 9 月 7 日至 10 日當下的 GitHub 網頁介面；**選單措辭與欄位位置會隨產品改版變動**，照著點不到的話以官方文件為準。來源設錯的症狀與切換後的結果同為當天在 market-barometer 上的**單次實測**，屬定性觀察。

---

> ```重要說明：本文所有數字與敘述僅為個人技術實作紀錄，```**```不構成投資建議```**```。```
