# 戰鬥結算部位破壞徽章與多巴胺獎勵入袋演出 驗收存證 (t_5492480c)

## 驗證項目與成果
- [x] **部位破壞成就徽章 (PART BREAK)**：戰鬥擊破 Boss 部位時，結算卡頂部清晰呈現破壞部位標籤（核心反應爐、動力履帶等果凍厚底徽章）。
- [x] **多巴胺獎勵入袋演出**：點擊領取按鈕時觸發金幣與鐵屑爆散並流向背包圖示 (BagTarget) 的粒子流向動畫與入袋音效反饋。
- [x] **手遊人體工學規範**：符合 750px 橫屏彈窗規範、奶油米白底與深藍紫描邊多巴胺色盤，按鈕熱區 >= 48px，零系統 emoji。
- [x] **六語系同步**：支援 zh_TW, zh_CN, en, ja, ko, es 即時切換，外語環境無中文殘留。
- [x] **單元測試全綠**：test_victory_part_break_badges.gd 0 錯誤全數通過。

## 實機截圖清單
1. `proof_01_zh_victory_part_break_badges.png`: 繁中部位破壞徽章、結算卡與背包圖示。
2. `proof_02_zh_victory_reward_particles_flying.png`: 金幣與鐵屑粒子流向背包動畫特寫。
3. `proof_03_en_victory_part_break_badges.png`: 英文語系部位破壞徽章 (Core Reactor, Power Tread) 零中文殘留。
