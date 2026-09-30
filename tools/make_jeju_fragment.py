# -*- coding: utf-8 -*-
"""產生 assets/fragments/2026-jeju.html。

版型、樣式與互動腳本整套沿用 tools/make_setouchi_fragment.py，只把 class 前綴從
seto- 換成 jeju-、配色換成濟州的玄武岩海藍＋柑橘，內容改成 2026/10 濟州島員工旅遊。

跟瀨戶內海那支一樣，這個 fragment 會被 {{< webapp >}} shortcode 原封不動塞進文章頁，
所以沒有 <html>/<head>，只有一段 <style>、一塊 markup、一段 <script>。
  1. 主題把 html 設成 font-size: 62.5%，所以 1rem = 10px。
  2. 深色模式由主題掛在 body 上的 .colorscheme-dark 控制，不是 prefers-color-scheme。

公開版刻意拿掉的東西（原始手冊裡有）：分房名單與備註、領隊與業務的姓名和手機、
海外緊急聯絡人的姓名與電話、公司名稱。飯店是營業場所，地址電話保留，填電子入境卡用得到。

地圖座標是概略值，只用來放圖釘；Google 地圖與導航連結改用地名搜尋（q 欄位），
這樣就算圖釘偏個幾百公尺，點出去還是會導到對的地方。
"""

import io, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "assets", "fragments", "2026-jeju.html")

DAYS = [
    ("D1", "10/17（六）", "桃園・濟州市・東門市場", "Air City Hotel Jeju"),
    ("D2", "10/18（日）", "雪綠茶園・西歸浦・藥泉寺", "Air City Hotel Jeju"),
    ("D3", "10/19（一）", "蓮洞・涯月海岸・神話世界", "神話世界 萬豪酒店"),
    ("D4", "10/20（二）", "城山日出峰・松堂・ECO LAND", "神話世界 萬豪酒店"),
    ("D5", "10/21（三）", "濟州・桃園", "當日返台"),
]

TABS = [
    ("overview", "總覽"),
    ("days", "分日行程"),
    ("map", "互動地圖"),
    None,
    ("preflight", "行前檢查"),
    ("korea", "入境韓國"),
    ("taiwan", "入境台灣"),
    None,
    ("out", "去程清單"),
    ("back", "回程清單"),
    ("souvenir", "伴手禮採買"),
]

# ── 地圖點位。(天, 時間, 名稱, 類別, lat, lng, 說明, Google 搜尋字串)
#    跆拳武藝秀、騎駱駝、Marina K.C 手冊沒寫地點，不放進地圖。──
AIRCITY = (33.4885, 126.4901, "Hotel Air City Jeju")
MARRIOTT = (33.3052, 126.3190, "Jeju Shinhwa World Marriott Resort")
CJU = (33.5104, 126.4914, "Jeju International Airport")
TPE1 = (25.0777, 121.2320, "Taoyuan International Airport Terminal 1")

POINTS = [
    (1, "12:00", "桃園機場 第一航廈", "機場", TPE1[0], TPE1[1], "泰瑞航空 11 號團體櫃台集合｜TW688 14:30 起飛", TPE1[2]),
    (1, "17:30", "濟州國際機場 CJU", "機場", CJU[0], CJU[1], "韓國時間，比台灣快 1 小時", CJU[2]),
    (1, "傍晚", "東門傳統市場", "自由", 33.5122, 126.5268, "停留約 1–1.5 小時｜夜市小吃、橘子", "Dongmun Traditional Market Jeju"),
    (1, "晚上", "Air City Hotel Jeju", "住宿", AIRCITY[0], AIRCITY[1], "第 1 夜｜新濟州蓮洞", AIRCITY[2]),
    (2, "上午", "O'sulloc 雪綠茶博物館", "景點", 33.3059, 126.2895, "綠茶主題館與茶園", "O'sulloc Tea Museum"),
    (2, "上午", "innisfree 濟州小屋", "景點", 33.3049, 126.2916, "玻璃建築的品牌體驗館", "innisfree Jeju House"),
    (2, "中午", "西歸浦每日偶來市場", "自由", 33.2497, 126.5636, "午餐 ₩8,000 自理｜《我們的藍調時光》", "Seogwipo Maeil Olle Market"),
    (2, "下午", "藥泉寺", "景點", 33.2467, 126.4634, "大寂光殿｜《Island》拍攝地", "Yakcheonsa Temple Jeju"),
    (2, "晚上", "Air City Hotel Jeju", "住宿", AIRCITY[0], AIRCITY[1], "第 2 夜", AIRCITY[2]),
    (3, "上午", "蓮洞購物商圈", "自由", 33.4878, 126.4919, "450 公尺行人步行街（蠶丘路）", "Nuwemaru Street Jeju"),
    (3, "中午", "漢潭海岸散步路", "景點", 33.4623, 126.3102, "涯月海岸咖啡街", "Handam Coastal Walk Aewol"),
    (3, "14:00", "神話主題樂園", "自由", 33.3067, 126.3169, "三項設施券＋韓服變裝 4 小時", "Shinhwa Theme Park Jeju"),
    (3, "18:00", "神話世界 萬豪酒店", "住宿", MARRIOTT[0], MARRIOTT[1], "第 3 夜｜5F 五雲閣自助晚餐", MARRIOTT[2]),
    (4, "上午", "城山日出峰", "景點", 33.4586, 126.9410, "停留 60–90 分｜登頂約 30 分", "Seongsan Ilchulbong"),
    (4, "下午", "松堂童話村＋星巴克 R 店", "景點", 33.4630, 126.7770, "星巴克飲料自理", "Starbucks The Jeju Songdang Park R"),
    (4, "下午", "ECO LAND", "景點", 33.4565, 126.6677, "英式森林小火車", "Eco Land Theme Park Jeju"),
    (4, "晚上", "神話世界 萬豪酒店", "住宿", MARRIOTT[0], MARRIOTT[1], "第 4 夜", MARRIOTT[2]),
    (5, "早上", "神話世界 萬豪酒店", "住宿", MARRIOTT[0], MARRIOTT[1], "早餐後退房", MARRIOTT[2]),
    (5, "10:20", "濟州國際機場 CJU", "機場", CJU[0], CJU[1], "起飛前 2 小時報到｜TW687 12:20 起飛", CJU[2]),
    (5, "13:25", "桃園機場 第一航廈", "機場", TPE1[0], TPE1[1], "抵台", TPE1[2]),
]

# ── 去程清單。(區塊標題, 提示, group, [(小節, [(id, 標籤)])]) ──
OUT_LIST = [
    ("身上", "每日必檢查", "body", [
        ("", [("ob1", "眼鏡"), ("ob2", "手機"), ("ob3", "手錶")]),
        ("穿著", [("ow1", "長袖上衣"), ("ow2", "長褲"), ("ow3", "防風外套"), ("ow4", "運動鞋")]),
        ("護照＆錢包", [("op1", "護照（效期 6 個月以上）"), ("op2", "身分證"), ("op3", "健保卡"),
                        ("op4", "信用卡（錢包）"), ("op5", "韓幣現金（錢包）"), ("op6", "台幣現金（錢包）")]),
    ]),
    ("隨身後背包", "手提限 1 件 10 kg；每容器 &lt; 100 ml、總液體 &lt; 1 L，塑膠袋裝", "bag", [
        ("電器類", [("oe1", "行動電源（≤ 100 Wh、孔貼絕緣）"), ("oe2", "充電線"), ("oe3", "充電器"),
                    ("oe4", "Sim 卡／eSIM"), ("oe5", "藍芽耳機"), ("oe6", "有線耳機（+ 轉接頭）")]),
        ("衛生用品類", [("oh1", "濕紙巾"), ("oh2", "衛生紙"), ("oh3", "面紙"),
                        ("oh4", "餐具"), ("oh5", "免洗餐具"), ("oh6", "酒精（&lt; 100 ml）")]),
        ("醫藥用品類", [("om1", "常備口服藥（不帶 EVE）"), ("om2", "暈車藥"), ("om3", "口內膏"),
                        ("om4", "酸痛貼布"), ("om5", "OK 蹦"), ("om6", "透氣膠帶／優肌絆"),
                        ("om7", "眼藥水"), ("om8", "外傷藥膏"), ("om9", "蚊蟲藥")]),
        ("睡覺用品類", [("os1", "人工淚液"), ("os2", "耳塞"), ("os3", "眼罩")]),
        ("日常用品類", [("od1", "眼鏡盒（墨鏡）"), ("od2", "筆"), ("od3", "筆記本／便條紙"),
                        ("od4", "保溫瓶"), ("od5", "機上的水與點心（安檢後買）"), ("od6", "易口舒／口香糖"),
                        ("od7", "保健食品"), ("od8", "口罩"), ("od9", "行李秤"),
                        ("od10", "頸枕（看個人需求）"), ("od11", "摺疊傘"), ("od12", "第二錢包"),
                        ("od13", "鑰匙")]),
    ]),
    ("託運行李", "不限件數，合計 ≤ 20 kg；總液體 &lt; 5 L", "checked", [
        ("衣物", [("oc1", "長袖上衣 ×4"), ("oc2", "長褲 ×4"), ("oc3", "內衣褲 ×4"),
                  ("oc4", "襪子 ×4"), ("oc5", "睡衣 ×2"), ("oc6", "薄毛衣／針織衫 ×1"),
                  ("oc7", "護膝"), ("oc8", "帽子 ×1")]),
        ("萬豪泳池", [("ow5", "泳衣"), ("ow6", "泳帽")]),
        ("外出用品", [("oo1", "止汗劑"), ("oo2", "防曬乳"), ("oo3", "衛生紙備品"),
                      ("oo4", "濕紙巾備品"), ("oo5", "衛生用品")]),
        ("房間用品", [("or1", "拖鞋"), ("or2", "毛巾"), ("or3", "衣架 &amp; 曬衣夾 ×4")]),
        ("保養用品", [("ok1", "護手霜"), ("ok2", "面霜"), ("ok3", "乳液")]),
        ("盥洗與清潔用品", [("oq1", "洗面乳"), ("oq2", "沐浴乳"), ("oq3", "洗髮精"),
                            ("oq4", "洗碗精"), ("oq5", "梳子"), ("oq6", "牙刷"),
                            ("oq7", "牙膏"), ("oq8", "牙線棒"), ("oq9", "刮鬍刀"),
                            ("oq10", "指甲剪"), ("oq11", "小鏡子")]),
        ("電器", [("ot1", "韓國轉接頭（旅行社每人送一個）"), ("ot2", "手錶充電器"), ("ot3", "自拍棒")]),
        ("其他", [("ox1", "隨身垃圾袋"), ("ox2", "折疊登機包"), ("ox3", "購物袋")]),
    ]),
]

BACK_LIST = [
    ("身上", "每日必檢查", "body", [
        ("", [("rb1", "眼鏡"), ("rb2", "手機"), ("rb3", "手錶")]),
        ("穿著", [("rw1", "長袖上衣"), ("rw2", "長褲"), ("rw3", "防風外套"), ("rw4", "運動鞋")]),
        ("護照＆錢包", [("rp1", "護照"), ("rp2", "身分證"), ("rp3", "健保卡"),
                        ("rp4", "信用卡（錢包）"), ("rp5", "韓幣零錢（機場花掉）"), ("rp6", "台幣現金（錢包）")]),
    ]),
    ("隨身後背包", "手提限 1 件 10 kg；每容器 &lt; 100 ml、總液體 &lt; 1 L，塑膠袋裝", "bag", [
        ("電器類", [("re1", "行動電源（≤ 100 Wh、孔貼絕緣）"), ("re2", "充電線"), ("re3", "充電器"),
                    ("re4", "Sim 卡／eSIM"), ("re5", "藍芽耳機"), ("re6", "有線耳機（+ 轉接頭）")]),
        ("衛生用品類", [("rh1", "濕紙巾"), ("rh2", "衛生紙"), ("rh3", "面紙"),
                        ("rh4", "餐具"), ("rh5", "免洗餐具"), ("rh6", "酒精（&lt; 100 ml）")]),
        ("醫藥用品類", [("rm1", "常備口服藥"), ("rm2", "暈車藥"), ("rm3", "口內膏"),
                        ("rm4", "酸痛貼布"), ("rm5", "OK 蹦"), ("rm6", "透氣膠帶／優肌絆"),
                        ("rm7", "眼藥水"), ("rm8", "外傷藥膏"), ("rm9", "蚊蟲藥")]),
        ("睡覺用品類", [("rs1", "人工淚液"), ("rs2", "耳塞"), ("rs3", "眼罩")]),
        ("日常用品類", [("rd1", "眼鏡盒（墨鏡）"), ("rd2", "筆"), ("rd3", "筆記本／便條紙"),
                        ("rd4", "保溫瓶"), ("rd5", "機上的水與點心（安檢後買）"), ("rd6", "易口舒／口香糖"),
                        ("rd7", "保健食品"), ("rd8", "口罩"), ("rd9", "行李秤"),
                        ("rd10", "頸枕（看個人需求）"), ("rd11", "摺疊傘"), ("rd12", "第二錢包"),
                        ("rd13", "鑰匙")]),
    ]),
    ("登機包・託運（伴手禮）", "回程多出來的那些", "shop", [
        ("登機包", [("rg1", "免稅商品"), ("rg2", "非液體物品"), ("rg3", "零食")]),
        ("託運", [("rl1", "酒（&gt; 1.5 公升要申報）"), ("rl2", "果醬、柑橘茶等玻璃罐"),
                  ("rl3", "食品（確認不含肉）"), ("rl4", "藥妝"), ("rl5", "伴手禮"), ("rl6", "保健食品")]),
    ]),
    ("託運行李", "不限件數，合計 ≤ 20 kg；總液體 &lt; 5 L", "checked", [
        ("衣物", [("rc1", "長袖上衣 ×4"), ("rc2", "長褲 ×4"), ("rc3", "內衣褲 ×4"),
                  ("rc4", "襪子 ×4"), ("rc5", "睡衣 ×2"), ("rc6", "薄毛衣／針織衫 ×1"),
                  ("rc7", "護膝"), ("rc8", "帽子 ×1")]),
        ("萬豪泳池", [("rw5", "泳衣（晾乾或裝防水袋）"), ("rw6", "泳帽")]),
        ("外出用品", [("ro1", "止汗劑"), ("ro2", "防曬乳"), ("ro3", "衛生紙備品"),
                      ("ro4", "濕紙巾備品"), ("ro5", "衛生用品")]),
        ("房間用品", [("rr1", "拖鞋"), ("rr2", "毛巾"), ("rr3", "衣架 &amp; 曬衣夾 ×4")]),
        ("保養用品", [("rk1", "護手霜"), ("rk2", "面霜"), ("rk3", "乳液")]),
        ("盥洗與清潔用品", [("rq1", "洗面乳"), ("rq2", "沐浴乳"), ("rq3", "洗髮精"),
                            ("rq4", "洗碗精"), ("rq5", "梳子"), ("rq6", "牙刷"),
                            ("rq7", "牙膏"), ("rq8", "牙線棒"), ("rq9", "刮鬍刀"),
                            ("rq10", "指甲剪"), ("rq11", "小鏡子")]),
        ("電器", [("rt1", "韓國轉接頭"), ("rt2", "手錶充電器"), ("rt3", "自拍棒")]),
    ]),
]

# ── 伴手禮（可勾選）。欄位：id、類別、品項、行程中哪裡買、備註（warn=True 的備註標紅）──
SHOP = [
    ("sj1", "柑橘", "橘子巧克力", "D1 東門市場、D5 機場", "分送同事最方便", False),
    ("sj2", "柑橘", "漢拏峰果醬／柑橘茶", "D1 東門市場、D2 偶來市場", "玻璃罐放託運", False),
    ("sj3", "柑橘", "新鮮橘子、漢拏峰", "D1 東門市場", "在韓國吃完，不能帶回台灣", True),
    ("sj4", "綠茶", "O'sulloc 茶包禮盒", "D2 雪綠茶博物館", "", False),
    ("sj5", "綠茶", "O'sulloc 綠茶抹醬", "D2 雪綠茶博物館", "乳製品，留意保存期限", False),
    ("sj6", "保養", "innisfree 保養品", "D2 innisfree 濟州小屋", "", False),
    ("sj7", "零食", "韓國海苔", "便利商店、機場", "", False),
    ("sj8", "零食", "HBAF 蜂蜜奶油杏仁", "便利商店、機場", "", False),
    ("sj9", "紀念品", "石頭爺爺小物", "市場、機場", "", False),
    ("sj10", "泡麵", "韓國泡麵", "便利商店", "多數含肉類調味粉，入境台灣禁止", True),
]

def esc_attr(s):
    return s.replace('"', "&quot;")


def render_nav():
    o = ['<nav class="jeju-nav" aria-label="分頁">', '  <div class="jeju-pills" role="tablist">']
    for t in TABS:
        if t is None:
            o.append('    <span class="jeju-sep" aria-hidden="true"></span>')
            continue
        pid, label = t
        o.append(
            '    <button class="jeju-pill" type="button" role="tab" data-panel="%s" '
            'id="jeju-tab-%s" aria-controls="jeju-panel-%s" aria-selected="false" tabindex="-1">%s</button>'
            % (pid, pid, pid, label)
        )
    o += ["  </div>", "</nav>"]
    return "\n".join(o)


def render_checklist(key, blocks):
    total = sum(len(items) for _, _, _, subs in blocks for _, items in subs)
    o = ['<div class="jeju-checklist" data-key="%s">' % key]
    o.append('  <div class="jeju-progress">')
    o.append('    <div class="jeju-bar"><i data-fill style="width:0"></i></div>')
    o.append('    <strong class="jeju-count"><span data-count>0</span> / %d</strong>' % total)
    o.append('    <button class="jeju-reset" type="button" data-reset>全部清空</button>')
    o.append("  </div>")
    o.append('  <div class="jeju-groupstats">')
    for title, _, group, subs in blocks:
        o.append('    <span class="jeju-groupstat" data-stat="%s">%s <b>0 / 0</b></span>' % (group, title))
    o.append("  </div>")
    for title, hint, group, subs in blocks:
        o.append('  <h4 class="jeju-sub">%s%s</h4>' % (
            title, (' <span>%s</span>' % hint) if hint else ""))
        for subtitle, items in subs:
            if subtitle:
                o.append('  <p class="jeju-subsub">%s</p>' % subtitle)
            o.append('  <div class="jeju-checkgrid">')
            for cid, label in items:
                o.append(
                    '    <label class="jeju-check" data-id="%s" data-group="%s">'
                    '<input type="checkbox"><span>%s</span></label>' % (cid, group, label)
                )
            o.append("  </div>")
    o.append("</div>")
    return "\n".join(o)



STYLE = """<style>
  /* ──────────────────────────────────────────────────────────────
     濟州島行程 App（2026-09，版型與字級沿用瀨戶內海那一頁）

     字級只有五級，而且每一處都明寫，不留任何繼承主題 1.8rem 的文字：
       2.2rem / 22px  分頁主標
       1.8rem / 18px  卡片標題
       1.6rem / 16px  區塊小標
       1.5rem / 15px  內文
       1.3rem / 13px  註記、標籤、表格

     主題把 html 設成 font-size: 62.5%，所以 1rem = 10px，改動前先確認這件事。
     配色：玄武岩海藍（accent）＋ 濟州柑橘（accent2），另有五天各自的色碼 d1–d5，
     那五色沿用互動地圖既有的一組，讓總覽、分日行程、地圖篩選對得起來。
     ────────────────────────────────────────────────────────────── */
  .jeju {
    --bg: #f7f9fb;
    --surface: #ffffff;
    --sunk: #eef3f7;
    --border: rgba(20, 58, 92, .14);
    --border-strong: rgba(20, 58, 92, .26);
    --text: #14222e;
    --muted: #5b7185;
    --accent: #15636f;
    --accent-ink: #0d454e;
    --accent2: #b0540c;
    --soft: rgba(21, 99, 111, .10);
    --soft2: rgba(217, 113, 28, .12);
    --stripe: rgba(21, 99, 111, .045);
    --shadow: 0 18px 44px rgba(16, 46, 74, .10);
    --shadow-sm: 0 4px 14px rgba(16, 46, 74, .07);
    --d1: #1C6E8C; --d2: #2E8B6F; --d3: #C08327; --d4: #C4452F; --d5: #5B4B8A;
    --on-accent: #ffffff;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 24px;
    box-shadow: var(--shadow);
    color: var(--text);
    margin-top: 2.4rem;
    overflow: clip;
  }

  .colorscheme-dark .jeju {
    --bg: #0f151c;
    --surface: #1a232d;
    --sunk: #141d26;
    --border: rgba(160, 195, 225, .14);
    --border-strong: rgba(160, 195, 225, .30);
    --text: #e9f1f8;
    --muted: #9db1c4;
    --accent: #63c3cc;
    --accent-ink: #a5e0e5;
    --accent2: #f4a85a;
    --soft: rgba(99, 195, 204, .14);
    --soft2: rgba(244, 168, 90, .14);
    --stripe: rgba(99, 195, 204, .05);
    --shadow: 0 18px 44px rgba(0, 0, 0, .38);
    --shadow-sm: 0 4px 14px rgba(0, 0, 0, .30);
    /* 淺色那組直接放進深底會糊掉，換成同色相、明度拉高的一組 */
    --d1: #5AA6C9; --d2: #5FB894; --d3: #D9A94E; --d4: #E8765A; --d5: #9182C4;
    --on-accent: #0f151c;
  }

  .jeju *, .jeju *::before, .jeju *::after { box-sizing: border-box; }
  @media only screen and (min-width: 1024px) { .jeju { border-radius: 28px; } }

  /* ── Hero ──
     瀨戶內海那頁是淺底加兩團柔光；這頁刻意反過來，用夜裡的海與玄武岩當底，
     右邊放一張用真實經緯度投影的濟州島路線圖，這是整頁唯一「用力」的地方。
     底色不跟著深淺模式翻轉（兩種模式都是深底），只在深色模式再壓暗一階，
     讓它和下方的頁面背景拉開。
     質感是兩層：密的小孔是玄武岩的氣孔，疏的大圈是海面的反光，都用
     radial-gradient 疊，不載圖片。 */
  .jeju-hero {
    --hero-bg: #0f3a42;
    --hero-bg2: #0a2a31;
    --hero-text: #f2f7f6;
    --hero-muted: rgba(226, 240, 238, .74);
    --hero-line: rgba(226, 240, 238, .16);
    /* 深底上要用提亮過的天別色，沿用深色模式那一組 */
    --d1: #5AA6C9; --d2: #5FB894; --d3: #D9A94E; --d4: #E8765A; --d5: #9182C4;
    background:
      radial-gradient(circle at 1px 1px, rgba(255, 255, 255, .07) 1px, transparent 1.6px) 0 0 / 9px 9px,
      radial-gradient(circle at 3px 4px, rgba(0, 0, 0, .22) 1.4px, transparent 2.2px) 0 0 / 13px 11px,
      linear-gradient(160deg, var(--hero-bg) 0%, var(--hero-bg2) 100%);
    border-bottom: 3px solid #e8892a;
    color: var(--hero-text);
    padding: 2.6rem 2rem 2.2rem;
  }
  .colorscheme-dark .jeju-hero { --hero-bg: #0b2a30; --hero-bg2: #071c21; }
  .jeju-herogrid { align-items: center; display: grid; gap: 1.6rem; grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); }
  .jeju-eyebrow { color: #f4a85a; font-size: 1.3rem; font-weight: 700; letter-spacing: .16em; }
  .jeju-hero h2 { color: var(--hero-text); font-size: 2.2rem; font-weight: 700; letter-spacing: -.01em; line-height: 1.35; margin: .7rem 0 .6rem; }
  /* 行長不在這裡管：全站 .container 已經收到 768px（見 assets/css/custom.css）。
     這裡再加 max-width 會變成雙重限制，而且 ch 量的是「0」的寬度、
     中文字約 2ch，用在中文上會提早一半換行。 */
  .jeju-herotext p { color: var(--hero-muted); font-size: 1.5rem; line-height: 1.7; margin: 0; }
  .jeju-island { margin: 0; }
  .jeju-island svg { display: block; height: auto; width: 100%; }
  .jeju-island figcaption { color: var(--hero-muted); font-size: 1.3rem; margin-top: .4rem; text-align: right; }
  .jeju-hero .jeju-rail span { color: var(--hero-text); }

  .jeju-rail { display: grid; gap: .7rem; grid-template-columns: repeat(5, minmax(0, 1fr)); margin-top: 1.8rem; }
  .jeju-rail > div { padding-top: .8rem; }
  .jeju-rail b { display: block; font-size: 1.3rem; font-weight: 700; }
  .jeju-rail span { display: block; font-size: 1.3rem; line-height: 1.5; margin-top: .2rem; }

  /* ── 分頁列 ── */
  .jeju-nav {
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 1.1rem 0 1.1rem 2rem; position: sticky; top: 0; z-index: 5;
  }
  .jeju-pills {
    align-items: center; display: flex; flex-wrap: wrap; gap: .6rem; padding-right: 2rem;
  }
  .jeju-pill {
    background: transparent; border: 1px solid var(--border); border-radius: 999px;
    color: var(--muted); cursor: pointer; font-family: inherit; font-size: 1.3rem;
    font-weight: 500; letter-spacing: .02em; padding: .5rem 1.3rem;
    transition: border-color .2s, color .2s; white-space: nowrap;
  }
  .jeju-pill:hover { border-color: var(--accent); color: var(--accent); }
  .jeju-pill[aria-selected="true"] {
    background: var(--accent); border-color: var(--accent); color: var(--on-accent); font-weight: 700;
  }
  .jeju-sep { background: var(--border); height: 1.5rem; margin: 0 .3rem; width: 1px; }

  /* ── 面板 ── */
  .jeju-panel { padding: 2.2rem 2rem 2.8rem; }
  .jeju-panel[hidden] { display: none; }
  .jeju-panel > h3 {
    font-size: 2.2rem; font-weight: 700; letter-spacing: -.01em;
    line-height: 1.35; margin: 0 0 .6rem;
  }
  .jeju-panel > h3 + p { color: var(--muted); font-size: 1.5rem; line-height: 1.7; margin: 0 0 1.6rem; }
  .jeju-h4 {
    border-left: 3px solid var(--accent); color: var(--accent);
    font-size: 1.6rem; font-weight: 700; line-height: 1.4; margin: 2.6rem 0 1rem; padding-left: .9rem;
  }
  .jeju-h4:first-child { margin-top: 0; }
  .jeju-h4 em { color: var(--muted); font-style: normal; font-weight: 500; }

  /* ── 卡片 ── */
  .jeju-g3 { display: grid; gap: 1rem; grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .jeju-g2 { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .jeju-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: var(--shadow-sm); padding: 1.4rem 1.5rem;
  }
  .jeju-card .k { color: var(--muted); font-size: 1.3rem; line-height: 1.5; }
  .jeju-card .t { font-size: 1.8rem; font-weight: 700; line-height: 1.35; margin-top: .3rem; }
  .jeju-card .d { color: var(--muted); font-size: 1.3rem; line-height: 1.55; margin-top: .5rem; }
  .jeju-card ul { margin: .5rem 0 0; padding-left: 1.9rem; }
  .jeju-card li { color: var(--muted); font-size: 1.3rem; line-height: 1.65; }

  /* ── 表格 ── */
  .jeju-tw {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; overflow-x: auto;
  }
  .jeju-table { border-collapse: collapse; font-size: 1.3rem; min-width: 100%; width: 100%; }
  .jeju-table thead tr { background: var(--sunk); }
  .jeju-table th {
    border-bottom: 1px solid var(--border); color: var(--muted); font-weight: 700;
    padding: .9rem 1.2rem; text-align: left; white-space: nowrap;
  }
  .jeju-table td { border-bottom: 1px solid var(--border); line-height: 1.6; padding: .9rem 1.2rem; vertical-align: top; }
  .jeju-table tbody tr:last-child td { border-bottom: 0; }
  .jeju-table tbody tr:nth-child(even) { background: var(--stripe); }
  .jeju-num { font-variant-numeric: tabular-nums; white-space: nowrap; }

  /* ── 天別列 ── */
  .jeju-rows { display: flex; flex-direction: column; gap: .7rem; }
  .jeju-row {
    align-items: center; background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; display: flex; gap: 1.3rem; padding: 1.1rem 1.4rem;
  }
  .jeju-row .d { flex: 0 0 7.4rem; font-size: 1.3rem; font-weight: 700; }
  .jeju-row .t { flex: 1 1 auto; font-size: 1.5rem; font-weight: 700; }
  .jeju-row .m { color: var(--muted); font-size: 1.3rem; text-align: right; }

  /* ── 標籤 ── */
  .jeju-tag { border-radius: 4px; font-size: 1.3rem; font-weight: 700; padding: .1rem .6rem; white-space: nowrap; }
  .jeju-tag.warn { background: var(--soft2); color: var(--accent2); }
  .jeju-tag.info { background: var(--soft); color: var(--accent); }

  /* ── 分日行程手風琴 ── */
  .jeju-acc { display: flex; flex-direction: column; gap: .8rem; }
  .jeju-day { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  .jeju-day > summary {
    align-items: center; cursor: pointer; display: flex; gap: 1.3rem;
    list-style: none; padding: 1.3rem 1.5rem;
  }
  .jeju-day > summary::-webkit-details-marker { display: none; }
  .jeju-day > summary:hover { background: var(--stripe); }
  /* 這欄放的是「D1　9/24（四）」完整日期，7.4rem 會把（四）擠到第二行 */
  .jeju-day > summary .d { flex: 0 0 10.6rem; font-size: 1.3rem; font-weight: 700; white-space: nowrap; }
  .jeju-day > summary .t { flex: 1 1 auto; font-size: 1.6rem; font-weight: 700; }
  .jeju-day > summary .m { color: var(--muted); font-size: 1.3rem; text-align: right; }
  .jeju-day > summary .chev { color: var(--muted); flex: 0 0 1.6rem; transition: transform .2s; }
  .jeju-day[open] > summary { background: var(--sunk); }
  .jeju-day[open] > summary .chev { transform: rotate(180deg); }
  .jeju-daybody { border-top: 1px solid var(--border); padding: .4rem 1.5rem 1.6rem; }

  .jeju-route {
    align-items: center; background: var(--sunk); border-radius: 8px; color: var(--muted);
    display: flex; flex-wrap: wrap; font-size: 1.3rem; gap: .6rem; line-height: 1.6;
    margin-top: 1.2rem; padding: .9rem 1.2rem;
  }
  .jeju-route i { color: var(--border-strong); font-style: normal; }

  .jeju-spot { background: var(--sunk); border-radius: 10px; margin-top: .8rem; padding: 1.2rem 1.4rem; }
  .jeju-spot h5 { display: inline; font-size: 1.6rem; font-weight: 700; margin: 0; }
  .jeju-spot .when { color: var(--muted); font-size: 1.3rem; margin-left: .8rem; }
  .jeju-spot p { color: var(--muted); font-size: 1.3rem; line-height: 1.65; margin: .4rem 0 0; }
  .jeju-daybody ul { margin: .6rem 0 0; padding-left: 1.9rem; }
  .jeju-daybody li { color: var(--muted); font-size: 1.3rem; line-height: 1.7; }
  .jeju-daybody li b { color: var(--text); }

  .jeju-dayfoot {
    align-items: center; border-top: 1px dashed var(--border); display: flex; flex-wrap: wrap;
    gap: 1.4rem; margin-top: 1.6rem; padding-top: 1.2rem;
  }
  .jeju-gotomap {
    align-items: center; background: transparent; border: 0; color: var(--accent); cursor: pointer;
    display: inline-flex; font-family: inherit; font-size: 1.3rem; font-weight: 700; gap: .5rem; padding: 0;
  }
  .jeju-gotomap:hover { color: var(--accent-ink); text-decoration: underline; }
  .jeju-dayfoot .meal { align-items: center; color: var(--muted); display: inline-flex; font-size: 1.3rem; gap: .5rem; }

  /* ── 互動地圖 ── */
  .jeju-mapchips { display: flex; flex-wrap: wrap; gap: .6rem; margin-bottom: 1.2rem; }
  .jeju-mapwrap {
    border: 1px solid var(--border); border-radius: 12px; box-shadow: var(--shadow-sm);
    display: grid; grid-template-columns: 23.2rem minmax(0, 1fr); overflow: hidden;
  }
  .jeju-mapside {
    background: var(--sunk); border-right: 1px solid var(--border);
    height: 46rem; overflow-y: auto; padding: 1.1rem;
  }
  .jeju-mapday { align-items: center; display: flex; gap: .7rem; margin: 1.2rem .2rem .6rem; }
  .jeju-mapday:first-child { margin-top: 0; }
  .jeju-mapday b { font-size: 1.3rem; font-weight: 700; }
  .jeju-mapday i { border-radius: 50%; flex: 0 0 .8rem; height: .8rem; }
  .jeju-mapcard {
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    cursor: pointer; margin-bottom: .6rem; padding: .9rem 1.1rem; transition: border-color .15s, transform .15s;
    width: 100%; text-align: left; font-family: inherit;
  }
  .jeju-mapcard:hover { border-color: var(--accent); transform: translateX(2px); }
  /* 這三個是 <span>，不宣告 display:block 會擠成一行、margin 也吃不到 */
  .jeju-mapcard .t { display: block; font-size: 1.3rem; font-weight: 700; font-variant-numeric: tabular-nums; }
  .jeju-mapcard .n { display: block; font-size: 1.5rem; font-weight: 700; line-height: 1.35; margin: .1rem 0 .2rem; }
  .jeju-mapcard .x { color: var(--muted); display: block; font-size: 1.3rem; line-height: 1.45; }
  .jeju-map { background: var(--sunk); height: 46rem; position: relative; }
  /* 手機上先蓋一層遮罩，點過才把地圖拖曳打開。
     不這樣做的話，單指滑到地圖就會被地圖吃掉、整頁捲不動；
     但直接關掉 dragging 又會讓地圖完全推不動（Leaflet 的雙指是縮放，不是平移）。 */
  .jeju-mapgate {
    align-items: center; background: rgba(15, 21, 28, .45); color: #fff; cursor: pointer;
    display: none; font-size: 1.5rem; font-weight: 700; inset: 0; justify-content: center;
    position: absolute; z-index: 500;
  }
  .jeju-mapgate span {
    background: rgba(15, 21, 28, .78); border-radius: 999px; padding: .9rem 1.8rem;
  }
  .jeju-map.gated .jeju-mapgate { display: flex; }
  .jeju-map .leaflet-popup-content { font-family: inherit; margin: 1.2rem 1.4rem; }
  .jeju-pop .h { font-size: 1.5rem; font-weight: 700; line-height: 1.3; }
  .jeju-pop .m { color: #5b7185; font-size: 1.3rem; margin: .2rem 0 .6rem; }
  .jeju-pop .x { font-size: 1.3rem; line-height: 1.5; }
  .jeju-pop .btns { display: flex; gap: .6rem; margin-top: .9rem; }
  .jeju-pop a { background: #15636f; border-radius: 5px; color: #fff; font-size: 1.3rem; padding: .4rem .9rem; text-decoration: none; }
  .jeju-pop a.alt { background: #fff; border: 1px solid #15636f; color: #15636f; }
  .jeju-pin {
    align-items: center; border: 2px solid #fff; border-radius: 50%; box-shadow: 0 1px 4px rgba(0,0,0,.35);
    color: #fff; display: flex; font-size: 1.2rem; font-weight: 700; height: 100%; justify-content: center; width: 100%;
  }
  .jeju-mapload { align-items: center; color: var(--muted); display: flex; font-size: 1.3rem; height: 100%; justify-content: center; }

  /* ── 規定橫條 ── */
  .jeju-rules { display: flex; flex-direction: column; }
  .jeju-rule {
    align-items: flex-start; background: var(--surface); border: 1px solid var(--border);
    display: flex; gap: 1.1rem; padding: 1.1rem 1.4rem;
  }
  .jeju-rule + .jeju-rule { border-top: 0; }
  .jeju-rule:first-child { border-radius: 10px 10px 0 0; }
  .jeju-rule:last-child { border-radius: 0 0 10px 10px; }
  .jeju-rule:only-child { border-radius: 10px; }
  .jeju-rule b { display: block; font-size: 1.5rem; line-height: 1.5; }
  .jeju-rule p { color: var(--muted); font-size: 1.3rem; line-height: 1.6; margin: .2rem 0 0; }

  .jeju-callout {
    align-items: flex-start; background: var(--surface); border: 1px solid var(--accent);
    border-radius: 12px; box-shadow: var(--shadow-sm); display: flex; gap: 1.2rem; padding: 1.4rem 1.5rem;
  }
  .jeju-callout svg { color: var(--accent); flex: 0 0 2rem; margin-top: .2rem; }
  .jeju-callout b { display: block; font-size: 1.6rem; font-weight: 700; line-height: 1.4; }
  .jeju-callout p { color: var(--muted); font-size: 1.3rem; line-height: 1.6; margin: .3rem 0 0; }

  /* ── 行前檢查時間軸 ── */
  .jeju-when {
    align-items: flex-start; background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; display: flex; gap: 1.3rem; padding: 1.3rem 1.5rem;
  }
  .jeju-when > .w { flex: 0 0 7.4rem; font-size: 1.3rem; font-weight: 700; }
  .jeju-when > div:last-child { flex: 1 1 auto; }
  .jeju-when b { display: block; font-size: 1.6rem; font-weight: 700; line-height: 1.4; }
  .jeju-when p { color: var(--muted); font-size: 1.3rem; line-height: 1.65; margin: .3rem 0 0; }
  .jeju-when a { font-size: 1.3rem; font-weight: 700; }

  /* ── 勾選清單 ── */
  .jeju-progress {
    align-items: center; background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; display: flex; gap: 1.3rem; padding: 1.3rem 1.5rem;
  }
  .jeju-bar { background: var(--soft); border-radius: 999px; flex: 1 1 auto; height: .7rem; overflow: hidden; }
  .jeju-bar i { background: linear-gradient(90deg, var(--accent2), var(--accent)); border-radius: 999px; display: block; height: 100%; transition: width .35s ease; }
  .jeju-count { font-size: 1.6rem; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .jeju-reset {
    background: transparent; border: 1px solid var(--border); border-radius: 999px; color: var(--muted);
    cursor: pointer; font-family: inherit; font-size: 1.3rem; padding: .4rem 1.1rem; white-space: nowrap;
  }
  .jeju-reset:hover { border-color: var(--accent2); color: var(--accent2); }
  .jeju-groupstats { display: flex; flex-wrap: wrap; gap: .7rem; margin-top: .9rem; }
  .jeju-groupstat {
    background: var(--sunk); border-radius: 999px; color: var(--muted); font-size: 1.3rem;
    font-weight: 700; padding: .4rem 1.1rem;
  }
  .jeju-groupstat b { font-variant-numeric: tabular-nums; font-weight: 500; }
  .jeju-groupstat.full { background: var(--soft); color: var(--accent); }
  .jeju-sub { font-size: 1.6rem; font-weight: 700; margin: 2.2rem 0 .2rem; }
  .jeju-sub span { color: var(--muted); font-size: 1.3rem; font-weight: 500; }
  .jeju-subsub { color: var(--muted); font-size: 1.3rem; margin: 1.1rem 0 0; }
  .jeju-checkgrid { display: grid; gap: .6rem; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: .8rem; }
  .jeju-check {
    align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    cursor: pointer; display: flex; font-size: 1.3rem; gap: .8rem; line-height: 1.4;
    min-height: 4.4rem; padding: .8rem 1rem; user-select: none;
  }
  .jeju-check:hover { border-color: var(--accent); }
  .jeju-check input { accent-color: var(--accent); flex: 0 0 1.5rem; height: 1.5rem; margin: 0; width: 1.5rem; }
  .jeju-check.done { background: var(--sunk); color: var(--muted); }
  .jeju-check.done span { text-decoration: line-through; }


  /* ── 說明條 ── */
  .jeju-note { background: var(--soft); border-radius: 10px; font-size: 1.3rem; line-height: 1.75; margin-top: 1.4rem; padding: 1.2rem 1.4rem; }
  .jeju-note b { color: var(--accent); }
  .jeju-note + .jeju-note { margin-top: .8rem; }

  /* ── 手機 ── */
  @media only screen and (max-width: 768px) {
    .jeju { border-radius: 18px; }
    .jeju-hero { padding: 2rem 1.5rem 1.8rem; }
    .jeju-herogrid { grid-template-columns: 1fr; gap: 1rem; }
    .jeju-island figcaption { text-align: left; }
    .jeju-hero h2 { font-size: 2rem; }
    .jeju-nav { padding: 1rem 0 1rem 1.5rem; }
    .jeju-pills { flex-wrap: nowrap; overflow-x: auto; padding-right: 1.5rem; -webkit-overflow-scrolling: touch; }
    .jeju-panel { padding: 1.8rem 1.5rem 2.2rem; }
    .jeju-panel > h3 { font-size: 2rem; }
    /* 五天骨幹在窄螢幕改直排，橫排五格會擠成一坨 */
    .jeju-rail { grid-template-columns: 1fr; gap: .5rem; }
    .jeju-rail > div { border-top: 0 !important; border-left: 3px solid; padding: .2rem 0 .2rem .9rem; }
    .jeju-rail > div:nth-child(1) { border-left-color: var(--d1); }
    .jeju-rail > div:nth-child(2) { border-left-color: var(--d2); }
    .jeju-rail > div:nth-child(3) { border-left-color: var(--d3); }
    .jeju-rail > div:nth-child(4) { border-left-color: var(--d4); }
    .jeju-rail > div:nth-child(5) { border-left-color: var(--d5); }
    .jeju-rail b, .jeju-rail span { display: inline; }
    .jeju-rail span::before { content: "　"; }
    .jeju-g3, .jeju-g2 { grid-template-columns: 1fr; }
    .jeju-checkgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .jeju-row, .jeju-day > summary { flex-wrap: wrap; }
    .jeju-row .m, .jeju-day > summary .m { flex: 1 1 100%; text-align: left; }
    .jeju-when { flex-wrap: wrap; }
    .jeju-mapwrap { grid-template-columns: 1fr; }
    .jeju-mapside { border-bottom: 1px solid var(--border); border-right: 0; height: 24rem; }
    .jeju-map { height: 38rem; }
  }
</style>"""

CHEV = ('<svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<polyline points="6 9 12 15 18 9"></polyline></svg>')
ICON_MAP = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<polygon points="1 6 8 3 16 6 23 3 23 18 16 21 8 18 1 21"></polygon>'
            '<line x1="8" y1="3" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="21"></line></svg>')
ICON_CLOCK = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle>'
              '<polyline points="12 6 12 12 16 14"></polyline></svg>')


def panel(pid, body):
    return ('<section class="jeju-panel" id="jeju-panel-%s" role="tabpanel" '
            'aria-labelledby="jeju-tab-%s" hidden>\n%s\n</section>' % (pid, pid, body))


def rail():
    o = ['<div class="jeju-rail">']
    for i, (code, date, title, _) in enumerate(DAYS, 1):
        o.append('  <div style="border-top:3px solid var(--d%d)"><b style="color:var(--d%d)">%s　%s</b>'
                 '<span>%s</span></div>' % (i, i, code, date.split("（")[0], title))
    o.append("</div>")
    return "\n".join(o)



# ── Hero 的濟州島路線圖。海岸線是手描的概略輪廓（經緯度節點），跟點位用同一個投影，
#    所以圖釘落在島上的相對位置是對的。1° 經度在北緯 33.4° 約 92.7 km、1° 緯度約 111 km，
#    y 方向乘 1.2 把比例拉回來。──
COAST = [
    (126.163, 33.312), (126.180, 33.270), (126.232, 33.222), (126.300, 33.232), (126.380, 33.232),
    (126.455, 33.240), (126.530, 33.238), (126.600, 33.255), (126.690, 33.282), (126.780, 33.303),
    (126.850, 33.330), (126.905, 33.380), (126.945, 33.445), (126.925, 33.492), (126.860, 33.528),
    (126.780, 33.556), (126.690, 33.556), (126.610, 33.533), (126.530, 33.520), (126.460, 33.506),
    (126.390, 33.480), (126.315, 33.447), (126.250, 33.405), (126.195, 33.360),
]
HALLASAN = (126.533, 33.362)
ISL_LNG0, ISL_LAT0, ISL_K = 126.12, 33.60, 400.0


def isl_xy(lng, lat):
    return ((lng - ISL_LNG0) * ISL_K, (ISL_LAT0 - lat) * ISL_K * 1.2)


def smooth_closed(pts):
    """Catmull-Rom 轉三次貝茲，讓折線的海岸變圓滑。"""
    n = len(pts)
    d = "M%.1f %.1f" % pts[0]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += " C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d + "Z"


def island_svg():
    # viewBox 貼著海岸線外框再留 14 單位，免得圖下方空一大塊
    cpts = [isl_xy(*c) for c in COAST]
    pad = 14
    x0, y0 = min(p[0] for p in cpts) - pad, min(p[1] for p in cpts) - pad - 6
    w, h = max(p[0] for p in cpts) + pad - x0, max(p[1] for p in cpts) + pad + 6 - y0
    coast = smooth_closed(cpts)
    hx, hy = isl_xy(*HALLASAN)
    o = ['<figure class="jeju-island">',
         '<svg viewBox="%.0f %.0f %.0f %.0f" role="img" aria-labelledby="jeju-island-t">' % (x0, y0, w, h),
         '<title id="jeju-island-t">濟州島上五天的停留點位置</title>',
         # 外圈等深線：一圈淡淡的海岸浪
         '<path d="%s" fill="none" stroke="rgba(226,240,238,.10)" stroke-width="10" stroke-linejoin="round"/>' % coast,
         '<path d="%s" fill="rgba(8,30,34,.55)" stroke="rgba(226,240,238,.42)" stroke-width="1.2" stroke-linejoin="round"/>' % coast]
    # 漢拏山：三圈同心的等高線
    for r, a in ((34, .10), (22, .14), (11, .20)):
        o.append('<ellipse cx="%.1f" cy="%.1f" rx="%d" ry="%.1f" fill="none" stroke="rgba(226,240,238,%.2f)" stroke-width="1"/>'
                 % (hx, hy, r * 1.5, r * 0.9, a))
    o.append('<text x="%.1f" y="%.1f" text-anchor="middle" fill="rgba(226,240,238,.62)" font-size="10">漢拏山</text>' % (hx, hy + 3.5))
    # 每天一條路線＋停留點，重複的飯店只畫一次
    seen = set()
    for n in range(1, 6):
        pts = [isl_xy(lng, lat) for (d, t, name, kind, lat, lng, note, q) in POINTS if d == n and q != TPE1[2]]
        if len(pts) > 1:
            o.append('<polyline points="%s" fill="none" stroke="var(--d%d)" stroke-width="1.6" '
                     'stroke-dasharray="4 3" stroke-linecap="round" opacity=".85"/>'
                     % (" ".join("%.1f,%.1f" % p for p in pts), n))
    for n in range(1, 6):
        for (d, t, name, kind, lat, lng, note, q) in POINTS:
            if d != n or q == TPE1[2] or q in seen:
                continue
            seen.add(q)
            x, y = isl_xy(lng, lat)
            if kind == "住宿":
                o.append('<rect x="%.1f" y="%.1f" width="7" height="7" rx="1.5" fill="#f2f7f6" stroke="var(--d%d)" stroke-width="2"/>'
                         % (x - 3.5, y - 3.5, n))
            else:
                o.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="var(--d%d)" stroke="#0a2a31" stroke-width="1.2"/>' % (x, y, n))
    # 三個地名當方位錨點
    for label, (lng, lat), anchor, dy in (("濟州市", (126.52, 33.515), "middle", -9),
                                          ("西歸浦", (126.56, 33.245), "middle", 15),
                                          ("城山", (126.94, 33.458), "end", -9)):
        x, y = isl_xy(lng, lat)
        o.append('<text x="%.1f" y="%.1f" text-anchor="%s" fill="rgba(226,240,238,.78)" font-size="10.5" font-weight="700">%s</text>'
                 % (x, y + dy, anchor, label))
    o.append("</svg>")
    o.append("<figcaption>圓點是景點，方塊是飯店；顏色對應下面五天</figcaption>")
    o.append("</figure>")
    return "".join(o)


def p_overview():
    rows = []
    for i, (code, date, title, stay) in enumerate(DAYS, 1):
        rows.append(
            '  <div class="jeju-row" style="border-left:3px solid var(--d%d)">'
            '<div class="d" style="color:var(--d%d)">%s　%s</div>'
            '<div class="t">%s</div><div class="m">%s</div></div>'
            % (i, i, code, date.split("（")[0], title, stay))
    meals = [
        ("D1", '<span style="color:var(--muted)">—</span>',
         '<span class="jeju-tag warn">機上不供餐</span>', "韓式炸全雞＋炸醬麵吃到飽"),
        ("D2", "早餐", '<span class="jeju-tag warn">自理</span> 發放 ₩8,000', "烤白帶魚＋烤青花魚＋海膽海帶湯"),
        ("D3", "飯店早餐", "年糕粉絲燉排骨＋白菜大醬湯", "五雲閣自助餐（酒水無限）"),
        ("D4", "飯店早餐", "豬肉壽喜燒吃到飽", "韓國烤肉吃到飽（豬、牛）"),
        ("D5", "飯店早餐", '<span class="jeju-tag warn">機上不供餐</span>', '<span style="color:var(--muted)">—</span>'),
    ]
    mrows = "\n".join(
        '        <tr><td style="color:var(--d%d);font-weight:700">%s</td>'
        '<td style="color:var(--muted)">%s</td><td>%s</td><td>%s</td></tr>' % (i, c, b, l, d)
        for i, (c, b, l, d) in enumerate(meals, 1))
    return panel("overview", """<h3>總覽</h3>
<p>五天的骨架、班機、住宿與餐食。每天配一個顏色，這個顏色會一路跟到分日行程和互動地圖。</p>

<div class="jeju-g3">
  <div class="jeju-card">
    <div class="k">出發前 3 天要做</div>
    <div class="t">電子入境卡</div>
    <div class="d">抵達前 72 小時內線上填好，最早 10/14（三）傍晚可以開始填。要護照照片、Email 與飯店地址。</div>
  </div>
  <div class="jeju-card">
    <div class="k">最容易忽略</div>
    <div class="t">機上零餐飲</div>
    <div class="d">去回程都不供餐，連水都不給。集合前先吃飽，過安檢後自己買水和點心。</div>
  </div>
  <div class="jeju-card">
    <div class="k">最需要體力的一天</div>
    <div class="t">D4　城山日出峰</div>
    <div class="d">登頂約 30 分鐘的階梯步道，而且這天從島的西南拉到最東邊，車程全程最長。</div>
  </div>
</div>

<h4 class="jeju-h4">來回班機 <em>泰瑞航空（原德威航空 T'way）</em></h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th>行程</th><th>航班</th><th>出發</th><th>抵達</th><th>飛行</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">去程</td><td class="jeju-num">TW 688</td>
        <td class="jeju-num">10/17 14:30　TPE</td><td class="jeju-num">10/17 17:30　CJU</td>
        <td style="color:var(--muted)">2h00m</td></tr>
      <tr><td style="font-weight:700">回程</td><td class="jeju-num">TW 687</td>
        <td class="jeju-num">10/21 12:20　CJU</td><td class="jeju-num">10/21 13:25　TPE</td>
        <td style="color:var(--muted)">2h05m</td></tr>
    </tbody>
  </table>
</div>
<div class="jeju-note">
  <b>集合：10/17（六）12:00，桃園機場第一航廈，泰瑞航空 11 號團體櫃台（華航代理）。</b>
  起飛前 1 小時關櫃，之後就辦不了登機。時間都是當地時間，韓國比台灣快 1 小時。
</div>

<h4 class="jeju-h4">行程與住宿</h4>
<div class="jeju-rows">
%s
</div>

<h4 class="jeju-h4">每日餐食</h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:5.6rem">日</th><th>早餐</th><th>午餐</th><th>晚餐</th></tr></thead>
    <tbody>
%s
    </tbody>
  </table>
</div>

<div class="jeju-note">
  <b>行程主線。</b>桃園 →（TW688）→ 濟州 → 東門市場 → 濟州市宿 → 雪綠茶園 → 西歸浦偶來市場 → 藥泉寺 →
  濟州市宿 → 蓮洞 → 涯月海岸 → 神話世界宿 → 跆拳武藝秀 → 騎駱駝 → 城山日出峰 → 松堂 → ECO LAND →
  神話世界宿 → 濟州（TW687）→ 桃園。旅行社會依天候與現場狀況調整順序，以領隊當天公布為準。
</div>""" % ("\n".join(rows), mrows))


# ── 分日行程內容。(路線節點, [(餐別, 內容)], [(景點, 時間, 說明)], [(小節標題, [條列])]) ──
DAY_CONTENT = [
    (
        ["桃園機場 T1", "TW 688", "濟州機場", "東門市場", "晚餐", "新濟州・飯店"],
        [("午餐", "機上不供餐"), ("晚餐", "韓式炸全雞＋炸醬麵吃到飽")],
        [
            ("東門傳統市場・夜市", "停留 1–1.5 小時",
             "濟州最具代表性的常設傳統市場，旁邊還連著東門水產市場。海鮮、水果、肉類分區清楚，"
             "邊走邊吃的選擇很多：紫菜飯捲、辣炒年糕、甜不辣、血腸、海鮮炸物。"
             "落地、入境再坐車過來，抵達時已是傍晚，市場裡的夜市攤位會陸續開張。"),
        ],
        [
            ("這天要注意的", [
                "<b>機上不供餐也不給水。</b>14:30 起飛、當地 17:30 落地，中午集合前先吃飽，"
                "過安檢後再買水和小點帶上機。",
                "泰瑞航空（Trinity Airways）就是原本的德威航空（T'way），2026 年更名，航班代碼仍是 TW。"
                "手冊安全守則裡寫的「濟州德威航空」是同一家。",
                "落地就把手錶調快 1 小時。",
                "市場很適合買橘子，但<b>新鮮柑橘不能帶回台灣</b>，買了就在韓國吃完；"
                "要帶回去的改買橘子巧克力、柑橘果醬這類加工品。",
            ]),
            ("晚餐與晚上", [
                "晚餐是韓式炸全雞（四人一隻）配炸醬麵吃到飽，可加價升等為兩人一隻配黑炸醬麵。",
                "飯店在新濟州蓮洞一帶，跟 D3 要去的蓮洞購物商圈同一區，晚上想散步可以先去踩點。",
            ]),
        ],
    ),
    (
        ["飯店", "O'sulloc 雪綠茶園", "innisfree 濟州小屋", "西歸浦每日偶來市場", "藥泉寺", "濟州市區"],
        [("午餐", "發放 ₩8,000 自理"), ("晚餐", "烤白帶魚＋烤青花魚＋海膽海帶湯")],
        [
            ("O'sulloc 雪綠茶園＋innisfree 玻璃小屋", "上午",
             "以綠茶為主題的茶博物館，外面就是整片茶園。名字裡的「O～」取自看到好東西時的讚嘆聲。"
             "隔壁的 innisfree 濟州小屋是 2013 年開的品牌體驗館，整棟玻璃建築很好拍。"
             "茶包、綠茶抹醬這類伴手禮這一站就能買齊。"),
            ("西歸浦每日偶來市場", "中午",
             "《我們的藍調時光》拍攝地。1960 年代自然形成的市場，從原本 120 公尺長到現在 620 公尺的拱廊商店街，"
             "內部呈王字型動線，有頂棚、下雨也能逛，另有免費宅配服務。午餐 ₩8,000 自理，"
             "這一站是全天最適合解決午餐的地方。"),
            ("藥泉寺", "下午",
             "《Island》拍攝地，也是《秘密花園》的場景。以能治病的泉水得名，是濟州規模最大的寺院之一。"
             "大寂光殿內供奉高 5 公尺的毘盧舍那佛，鐘閣掛著 18 噸的梵鐘，另有三星閣與舍利塔。"),
        ],
        [
            ("這天要注意的", [
                "₩8,000 大約夠一份市場小吃，想吃得豐盛要自己補差額。市場攤商多收現金，零錢先準備好。",
                "寺院內放低音量，法堂內能不能拍照依現場告示。",
                "晚餐的烤白帶魚是濟州代表性料理（四人一隻），配烤青花魚與海膽海帶湯。",
            ]),
        ],
    ),
    (
        ["飯店", "Marina K.C 彩妝", "蓮洞商圈", "漢潭海岸散步路", "神話世界", "五雲閣"],
        [("午餐", "年糕粉絲燉排骨＋白菜大醬湯"), ("晚餐", "五雲閣自助餐（酒水無限）")],
        [
            ("Marina K.C 彩妝名品", "上午",
             "團體購物站，賣韓國在地的保養品牌（YIHANCARINO、RE:TIMES 等），每人送一份小禮物。沒有需要可以不買。"),
            ("蓮洞購物商圈", "上午",
             "新濟州的時尚商店街，全長 450 公尺，以蠶丘路（原寶健路）最熱鬧，車輛不能進入、逛起來很安全。"
             "這天是白天經過，它酒吧、居酒屋那一面要晚上才看得到。"),
            ("漢潭海岸散步路（涯月海岸咖啡街）", "中午前後",
             "沿著玄武岩海岸的步道，一側是海、一側是一整排海景咖啡館。海風很大，外套穿著下車。"),
            ("神話世界半日自由活動", "14:00 後",
             "含神話主題樂園門票（三項設施券）與韓服變裝 4 小時。樂園約 28 萬平方公尺、分七大故事區，"
             "韓服可以直接穿進樂園拍照。"),
            ("五雲閣頂級自助餐廳", "18:00–21:30",
             "萬豪酒店 5 樓。六個現場烹調的料理站，韓、日、中、西式都有，葡萄酒與生啤無限暢飲。"
             "訂位滿或休館時改到藍鼎廳。"),
        ],
        [
            ("神話世界怎麼安排", [
                "三項設施券只夠挑三個，先看園區地圖再決定，其餘設施自費。戶外設施遇天候可能暫停。",
                "韓服有 4 小時，歸還時間抓好，別跟 18:00 的晚餐撞在一起。",
                "<b>煙火秀只在週五、六、日 20:10</b>，這天是週一，看不到。",
                "度假村內還有藍鼎娛樂場（Casino）、亞洲美食街，以及保齡球、K 歌的娛樂城（自費）。",
            ]),
            ("萬豪酒店", [
                "莫西爾泳池住客免費：室內 09:00–21:00、室外 09:00–19:00，健身房也可用。泳衣與泳帽要自己帶。",
                "<b>飯店不提供牙刷、牙膏等一次性備品</b>，盥洗用品全部自備。",
                "接下來連住兩晚，行李可以攤開整理一次。",
            ]),
        ],
    ),
    (
        ["神話世界", "跆拳武藝秀", "騎駱駝", "城山日出峰", "松堂童話村", "ECO LAND", "神話世界"],
        [("午餐", "豬肉壽喜燒吃到飽"), ("晚餐", "韓國烤肉吃到飽")],
        [
            ("濟州阿里郎『魂』跆拳武藝秀", "上午",
             "擊鼓、韓國舞蹈與跆拳道擊破示範串成的劇場演出，曾受邀於平昌冬奧演出。"
             "故事講守護耽羅國的武人，中段有觀眾上台參與的橋段。"),
            ("騎駱駝體驗", "上午",
             "單峰駱駝，馬鞍兩人一座，小孩可由大人陪同。園區裡有韓國首次誕生的小駱駝，餵食要另外付費。"),
            ("城山日出峰", "停留 60–90 分",
             "約 10 萬年前海底火山噴發形成的火山口，2007 年登錄世界自然遺產。登頂約 30 分鐘，"
             "山頂可以俯瞰整個火山口與城山浦。西側海岸運氣好能看到海女作業。"
             "每月第一個週一公休，這天是週二不受影響；遇天候不開放時改去室內的仙女與樵夫主題公園。"),
            ("松堂童話村主題花園＋星巴克", "下午",
             "分樹木、岩石、文化、神話四個主題區的花園。園內的星巴克 THE 濟州松堂公園 R 店是典藏咖啡門市，"
             "可以邊喝邊看漢拏山方向的風景，飲料自理。"),
            ("ECO LAND 英式森林小火車", "下午",
             "以 Baldwin 蒸汽火車頭為原型打造的小火車，繞行濟州特有的火山岩森林（곶자왈）。"
             "沿途停 E 酷橋站、湖畔站、野餐庭院站、綠茶＆玫瑰花園站，每站都能下車走一段再搭下一班。"),
        ],
        [
            ("這天要注意的", [
                "<b>全程最耗體力的一天。</b>日出峰是連續階梯，穿好走的鞋；山頂風大，外套帶下車。",
                "行程從島的西南（神話世界）拉到最東邊的城山再繞回來，車程長，能睡就睡。",
                "晚餐是烤肉吃到飽（豬、牛），另有炒年糕、燉雞、義大利麵。",
            ]),
        ],
    ),
    (
        ["神話世界", "濟州機場", "TW 687", "桃園機場"],
        [("早餐", "飯店早餐"), ("午餐", "機上不供餐")],
        [
            ("濟州 → 桃園", "12:20 起飛",
             "早餐後專車前往濟州機場，TW687 12:20 起飛，台灣時間 13:25 抵達桃園。"),
        ],
        [
            ("收尾提醒", [
                "萬豪在西歸浦的安德面，到濟州機場有一段車程，加上起飛前 2 小時報到，這天會比平常早出發。"
                "集合時間以領隊公布為準。",
                "退房前先把「隨身」與「託運」分好：託運合計 20 公斤、手提一件 10 公斤。"
                "超重只能在機場現場加購，每公斤 NT$420 或等值韓元，濟州機場只收韓元（可刷卡）。",
                "回程一樣<b>不供餐不給水</b>，在機場先吃點東西。剩下的韓元零錢可以在機場花掉。",
                "入境台灣別帶肉製品與新鮮蔬果。韓國泡麵多數含肉類調味粉，同樣在禁止之列。",
            ]),
        ],
    ),
]


def p_days():
    o = ["<h3>分日行程</h3>", "<p>單欄排列，點日期列展開。展開後有當日路線、景點細節與要注意的事，"
         "最下方可以直接跳到互動地圖看那一天的點位。</p>", '<div class="jeju-acc">']
    for i, (code, date, title, stay) in enumerate(DAYS, 1):
        route, meals, spots, sections = DAY_CONTENT[i - 1]
        o.append('  <details class="jeju-day" style="border-left:3px solid var(--d%d)"%s>' % (i, " open" if i == 1 else ""))
        o.append('    <summary><span class="d" style="color:var(--d%d)">%s　%s</span>'
                 '<span class="t">%s</span><span class="m">%s</span>%s</summary>' % (i, code, date, title, stay, CHEV))
        o.append('    <div class="jeju-daybody">')
        o.append('      <div class="jeju-route">' +
                 '<i>→</i>'.join('<span>%s</span>' % r for r in route) + '</div>')
        for name, when, text in spots:
            o.append('      <div class="jeju-spot"><h5>%s</h5><span class="when">%s</span>'
                     '<p>%s</p></div>' % (name, when, text))
        for sect_title, items in sections:
            o.append('      <h4 class="jeju-h4" style="margin:1.8rem 0 0">%s</h4>' % sect_title)
            o.append("      <ul>")
            for it in items:
                o.append("        <li>%s</li>" % it)
            o.append("      </ul>")
        o.append('      <div class="jeju-dayfoot">')
        o.append('        <button class="jeju-gotomap" type="button" data-goto-day="%d">%s在地圖上看這天</button>' % (i, ICON_MAP))
        for label, text in meals:
            o.append('        <span class="meal">%s%s　%s</span>' % (ICON_CLOCK, label, text))
        o.append("      </div>")
        o.append("    </div>")
        o.append("  </details>")
    o.append("</div>")
    return panel("days", "\n".join(o))


def p_map():
    chips = ['  <button class="jeju-pill" type="button" data-day="0" aria-selected="true">全部</button>']
    for i, (code, date, title, _) in enumerate(DAYS, 1):
        chips.append('  <button class="jeju-pill" type="button" data-day="%d" aria-selected="false" '
                     'style="border-color:var(--d%d);color:var(--d%d)">%s　%s</button>'
                     % (i, i, i, code, title.split("・")[0]))
    return panel("map", """<h3>互動地圖</h3>
<p>%d 個點位、五條當日路線，底圖是 CARTO（OpenStreetMap 資料），深色模式會換成暗色底圖。點左側卡片或地圖圖釘看細節，每個點都附 Google 地圖與導航連結。
地圖只在第一次打開這頁時才載入，不會拖慢其他分頁。</p>

<div class="jeju-mapchips" id="jeju-mapchips">
%s
</div>

<div class="jeju-mapwrap">
  <div class="jeju-mapside" id="jeju-mapside"></div>
  <div class="jeju-map" id="jeju-mapcanvas"><div class="jeju-mapload">地圖載入中…</div></div>
</div>

<div class="jeju-note">
  <b>圖釘是概略位置，導航連結用的是地名搜尋</b>，點出去會導到正確的地點。
  跆拳武藝秀、騎駱駝與 Marina K.C 的地點手冊沒寫，不在地圖上；桃園機場也不放進來，免得整張圖被拉到台灣海峽。
</div>
<div class="jeju-note">
  桌機滾輪只會捲頁，不會誤縮放地圖，要縮放請用左上角的 + / − 或雙指。
  手機上地圖預設是擋住的，點一下才開放拖曳，不然手指滑到地圖就會把整頁的捲動吃掉。
</div>""" % (len([p for p in POINTS if p[7] != TPE1[2]]), "\n".join(chips)))


def p_preflight():
    return panel("preflight", """<h3>行前檢查</h3>
<p>出發前要動手的事，按「什麼時候做」排，不按類別排。</p>

<div class="jeju-rows">
  <div class="jeju-when" style="border-left:3px solid var(--accent2)">
    <div class="w" style="color:var(--accent2)">現在</div>
    <div>
      <b>確認護照效期</b>
      <p>以出國日算要有 6 個月以上，也就是效期要到 2027/04/17 之後。不夠就得趕快換發。</p>
    </div>
  </div>
  <div class="jeju-when" style="border-left:3px solid var(--accent2)">
    <div class="w" style="color:var(--accent2)">前一週</div>
    <div>
      <b>在台灣先換韓幣</b>
      <p>D2 午餐只發 ₩8,000，市場攤商、ECO LAND 與松堂的小店都可能需要現金。千元、萬元鈔都帶一些。</p>
    </div>
  </div>
  <div class="jeju-when" style="border-left:3px solid var(--accent)">
    <div class="w" style="color:var(--accent)">10/14 起</div>
    <div>
      <b>填電子入境卡</b>
      <p>抵達前 72 小時內填，最早 10/14（三）傍晚可以開始。飯店地址旅行社會在出團前 3 個工作天提供，
      也可以直接用「入境韓國」分頁裡的第一晚飯店地址。填完把確認畫面存在手機裡。</p>
      <p><a href="https://www.e-arrivalcard.go.kr/" target="_blank" rel="noopener">e-arrivalcard.go.kr →</a></p>
    </div>
  </div>
  <div class="jeju-when" style="border-left:3px solid var(--d1)">
    <div class="w" style="color:var(--d1)">D1 中午</div>
    <div>
      <b>12:00 前到第一航廈，先吃飽</b>
      <p>泰瑞航空 11 號團體櫃台（華航代理），起飛前 2.5 小時集合、1 小時關櫃。
      機上不供餐不給水，過安檢後買好水與點心。</p>
    </div>
  </div>
  <div class="jeju-when" style="border-left:3px solid var(--d3)">
    <div class="w" style="color:var(--d3)">D3 早上</div>
    <div>
      <b>泳衣放在好拿的地方</b>
      <p>下午進神話世界，萬豪的莫西爾泳池住客免費，室外池開到 19:00、室內池到 21:00。泳帽也要帶。</p>
    </div>
  </div>
  <div class="jeju-when" style="border-left:3px solid var(--d5)">
    <div class="w" style="color:var(--d5)">D5 早上</div>
    <div>
      <b>退房前先分行李、秤重</b>
      <p>當天直接去機場。託運合計 20 公斤、手提一件 10 公斤，超重只能現場加購。</p>
    </div>
  </div>
</div>

<h4 class="jeju-h4">帶什麼、帶多少</h4>
<div class="jeju-g2">
  <div class="jeju-card">
    <div class="t" style="margin-top:0">衣服</div>
    <div class="d">10 月濟州平均約 13–23°C。白天長袖或薄針織衫，早晚加一件外套。濟州風大，那件外套最好防風。</div>
  </div>
  <div class="jeju-card">
    <div class="t" style="margin-top:0">盥洗用品</div>
    <div class="d">韓國飯店響應環保，不提供牙刷、牙膏等一次性備品。牙刷、牙膏、拖鞋、沐浴乳、洗髮精都自己帶。</div>
  </div>
  <div class="jeju-card">
    <div class="t" style="margin-top:0">插頭</div>
    <div class="d">220 V、圓頭兩孔。旅行社每人送一個轉接頭。房內不要用多孔延長線，容易跳電。</div>
  </div>
  <div class="jeju-card">
    <div class="t" style="margin-top:0">鞋子</div>
    <div class="d">D4 城山日出峰是連續階梯，登頂約 30 分鐘；其他天多半是市場與園區的平路。</div>
  </div>
</div>

<h4 class="jeju-h4">網路</h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:9.6rem">方式</th><th>方案</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">eSIM</td><td>KLOOK、KKday、易遊網等平台的韓國方案，出發前先安裝好</td></tr>
      <tr><td style="font-weight:700">實體 SIM</td><td>韓國上網卡，出發前在台灣買好</td></tr>
      <tr><td style="font-weight:700">漫遊</td><td>各家電信的韓國漫遊方案</td></tr>
    </tbody>
  </table>
</div>

<h4 class="jeju-h4">泰瑞航空行李規定 <em>團體票</em></h4>
<div class="jeju-g3">
  <div class="jeju-card"><div class="k">手提</div><div class="t" style="font-size:1.6rem">1 件　10 kg</div>
    <div class="d">去回程各一件</div></div>
  <div class="jeju-card"><div class="k">託運</div><div class="t" style="font-size:1.6rem">不限件數　合計 20 kg</div>
    <div class="d">自拍棒、腳架、刀剪類一定要託運</div></div>
  <div class="jeju-card"><div class="k">超重</div><div class="t" style="font-size:1.6rem">每公斤 NT$420</div>
    <div class="d">只能在機場現場買；濟州機場只收韓元，可刷卡</div></div>
</div>
<div class="jeju-note">
  <b>機票限制。</b>不能改日期或航班、不能轉讓、開票後不能退；座位由航空公司安排，也無法加價指定緊急出口座位。
</div>""")


def p_korea():
    return panel("korea", """<h3>入境韓國</h3>
<p>2026 年的規定。這趟唯一有時間壓力的是電子入境卡。</p>

<div class="jeju-callout">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
    stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"></rect>
    <line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line>
    <line x1="3" y1="10" x2="21" y2="10"></line></svg>
  <div>
    <b>電子入境卡（e-Arrival Card）　抵達前 72 小時內填妥</b>
    <p>免費，不是簽證。要準備：護照資料頁照片（含下方條碼區、不可反光）、Email、韓國飯店地址、航班 TW688。
    入境目的選「旅遊（個人）」，航班號碼直接填、不用按搜尋。已辦 SES 自動通關的人不用填。</p>
  </div>
</div>

<h4 class="jeju-h4">填表用的資料</h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:11rem">欄位</th><th>填什麼</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">抵達</td><td class="jeju-num">2026/10/17　航空　TW 688</td></tr>
      <tr><td style="font-weight:700">出發（離境）</td><td class="jeju-num">2026/10/21　航空　TW 687</td></tr>
      <tr><td style="font-weight:700">住宿地址</td><td>Hotel Air City Jeju　56, Sammu-ro, Jeju-si, Jeju-do 63124
        <span style="color:var(--muted)">　輸入英文後按選取，系統會帶出韓文</span></td></tr>
      <tr><td style="font-weight:700">聯絡電話</td><td class="jeju-num">+82-64-720-5000<span style="color:var(--muted)">　填飯店電話即可</span></td></tr>
    </tbody>
  </table>
</div>
<div class="jeju-note">
  同行 1–9 人可以一起申請，代表人需年滿 14 歲；入境日期若有變動要重新申請。完成後會寄確認信，存手機或印紙本備用。
  另外，系統的國家欄把台灣列為「CHINA(TAIWAN)」，外交部 2026 年 3 月曾因此建議民眾改填紙本入境卡；
  不過這團手冊寫明不提供紙本，實際以領隊指示為準。
</div>

<h4 class="jeju-h4">免申請 K-ETA</h4>
<div class="jeju-rules">
  <div class="jeju-rule"><span class="jeju-tag info">免</span>
    <div><b>台灣護照 2026/12/31 前入境韓國免申請 K-ETA</b><p>持效期 6 個月以上的護照與回程機票即可。17 歲以上入境時會留存雙手食指指紋與臉部照片。</p></div></div>
</div>

<h4 class="jeju-h4">禁止與限制</h4>
<div class="jeju-rules">
  <div class="jeju-rule"><span class="jeju-tag warn">禁</span>
    <div><b>EVE 系列止痛藥</b><p>部分品項含 allylisopropylacetylurea，在韓國屬管制藥品。需要止痛藥請換其他成分，並帶英文處方或成分說明。</p></div></div>
  <div class="jeju-rule"><span class="jeju-tag warn">禁</span>
    <div><b>行動電源、備用鋰電池不可託運</b><p>只能隨身，機上不能使用也不能充電。需清楚標示 Wh，100 Wh 以下可帶，100–160 Wh 要航空公司同意，160 Wh 以上禁止。
    充電孔貼絕緣膠帶、每顆分開裝袋。</p></div></div>
  <div class="jeju-rule"><span class="jeju-tag info">限</span>
    <div><b>暖暖包不可託運</b><p>2026 年起濟州等主要機場要求隨身攜帶。</p></div></div>
  <div class="jeju-rule"><span class="jeju-tag info">限</span>
    <div><b>噴霧類壓力瓶，出境每人限 1 瓶</b><p>例如髮妝噴霧。</p></div></div>
  <div class="jeju-rule"><span class="jeju-tag info">限</span>
    <div><b>金飾、金錶、項鍊</b><p>韓國海關管制嚴格，非必要少帶，免得通關卡住。</p></div></div>
</div>

<h4 class="jeju-h4">數量與金額上限</h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:12rem">項目</th><th>上限</th><th style="width:17rem">備註</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">隨身物品總值</td><td>USD 800</td>
        <td style="color:var(--muted)">自用品、禮品合計，超過會被課稅</td></tr>
      <tr><td style="font-weight:700">酒</td><td>2 瓶，合計 2 公升以內、USD 400 以內</td>
        <td style="color:var(--muted)">超過需申報</td></tr>
      <tr><td style="font-weight:700">香菸・香水</td><td>香菸 200 支／香水 100 ml</td>
        <td style="color:var(--muted)">超過需申報</td></tr>
    </tbody>
  </table>
</div>""")


def p_taiwan():
    return panel("taiwan", """<h3>入境台灣</h3>
<p>回程那一段。禁攜帶清單特地標了「最常見」，因為出事的幾乎都是那幾樣。</p>

<h4 class="jeju-h4">禁止攜帶</h4>
<div class="jeju-g2">
  <div class="jeju-card"><div class="k">最常見</div><div class="t" style="font-size:1.6rem">肉類製品</div>
    <div class="d">香腸、火腿、肉乾、肉鬆、罐裝肉，<b>以及含肉類調味粉的泡麵</b>。韓國泡麵大多屬於這一類。</div></div>
  <div class="jeju-card"><div class="k">最常見</div><div class="t" style="font-size:1.6rem">所有生鮮水果、蔬菜</div>
    <div class="d">濟州橘子、漢拏峰都算，市場買的請在韓國吃完</div></div>
  <div class="jeju-card"><div class="k">最常見</div><div class="t" style="font-size:1.6rem">未經核准的乳製品</div>
    <div class="d">生乳、未殺菌乳酪、部分手工起司</div></div>
  <div class="jeju-card"><div class="k">最常見</div><div class="t" style="font-size:1.6rem">高風險蛋製品</div>
    <div class="d">生蛋、半熟蛋、溏心蛋、未檢疫鹹蛋、茶葉蛋</div></div>
</div>

<div class="jeju-note">
  <b>判斷不了就主動問。</b>下機後可把動植物產品丟進農畜產品棄置箱，或到檢疫櫃檯主動申報，現場判定不合格也不會受罰。
  未申報被查獲至少罰 NT$3,000，違規攜帶肉類產品最高可罰 NT$100 萬。
</div>

<h4 class="jeju-h4">數量上限</h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:17rem">類別</th><th>限量</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">購物免稅額</td><td>每人 NT$20,000<span style="color:var(--muted)">　超過沒申報會被沒收或罰鍰</span></td></tr>
      <tr><td style="font-weight:700">一般食品</td>
        <td>總價值 &lt; USD 1,000，且總重量 ≤ 6 公斤<span style="color:var(--muted)">　零食、飲料、茶包等</span></td></tr>
      <tr><td style="font-weight:700">錠狀／膠囊保健食品</td>
        <td>每種 ≤ 12 瓶（盒、罐、包、袋），合計 ≤ 36 瓶<span style="color:var(--muted)">　維他命、酵素、膠原蛋白等</span></td></tr>
      <tr><td style="font-weight:700">應申報</td><td>酒類 &gt; 1.5 公升、捲菸 &gt; 1 條（200 支）、雪茄 &gt; 25 支</td></tr>
    </tbody>
  </table>
</div>

<h4 class="jeju-h4">醫療器材限量 <em>每人每半年一次為原則，且僅供個人自用</em></h4>
<div class="jeju-tw">
  <table class="jeju-table">
    <thead><tr><th style="width:22rem">類別</th><th>限量</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700">液體 OK 繃</td><td>最多 4 條（罐、瓶、支）</td></tr>
      <tr><td style="font-weight:700">醫用棉棒</td><td>最多 200 支</td></tr>
      <tr><td style="font-weight:700">日拋型隱形眼鏡</td><td>單一度數最多 60 片，每人限單一品牌、最多兩種度數</td></tr>
      <tr><td style="font-weight:700">矯正鏡片（近視／遠視）</td><td>最多 1 副</td></tr>
      <tr><td style="font-weight:700">醫用口罩</td><td>最多 250 片（個）</td></tr>
    </tbody>
  </table>
</div>""")


def p_out():
    return panel("out", """<h3>去程行李清單</h3>
<p>勾選狀態存在這台裝置的瀏覽器裡，關掉再打開還在。去程與回程各自獨立計數。</p>
""" + render_checklist("jeju2026Out", OUT_LIST) + """
<div class="jeju-note">
  <b>行動電源只能放隨身包，標示要看得到 Wh，而且要 100 Wh 以內。</b>充電孔貼絕緣膠帶、每顆各自裝袋。
  這條放在清單裡而不是規定頁，因為要在收行李的當下看到。
</div>""")


def p_back():
    return panel("back", """<h3>回程行李清單</h3>
<p>比去程多了一塊「伴手禮」，那是買回來的東西要放的地方。託運仍是合計 20 公斤，買之前先想好重量。</p>
""" + render_checklist("jeju2026Back", BACK_LIST) + """
<div class="jeju-note">
  <b>液體規則兩層都要顧。</b>隨身每容器 &lt; 100 ml、總量 &lt; 1 L；託運總液體 &lt; 5 L，
  酒單獨還有 1.5 公升的申報線。果醬、柑橘茶這類玻璃罐一律放託運。
</div>""")


def p_souvenir():
    rows = []
    for cid, cat, item, where, note, warn in SHOP:
        note_html = ('<span class="jeju-tag warn">%s</span>' % note) if (note and warn) else note
        rows.append(
            '        <tr><td><label class="jeju-check" data-id="%s" data-group="shop" '
            'style="border:0;background:transparent;min-height:0;padding:0">'
            '<input type="checkbox"><span class="sr"></span></label></td>'
            '<td style="color:var(--muted)">%s</td><td>%s</td>'
            '<td style="color:var(--muted)">%s</td>'
            '<td style="color:var(--muted)">%s</td></tr>' % (cid, cat, item, where, note_html))
    shop = ('<div class="jeju-checklist" data-key="jeju2026Shop">\n'
            '  <div class="jeju-progress">\n'
            '    <div class="jeju-bar"><i data-fill style="width:0"></i></div>\n'
            '    <strong class="jeju-count"><span data-count>0</span> / %d</strong>\n'
            '    <button class="jeju-reset" type="button" data-reset>清空</button>\n'
            '  </div>\n'
            '  <div class="jeju-tw" style="margin-top:1rem">\n'
            '    <table class="jeju-table">\n'
            '      <thead><tr><th style="width:3.4rem"></th><th style="width:7.2rem">類別</th><th>品項</th>'
            '<th style="width:16rem">行程中哪裡買</th><th style="width:17rem">備註</th></tr></thead>\n'
            '      <tbody>\n%s\n      </tbody>\n    </table>\n  </div>\n</div>' % (len(SHOP), "\n".join(rows)))
    return panel("souvenir", """<h3>伴手禮採買</h3>
<p>跟團行程沒有安排大型超市，能買東西的時段是 D1 東門市場、D2 雪綠茶園與偶來市場、D3 蓮洞與神話世界，
最後是 D5 的濟州機場。柑橘類與綠茶類在前兩天就能買齊。</p>

<h4 class="jeju-h4">按地點買什麼</h4>
<div class="jeju-g3">
  <div class="jeju-card" style="border-top:3px solid var(--d1)">
    <div class="k">濟州市　D1 東門市場／D3 蓮洞</div>
    <div class="d" style="color:var(--text)">橘子巧克力、柑橘果醬與柑橘茶、石頭爺爺小物；蓮洞有藥妝與韓系服飾</div>
  </div>
  <div class="jeju-card" style="border-top:3px solid var(--d2)">
    <div class="k">西歸浦　D2 雪綠茶園／偶來市場</div>
    <div class="d" style="color:var(--text)">O'sulloc 茶包禮盒、綠茶抹醬、innisfree 保養品、市場裡的柑橘加工品</div>
  </div>
  <div class="jeju-card" style="border-top:3px solid var(--d5)">
    <div class="k">收尾　D5 濟州機場</div>
    <div class="d" style="color:var(--text)">漏買的橘子巧克力、海苔、零食；剩下的韓元零錢在這裡用掉</div>
  </div>
</div>

<h4 class="jeju-h4">採買清單 <em>可勾選</em></h4>
""" + shop + """

<div class="jeju-note">
  <b>退稅。</b>貼有 Tax Free／Tax Refund 標誌的店家，結帳時出示護照就能辦理；部分店家可當場扣稅，
  其餘在機場辦理。實際門檻以店家與現場公告為準。
</div>
<div class="jeju-note">
  <b>回台免稅額每人 NT$20,000。</b>肉製品、新鮮柑橘、含肉泡麵都不能帶回台灣，詳見「入境台灣」分頁。
</div>""")


SCRIPT = r"""<script>
  (function () {
    'use strict';

    var root = document.getElementById('jeju-app');
    if (!root) { return; }

    var PANEL_KEY = 'jejuTripPanelV1',
      /* 地圖上的線與圖釘畫在淺色的 OSM 圖磚上，深淺模式都用這組較深的顏色，
         不跟著主題走——它要對比的是地圖底圖，不是頁面背景。
         頁面上的 chip 與側欄則相反，一律用 var(--d1..--d5)，那組會跟著主題提亮。 */
      DAY_COLORS = ['#1C6E8C', '#2E8B6F', '#C08327', '#C4452F', '#5B4B8A'],
      MAP_DATA = __MAP_DATA__,
      DAY_LABELS = __DAY_LABELS__,
      /* 必須在這裡就給值。下面的 showPanel(initial) 在開頁時就會執行，
         如果初始分頁是地圖（網址帶 #jeju-map，或上次停在地圖），
         它會呼叫 initMap()；那時若 mapState 還沒賦值就是 undefined，
         讀 .ready 會拋錯，整段 IIFE 後面全部不會執行，地圖就卡在「載入中」。 */
      mapState = { loading: false, ready: false, map: null, layers: {}, markers: {}, day: 0 };

    function $(sel, ctx) { return (ctx || root).querySelector(sel); }
    function $$(sel, ctx) { return [].slice.call((ctx || root).querySelectorAll(sel)); }

    /* ────────────────────────────────────────────────
       分頁切換。用 hidden 顯示／隱藏，不用 transform 平移，
       因為 Leaflet 在被 transform 過的容器裡算不準尺寸。
       ──────────────────────────────────────────────── */
    var tabs = $$('.jeju-pill[data-panel]'),
      panels = $$('.jeju-panel'),
      ids = tabs.map(function (t) { return t.getAttribute('data-panel'); });

    function showPanel(id, opts) {
      opts = opts || {};
      if (ids.indexOf(id) < 0) { id = ids[0]; }
      panels.forEach(function (p) { p.hidden = p.id !== 'jeju-panel-' + id; });
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-panel') === id;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (on && opts.scrollTab !== false) {
          t.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
      });
      try { localStorage.setItem(PANEL_KEY, id); } catch (e) {}
      if (id === 'map') { initMap(); }
      if (opts.scrollTop) {
        root.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        var id = t.getAttribute('data-panel');
        showPanel(id);
        if (history.replaceState) { history.replaceState(null, '', '#jeju-' + id); }
      });
    });

    /* 鍵盤左右鍵在分頁列上移動 */
    $('.jeju-pills').addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') { return; }
      var cur = ids.indexOf(document.activeElement.getAttribute('data-panel'));
      if (cur < 0) { return; }
      e.preventDefault();
      var next = (cur + (e.key === 'ArrowRight' ? 1 : -1) + ids.length) % ids.length;
      tabs[next].focus();
      showPanel(ids[next]);
    });

    /* 開頁時決定停在哪一頁：網址 hash 優先，其次上次看的那頁 */
    var initial = (location.hash || '').replace('#jeju-', '');
    if (ids.indexOf(initial) < 0) {
      try { initial = localStorage.getItem(PANEL_KEY) || ids[0]; } catch (e) { initial = ids[0]; }
    }
    showPanel(initial, { scrollTab: false });

    /* 分日行程的「在地圖上看這天」 */
    $$('[data-goto-day]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var d = parseInt(btn.getAttribute('data-goto-day'), 10);
        showPanel('map', { scrollTop: true });
        setDayFilter(d);
      });
    });

    /* ────────────────────────────────────────────────
       勾選清單。每份清單各自一組 localStorage，
       改版沿用舊 key 與舊 data-id，既有勾選不會被清掉。
       ──────────────────────────────────────────────── */
    $$('.jeju-checklist').forEach(function (list) {
      var key = list.getAttribute('data-key'),
        labels = $$('[data-id]', list),
        fill = $('[data-fill]', list),
        count = $('[data-count]', list),
        stats = $$('[data-stat]', list),
        state = {};

      try { state = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { state = {}; }

      function save() {
        try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) {}
      }

      function refresh() {
        var done = 0, gDone = {}, gTotal = {};
        labels.forEach(function (lbl) {
          var id = lbl.getAttribute('data-id'),
            g = lbl.getAttribute('data-group'),
            box = lbl.querySelector('input'),
            on = !!state[id];
          box.checked = on;
          lbl.classList.toggle('done', on);
          /* 藥妝表的勾選格塞在 <td> 裡，整列一起劃掉才看得出來 */
          var tr = lbl.closest('tr');
          if (tr) { tr.style.opacity = on ? '.5' : ''; }
          gTotal[g] = (gTotal[g] || 0) + 1;
          if (on) { done++; gDone[g] = (gDone[g] || 0) + 1; }
        });
        if (count) { count.textContent = done; }
        if (fill) { fill.style.width = labels.length ? (done / labels.length * 100) + '%' : '0'; }
        stats.forEach(function (s) {
          var g = s.getAttribute('data-stat'),
            d = gDone[g] || 0, t = gTotal[g] || 0;
          s.querySelector('b').textContent = d + ' / ' + t;
          s.classList.toggle('full', t > 0 && d === t);
        });
      }

      labels.forEach(function (lbl) {
        lbl.querySelector('input').addEventListener('change', function (e) {
          state[lbl.getAttribute('data-id')] = e.target.checked;
          save();
          refresh();
        });
      });

      var reset = $('[data-reset]', list);
      if (reset) {
        reset.addEventListener('click', function () {
          state = {};
          save();
          refresh();
        });
      }

      refresh();
    });

    /* ────────────────────────────────────────────────
       互動地圖。Leaflet 只在第一次打開這頁時才抓，
       其他分頁不必為了它多下載 150 KB。
       ──────────────────────────────────────────────── */
    function loadOnce(tag, attrs) {
      return new Promise(function (resolve, reject) {
        var el = document.createElement(tag);
        Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
        el.onload = resolve;
        el.onerror = function () { reject(new Error('load failed')); };
        document.head.appendChild(el);
      });
    }

    function initMap() {
      if (mapState.ready || mapState.loading) {
        if (mapState.ready) { mapState.map.invalidateSize(); }
        return;
      }
      mapState.loading = true;
      Promise.all([
        loadOnce('link', { rel: 'stylesheet', href: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css' }),
        loadOnce('script', { src: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js' })
      ]).then(buildMap).catch(function () {
        var c = document.getElementById('jeju-mapcanvas');
        c.innerHTML = '<div class="jeju-mapload">地圖載入失敗，請確認網路連線後重新整理。</div>';
        mapState.loading = false;
      });
    }

    function buildMap() {
      var canvas = document.getElementById('jeju-mapcanvas');
      canvas.innerHTML = '';
      /* scrollWheelZoom 關掉，桌機滾輪就只是捲頁、不會誤縮放。 */
      var mobile = L.Browser.mobile,
        map = L.map(canvas, {
          scrollWheelZoom: false,
          dragging: !mobile
        }).setView([33.38, 126.56], 10);
      /* 底圖換成 CARTO：淺色模式用 Voyager（色調偏暖、道路較淡，彩色圖釘比較跳），
         深色模式用 Dark Matter。瀨戶內海那頁用的是 OSM 標準圖磚，這裡刻意不同。
         主題可以在頁面上即時切換，所以監看 body 的 class，變了就換一組圖磚。 */
      var TILE = {
          light: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
          dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
        },
        isDark = function () { return document.body.classList.contains('colorscheme-dark'); },
        tiles = L.tileLayer(isDark() ? TILE.dark : TILE.light, {
          maxZoom: 19,
          subdomains: 'abcd',
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors ' +
            '&copy; <a href="https://carto.com/attributions">CARTO</a>'
        }).addTo(map);
      if (window.MutationObserver) {
        new MutationObserver(function () {
          var want = isDark() ? TILE.dark : TILE.light;
          if (tiles._url !== want) { tiles.setUrl(want); }
        }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
      }

      /* 手機：先擋著，點一下才開放拖曳。開了就不再關。 */
      if (mobile) {
        canvas.classList.add('gated');
        var gate = document.createElement('div');
        gate.className = 'jeju-mapgate';
        gate.innerHTML = '<span>點一下啟用地圖</span>';
        gate.addEventListener('click', function () {
          map.dragging.enable();
          canvas.classList.remove('gated');
        });
        canvas.appendChild(gate);
      }

      MAP_DATA.forEach(function (day, di) {
        var n = di + 1,
          color = DAY_COLORS[di],
          group = L.layerGroup();
        L.polyline(day.map(function (p) { return [p.lat, p.lng]; }), {
          color: color, weight: 3, opacity: 0.65, dashArray: '7,6'
        }).addTo(group);
        day.forEach(function (p, k) {
          /* 圖釘一律用「當天」的顏色。先前是按類別上色，但那組類別色
             跟天別色是同一批 hex，於是 Day 2 的景點會顯示成 Day 4 的顏色。
             類別本來就寫在 popup 的第二行，不需要再用顏色編碼一次。 */
          var c = color,
            q = encodeURIComponent(p.q || (p.lat + ',' + p.lng)),
            m = L.marker([p.lat, p.lng], {
              icon: L.divIcon({
                className: '', iconSize: [26, 26], iconAnchor: [13, 13],
                html: '<span class="jeju-pin" style="background:' + c + '">' + (k + 1) + '</span>'
              })
            });
          m.bindPopup(
            '<div class="jeju-pop"><div class="h">' + p.name + '</div>' +
            '<div class="m">Day ' + n + '　' + p.t + '　' + p.kind + '</div>' +
            '<div class="x">' + p.note + '</div>' +
            '<div class="btns">' +
            '<a target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=' + q + '">Google 地圖</a>' +
            '<a class="alt" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=' + q + '">導航</a>' +
            '</div></div>', { maxWidth: 280 });
          m.addTo(group);
          mapState.markers[n + '_' + k] = m;
        });
        mapState.layers[n] = group;
        group.addTo(map);
      });

      mapState.map = map;
      mapState.ready = true;
      mapState.loading = false;
      renderSide();
      applyFilter();
      setTimeout(function () { map.invalidateSize(); }, 60);
    }

    function renderSide() {
      var side = document.getElementById('jeju-mapside'), html = '';
      MAP_DATA.forEach(function (day, di) {
        var n = di + 1;
        if (mapState.day !== 0 && mapState.day !== n) { return; }
        html += '<div class="jeju-mapday"><i style="background:var(--d' + n + ')"></i>' +
          '<b>Day ' + n + '　' + DAY_LABELS[di] + '</b></div>';
        day.forEach(function (p, k) {
          html += '<button class="jeju-mapcard" type="button" data-marker="' + n + '_' + k + '">' +
            '<span class="t" style="color:var(--d' + n + ')">' + p.t + '</span>' +
            '<span class="n">' + p.name + '</span>' +
            '<span class="x">' + p.note + '</span></button>';
        });
      });
      side.innerHTML = html;
      $$('[data-marker]', side).forEach(function (btn) {
        btn.addEventListener('click', function () {
          var m = mapState.markers[btn.getAttribute('data-marker')];
          if (!m) { return; }
          mapState.map.setView(m.getLatLng(), 13, { animate: true });
          m.openPopup();
        });
      });
    }

    function applyFilter() {
      if (!mapState.ready) { return; }
      var bounds = [];
      Object.keys(mapState.layers).forEach(function (n) {
        var show = mapState.day === 0 || String(mapState.day) === n;
        if (show) {
          mapState.layers[n].addTo(mapState.map);
          MAP_DATA[n - 1].forEach(function (p) { bounds.push([p.lat, p.lng]); });
        } else {
          mapState.map.removeLayer(mapState.layers[n]);
        }
      });
      if (bounds.length) { mapState.map.fitBounds(bounds, { padding: [30, 30] }); }
    }

    function setDayFilter(d) {
      mapState.day = d;
      $$('#jeju-mapchips [data-day]').forEach(function (c) {
        var i = parseInt(c.getAttribute('data-day'), 10),
          on = i === d,
          /* 用 CSS 變數而不是寫死的 hex，否則一點下去就會把深色模式
             提亮過的那組換成淺色模式的深色，chip 在深底上讀不出來。 */
          tint = i > 0 ? 'var(--d' + i + ')' : '';
        c.setAttribute('aria-selected', on ? 'true' : 'false');
        /* 選取＝該天的顏色填滿；未選＝同色描邊。「全部」沒有專屬色，
           留空讓 CSS 的 aria-selected 規則接手。 */
        c.style.background = on && tint ? tint : '';
        c.style.borderColor = tint;
        c.style.color = on ? (tint ? 'var(--on-accent)' : '') : tint;
        c.style.fontWeight = on ? '700' : '';
      });
      initMap();
      renderSide();
      applyFilter();
    }

    $$('#jeju-mapchips [data-day]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        setDayFilter(parseInt(chip.getAttribute('data-day'), 10));
      });
    });
  })();
</script>"""


def build():
    # 地圖路線只畫濟州島上的點；桃園機場那兩筆留在卡片清單，不畫線、不放圖釘，
    # 否則 fitBounds 會把整張地圖拉到台灣海峽。
    days_json = []
    for n in range(1, 6):
        days_json.append([
            {"t": t, "name": name, "kind": kind, "lat": lat, "lng": lng, "note": note, "q": q}
            for (d, t, name, kind, lat, lng, note, q) in POINTS if d == n and q != TPE1[2]
        ])
    labels = [d[1] for d in DAYS]

    script = (SCRIPT
              .replace("__MAP_DATA__", json.dumps(days_json, ensure_ascii=False))
              .replace("__DAY_LABELS__", json.dumps(labels, ensure_ascii=False)))

    parts = [
        STYLE,
        "",
        '<div class="jeju" id="jeju-app">',
        '  <section class="jeju-hero">',
        '    <div class="jeju-herogrid">',
        '      <div class="jeju-herotext">',
        '        <div class="jeju-eyebrow">JEJU · 5 DAYS</div>',
        "        <h2>直飛來回　濟州島五日</h2>",
        "        <p>2026/10/17（六）－10/21（三）。跟團行程，泰瑞航空桃園－濟州直飛來回；"
        "前兩晚住濟州市區，後兩晚住西歸浦的神話世界度假村。</p>",
        "      </div>",
        "      " + island_svg(),
        "    </div>",
        rail(),
        "  </section>",
        "",
        render_nav(),
        "",
        p_overview(), "",
        p_days(), "",
        p_map(), "",
        p_preflight(), "",
        p_korea(), "",
        p_taiwan(), "",
        p_out(), "",
        p_back(), "",
        p_souvenir(),
        "</div>",
        "",
        script,
        "",
    ]
    banner = ("<!-- 這個檔案由 tools/make_jeju_fragment.py 產生，請勿手動編輯。\n"
              "     要改內容請改那支腳本再重跑，否則下次執行就會被蓋掉。 -->")
    html = "\n".join([banner] + parts)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return html


if __name__ == "__main__":
    html = build()
    # 這台機器的 stdout 走 cp950，印中文會變亂碼，所以摘要一律用 ASCII。
    n_out = sum(len(x) for _, _, _, subs in OUT_LIST for _, x in subs)
    n_back = sum(len(x) for _, _, _, subs in BACK_LIST for _, x in subs)
    print("out      : %s" % OUT)
    print("size     : %.1f KB" % (len(html.encode("utf-8")) / 1024.0))
    print("panels   : %d" % len([t for t in TABS if t]))
    print("map pts  : %d" % len([p for p in POINTS if p[7] != TPE1[2]]))
    print("checkbox : outbound %d / return %d / shop %d" % (n_out, n_back, len(SHOP)))
