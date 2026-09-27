# 第二十種動物「星巡浣熊（The Orbit Raccoon）」美術與角色設計提案

> 本文件完整規格書已歸檔於：[`docs/design/ORBIT_RACCOON_DESIGN_PROPOSAL.md`](../design/ORBIT_RACCOON_DESIGN_PROPOSAL.md) 與 [`docs/world/ORBIT_RACCOON_DESIGN_PROPOSAL.md`](../world/ORBIT_RACCOON_DESIGN_PROPOSAL.md)  
> 制定日期：2026-09-27  
> 負責人：側案·程式 阿宏（sideworker） / 側案·策劃總監 小凱（sideplan）  
> 對應看板任務：`t_1b9f32a6`  

請美術總監（小柔 sideart）與製作人（老周 side）參閱主文件：[`docs/design/ORBIT_RACCOON_DESIGN_PROPOSAL.md`](../design/ORBIT_RACCOON_DESIGN_PROPOSAL.md)。

內容完整包含：
1. **職業與武器定位**（反重力脈衝光銃 / 軌道聚焦發條銃、遊俠（Ranger）·銃體系、失重滑行反衝彈射與超光速過載脈衝掃射 speed:0/crit:4.0/atk:5/def:-1/hp:-6、一響定生死、失重微浮力散熱彈射、深入論證與蒸氣企鵝雙管火槍絕不撞型之理由，補足遊俠職業火槍武器缺口，達成遊俠弓 2 銃 2 對稱，開啟朝 24 族邁進新局）
2. **外觀定調**（CANON 100% 零真皮毛零獸肉零肉身、航太電光青工程聚合物外殼 #00C2CB、象牙米白工程塑料面頰與胸腹減震板 #FFFDF8、多巴胺金黃光子太陽能翼板發條鑰匙與耳廓銅圈 #FFD028、薄荷螢綠 HUD 能量游標與瞄準鏡 #4ED86A、珊瑚粉耐壓真空密封矽膠圈與冷氣噴嘴 #FF5E8A、深藍紫厚描邊 #1F1A3A、深邃聚碳酸酯 HUD 偏光護目鏡罩、雙聯微型碟形定向通訊雷達耳、厚底黑色防滑減震磁吸工程矽膠靴、輕量聚合物反重力脈衝光銃、五節同軸高壓放電環形天線長尾、背部四葉光子太陽能翼板發條鑰匙）
3. **7 大紙娃娃槽位分層架構與尺寸規格**（400x840 立牌、128x128 遊戲內圖層、HUD/對話框頭像，涵蓋 chassis / head_unit / winding_key / costume / optic_core 即 accessory / weapon / back_curio 即 curio）
4. **六大戰鬥動作姿態**（idle / telegraph / attack / skill / hit / recover）招式意象拆解
5. **產品層准入**：《0.20 Product Lock》§9 准入門檻六題完整自答
6. **機器讀取規格配置章節**（比照 `paperdoll_slots.json` 完整 JSON 定義與 14 項 pending 資產清單）
7. **包體 / Token 成本評估**（單族資產增量 < 0.8 MB、Web 目錄 135 MB 現狀據實引用、JSON 結構化控制在 ~340 tokens）
8. **0-ART 系列與 CANON.md 鐵律自檢表**（100% 全綠通過）
