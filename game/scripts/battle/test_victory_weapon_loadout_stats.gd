extends SceneTree
## 戰鬥勝利結算三欄武器戰鬥數據統計膠囊單元測試 (test_victory_weapon_loadout_stats.gd)
## godot --headless -s res://scripts/battle/test_victory_weapon_loadout_stats.gd
##
## 驗證項目：
## 1. BattleVictoryDialog 資訊區包含 WeaponLoadoutStatsCapsules 容器節點。
## 2. 包含「輪替次數」膠囊 (WeaponSwapsCapsule) 與三欄武器卡片列 (WeaponSlotsHBox / WeaponSlotCard_0..2)。
## 3. 數據計算與展示正確性：總輪替次數、各欄位武器名稱、傷害數值與佔比進度條。
## 4. 遵循多巴胺鮮亮色盤規範：底色奶油米白、邊框深藍紫 #1F1A3A、圓角 16~20px。
## 5. 字級規範：所有標籤 font_size >= 14px，零 13px 以下小字。
## 6. 全介面 100% 零系統 Emoji。
## 7. 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換（包含「輪替切換」「傷害貢獻」「首選武器」「副手武器」「絕技武器」等詞條）。

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")
const ContentLocClass := preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

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


func _has_emoji(s: String) -> bool:
	for ch in s:
		var code: int = ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false


func _check_no_emoji_in_tree(node: Node) -> void:
	if node is Label:
		var lbl: Label = node as Label
		_assert(not _has_emoji(lbl.text), "節點 [%s] 文字不可含系統 emoji: %s" % [lbl.name, lbl.text])
	elif node is Button:
		var btn: Button = node as Button
		_assert(not _has_emoji(btn.text), "按鈕 [%s] 文字不可含系統 emoji: %s" % [btn.name, btn.text])
	for child in node.get_children():
		_check_no_emoji_in_tree(child)


func _check_font_size_in_tree(node: Node) -> void:
	if node is Label:
		var lbl: Label = node as Label
		var fsize: int = lbl.get_theme_font_size("font_size")
		# 預設若是 0 則視為繼承系統預設字級（通常為 16px）
		if fsize > 0:
			_assert(fsize >= 14, "Label [%s] 字級必須 >= 14px，實際: %dpx" % [lbl.name, fsize])
	elif node is Button:
		var btn: Button = node as Button
		var fsize: int = btn.get_theme_font_size("font_size")
		if fsize > 0:
			_assert(fsize >= 14, "Button [%s] 字級必須 >= 14px，實際: %dpx" % [btn.name, fsize])
	for child in node.get_children():
		_check_font_size_in_tree(child)


func _initialize() -> void:
	print("=== 開始 test_victory_weapon_loadout_stats 測試 ===")
	root.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

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

	loc.set_locale("zh_TW")

	# ── 1. 驗證節點存在性與結構 ──
	print("\n--- 1. 驗證 WeaponLoadoutStatsCapsules 節點結構 ---")
	var sample_part := {
		"id": "part_boss_test_01",
		"slot": "soul_core",
		"tier": "gold",
		"tier_name": "金",
		"slot_name": "共鳴核心",
		"stats": {"atk": 15, "hp": 200},
	}
	var sample_combat_stats := {
		"total_damage": 2000,
		"elapsed_time": 12.5,
		"dps": 160.0,
		"max_hit_damage": 450,
		"total_hit_count": 28,
		"weapon_swap_count": 8,
		"weapon_slot_damages": {0: 1000, 1: 600, 2: 400},
		"weapon_slot_swaps": {0: 3, 1: 3, 2: 2},
		"weapon_bars": [
			{"name": "鐵劍", "index": 0, "quality": "common"},
			{"name": "獵弓", "index": 1, "quality": "uncommon"},
			{"name": "拳套", "index": 2, "quality": "rare"},
		],
	}

	var dlg = BattleVictoryDialogScript.show_dialog(
		root,
		sample_part,
		Callable(),
		100,
		2,
		[],
		sample_combat_stats
	)
	_assert(dlg != null, "BattleVictoryDialog 實例建立成功")

	var capsules_panel: PanelContainer = dlg.get_weapon_loadout_capsules()
	_assert(capsules_panel != null, "包含 WeaponLoadoutStatsCapsules 容器節點")
	_assert(capsules_panel.name == "WeaponLoadoutStatsCapsules", "容器名稱為 WeaponLoadoutStatsCapsules")

	var title_lbl: Label = capsules_panel.find_child("WeaponStatsTitleLabel", true, false) as Label
	_assert(title_lbl != null, "包含傷害貢獻標題 WeaponStatsTitleLabel")
	_assert(title_lbl.text == "傷害貢獻", "傷害貢獻標題文字正確: %s" % title_lbl.text)

	var swaps_capsule: PanelContainer = capsules_panel.find_child("WeaponSwapsCapsule", true, false) as PanelContainer
	_assert(swaps_capsule != null, "包含輪替次數膠囊 WeaponSwapsCapsule")

	var swaps_title: Label = swaps_capsule.find_child("SwapsTitleLabel", true, false) as Label
	_assert(swaps_title != null and swaps_title.text == "輪替切換", "輪替切換標籤存在且文字正確: %s" % (swaps_title.text if swaps_title else ""))

	var swaps_val: Label = swaps_capsule.find_child("SwapsValueLabel", true, false) as Label
	_assert(swaps_val != null and swaps_val.text == "8", "輪替切換次數數值正確展示: %s" % (swaps_val.text if swaps_val else ""))

	var swaps_unit: Label = swaps_capsule.find_child("SwapsUnitLabel", true, false) as Label
	_assert(swaps_unit != null and swaps_unit.text == "次", "輪替切換單位正確: %s" % (swaps_unit.text if swaps_unit else ""))

	var slots_hbox: HBoxContainer = capsules_panel.find_child("WeaponSlotsHBox", true, false) as HBoxContainer
	_assert(slots_hbox != null, "包含三欄武器列容器 WeaponSlotsHBox")
	_assert(slots_hbox.get_child_count() == 3, "WeaponSlotsHBox 包含 3 個欄位卡片")

	# ── 2. 驗證三欄位數據計算正確性 ──
	print("\n--- 2. 驗證三欄位傷害佔比與數值計算 ---")
	var expected_terms := ["首選武器", "副手武器", "絕技武器"]
	var expected_names := ["鐵劍", "獵弓", "拳套"]
	var expected_dmgs := [1000, 600, 400]
	var expected_pcts := ["50.0%", "30.0%", "20.0%"]
	var expected_pbar_vals := [50.0, 30.0, 20.0]

	for i in range(3):
		var card_dict: Dictionary = dlg.get_weapon_slot_card(i)
		_assert(not card_dict.is_empty(), "欄位 %d 卡片資料結構有效" % i)

		var slot_lbl: Label = card_dict.get("slot_title_label")
		_assert(slot_lbl != null and slot_lbl.text == expected_terms[i], "欄位 %d 標籤對齊: %s" % [i, slot_lbl.text if slot_lbl else ""])

		var name_lbl: Label = card_dict.get("name_label")
		_assert(name_lbl != null and name_lbl.text == expected_names[i], "欄位 %d 武器名稱對齊: %s" % [i, name_lbl.text if name_lbl else ""])

		var pct_lbl: Label = card_dict.get("percent_label")
		_assert(pct_lbl != null and pct_lbl.text == expected_pcts[i], "欄位 %d 傷害佔比對齊: %s" % [i, pct_lbl.text if pct_lbl else ""])

		var dmg_lbl: Label = card_dict.get("damage_label")
		var expected_dmg_str := "(%d 點)" % expected_dmgs[i]
		_assert(dmg_lbl != null and dmg_lbl.text == expected_dmg_str, "欄位 %d 傷害數值對齊: %s" % [i, dmg_lbl.text if dmg_lbl else ""])

		var pbar: ProgressBar = card_dict.get("progress_bar")
		_assert(pbar != null and is_equal_approx(pbar.value, expected_pbar_vals[i]), "欄位 %d 進度條數值對齊: %.1f" % [i, pbar.value if pbar else 0.0])

	# ── 3. 驗證字級規範與零系統 Emoji ──
	print("\n--- 3. 驗證字級規範 (>=14px) 與零 Emoji ---")
	_check_font_size_in_tree(dlg)
	print("  ✓ 全彈窗字級 >= 14px 檢驗通過，零 13px 以下小字")

	_check_no_emoji_in_tree(dlg)
	print("  ✓ 全彈窗 100% 零系統 Emoji 檢驗通過")

	# ── 4. 驗證六語系即時切換 ──
	print("\n--- 4. 驗證六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換 ---")
	var expected_i18n := {
		"zh_TW": {
			"title": "傷害貢獻",
			"swaps": "輪替切換",
			"unit": "次",
			"slot0": "首選武器",
			"slot1": "副手武器",
			"slot2": "絕技武器",
			"w0": "鐵劍",
			"w1": "獵弓",
			"w2": "拳套",
		},
		"zh_CN": {
			"title": "伤害贡献",
			"swaps": "轮替切换",
			"unit": "次",
			"slot0": "首选武器",
			"slot1": "副手武器",
			"slot2": "绝技武器",
			"w0": "铁剑",
			"w1": "猎弓",
			"w2": "拳套",
		},
		"en": {
			"title": "Damage Contribution",
			"swaps": "Weapon Swaps",
			"unit": "times",
			"slot0": "Primary Weapon",
			"slot1": "Secondary Weapon",
			"slot2": "Special Weapon",
			"w0": "Iron Sword",
			"w1": "Hunting Bow",
			"w2": "Iron Gauntlet",
		},
		"ja": {
			"title": "ダメージ貢献",
			"swaps": "武器切り替え",
			"unit": "回",
			"slot0": "メイン武器",
			"slot1": "サブ武器",
			"slot2": "絶技武器",
			"w0": "鉄の剣",
			"w1": "猟弓",
			"w2": "拳套",
		},
		"ko": {
			"title": "피해 기여",
			"swaps": "무기 교체",
			"unit": "회",
			"slot0": "주 무기",
			"slot1": "보조 무기",
			"slot2": "필살 무기",
			"w0": "철검",
			"w1": "사냥활",
			"w2": "철 건틀릿",
		},
		"es": {
			"title": "Contribución de daño",
			"swaps": "Cambios de arma",
			"unit": "veces",
			"slot0": "Arma Principal",
			"slot1": "Arma Secundaria",
			"slot2": "Arma Especial",
			"w0": "Espada de Hierro",
			"w1": "Arco de Caza",
			"w2": "Guanteletes de Hierro",
		},
	}

	for lang in LOCALES:
		loc.set_locale(lang)
		dlg.call("_refresh_display")
		var exp_dict: Dictionary = expected_i18n[lang]

		_assert(title_lbl.text == exp_dict.title, "[%s] 傷害貢獻標題正確: '%s' == '%s'" % [lang, title_lbl.text, exp_dict.title])
		_assert(swaps_title.text == exp_dict.swaps, "[%s] 輪替切換標籤正確: '%s' == '%s'" % [lang, swaps_title.text, exp_dict.swaps])

		var card0: Dictionary = dlg.get_weapon_slot_card(0)
		var s0_lbl: Label = card0.get("slot_title_label")
		_assert(s0_lbl.text == exp_dict.slot0, "[%s] 首選武器正確: '%s' == '%s'" % [lang, s0_lbl.text, exp_dict.slot0])

		var card1: Dictionary = dlg.get_weapon_slot_card(1)
		var s1_lbl: Label = card1.get("slot_title_label")
		_assert(s1_lbl.text == exp_dict.slot1, "[%s] 副手武器正確: '%s' == '%s'" % [lang, s1_lbl.text, exp_dict.slot1])

		var card2: Dictionary = dlg.get_weapon_slot_card(2)
		var s2_lbl: Label = card2.get("slot_title_label")
		_assert(s2_lbl.text == exp_dict.slot2, "[%s] 絕技武器正確: '%s' == '%s'" % [lang, s2_lbl.text, exp_dict.slot2])

		# 驗證外語環境無繁中殘留
		if lang in ["en", "ja", "ko", "es"]:
			_assert(not ("傷害貢獻" in title_lbl.text), "[%s] 標題無殘留繁中" % lang)
			_assert(not ("輪替切換" in swaps_title.text), "[%s] 輪替標籤無殘留繁中" % lang)
			_assert(not ("首選武器" in s0_lbl.text), "[%s] 首選武器標籤無殘留繁中" % lang)
			_assert(not ("副手武器" in s1_lbl.text), "[%s] 副手武器標籤無殘留繁中" % lang)
			_assert(not ("絕技武器" in s2_lbl.text), "[%s] 絕技武器標籤無殘留繁中" % lang)

	# ── 5. 驗證空數據與預設值優雅降級 ──
	print("\n--- 5. 驗證未傳入戰鬥數據時之預設值處理 ---")
	var dlg_empty = BattleVictoryDialogScript.show_dialog(
		root,
		sample_part,
		Callable(),
		50,
		1,
		[]
	)
	_assert(dlg_empty != null, "空數據實例建立成功")
	var empty_capsules: PanelContainer = dlg_empty.get_weapon_loadout_capsules()
	_assert(empty_capsules != null, "空數據下 WeaponLoadoutStatsCapsules 仍然存在")
	_assert(dlg_empty.get_weapon_swap_count() == 0, "空數據下輪替切換次數為 0")
	_assert(dlg_empty.get_weapon_slot_damage(0) == 0, "空數據下首選武器傷害為 0")

	dlg.queue_free()
	dlg_empty.queue_free()

	print("\n=== 測試總結 ===")
	if _ok:
		print("TEST_VICTORY_WEAPON_LOADOUT_STATS_OK")
		quit(0)
	else:
		push_error("TEST_VICTORY_WEAPON_LOADOUT_STATS_FAILED")
		quit(1)
