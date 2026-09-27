# 第二十一種動物「棘輪刺蝟（The Ratchet Hedgehog）」美術與角色設計提案

> 本文件完整規格書已歸檔於：[`docs/design/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md`](../design/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md) 與 [`docs/world/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md`](../world/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md)  
> 制定日期：2026-09-27  
> 負責人：側案·策劃總監 小凱（sideplan）  
> 對應看板任務：`t_2fcea592`  

請美術總監（小柔 sideart）與製作人（老周 side）參閱主文件：[`docs/design/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md`](../design/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md)。

內容完整包含：
1. **職業與武器定位**（棘輪穿針機關鏢 / 巡影飛棘、忍者（Ninja）·鏢體系、地面圓滾滾自鎖防禦與引線多段折返連續穿刺 speed:3/crit:3.5/atk:2/def:0/hp:-2、真假同色的一手、引線穿針與提線制動散熱彈射、深入論證與碧簧蛙旋刃飛鏢絕不撞型之理由，補足忍者職業飛鏢武器缺口，達成忍者匕 2 鏢 2 對稱，向 24 族大圓滿陣容邁出決定性一步）
2. **外觀定調**（CANON 100% 零真皮毛零刺毛零肉身、拋光黃銅外殼 #FF8C42、象牙米白琺瑯面頰與胸腹減震板 #FFFDF8、多巴胺金黃單向棘爪發條鑰匙與耳廓銅圈 #FFD028、薄荷螢綠單片鐘錶放大鏡與微米刻度 #4ED86A、珊瑚粉耐震密封矽膠圈與引線端子 #FF5E8A、消光淬火彈簧鋼棘針 #5A5666、深藍紫厚描邊 #1F1A3A、黑曜石寶石左眼、半圓拋光黃銅音叉耳、厚底黑色防滑減震工匠矽膠靴、三組放射狀淬火彈簧鋼棘發射槽、背部單向棘爪棘輪發條鑰匙）
3. **7 大紙娃娃槽位分層架構與尺寸規格**（400x840 立牌、128x128 遊戲內圖層、HUD/對話框頭像，涵蓋 chassis / head_unit / winding_key / costume / optic_core 即 accessory / weapon / back_curio 即 curio）
4. **六大戰鬥動作姿態**（idle / telegraph / attack / skill / hit / recover）招式意象拆解
5. **產品層准入**：《0.20 Product Lock》§9 准入門檻六題完整自答
6. **機器讀取規格配置章節**（比照 `paperdoll_slots.json` 完整 JSON 定義與 14 項 pending 資產清單）
7. **包體 / Token 成本評估**（單族資產增量 < 0.8 MB、Web 目錄 135 MB 現況據實引用、JSON 結構化控制在 ~330 tokens）
8. **0-ART 系列與 CANON.md 鐵律自檢表**（100% 全綠通過）
