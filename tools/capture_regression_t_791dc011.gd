extends SceneTree
## 《發條之心》大廳角色頁五大機芯槽位支援一鍵配置最高戰力機芯與即時屬性刷新實機截圖存證腳本 (t_791dc011)
## 依據任務 t_791dc011 驗收標準：
## 1. 大廳角色頁展示五大機芯槽位與「一鍵配置」果凍按鈕 (BtnCoreAutoEquip)，熱區 >= 48px。
## 2. 點擊一鍵配置自動換上背包內最高戰力機芯，頂部戰力即時刷新，彈出「戰力提升 +XX！」飄字。
## 3. 最佳狀態下再次點擊一鍵配置，彈出「目前已是最佳機芯配置！」飄字。
## 4. 英文 (en) 與日文 (ja) 語系切換正常，按鈕與飄字在地化完整，零中文殘留，零系統 Emoji。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_791dc011/proofs/t_791dc011",
	"/opt/side/bravesoul-game/proofs/t_791dc011"
]

var _step: int = 0
var _frame: int = 0
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null


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

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("=== 開始執行 t_791dc011 實機 Framebuffer 截圖存證 ===")
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
			# 初始化角色頁五槽為白板低階機芯，背包注入高階機芯
			if _frame >= 20:
				CoreSystemClass.clear_inventory()
				_gs.ensure_core_slots("white")

				var p_mainspring := CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 20, "CRIT": 3.0})
				var p_chassis := CoreSystemClass.create_part_by_tier("chassis", "blue", {"DEF": 15, "HP": 50})
				var p_escapement := CoreSystemClass.create_part_by_tier("escapement", "purple", {"ATK": 15, "DEF": 10})
				var p_gear := CoreSystemClass.create_part_by_tier("gear_train", "green", {"ATK": 35, "CRIT": 5.0})
				var p_soul := CoreSystemClass.create_part_by_tier("soul_core", "red", {"ATK": 50, "DEF": 30})

				CoreSystemClass.add_part_to_inventory(p_mainspring)
				CoreSystemClass.add_part_to_inventory(p_chassis)
				CoreSystemClass.add_part_to_inventory(p_escapement)
				CoreSystemClass.add_part_to_inventory(p_gear)
				CoreSystemClass.add_part_to_inventory(p_soul)

				# 切換至角色頁
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.call("_refresh_char_core_slots")
				_lobby.call("refresh_hud")
				_step = 2
				_frame = 0
		2:
			# 截圖 1: 一鍵配置前（白板槽位與 BtnCoreAutoEquip 按鈕）
			if _frame >= 20:
				_save_viewport("proof_01_char_core_slots_before_auto_equip_zh_TW.png")
				# 執行一鍵配置
				_lobby.auto_equip_cores()
				_step = 3
				_frame = 0
		3:
			# 截圖 2: 一鍵配置後（高階五槽換上、頂部飄字戰力提升 +XX、有效戰力即時刷新）
			if _frame >= 20:
				_save_viewport("proof_02_char_core_auto_equipped_toast_zh_TW.png")
				# 再次點擊一鍵配置，觸發最佳配置提示
				_lobby.auto_equip_cores()
				_step = 4
				_frame = 0
		4:
			# 截圖 3: 已是最佳配置提示（飄字「目前已是最佳機芯配置！」）
			if _frame >= 20:
				_save_viewport("proof_03_char_core_auto_equip_already_best_zh_TW.png")
				# 切換至英文 (en)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_apply_locale_texts")
				_lobby.auto_equip_cores()
				_step = 5
				_frame = 0
		5:
			# 截圖 4: 英文 (en) 角色頁 Auto-Equip 按鈕與最佳配置飄字 (Already at optimal core configuration!)
			if _frame >= 25:
				_save_viewport("proof_04_char_core_auto_equip_en.png")
				# 切換至日文 (ja)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_apply_locale_texts")
				_lobby.auto_equip_cores()
				_step = 6
				_frame = 0
		6:
			# 截圖 5: 日文 (ja) 角色頁 一括装着 按鈕與最佳配置飄字 (現在は最適なコア配置です！)
			if _frame >= 25:
				_save_viewport("proof_05_char_core_auto_equip_ja.png")
				# 切回繁中 (zh_TW) 並截取按鈕特寫與五槽狀態
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_apply_locale_texts")
				_step = 7
				_frame = 0
		7:
			# 截圖 6: 一鍵配置按鈕特寫與高階槽位完成態
			if _frame >= 20:
				_save_viewport("proof_06_btn_auto_equip_min_size_48px.png")
				print("=== 全部 6 張實機 Framebuffer 截圖存證完成 ===")
				quit(0)
				return true

	return false
