extends SceneTree
## 戰鬥「停擺核的誘惑」彈窗多巴胺亮色盤實機截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_temptation_dopamine.gd

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/tempt_dopamine")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

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
			# 等待戰鬥畫面載入並呼叫 _show_temptation
			if _frame >= 25:
				var host: Control = _main.get("host") as Control
				var battle_node: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if battle_node and is_instance_valid(battle_node):
					if battle_node.has_method("_show_temptation"):
						battle_node.call("_show_temptation", {
							"stage": 1,
							"title": "力量",
							"text": "我給你力量。一擊劈開黑鏽。你的閣樓、你的同伴，瞬間安全。你不是過緊。你只是——效率。",
							"refuse_scale": 1.0,
						})
						_step = 2
						_frame = 0
		2:
			# 等待 15 幀讓彈窗所有文字、樣式、按鈕完整繪製更新
			if _frame >= 15:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_temptation_dopamine.png")
					var p2 := _proof_dir.path_join("proof_temptation_dopamine.png")
					img.save_png(p1)
					img.save_png(p2)
					print("SAVED_TEMPTATION_PROOF: ", p1, " & ", p2)

				print("TEMPTATION_DOPAMINE_CAPTURE_OK")
				quit(0)
				return true
	return false
