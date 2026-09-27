# 第二十三種動物「琉璃海馬（The Crystal Seahorse）」美術與角色設計提案

> 本文件完整規格書已歸檔於：[`docs/design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md) 與 [`docs/world/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../world/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md)  
> 制定日期：2026-09-28  
> 負責人：側案·策劃總監 小凱（sideplan）  
> 對應看板任務：`t_f5db0642`  

請美術總監（小柔 sideart）與製作人（老周 side）參閱主文件：[`docs/design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md)。

內容完整包含：
1. **職業與武器定位**（深海靈晶浮空星盤 / 琉璃棱鏡核心、法師（Mage）·水晶（`crystal`）體系、立體浮力洋流阻尼懸停聚焦射擊與護盾織刃反震 speed:0/crit:1.0/atk:0/def:3/hp:10、把護盾織成刃、深入論證與玄機龜八卦星盤絕不撞型之理由，補足法師職業水晶武器缺口，達成法師杖 2 晶 2 對稱，使戰士/遊俠/忍者/騎士/法師五大核心職業全數達成 4 族完全平衡，向 24 族大圓滿陣容邁出決定性一步，並使 R05 琉璃汪洋形成海獺與海馬雙守護陣容）
2. **外觀定調**（CANON 100% 零真魚皮零魚鰓零黏液零肉身、拋光海藍琺瑯烤漆 #38A0FF、薄荷螢綠矽膠雙聯推進背鰭 #2EC4B6、象牙米白陶瓷面頰與前胸護甲 #FFFDF8、珊瑚晶金三叉戟發條鑰匙與齒輪冠冕 #FFD028、珊瑚粉耐壓密封圈 #FF5E8A、深海藍寶石透鏡目鏡 #1C54B2、消光鍍鈦骨架 #7A8B99、深藍紫厚描邊 #1F1A3A、套筒式吸水長吻、五節高彈錳鋼螺旋板簧尾部足底、背部高位三叉戟珊瑚晶簇黃銅發條鑰匙）
3. **7 大紙娃娃槽位分層架構與尺寸規格**（400x840 立牌、128x128 遊戲內圖層、HUD/對話框頭像，涵蓋 chassis / head_unit / winding_key / costume / optic_core 即 accessory / weapon / back_curio 即 curio）
4. **六大戰鬥動作姿態**（idle / telegraph / attack / skill / hit / recover）招式意象拆解
5. **產品層准入**：《0.20 Product Lock》§9 准入門檻六題完整自答
6. **機器讀取規格配置章節**（比照 `paperdoll_slots.json` 完整 JSON 定義與 14 項 pending 資產清單）
7. **包體 / Token 成本評估**（單族資產增量 < 0.8 MB、Web 目錄 135 MB 現況據實引用、JSON 結構化控制在 ~330 tokens）
8. **0-ART 系列與 CANON.md 鐵律自檢表**（100% 全綠通過）
