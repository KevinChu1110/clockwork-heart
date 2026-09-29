extends SceneTree
## 探索性 QA 腳本：合併已過審的撼野牛/巡管守宮/重閘河馬官方資產套件三分支後實機驗收
## 輸出目錄：proofs/qa_t_2abac995/

const OUT_DIR := "res://../proofs/qa_t_2abac995"

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
	print("── 開始執行 QA 撼地野牛/巡管守宮/重閥河馬三族探索性實機截圖驗收 ──")
	print("輸出目錄: ", _resolved_out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# 1. DevPaperdollPreview bison
		1:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "bison")
					_current_node = p
			elif _wait >= 15:
				var path := "%s/proof_01_bison_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [1/9] 已截取撼地野牛 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		# 2. DevPaperdollPreview gecko
		2:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "gecko")
					_current_node = p
			elif _wait >= 15:
				var path := "%s/proof_02_gecko_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [2/9] 已截取巡管守宮 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		# 3. DevPaperdollPreview hippo
		3:
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "hippo")
					_current_node = p
			elif _wait >= 15:
				var path := "%s/proof_03_hippo_paperdoll.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [3/9] 已截取重閥河馬 7 槽位紙娃娃預覽: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		# 4. Battle scene bison
		4:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "bison")
					_gs.set("player_race", "bison")
					_gs.set("player_name", "撼地野牛")
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
						"damage": 88,
						"crit": true,
						"hp": 12,
						"max_hp": 100
					})
			elif _wait >= 20:
				var path := "%s/proof_04_bison_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [4/9] 已截取撼地野牛戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		# 5. Battle scene gecko
		5:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "gecko")
					_gs.set("player_race", "gecko")
					_gs.set("player_name", "巡管守宮")
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
						"damage": 55,
						"crit": true,
						"hp": 45,
						"max_hp": 100
					})
			elif _wait >= 20:
				var path := "%s/proof_05_gecko_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [5/9] 已截取巡管守宮戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		# 6. Battle scene hippo
		6:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "hippo")
					_gs.set("player_race", "hippo")
					_gs.set("player_name", "重閥河馬")
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
						"damage": 120,
						"crit": true,
						"hp": 0,
						"max_hp": 100
					})
			elif _wait >= 20:
				var path := "%s/proof_06_hippo_battle.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [6/9] 已截取重閥河馬戰鬥實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		# 7. Mobile lobby bison
		7:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "bison")
					_gs.set("player_race", "bison")
					_gs.set("player_name", "撼地野牛")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 20:
				var path := "%s/proof_07_bison_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [7/9] 已截取撼地野牛手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 8
				_wait = 0

		# 8. Mobile lobby gecko
		8:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "gecko")
					_gs.set("player_race", "gecko")
					_gs.set("player_name", "巡管守宮")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 20:
				var path := "%s/proof_08_gecko_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [8/9] 已截取巡管守宮手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		# 9. Mobile lobby hippo
		9:
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "hippo")
					_gs.set("player_race", "hippo")
					_gs.set("player_name", "重閥河馬")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 20:
				var path := "%s/proof_09_hippo_lobby.png" % _resolved_out_dir
				_save_screenshot(path)
				print("  ✓ [9/9] 已截取重閥河馬手遊大廳實機: ", path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				print("🎉 探索性 QA 實機截圖完成！全部 9 張實機截圖已輸出至: ", _resolved_out_dir)
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
	if img == null:
		push_error("Failed to get image from viewport")
		return
	var err := img.save_png(target_path)
	if err != OK:
		push_error("Failed to save png to " + target_path)
