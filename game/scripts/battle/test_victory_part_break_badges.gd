extends SceneTree
## 戰鬥勝利結算部位破壞徽章與多巴胺獎勵入袋演出單元測試 (test_victory_part_break_badges.gd)
##
## 驗收規範：
## 1. 當戰鬥擊破 Boss 部位時，結算卡頂部展示對應破壞部位成就徽章（例：核心反應爐、動力履帶等）。
## 2. 無部位破壞時，頂部徽章容器隱藏或為空。
## 3. 符合 750px 橫屏彈窗規範、奶油米白底與深藍紫描邊多巴胺色盤，按鈕熱區 >= 48px，零系統 emoji。
## 4. 背包圖示 (BagTarget) 存在，點擊領取按鈕觸發金幣/鐵屑飛散粒子流向動畫與入袋音效。
## 5. 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換，外語環境無殘留中文部位名。

const BattleVictoryDialogScript = preload("res://scripts/battle/battle_victory_dialog.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

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


func _initialize() -> void:
	print("=== 開始 test_victory_part_break_badges 測試 ===")
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

	# ── 1. 驗證擊破 Boss 部位時結算卡頂部展示部位破壞徽章 ──
	print("\n--- 1. 驗證部位破壞徽章（PART BREAK Badges）展示 ---")
	var sample_part_with_breaks := {
		"id": "part_boss_drop_01",
		"slot": "soul_core",
		"tier": "gold",
		"tier_name": "金",
		"slot_name": "共鳴核心",
		"is_colossus": true,
		"exp_gain": 120,
		"scrap_gain": 3,
		"broken_parts": ["核心反應爐", "動力履帶"]
	}

	var confirmed_called := {"ok": false}
	var dlg = BattleVictoryDialogScript.show_dialog(
		root,
		sample_part_with_breaks,
		func(): confirmed_called["ok"] = true,
		120,
		3,
		["核心反應爐", "動力履帶"]
	)
	_assert(dlg != null, "BattleVictoryDialog 實例建立成功")

	var badges_container: HBoxContainer = dlg.find_child("PartBreakBadgesContainer", true, false) as HBoxContainer
	_assert(badges_container != null, "結算卡頂部包含 PartBreakBadgesContainer 容器")
	_assert(badges_container.visible, "擊破部位時 PartBreakBadgesContainer 為可見狀態")
	_assert(badges_container.get_child_count() == 2, "PartBreakBadgesContainer 應展示 2 個部位徽章，實際: %d" % badges_container.get_child_count())

	# 檢查個別徽章結構
	var badge0: PanelContainer = badges_container.get_child(0) as PanelContainer
	_assert(badge0 != null, "第一個徽章實例存在")
	var tag0: Label = badge0.find_child("BreakTagLabel", true, false) as Label
	var name0: Label = badge0.find_child("PartNameLabel", true, false) as Label
	_assert(tag0 != null and tag0.text.contains("PART BREAK"), "徽章 1 包含 PART BREAK 標籤")
	_assert(name0 != null and name0.text.contains("核心反應爐"), "徽章 1 名稱包含核心反應爐，實際: %s" % name0.text)

	var badge1: PanelContainer = badges_container.get_child(1) as PanelContainer
	_assert(badge1 != null, "第二個徽章實例存在")
	var tag1: Label = badge1.find_child("BreakTagLabel", true, false) as Label
	var name1: Label = badge1.find_child("PartNameLabel", true, false) as Label
	_assert(tag1 != null and tag1.text.contains("PART BREAK"), "徽章 2 包含 PART BREAK 標籤")
	_assert(name1 != null and name1.text.contains("動力履帶"), "徽章 2 名稱包含動力履帶，實際: %s" % name1.text)

	# ── 2. 驗證無部位破壞時徽章容器隱藏 ──
	print("\n--- 2. 驗證無部位破壞時徽章隱藏 ---")
	var no_break_part := sample_part_with_breaks.duplicate(true)
	no_break_part["broken_parts"] = []
	dlg.setup(no_break_part, Callable(), 50, 0, [])
	_assert(not badges_container.visible, "無部位破壞時 PartBreakBadgesContainer 隱藏")

	# 恢復部位破壞以便後續測試
	dlg.setup(sample_part_with_breaks, func(): confirmed_called["ok"] = true, 120, 3, ["核心反應爐", "動力履帶"])

	# ── 3. 驗證 750px 橫屏彈窗規範、按鈕熱區與零系統 Emoji ──
	print("\n--- 3. 驗證 750px 橫屏彈窗規範、按鈕熱區與零系統 Emoji ---")
	var card: PanelContainer = dlg.find_child("VictoryCard", true, false) as PanelContainer
	_assert(card != null, "結算卡包含 VictoryCard 節點")
	_assert(card.custom_minimum_size.x >= 740, "彈窗寬度符合 750px 規範（>=740px），實際: %f" % card.custom_minimum_size.x)

	var btn_confirm: Button = dlg.find_child("BtnConfirm", true, false) as Button
	_assert(btn_confirm != null and btn_confirm.custom_minimum_size.y >= 50, "BtnConfirm 熱區高度 >= 50px（>=48px）")

	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	_assert(btn_equip != null and btn_equip.custom_minimum_size.y >= 50, "BtnEquip 熱區高度 >= 50px（>=48px）")

	var btn_close: Button = dlg.find_child("CloseButton", true, false) as Button
	_assert(btn_close != null and btn_close.custom_minimum_size.x >= 50 and btn_close.custom_minimum_size.y >= 50, "CloseButton 熱區 >= 50px")

	var bag_target: PanelContainer = dlg.find_child("BagTarget", true, false) as PanelContainer
	_assert(bag_target != null, "包含背包圖示目標 BagTarget")
	_assert(bag_target.custom_minimum_size.x >= 48 and bag_target.custom_minimum_size.y >= 48, "BagTarget 熱區尺寸 >= 48px")

	var bag_icon: TextureRect = dlg.find_child("BagIcon", true, false) as TextureRect
	_assert(bag_icon != null, "BagTarget 內部包含 BagIcon TextureRect")

	# 檢查全域零系統 Emoji
	_check_no_emoji_in_tree(dlg)
	print("  ✓ 全介面 100% 零系統 Emoji 檢驗通過")

	# ── 4. 驗證多巴胺金幣/鐵屑飛散演出與入袋動畫觸發 ──
	print("\n--- 4. 驗證金幣/鐵屑飛散粒子演出與入袋回饋 ---")
	var fx_layer: Control = dlg.find_child("FxLayer", true, false) as Control
	_assert(fx_layer != null, "結算卡包含 FxLayer 特效圖層")

	# 模擬觸發飛散動畫
	var anim_done := {"ok": false}
	dlg.play_reward_particles_to_bag(func(): anim_done["ok"] = true)
	_assert(fx_layer.get_child_count() > 0, "觸發飛散演出後 FxLayer 產生金幣與鐵屑粒子（粒子數: %d）" % fx_layer.get_child_count())

	# 驗證確認按鈕點擊
	btn_confirm.pressed.emit()
	_assert(confirmed_called["ok"], "點擊領取按鈕 (BtnConfirm) 成功觸發確認回呼")

	# ── 5. 驗證六語系同步切換與無中文殘留 ──
	print("\n--- 5. 驗證六語系（zh_TW, zh_CN, en, ja, ko, es）同步 ---")
	var test_locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var expected_core_reactor_map := {
		"zh_TW": "核心反應爐",
		"zh_CN": "核心反应炉",
		"en": "Core Reactor",
		"ja": "コア反応炉",
		"ko": "코어 반응로",
		"es": "Reactor del Núcleo"
	}
	var expected_tread_map := {
		"zh_TW": "動力履帶",
		"zh_CN": "动力履带",
		"en": "Power Tread",
		"ja": "動力キャタピラ",
		"ko": "동력 무한궤도",
		"es": "Oruga de Potencia"
	}

	for lc in test_locales:
		loc.set_locale(lc)
		dlg.call("_refresh_display")

		var b0: PanelContainer = badges_container.get_child(0) as PanelContainer
		var b1: PanelContainer = badges_container.get_child(1) as PanelContainer
		var n0: Label = b0.find_child("PartNameLabel", true, false) as Label
		var n1: Label = b1.find_child("PartNameLabel", true, false) as Label
		var expected0: String = expected_core_reactor_map[lc]
		var expected1: String = expected_tread_map[lc]

		_assert(n0.text == expected0, "[%s] 部位 1 翻譯對齊: '%s' == '%s'" % [lc, n0.text, expected0])
		_assert(n1.text == expected1, "[%s] 部位 2 翻譯對齊: '%s' == '%s'" % [lc, n1.text, expected1])

		if lc in ["en", "ja", "ko", "es"]:
			_assert(not n0.text.contains("核心反應爐"), "[%s] 核心反應爐不准殘留繁中原文" % lc)
			_assert(not n1.text.contains("動力履帶"), "[%s] 動力履帶不准殘留繁中原文" % lc)

	dlg.queue_free()

	print("\n=== 測試總結 ===")
	if _ok:
		print("TEST_VICTORY_PART_BREAK_BADGES_OK")
		quit(0)
	else:
		print("TEST_VICTORY_PART_BREAK_BADGES_FAIL")
		quit(1)
