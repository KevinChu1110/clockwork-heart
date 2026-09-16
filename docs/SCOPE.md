# SCOPE · 範圍與砍單

> 完整作品靠「收斂」，不靠「什麼都做」。  
> **2026-08 R2：** 採納第二輪審——3 個月縮為 C0+C1+C2+C6，約 4～5 小時。  
> **2026-09 稽核：** 依 ROADMAP.md、PROJECTS.json 與 main 實作進度完成過期待辦核對與狀態回填。  
> 變更範圍時先改本檔，再改實作。

## 產品形態

| 項目 | 3 個月（現實版） | 6 個月 |
|------|------------------|--------|
| 主線 | **C0+C1+C2+C6** 可通關；約 **4～5 小時** | 加 C3/C4/C5 完整域；**8～12 小時** |
| 存檔 | **本地 + 匯出／匯入** | 雲存檔可選 |
| 連線 | 不做（或極簡 stub） | L1 殘影／蠟燭等 |
| 平台 | **手機（iOS／Android）＋ 電腦／Web**（TestFlight／Google Play 內測 ＋ Web 版） | 多平台正式發行／上架（手機雙商店 ＋ 電腦／Web） |
| 宣發句 | 「日常如呼吸，聖獸戰會記得你」 | 同左加深 |

---

## 垂直切片（月 1 第一優先）✅

**C0 序章 + C1 騎士域到雷歐戰結束**（約 1.5～2h 可玩）

驗收：陌生人能說出 **灰鬚、釘釘、以劍抵爪** 三個詞。

- [x] 可行走／對話／存檔讀檔（已於 main 實裝，見 game/scripts/player.gd、dialogue_manager.gd、save_manager.gd）  
- [x] 即時雜魚戰（已於 main 實裝，見 game/scripts/battle/battle_sim.gd）  
- [x] 雷歐：王者斬格擋 → 以劍抵爪 → 微末一格（已於 main 實裝，見 game/scripts/battle/battle_sim.gd、test_combat_acceptance.gd）  
- [x] 拔劍三振、釘釘認劍、麥穗桿、體型對照（已於 main 實裝/落定：拔劍三振/釘釘認劍/麥稈見 game/scripts/main.gd；體型對照已於 0.15.1 依回饋降噪撤除，見 battle_view.gd:237）  
- [x] 器階基礎、觀星教學（簡）、橫斬（已於 main 實裝，見 equipment_system.gd、soul_system.gd、skill_system.gd）  

---

## 3 個月 —— 可通關短篇（砍後）

### 主線路徑（定案）

```
C0 序章 → C1 騎士域（完整）→ C2 白霧之地（完整，白霧看破）
    → C3～C5 旅途蒙太奇（簡）→ C6 塔＋魔王＋終章
```

| 章 | 3m 深度 | 備註 |
|----|---------|------|
| C0 | 完整 | 含爆點 |
| C1 | 完整 | 含雷歐精做、淨化前後視覺 |
| C2 | 完整可玩 | 白霧機制精做；**中段信 N8** |
| C3 道場 | **蒙太奇** | 一句旁白+可選一場簡戰；完整阿波 6m |
| C4/C5 | 日誌／地圖節點提及即可 | 6m 展開 |
| C6 | 完整反轉+戰+終章 | 不砍 |

### 敘事
- [x] 主反轉（魔王＝前任至弱者）決戰前（已於 main 實裝，見 main.gd:7544、codex.json）  
- [x] 鏽劍伏筆回收（器之廳／釘釘）（已於 main 實裝，見 main.gd:7531-7536、7631）  
- [x] **N8 延遲的信**（C2 休息點，中段情感錨）（已於 main 實裝，見 story_anchors.gd、ROADMAP 月2）  
- [x] 騎士域淨化前後視覺差（**僅此域 3m 必做**）（已於 main 實裝，戰勝後旗幟/門開/地圖實體切換，見 main.gd:6785、map_catalog.gd:329）  
- [x] 典籍／日誌精簡版（已於 main 實裝，見 story_codex.gd、codex.json、main.gd）  

### NPC
- [x] P0 核心進遊戲（可略簡立繪）：至少麥穗、灰鬚、釘釘、絲絨、小芽、霧隱、星讀、斷頁；浪人／阿茶可簡（已於 main 實裝，見 game/data/npc_lines/ 及 sprite_db.gd）  
- [x] 主線 flag ≥2 階台詞（灰鬚、釘釘、麥穗線）（已於 main 實裝，見 game/data/npc_lines/greybeard.json、ding.json、maisui_village.json）  
- [x] 支線 ≥2（小芽木劍、可選一條）（已於 main 實裝，包含小芽木劍、釘釘舊債、白霧家書、浪人酒共 4 條，見 quest_system.gd、main.gd）  

### 戰鬥
- [x] 即時自動雜魚（已於 main 實裝，見 game/scripts/battle/battle_sim.gd）  
- [x] **雷歐以劍抵爪**（P0）（已於 main 實裝，見 game/scripts/battle/battle_sim.gd、test_combat_acceptance.gd）  
- [x] **白霧看破**（3m 第二精做機制）（已於 main 實裝，見 game/scripts/battle/battle_sim.gd、ROADMAP 月2）  
- [x] 阿波／其餘：部位+台詞底模或蒙太奇（已於 main 實裝，阿波/疾影/石拳均已實裝部位破壞與戰鬥，見 battle_sim.gd、ROADMAP 月4）  
- [x] 時間模型鎖版（已於 main 實裝，見 docs/PROJECTS.json balance-lock、BALANCE.md §5、ROADMAP 月2）  

### 養成（能用即可）
- [x] 器：鍛造升階（失敗不掉階）；主線夠用到通關（已於 main 實裝，見 equipment_system.gd、forge_dialog.gd、ROADMAP 月2）  
- [x] 魂：星屑→觀星（足跡權重）；**儀式感**見 PROGRESSION（已於 main 實裝，見 soul_system.gd、ROADMAP 月2、PROJECTS.json soul-simplify）  
- [x] 招：劍系習得+升級 **只改倍率**（不換動作幀）（已於 main 實裝，見 skill_system.gd、ROADMAP 月2）  
- [ ] 技能升級華麗特效 → **6m**（現況：未做，依包體控制與降噪原則維持純倍率升級，後置 6m）  

### 爆點 3m 必做

**原 6 料：**
- [x] M1 拔劍三振（已於 main 實裝，見 main.gd:1633 c0_sword_triple_pull、codex.json）  
- [x] M2 體型對照（已於 0.15.1 依玩家回饋畫面花雜降噪撤除，見 commit 286a83f、battle_view.gd:237 _hide_size_compare()）  
- [x] C3 微末一格（已於 main 實裝，見 battle_view.gd:2711、title_catalog.gd、SCRIPT_C1.md）  
- [x] C6 我拒絕字級（已於 main 實裝，見 battle_view.gd、test_temptation_dopamine.gd、test_c6_dual_ending.gd）  
- [x] N2 釘釘認劍（**主線必經，不可藏**）（已於 main 實裝，見 main.gd:6310 c1_ding_recognized_sword、7535）  
- [x] N4+N5 麥稈 + 託付句（已於 main 實裝，見 story_anchors.gd、test_c6_dual_ending.gd）  

**R2 追加（極低成本）：**
- [x] **N8 延遲的信**（中段錨）（已於 main 實裝，見 story_anchors.gd、main.gd、ROADMAP 月2）  
- [x] **M5 旗幟簽名**（淨化後歪扭兔爪）（已於 main 實裝，見 main.gd:6786 c1_flag_paw、map_catalog.gd:329）  
- [x] **N3 灰鬚轉身開門**（已於 main 實裝，見 main.gd:6785 c1_gate_open_back、UI 多語系）  
- [x] **W4 釘釘連敗摔錘台詞**（已於 main 實裝，見 forge_dialog.gd、forge_system.gd、main.gd、ROADMAP 月2）  

**時間夠再做（P1）：** M4 勝利坐姿、M6 黑焰咬劍  

### 存檔／連線 3m
- [x] 本地存檔（已於 main 實裝，見 save_manager.gd、ROADMAP 月3）  
- [x] 匯出／匯入檔案（當「雲」替代）（已於 main 實裝，見 save_manager.gd、mobile_settings.gd、ROADMAP 月3）  
- [ ] ~~雲存檔~~ → **6m**（現況：未做，依 3m 砍單規劃後置 6m，以本地匯出入備份替代）  
- [ ] ~~殘影／共鬥~~ → **6m**（現況：未做，依 docs/BUSINESS.md 採單機 F2P 體驗，連線共鬥後置/不進）  

### 傳播
- [x] 成就 **6～8** 個核心（非 12）（已於 main 實裝核心 11 項稱號，見 title_catalog.gd、ROADMAP 月3）  
- [x] 隱藏 HUD（已於 main 實裝精簡 HUD 與 F3 切換，見 main.gd、ROADMAP 月3）  
- [x] 多平台商店／發行文案用定稿句（SHARE）（已於 main/docs 實裝，見 docs/SHARE.md、ROADMAP 月3）  

### 明確不進 3 個月
- C3/C4/C5 完整可玩密度  
- 雲存檔、連線 L1+  
- 公會、賽季、Steam 全套  
- 全武器線、飾品六槽、技能特效升級  
- 全域淨化視覺、五星畫兔（可 6m）  

**3 個月驗收：**  
通關約 4～5h；記得 ≥2 NPC；有抵爪 clip；聽懂魔王反轉；中段有信。

---

## 6 個月 —— 加厚（不另開 IP）

- [x] C3 阿波完整（對話並行可做）（已於 main 實裝，見 battle_sim.gd、ROADMAP 月4）  
- [x] C4/C5 可玩（已於 main 實裝，見 battle_sim.gd、region_catalog.gd、ROADMAP 月4）  
- [ ] 雲存檔、殘影、可選共鬥（現況：未做，依 docs/BUSINESS.md 維持本地 F2P 單機，雲端連線後置/不列當前範圍）  
- [ ] 技能特效分級、更多成就（現況：未做/部分完成；稱號已擴充至 11 項，技能特效分級依降噪與包體控制維持純倍率）  
- [ ] 全域淨化差、記憶節、五星畫兔（現況：未做，列為 6m/P2 待定項目，見 ROADMAP.md 月6）  
- [ ] 黑焰迴響／計時器／隱藏 BOSS（已作廢，見 docs/BUSINESS.md 與 docs/PROJECTS.json cut-systems 下架項，聚焦手遊主線與每日發條）  
- [ ] 多平台正式發行（手機＋電腦／Web，若測試有反響）（現況：進行中/待發行；0.7.0 內測包已產出，待雙商店審核上架，見 ROADMAP.md 月6）  

---

## 永不做（同前）

Discord 唯一客戶端、主線鎖網、無縫大世界、付費 gacha、麥穗幻覺主線、半途換 Phaser 空轉。
（2026-09-04 已由 DECISIONS 變現模式定案取代，保留供歷史對照）
