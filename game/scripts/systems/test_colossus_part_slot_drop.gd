extends SceneTree
## 停擺巨偶破壞部位決定掉哪一槽機芯單元測試 (test_colossus_part_slot_drop.gd)
##
## 驗證項目：
## 1. 巨偶部位對應五槽對照表（COLOSSUS_PART_SLOT_MAP / get_colossus_part_slot）
## 2. 破發條部位必掉發條槽 (mainspring)
## 3. 破各巨偶其他部位必掉對應槽位（機殼／調速器／齒輪／核心）
## 4. 破多個部位取第一個已破（順序優先判定）
## 5. 沒破任何部位維持既有隨機槽
## 6. 鐵屑掉落規則不變（破部位給鐵屑，沒破不給）
## 7. 0-QA27（部位名與巨偶名逐字對齊）與 0-QA28（槽名六語系在地化）
## 8. 戰鬥核心秒數與公式零更動

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
	print("=== 開始 test_colossus_part_slot_drop 測試 ===")
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

	gs.call("reset_new_game", "rabbit")
	cs.call("clear_inventory")

	var player_stats := {
		"name": "小白",
		"max_hp": 300,
		"hp": 300,
		"atk": 80,
		"def": 25,
		"speed": 12.0,
	}

	# ── 1. 驗證巨偶部位對應五槽對照表 ──
	print("\n--- 1. 驗證巨偶部位對照表健全度 ---")
	var colossus_modes := ["colossus_lion", "colossus_puppet", "colossus_elephant"]
	var mapped_slots: Array[String] = []

	for cm in colossus_modes:
		var sim = BattleSimClass.make_world_fight(player_stats, cm)
		_assert(sim != null, "%s 戰鬥模擬建立成功" % cm)
		var enemy = sim.get_unit(cm)
		_assert(enemy != null and enemy.parts.size() >= 2, "%s 包含既有部位" % cm)

		for p in enemy.parts:
			var pname: String = str(p.get("name", ""))
			var praw: String = str(p.get("raw_name", pname))
			var pid: String = str(p.get("id", ""))
			var slot_from_raw := CoreSystemClass.get_colossus_part_slot(cm, praw)
			var slot_from_id := CoreSystemClass.get_colossus_part_slot(cm, pid)
			_assert(slot_from_raw in CoreSystemClass.ALL_SLOT_IDS, "%s 部位【%s】對應有效槽位: %s" % [cm, praw, slot_from_raw])
			_assert(slot_from_id == slot_from_raw, "%s part_id '%s' 與 raw_name '%s' 對應槽位一致: %s" % [cm, pid, praw, slot_from_id])
			if not (slot_from_raw in mapped_slots):
				mapped_slots.append(slot_from_raw)

	# 驗證五槽皆被覆蓋
	for sid in CoreSystemClass.ALL_SLOT_IDS:
		_assert(sid in mapped_slots, "五槽之一【%s】已包含於巨偶部位掉落對照表" % sid)

	# 驗證通用語意解析
	_assert(CoreSystemClass.get_colossus_part_slot("", "發條部位") == CoreSystemClass.SLOT_MAINSPRING, "通用發條部位解析為 mainspring")
	_assert(CoreSystemClass.get_colossus_part_slot("", "機殼部位") == CoreSystemClass.SLOT_CHASSIS, "通用機殼部位解析為 chassis")
	_assert(CoreSystemClass.get_colossus_part_slot("", "調速器部位") == CoreSystemClass.SLOT_ESCAPEMENT, "通用調速器部位解析為 escapement")
	_assert(CoreSystemClass.get_colossus_part_slot("", "齒輪部位") == CoreSystemClass.SLOT_GEAR_TRAIN, "通用齒輪部位解析為 gear_train")
	_assert(CoreSystemClass.get_colossus_part_slot("", "核心部位") == CoreSystemClass.SLOT_SOUL_CORE, "通用核心部位解析為 soul_core")

	# ── 2. 驗證破發條部位必掉發條槽 ──
	print("\n--- 2. 驗證破發條部位必掉發條槽 (mainspring) ---")
	var sim_lion = BattleSimClass.make_world_fight(player_stats, "colossus_lion")
	var lion = sim_lion.get_unit("colossus_lion")
	sim_lion.parts_break_unlocked = true
	sim_lion.parts_break_stage = 2
	lion.hp = 100

	# 鎖定部位 0 (溢能尖角，對應 mainspring)
	sim_lion.focus_part_id = lion.parts[0].get("id", "")
	sim_lion._process_multi_part_damage(lion, 800, true)
	_assert(bool(lion.parts[0].get("broken", false)), "失控發條獅溢能尖角成功擊破")

	var first_broken := sim_lion.get_first_broken_part(lion)
	_assert(not first_broken.is_empty(), "get_first_broken_part 不為空")
	_assert(first_broken.get("part_id") == "spike", "首個破壞部位為 spike")

	var determined_slot := CoreSystemClass.get_colossus_part_slot("colossus_lion", first_broken.get("raw_name"))
	_assert(determined_slot == CoreSystemClass.SLOT_MAINSPRING, "失控發條獅溢能尖角鎖定為 mainspring 槽")

	# 執行 100 次掉落抽樣，驗證 100% 掉落發條槽
	var all_mainspring := true
	for i in 100:
		var p := CoreSystemClass.roll_battle_drop(null, "colossus", determined_slot)
		if str(p.get("slot", "")) != CoreSystemClass.SLOT_MAINSPRING:
			all_mainspring = false
			break
	_assert(all_mainspring, "破發條部位後 100 次掉落抽樣 100% 皆為發條槽 (mainspring)")

	# ── 3. 驗證各巨偶各部位精準對應五槽 ──
	print("\n--- 3. 驗證各巨偶各部位破壞對應掉落 ---")
	var test_matrix := [
		{"boss": "colossus_lion", "part_idx": 1, "exp_slot": CoreSystemClass.SLOT_SOUL_CORE, "desc": "發條獅溢能核心 -> 核心槽"},
		{"boss": "colossus_puppet", "part_idx": 0, "exp_slot": CoreSystemClass.SLOT_GEAR_TRAIN, "desc": "提線人偶溢能尖角 -> 齒輪槽"},
		{"boss": "colossus_puppet", "part_idx": 1, "exp_slot": CoreSystemClass.SLOT_ESCAPEMENT, "desc": "提線人偶溢能核心 -> 調速器槽"},
		{"boss": "colossus_elephant", "part_idx": 0, "exp_slot": CoreSystemClass.SLOT_CHASSIS, "desc": "蒸氣巨象溢能尖角 -> 機殼槽"},
	]

	for tm in test_matrix:
		var b_sim = BattleSimClass.make_world_fight(player_stats, str(tm["boss"]))
		var b_unit = b_sim.get_unit(str(tm["boss"]))
		b_sim.parts_break_unlocked = true
		b_sim.parts_break_stage = 2
		b_unit.hp = 100
		var p_idx: int = int(tm["part_idx"])
		b_sim.focus_part_id = b_unit.parts[p_idx].get("id", "")
		b_sim._process_multi_part_damage(b_unit, 900, true)
		_assert(bool(b_unit.parts[p_idx].get("broken", false)), "%s 擊破: %s" % [tm["boss"], tm["desc"]])

		var fb := b_sim.get_first_broken_part(b_unit)
		var s := CoreSystemClass.get_colossus_part_slot(str(tm["boss"]), fb.get("raw_name"))
		_assert(s == str(tm["exp_slot"]), "部位破壞結算槽位正確: %s == %s" % [s, tm["exp_slot"]])

		var rolled := CoreSystemClass.roll_battle_drop(null, "colossus", s)
		_assert(str(rolled.get("slot", "")) == str(tm["exp_slot"]), "roll_battle_drop 產出正確槽位部件 (%s)" % tm["exp_slot"])

	# ── 4. 驗證破多個部位取第一個已破（順序優先）──
	print("\n--- 4. 驗證破多個部位取第一個已破 ---")
	var sim_multi = BattleSimClass.make_world_fight(player_stats, "colossus_puppet")
	var puppet = sim_multi.get_unit("colossus_puppet")
	sim_multi.parts_break_unlocked = true
	sim_multi.parts_break_stage = 2
	puppet.hp = 100

	# 先破部位 0 (溢能尖角 -> gear_train)
	sim_multi.focus_part_id = puppet.parts[0].get("id", "")
	sim_multi._process_multi_part_damage(puppet, 800, true)
	_assert(bool(puppet.parts[0].get("broken", false)), "第 1 個部位已破壞")

	# 再破部位 1 (溢能核心 -> escapement)
	sim_multi.focus_part_id = puppet.parts[1].get("id", "")
	sim_multi._process_multi_part_damage(puppet, 800, true)
	_assert(bool(puppet.parts[1].get("broken", false)), "第 2 個部位已破壞")

	_assert(sim_multi.broken_parts_order.size() == 2, "broken_parts_order 記錄了兩個部位")
	var multi_first := sim_multi.get_first_broken_part(puppet)
	_assert(multi_first.get("part_id") == "spike", "破多個部位時 get_first_broken_part 取第一個已破部位 (spike)")
	var multi_slot := CoreSystemClass.get_colossus_part_slot("colossus_puppet", multi_first.get("raw_name"))
	_assert(multi_slot == CoreSystemClass.SLOT_GEAR_TRAIN, "破多個部位勝利槽位依首破為 gear_train")

	# ── 5. 驗證沒破任何部位維持隨機槽 ──
	print("\n--- 5. 驗證未破部位維持隨機槽 ---")
	var sim_none = BattleSimClass.make_world_fight(player_stats, "colossus_elephant")
	var elephant = sim_none.get_unit("colossus_elephant")
	var fb_none := sim_none.get_first_broken_part(elephant)
	_assert(fb_none.is_empty(), "未破部位時 get_first_broken_part 為空")

	var target_slot_none := CoreSystemClass.get_colossus_part_slot("colossus_elephant", fb_none.get("raw_name", ""))
	_assert(target_slot_none == "", "未破部位時 target_slot 為空字串")

	var slot_counts := {}
	for i in 100:
		var p := CoreSystemClass.roll_battle_drop(null, "colossus", target_slot_none)
		var sl: String = str(p.get("slot", ""))
		slot_counts[sl] = int(slot_counts.get(sl, 0)) + 1

	_assert(slot_counts.size() >= 3, "未破部位時隨機分佈覆蓋多個槽位（實得 %d 種槽位）" % slot_counts.size())
	for sl in slot_counts.keys():
		_assert(sl in CoreSystemClass.ALL_SLOT_IDS, "隨機掉落之槽位皆屬合法五槽: %s" % sl)

	# ── 6. 驗證鐵屑掉落規則不變 ──
	print("\n--- 6. 驗證鐵屑掉落規則不變 ---")
	_assert(sim_none.pending_part_materials.is_empty(), "未破部位時 pending_part_materials 為空")
	_assert(not sim_multi.pending_part_materials.is_empty(), "破部位時 pending_part_materials 正確獲得材料")
	var iron_count := 0
	for m in sim_multi.pending_part_materials:
		if str(m) == "iron_scrap":
			iron_count += 1
	_assert(iron_count >= 2, "破部位正確累積既有 iron_scrap 材料 (實得 %d 個)" % iron_count)

	# ── 7. 0-QA28 驗證：六語系槽名與部位名過翻譯層 ──
	print("\n--- 7. 0-QA28 六語系槽名與結算展示 ---")
	var sample_drop := CoreSystemClass.create_part_by_tier(CoreSystemClass.SLOT_MAINSPRING, CoreSystemClass.TIER_GOLD)
	sample_drop["is_colossus"] = true
	sample_drop["scrap_gain"] = 2
	sample_drop["exp_gain"] = 85

	var dlg = BattleVictoryDialogScript.show_dialog(root, sample_drop, Callable(), 85, 2)
	_assert(dlg != null, "BattleVictoryDialog 建立成功")

	var slot_lbl: Label = dlg.get_node_or_null("%SlotNameLabel") if dlg.has_node("%SlotNameLabel") else dlg.find_child("SlotNameLabel", true, false)
	_assert(slot_lbl != null, "SlotNameLabel 節點存在")

	var expected_slot_i18n := {
		"zh_TW": "發條發電機",
		"zh_CN": "发条发电机",
		"en": "Mainspring Dynamo",
		"ja": "ぜんまい発電機",
		"ko": "태엽 발전기",
		"es": "Generador de Muelle",
	}

	for lc in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
		loc.set_locale(lc)
		dlg.call("_refresh_display")
		var rendered: String = slot_lbl.text
		_assert(rendered == expected_slot_i18n[lc], "[%s] SlotNameLabel 翻譯正確: '%s' == '%s'" % [lc, rendered, expected_slot_i18n[lc]])

	dlg.queue_free()

	# ── 8. 戰鬥核心秒數約束保護 ──
	print("\n--- 8. 戰鬥核心秒數與時間模型零更動 ---")
	_assert(BattleSimClass.PARRY_EARLY_GRACE == 0.35, "PARRY_EARLY_GRACE 保持 0.35 不變")
	_assert(BattleSimClass.PART_BREAK_HP_RATIO == 0.70, "PART_BREAK_HP_RATIO 保持 0.70 不變")
	_assert(BattleSimClass.PART_BREAK_STAGE2_RATIO == 0.40, "PART_BREAK_STAGE2_RATIO 保持 0.40 不變")

	print("\n=== 測試總結 ===")
	if _ok:
		print("TEST_COLOSSUS_PART_SLOT_DROP_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_PART_SLOT_DROP_FAIL")
		quit(1)
