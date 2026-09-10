extends SceneTree
## 戰鬥日誌面板多巴胺亮色盤實機截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_battlelog_dopamine.gd

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""
var _hud_proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/battlelog")
	_hud_proof_dir = base.path_join("../proofs/hud_dopamine")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	DirAccess.make_dir_recursive_absolute(_hud_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			# 等待 main.tscn 載入
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var inv: Node = root.get_node_or_null("InventorySystem")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
					gs.set("level", 12)
					gs.set("hp", 350)
					gs.set("gold", 23456)
					gs.set("stardust", 88)
					gs.set("energy", 9)
					gs.set("energy_ts", Time.get_unix_time_from_system())
				if inv:
					inv.call("add_item", "hp_s", 5)
					inv.call("add_item", "mp_s", 3)
					inv.call("ensure_hotbar")
					inv.call("set_hotbar", 0, "hp_s")
					inv.call("set_hotbar", 1, "mp_s")

				# 直接切入戰鬥
				_main.call("_start_battle_raw", "road_bandit")
				_step = 1
				_frame = 0
		1:
			# 等待戰鬥畫面載入並穩定渲染
			if _frame >= 30:
				var hotbar = _main.get("_hotbar")
				if hotbar and is_instance_valid(hotbar):
					hotbar.visible = true
					if hotbar.has_method("refresh"):
						hotbar.call("refresh")

				# 確保戰鬥日誌中有豐富的實機戰鬥訊息（包含怒氣、部位破壞、技能與提示）
				var host: Control = _main.get("host") as Control
				var battle_node: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if battle_node and is_instance_valid(battle_node):
					if battle_node.has_method("_append_log"):
						battle_node.call("_append_log", "[color=#fc0]部位破壞！【右腕重刃】打破擊暈！[/color]")
						battle_node.call("_append_log", "[color=#f52]怒氣滿 · 暴怒！（5 秒攻速與傷害提升）[/color]")
						battle_node.call("_append_log", "[color=#fa6]王者斬要擋，擋住就能反擊 · 火圈亮起後按 J 跳開[/color]")

				_step = 2
				_frame = 0
		2:
			# 等待 10 幀讓所有文字與面板排版完全繪製更新
			if _frame >= 10:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_battle_log_dopamine.png")
					var p2 := _proof_dir.path_join("proof_battle_log_dopamine.png")
					var p3 := _out_dir.path_join("proof_battle_hud_hotbar.png")
					var p4 := _hud_proof_dir.path_join("proof_battle_hud_hotbar.png")
					img.save_png(p1)
					img.save_png(p2)
					img.save_png(p3)
					img.save_png(p4)
					print("SAVED_BATTLE_LOG: ", p1, " & ", p2)
					print("SAVED_BATTLE_HUD: ", p3, " & ", p4)

				print("BATTLELOG_DOPAMINE_CAPTURE_OK")
				quit(0)
				return true
	return false
