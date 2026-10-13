# 驗收項目自檢表（t_73dedb6c: 🎮 遊戲開發｜MapleInventory 探索背包選取裝備支援鎖定與解鎖切換）

## 1. 規格與功能檢查
- [x] 在 MapleInventory 探索背包物品詳情面板中，為裝備類型（武器/防具）配置『鎖定/解鎖』按鈕（BtnLock）
- [x] 在詳情面板標題列配置鎖定狀態標籤膠囊（LockCapsule / LockStatusLabel）
- [x] 未鎖定狀態：
  - 狀態標籤顯示『未鎖定』（深藍灰膠囊 #7A7090，白字）
  - 按鈕顯示『鎖定』（多巴胺果凍厚底規格，米黃底 #FFF3D6，深藍紫描邊 #1F1A3A）
  - 連動 EquipmentSystem.is_locked(uid) 回傳 false
- [x] 點擊鎖定按鈕切換：
  - 連動呼叫 EquipmentSystem.toggle_lock(uid) / set_locked(uid, true)
  - 狀態標籤切換顯示『已鎖定』（金色多巴胺膠囊 #FFD028，深色字 #1F1A3A）
  - 按鈕切換顯示『解鎖』（金黃果凍厚底按鈕 #FFD028，深藍紫描邊 #1F1A3A）
  - EquipmentSystem.is_locked(uid) 同步回傳 true，並持久化至 GameState
- [x] 再次點擊按鈕切換解鎖：
  - 連動呼叫 EquipmentSystem.toggle_lock(uid) / set_locked(uid, false)
  - 狀態標籤切換回『未鎖定』，按鈕切換回『鎖定』
- [x] 鎖定時防止誤賣與防誤操作：
  - 詳情面板說明文字包含『裝備已鎖定無法出售』警告提示（#E05020）
  - 若處於賣出/拆解操作情境，按鈕自動禁用並提示『已鎖定（無法出售）』或『裝備已鎖定無法出售』
- [x] 非裝備類型道具（消耗品/素材/重要道具）與未選取狀態：
  - 鎖定膠囊與按鈕全數隱藏（visible = false）
- [x] 手遊人因與視覺規範：
  - 按鈕高度 52px（>= 48px 手遊點擊熱區規範）
  - 多巴胺立體厚底 5px，圓角 18px，深藍紫描邊 #1F1A3A
  - 字級 >= 14px，開源粉圓體（Open-Huninn）
  - 100% 零系統 Unicode Emoji
- [x] 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換無缺詞：
  - zh_TW: 鎖定 / 解鎖 / 已鎖定 / 未鎖定 / 裝備已鎖定無法出售
  - zh_CN: 锁定 / 解锁 / 已锁定 / 未锁定 / 装备已锁定无法出售
  - en: Lock / Unlock / Locked / Unlocked / Equipment is locked and cannot be sold
  - ja: ロック / ロック解除 / ロック中 / 未ロック / 装備がロックされているため売却できません
  - ko: 잠금 / 잠금 해제 / 잠김 / 미잠금 / 장비가 잠겨 있어 판매할 수 없습니다
  - es: Bloquear / Desbloquear / Bloqueado / Desbloqueado / El equipo está bloqueado y no se puede vender

## 2. 測試與存證
- [x] 新增單元測試 test_maple_inventory_lock.gd：全綠通過（MAPLE_INVENTORY_LOCK_OK）
- [x] 既有測試回歸 test_maple_inventory.gd：全綠通過（MAPLE_INVENTORY_OK）
- [x] 既有測試回歸 test_maple_inventory_diff.gd：全綠通過（MAPLE_INVENTORY_DIFF_OK）
- [x] 既有測試回歸 test_maple_inventory_equip.gd：全綠通過（MAPLE_INVENTORY_EQUIP_OK）
- [x] 既有測試回歸 test_maple_inventory_chips.gd：全綠通過（MAPLE_INVENTORY_CHIPS_OK）
- [x] 無頭冒煙測試 godot --path game --headless --quit-after 3：0 錯誤、0 SCRIPT ERROR
- [x] clock-check 檢查：全數通過，無缺 .import、語系 key 齊、無退役舊名詞
- [x] 實機截圖存證（1280x720 PNG，經 Vision 審查版面完整、零重疊、零截字、零 Emoji）：
  - `proofs/t_73dedb6c/proof_01_maple_equip_unlocked.png`（SHA256: 7662164e12cc668e...）
  - `proofs/t_73dedb6c/proof_02_maple_equip_locked.png`（SHA256: f6c6bf83852aa20d...）
  - `proofs/t_73dedb6c/proof_03_maple_equip_lock_en.png`（SHA256: dee46f29ee92994b...）
- [x] 實機截圖獨立不重複（SHA256 均不相同）
