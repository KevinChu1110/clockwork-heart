extends SceneTree
## REC-01 右手拇指操作熱區 (ThumbPad HUD)
## 時長: 4.5s (由握手信號觸發錄製)
## 操作: 荒路殘兵 setup("road_bandit") -> 3次普攻揮斬 -> 1次換武(巨錘) -> 1次鎖定切換

var _elapsed: float = 0.0
var _step_timer: float = 0.0
var _main: Node = null
var _battle: Control = null
var _sim = null
var _step: int = 0
var _ready_written: bool = false
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _saved_png: bool = false
var _out_dir: String = ""
var _ready_file: String = ""
var _start_file: String = ""

const ID: String = "rec01_thumb_pad"
const TOTAL_DURATION: float = 4.5

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws == "":
		ws = "/tmp"
	_ready_file = ws.path_join(ID + ".ready")
	_start_file = ws.path_join(ID + ".start")
	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			# 等待 main.tscn 載入完成並確認具有 _start_battle_raw
			if current_scene != null and current_scene.has_method("_start_battle_raw"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var eq: Node = root.get_node_or_null("EquipmentSystem")
				if gs and eq:
					gs.call("reset_new_game")
					gs.call("set_flag", "c0_first_battle", true)
					eq.call("_ensure_state")
					gs.set("level", 16)
					var w1: Dictionary = {
						"uid": "rec_sword", "base_id": "test_sword", "name": "金屬長劍", "slot": "weapon",
						"tier": 1, "line": "sword", "quality": "rare", "quality_label": "靈",
						"rolled": {"atk": 18, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
					}
					var w2: Dictionary = {
						"uid": "rec_hammer", "base_id": "test_hammer", "name": "精鋼重錘", "slot": "weapon",
						"line": "hammer", "tier": 1, "quality": "rare", "quality_label": "靈",
						"rolled": {"atk": 28, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
					}
					gs.set("equip_bag", [w1, w2])
					gs.set("equip_worn", {})
					gs.set("weapon_loadout", ["", "", ""])
					gs.set("weapon_loadout_active", 0)
					eq.call("equip_weapon_to_loadout", "rec_sword", 0)
					eq.call("equip_weapon_to_loadout", "rec_hammer", 1)
					eq.call("switch_weapon_loadout", 0)
					_main.call("_start_battle_raw", "road_bandit")
					_step = 1
					print("REC01_BATTLE_STARTED at ", _elapsed)
		1:
			# 等待戰鬥場景節點就緒
			var host: Node = _main.get("host") if _main else null
			if host and host.get_child_count() > 0:
				_battle = host.get_child(host.get_child_count() - 1) as Control
				if _battle and _battle.is_inside_tree():
					_sim = _battle.get("sim")
					if _battle.has_method("_ensure_thumb_hud"):
						_battle.call("_ensure_thumb_hud")
					_step = 2
					_step_timer = 0.0
					print("REC01_BATTLE_NODE_READY at ", _elapsed)
		2:
			# 讓畫面渲染穩定，確保 Xvfb 上已經完全是遊戲戰鬥畫面
			_step_timer += delta
			if _step_timer >= 1.0 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("REC01_READY_FOR_RECORDING written at elapsed=", _elapsed)

			# 等待錄影啟動訊號
			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 3
				_rec_elapsed = 0.0
				print("REC01_RECORDING_STARTED at elapsed=", _elapsed)
		3:
			# 正式錄影時間序列（全部以 _rec_elapsed 為準）
			_rec_elapsed += delta

			# +0.8s: 第 1 次普攻
			if _rec_elapsed >= 0.8 and _step == 3:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_1 at rec_elapsed=", _rec_elapsed)
				_step = 4
		4:
			_rec_elapsed += delta
			# +1.6s: 第 2 次普攻
			if _rec_elapsed >= 1.6 and _step == 4:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_2 at rec_elapsed=", _rec_elapsed)
				_step = 5
		5:
			_rec_elapsed += delta
			# +2.4s: 第 3 次普攻
			if _rec_elapsed >= 2.4 and _step == 5:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_3 at rec_elapsed=", _rec_elapsed)
				_step = 6
		6:
			_rec_elapsed += delta
			# +3.2s: 換武 ThumbSwitch
			if _rec_elapsed >= 3.2 and _step == 6:
				if _battle:
					_battle.call("_on_thumb_switch")
				print("REC01_SWITCH_WEAPON at rec_elapsed=", _rec_elapsed)
				_step = 7
		7:
			_rec_elapsed += delta
			# +3.8s: 鎖定切換 ThumbLock
			if _rec_elapsed >= 3.8 and _step == 7:
				if _battle:
					_battle.call("_thumb_cycle_lock", 1)
				print("REC01_CYCLE_LOCK at rec_elapsed=", _rec_elapsed)
				_step = 8
		8:
			_rec_elapsed += delta
			# +4.0s: 保存關鍵幀截圖
			if _rec_elapsed >= 4.0 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec01_thumb_pad.png")
			# +4.5s: 錄影結束
			if _rec_elapsed >= TOTAL_DURATION:
				print("REC01_DONE at rec_elapsed=", _rec_elapsed)
				quit(0)
				return true
	return false

func _save_screenshot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img:
		var p1 := _out_dir.path_join(filename)
		img.save_png(p1)
		print("SAVED_SCREENSHOT: ", p1)
		var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
		if ws != "":
			DirAccess.make_dir_recursive_absolute(ws)
			img.save_png(ws.path_join(filename))
			print("SAVED_WORKSPACE: ", ws.path_join(filename))
