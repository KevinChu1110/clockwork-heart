extends SceneTree
## 依據任務 t_967c59f4 規範：
## 1. 截圖必須是 capture_*.gd framebuffer，不准 PIL 假圖（review.md 0-QA5/0-QA26）
## 2. OUT_DIR 只准寫入自己本輪 proofs（0-QA23，預設 proofs/t_967c59f4）
## 3. 橫屏 1280x720 畫面：英文、日文各一張「有機芯掉落卡的勝利結算」
##    - proof_01_en_victory_core_drop.png
##    - proof_02_ja_victory_core_drop.png
## 4. 英文圖零中日韓字元；日文圖無繁中殘留
## 5. 立即裝備／收下完成熱區高 >= 50px，多巴胺亮色盤，無系統 emoji

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const ContentLocClass := preload("res://scripts/systems/content_loc.gd")
const CoreSystemClass := preload("res://scripts/systems/core_system.gd")

var _step := 0
var _wait := 0
var _out_dir := ""
var _loc_node: Node = null
var _gs: Node = null
var _sdb: Node = null
var _battle: Node = null
var _victory_dlg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_out_dir = env_out
		else:
			_out_dir = ProjectSettings.globalize_path("res://../").path_join(env_out)
	else:
		_out_dir = ProjectSettings.globalize_path("res://../proofs/t_967c59f4")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行 t_967c59f4 機芯掉落結算卡六語系實機截圖 ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		# ──────────────────────────────────────────────────────────
		# 步驟 1: 英文 (en) 巨偶勝場機芯掉落結算卡片
		# ──────────────────────────────────────────────────────────
		1:
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "Xiaobai")
					_gs.set("level", 25)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")

				var dropped: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 47, "HP": 230})
				dropped["is_colossus"] = true
				_victory_dlg = BattleVictoryDialogScript.show_dialog(root, dropped, Callable(), 450, 60)
			elif _wait >= 35:
				var path := "%s/proof_01_en_victory_core_drop.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 2: 日文 (ja) 巨偶勝場機芯掉落結算卡片
		# ──────────────────────────────────────────────────────────
		2:
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				ContentLocClass.reload()
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "シロ")
					_gs.set("level", 25)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")

				var dropped: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 47, "HP": 230})
				dropped["is_colossus"] = true
				_victory_dlg = BattleVictoryDialogScript.show_dialog(root, dropped, Callable(), 450, 60)
			elif _wait >= 35:
				var path := "%s/proof_02_ja_victory_core_drop.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				# 恢復繁中
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數 2 張實機截圖完成 ──")
				quit(0)
				return true

	return false


func _save_screenshot(path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var tex := vp.get_texture()
		if tex:
			var img := tex.get_image()
			if img:
				img.save_png(path)
				print("  [Screenshot] 已儲存: %s (%dx%d)" % [path, img.get_width(), img.get_height()])
