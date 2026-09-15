# 第一部 · 發條之心的開始（審閱包 v0.1）

給 Kevin 看的第一版：**場景卡全表 + C0 首場正文三件套 + 遊戲內手札**。

---

## 你要看的檔

| 檔案 | 內容 |
|------|------|
| [00_outline_scene_cards.md](00_outline_scene_cards.md) | **60 張**主線／外傳場景卡標題 |
| [book1_c0_s02_ember_night.md](book1_c0_s02_ember_night.md) | **C0 燃燒之夜**全文 ≈1500 字 + 對白壓稿 + Short 字幕 |
| [book1_c1_s01-04_gate_forge.md](book1_c1_s01-04_gate_forge.md) | **C1-S01~S04 門衛與重鍛**全文 ≈1800 字 |
| [book1_c1_s05-08_leo_eve.md](book1_c1_s05-08_leo_eve.md) | **C1-S05~S08 星讀至雷歐前夜**全文 ≈1800 字 |
| [book1_c1_s09-13_leo_climax.md](book1_c1_s09-13_leo_climax.md) | **C1-S09~S13 雷歐高潮～五柱皆危**全文 ≈2600 字 + 對白壓稿 + Short 字幕 |
| [book1_c2_s01-04_white_fog.md](book1_c2_s01-04_white_fog.md) | **C2-S01~S04 白霧之地至真假同色**全文 ≈2600 字 + 對白壓稿 + Short 字幕 |
| [book1_c2_s05-07_third_shadow.md](book1_c2_s05-07_third_shadow.md) | **C2-S05~S07 白霧第三個影子至家書與舊影**全文 ≈3400 字 + 對白壓稿 + Short 字幕 |
| [book1_c3_s01-05_why_we_fight.md](book1_c3_s01-05_why_we_fight.md) | **C3-S01~S05 道場的鐘至塔路開了**全文 ≈3200 字 + 對白壓稿 + Short 字幕 |
| [book5_c4_s01-03_wait_for_wind.md](book5_c4_s01-03_wait_for_wind.md) | **C4-S01~S03 等風的人至你追上了風**全文 ≈3200 字 + 對白壓稿 + Short 字幕 |
| [book5_c5_s01-03_stone_fist.md](book5_c5_s01-03_stone_fist.md) | **C5-S01~S03 岸上沒有退路至站到最後**全文 ≈4800 字 + 對白壓稿 + Short 字幕 |
| [bookX_cx_s01_six_realms.md](bookX_cx_s01_six_realms.md) | **CX-S01 六域風物詩**全文 ≈516 字（純漢字 470 字）+ 對白壓稿 + Short 字幕 |
| `game/data/story/codex.json` | 手札 10 條（C0～C1 雷歐、C2 白霧仙狐、C3 阿波、C4 疾影） |
| `game/scripts/systems/story_codex.gd` | 解鎖邏輯 |
| 暫停選單 → **旅途手札** | 遊戲內閱讀入口 |

架構說明仍見：`docs/marketing/STORY_NOVEL_AND_SHORTS.md`

---

## 第一部範圍（Book 1）

場景卡 **#01～#35**（C0 序章離村 → C1 堡壘雷歐 → C2 白霧之地收束 → C3 武鬥道場與開通塔路）  
目前已完成正文進度：
- **C0**（#01～#08 全部場景卡正文已完稿）
- **C1**（#09～#23 全部場景卡正文已完稿）
- **C2**（#24～#30 全部場景卡正文已完稿，含白霧仙狐戰與霧中家書）
- **C3**（#31～#35 全部場景卡正文已完稿，含阿波破勢試煉與塔路解鎖）
- **C4**（#36～#38 全部場景卡正文已完稿，含疾影停拍試煉與銀羽獲取）
- **C5**（#39～#41 全部場景卡正文已完稿，含石拳對撞破岩甲試煉與炎心獲取）
- **CX-S01**（#42 間章「六域風物詩」蒙太奇過場正文完稿，銜接 C6 通天黑塔）

建議你審的重點：

1. **語氣**：怕、但不油；舊鑰溫度夠不夠  
2. **三選一**：小說是否保留選擇空間（目前用括號交代）  
3. **拔劍三振**：節奏是否值得當 Short 梗  
4. **手札密度**：遊戲裡讀的 `body` 是否太短／太長  

---

## 遊戲裡怎麼試手札

1. 開新局走序章  
2. 開場旁白後 → 解鎖「預言與今夜」  
3. 拔起鏽劍 → 「燃燒之夜」  
4. 離村 → 「舊閣樓的氣味」  
5. 荒路首戰勝 → 「第一戰·像呼吸」  
6. **Esc → 旅途手札（n/max）** 點開閱讀  

Toast 會提示「旅途手札：××」。

---

## Short（W1）成片 · 完整 30 秒

| 項目 | 位置 |
|------|------|
| **上傳用 30s** | `web/media/shorts/w01_c0_ember_night_30s.mp4` |
| 分鏡原料 | 同資料夾 `w01_*` 三支 8s |
| 字幕腳本 | `book1_c0_s02_ember_night.md` 附 B |
| 說明 | `web/media/shorts/README.txt` |

**字幕請在剪映加上後再發** YT Shorts／FB。

---

## 下一版若 OK 可接著

- 寫 C0-S04 鏽劍三振專場、C0-S05 舊閣樓的氣味擴寫  
- 手札加 C1 釘釘／星讀  
- 官網「故事」頁連載第一場  

有要改的語氣或情節，直接批在 md 上即可。
