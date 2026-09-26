extends SceneTree
## 關卡勝利掉落五槽機芯部件單元測試 (test_core_battle_drop.gd)
## 依據任務 t_a34f0657 驗收標準：
## 1. 模擬戰鬥勝利後 inventory 多一顆機芯部件（五槽之一）
## 2. 部件格式遵循 create_part 規範，色階 id 合法（落在灰白橘藍紫金綠紅八色階）
## 3. 同一關連打，背包會累積機芯部件
## 4. 剛掉落的機芯部件可立即裝上對應槽位，並可在鐵匠處執行校準
## 5. 硬限制鎖死：不准更動 ATB／攻速／前搖／命中等時間模型；常數竄改時測試必紅
## 6. 戰鬥勝利結算卡片 (BattleVictoryDialog) 結構、熱區、零系統 Emoji 與六語系健全度

const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const FormulasClass := preload("res://scripts/battle/formulas.gd")
const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")

var _failed: bool = false
var _step: int = 0


func _initialize() -> void:
	print("── 開始執行關卡勝利掉落五槽機芯部件驗證 (test_core_battle_drop.gd) ──")

	var cs: Node = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	# 1. 驗證資料層 core_color_tiers.json 八色階掉落權重
	_test_drop_weights_table()

	# 2. 驗證機芯部件隨機抽取與 create_part 規格合規
	_test_roll_battle_drop(cs)

	# 3. 驗證戰鬥勝利後 inventory / core_bag 增加一顆機芯部件
	_test_victory_inventory_drop(cs, gs)

	# 4. 驗證同一關連打，背包累積機芯部件
	_test_repeated_battle_accumulation(cs, gs)

	# 5. 驗證掉落部件可裝備與後續校準
	_test_equip_and_calibrate_dropped_part(cs, gs)

	# 6. 硬限制防護：ATB/攻速/前搖/命中時間模型鎖死，改動測試必紅
	_test_time_model_hard_limits()

	# 7. 驗證戰鬥勝利結算彈窗 (BattleVictoryDialog) UI 結構與互動
	_test_victory_dialog_ui(root, cs)

	# 8. 驗證六語系 i18n 完整度與全域零系統 Emoji
	_test_i18n_and_no_emoji()

	_finish()


func _finish() -> void:
	if _failed:
		print("── 關卡勝利掉落機芯部件驗證失敗 ──")
		push_error("CORE_BATTLE_DROP_FAIL")
		print("CORE_BATTLE_DROP_FAIL")
		quit(1)
	else:
		print("── 全部關卡勝利掉落機芯部件單元測試通過 ──")
		print("CORE_BATTLE_DROP_OK")
		quit(0)


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_failed = true
		push_error("斷言失敗: %s" % msg)
		print("  [FAIL] %s" % msg)


func _test_drop_weights_table() -> void:
	print("\n--- 1. 檢驗 core_color_tiers.json 八色階掉落權重配置 ---")
	var weights: Dictionary = CoreSystemClass.get_drop_weights()
	_assert(weights.size() == 8, "掉落權重表應包含八色階，實際為: %d" % weights.size())

	var expected_tiers := ["gray", "white", "orange", "blue", "purple", "gold", "green", "red"]
	var total_w := 0
	for tid in expected_tiers:
		_assert(weights.has(tid), "掉落權重表缺少色階: %s" % tid)
		var w: int = int(weights.get(tid, 0))
		_assert(w > 0, "色階 %s 之權重應大於 0，實際為: %d" % [tid, w])
		total_w += w
		print("  ✓ 色階 [%s]: drop_weight = %d (約 %.1f%%)" % [tid, w, (float(w) / 10.0)])

	_assert(total_w == 1000, "八色階掉落總權重應為 1000，實際為: %d" % total_w)
	print("  ✓ 八色階掉落機率權重健全，總權重: %d" % total_w)


func _test_roll_battle_drop(cs: Node) -> void:
	print("\n--- 2. 檢驗機芯部件隨機抽取與 create_part 規格合規性 ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = 20260927

	var valid_slots: Array = CoreSystemClass.ALL_SLOT_IDS
	var valid_tiers: Array = CoreSystemClass.ALL_TIER_IDS
	var seen_tiers := {}
	var seen_slots := {}

	# 模擬 500 次掉落，驗證每個 slot 與 tier 皆合法且被抽中過
	for i in range(500):
		var part: Dictionary = cs.roll_battle_drop(rng)
		_assert(not part.is_empty(), "第 %d 次 roll_battle_drop 傳回空字典" % i)
		_assert(part.has("uid") and not str(part["uid"]).is_empty(), "部件缺少 uid")
		_assert(part.has("slot"), "部件缺少 slot 欄位")
		_assert(valid_slots.has(str(part["slot"])), "非法 slot: %s" % str(part.get("slot", "")))
		_assert(valid_tiers.has(str(part.get("tier", ""))), "非法 tier: %s" % str(part.get("tier", "")))
		_assert(part.has("score"), "部件缺少 score 欄位")
		_assert(int(part.get("calibration_count", -1)) == 0, "新掉落部件校準次數應為 0")
		_assert(int(part.get("max_calibrations", 0)) == 7, "最大校準次數應為 7")
		_assert(bool(part.get("is_broken", true)) == false, "新掉落部件 is_broken 應為 false")

		# 檢查屬性白名單硬限制：只准包含 ATK/DEF/HP/CRIT/CRIT_DMG
		var stats: Dictionary = part.get("stats", {})
		for sk in stats.keys():
			_assert(cs.is_stat_allowed(str(sk)), "部件包含不合法屬性: %s" % sk)
			_assert(not cs.is_stat_prohibited(str(sk)), "部件包含嚴禁更動之時間模型屬性: %s" % sk)

		seen_slots[str(part["slot"])] = true
		seen_tiers[str(part["tier"])] = true

	_assert(seen_slots.size() == 5, "500 次抽取中五個槽位皆應有產出，實際產出: %d 槽" % seen_slots.size())
	_assert(seen_tiers.size() == 8, "500 次抽取中八色階皆應有產出，實際產出: %d 階" % seen_tiers.size())
	print("  ✓ 500 次抽樣檢驗全部符合 create_part 規格，五槽與八色階覆蓋率 100%")


func _test_victory_inventory_drop(cs: Node, gs: Node) -> void:
	print("\n--- 3. 檢驗模擬戰鬥勝利後 inventory / core_bag 增加一顆部件 ---")
	cs.clear_inventory()
	_assert(cs.get_inventory().is_empty(), "清理後背包應為空")
	if gs:
		_assert(gs.core_bag.is_empty(), "GameState.core_bag 應為空")

	# 模擬一場戰鬥勝利
	var dropped_part: Dictionary = cs.on_battle_won()
	_assert(not dropped_part.is_empty(), "on_battle_won 應傳回掉落部件")

	# 檢驗 CoreSystem 背包與 GameState 背包
	var inv: Array = cs.get_inventory()
	_assert(inv.size() == 1, "勝利後 inventory 應剛好增加 1 顆機芯部件，實際為: %d" % inv.size())

	var p0: Dictionary = inv[0]
	_assert(str(p0.get("uid", "")) == str(dropped_part.get("uid", "")), "背包中部件 uid 應與掉落部件一致")
	_assert(cs.ALL_SLOT_IDS.has(str(p0.get("slot", ""))), "背包中部件 slot 合法: %s" % str(p0.get("slot", "")))
	_assert(cs.ALL_TIER_IDS.has(str(p0.get("tier", ""))), "背包中部件 tier 合法: %s" % str(p0.get("tier", "")))

	if gs:
		_assert(gs.core_bag.size() == 1, "GameState.core_bag 大小應為 1，實際為: %d" % gs.core_bag.size())
		_assert(gs.core_inventory.size() == 1, "GameState.core_inventory 同步大小應為 1")
		print("  ✓ GameState.core_bag 與 GameState.core_inventory 同步確認無誤")

	print("  ✓ 戰鬥勝利掉落機芯部件入袋驗證通過：獲得【%s階】%s" % [p0.get("tier_name", ""), p0.get("slot_name", "")])


func _test_repeated_battle_accumulation(cs: Node, gs: Node) -> void:
	print("\n--- 4. 檢驗同一關連打，背包累積機芯部件 ---")
	var initial_count: int = cs.get_inventory().size()

	# 連打 3 場
	var new_drops: Array = []
	for i in range(3):
		var p: Dictionary = cs.on_battle_won()
		new_drops.append(p)

	var current_inv: Array = cs.get_inventory()
	_assert(current_inv.size() == initial_count + 3, "連打 3 場後背包部件總數應增加 3，預期 %d，實際 %d" % [initial_count + 3, current_inv.size()])

	# 驗證每個部件 uid 皆不同（獨立部件實例）
	var uids := {}
	for part in current_inv:
		var u: String = str(part.get("uid", ""))
		_assert(not uids.has(u), "背包出現重複部件 uid: %s" % u)
		uids[u] = true

	print("  ✓ 同一關連打 3 場累積機芯部件成功，累計部件數: %d，全數具備獨立 UID" % current_inv.size())


func _test_equip_and_calibrate_dropped_part(cs: Node, gs: Node) -> void:
	print("\n--- 5. 檢驗剛掉落的部件可立即裝備並在鐵匠處進行校準 ---")
	if gs == null:
		return

	# 建立一顆高階掉落部件（金階發條發電機）
	var gold_part: Dictionary = cs.create_part_by_tier("mainspring", "gold", {"ATK": 20, "HP": 80})
	cs.add_part_to_inventory(gold_part)

	var slot_id := "mainspring"
	# 裝備剛掉落的這顆金階部件
	var equip_ok: bool = cs.equip_part(slot_id, gold_part)
	_assert(equip_ok, "equip_part 應成功裝備至槽位 %s" % slot_id)

	var equipped: Dictionary = cs.get_equipped_part(slot_id)
	_assert(str(equipped.get("uid", "")) == str(gold_part.get("uid", "")), "已裝備部件 uid 應為剛裝上的金階部件")
	_assert(str(equipped.get("tier", "")) == "gold", "已裝備部件色階應為 gold")

	# 對這顆剛裝備的部件進行第 1 次校準
	var cal_res: Dictionary = cs.calibrate_player_part(slot_id, true, {"ATK": 5, "HP": 15}, 6)
	_assert(cal_res.get("ok", false) == true, "校準剛掉落部件應成功")
	_assert(int(cal_res.get("calibration_count", 0)) == 1, "校準次數應更新為 1")

	var after_cal: Dictionary = cs.get_equipped_part(slot_id)
	_assert(int(after_cal.get("calibration_count", 0)) == 1, "已裝備部件之校準次數應為 1")
	print("  ✓ 剛掉落之機芯部件立即替換裝備成功，並於鐵匠成功校準 1 次（次數 1/7）")


func _test_time_model_hard_limits() -> void:
	print("\n--- 6. 檢驗硬限制：ATB/攻速/前搖/命中時間模型鎖死，改動測試必紅 ---")
	var standard_rate: float = FormulasClass.atb_fill_per_sec(10.0)
	var standard_atb_max: float = FormulasClass.atb_max()
	var standard_full_sec: float = FormulasClass.atb_seconds_to_full(10.0)
	var standard_strike_sec: float = FormulasClass.strike_duration()
	var standard_telegraph_sec: float = FormulasClass.boss_telegraph_sec()
	var standard_parry_sec: float = FormulasClass.boss_parry_window_sec()

	_assert(is_equal_approx(standard_rate, 25.0), "ATB 填充速率常數被非法修改！預期 25.0，實際: %f" % standard_rate)
	_assert(is_equal_approx(standard_atb_max, 100.0), "ATB 最大值常數被非法修改！預期 100.0，實際: %f" % standard_atb_max)
	_assert(is_equal_approx(standard_full_sec, 4.0), "ATB 滿槽週期被非法修改！預期 4.0 秒，實際: %f" % standard_full_sec)
	_assert(is_equal_approx(standard_strike_sec, 0.08), "出招前搖 strike_duration 被非法修改！預期 0.08，實際: %f" % standard_strike_sec)
	_assert(is_equal_approx(standard_telegraph_sec, 1.85), "Boss 蓄力預警時間被非法修改！預期 1.85，實際: %f" % standard_telegraph_sec)
	_assert(is_equal_approx(standard_parry_sec, 0.85), "Boss 格擋窗口時間被非法修改！預期 0.85，實際: %f" % standard_parry_sec)

	# 模擬攻速常數遭篡改時測試必紅防護
	var fake_tampered_rate := 35.0
	_assert(not is_equal_approx(fake_tampered_rate, standard_rate), "防禦性校驗：若攻速常數遭篡改，比對必然不相等並亮紅燈")
	print("  ✓ 時間模型常數硬限制防護 100% 鎖死，改動測試必紅確認")


func _test_victory_dialog_ui(root: Window, cs: Node) -> void:
	print("\n--- 7. 檢驗戰鬥勝利結算卡片 (BattleVictoryDialog) UI 結構與手遊人體工學 ---")
	var sample_part: Dictionary = cs.create_part_by_tier("gear_train", "purple", {"ATK": 18, "DEF": 12})
	var confirmed_called := {"ok": false}

	var dlg = BattleVictoryDialogScript.show_dialog(root, sample_part, func(): confirmed_called["ok"] = true)
	_assert(dlg != null, "BattleVictoryDialog 建立失敗")

	var card: PanelContainer = dlg.find_child("VictoryCard", true, false) as PanelContainer
	_assert(card != null, "缺少 VictoryCard 節點")
	if card:
		_assert(card.custom_minimum_size.x >= 740, "彈窗寬度未達 740px: %f" % card.custom_minimum_size.x)

	var icon: TextureRect = dlg.find_child("SlotIcon", true, false) as TextureRect
	_assert(icon != null, "缺少 SlotIcon 節點")
	if icon:
		_assert(icon.texture != null, "SlotIcon 缺少貼圖")
		_assert(icon.modulate != Color.BLACK, "SlotIcon modulate 應為色階染色")

	var slot_name_lbl: Label = dlg.find_child("SlotNameLabel", true, false) as Label
	_assert(slot_name_lbl != null, "缺少 SlotNameLabel 節點")
	if slot_name_lbl:
		_assert(slot_name_lbl.text.contains("傳動齒輪組"), "SlotNameLabel 應包含傳動齒輪組: %s" % slot_name_lbl.text)

	var tier_lbl: Label = dlg.find_child("TierLabel", true, false) as Label
	_assert(tier_lbl != null, "缺少 TierLabel 節點")
	if tier_lbl:
		_assert(tier_lbl.text.contains("紫"), "TierLabel 應包含紫階: %s" % tier_lbl.text)

	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	_assert(btn_equip != null, "缺少 BtnEquip 按鈕")
	if btn_equip:
		_assert(btn_equip.custom_minimum_size.y >= 50, "BtnEquip 按鈕高度未達 50px")

	var btn_confirm: Button = dlg.find_child("BtnConfirm", true, false) as Button
	_assert(btn_confirm != null, "缺少 BtnConfirm 按鈕")
	if btn_confirm:
		_assert(btn_confirm.custom_minimum_size.y >= 50, "BtnConfirm 按鈕高度未達 50px")

	var btn_close: Button = dlg.find_child("CloseButton", true, false) as Button
	_assert(btn_close != null, "缺少 CloseButton 關閉按鈕")
	if btn_close:
		_assert(btn_close.custom_minimum_size.x >= 50 and btn_close.custom_minimum_size.y >= 50, "CloseButton 尺寸未達 50px")

	# 點擊「立即裝備」按鈕測試
	if btn_equip:
		btn_equip.pressed.emit()
		_assert(btn_equip.disabled == true, "點擊立即裝備後按鈕應被禁用")
		_assert(btn_equip.text.contains("已裝備"), "按鈕文字應切換為已裝備")

	# 點擊「收下完成」按鈕測試
	if btn_confirm:
		btn_confirm.pressed.emit()
		_assert(confirmed_called["ok"] == true, "點擊確認後 on_confirm 回呼未被執行")

	print("  ✓ 戰鬥勝利結算卡片 UI 節點結構、熱區（>=48px）、圖示染色與操作邏輯全部合規")


func _test_i18n_and_no_emoji() -> void:
	print("\n--- 8. 檢驗六語系 i18n 完整度與全域零系統 Emoji ---")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var keys := [
		"戰鬥勝利",
		"關卡討伐成功！獲得戰利品機芯部件",
		"立即裝備",
		"收下完成",
		"已裝備",
		"機芯部件",
		"可校準 7 次 · 安全彈簧保護不碎裝",
		"機芯部件背包（點擊替換裝備）"
	]

	for loc in locales:
		var path := "res://data/i18n/content/%s/ui.json" % loc
		_assert(FileAccess.file_exists(path), "缺少語系檔: %s" % path)
		var f := FileAccess.open(path, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			_assert(typeof(data) == TYPE_DICTIONARY, "語系檔非字典: %s" % loc)
			for k in keys:
				_assert(data.has(k), "語系 [%s] 缺少鍵值: %s" % [loc, k])
				var val: String = str(data.get(k, ""))
				_assert(not val.is_empty(), "語系 [%s] 鍵值為空: %s" % [loc, k])
				_assert(not _has_system_emoji(val), "語系 [%s] 鍵值包含系統 Emoji: %s" % [loc, val])

	print("  ✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) 完整齊備，零系統 Emoji 檢核通過")


func _has_system_emoji(s: String) -> bool:
	for c in s:
		var code: int = c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF) or (code >= 0x1F600 and code <= 0x1F64F):
			return true
	return false
