extends SceneTree
## §8 標準場：錄「探索→戰鬥→拆一個部位」驗收演出腳本
## S1 探索 (0~4.5s) → S2 進戰 (4.5~8.0s) → S3 預告/交手 (8.0~13.0s) → S4 拆部位 (13.0~18.0s) → S5 收束 (18.0~22.0s)

var _elapsed: float = 0.0
var _step: int = 0
var _step_timer: float = 0.0
var _main: Node = null
var _battle: Control = null
var _sim = null
var _out_dir: String = ""

var _shot01_taken: bool = false
var _shot02_taken: bool = false
var _shot03_taken: bool = false
var _shot04_taken: bool = false
var _shot05_taken: bool = false

var _part_broken_triggered: bool = false
var _telegraph_triggered: bool = false
var _clash_triggered: bool = false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	Engine.max_fps = 30
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../交付/標準場-§8")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var alt_dir := ProjectSettings.globalize_path("res://").path_join("../delivery/standard_scene_s8")
	DirAccess.make_dir_recursive_absolute(alt_dir)
	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	_step_timer += delta

	match _step:
		0:
			# 初始化並切入探索
			if current_scene != null and current_scene.has_method("proof_jump_explore"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_race", "rabbit")
					gs.set("player_name", "小白")
					gs.set("level", 12)
					gs.set("gold", 1200)
					gs.set("weapon_name", "微末之刃")
					gs.set("weapon_tier", 2)
					gs.set("weapon_atk", 45)
					gs.set("hp", 200)
					gs.set("max_hp", 200)
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)
				var es: Node = root.get_node_or_null("EnergySystem")
				if es and es.has_method("grant"):
					es.call("grant", 15)
				_main.call("proof_jump_explore", "town")
				_step = 1
				_step_timer = 0.0
				print("[S8_SCENE] S1: 探索開始 (t=%.2fs)" % _elapsed)

		1:
			# S1 探索 (0.0s ~ 4.5s)：小白在亮色日常域 (town) 走動與待機
			if _step_timer >= 1.2 and _step_timer < 1.4:
				if _main.get("_explore") and is_instance_valid(_main.get("_explore")):
					var exp_v: Node = _main.get("_explore")
					if exp_v.has_method("play_action_pose"):
						exp_v.call("play_action_pose", "walk", 0.6)
			if not _shot01_taken and _step_timer >= 2.5:
				_capture("shot_01.png")
				_shot01_taken = true
				print("[S8_SCENE] S1: 截圖 shot_01.png (t=%.2fs)" % _elapsed)
			if _step_timer >= 4.5:
				print("[S8_SCENE] S2: 進戰開始 (t=%.2fs)" % _elapsed)
				_main.call("_start_battle_raw", "leo")
				_step = 2
				_step_timer = 0.0

		2:
			# S2 進戰 (4.5s ~ 8.0s)：切入戰鬥 (雷歐)，站位乾淨、奶油HUD、果凍鈕、無Emoji
			var host: Node = _main.get("host") if _main else null
			if host and host.get_child_count() > 0:
				_battle = host.get_child(host.get_child_count() - 1) as Control
				if _battle and _battle.is_inside_tree() and _battle.get("sim"):
					_sim = _battle.get("sim")
					_sim.set("hazard_kind", "")
					if not _shot02_taken and _step_timer >= 2.2:
						_capture("shot_02.png")
						_shot02_taken = true
						print("[S8_SCENE] S2: 截圖 shot_02.png (t=%.2fs)" % _elapsed)
					if _step_timer >= 3.2:
						_step = 3
						_step_timer = 0.0
						print("[S8_SCENE] S3: 預告/交手開始 (t=%.2fs)" % _elapsed)

		3:
			# S3 預告／交手 (8.0s ~ 13.0s)：預告圈/格擋倒數 + 受擊糖果色碎屑與黃銅齒輪片
			if _sim and _battle:
				var leo = _sim.call("get_unit", "leo")
				if not _telegraph_triggered and _step_timer >= 0.5:
					_telegraph_triggered = true
					if leo:
						leo.set("telegraph_active", true)
						leo.set("state_timer", 2.0)
						_battle.call("_set_boss_pose", "telegraph")
						var countdown_lbl: Label = _battle.get("countdown")
						if countdown_lbl:
							countdown_lbl.visible = true
							countdown_lbl.text = "格擋"
				if not _clash_triggered and _step_timer >= 1.5:
					_clash_triggered = true
					_battle.call("_spawn_hit_fx", "leo", "slash_arc")
					_battle.call("_spawn_float", "leo", "CRIT！85", Color("#FFD028"), false, true)
				if not _shot03_taken and _step_timer >= 2.2:
					_capture("shot_03.png")
					_shot03_taken = true
					print("[S8_SCENE] S3: 截圖 shot_03.png (t=%.2fs)" % _elapsed)
				if _step_timer >= 4.5:
					_step = 4
					_step_timer = 0.0
					print("[S8_SCENE] S4: 拆部位開始 (t=%.2fs)" % _elapsed)

		4:
			# S4 拆部位 (13.0s ~ 18.0s)：
			# ① 部位閃邊 → ② 裂縫 → ③ 零件飛出 → ④ 獎勵欄出現對應圖示
			if _sim and _battle:
				var leo = _sim.call("get_unit", "leo")
				if not _part_broken_triggered and _step_timer >= 0.5:
					_part_broken_triggered = true
					if leo:
						leo.set("telegraph_active", false)
						leo.set("hp", int(float(leo.get("max_hp")) * 0.6))
						_sim.set("parts_break_unlocked", true)
						_sim.set("parts_break_stage", 1)
						_sim.set("focus_part_id", "helm")
						_sim.call("_process_part_damage", leo, 999, true)
						print("[S8_SCENE] S4: 觸發 _process_part_damage 破壞獅衛重盔")
				if not _shot04_taken and _step_timer >= 1.8:
					_capture("shot_04.png")
					_shot04_taken = true
					print("[S8_SCENE] S4: 截圖 shot_04.png (t=%.2fs)" % _elapsed)
				if _step_timer >= 5.0:
					_step = 5
					_step_timer = 0.0
					print("[S8_SCENE] S5: 收束結算開始 (t=%.2fs)" % _elapsed)

		5:
			# S5 收束 (18.0s ~ 22.0s)：小白仍可辨、體力／發條顯示仍在 (15點胸口光芒＋刻度)、獎勵欄在場
			if not _shot05_taken and _step_timer >= 1.8:
				_capture("shot_05.png")
				_shot05_taken = true
				print("[S8_SCENE] S5: 截圖 shot_05.png (t=%.2fs)" % _elapsed)
			if _step_timer >= 3.5:
				print("[S8_SCENE] 全部 5 階段演出完成！(總時長=%.2fs)" % _elapsed)
				quit(0)

	return false

func _capture(filename: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img := vp.get_texture().get_image()
		if img and not img.is_empty():
			var p1 := _out_dir.path_join(filename)
			img.save_png(p1)
			var alt_dir := ProjectSettings.globalize_path("res://").path_join("../delivery/standard_scene_s8")
			var p2 := alt_dir.path_join(filename)
			img.save_png(p2)
			print("[S8_SCENE] SAVED: %s" % filename)
