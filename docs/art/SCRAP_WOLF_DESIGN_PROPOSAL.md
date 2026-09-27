# 第二十二種動物「荒原鋼狼（The Scrap Wolf）」美術與角色設計提案

> 本文件完整規格書已歸檔於：[`docs/design/SCRAP_WOLF_DESIGN_PROPOSAL.md`](../design/SCRAP_WOLF_DESIGN_PROPOSAL.md) 與 [`docs/world/SCRAP_WOLF_DESIGN_PROPOSAL.md`](../world/SCRAP_WOLF_DESIGN_PROPOSAL.md)  
> 制定日期：2026-09-27  
> 負責人：側案·策劃總監 小凱（sideplan）  
> 對應看板任務：`t_38d295bd`  

請美術總監（小柔 sideart）與製作人（老周 side）參閱主文件：[`docs/design/SCRAP_WOLF_DESIGN_PROPOSAL.md`](../design/SCRAP_WOLF_DESIGN_PROPOSAL.md)。

內容完整包含：
1. **職業與武器定位**（廢土鋸齒重鋼劍 / 破軍殘刃、騎士（Knight）·劍體系、踏地沉穩重鋼鋸斬與生鏽卡阻散熱窗口 200% 破甲暴擊 atk:2/def:1/hp:0/crit:1.0/speed:0、平衡的刃、深入論證與白金兔單手長劍絕不撞型之理由，補足騎士職業長劍武器自創角以來的唯一缺口，達成騎士劍 2 槍 2 對稱，使四大核心戰鬥職業（戰士 4、遊俠 4、忍者 4、騎士 4）邁向完全對稱平衡陣容）
2. **外觀定調**（CANON 100% 零真皮毛零刺毛零肉身、廢土多巴胺暖橘防鏽烤漆鋼板 #FFA010、象牙米白琺瑯面頰與前胸減震甲 #FFFDF8、金黃多巴胺重工十字發條鑰匙與齒輪組 #FFD028、星輝天藍雙聯光學晶核目鏡 #38A0FF、珊瑚粉減震密封矽膠圈與油路端子 #FF5E8A、消光沖壓鎢鋼鋸齒刃部與齒輪護頸 #5A5666、深藍紫厚描邊 #1F1A3A、折疊沖壓黃銅導風耳、厚底黑色防滑減震工業矽膠行軍靴、五層同心鎢鋼齒輪咬合護頸護甲、背部高扭力破軍重工十字發條鑰匙、七節螺旋發條多節平衡鋼尾）
3. **7 大紙娃娃槽位分層架構與尺寸規格**（400x840 立牌、128x128 遊戲內圖層、HUD/對話框頭像，涵蓋 chassis / head_unit / winding_key / costume / optic_core 即 accessory / weapon / back_curio 即 curio）
4. **六大戰鬥動作姿態**（idle / telegraph / attack / skill / hit / recover）招式意象拆解
5. **產品層准入**：《0.20 Product Lock》§9 准入門檻六題完整自答
6. **機器讀取規格配置章節**（比照 `paperdoll_slots.json` 完整 JSON 定義與 14 項 pending 資產清單）
7. **包體 / Token 成本評估**（單族資產增量 < 0.8 MB、Web 目錄 135 MB 現況據實引用、JSON 結構化控制在 ~330 tokens）
8. **0-ART 系列與 CANON.md 鐵律自檢表**（100% 全綠通過）
