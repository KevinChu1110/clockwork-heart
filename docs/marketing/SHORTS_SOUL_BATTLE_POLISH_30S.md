# 《發條之心》30 秒短影音分鏡腳本與實機錄影素材清單
## 主題：戰魂收斂與戰鬥手感全面升級（內部代號：mk-shorts）

> **文件狀態**：純文件與分鏡規劃階段（不產圖、不產影片、不花錢調用付費 API）。  
> **制定日期**：2026-09-08  
> **負責人**：行銷總監 阿珊（sidemkt）  
> **對應項目**：`docs/PROJECTS.json` 中的 `mk-shorts`（短影音腳本與實機素材）  
> **核心賣點**：**「戰魂收斂後的新手感與戰鬥打擊全面升級」** —— 不重講世界觀，聚焦展現戰鬥變得直覺、爽快、好看，系統收斂告別繁瑣。  
> **交付物依據**：對齊 `references/media.md` 短影音格式、`references/brand_assets.md` 鏡頭語言準則、`references/art_direction.md` §6.5 之 9:16 規格，以及 `references/review.md` 第 10～19 條影片檢查清單。

---

## 一、基本參數與製作規範

| 項目 | 規範標準 | 說明 |
|---|---|---|
| **本片主題（內部代號）** | 戰魂收斂＋戰鬥手感新版（`mk-shorts`） | ⚠️ 內部企劃代號，片內絕不出現此字串；片尾點題卡僅呈現官方字標 `branding/logo_cn.png` |
| **總長度** | **剛好 30.0 秒** | 平台黃金完播區（28～32 秒），節奏明快緊湊 |
| **畫幅比例** | **9:16 直式（1080×1920）** | 全片各鏡統一比例，嚴禁混用 16:9 或 4:5 |
| **總鏡頭數** | 6 個分鏡（Shot 1～6） | 鏡次接龍銜接，同一機位與動態軸線，拒絕靜圖幻燈片輪播 |
| **發布平台** | YouTube Shorts / Facebook Reels / TikTok | 直式短影音主戰場 |
| **開場 3 秒（Hook）** | **狀態與懸念**（極近微距發條上弦＋核心充能） | 嚴禁 Logo、嚴禁遊戲名稱、嚴禁自我介紹與公版宣傳語 |
| **點題卡（CTA）** | 僅置於 Shot 6（27.0～30.0s） | 標題卡由後製無失真疊加 `branding/logo_cn.png`，嚴禁 AI 生成；標註「開發中畫面 · 官網搶先看」 |
| **音效原則** | **真實金屬發條實體音效優先** | 發條緊繃、齒輪咬合、金屬斬擊、蒸氣洩壓；嚴禁罐頭史詩管弦配樂 |
| **素材來源真實性** | **100% 基於已合併 main 之功能** | 嚴格遵守 review.md 第 19 條與第 19b 條，標「實機」者必須為真實 Godot 錄影 |

---

## 二、核心賣點轉譯：從痛點到手感

本支短影音專門針對玩家最在意的「好不好玩、打得爽不爽、養起來累不累」進行反轉訴求，徹底打消複雜度疑慮：

1. **視覺換血（告別粗顆粒）**：
   - 全面去像素量化，手繪插畫質感渲染。
   - 角色深色厚描邊（`game/shaders/outline.gdshader`）＋ 獨立層落地柔化橢圓軟影（`game/shaders/foot_shadow.gdshader`），角色輪廓立體、腳踏實地不飄浮。
2. **手感進化（單手輕鬆打）**：
   - 右手拇指人體工學熱區（`ThumbPad`：攻擊、換武、鎖定、技能、暫停），熱區 ≥50px，單手拇指打完一場。
   - 0.15s 打擊停頓時間模型（Hitstop），受擊震顫與金光暴擊跳字，刀刀有肉、金屬反饋扎實。
3. **聚魂養成（透明首屏保底）**：
   - 聚魂殿四階金屬發條封靈罐（綠→藍→紫→橙），無任何業餘 Emoji，發條機械儀式感十足。
   - 首屏透明保底進度條（60/100 虔誠度，每滿 100 轉化 1 碎片），機制清楚透明，告別隱形坑與繁瑣。

---

## 三、接鏡軸線與運鏡節奏設計

本片拒絕靜圖硬切與 PPT 投影片感，採用「微距懸念 → 實機指尖操作 → 打擊爆發 → 養成回饋 → 終極過載 → 品牌點題」的連續鏡頭流：

```
Shot 1 (0.0-3.0s)  【概念·微距】上背發條微距慢推，鑰匙轉半圈，青綠核心充能爆亮
        │ (光芒暴漲，轉場穿透進入實機手遊螢幕)
Shot 2 (3.0-7.5s)  【實機·操控】神殿荒路戰鬥，單手右手拇指熱區連點：長劍突刺＋換武
        │ (揮劍橫斬動態接刀，鏡頭跟隨劍尖衝擊)
Shot 3 (7.5-15.5s) 【實機·視覺】雷歐戰平視特寫：厚描邊＋落地柔化軟影＋0.15s 打擊停頓火花與受擊反饋
        │ (劍刃擊破金光，金色光弧向下注入封靈罐)
Shot 4 (15.5-20.5s)【實機·養成】聚魂殿封靈罐開光金芒，鏡頭推入展示首屏透明保底進度條
        │ (罐口金光流轉，能量注入戰魂插槽，急切回戰場)
Shot 5 (20.5-27.0s)【實機·高潮】怒氣滿 100%，一指點擊 Overdrive 齒輪過載超轉速狂暴斬擊與部位 BREAK
        │ (最後一記重劈震屏白閃，瞬間切純黑)
Shot 6 (27.0-30.0s)【合成·點題】純黑底板微推，後製疊加官方字標《發條之心》（branding/logo_cn.png），發條定格
```

---

## 四、30 秒分鏡詳表（Shot-by-Shot）

| 鏡次 | 秒數 | 畫面內容 | 鏡頭運動（運鏡語言） | 聲音設計（實體音優先） | 字幕與文案 | 素材標註與真實性（對齊 review.md） |
|---|---|---|---|---|---|---|
| **Shot 1<br>【上弦懸念】** | `0.0-3.0s`<br>(3.0s) | 昏暗工坊微距。米白金屬發條兔小白背後四分之三側背，斑駁黃銅發條鑰匙清晰破出剪影。鑰匙猛然自動上弦轉動半圈，胸口青綠核心光芒瞬間爆亮，照亮斑駁齒輪與金屬長劍。 | 極近距微距慢推（Dolly In 105%），景深極淺，焦點由後背鑰匙移至劍刃火星。兔子主體不位移。 | 開場第 0 秒一記清脆乾淨的發條咬合「喀——嗒！」，緊接著發條緊繃與核心充能的沉穩共鳴低音。**禁止任何 BGM，禁止開場音效庫。** | （開場 3 秒無文字，無 Logo，僅在畫面邊緣呈現微弱金屬反光） | **【概念素材·9:16】**<br>依據 `ART_DIRECTION.md` §6.5 提示詞規格生成之首幀定格微動畫面。<br>⚠️ 依第 11 條：嚴禁開場出現遊戲名、Logo 或任何宣傳字。 |
| **Shot 2<br>【單手熱區】** | `3.0-7.5s`<br>(4.5s) | 鏡頭穿透光芒無縫切入實機戰鬥。小白 vs 荒路殘兵。展示神殿荒路背景與右側「右手拇指操作熱區」（`ThumbPad`）。玩家虛擬指尖輕點右下角 `ThumbAttack`（攻擊）連續出招，隨即點擊 `ThumbSwitch` 順暢切換巨錘。 | 平視直式實機展示視角，戰鬥畫面居中，右側熱區在按鈕觸發時伴隨微幅觸控反饋漣漪縮放。 | 乾脆俐落的機械按鍵點擊音「嗒、嗒」，長劍出鞘破空聲「颼——」，武器切換時齒輪彈射嵌合聲「咔嚓」。 | 【一指打完整場】<br>右手拇指熱區 · 普攻換武秒切換 | **【實機素材·REC-01】**<br>錄製自 Godot 實機 `res://scenes/battle/battle.tscn`。<br>展示已合併 main 的 `_ensure_thumb_hud()` 右手操作熱區。 |
| **Shot 3<br>【打擊換血】** | `7.5-15.5s`<br>(8.0s) | 小白正面交鋒守衛巨獸雷歐。畫面細節特寫：告別 16x16 粗像素方塊，呈現通透平滑插畫感。角色身上帶有深暖褐粗描邊（`outline.gdshader`），腳底踩著清晰貼地的獨立柔化橢圓軟影（`foot_shadow.gdshader`）。長劍斬中，觸發精確 0.15s 打擊停頓（Hitstop），爆出金色齒輪火花與微震反饋。 | 隨武器劈砍軌跡向左下微幅下搖（Pan Down），命中瞬間觸發 0.15s 畫面急停微震，緊接著火花爆散。特寫展現受擊停頓與流暢動作銜接。 | 沉重鈍擊與金屬切割交錯聲「鏘——轟！」，0.15s 命中停頓瞬間聲場短暫抽真空，隨後火花炸裂。 | 【全新打擊手感】<br>去像素插畫感 × 落地柔影 × 0.15s 停頓 | **【實機素材·REC-02】**<br>錄製自 Godot 實機 `res://scenes/battle/battle.tscn`（`setup("leo")` 或 `setup("road_bandit")`）。<br>展示已合併 main 的 `game/shaders/outline.gdshader`、`game/shaders/foot_shadow.gdshader` 與 `capture_battle_polish.gd`。 |
| **Shot 4<br>【封靈開光】** | `15.5-20.5s`<br>(5.0s) | 戰鬥火花化為聚魂殿金光。展示四大殿堂之「聚魂殿」。中央黃銅發條封靈罐（無任何系統 Emoji）震動進階，金光滿溢。鏡頭帶出畫面上方直觀透明的「首屏保底進度條」（60/100 虔誠度，4 碎片明確標示），點擊抽魂，橙罐爆裂開光！ | 鏡頭自全景向中央封靈罐平滑推入（Push In），光芒爆發時輕微拉遠展現完整 UI 介面。 | 發條罐劇烈上弦發條聲「嘸——咔啦啦」，金屬鎖扣彈開聲，開光爆發的清脆天籟鐘鳴「鐺——」。 | 【透明首屏保底】<br>發條封靈罐 · 告別隱形坑 | **【實機素材·REC-03】**<br>錄製自 Godot 實機 `res://scenes/main.tscn` 之 `_go_soul_panel()`。<br>展示已合併 main 的首屏保底進度條與封靈罐系統（無 Emoji 現代 UI）。 |
| **Shot 5<br>【過載狂斬】** | `20.5-27.0s`<br>(6.5s) | 能量注入，畫面急切回戰鬥現場！怒氣累積滿 100%，右下角 `ThumbSkill` / `PlayerRage` 爆散彩糖星芒。一指點下，小白安全閥掀開，蒸氣噴薄，啟動「齒輪過載（Overdrive）」，攻速暴增 25%！長劍化為漫天金屬金光，BOSS 部位瞬間承受連環重擊，打出金字「BREAK！」零件崩飛！ | 鏡頭拉近平視動態跟隨，刀光閃爍伴隨劇烈節奏微震，部位擊破時畫面短暫放射狀模糊（Radial Blur），展現高潮絕殺力度。 | 高壓蒸氣劇烈排氣「嘶——！」，發條超轉速蜂鳴，密集成串的金屬暴擊「乒乒乓乓！」，部位崩落的金屬碎裂聲。 | 【超轉速過載】<br>部位拆卸 · 一指逆轉戰局！ | **【實機素材·REC-04】**<br>錄製自 Godot 實機 `res://scenes/battle/battle.tscn`。<br>展示已合併 main 的怒氣暴怒覺醒（`trigger_fury_awakening`）與部位破壞跳字。 |
| **Shot 6<br>【點題收束】** | `27.0-30.0s`<br>(3.0s) | 漫天火花切純黑。純黑點題底板（`branding/title_plate.png`）中央顯現手繪繪本風主字標《發條之心》。下方標語：「給心上弦，重新出發。」右下角顯現小白黃銅發條鑰匙剪影。底部標註：「開發中畫面 · 官網搶先看」。 | 純黑底板微幅向前緩推 102%，字標金屬邊緣一道柔和暖金高光緩慢掃過。 | 一聲清脆悠長、餘音裊裊的單聲「喀嗒」。全片安靜收尾。 | 標題卡由後製無失真疊加 `branding/logo_cn.png`，不得由 AI 生成。<br>官網搶先看（連結在簡介） | **【固定資產·合成】**<br>使用官方固定品牌資產 `branding/logo_cn.png` 與 `title_plate.png`。<br>⚠️ 依第 15/16 條：不放下載鈕、不承諾上市日期、不提價格。 |

- **秒數累計核對**：`3.0 + 4.5 + 8.0 + 5.0 + 6.5 + 3.0 = 30.0 秒`（精準嚴絲合縫，共 6 鏡）。

---

## 五、Godot 實機素材錄影清單與操作序列（對齊已合併 main 功能）

> **審核鐵則（review.md 第 19 條與第 19b 條）**：  
> 所有標示「實機」之素材，**必須能在既有 Godot 引擎中重現與錄製，且功能 100% 已合併進 main**。嚴禁以 AI 主視覺充當實機，嚴禁列出「尚未實裝」的設計功能。

以下為本片所需之 4 支實機錄影片段規格與操作序列清單：

### 【實機素材 1：REC-01 右手拇指操作熱區 (ThumbPad HUD)】
- **對應分鏡**：Shot 2 (3.0s～7.5s)
- **所屬功能**：`mob-battle`（觸控優先戰鬥，main 合併 commit `0975523`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`（`_ensure_thumb_hud()`、`_install_touch_controls()`）
- **驗證測試依據**：`game/scripts/battle/test_battle_thumb.gd`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("road_bandit")`。
  2. 鏡頭聚焦右下角 `ThumbPad` 區域（包含 `ThumbAttack` 攻擊 88×72、`ThumbSwitch` 換武、`ThumbSkill` 技能、`ThumbLock` 鎖定）。
  3. 連續觸發 3 次 `ThumbAttack` 點擊事件，記錄小白單手持劍揮斬前進動作與怪物受擊反饋。
  4. 觸發 1 次 `ThumbSwitch` 點擊事件，展示武器欄由單手劍切換為備用武器（巨錘），UI 圖示即時更換。
  5. 觸發 1 次 `ThumbLock`，展示目標指示器在敵人與部位間循環切換。
- **預期畫面**：右側操作熱區緊湊明確、符合人體工學，無虛擬搖桿，單手點擊回饋流暢。

### 【實機素材 2：REC-02 視覺換血（粗描邊、落地軟影與 0.15s 打擊停頓）】
- **對應分鏡**：Shot 3 (7.5s～15.5s)
- **所屬功能**：`game-battle-polish`（戰鬥畫面優化，main 合併 commit `3a801b6`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應著色器與腳本**：
  - `game/shaders/outline.gdshader`（角色深色描邊，寬度 2.5px，色值 `#331F12`）
  - `game/shaders/foot_shadow.gdshader`（獨立 `ShadowLayer` 落地柔化橢圓軟影）
  - `game/scripts/dev/capture_battle_polish.gd`
- **錄製操作序列**：
  1. 執行 `res://scripts/dev/capture_battle_polish.gd`，載入 `setup("leo")` 雷歐守衛泰坦戰鬥。
  2. 保持線性平滑過濾（`texture_filter = 2`），確認無舊版 16×16 粗方塊像素量化濾鏡。
  3. 觀察小白（`PlayerBody`）與雷歐（`EnemyBody`）腳底下的 `FootShadow_PlayerBody` 與 `FootShadow_EnemyBody`，錄製其落地寬核、柔和衰減的半透明陰影。
  4. 觸發小白普通攻擊橫斬命中，捕捉 0.15s Hitstop 打擊停頓瞬間、受擊微幅震顫與金色傷害跳字爆散。
- **預期畫面**：插畫感立體角色、清晰接地陰影、扎實打擊節奏，與舊版粗顆粒畫面形成強烈對比。

### 【實機素材 3：REC-03 聚魂殿四階封靈罐開光與首屏透明保底】
- **對應分鏡**：Shot 4 (15.5s～20.5s)
- **所屬功能**：`soul-pity`（戰魂首屏保底進度條與封靈罐系統，main 合併 commit `0736a53`）
- **Godot 場景路徑**：`res://scenes/main.tscn`
- **對應腳本**：`game/scripts/systems/soul_system.gd`、`game/scripts/main.gd`（`_go_soul_panel()` 所在腳本）
- **參考現存截圖**：`screenshots/soul_panel_pity.png`
- **錄製操作序列（手動操作序列，無自動腳本）**：
  1. 啟動 `res://scenes/main.tscn`，注入測試狀態：`GameState.set_flag("soul.piety", 60)`，`GameState.set_flag("soul.shards", 4)`，金幣 1500。
  2. 點擊進入聚魂殿（或呼叫 `_go_soul_panel()`）。
  3. 展示乾淨純粹、去除所有系統 Emoji 的現代化手遊介面，展示綠、藍、紫、橙四階發條封靈罐（Spirit-Seal Jar）。
  4. 鏡頭特寫首屏上方進度條：清楚標明「虔誠度 60/100（每滿 100 轉化 1 碎片）· 稀世需 6 片 / 神魂需 15 片」，展示百分之百透明的保底機制。
  5. 點擊抽魂按鈕，錄製橙色封靈罐發條震動、金光迸裂並揭曉戰魂的動態效果。
- **預期畫面**：多巴胺發條機械儀式感、無 Emoji 專業 UI、進度條一目了然給予玩家心理安全感。

### 【實機素材 4：REC-04 怒氣滿額超轉速過載（Overdrive）與部位 BREAK】
- **對應分鏡**：Shot 5 (20.5s～27.0s)
- **所屬功能**：`mob-battle` 與 `balance-lock`（暴怒覺醒與部位破壞，main 合併 commit `985ba28`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`（`setup("leo")`）
- **對應腳本**：`game/scripts/battle/battle_view.gd`（`_on_rage_gui()`、`trigger_fury_awakening()`）
- **錄製操作序列**：
  1. 載入雷歐戰鬥，預充怒氣值至 100%（`player_rage.value = 100.0`）。
  2. 畫面中央上方 `_rage_ready` 提示浮現並高頻微爍。
  3. 點擊 `_rage_ready` 或右側 `ThumbSkill` 按鍵，觸發「暴怒覺醒 / 齒輪過載」。
  4. 捕捉小白背後發條超轉速狂飆動態、蒸氣排氣粒子爆散。
  5. 小白以 +25% 攻擊速度進行高速連斬，最後一記重擊打碎雷歐獅鬃裝甲，彈出金色「BREAK！」字樣與齒輪零件四散爆散。
- **預期畫面**：戰鬥高潮、多巴胺打擊反饋拉滿，機械裝甲部位崩解的視覺快感。

---

## 六、首幀（Shot 1）9:16 概念圖提示詞規格（對齊 ART_DIRECTION.md §6.5）

為確保本短影音在 Reels / Shorts / TikTok 動態牆第一幀（Cover / Hook）具備極致吸睛度，且在小螢幕縮圖下依然具備 30 公尺辨識度，首幀若需輔助產圖，必須**嚴格遵守 `ART_DIRECTION.md` §6.5 規格**：

### 提示詞（Prompt - 9:16 Vertical Composition）
```
A vertical 9:16 cinematic mobile RPG game opening frame for a charming mechanical toy fantasy advertisement.

Extreme close-up macro shot of a tiny ivory-white mechanical toy rabbit swordsman hero standing in the dim corner of an abandoned antique clockwork workshop. 

The rabbit is a 2.5-head-tall chibi mechanical toy automaton, constructed entirely from aged ivory painted metal panels and antique brass joints, with visible tiny screws, worn rivets, chipped enamel, subtle rust-red scratches and authentic workshop dust. Rigid upright metal rabbit ears with rust-red inner surfaces, large expressive cyan-green glass eyes with bright internal reflections. 

A prominent antique brass winding key is mounted on its upper back; the rabbit is angled at a sharp three-quarter rear perspective so the winding key clearly protrudes beyond its silhouette, catching a sharp rim light as it suddenly twists half a turn.

In its chest, an intricate circular clockwork core suddenly bursts into a powerful glowing cyan-green light, casting radiant volumetric rays through the dusty air and illuminating the single long single-handed mechanical sword gripped in its metal paw. The blade has subtle notches and glowing sparks along the edge.

Material: worn brass, chipped ivory metal, matte aged steel, handcrafted antique toy imperfections. Absolutely no plush fabric, no real fur, no biological rabbit parts.

Color palette: Nutcracker stage toy palette — deep navy shadows, rich burgundy and warm antique brass, contrasted against brilliant cyan-green glowing core and golden spark reflections.

Lighting: dramatic warm theatrical rim light, high-contrast chiaroscuro, volumetric dust rays, radiant cyan-green illumination from the chest core.

Camera: vertical 9:16 framing, 35mm lens equivalent, low-angle macro perspective, dynamic depth of field with background wooden blocks and antique brass cogs softly blurred. Strong character silhouette readable in one second on a mobile phone screen.

Style keywords: premium stylized 3D game art, handcrafted mechanical toy fantasy, whimsical steampunk fairy tale, Nutcracker-inspired toy theater, high visual readability, mobile-first design.

NEGATIVE PROMPT:
plush rabbit, furry animal, real fur, stuffed toy, biological rabbit, humanoid robot, military mech, giant robot, futuristic cyborg, Iron Man, smooth glossy plastic, mirror chrome, horror, creepy doll, porcelain doll, scary eyes, blank eyes, floppy ears, multiple swords, dual wielding, extra limbs, extra fingers, text, logo, watermark, UI overlay, 16:9 landscape.
```

---

## 七、總監審核清單逐項對照（對齊 review.md）

本份腳本已完成自我審查，逐條符合 `references/review.md` 之所有紅線與標準：

| 檢查項目 | 審查標準 | 本腳本具體落實措施 | 判定 |
|---|---|---|---|
| **第 10 條** | **畫面真的在動** | 拒絕靜圖幻燈片。每鏡均標明實體運鏡（微距推軌、平視橫移、打擊震顫、開光推拉、過載連斬）；Shot 1 亦要求發條鑰匙動態旋轉與核心爆光。 | ✅ 合格 |
| **第 11 條** | **開場三秒給懸念，不給 Logo** | Shot 1（0.0～3.0s）為發條兔背後鑰匙旋轉與核心充能微距特寫，純實體音效，畫面零文字、無 Logo、無遊戲名。 | ✅ 合格 |
| **第 12 條** | **鏡次接得上** | 嚴格維持接鏡動態軸線：微距光芒穿透 → 實機指尖操作 → 揮斬震顫打擊 → 開光爆發展示保底 → 終極過載連斬 → 點題收束。 | ✅ 合格 |
| **第 13 條** | **標「不移動」的鏡次真的不走** | Shot 1 標明小白原位靜止（僅鑰匙旋轉與核心充能），Shot 6 標明純黑定格微推，無任意漫步。 | ✅ 合格 |
| **第 14 條** | **實體音優先，拒絕罐頭史詩配樂** | 全片音效皆為實體採樣：發條咬合、齒輪旋轉、金屬斬擊、蒸氣洩壓、天籟鐘鳴，禁止任何罐頭交響樂填塞。 | ✅ 合格 |
| **第 15 條** | **嚴禁承諾上架日、價格、合作** | 片尾僅呈現「開發中畫面 · 官網搶先看」，禁止提及任何上架時間、收費定價或下載按鈕。 | ✅ 合格 |
| **第 16 條** | **不暗示已完成，不拿 AI 圖充當實機** | 概念鏡次（Shot 1）與合成鏡次（Shot 6）明確標示為概念與品牌字標；實機鏡次（Shot 2～5）100% 來自真實 Godot 錄影。 | ✅ 合格 |
| **第 17 條** | **切入點獨立，風格不撞車** | 本片切入點為純粹的「戰鬥打擊手感與聚魂保底爽感」，與劇情向短影音腳本 `docs/marketing/STORYBOARD_C0_30S.md`、品牌概念片腳本 `docs/marketing/STORYBOARD_AWAKENING.md` 之調性與賣點截然不同。 | ✅ 合格 |
| **第 19 條** | **素材列出必須是已存在之合併功能** | 所列 4 項實機素材（REC-01 至 REC-04）皆對應 main 上已合併之真實功能與 commit（`0975523`、`3a801b6`、`0736a53`、`985ba28`），已完全剔除尚未實裝之四大核心圖鑑。 | ✅ 合格 |
| **第 19b 條** | **標實機的必須真的是 Godot 錄影** | 實機清單所有檔案與腳本逐項查證無訛：已 ls 確認 `game/scenes/battle/battle.tscn`、`game/scenes/main.tscn`、`game/shaders/outline.gdshader`、`game/shaders/foot_shadow.gdshader`、`game/scripts/battle/battle_view.gd`、`game/scripts/battle/test_battle_thumb.gd`、`game/scripts/dev/capture_battle_polish.gd`、`game/scripts/main.gd`（`_go_soul_panel()` 所在處）、`game/scripts/systems/soul_system.gd` 及 `screenshots/soul_panel_pity.png` 均存在；已 git branch --contains 確認 4 個 commit（`0975523`、`3a801b6`、`0736a53`、`985ba28`）皆在 main；REC-03 註明手動操作序列。 | ✅ 合格 |
| **第 19c 條** | **不得自立片名與分歧點題** | 移除自立片名欄位，統一為內部代號 `mk-shorts`（片內不呈現）；Shot 6 點題卡標明由後製無失真疊加官方字標 `branding/logo_cn.png`，不得由 AI 生成。 | ✅ 合格 |
| **第 22 條** | **不違背 CANON 世界憲章** | 嚴格遵守「覺醒的金屬發條玩具」世界觀：零毛皮、背後鑰匙、胡桃鉗色盤、齒輪部位破壞無血肉、舊 IP 詞彙全面掃蕩。 | ✅ 合格 |
| **第 23 條** | **名詞六語系皆可翻譯** | 涉及之核心名詞如封靈罐（Spirit-Seal Jar）、虔誠度（Piety）、暴怒覺醒（Fury Awakening）等皆在五／六語系本地化字典內。 | ✅ 合格 |

---

## 八、下一步實作指引（下一輪派工，本輪不做）

1. **實機素材錄製（sideworker）**：依據本清單第五節之 REC-01 至 REC-04 操作序列，使用 `/root/gameplay_capture.sh` 或 Godot 實機測試環境錄製 4 段乾淨的無壓縮 60fps 畫面片段。
2. **首幀素材生成（需經確認）**：依據第六節 9:16 提示詞使用 `gen_media.py` 產出 Shot 1 封面圖（需帶 `--ref branding/key_visual_main.png`）。
3. **剪接合成**：使用 ffmpeg 依據第四節時間軸（30.0s，6 鏡）進行接鏡與實體音效混音，產出最終 1080×1920 直式短影音。
