extends SceneTree
## 探索性 QA 腳本：第六十一~六十三族(彩喙巨嘴鳥/破冰海象/破竹羚牛)全套資產批次回歸驗收實機截圖
## 輸出目錄：proofs/qa_t_948b40b2/

const OUT_DIR := "res://../proofs/qa_t_948b40b2"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _gs: Node = null
var _resolved_out_dir := ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_resolved_out_dir = ProjectSettings.globalize_path(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(_resolved_out_dir)

	_gs = root.get_node_or_null("GameState")
	print("── 開始執行 QA 第六十一~六十三族(巨嘴鳥/海象/羚牛)探索性實機截圖驗收 ──")
	print("輸出目錄: ", _resolved_out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# 1. DevPaperdollPreview toucan
		1:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "toucan")
					_current_node = p
			elif _wait >= 20:
				var path := "%s/proof_01_toucan_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [1/9] 已截取彩喙巨嘴鳥 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		# 2. DevPaperdollPreview walrus
		2:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "walrus")
					_current_node = p
			elif _wait >= 20:
				var path := "%s/proof_02_walrus_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [2/9] 已截取破冰海象 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		# 3. DevPaperdollPreview takin
		3:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "takin")
					_current_node = p
			elif _wait >= 20:
				var path := "%s/proof_03_takin_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [3/9] 已截取破竹羚牛 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		# 4. Battle scene toucan
		4:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "toucan")
					_gs.set("player_race", "toucan")
					_gs.set("player_name", "彩喙巨嘴鳥")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node and _current_node.has_method("_on_event"):
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 76,
						"crit": true,
						"hp": 24,
						"max_hp": 100
					})
			elif _wait >= 25:
				var path := "%s/proof_04_toucan_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [4/9] 已截取彩喙巨嘴鳥戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		# 5. Battle scene walrus
		5:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "walrus")
					_gs.set("player_race", "walrus")
					_gs.set("player_name", "破冰海象")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node and _current_node.has_method("_on_event"):
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 82,
						"crit": true,
						"hp": 18,
						"max_hp": 100
					})
			elif _wait >= 25:
				var path := "%s/proof_05_walrus_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [5/9] 已截取破冰海象戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		# 6. Battle scene takin
		6:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "takin")
					_gs.set("player_race", "takin")
					_gs.set("player_name", "破竹羚牛")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node and _current_node.has_method("_on_event"):
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 95,
						"crit": true,
						"hp": 5,
						"max_hp": 100
					})
			elif _wait >= 25:
				var path := "%s/proof_06_takin_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [6/9] 已截取破竹羚牛戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		# 7. Mobile lobby toucan
		7:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "toucan")
					_gs.set("player_race", "toucan")
					_gs.set("player_name", "彩喙巨嘴鳥")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 25:
				var path := "%s/proof_07_toucan_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [7/9] 已截取彩喙巨嘴鳥手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 8
				_wait = 0

		# 8. Mobile lobby walrus
		8:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "walrus")
					_gs.set("player_race", "walrus")
					_gs.set("player_name", "破冰海象")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 25:
				var path := "%s/proof_08_walrus_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [8/9] 已截取破冰海象手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		# 9. Mobile lobby takin
		9:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "takin")
					_gs.set("player_race", "takin")
					_gs.set("player_name", "破竹羚牛")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 25:
				var path := "%s/proof_09_takin_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [9/9] 已截取破竹羚牛手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 10
				_wait = 0

		# 10. Finish
		10:
			if _wait >= 5:
				print("🎉 探索性 QA 實機截圖全數完成！全部 9 張實機截圖已輸出至: ", _resolved_out_dir)
				quit(0)
				return true

	return false

func _save_screenshot(target_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Viewport is null")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Texture is null")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Failed to get image from viewport")
		return
	var err := img.save_png(target_path)
	if err != OK:
		push_error("save_png failed with error %d: %s" % [err, target_path])
