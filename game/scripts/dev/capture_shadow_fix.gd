extends SceneTree
## 截取修復後的兔族與猴族戰鬥截圖 (t_89b36553)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/shadow_fix",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_89b36553/screenshots"
]

var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []

var _races = [
	{"race": "rabbit", "name": "星芒兔", "skill": "橫斬", "mode": "road_bandit", "file": "proof_03_battle_rabbit.png", "tag": "Battle Rabbit"},
	{"race": "macaque", "name": "金毛猴", "skill": "連環拳", "mode": "bamboo_spirit", "file": "proof_07_battle_macaque.png", "tag": "Battle Macaque"},
]
var _race_idx: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				_race_idx = 0
				_start_race_battle(_race_idx)
				_step = 1
				_wait = 0
		1:
			# 等待戰鬥載入並注入技能/滿怒
			if _wait == 25:
				var cur = _races[_race_idx]
				var host: Control = _main.get("host") as Control
				var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if bnode and is_instance_valid(bnode):
					var sim = bnode.get("sim")
					if sim != null:
						var p = sim.call("get_unit", "player")
						if p != null:
							p.rage = 100.0
					if bnode.has_method("_append_log"):
						bnode.call("_append_log", "[color=#1a4a75]%s 開局 T1 武器整備，滿怒 100%% 爆發！[/color]" % cur["name"])
						bnode.call("_append_log", "[color=#b24a00]%s 使出 %s！[/color]" % [cur["name"], cur["skill"]])
					if bnode.has_method("_flash_skill_banner"):
						bnode.call("_flash_skill_banner", cur["skill"], true)
			elif _wait >= 55:
				var cur = _races[_race_idx]
				_save_viewport(cur["file"], cur["tag"])
				_race_idx += 1
				if _race_idx < _races.size():
					_wait = 0
					_start_race_battle(_race_idx)
				else:
					_step = 2
					_wait = 0
		2:
			_finish()
			return true
	return false

func _setup_player_env(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var tut: Node = root.get_node_or_null("TutorialSystem")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("energy", 15)
		gs.set("gold", 2500)
		gs.set("stardust", 10)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
	if tut and tut.has_method("mark"):
		for k in ["boot", "explore", "battle_auto", "battle_parry", "battle_fog", "forge", "paths", "soul", "fort", "flag_hint", "ng"]:
			tut.call("mark", k)
	if sk and sk.has_method("ensure_skill_map"):
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")

func _start_race_battle(idx: int) -> void:
	var cur = _races[idx]
	_setup_player_env(cur["race"])
	if _main:
		_main.call("_start_battle_raw", cur["mode"])

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])

func _finish() -> void:
	print("CAPTURE_SHADOW_FIX: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
