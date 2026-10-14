extends SceneTree
## 戰敗結算 BattleDefeatDialog 新增『前往戰力』快捷果凍按鈕實機截圖存證腳本
## (tools/capture_battle_defeat_power_stat_proof.gd)

var _out_dir: String = ""
var _step := 0
var _wait := 0

var _battle: Control = null
var _current_dlg: Control = null
var _power_stat_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

const TASKS := [
	{"loc": "zh_TW", "file": "proof_01_battle_defeat_five_buttons_zh_TW.png"},
	{"loc": "en", "file": "proof_02_battle_defeat_power_stat_en.png"},
	{"loc": "ja", "file": "proof_03_battle_defeat_power_stat_ja.png"},
	{"loc": "ko", "file": "proof_04_battle_defeat_power_stat_ko.png"},
	{"loc": "es", "file": "proof_05_battle_defeat_power_stat_es.png"},
	{"loc": "zh_CN", "file": "proof_06_battle_defeat_power_stat_zh_CN.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_2cf9d674")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_es = root.get_node_or_null("EnergySystem")
	if _es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			_es = EsClass.new()
			_es.name = "EnergySystem"
			root.add_child(_es)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("has_removed_ads", false)
	if _es:
		_es.call("refresh")
		_es.call("refresh_ad_daily")

	print("── 開始執行戰敗結算前往戰力存證截圖腳本 (t_2cf9d674) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step == 0 and _wait == 1:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		if b_scn:
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "training_dummy")

		var DefeatClass: GDScript = load("res://scripts/battle/battle_defeat_dialog.gd")
		if DefeatClass:
			_current_dlg = DefeatClass.new()
			_current_dlg.z_index = 95
			root.add_child(_current_dlg)
		return false

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])

		if _wait == 5:
			print("  -> 開啟彈窗中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)

		elif _wait >= 25:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 實機截圖完成 [%s]: %s" % [_step + 1, TASKS.size() + 1, code, path])

			_step += 1
			_wait = 0
	elif _step == TASKS.size():
		# Step 7: 模擬點擊 BtnGoPowerStat，調起 PowerStatDialog
		if _wait == 5:
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			print("  -> 模擬點擊 BtnGoPowerStat 按鈕，調起 PowerStatDialog...")
			var btn: Button = _current_dlg.find_child("BtnGoPowerStat", true, false) as Button
			if btn:
				btn.pressed.emit()
		elif _wait >= 25:
			var path := _out_dir.path_join("proof_07_click_go_power_stat_opens_power_stat_dialog.png")
			_save_screenshot(path)
			print("  ✓ [%d/%d] 實機截圖完成 [點擊連動 PowerStatDialog]: %s" % [TASKS.size() + 1, TASKS.size() + 1, path])
			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		_cleanup_nodes()
		print("── 戰敗結算前往戰力存證截圖腳本執行完畢 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_dlg and is_instance_valid(_current_dlg):
		_current_dlg.queue_free()
		_current_dlg = null
	if _power_stat_dlg and is_instance_valid(_power_stat_dlg):
		_power_stat_dlg.queue_free()
		_power_stat_dlg = null
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img: Image = vp.get_texture().get_image()
		if img and not img.is_empty():
			img.save_png(abs_path)
