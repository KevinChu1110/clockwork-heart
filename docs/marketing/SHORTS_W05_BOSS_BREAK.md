# W5 Short 腳本 · 點哪碎哪！泰坦部位拆卸（小魚 · 短影音草案）

> **Persona**：小魚 · 短影音  
> **核心信念**：前三秒決定生死，畫面自己會說話。一支只講一件事。  
> **對齊進度**：本週最新實裝（§8 標準場探索→戰鬥→拆部位、泰坦雷歐雙部位鎖定破甲、四族武裝打擊手感與 Hitstop 停頓、BREAK 齒輪零件崩飛與洩壓機制）。  
> **世界觀與武器規格（嚴格對齊 CANON 與 review.md）**：  
> - 兔＝單手長劍、獅＝長槍、狐＝法杖、豬＝巨錘。  
> - 全員金屬板件／琺瑯烤漆公仔，零毛皮，背後外露黃銅發條鑰匙。  
> - BREAK 演出為發條機械結構崩解、螺絲齒輪爆散與蒸氣洩壓，全年齡友善，**嚴禁血肉、生物骨骼與斷肢**。  
> **製作規範**：本單為純文件規格，嚴禁使用 AI 冒充實機。素材一律指向 repo 既有之實機錄影（REC-01~04）、§8 標準場截圖（proofs）與五族已過審姿態資產。

---

## 基本資料

| 項目 | 內容 |
|---|---|
| **週次** | W5（12 週題庫 Boss 專題） |
| **片名** | 《點哪碎哪！泰坦部位拆卸》 |
| **規格時長** | 剛好 30.0 秒（直式 9:16，1080×1920，30fps） |
| **前 3 秒鉤子** | **【點哪碎哪，裝甲崩解！】**（第 0 秒即 Boss 戰極限格擋 ＋ 泰坦重盾部位護甲炸裂高光） |
| **預期指標** | 完播率、重播率、吸引留言「打擊感很讚」「部位拆卸好爽」「這是什麼遊戲」 |
| **成片檔名** | `web/media/shorts/w05_boss_break_30s.mp4` |
| **實機素材來源** | `game/scenes/battle/battle.tscn`（雷歐戰鬥與部位 HUD）、REC-01~04 實機錄影、§8 標準場流程、五族戰鬥攻擊實機姿態 |

---

## 30 秒鏡頭分鏡與時間軸（Shot-by-Shot）

| 秒數區段 | 鏡頭與畫面動作 | 實機操作與鏡頭語言 | 聲音設計（實體金屬音優先） | 畫面字幕（中下 1/3 安全區） | 對應 repo 真實素材路徑 |
|---|---|---|---|---|---|
| **0.0s – 3.0s**<br>（爆發鉤子<br>Hook 3s） | **【鏡 A：開局極限格擋＋部位炸裂】**<br>第 0 秒無片頭、無 Logo，畫面直接特寫守衛泰坦·雷歐（Leo）揮刃猛劈。指尖瞬間點擊畫面觸發「PARRY!」藍白光芒爆散；緊接著指尖疾點雷歐「獅衛重盾」部位條，金光與碎裂特效炸開，金色立體大字「BREAK」破空爆散，雷歐重盾護甲崩解後仰！ | 實機戰鬥手勢招架與部位條破壞。開局 0 秒直接給破壞的高光爽感。<br>鏡頭：平視平滑微推（Push In 115%），聚焦受擊停頓與金色 BREAK 跳字。 | 呼嘯破空重風聲 → 金屬彈刀重音（Clang!）→ 發條齒輪崩解碎裂聲（Shatter!）與高壓洩壓音。<br>⚠️ 嚴禁開場 BGM，以金屬實體音直擊耳膜。 | **點哪碎哪，裝甲崩解！**<br>（高飽和金黃粗體字） | - `docs/marketing/shots/rec04_overdrive_break_9x16.mp4`<br>- `docs/marketing/shots/rec04_overdrive_break.png`<br>- `screenshots/proof_battle_attack_strike.png`<br>- `screenshots/proof_mobile_battle_damage.png` |
| **3.0s – 10.0s**<br>（情境鋪陳<br>Setup 7s） | **【鏡 B：§8 探索遇敵＋直覺指尖鎖定部位】**<br>畫面自神殿小鎮荒路探索切入實機戰鬥全景。展示手機端純手勢操作與右手拇指熱區（`ThumbPad`）。玩家遭遇守衛泰坦雷歐（HP 420），畫面右側展開部位 HUD（`PartBars`：獅衛重盔、獅衛重盾）。指尖點擊 `ThumbLock` 或直接觸控雷歐重盾部位條，鎖定指示器清晰圈定重盾，展現直覺鎖定。 | 展示手機端人體工學：告別笨拙的虛擬搖桿與技能輪盤，指尖即武器，全手勢直覺開打。<br>鏡頭：平視直式實機視野平滑推向右側操作熱區與敵方血條（Push In 112%）。 | 明快的 16-bit 戰鬥節奏打擊鼓點，俐落的機械按鍵點擊音「噠、噠」，部位鎖定蜂鳴「滴！」。 | **告別虛擬搖桿<br>指尖直鎖泰坦部位** | - `screenshots/proof_02_explore_town.png`<br>- `screenshots/proof_battle_polish_leo.png`<br>- `screenshots/proof_leo_shadow_box.png`<br>- `screenshots/proof_battle_crop_enemytag.png`<br>- `docs/marketing/shots/rec01_thumb_pad_9x16.mp4`<br>- `docs/marketing/shots/rec01_thumb_pad.png`<br>- `game/scripts/systems/standard_scene_s8/s8_smoke_flow.gd`<br>- `game/scripts/systems/standard_scene_s8/s8_smoke_view.gd` |
| **10.0s – 22.0s**<br>（核心賣點<br>Core 12s） | **【鏡 C：四職發條武裝連擊＋裝甲零件崩解】**<br>四職發條武裝輪番登場集火雷歐重盾部位：<br>1. 白金兔手持「單手長劍」突刺揮斬；<br>2. 烈鬃獅雙手端「長槍」前衝貫穿；<br>3. 靈尾狐高舉「法杖」晶核引爆；<br>4. 鋼牙豕雙手揚起「巨錘」重砸地裂！<br>精準觸發 0.08s~0.15s Hitstop 停頓，怒氣滿額引動金光，重盾部位條徹底見底！雷歐重盾金屬板件崩飛，齒輪彈簧與糖果屑粒子漫天噴散，觸發破防降防（def_down）！ | 嚴格遵守 CANON 與 review.md 武器規範：兔劍、獅槍、狐杖、豬錘。展示刀刀有回饋的金屬打擊感與零件崩解特效（零血肉）。<br>鏡頭：隨四職招式交替快速推進（Push In 120%），打擊卡點白閃。 | 晨光長劍出鞘破空「颼——」→ 皇家長槍貫擊「鏘啷！」→ 法杖晶爆「轟！」→ 鍛爐戰鎚重砸「咚——！」→ 金屬零件齒輪爆散「乒乓咔啦！」。 | **四職武裝鎖定狂攻<br>零件崩散 · 徹底拆卸！** | - `screenshots/proof_battle_rabbit.png`<br>- `screenshots/proof_battle_attack_sword.png`<br>- `game/assets/sprites/player/poses/attack.png`<br>- `screenshots/proof_battle_lion.png`<br>- `screenshots/proof_battle_lion_attack_lance.png`<br>- `game/assets/sprites/player/poses/lion/attack.png`<br>- `screenshots/proof_battle_fox.png`<br>- `screenshots/proof_battle_fox_attack_staff.png`<br>- `game/assets/sprites/player/poses/fox/attack.png`<br>- `screenshots/proof_battle_boar.png`<br>- `screenshots/proof_battle_boar_attack_hammer.png`<br>- `game/assets/sprites/player/poses/boar/attack.png`<br>- `screenshots/proof_battle_crop_rage.png`<br>- `game/scripts/systems/candy_chip_vfx/candy_chip_vfx.gd` |
| **22.0s – 27.0s**<br>（情緒收束<br>Payoff 5s） | **【鏡 D：洩壓解除暴走＋收劍勝利姿態】**<br>重盾崩解後，守衛泰坦雷歐背部安全閥彈開，劇烈噴出高壓白色蒸氣（洩壓解除暴走狀態），陷入短暫機械硬直。白兔勇者側身俐落收劍，背後噴散多巴胺彩糖星芒粒子（大廳戳碰揮劍動作），對話氣泡彈出可愛互動，定格展現反差治癒感。 | 戰鬥勝利與危機化解的反差回饋，展現 2.2 頭身 Q 萌與俐落動作反差，引導觀眾互動。<br>鏡頭：鏡頭緩慢向主角收劍姿態拉近（Push In 108%），周圍星芒擴散。 | 高壓蒸氣劇烈排氣「嘶——！」→ 清脆收劍「叮」聲（Ching!）→ 溫暖柔和的 16-bit 木管尾音。 | **洩壓解除暴走<br>這打擊感，你給幾分？** | - `docs/marketing/shots/rec02_battle_polish_9x16.mp4`<br>- `docs/marketing/shots/rec02_battle_polish.png`<br>- `screenshots/proof_bravesoul_hero_interact.png`<br>- `screenshots/proof_bravesoul_village.png` |
| **27.0s – 30.0s**<br>（品牌收束<br>CTA 3s） | **【鏡 E：品牌字標與簡介引流】**<br>白閃無縫切入純黑底板（`title_plate.png`），中央後製疊加官方字標《發條之心》（`logo_cn.png`）。下方標語：「給心上弦，重新出發。」右下角顯現小白黃銅發條鑰匙剪影。底部標註：「開發中畫面 · 官網搶先看」。 | 品牌官方識別定格，維持純淨設計，依第 15/16 條不提價格、不承諾上市日、不放未上架商店鈕。<br>鏡頭：純黑底板微幅緩推 102%，字標金屬邊緣一道柔和暖金光澤掠過。 | 一聲清脆悠長、餘音裊裊的單聲發條齒輪咬合「喀嗒」（`clock.wav`），全片乾淨收尾。 | **官網連結在簡介 · 發條之心**<br>（留言區聊聊） | - `branding/title_plate.png`<br>- `branding/logo_cn.png`<br>- `screenshots/proof_title_bright.png` |

---

## 實機素材檔案真實性清單（全部通過 `test -f` 驗證）

本腳本各鏡次所引用之畫面與資產，100% 存在於倉庫之中，嚴禁任何虛構路徑：

### 1. 核心實機錄影片段（9:16 直式 H.264）
- `docs/marketing/shots/rec01_thumb_pad_9x16.mp4`（右手拇指熱區實機操作，301 KB）
- `docs/marketing/shots/rec01_thumb_pad.png`（右手拇指熱區截圖，1,631 KB）
- `docs/marketing/shots/rec02_battle_polish_9x16.mp4`（戰鬥平滑渲染與受擊反饋實機，325 KB）
- `docs/marketing/shots/rec02_battle_polish.png`（戰鬥畫面截圖，1,480 KB）
- `docs/marketing/shots/rec04_overdrive_break_9x16.mp4`（暴怒與打擊實機錄影，411 KB）
- `docs/marketing/shots/rec04_overdrive_break.png`（暴怒打擊截圖，1,495 KB）

### 2. §8 標準場與戰鬥證明截圖（Screenshots & Proofs）
- `screenshots/proof_02_explore_town.png`（§8 標準場城鎮探索實機，1,406 KB）
- `screenshots/proof_battle_polish_leo.png`（雷歐守衛泰坦實機戰鬥，1,530 KB）
- `screenshots/proof_leo_shadow_box.png`（雷歐雙部位與落地陰影，1,351 KB）
- `screenshots/proof_battle_attack_strike.png`（戰鬥斬擊命中高光瞬間，1,191 KB）
- `screenshots/proof_battle_crop_enemytag.png`（敵方 Boss 血條與標籤裁切，15 KB）
- `screenshots/proof_battle_crop_rage.png`（怒氣槽狀態裁切，19 KB）
- `screenshots/proof_11_battle.png`（橫屏實機對決介面，1,658 KB）
- `screenshots/proof_mobile_battle_damage.png`（暴擊飄字與 BREAK 破防標籤，841 KB）
- `screenshots/proof_bravesoul_hero_interact.png`（主角大廳戳碰彩糖星芒與揮劍姿態，423 KB）
- `screenshots/proof_bravesoul_village.png`（浮空島大廳晴空全景，414 KB）
- `screenshots/proof_title_bright.png`（明亮標題畫面，1,425 KB）

### 3. 四族發條武裝資產（嚴格對齊武器世界觀）
- **兔族（白金兔 · 劍士 · 單手長劍）**：
  - 姿態檔案：`game/assets/sprites/player/poses/attack.png`（12,808 Bytes）
  - 實機截圖：`screenshots/proof_battle_rabbit.png`（1,200 KB）
  - 武器截圖：`screenshots/proof_battle_attack_sword.png`（795 KB）
- **獅族（烈鬃獅 · 騎士 · 長槍）**：
  - 姿態檔案：`game/assets/sprites/player/poses/lion/attack.png`（21,930 Bytes）
  - 實機截圖：`screenshots/proof_battle_lion.png`（1,209 KB）
  - 武器截圖：`screenshots/proof_battle_lion_attack_lance.png`（829 KB）
- **狐族（靈尾狐 · 法師 · 法杖）**：
  - 姿態檔案：`game/assets/sprites/player/poses/fox/attack.png`（22,205 Bytes）
  - 實機截圖：`screenshots/proof_battle_fox.png`（1,207 KB）
  - 武器截圖：`screenshots/proof_battle_fox_attack_staff.png`（830 KB）
- **豬族（鋼牙豕 · 戰士 · 巨錘）**：
  - 姿態檔案：`game/assets/sprites/player/poses/boar/attack.png`（28,444 Bytes）
  - 實機截圖：`screenshots/proof_battle_boar.png`（1,206 KB）
  - 武器截圖：`screenshots/proof_battle_boar_attack_hammer.png`（821 KB）

### 4. 品牌固定資產與程式系統
- `branding/key_visual_main.png`（主視覺基準圖，1,735 KB）
- `branding/logo_cn.png`（手繪中文官方字標）
- `branding/title_plate.png`（片尾黑底板）
- `game/scenes/battle/battle.tscn`（實機戰鬥主場景）
- `game/scripts/battle/battle_view.gd`（`_ensure_part_hud`、`_part_bars` 部位破壞系統）
- `game/scripts/systems/standard_scene_s8/s8_smoke_flow.gd`（§8 探索→戰鬥→拆部位煙測流程）
- `game/scripts/systems/candy_chip_vfx/candy_chip_vfx.gd`（糖果屑與金屬崩散粒子）

---

## 剪輯組裝指引（剪映／Premiere 貼上執行）

1. **畫幅與幀率**：統一 9:16（1080×1920），30fps，重要 UI 與打擊數值維持在中央 70% 安全區內。
2. **0–3s 鉤子黃金律**：第 0 秒絕不黑屏、絕不放 Logo，第 1 秒準確卡點 PARRY 金屬彈刀重音，第 2 秒準確卡點 BREAK 護甲炸開音效。
3. **四職換招節奏（10–22s）**：每職招式約 2.5～3.0 秒，招式交替以「4 幀白閃（Flash White）」或金屬打擊衝擊線轉場，保持連續打擊節奏。
4. **零件崩解視覺**：BREAK 爆開時疊加 `candy_chip_vfx` 粒子與齒輪裝甲彈飛動態，展現「金屬拆卸、無血肉」的爽快感。
5. **音效層次**：BGM 採用低飽和 16-bit 輕快節奏鼓點，音量控制在 -18dB；前方金屬打擊音（刀劍、長槍、法術、戰鎚、齒輪崩解、蒸氣洩壓）維持在 -6dB，強化刀刀到肉的反饋。

---

## 社群貼文文案（YouTube Shorts / Facebook Reels / TikTok）

```
點哪碎哪！這才是玩具世界的部位拆卸 🔥

誰說像素手遊只能互相刮痧？
看準守衛泰坦「雷歐」的重盾與裝甲，
長劍突刺、長槍破防、法杖引爆、戰鎚重砸！
打碎接縫、金光崩解，直接洩壓解除暴走！

⚡ 本週實裝焦點：
・純手勢直覺觸控，指尖直鎖泰坦部位
・四職武裝（兔劍／獅槍／狐杖／豬錘）連擊破甲
・齒輪裝甲崩解，零毛皮、零血肉機械拆卸！

這部位拆卸打擊感，你給幾分？留言區告訴我們👇

▶️ 官網探索：https://KevinChu1110.github.io/clockwork-heart/
⬇️ 下載頁面：https://KevinChu1110.github.io/clockwork-heart/pages/download.html

#發條之心 #ClockworkHeart #手遊推薦 #打擊感 #部位拆卸 #極限格擋 #Shorts #獨立遊戲 #像素動作
```

---

## 總監審核規範逐項對照核對表（review.md）

- [x] **0–3 秒鉤子（第 11 條）**：前 3 秒無片頭、無遊戲名、無 Logo、無自我介紹，直接給「極限格擋＋部位炸裂」高光結果。
- [x] **四職武器規範（review.md 9/9a 條）**：嚴格對齊兔＝單手長劍、獅＝長槍、狐＝法杖、豬＝巨錘，絕無混淆。
- [x] **世界觀 CANON 規範（CANON 第 22 條）**：覺醒的金屬發條玩具公仔，外露發條鑰匙、胡桃鉗色盤、金屬板件與螺絲，BREAK 為機械結構零件崩解，全年齡友善零血肉。
- [x] **真實素材規範（第 19/19b 條）**：全數素材均指向 repo 內真實存在的實機錄影與截圖資產，無杜撰路徑，無 AI 虛假概念圖。
- [x] **片尾點題卡規範（第 15/16/19c 條）**：後製無失真疊加 `branding/logo_cn.png` 於 `branding/title_plate.png`，不承諾上市日、不提價格、不放未實裝商店按鈕。
- [x] **純文件守則**：本任務僅新增腳本文件，未產圖、未產片、未調用任何付費 API。
