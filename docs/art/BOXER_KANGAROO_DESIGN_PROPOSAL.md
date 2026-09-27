# 第二十四種動物「鐵拳袋鼠（The Boxer Kangaroo）」美術與角色設計提案

> 本文件完整規格書已歸檔於：[`docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../design/BOXER_KANGAROO_DESIGN_PROPOSAL.md) 與 [`docs/world/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../world/BOXER_KANGAROO_DESIGN_PROPOSAL.md)  
> 制定日期：2026-09-28  
> 負責人：側案·策劃總監 小凱（sideplan）  
> 對應看板任務：`t_ebe16a1f`  

請美術總監（小柔 sideart）與製作人（老周 side）參閱主文件：[`docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../design/BOXER_KANGAROO_DESIGN_PROPOSAL.md)。

內容完整包含：
1. **職業與武器定位**（氣壓活塞衝壓黃銅拳套、武術家（Monk）·拳（`fist`）體系、西洋拳擊步法彈跳與刺拳連打破勢 speed:2/crit:1.5/atk:1/def:1/hp:4、破勢在勤、深入論證與瓷韻熊貓太極拳套絕不撞型之理由，補足武術家職業拳套武器缺口，達成武術家爪 2 拳 2 對稱，使全遊戲戰士/遊俠/忍者/騎士/法師/武術家六大核心職業全數達成 4 族完全平衡，正式宣告 24 族大圓滿完全閉環，並使 R04 黃銅都市迎來武術家常駐素體）
2. **外觀定調**（CANON 100% 零真皮毛零肉身零肉墊零生物育兒袋、沖壓厚鑄焦糖暖褐赤銅板件 #C86D20、多巴胺冠軍胡桃鉗朱紅拳套裝甲 #E63946、溫潤奶油米白琺瑯腹袋外殼與下顎 #FFFDF8、雙環冠軍金黃黃銅發條鑰匙與齒輪裝飾 #FFD028、蒸氣暖橘導管 #FFA010、雙聯琥珀光學儀表目鏡 #FF9F1C、冷軋鎢鋼雙螺旋減震彈簧後腿與骨架 #4A5568、深藍紫厚描邊 #1F1A3A、雙豎立沖壓長耳、分節黃銅重力平衡長尾、背部高位雙環冠軍發條鑰匙）
3. **7 大紙娃娃槽位分層架構與尺寸規格**（400x840 立牌、128x128 遊戲內圖層、HUD/對話框頭像，涵蓋 chassis / head_unit / winding_key / costume / optic_core 即 accessory / weapon / curio 即 back_curio）
4. **六大戰鬥動作姿態**（idle / telegraph / attack / skill / hit / recover）招式意象拆解
5. **產品層准入**：《0.20 Product Lock》§9 准入門檻六題完整自答
6. **機器讀取規格配置章節**（比照 `paperdoll_slots.json` 完整 JSON 定義與 14 項 pending 資產清單）
7. **包體 / Token 成本評估**（單族資產增量 < 0.8 MB、Web 目錄 135 MB 現況據實引用、JSON 結構化控制在 ~330 tokens）
8. **0-ART 系列與 CANON.md 鐵律自檢表**（100% 全綠通過）
