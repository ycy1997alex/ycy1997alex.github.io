---
title: "Day 22｜是不是可以用 Claude 開一家旅行社了？"
date: 2026-09-05T00:00:00+08:00
authors: ["尤俊硯"]
series: ["iThome 2026 鐵人賽"]
tags: ["Claude", "iThome"]
summary: "把日本旅行的行程交給 Claude：從 Word 整理出 Excel 時間表、PowerPoint 簡報與互動地圖，拿掉不能公開的內容後整合成網站上的一頁。"
description: "把日本旅行的行程交給 Claude：從 Word 整理出 Excel 時間表、PowerPoint 簡報與互動地圖，拿掉不能公開的內容後整合成網站上的一頁。"
---

> 本文首發於 [iThome 2026 鐵人賽](https://ithelp.ithome.com.tw/articles/10407930)。

> 本篇階段：Prj#4 個人網頁

> 使用介面：Claude Code（via VS Code）

---

## 前情

[Day 21](https://ithelp.ithome.com.tw/articles/10407692) 把兩份教召清單從 Word 跟 Excel 搬上網站，是從無到有。今天材料換成九月底一趟即將成行的日本旅行，嘗試看看查閱景點之後，能不能讓 Claude 幫我完成更多的事項，無論是自由行或跟團，都能夠有更簡單的準備方式並可以記錄在個人網頁上，作為自己的生活雜記。

一開始是拿一份行程初稿做的，但最近拿到最終版行程，我自己重新整理了一份 Word 後，接著請 Claude 依它做出 Excel 時間表、PowerPoint 簡報，還有一張互動地圖的 HTML。

所以今天來看看 Claude 依照我的改版需求，會做出什麼樣的內容？而且也順便看看請 Claude 做出一個旅遊靜態網頁的能力如何（包含我指定的互動式地圖功能）！

---

## 1. 這頁本來長怎樣

原本這頁的內容，我放在 [2026-setouchi_舊版存檔.html](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/2026-setouchi_%E8%88%8A%E7%89%88%E5%AD%98%E6%AA%94.html)，而原始碼我放在 [2026-setouchi_舊版存檔.html (原始碼)](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day22_20260905/2026-setouchi_%E8%88%8A%E7%89%88%E5%AD%98%E6%AA%94.html)。

存檔頁最上面那條黃底提示，是留給誤點進來的人看的，說明這份不再更新。整頁是一個卡片式的分頁介面：上半部固定放行程摘要，下半部用 11 個分頁切換，從總覽、行前檢查、入境與行李、去程與回程的打勾清單，一路排到 Day 1 至 Day 5 與伴手禮採買，勾選狀態會存到瀏覽器裡。

![舊版存檔頁的「總覽」分頁](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-01-old-overview.png)

單看內容其實沒什麼問題，行程主線、五天摘要、來回班機、住宿，連跟第二梯次會在哪幾天碰上都整理進去了，資料密度是夠的。切到 Day 1 是同一套版型，當日路線一條、景點卡片一排、底下一則小提醒：

![舊版存檔頁的 Day 1 分頁](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-02-old-day1.png)

問題不在資訊，而在排版，會使得眼睛不知道要先看哪裡。

---

## 2. 原本有的問題

我對舊版不滿意的地方是字級，覺得「字太大」，所以請 Claude 去比對昨天做的那兩頁，看差在哪。

它給的答案是：

第一，舊版有大量文字根本沒被設定字級，直接繼承主題預設的 18px；而我覺得剛好的那頁，幾乎每個元素都明寫了尺寸，沒有一處是靠繼承來的。

第二，舊版用了 16 種不同尺寸，從 13.5px 排到 40px，相鄰級距有三處只差 0.5px。人眼分不出 0.5px，那些階層在視覺上等於不存在，只留下「整片都偏大」的印象。

所以在新版先設定成 22 / 18 / 16 / 15 / 13 五級，每一處都明寫。這裡有個細節：主題把 `html` 設成 `font-size: 62.5%`，所以 `1rem` 是 10px 而不是 16px，所有數字都得照這個基準換算。

把兩版的頁首擺在一起最清楚。舊版：

![舊版頁首：主標 40px，摘要卡數值 21px，分頁鈕 16px](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-03-fontsize-old.png)

新版：

![新版頁首：主標 22px，日期軸與分頁鈕都是 13px](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-04-fontsize-new.png)

同樣是 1440 寬的視窗，舊版光頁首就吃掉 379px，新版是 278px。主標從 40px 收到 22px，原本橫排的「旅遊天數／交通方式／住宿數量／主題重點」四張摘要卡，換成五格一列的日期軸，D1 到 D5 直接把五天的地名排出來。少掉的那一百多 px 不是重點，重點是縮完以後，頁面上終於有層次的感覺（標題大、其他一律小）。

---

## 3. 把分散生成的內容整理到同一頁面

在拿到最新版的行程手冊之後，我重新整理了一份 Word，裡面加了不少自己簡單查到的旅遊資訊，接著請 Claude 依它做出 Excel 時間預估表（想大概知道行程可能怎麼走、行程多久）、PowerPoint 簡報，還有一張互動地圖的 HTML。最可惜的是那張互動地圖沒有放到網頁上，所以這次請 Claude 把這些分散的資訊整理後，放到個人網頁上。

原本的 [WORD 檔案](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day22_20260905/%E5%BB%A3%E5%B3%B6%E9%80%B2%E3%83%BB%E9%AB%98%E6%9D%BE%E5%87%BA%EF%BC%88%E7%80%A8%E6%88%B6%E5%85%A7%E6%B5%B7%EF%BC%89%E4%BA%94%E6%97%A5%E8%A1%8C%E7%A8%8B%E6%94%BB%E7%95%A5_%E5%85%AC%E9%96%8B%E7%89%88.docx)與[EXCEL 檔案](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day22_20260905/%E5%BB%A3%E5%B3%B6%E9%80%B2%E3%83%BB%E9%AB%98%E6%9D%BE%E5%87%BA%EF%BC%88%E7%80%A8%E6%88%B6%E5%85%A7%E6%B5%B7%EF%BC%89%E4%BA%94%E6%97%A5%E8%A1%8C%E7%A8%8B%E6%99%82%E9%96%93%E8%A1%A8_%E5%85%AC%E9%96%8B%E7%89%88.xlsx)與[PPT 檔案](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day22_20260905/%E5%BB%A3%E5%B3%B6%E9%AB%98%E6%9D%BE%E4%BA%94%E6%97%A5%E8%A1%8C%E7%A8%8B_%E5%85%AC%E9%96%8B%E7%89%88.pptx)都可以透過連結獲得。

而原本生成的互動地圖，放在[互動網頁](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/%E5%BB%A3%E5%B3%B6%E9%AB%98%E6%9D%BE%E4%BA%94%E6%97%A5_%E4%BA%92%E5%8B%95%E5%9C%B0%E5%9C%96_%E5%85%AC%E9%96%8B%E7%89%88.html)與[互動網頁原始碼](https://github.com/ycy1997alex/ycy1997alex-oss-projects/blob/main/iThome-2026-Ironman/Day22_20260905/%E5%BB%A3%E5%B3%B6%E9%AB%98%E6%9D%BE%E4%BA%94%E6%97%A5_%E4%BA%92%E5%8B%95%E5%9C%B0%E5%9C%96_%E5%85%AC%E9%96%8B%E7%89%88.html)。

我給 Claude 的 Word 大概是這個樣子，入境規定、網路方案、行李限制、每日行程、伴手禮清單全部堆在同一份文件裡：

![整理給 Claude 的 Word（公開版）中的「入境前注意事項」一節](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-05-word-source.png)

它做出來的 Excel 是五張工作表：行程總覽、每日行程、移動時間估算、住宿與聯絡、說明與假設。每日行程那張最有意思的是「時長(分)」這一欄。藍字是可以自己改的輸入值，結束時間則是公式串起來的，改一格，後面整串時間會跟著往後移：

![Excel 時間表「每日行程」工作表的 Day 1 段落](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-06-excel-timetable.png)

簡報是 12 頁：封面、五日總覽、航班與集合、Day 1 到 Day 5 各一頁，最後是行程節奏、自由活動時段、住宿資訊與行前提醒。抓四頁出來看：

![簡報的封面、五日總覽、Day 1 時間軸與行程節奏](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-07-pptx-slides.png)

互動地圖則是一個單檔 HTML，Leaflet 配 OpenStreetMap 底圖，左邊是當日卡片、右邊是地圖，上方用日期標籤過濾：

![互動地圖公開版，顯示全部日期的狀態](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-08-standalone-map.png)

把這四個檔案整合到同一頁，看起來舒服多了！

---

## 4. 上線前必須拿掉的內容

我給 Claude 的那份 Word 裡有集合地點的名稱，還有領隊與旅行社窗口的姓名和手機號碼。這些放在自己電腦裡沒問題，放上公開網站是另一回事，那是第三人的個人資料，而且會被搜尋引擎收錄。

我把整份 Word 匯出成 PDF 掛在頁面上，所以先做了一份公開版，把公司名換成泛稱、姓名電話那段改成一句「見紙本手冊」。

比較不直覺的是地圖。原始資料裡 Day 1 的第一個點是公司集合地點，帶著精確到小數點後五位的經緯度。就算把名稱改成「集合地點」，那組座標本身就是揭露。所以那一筆整個刪掉，Day 1 從桃園機場起算。

---

## 5. 成品

最終的成品在網站上：[2026 瀨戶內海五日跟團遊](https://ycy1997alex.github.io/zh-tw/posts/2026-setouchi/)。

新版一樣是分頁，但分頁重新分過：總覽、分日行程、互動地圖是主要的三個，後面用分隔線隔成行前檢查／入境日本／入境台灣、去程與回程清單、伴手禮採買三組。

![新版的「總覽」分頁](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-09-new-overview.png)

分日行程改成單欄摺疊，點日期才展開，展開後有當日路線、景點細節、晚上可以去哪，最下面一行能直接跳到互動地圖看那一天的點位：

![新版的「分日行程」分頁，D1 展開的狀態](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-10-new-days.png)

地圖是這次最想搬進來的部分。24 個點位、五條當日路線，每個點都附 Google 地圖與導航連結。有兩個處理我覺得做得不錯：地圖只在第一次切到這個分頁時才載入，不會拖慢其他分頁；桌機滾輪只捲頁、不縮放地圖，免得滑過去整頁被吃掉。

![新版的「互動地圖」分頁](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-11-new-map.png)

> 註：Setouchi（瀨戶內）指的是日本本州西部、四國與九州北部之間，環繞瀨戶內海的地理區域與周邊島嶼。

---

## 小結

今日主要在測試以 Claude 輔助規劃行程的效果怎麼樣。

其實在今年稍早的自由行我已經試著用免費版的 Claude 試做過了（製作時間約是 2026 年 3 月），請見 [2026東京近郊自駕](https://ycy1997alex.github.io/posts/2026-tokyo-drive/)，還記得當時是使用 Sonnet 4.X 的模型做的，其實完成度已經算是不錯了。但到現在已經有 Fable 5.X & Opus 5 & Sonnet 5 的時代，整體的完成度又高了一截，還是讓我驚豔。

![2026 東京近郊自駕，2026 年 3 月用免費版做出來的版本](https://ycy1997alex.github.io/ycy1997alex-oss-projects/iThome-2026-Ironman/Day22_20260905/day22-12-tokyo-drive.png)

其實同一套卡片加分頁的骨架，那時候就已經成形了XD

~~看來日後的出遊對我這種 J 人來說可以偷懶一點了XD~~

## 參考資料

網頁地圖技術

- Leaflet — 開源互動地圖函式庫 — https://leafletjs.com/
- OpenStreetMap（地圖底圖資料） — https://www.openstreetmap.org/copyright

---

> 註一：本篇的行程資訊與入境規定均以 2026 年 9 月當下查到的版本為準，請以官方公告為準。

> 註二：文中描述的 Claude Code 行為以 2026 年 9 月這段期間的實際操作為準，屬於單次操作的定性觀察，不一定是可重現的評測；產品行為會隨版本改變。

> 註三：頁面上與本文提到的原始檔，凡涉及第三人姓名、聯絡方式或特定地點座標的部分均已移除，公開的版本與我手邊的版本並不相同。
