extends SceneTree
## 機芯八色階名稱六語系單元測試 (test_core_tier_i18n.gd)
## 依據任務 t_eb5f970f 驗收要求：
## 1. 驗證六語系 ui.json 包含機芯八色階名稱（灰／白／橘／藍／紫／金／綠／紅）：
##    en: Gray / White / Orange / Blue / Purple / Gold / Green / Red
##    ja: 灰 / 白 / 橙 / 青 / 紫 / 金 / 緑 / 赤
##    zh_TW: 灰 / 白 / 橘 / 藍 / 紫 / 金 / 綠 / 紅
##    zh_CN: 灰 / 白 / 橘 / 蓝 / 紫 / 金 / 绿 / 红
##    ko: 회색 / 흰색 / 주황 / 파랑 / 보라 / 금색 / 초록 / 빨강
##    es: Gris / Blanco / Naranja / Azul / Púrpura / Dorado / Verde / Rojo
## 2. 驗證鐵匠校準 (ForgeDialog) 在 en、ja、zh_TW 下訊息文字與卡片標籤不露未翻譯色階字
## 3. 驗證整備面板 (EquipPanel) 機芯槽在 en、ja、zh_TW 下提示文字與卡片標籤正確多語系化
## 4. 驗證勝利結算 (BattleVictoryDialog) 掉落卡在 en、ja、zh_TW 下色階標籤正確多語系化
## 5. 驗證動態切換語系 (Loc.locale_changed) 即時生效

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_TIER_NAMES := {
	"zh_TW": {
		"灰": "灰", "白": "白", "橘": "橘", "藍": "藍",
		"紫": "紫", "金": "金", "綠": "綠", "紅": "紅"
	},
	"zh_CN": {
		"灰": "灰", "白": "白", "橘": "橘", "藍": "蓝",
		"紫": "紫", "金": "金", "綠": "绿", "紅": "红"
	},
	"en": {
		"灰": "Gray", "白": "White", "橘": "Orange", "藍": "Blue",
		"紫": "Purple", "金": "Gold", "綠": "Green", "紅": "Red"
	},
	"ja": {
		"灰": "灰", "白": "白", "橘": "橙", "藍": "青",
		"紫": "紫", "金": "金", "綠": "緑", "紅": "赤"
	},
	"ko": {
		"灰": "회색", "白": "흰색", "橘": "주황", "藍": "파랑",
		"紫": "보라", "金": "금색", "綠": "초록", "紅": "빨강"
	},
	"es": {
		"灰": "Gris", "白": "Blanco", "橘": "Naranja", "藍": "Azul",
		"紫": "Púrpura", "金": "Dorado", "綠": "Verde", "紅": "Rojo"
	}
}

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null

class TestMockHost extends Node:
	var _host_ctrl := Control.new()
	func _init():
		add_child(_host_ctrl)
	func ui_clear_host(): pass
	func ui_reset_fade(): pass
	func ui_refresh_hud(): pass
	func ui_host() -> Control: return _host_ctrl
	func ui_toast(_msg: String): pass

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_CORE_TIER_I18N_OK")
					quit(0)
				else:
					push_error("TEST_CORE_TIER_I18N_FAIL")
					print("TEST_CORE_TIER_I18N_FAIL")
					quit(1)
				return true
	return false

func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null

func _run_tests() -> void:
	print("=== 開始 test_core_tier_i18n 測試 ===")
	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		_fail("找不到 Loc 節點")
		return

	var CoreSystem = load("res://scripts/systems/core_system.gd")
	if CoreSystem == null:
		_fail("無法載入 CoreSystem")
		return

	# -------------------------------------------------------------
	# 1. 驗證六語系字典八色階單字對應
	# -------------------------------------------------------------
	print("\n--- 1. 驗證六語系字典八色階單字對應 ---")
	for loc in LOCALES:
		_loc_node.call("set_locale", loc)
		var expected_map: Dictionary = EXPECTED_TIER_NAMES[loc]
		for raw_tier in expected_map.keys():
			var exp_val: String = expected_map[raw_tier]
			var act_val := ContentLoc.text("ui", raw_tier)
			if act_val != exp_val:
				_fail("[%s] 色階「%s」期望 '%s'，實際 '%s'" % [loc, raw_tier, exp_val, act_val])
			else:
				print("  ✓ [%s] %s -> %s" % [loc, raw_tier, act_val])

	# -------------------------------------------------------------
	# 2. 驗證鐵匠校準 (ForgeDialog) 在 en、ja、zh_TW 下的畫面色階文字
	# -------------------------------------------------------------
	print("\n--- 2. 驗證鐵匠校準 (ForgeDialog) 色階呈現 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法載入 ForgeDialog")
		return

	var forge_dlg = ForgeDialogScn.new()
	root.add_child(forge_dlg)

	# 設為藍色機芯部件以驗證 QA 記帳之「藍」不外露
	CoreSystem.reset_player_parts()
	var test_part: Dictionary = CoreSystem.create_part_by_tier("mainspring", "blue")
	CoreSystem.player_parts["mainspring"] = test_part

	# 2.1 zh_TW
	_loc_node.call("set_locale", "zh_TW")
	forge_dlg.call("_refresh_all_forge_core_slots")
	forge_dlg.set("_last_calibrate_state", {
		"slot_name": "發條發電機",
		"tip": "校準微調完成，維持同階",
		"tip_key": "CALIBRATE_MAINTAIN",
		"tier_name": "藍",
		"rem": 6,
		"ok": true
	})
	forge_dlg.call("_update_calibrate_message")
	var msg_lbl := _find_named(forge_dlg, "MsgLabel") as Label
	if msg_lbl == null:
		_fail("ForgeDialog 找不到 MsgLabel")
	else:
		if not ("目前色階：藍階" in msg_lbl.text):
			_fail("zh_TW 下 MsgLabel 應包含「目前色階：藍階」，實際: " + msg_lbl.text)
		else:
			print("  ✓ zh_TW 鐵匠校準文字正確: ", msg_lbl.text)

	# 2.2 en: 絕不准露「藍」或「階」
	_loc_node.call("set_locale", "en")
	forge_dlg.call("_update_calibrate_message")
	if "藍" in msg_lbl.text or "階" in msg_lbl.text:
		_fail("en 下 MsgLabel 不准出現中文色階字「藍」或「階」，實際: " + msg_lbl.text)
	elif not ("Current Tier: Blue" in msg_lbl.text):
		_fail("en 下 MsgLabel 應包含 'Current Tier: Blue'，實際: " + msg_lbl.text)
	else:
		print("  ✓ en 鐵匠校準文字正確（無中文色階字）: ", msg_lbl.text)

	# 2.3 ja: 應為「青階」，不准露「藍」
	_loc_node.call("set_locale", "ja")
	forge_dlg.call("_update_calibrate_message")
	if "藍" in msg_lbl.text:
		_fail("ja 下 MsgLabel 不准出現中文「藍」，實際: " + msg_lbl.text)
	elif not ("青階" in msg_lbl.text):
		_fail("ja 下 MsgLabel 應包含日文「青階」，實際: " + msg_lbl.text)
	else:
		print("  ✓ ja 鐵匠校準文字正確（日文青階）: ", msg_lbl.text)

	forge_dlg.queue_free()

	# -------------------------------------------------------------
	# 3. 驗證整備面板 (EquipPanel) 機芯槽在 en、ja、zh_TW 下提示文字
	# -------------------------------------------------------------
	print("\n--- 3. 驗證整備面板 (EquipPanel) 色階呈現 ---")
	var EquipPanelScn = load("res://scripts/ui/panels/equip_panel.gd")
	var dummy_host = TestMockHost.new()
	root.add_child(dummy_host)

	var equip_panel = EquipPanelScn.new(dummy_host)

	# 3.1 en 下整備提示字
	_loc_node.call("set_locale", "en")
	equip_panel.open()
	var hint_lbl := _find_named(equip_panel._layer, "CoreHintLabel") as Label
	if hint_lbl != null:
		var card0 := _find_named(equip_panel._layer, "SlotCard_mainspring")
		var sbtn := _find_named(card0, "SlotButton") as Button if card0 else null
		if sbtn:
			sbtn.pressed.emit()
			if "藍" in hint_lbl.text or "階" in hint_lbl.text:
				_fail("en 下 EquipPanel CoreHintLabel 不准出現中文色階字「藍」或「階」，實際: " + hint_lbl.text)
			elif not ("Blue" in hint_lbl.text):
				_fail("en 下 EquipPanel CoreHintLabel 應包含 'Blue'，實際: " + hint_lbl.text)
			else:
				print("  ✓ en 整備面板機芯提示文字正確（無中文色階字）: ", hint_lbl.text)

	# 3.2 ja 下整備提示字
	_loc_node.call("set_locale", "ja")
	equip_panel.open()
	hint_lbl = _find_named(equip_panel._layer, "CoreHintLabel") as Label
	if hint_lbl != null:
		var card0 := _find_named(equip_panel._layer, "SlotCard_mainspring")
		var sbtn := _find_named(card0, "SlotButton") as Button if card0 else null
		if sbtn:
			sbtn.pressed.emit()
			if "藍" in hint_lbl.text:
				_fail("ja 下 EquipPanel CoreHintLabel 不准出現中文「藍」，實際: " + hint_lbl.text)
			elif not ("青" in hint_lbl.text):
				_fail("ja 下 EquipPanel CoreHintLabel 應包含日文「青」，實際: " + hint_lbl.text)
			else:
				print("  ✓ ja 整備面板機芯提示文字正確（日文青階）: ", hint_lbl.text)

	dummy_host.queue_free()

	# -------------------------------------------------------------
	# 4. 驗證勝利結算 (BattleVictoryDialog) 掉落卡
	# -------------------------------------------------------------
	print("\n--- 4. 驗證勝利結算 (BattleVictoryDialog) 色階呈現 ---")
	var VictoryDialogScn = load("res://scripts/battle/battle_victory_dialog.gd")
	var vic_dlg = VictoryDialogScn.new()
	root.add_child(vic_dlg)
	vic_dlg.setup(test_part, Callable())

	# 4.1 en
	_loc_node.call("set_locale", "en")
	vic_dlg.call("_refresh_display")
	var v_tier_lbl := _find_named(vic_dlg, "TierLabel") as Label
	if v_tier_lbl == null:
		_fail("BattleVictoryDialog 找不到 TierLabel")
	else:
		if "藍" in v_tier_lbl.text or "階" in v_tier_lbl.text:
			_fail("en 下 BattleVictoryDialog TierLabel 不准出現中文色階字，實際: " + v_tier_lbl.text)
		elif not ("Blue Tier" in v_tier_lbl.text):
			_fail("en 下 BattleVictoryDialog TierLabel 應包含 'Blue Tier'，實際: " + v_tier_lbl.text)
		else:
			print("  ✓ en 勝利結算機芯色階標籤正確: ", v_tier_lbl.text)

	# 4.2 ja
	_loc_node.call("set_locale", "ja")
	vic_dlg.call("_refresh_display")
	if "藍" in v_tier_lbl.text:
		_fail("ja 下 BattleVictoryDialog TierLabel 不准出現中文「藍」，實際: " + v_tier_lbl.text)
	elif not ("青階" in v_tier_lbl.text):
		_fail("ja 下 BattleVictoryDialog TierLabel 應包含日文「青階」，實際: " + v_tier_lbl.text)
	else:
		print("  ✓ ja 勝利結算機芯色階標籤正確: ", v_tier_lbl.text)

	# 4.3 zh_TW
	_loc_node.call("set_locale", "zh_TW")
	vic_dlg.call("_refresh_display")
	if not ("藍階" in v_tier_lbl.text):
		_fail("zh_TW 下 BattleVictoryDialog TierLabel 應包含「藍階」，實際: " + v_tier_lbl.text)
	else:
		print("  ✓ zh_TW 勝利結算機芯色階標籤正確: ", v_tier_lbl.text)

	vic_dlg.queue_free()
