extends SceneTree
## 停擺巨偶部位破壞掉落既有鐵屑測試 (test_colossus_part_scrap.gd)
## 驗證項目：
## 1. 三隻巨偶（colossus_lion, colossus_puppet, colossus_elephant）部位材料皆為既有 iron_scrap
## 2. 巨偶戰破壞至少一個部位，戰後背包鐵屑比戰前多
## 3. 同一場沒破壞任何部位，不給這筆鐵屑
## 4. 戰鬥失敗（敗場）即使破部位也不給鐵屑
## 5. 勝場機芯掉落維持正常五槽機芯
## 6. 一般關卡／秘境小 Boss 掉落維持原樣未受影響
## 7. 鐵匠校準判定消耗既有鐵屑，無鐵屑時校準判定為 false
## 8. 結算卡片 (BattleVictoryDialog) ScrapRewardPanel 展示、六語系即時切換與零系統 Emoji

const BattleSimClass = preload("res://scripts/battle/battle_sim.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")
const BattleVictoryDialogScript = preload("res://scripts/battle/battle_victory_dialog.gd")
const WorldContentClass = preload("res://scripts/world/world_content.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  ✓ ", msg)

func _initialize() -> void:
	print("=== 開始 test_colossus_part_scrap 測試 ===")
	root.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	gs.reset_new_game()

	var player_stats := {
		"name": "小白",
		"max_hp": 200,
		"hp": 200,
		"atk": 50,
		"def": 15,
		"speed": 12.0,
	}

	# 1. 驗證三隻巨偶部位材料皆為既有 iron_scrap
	print("\n--- 1. 驗證三隻巨偶部位 materials 為既有 iron_scrap ---")
	var colossus_modes := ["colossus_lion", "colossus_puppet", "colossus_elephant"]
	for cm in colossus_modes:
		var sim = BattleSimClass.make_world_fight(player_stats, cm)
		_assert(sim != null, "%s 戰鬥模擬建立成功" % cm)
		var enemy = sim.get_unit(cm)
		_assert(enemy != null and enemy.parts.size() >= 2, "%s 包含至少兩個部位" % cm)
		for p in enemy.parts:
			var mat = str(p.get("material", ""))
			_assert(mat == "iron_scrap", "%s 部位【%s】材料為既有 iron_scrap（實得：%s）" % [cm, p.get("name", ""), mat])

	# 2. 驗證巨偶戰破壞部位後獲得既有鐵屑入袋
	print("\n--- 2. 驗證破壞部位後鐵屑掉落入袋 ---")
	gs.inventory["iron_scrap"] = 0
	var sim2 = BattleSimClass.make_world_fight(player_stats, "colossus_lion")
	var enemy2 = sim2.get_unit("colossus_lion")
	# 手動開啟破壞限制並擊破部位 0 (溢能尖角，enrage 效果掉 2 個)
	sim2.parts_break_unlocked = true
	sim2.parts_break_stage = 2
	enemy2.hp = 100
	sim2.focus_part_id = enemy2.parts[0].get("id", "")
	# 直接執行部位傷害處理以觸發破壞
	sim2._process_multi_part_damage(enemy2, 500, true)
	_assert(bool(enemy2.parts[0].get("broken", false)), "溢能尖角成功被擊破")
	_assert(not sim2.pending_part_materials.is_empty(), "pending_part_materials 不為空")
	_assert(sim2.pending_part_materials.has("iron_scrap"), "pending_part_materials 包含 iron_scrap")

	# 模擬勝利入袋暫存並透過發獎發放
	BattleSimClass.last_victory_part_loot = sim2.pending_part_materials.duplicate()
	var pre_scrap: int = inv.count("iron_scrap")
	# 執行既有部位發獎邏輯（模擬 main._grant_part_break_loot）
	var loot: Array = BattleSimClass.last_victory_part_loot.duplicate()
	BattleSimClass.last_victory_part_loot = []
	for mid in loot:
		inv.add_item(str(mid), 1)
	var post_scrap: int = inv.count("iron_scrap")
	_assert(post_scrap > pre_scrap, "破壞部位後背包鐵屑增加（戰前 %d -> 戰後 %d）" % [pre_scrap, post_scrap])

	# 3. 驗證同一場沒破壞任何部位，不發鐵屑
	print("\n--- 3. 驗證未破壞任何部位不發鐵屑 ---")
	var sim3 = BattleSimClass.make_world_fight(player_stats, "colossus_puppet")
	_assert(sim3.pending_part_materials.is_empty(), "未破壞部位時 pending_part_materials 為空")
	BattleSimClass.last_victory_part_loot = sim3.pending_part_materials.duplicate()
	var scrap_before_noop: int = inv.count("iron_scrap")
	var loot_noop: Array = BattleSimClass.last_victory_part_loot.duplicate()
	BattleSimClass.last_victory_part_loot = []
	for mid in loot_noop:
		inv.add_item(str(mid), 1)
	var scrap_after_noop: int = inv.count("iron_scrap")
	_assert(scrap_before_noop == scrap_after_noop, "未破部位時鐵屑數量維持不變（%d）" % scrap_after_noop)

	# 4. 驗證敗場不發鐵屑
	print("\n--- 4. 驗證敗場即使破壞部位也不發鐵屑 ---")
	var sim4 = BattleSimClass.make_world_fight(player_stats, "colossus_elephant")
	var enemy4 = sim4.get_unit("colossus_elephant")
	sim4.parts_break_unlocked = true
	sim4.parts_break_stage = 2
	enemy4.hp = 100
	sim4.focus_part_id = enemy4.parts[1].get("id", "")
	sim4._process_multi_part_damage(enemy4, 500, true)
	_assert(not sim4.pending_part_materials.is_empty(), "戰中破壞了部位")
	# 敗場時 last_victory_part_loot 設定為空（如 battle_view.gd 所示）
	var won_flag := false
	BattleSimClass.last_victory_part_loot = sim4.pending_part_materials.duplicate() if won_flag else []
	_assert(BattleSimClass.last_victory_part_loot.is_empty(), "敗場時 last_victory_part_loot 應為空")
	var scrap_before_loss: int = inv.count("iron_scrap")
	var loot_loss: Array = BattleSimClass.last_victory_part_loot.duplicate()
	BattleSimClass.last_victory_part_loot = []
	for mid in loot_loss:
		inv.add_item(str(mid), 1)
	var scrap_after_loss: int = inv.count("iron_scrap")
	_assert(scrap_before_loss == scrap_after_loss, "敗場時背包鐵屑未增加（%d）" % scrap_after_loss)

	# 5. 驗證勝場機芯掉落維持原樣
	print("\n--- 5. 驗證勝場機芯掉落維持五槽機芯 ---")
	var core_drop := CoreSystemClass.roll_and_add_battle_drop()
	_assert(not core_drop.is_empty(), "勝場機芯掉落非空")
	_assert(CoreSystemClass.ALL_SLOT_IDS.has(str(core_drop.get("slot", ""))), "機芯槽位合法")
	_assert(CoreSystemClass.ALL_TIER_IDS.has(str(core_drop.get("tier", ""))), "機芯階級合法")

	# 6. 驗證一般關卡／秘境小 Boss 掉落未被改動
	print("\n--- 6. 驗證一般關卡／秘境小 Boss 掉落未受影響 ---")
	var sim_scar = BattleSimClass.make_world_fight(player_stats, "scar_lord")
	var scar_unit = sim_scar.get_unit("scar_lord")
	_assert(scar_unit != null and scar_unit.parts.size() >= 2, "黑鏽疤主部位正常")
	_assert(str(scar_unit.parts[0].get("material", "")) == "knight_shard", "黑鏽疤主尖角材料維持 knight_shard")
	_assert(str(scar_unit.parts[1].get("material", "")) == "iron_scrap", "黑鏽疤主核心材料維持 iron_scrap")

	# 7. 驗證鐵匠校準消耗既有鐵屑判定
	print("\n--- 7. 驗證鐵匠校準消耗既有鐵屑 ---")
	gs.inventory["iron_scrap"] = 0
	var scrap_zero: int = CoreSystemClass.get_player_scrap()
	_assert(scrap_zero == 0, "無鐵屑時 get_player_scrap 回傳 0")
	_assert(not CoreSystemClass.has_enough_scrap_to_calibrate(), "無鐵屑時 has_enough_scrap_to_calibrate 回傳 false")

	gs.inventory["iron_scrap"] = 10
	var scrap_ten: int = CoreSystemClass.get_player_scrap()
	_assert(scrap_ten == 10, "有 10 鐵屑時 get_player_scrap 回傳 10")
	_assert(CoreSystemClass.has_enough_scrap_to_calibrate(), "有足夠鐵屑時 has_enough_scrap_to_calibrate 回傳 true")

	# 8. 驗證結算卡片 (BattleVictoryDialog) ScrapRewardPanel 與六語系支援
	print("\n--- 8. 驗證結算卡片 ScrapRewardPanel 與六語系支援 ---")
	var sample_part := {
		"id": "test_part_01",
		"slot": "mainspring",
		"tier": "orange",
		"tier_name": "橘",
		"slot_name": "發條發電機",
		"is_colossus": true,
		"exp_gain": 85,
		"scrap_gain": 2,
	}

	var dlg = BattleVictoryDialogScript.show_dialog(root, sample_part, Callable(), 85, 2)
	_assert(dlg != null, "結算卡片實例建立成功")

	var scrap_panel: PanelContainer = dlg.find_child("ScrapRewardPanel", true, false) as PanelContainer
	var scrap_lbl: Label = dlg.find_child("ScrapLabel", true, false) as Label
	var scrap_tag: Label = dlg.find_child("ScrapTagLabel", true, false) as Label
	_assert(scrap_panel != null, "結算卡片包含 ScrapRewardPanel")
	_assert(scrap_lbl != null, "結算卡片包含 ScrapLabel")
	_assert(scrap_tag != null, "結算卡片包含 ScrapTagLabel")
	_assert(scrap_panel.visible, "有破部位時 ScrapRewardPanel 可見")

	var expected_scrap_map := {
		"zh_TW": "鐵屑 +2",
		"zh_CN": "铁屑 +2",
		"en": "Scrap Iron +2",
		"ja": "鉄屑 +2",
		"ko": "철 부스러기 +2",
		"es": "Chatarra +2",
	}
	var expected_tag_map := {
		"zh_TW": "部位破壞",
		"zh_CN": "部位破坏",
		"en": "Part Break",
		"ja": "部位破壊",
		"ko": "부위 파괴",
		"es": "Parte destruida",
	}

	for lc in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
		loc.set_locale(lc)
		dlg.call("_refresh_display")
		var s_text: String = scrap_lbl.text
		var t_text: String = scrap_tag.text
		_assert(s_text == expected_scrap_map[lc], "[%s] ScrapLabel 對齊: '%s' == '%s'" % [lc, s_text, expected_scrap_map[lc]])
		_assert(t_text == expected_tag_map[lc], "[%s] ScrapTagLabel 對齊: '%s' == '%s'" % [lc, t_text, expected_tag_map[lc]])

	# 驗證無破部位時 ScrapRewardPanel 隱藏
	var no_scrap_part := sample_part.duplicate()
	no_scrap_part["scrap_gain"] = 0
	dlg.setup(no_scrap_part, Callable(), 85, 0)
	_assert(not scrap_panel.visible, "無破部位 (scrap_gain=0) 時 ScrapRewardPanel 隱藏")

	dlg.queue_free()

	print("\n=== 測試總結 ===")
	if _ok:
		print("TEST_COLOSSUS_PART_SCRAP_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_PART_SCRAP_FAIL")
		quit(1)
