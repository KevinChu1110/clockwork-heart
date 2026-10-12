extends SceneTree
## 《發條之心》大廳角色頁五大機芯槽位點擊更換支援 CoreReplaceDialog 比較確認彈窗連動實機截圖存證腳本 (t_f800a6fa)
## 依據任務 t_f800a6fa 驗收要求：
## 1. 大廳角色頁（mobile_lobby.gd, Tab.CHARACTER）展示五大機芯槽位（CoreSlotsRow），熱區 >= 48px，字級 >= 14px。
## 2. 點擊機芯槽位彈出多巴胺風格 CoreReplaceDialog（CompareLayer），呈現屬性對比（攻/防/血/色階/階級）。
## 3. 點擊確認替換後 GameState.core_slots 與大廳即時同步刷新，外觀切換為金階，戰力更新。
## 4. 英文 (en) 與日文 (ja) 語系切換正常，無中文殘留，零系統 Emoji。
## 5. 背包未裝備機芯部件卡片（5347 行 ActionLabel）字級為 14px 加粗，深藍紫描邊。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f800a6fa/bravesoul-game/proofs/t_f800a6fa",
	"/opt/side/bravesoul-game/proofs/t_f800a6fa"
]

var _step: int = 0
var _frame: int = 0
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null

var _old_part: Dictionary = {
	"uid": "proof_old_mainspring",
	"slot": "mainspring",
	"slot_name": "發條發電機",
	"tier": "white",
	"tier_name": "白",
	"calibration_count": 1,
	"max_calibrations": 7,
	"stats": {"atk": 10, "hp": 40}
}

var _new_part: Dictionary = {
	"uid": "proof_new_mainspring",
	"slot": "mainspring",
	"slot_name": "發條發電機",
	"tier": "gold",
	"tier_name": "金",
	"calibration_count": 0,
	"max_calibrations": 7,
	"stats": {"atk": 45, "hp": 180}
}


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("=== 開始執行 t_f800a6fa 實機 Framebuffer 截圖存證 ===")
	_step = 1
	_frame = 0


func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	for p in OUT_PATHS:
		var target := p.path_join(filename)
		img.save_png(target)
		print("  [CAPTURE] 已儲存: %s (%dx%d)" % [target, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			# 初始化資料並切換至 Tab.CHARACTER (角色頁)
			if _frame >= 15:
				_cs.call("clear_inventory")
				_cs.call("equip_part", "mainspring", _old_part)
				_cs.call("add_part_to_inventory", _new_part)
				if _gs and "core_slots" in _gs:
					_gs.core_slots["mainspring"] = _old_part
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.call("_refresh_char_core_slots")
				_lobby.call("refresh_hud")
				_step = 2
				_frame = 0
		2:
			# 截圖 1: 繁中大廳角色頁五大機芯槽位
			if _frame >= 20:
				_save_viewport("proof_01_char_core_slots_zh_TW.png")
				# 點擊 CoreSlot_mainspring 觸發比較彈窗
				var core_slots_row: Control = _lobby.find_child("CoreSlotsRow", true, false) as Control
				if core_slots_row:
					var ms_card: Control = core_slots_row.find_child("CoreSlot_mainspring", true, false) as Control
					if ms_card:
						var btn: Button = ms_card.find_child("SlotButton", true, false) as Button
						if btn:
							btn.pressed.emit()
				_step = 3
				_frame = 0
		3:
			# 截圖 2: 繁中 CoreReplaceDialog 比較彈窗 (白階 vs 金階)
			if _frame >= 25:
				_save_viewport("proof_02_core_replace_dialog_zh_TW.png")
				# 點擊確認替換
				var cmp_layer: Control = _lobby.find_child("CompareLayer", true, false) as Control
				if cmp_layer:
					var btn_confirm: Button = cmp_layer.find_child("BtnConfirmReplace", true, false) as Button
					if btn_confirm:
						btn_confirm.pressed.emit()
				_step = 4
				_frame = 0
		4:
			# 截圖 3: 確認替換後，大廳槽位外觀刷新為金階，有效戰力即時刷新，呈現 Toast 提示
			if _frame >= 8:
				_save_viewport("proof_03_core_replaced_combat_power_refreshed_zh_TW.png")
				# 準備英文 (en) 測試
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_apply_locale_texts")
				_step = 5
				_frame = 0
		5:
			# 截圖 4: 英文角色頁五大機芯槽位 (5 Core Slots Configuration)
			if _frame >= 20:
				_save_viewport("proof_04_char_core_slots_en.png")
				# 裝備舊件並加入新件，打開英文比較彈窗
				_cs.call("clear_inventory")
				_cs.call("equip_part", "mainspring", _old_part)
				_cs.call("add_part_to_inventory", _new_part)
				if _gs and "core_slots" in _gs:
					_gs.core_slots["mainspring"] = _old_part
				_lobby.open_core_replace_dialog("mainspring", _new_part)
				_step = 6
				_frame = 0
		6:
			# 截圖 5: 英文 CoreReplaceDialog 比較彈窗 (零中文殘留)
			if _frame >= 25:
				_save_viewport("proof_05_core_replace_dialog_en.png")
				var cmp_layer: Control = _lobby.find_child("CompareLayer", true, false) as Control
				if cmp_layer:
					var btn_cancel: Button = cmp_layer.find_child("BtnCancelReplace", true, false) as Button
					if btn_cancel:
						btn_cancel.pressed.emit()
				# 準備日文 (ja) 測試
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_apply_locale_texts")
				_lobby.open_core_replace_dialog("mainspring", _new_part)
				_step = 7
				_frame = 0
		7:
			# 截圖 6: 日文 CoreReplaceDialog 比較彈窗 (白階／金階)
			if _frame >= 25:
				_save_viewport("proof_06_core_replace_dialog_ja.png")
				var cmp_layer: Control = _lobby.find_child("CompareLayer", true, false) as Control
				if cmp_layer:
					var btn_cancel: Button = cmp_layer.find_child("BtnCancelReplace", true, false) as Button
					if btn_cancel:
						btn_cancel.pressed.emit()
				# 切換至 Tab.BAG 驗證 5347 行 ActionLabel 14px
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_apply_locale_texts")
				_lobby.call("_switch_tab", 4) # Tab.BAG
				_cs.call("clear_inventory")
				_cs.call("add_part_to_inventory", _new_part)
				_lobby.call("_refresh_bag_tab", false)
				_step = 8
				_frame = 0
		8:
			# 截圖 7: 背包卡片 ActionLabel 14px 加粗深藍紫描邊
			if _frame >= 20:
				_save_viewport("proof_07_core_bag_action_label_14px.png")
				print("=== 全部 7 張實機 Framebuffer 截圖存證完成 ===")
				quit(0)
				return true
	return false
