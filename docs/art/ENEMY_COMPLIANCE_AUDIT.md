# 《發條之心》全敵人／Boss 立繪零毛皮合規性盤點總報告（含主線六域首領與秘境小Boss）

> **審查日期**：2026-09-15  
> **執行者**：側案·美術總監 小柔 (@sideart)  
> **依據標準**：  
> - 世界觀憲章 `docs/world/CANON.md` 第五章「所有敵人本質上也都是玩具」、零毛皮禁令、金屬板件與發條鑰匙核心規範  
> - 審核準則 `references/review.md` 第 19g-10 條收緊審查法（頭部區域放大裁切＋三項封閉問題自檢）與第 0c-28 條（前後辨識度與標誌特徵保留）  
> - 任務編號：  
>   - 秘境小Boss／雜魚：`t_6f331585`（初始盤點）、`t_63073ba4`（重繪批次1）、`t_b51e9456`（重繪批次2）、`t_0d32007c`（重繪批次3：11位全數合規）  
>   - 主線首領：`t_2e6dee93`（雷歐改造合規）、`t_1402bdfb`（主線六域首領合規性專案盤點）  

---

## 1. 審查方法與三項封閉問題門檻

依據 `review.md` 第 19g-10 條規範，所有敵人立繪全面杜絕全圖遠看誤判（避免全身鎧甲掩蓋內部有機毛皮或血肉），逐一將敵人立繪頭部／上半身特寫放大檢驗，強制回答以下三項封閉問題：

1. **① 有沒有毛髮質感的鬃毛／絨毛／羽毛？**
   - **合格標準**：必須為「**無**」。若有有機毛髮、絨毛、羽毛、動物鬍鬚、毛皮滾邊皆判定違規。
2. **② 有沒有生物皮膚（腮紅／毛孔／肉色／肉質器官）？**
   - **合格標準**：必須為「**無**」。若有肉色皮膚、粉色腮紅、哺乳動物豬鼻、肉質耳道、血肉器官皆判定違規。
3. **③ 頭部或背後有沒有發條鑰匙與螺栓／接縫？**
   - **合格標準**：必須為「**有**」。必須清楚具備世界觀核心視覺符號——發條鑰匙（winding key）、外露螺栓、鉚釘或玩具金屬板件分片接縫。

**判定門檻**：三題必須全部合規（①無 ②無 ③有）才可判定為「**合格**」；任何一題不符即判定為「**不合格**」。  
**0c-28 條原則**：盤點與後續重繪規劃時，必須嚴格記錄敵人之核心戰鬥辨識度（剪影、標誌性武器、配色特徵），重繪為發條玩具時必須保留識別度，禁止抹殺角色辨識特徵。

---

## 2. 審查結果總表

### 【A. 七位主線區域首領 (C0～C6 Main Bosses) 盤點】

| 編號 | 關卡區域 | 首領代號 | 首領名稱 | 資源原圖路徑 | 審查截圖依據 (Panel) | ①毛髮/羽毛 | ②生物皮膚/腮紅 | ③發條鑰匙/螺栓 | 綜合判定 | 狀態說明 |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| M0 | C0 荒路 | `wolf` | 渣滓之狼 | `game/assets/sprites/bosses/wolf.png` | `proofs/enemy_audit/wolf_audit_panel.png` | **有** (違規) | **有** (違規) | **無** (違規) | ❌ **不合格** | 生物灰狼毛皮、粉紅肉質耳道與腮紅，無發條鑰匙 |
| M1 | C1 王庭 | `leo` | 守衛泰坦·雷歐 | `game/assets/sprites/bosses/leo.png` | `proofs/leo_verify_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** | `t_2e6dee93` 完成金屬化改造，具備黃銅雙環發條鑰匙與面甲螺栓 |
| M2 | C2 霧村 | `fog` | 白霧 | `game/assets/sprites/bosses/fog.png` | `proofs/enemy_audit/fog_audit_panel.png` | **有** (違規) | **有** (違規) | **無** (違規) | ❌ **不合格** | 生物白狐毛髮、肉質內耳、巨大蓬鬆狐尾，無發條鑰匙 |
| M3 | C3 道場 | `abo` | 阿波 | `game/assets/sprites/bosses/abo.png` | `proofs/enemy_audit/abo_audit_panel.png` | **有** (違規) | **有** (違規) | **無** (違規) | ❌ **不合格** | 生物大貓熊毛皮、粉紅腮紅與肉鼻，無發條鑰匙 |
| M4 | C4 森林 | `falcon` | 疾影 | `game/assets/sprites/bosses/falcon.png` | `proofs/enemy_audit/falcon_audit_panel.png` | **有** (違規) | **有** (違規) | **無** (違規) | ❌ **不合格** | 生物鳥羽、粉紅腮紅、有機鳥喙，無發條鑰匙 |
| M5 | C5 海岸 | `boar` | 石拳 | `game/assets/sprites/bosses/boar.png` | `proofs/enemy_audit/boar_audit_panel.png` | **有** (違規) | **有** (違規) | **無** (違規) | ❌ **不合格** | 生物野豬剛毛、頸部獸皮毛領、肉質粉紅豬鼻，無發條鑰匙 |
| M6 | C6 高塔 | `demon` | 停擺核 | `game/assets/sprites/bosses/demon.png` | `proofs/enemy_audit/demon_audit_panel.png` | **無** (合格) | **有** (違規) | **無** (違規) | ❌ **不合格** | 紫色生物魔族皮膚、蝙蝠肉翼、有機惡魔角，無發條鑰匙 |

> **主線首領盤點統計**：
> - 審查總數：7
> - **合格**：**1** 位（`leo` 雷歐，已改造）
> - **不合格**：**6** 位（`wolf`、`fog`、`abo`、`falcon`、`boar`、`demon`，不合格率高達 **85.7%**！）

---

### 【B. 十一位秘境小 Boss／雜魚 (Secret Bosses & Creeps) 盤點】

| 編號 | 敵人代號 | 敵人名稱 | 資源原圖路徑 | 審查截圖依據 (Panel) | ①毛髮質感 | ②生物皮膚 | ③發條鑰匙/螺栓 | 綜合判定 |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| 01 | `ash_rat` | 灰燼鼠 | `game/assets/sprites/bosses/ash_rat.png` | `proofs/enemy_audit/ash_rat_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 02 | `bamboo_spirit` | 竹靈 | `game/assets/sprites/bosses/bamboo_spirit.png` | `proofs/enemy_audit/bamboo_spirit_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_b51e9456 重繪) |
| 03 | `coast_raider` | 海岸掠奪者 | `game/assets/sprites/bosses/coast_raider.png` | `proofs/enemy_audit/coast_raider_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 04 | `fog_shade` | 迷霧暗影 | `game/assets/sprites/bosses/fog_shade.png` | `proofs/enemy_audit/fog_shade_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 05 | `forest_sprite` | 森林精靈 | `game/assets/sprites/bosses/forest_sprite.png` | `proofs/enemy_audit/forest_sprite_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_b51e9456 重繪) |
| 06 | `mirror_wraith` | 鏡中幽靈 | `game/assets/sprites/bosses/mirror_wraith.png` | `proofs/enemy_audit/mirror_wraith_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_b51e9456 重繪) |
| 07 | `road_bandit` | 荒路匪徒 | `game/assets/sprites/bosses/road_bandit.png` | `proofs/enemy_audit/road_bandit_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_f1fcef58 重繪) |
| 08 | `scar_lord` | 黑焰領主 | `game/assets/sprites/bosses/scar_lord.png` | `proofs/enemy_audit/scar_lord_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_0d32007c 重繪) |
| 09 | `scar_wisp` | 黑焰幽火 | `game/assets/sprites/bosses/scar_wisp.png` | `proofs/enemy_audit/scar_wisp_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_0d32007c 重繪) |
| 10 | `sewer_slime` | 下水道史萊姆 | `game/assets/sprites/bosses/sewer_slime.png` | `proofs/enemy_audit/sewer_slime_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_0d32007c 重繪) |
| 11 | `wreck_captain` | 沉船船長 | `game/assets/sprites/bosses/wreck_captain.png` | `proofs/enemy_audit/wreck_captain_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_0d32007c 重繪) |

> **全體敵人／Boss 匯總統計 (18 隻)**：
> - 審查總數：18
> - **合格**：**12** 位（秘境小Boss 11 位 ＋ 主線雷歐 1 位，已 100% 重繪合規）
> - **不合格**：**6** 位（主線六域首領 wolf、fog、abo、falcon、boar、demon，尚待排期重繪）

---

## 3. 逐項詳細審查紀錄

### 【第一部分：六位主線首領專案審查紀錄與 0c-28 規劃】

#### M0. 渣滓之狼 (wolf) · C0 荒野荒路
- **原始資產**：`game/assets/sprites/bosses/wolf.png` (193×232 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/wolf_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/wolf_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/wolf_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。頰側帶鋸齒毛簇、尖耳內外覆蓋毛髮、頸部毛茸、尾巴為蓬鬆狼尾，純有機生物毛皮。
  - ② 生物皮膚：**有**。耳道內為肉色／粉紅生物肉質皮膚，雙頰有明顯粉紅腮紅斑。
  - ③ 發條鑰匙與螺栓：**無**。全身完全無發條鑰匙、無機械螺栓、無玩具金屬板件分模接縫。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：灰白相間狼族戰鬥剪影、堅定敏銳眼神、四足站立之戰鬥警戒姿態。
  - **合規改造方向**：改為「失控的鐵皮發條狼玩具（Clockwork Tin Wolf）」，外殼為沖壓暗鐵與鍍鋅馬口鐵板件，四肢採用金屬球形鉸鏈關節，耳部改為沖壓鐵片耳，背部配備巨大雙環黃銅發條鑰匙，尾巴改為分節金屬彈簧鋼尾，雙眼改為發光琥珀黃光學透鏡。

---

#### M2. 白霧 (fog) · C2 迷霧之村
- **原始資產**：`game/assets/sprites/bosses/fog.png` (216×198 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/fog_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/fog_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/fog_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。頭頂為白狐有機毛髮、面頰帶毛茸、背後展開數條巨大蓬鬆之九尾狐有機毛皮尾巴。
  - ② 生物皮膚：**有**。耳道內側為粉紅／鮭肉色生物皮膚。
  - ③ 發條鑰匙與螺栓：**無**。全身無任何發條鑰匙、無機械螺栓，身著傳統布質白忍服與布質面罩。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：雙持苦無匕首、忍者面罩潛行刺客身姿、白紫雙色調、多尾扇形展開之視覺張力。
  - **合規改造方向**：改為「機巧白狐傀儡忍者（Clockwork Kitsune Automaton）」，頭部採用白瓷烤漆狐面機巧面甲，尾巴改為鏤空黃銅齒輪與半透明導光白鐵薄片構造（或蒸氣噴霧排氣分節結構），背部軸心突出巴洛克黃銅發條鑰匙，關節為漆黑球形機械關節。

---

#### M3. 阿波 (abo) · C3 竹林道場
- **原始資產**：`game/assets/sprites/bosses/abo.png` (209×240 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/abo_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/abo_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/abo_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。圓耳、頭部、四肢皆為大熊貓黑白有機毛皮，爪子為生物肉掌。
  - ② 生物皮膚：**有**。眼眶下方有兩團鮮豔粉紅珊瑚色腮紅，鼻頭為肉質黑鼻。
  - ③ 發條鑰匙與螺栓：**無**。全身無發條鑰匙、無金屬螺栓，身著刺繡金龍紅綾漢服與翡翠玉珠念珠。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：經典國術武僧架式（白鶴亮翅/虎爪格鬥姿態）、鮮紅武術袍、金刺繡龍紋、綠翡翠玉珠項圈、黑金利爪臂鎧。
  - **合規改造方向**：改為「漆器機巧熊貓武僧（Lacquer Karakuri Panda Master）」，面部與肢體改為黑白雙色亮面生漆人偶板件，臉頰帶玩具分模接縫，耳朵改為鉚釘固定黑漆金屬圓盤，背部外露大型太極八卦造型黃銅發條鑰匙，關節處設有精密黃銅咬合齒輪與軸承。

---

#### M4. 疾影 (falcon) · C4 永夜森林
- **原始資產**：`game/assets/sprites/bosses/falcon.png` (220×173 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/falcon_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/falcon_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/falcon_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。頭部覆蓋紫白雙色有機鳥羽、兩側展開巨大之紫色真羽翅膀。
  - ② 生物皮膚：**有**。雙頰明顯帶有粉紅腮紅、眼睛為生物靈動眼珠、鳥喙為角質有機器官。
  - ③ 發條鑰匙與螺栓：**無**。全身無發條鑰匙、無機械螺栓，身穿青銅鱗甲胸甲與戰術單眼瞄準鏡。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：紫金綠三色羽翼射手剪影、戰術單眼瞄準鏡、金屬鱗甲胸盾、獵鷹銳利神態。
  - **合規改造方向**：改為「發條天隼狙擊機偶（Clockwork Sky Falcon Automaton）」，羽翼改為沖壓黃銅與紫晶金屬排片（薄片刀刃翼），臉部改為精細鳥首金屬面甲，鳥喙為拋光黃銅機械啄，單眼瞄準鏡改為帶黃銅齒輪微調環之光學透鏡，背部軸心外露螺旋推進黃銅發條鑰匙。

---

#### M5. 石拳 (boar) · C5 殘破海岸
- **原始資產**：`game/assets/sprites/bosses/boar.png` (220×225 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/boar_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/boar_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/boar_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。臉部與下顎覆蓋粗糙暗褐野豬剛毛，肩部披掛蓬鬆厚重乳白色動物獸皮毛領披肩。
  - ② 生物皮膚：**有**。正中央為巨大肉質粉紅野豬豬鼻（帶鼻孔與皮褶）、血盆獠牙、生物兇狠紅眼。
  - ③ 發條鑰匙與螺栓：**有螺栓但無發條鑰匙**。頭戴維京鉚釘鐵盔，但全身無任何發條鑰匙，本質仍是生物野豬戰士。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：雙角維京鐵盔、符文巨斧、野豬衝撞狂暴體型、厚實鋼鐵護甲與獠牙。
  - **合規改造方向**：改為「鑄鐵發條維京野豬機偶（Cast-Iron Viking Boar Automaton）」，全身改為厚重生鐵鑄鐵板件與暗鋼鉚釘，豬鼻改為金屬排氣活塞閥門，毛領披肩替換為鍛造鏈甲披肩或齒輪箱護頸，獠牙改為拋光合金衝壓角，背部配備重型大型十字齒輪黃銅發條鑰匙。

---

#### M6. 停擺核 (demon) · C6 停擺高塔
- **原始資產**：`game/assets/sprites/bosses/demon.png` (219×204 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/demon_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/demon_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/demon_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。臉部為光滑紫色生物皮膚。
  - ② 生物皮膚：**有**。紫色生物魔族肉色皮膚、五官肉質嘴角、粉紅鼻點/腮紅、背後為生物蝙蝠肉膜翼、頭側為有機骨質惡魔角。
  - ③ 發條鑰匙與螺栓：**無**。身穿哥德奇幻王冠魔甲，完全無機械螺栓、無金屬分模接縫、無發條鑰匙。
- **判定結果**：❌ **不合格**
- **0c-28 前後辨識度保留與重繪建議**：
  - **核心特徵保留**：停擺核心巨劍、紫黑哥德魔王重鎧、頭頂華麗紫晶王冠、雙角魔王霸氣剪影。
  - **合規改造方向**：改為「高塔停擺核心機偶·魔王玩具（Stasis Core Sovereign Puppet）」，面部改為暗鐵沖壓無面魔甲配猩紅發光視縫透鏡，蝙蝠肉翼改為分節黑曜金屬刀鋒翼，胸口外露巨大的停擺齒輪鐘錶心臟，背部軸心裝配巨大無比的懸浮鐘錶王冠發條鑰匙，全身關節以粗重機械螺栓與液壓鉸鏈接合。

---

### 【第二部分：十一位秘境小Boss／雜魚詳細審查紀錄】


### 01. 灰燼鼠 (ash_rat)
- **原始資產**：`game/assets/sprites/bosses/ash_rat.png` (270×200 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/ash_rat_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/ash_rat_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/ash_rat_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/ash_rat_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。全身改為上漆白鐵皮與暗灰鐵板件，四肢為球形機械關節與鉸鏈，鼠尾為分節鋼製彈簧金屬尾，完全零毛皮、零絨毛、零鬍鬚。
  - ② 生物皮膚：**無**。臉部為鉚釘沖壓金屬面甲與螺栓下顎，雙耳為帶固定螺絲之沖壓金屬薄片（無粉色內耳生物肉色），雙眼為圓形發光琥珀橙透鏡，零腮紅、零生物皮膚。
  - ③ 發條鑰匙與螺栓：**有**。**背部清晰可見巨大黃銅雙環發條鑰匙**，頭部、面甲、下顎與身體板件皆有外露螺栓與分片接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_63073ba4` 成功重繪為發條金屬玩具老鼠，100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 02. 竹靈 (bamboo_spirit)
- **原始資產**：`game/assets/sprites/bosses/bamboo_spirit.png` (240×300 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/bamboo_spirit_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/bamboo_spirit_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/bamboo_spirit_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/bamboo_spirit_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。全身改為漆綠竹筒外殼與拋光黃銅板件，無任何有機動物毛髮或鬃毛。
  - ② 生物皮膚：**無**。臉部為精細雕刻之原木機巧面甲，雙眼為青藍色發光圓形透鏡，額頭與胸口鑲嵌鉚釘白鐵片與齒輪能量核心，完全零血肉、零生物皮膚、零腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**背部外露巨大齒輪齒緣之黃銅發條鑰匙**，四肢採用金屬球形關節與鉸鏈，竹杖兩側裝配黃銅齒輪環，全身關節具備清晰金屬螺栓與機械接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_b51e9456` 成功重繪為竹製發條機巧人偶（Karakuri Toy Automaton），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 03. 海岸掠奪者 (coast_raider)
- **原始資產**：`game/assets/sprites/bosses/coast_raider.png` (270×320 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/coast_raider_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/coast_raider_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/coast_raider_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/coast_raider_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。大鬍鬚完全改為分片重疊的紅銅／黃銅金屬排片（胡桃鉗玩具風格），盔甲邊緣去除所有毛皮飾邊，完全無有機毛髮與毛皮。
  - ② 生物皮膚：**無**。頭部為金屬鉚接牛角鐵盔，面甲為金屬沖壓件，雙眼為圓形發光琥珀黃光學透鏡，全身為鋼鐵與黃銅板件，零人類肉色皮膚、零血肉五官。
  - ③ 發條鑰匙與螺栓：**有**。**右肩背後外露大型黃銅發條鑰匙（雙環透空結構清晰）**，頭盔、胸甲、腰帶、肩部與四肢均有清晰可見之球形機械關節、十字螺栓與鉚釘。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_63073ba4` 成功重繪為發條錫兵海盜玩具，100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 04. 迷霧暗影 (fog_shade)
- **原始資產**：`game/assets/sprites/bosses/fog_shade.png` (240×310 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/fog_shade_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/fog_shade_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/fog_shade_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/fog_shade_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。全身為深鐵色金屬斗篷罩殼與黃銅邊框，完全無毛髮或毛皮。
  - ② 生物皮膚：**無**。頭戴鍛鐵金屬兜帽，面部為黃銅通風格柵面罩，內部配備兩顆圓形發光琥珀透鏡，胸腔外露機械齒輪箱與排氣管，下身由分節金屬甲片與排氣噴嘴噴出青藍玩具霧氣構成，零生物皮膚、零血肉。
  - ③ 發條鑰匙與螺栓：**有**。**左肩背後外露大型雙環黃銅發條鑰匙（鏤空雙環清晰可見）**，兜帽周圍、胸甲與腰部皆具備凸起之黃銅鉚釘與機械接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_63073ba4` 成功重繪為發條蒸氣噴霧機偶玩具，100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 05. 森林精靈 (forest_sprite)
- **原始資產**：`game/assets/sprites/bosses/forest_sprite.png` (220×320 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/forest_sprite_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/forest_sprite_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/forest_sprite_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/forest_sprite_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。髮型改為分片沖壓金屬綠葉板件（葉脈帶微型固定螺栓與鉚釘），頂部為金屬葉梗，完全零有機髮絲與毛茸。
  - ② 生物皮膚：**無**。全臉改為光滑純白瓷面金屬烤漆人偶面甲，雙頰無任何腮紅，雙眼為銀白金屬透鏡，臉頰帶玩具分模接縫線，四肢均為純白瓷漆球形關節肢體，零生物皮膚。
  - ③ 發條鑰匙與螺栓：**有**。**背部右側突出明顯雙環巴洛克雕花黃銅發條鑰匙**，背後翅膀為鏤空黃銅齒輪薄片翅膀，腰部設有黃銅鉸鏈皮帶，葉片洋裝皆有金屬固定鉚釘與接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_b51e9456` 成功重繪為八音盒發條芭蕾精靈公仔（Music Box Fairy Figurine），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 06. 鏡中幽靈 (mirror_wraith)
- **原始資產**：`game/assets/sprites/bosses/mirror_wraith.png` (270×300 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/mirror_wraith_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/mirror_wraith_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/mirror_wraith_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/mirror_wraith_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。傀儡頭部為紫靛色金屬螺栓頭殼，鏡面本體為水銀漩渦，無任何有機毛髮。
  - ② 生物皮膚：**無**。面部為純白瓷質威尼斯面具，雙眼為青藍色發光透鏡，身軀為紫靛色琺瑯漆金屬胸甲，四肢為金屬球形關節與黃銅機械手，零生物皮膚、零腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**鏡框右側齒輪傳動箱外露巨大雙環黃銅發條鑰匙**，鏡框頂部與邊緣密布咬合金屬齒輪，古董金屬底座帶有機械獸爪腳座與螺栓接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_b51e9456` 成功重繪為發條魔鏡機偶（Clockwork Magic Mirror Automaton），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 07. 荒路匪徒 (road_bandit)
- **原始資產**：`game/assets/sprites/bosses/road_bandit.png` (270×320 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/road_bandit_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/road_bandit_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/road_bandit_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/road_bandit_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。頭部已改為球形金屬金屬頭，無任何鬍渣或有機毛髮。
  - ② 生物皮膚：**無**。全金屬與磨損鐵皮材質，雙眼為青藍發光鏡片，無肉色皮膚與腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**背後有巨大清晰的黃銅發條鑰匙**，頭殼兩側、下顎與胸甲皆有清楚的十字固定螺栓與分片金屬接縫，盾牌已改為鉚釘鐵皮盾。
- **判定結果**：✅ **合格**
- **說明**：本資產已於任務 `t_f1fcef58` 重新繪製完成並合入 main，100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 08. 黑焰領主 (scar_lord)
- **原始資產**：`game/assets/sprites/bosses/scar_lord.png` (280×260 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/scar_lord_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/scar_lord_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/scar_lord_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/scar_lord_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。全身為暗黑曜鐵板件與紫晶能量導管，無任何毛髮、鬃毛或毛皮。
  - ② 生物皮膚：**無**。頭部為暗鐵封閉騎士頭盔配備琥珀黃發光透鏡視縫，胸前鑲嵌紫水晶齒輪動力核心，雙手持握雙鋸齒符文黑鐵刃，四肢為金屬球形關節，零生物皮膚、零腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**背部正中央外露巨大黃銅齒輪發條鑰匙**，肩甲、胸甲與耳軸皆具備分明的外露十字螺栓、鉚釘與板件接縫。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_0d32007c` 成功重繪為發條黑鐵領主機偶（Clockwork Dark Knight Automaton），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 09. 黑焰幽火 (scar_wisp)
- **原始資產**：`game/assets/sprites/bosses/scar_wisp.png` (140×220 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/scar_wisp_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/scar_wisp_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/scar_wisp_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/scar_wisp_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。主體為古董黃銅金屬燈籠罩框、透明玻璃罩與內藏紫火，無毛皮毛髮。
  - ② 生物皮膚：**無**。前框鑲嵌三顆青藍發光透鏡眼，下方垂吊兩副黃銅多關節機械爪，零肉色皮膚、零腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**燈籠圓頂頂部外露大型雙環黃銅發條鑰匙**，金屬外框、頂蓋與底座均有清晰的固定螺絲與金屬托架。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_0d32007c` 成功重繪為發條幽火燈籠機偶（Clockwork Lantern Wisp Toy），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 10. 下水道史萊姆 (sewer_slime)
- **原始資產**：`game/assets/sprites/bosses/sewer_slime.png` (180×180 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/sewer_slime_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/sewer_slime_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/sewer_slime_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/sewer_slime_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。半透明薄荷綠橡膠果凍玩具材質，無任何有機毛髮。
  - ② 生物皮膚：**無**。雙眼為深鐵色十字螺絲釘扣眼，側邊帶有注塑分模線，透明膠體內包裹黃銅咬合齒輪機芯，零生物皮膚、零腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**頂部右上外露巨大黃銅雙環發條鑰匙**，直接插入體內與內部齒輪機芯相連，雙眼即為十字固定螺栓。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_0d32007c` 成功重繪為發條橡膠齒輪史萊姆玩具（Clockwork Toy Slime），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 11. 沉船船長 (wreck_captain)
- **原始資產**：`game/assets/sprites/bosses/wreck_captain.png` (240×260 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/wreck_captain_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/wreck_captain_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/wreck_captain_audit_panel.png`
  - 重繪前後對比：`proofs/enemy_audit/wreck_captain_compare.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。海盜帽為風化木板與金屬包邊（金屬船舵帽徽），完全去除有機羽毛與鬍鬚。
  - ② 生物皮膚：**無**。臉部為雕刻風化木紋人偶面甲與機械接縫分模線，左眼為鉚釘金屬眼罩、右眼為青藍透鏡眼，身軀為鉚接木板與海軍藍大衣，右腿為木製假腿、左腿為木靴，四肢為金屬合頁與球形關節，零人類血肉皮膚。
  - ③ 發條鑰匙與螺栓：**有**。**背部軸心外露巨大的生鏽黃銅船舵造型發條鑰匙**，頭部、耳軸、胸甲與肢體密布外露螺栓與固定鉚釘。
- **判定結果**：✅ **合格**
- **說明**：已於任務 `t_0d32007c` 成功重繪為沉船木偶發條海盜水手（Wreckage Pirate Puppet Automaton），100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

---

## 4. 行銷團隊素材選用指引（嚴防 19g-10 事故再次發生）

為避免行銷宣傳、FB 排程、短影音與商店截圖再次踩中 `review.md 19g-10` 條款而遭全面退單，即日起行銷團隊選用敵人素材時，**一律嚴格遵守以下白名單與黑名單**：

### 🟢 允許對外發佈之合規敵人白名單 (Whitelist - 共 12 位已合規)
1. **守衛泰坦·雷歐 (`leo`)**：已於 `t_2e6dee93` 完成發條機械化改造，具備放射金屬鬃毛、螺栓面甲與黃銅發條鑰匙。
2. **荒路匪徒 (`road_bandit`)**：已於 `t_f1fcef58` 完成重繪，具備金屬球形頭部、鐵皮胸甲與背部發條鑰匙。
3. **灰燼鼠 (`ash_rat`)**：已於 `t_63073ba4` 完成重繪，具備上漆白鐵皮與暗灰鐵板件、彈簧金屬尾與背部黃銅發條鑰匙。
4. **海岸掠奪者 (`coast_raider`)**：已於 `t_63073ba4` 完成重繪，具備牛角鐵盔、銅片玩具鬍、球形關節與背部黃銅發條鑰匙。
5. **迷霧暗影 (`fog_shade`)**：已於 `t_63073ba4` 完成重繪，具備鍛鐵兜帽、齒輪胸腔、格柵面甲與背部黃銅發條鑰匙。
6. **竹靈 (`bamboo_spirit`)**：已於 `t_b51e9456` 完成重繪，具備原木機巧面甲、拋光黃銅齒輪杖與背部黃銅齒輪發條鑰匙。
7. **森林精靈 (`forest_sprite`)**：已於 `t_b51e9456` 完成重繪，具備純白瓷面面甲、沖壓金屬綠葉髮型與背部雙環黃銅發條鑰匙。
8. **鏡中幽靈 (`mirror_wraith`)**：已於 `t_b51e9456` 完成重繪，具備威尼斯白瓷面具、紫靛金屬胸甲與鏡框側邊巨大黃銅發條鑰匙。
9. **黑焰領主 (`scar_lord`)**：已於 `t_0d32007c` 完成重繪，具備黑曜暗鐵板件、紫晶齒輪胸芯、雙鋸齒符文刃與背部黃銅發條鑰匙。
10. **黑焰幽火 (`scar_wisp`)**：已於 `t_0d32007c` 完成重繪，具備黃銅六角燈籠骨架、紫晶齒輪幽火、金屬機械爪與頂部黃銅發條鑰匙。
11. **下水道史萊姆 (`sewer_slime`)**：已於 `t_0d32007c` 完成重繪，具備半透明薄荷綠果凍體、體內咬合黃銅齒輪機芯、十字螺絲雙眼與頂部黃銅發條鑰匙。
12. **沉船船長 (`wreck_captain`)**：已於 `t_0d32007c` 完成重繪，具備風化木板拼裝身軀、金屬船舵帽徽、球形合頁關節與背部巨大黃銅船舵發條鑰匙。

---

### 🔴 嚴格禁止對外發佈之未合規黑名單 (Blacklist - 共 6 位主線首領)
⚠️ **重大警告：以下 6 位主線區域首領為目前遊戲中嚴重違反 CANON「敵人也是玩具」與零毛皮憲章之資產，行銷與社群團隊嚴禁在任何對外文案、影片、截圖中使用以下角色：**
1. ❌ **渣滓之狼 (`wolf`)**：C0 荒野荒路首領。有機狼毛皮、粉紅肉質耳道與腮紅，無發條鑰匙。
2. ❌ **白霧 (`fog`)**：C2 迷霧之村首領。有機白狐毛皮、肉質內耳、巨大狐尾，無發條鑰匙。
3. ❌ **阿波 (`abo`)**：C3 竹林道場首領。有機大熊貓毛皮、粉紅腮紅與肉鼻，無發條鑰匙。
4. ❌ **疾影 (`falcon`)**：C4 永夜森林首領。有機鳥羽翅膀、粉紅腮紅、有機鳥喙，無發條鑰匙。
5. ❌ **石拳 (`boar`)**：C5 殘破海岸首領。有機野豬剛毛、獸皮毛領、肉質粉紅豬鼻，無發條鑰匙。
6. ❌ **停擺核 (`demon`)**：C6 停擺高塔首領。紫色生物魔族皮膚、蝙蝠肉膜翼、有機惡魔角，無發條鑰匙。

---

## 5. 後續重繪分批推進規劃建議（比照 t_63073ba4/t_b51e9456/t_0d32007c）

由於主線首領具備關卡核心地位與招牌技能，重繪工作量龐大且需嚴格維持 0c-28 前後辨識度，建議由製作人（side）另開三批次任務推進：
- **批次 1 (前期兩大門面)**：`wolf`（C0 渣滓之狼）＋ `fog`（C2 白霧）——新手期最高頻接觸之首領。
- **批次 2 (中期兩大高手)**：`abo`（C3 阿波）＋ `falcon`（C4 疾影）——武道家與射手風格機偶。
- **批次 3 (後期兩大終局)**：`boar`（C5 石拳）＋ `demon`（C6 停擺核）——海岸狂暴戰士與高塔魔王終局核心。

---
*本報告存檔於 `docs/art/ENEMY_COMPLIANCE_AUDIT.md`，審查截圖依據保存於 `proofs/enemy_audit/`。*
