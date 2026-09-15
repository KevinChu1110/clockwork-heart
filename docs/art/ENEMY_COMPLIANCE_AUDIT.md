# 《發條之心》現有 11 位非雷歐 Boss／敵人立繪零毛皮合規性盤點報告

> **審查日期**：2026-09-15  
> **執行者**：側案·美術總監 小柔 (@sideart)  
> **依據標準**：  
> - 世界觀憲章 `docs/world/CANON.md` 第五章「所有敵人本質上也都是玩具」、零毛皮禁令、金屬板件與發條鑰匙核心規範  
> - 審核準則 `references/review.md` 第 19g-10 條收緊審查法（頭部區域放大裁切＋三項封閉問題自檢）  
> - 任務編號：`t_6f331585`（盤點現有 11 個非雷歐 Boss/敵人立繪的零毛皮合規性）  
> 
> ⛔ **本報告僅進行盤點與審查，不直接產出替換新圖。不合格項目留待後續專項重繪任務執行。**

---

## 1. 審查方法與三項封閉問題門檻

依據 `review.md` 第 19g-10 條規範，所有敵人立繪全面杜絕全圖遠看誤判（避免全身鎧甲掩蓋內部有機毛皮或血肉），逐一將敵人立繪頭部／上半身特寫放大檢驗，強制回答以下三項封閉問題：

1. **① 有沒有毛髮質感的鬃毛／絨毛？**
   - **合格標準**：必須為「**無**」。若有有機毛髮、絨毛、動物鬍鬚、毛皮滾邊皆判定違規。
2. **② 有沒有生物皮膚（腮紅／毛孔／肉色）？**
   - **合格標準**：必須為「**無**」。若有肉色皮膚、粉色腮紅、哺乳動物或人類五官肉質肌理皆判定違規。
3. **③ 頭部或背後有沒有發條鑰匙與螺栓／接縫？**
   - **合格標準**：必須為「**有**」。必須清楚具備世界觀核心視覺符號——發條鑰匙（winding key）、外露螺栓、鉚釘或玩具金屬板件分片接縫。

**判定門檻**：三題必須全部合規（①無 ②無 ③有）才可判定為「**合格**」；任何一題不符即判定為「**不合格**」。

---

## 2. 審查結果總表

| 編號 | 敵人代號 | 敵人名稱 | 資源原圖路徑 | 審查截圖依據 (Panel) | ①毛髮質感 | ②生物皮膚 | ③發條鑰匙/螺栓 | 綜合判定 |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| 01 | `ash_rat` | 灰燼鼠 | `game/assets/sprites/bosses/ash_rat.png` | `proofs/enemy_audit/ash_rat_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 02 | `bamboo_spirit` | 竹靈 | `game/assets/sprites/bosses/bamboo_spirit.png` | `proofs/enemy_audit/bamboo_spirit_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |
| 03 | `coast_raider` | 海岸掠奪者 | `game/assets/sprites/bosses/coast_raider.png` | `proofs/enemy_audit/coast_raider_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 04 | `fog_shade` | 迷霧暗影 | `game/assets/sprites/bosses/fog_shade.png` | `proofs/enemy_audit/fog_shade_audit_panel.png` | **無** (合格) | **無** (合格) | **有** (合格) | ✅ **合格** (t_63073ba4 重繪) |
| 05 | `forest_sprite` | 森林精靈 | `game/assets/sprites/bosses/forest_sprite.png` | `proofs/enemy_audit/forest_sprite_audit_panel.png` | **有** (髮絲) | **有** (違規) | **無** (違規) | ❌ **不合格** |
| 06 | `mirror_wraith` | 鏡中幽靈 | `game/assets/sprites/bosses/mirror_wraith.png` | `proofs/enemy_audit/mirror_wraith_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |
| 07 | `road_bandit` | 荒路匪徒 | `game/assets/sprites/bosses/road_bandit.png` | `proofs/enemy_audit/road_bandit_audit_panel.png` | **無** | **無** | **有** (合格) | ✅ **合格** |
| 08 | `scar_lord` | 黑焰領主 | `game/assets/sprites/bosses/scar_lord.png` | `proofs/enemy_audit/scar_lord_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |
| 09 | `scar_wisp` | 黑焰幽火 | `game/assets/sprites/bosses/scar_wisp.png` | `proofs/enemy_audit/scar_wisp_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |
| 10 | `sewer_slime` | 下水道史萊姆 | `game/assets/sprites/bosses/sewer_slime.png` | `proofs/enemy_audit/sewer_slime_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |
| 11 | `wreck_captain` | 沉船船長 | `game/assets/sprites/bosses/wreck_captain.png` | `proofs/enemy_audit/wreck_captain_audit_panel.png` | 無 | 無 | **無** (違規) | ❌ **不合格** |

> **盤點統計**：
> - 審查總數：11
> - **合格**：**4** 個（`road_bandit` 已於 `t_f1fcef58` 重繪；`ash_rat`、`coast_raider`、`fog_shade` 已於 `t_63073ba4` 依 19g-10 標準成功重繪為發條金屬玩具）
> - **不合格**：**7** 個（其餘皆未玩具機械化，缺乏發條鑰匙與螺栓接縫，或包含血肉/毛皮/腮紅）

*(補充：C1 首領守衛泰坦·雷歐 `leo` 已於 `t_2e6dee93` 完成金屬化改造重繪，具備黃銅雙環發條鑰匙與金屬面甲螺栓，為合規資產。)*

---

## 3. 逐項詳細審查紀錄

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
- **原始資產**：`game/assets/sprites/bosses/bamboo_spirit.png` (122×150 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/bamboo_spirit_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/bamboo_spirit_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/bamboo_spirit_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。整體為竹筒與自然碎屑/靈氣粒子，無動物毛髮。
  - ② 生物皮膚：**無**。呈現天然植物青竹色，無肉色皮膚或腮紅。
  - ③ 發條鑰匙與螺栓：**無**。頭頂為自然斜切空心竹筒，背後背負的是斜插竹管（非發條鑰匙）；全身為植物與布料道袍，完全無金屬螺栓、機械接縫或發條玩具機關。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：雖然無動物毛皮，但完全未落實「發條玩具」世界觀。未來應改為「竹製發條機巧人偶（Karakuri Toy）」——頭部加入雕花黃銅發條鎖栓，關節改為木製卡榫與金屬軸心，背部增設黃銅發條鑰匙。

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
- **原始資產**：`game/assets/sprites/bosses/forest_sprite.png` (125×141 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/forest_sprite_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/forest_sprite_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/forest_sprite_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**有**。頭頂具備柔順的綠色人類少女髮束與馬尾（非金屬片）。
  - ② 生物皮膚：**有**。臉部、脖頸與手臂均為鮮嫩的生物肉色皮膚，雙頰有極為明顯的**粉色少女腮紅**與尖尖的精靈肉耳。
  - ③ 發條鑰匙與螺栓：**無**。純粹的人形生物妖精，無發條鑰匙、無螺栓與金屬接縫。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：典型的二次元生物精靈，嚴重違反「零人類血肉、零腮紅」規範。後續應重繪為「八音盒上的發條芭蕾精靈公仔」——琺瑯金屬烤漆臉、球形木偶關節、背後帶黃銅發條鑰匙、金屬雕刻薄片翅膀。

---

### 06. 鏡中幽靈 (mirror_wraith)
- **原始資產**：`game/assets/sprites/bosses/mirror_wraith.png` (181×200 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/mirror_wraith_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/mirror_wraith_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/mirror_wraith_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。飄散的為以太幽能，非毛皮。
  - ② 生物皮膚：**無**。整體為冷灰藍死靈骷髏質感，無肉色腮紅。
  - ③ 發條鑰匙與螺栓：**無**。為傳統奇幻死靈怨女，全身為破布與靈體，持握普通金屬鏡，身上與背後無發條鑰匙、無機關螺栓。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：缺乏發條玩具屬性。後續重繪應將其改造為「發條魔鏡機偶」——以古董金屬框立鏡為本體，背後有巨大齒輪箱與發條鑰匙，透過活動金屬支架操縱鏡中傀儡。

---

### 07. 荒路匪徒 (road_bandit)
- **原始資產**：`game/assets/sprites/bosses/road_bandit.png` (270×320 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/road_bandit_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/road_bandit_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/road_bandit_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。頭部已改為球形金屬金屬頭，無任何鬍渣或有機毛髮。
  - ② 生物皮膚：**無**。全金屬與磨損鐵皮材質，雙眼為青藍發光鏡片，無肉色皮膚與腮紅。
  - ③ 發條鑰匙與螺栓：**有**。**背後有巨大清晰的黃銅發條鑰匙**，頭殼兩側、下顎與胸甲皆有清楚的十字固定螺栓與分片金屬接縫，盾牌已改為鉚釘鐵皮盾。
- **判定結果**：✅ **合格**
- **說明**：本資產已於任務 `t_f1fcef58` 重新繪製完成並合入 main，100% 符合 CANON 玩具世界觀與 `review.md 19g-10` 驗收標準，行銷素材可安心選用。

---

### 08. 黑焰領主 (scar_lord)
- **原始資產**：`game/assets/sprites/bosses/scar_lord.png` (220×229 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/scar_lord_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/scar_lord_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/scar_lord_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。頂部為黑焰火苗，無毛髮。
  - ② 生物皮膚：**無**。全覆式黑晶重鎧與怨靈紫焰，無肉色皮膚。
  - ③ 發條鑰匙與螺栓：**無**。雖然是金屬鎧甲，但整體造型為傳統暗黑魔王/黑騎士，頭部背後**完全沒有發條鑰匙**，鎧甲接縫為尖刺奇幻風格而非玩具板件接縫與螺栓。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：犯了與雷歐初期相同的錯誤——「把穿金屬鎧甲當成發條玩具」。後續重繪應在頭部兩側或背部加上顯眼的齒輪咬合箱與黑鐵發條鑰匙，胸甲外露發光核心，鎧甲增加手工玩具螺栓與分片模線。

---

### 09. 黑焰幽火 (scar_wisp)
- **原始資產**：`game/assets/sprites/bosses/scar_wisp.png` (84×132 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/scar_wisp_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/scar_wisp_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/scar_wisp_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。為純暗影火焰與煙霧。
  - ② 生物皮膚：**無**。純紫色能量體，無肉色皮膚。
  - ③ 發條鑰匙與螺栓：**無**。純粹飄浮的鬼火，無任何外殼、接縫、螺栓或發條鑰匙。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：純能量體不符合玩具世界實體感。建議改為「發條煤油燈偶」或「帶金屬外框與發條鑰匙的漂浮鬼火燈籠玩具」。

---

### 10. 下水道史萊姆 (sewer_slime)
- **原始資產**：`game/assets/sprites/bosses/sewer_slime.png` (126×124 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/sewer_slime_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/sewer_slime_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/sewer_slime_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。流體凝膠狀，無毛髮。
  - ② 生物皮膚：**無**。綠白雙色果凍黏液，無生物肉色。
  - ③ 發條鑰匙與螺栓：**無**。為傳統 RPG 黏液怪，無機械結構，無螺栓，無發條鑰匙。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：應改為符合世界觀的玩具型史萊姆——例如「橡膠發條玩具史萊姆」、「半透明凝膠內部包裹著咬合齒輪與發條芯軸」，頂部或背部插著發條鑰匙。

---

### 11. 沉船船長 (wreck_captain)
- **原始資產**：`game/assets/sprites/bosses/wreck_captain.png` (176×217 RGBA)
- **依據截圖**：
  - 完整立繪：`proofs/enemy_audit/wreck_captain_full.png`
  - 頭部裁切放大：`proofs/enemy_audit/wreck_captain_head_crop.png`
  - 審查對照面板：`proofs/enemy_audit/wreck_captain_audit_panel.png`
- **三項問題答覆**：
  - ① 毛髮質感：**無**。帽上有羽毛，下巴為水草/破布，無鬃毛絨毛。
  - ② 生物皮膚：**無**。為幽靈白骨面具與青藍光眼，無肉色皮膚。
  - ③ 發條鑰匙與螺栓：**無**。背後插著的是**被擊斃的斷箭殘木**（並非發條鑰匙）；全身衣服為撕裂帆布，武器為腐蝕鐵斧，缺乏發條機械關節與玩具螺栓分片。
- **判定結果**：❌ **不合格**
- **違規詳情與後續建議**：背後的斷箭常被誤認，但經特寫驗證並非發條鑰匙，整體仍是傳統不死幽靈海盜。後續應重繪為「廢棄沈船玩具水手人偶」——以拼接船板為身體，背後插著生鏽黃銅船舵造型的發條鑰匙，四肢採用金屬合頁與螺栓連接。

---

## 4. 行銷團隊素材選用指引（嚴防 19g-10 事故再次發生）

為避免行銷宣傳、FB 排程、短影音與商店截圖再次踩中 `review.md 19g-10` 條款而遭全面退單，即日起行銷團隊選用敵人素材時，**一律嚴格遵守以下白名單與黑名單**：

### 🟢 允許對外發佈之合規敵人白名單 (Whitelist)
1. **守衛泰坦·雷歐 (`leo`)**：已於 `t_2e6dee93` 完成發條機械化改造，具備放射金屬鬃毛、螺栓面甲與黃銅發條鑰匙。
2. **荒路匪徒 (`road_bandit`)**：已於 `t_f1fcef58` 完成重繪，具備金屬球形頭部、鐵皮胸甲與背部發條鑰匙。
3. **灰燼鼠 (`ash_rat`)**：已於 `t_63073ba4` 完成重繪，具備上漆白鐵皮與暗灰鐵板件、彈簧金屬尾與背部黃銅發條鑰匙。
4. **海岸掠奪者 (`coast_raider`)**：已於 `t_63073ba4` 完成重繪，具備牛角鐵盔、銅片玩具鬍、球形關節與背部黃銅發條鑰匙。
5. **迷霧暗影 (`fog_shade`)**：已於 `t_63073ba4` 完成重繪，具備鍛鐵兜帽、齒輪胸腔、格柵面甲與背部黃銅發條鑰匙。

### 🔴 嚴格禁止對外發佈之未合規黑名單 (Blacklist - 待後續美術任務重繪)
- ❌ **森林精靈 (`forest_sprite`)**：含人類肉色皮膚、粉色腮紅與少女髮絲
- ❌ **竹靈 (`bamboo_spirit`)**：無發條鑰匙與玩具機械結構
- ❌ **鏡中幽靈 (`mirror_wraith`)**：純幽靈，無玩具機械結構
- ❌ **黑焰領主 (`scar_lord`)**：純黑鎧魔王，無發條鑰匙與玩具板件
- ❌ **黑焰幽火 (`scar_wisp`)**：純鬼火，無玩具機械結構
- ❌ **下水道史萊姆 (`sewer_slime`)**：純黏液怪，無玩具機械結構
- ❌ **沉船船長 (`wreck_captain`)**：純幽靈海盜，無發條鑰匙（背後為殘箭）

---
*本報告存檔於 `docs/art/ENEMY_COMPLIANCE_AUDIT.md`，審查截圖依據保存於 `proofs/enemy_audit/`。*
