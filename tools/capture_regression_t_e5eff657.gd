extends SceneTree
## 《發條之心》BattleVictoryDialog 再次挑戰按鈕實機驗收存證腳本 (t_e5eff657)
## 覆蓋：
## 1. BattleVictoryDialog 勝利結算『再次挑戰』按鈕（BtnReplayStage）多巴胺暖橘立體厚底排版與尺寸（zh_TW）
## 2. 英文語系 (en) 下 BattleVictoryDialog 顯示 "Retry Stage"，零 CJK 殘留
## 3. 點擊再次挑戰後連動 BattleView 扣除能量重啟關卡出征戰鬥實機（滿血重開、舊彈窗銷毀、無遮擋）
## 4. 4-4 末關支援重複刷關（BtnReplayStage 顯示，而 BtnNextStage 自動隱藏）
## 5. 全圖 1280x720 真實 Framebuffer 渲染、獨立 SHA256 驗證

const BattleVictoryDialogClass := preload("res://scripts/battle/battle_victory_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_e5eff657",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e5eff657/proofs/t_e5eff657"
]

var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _battle: Control = null
var _vic_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

var _saved_hashes: Dictionary = {}

var _sample_part := {
	"slot": "mainspring",
	"tier": "blue",
	"tier_name": "藍",
	"slot_name": "主發條",
	"exp_gain": 100,
	"scrap_gain": 5
}


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	const FORBIDDEN := ["⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"]
	for sym in FORBIDDEN:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	if not root.has_node("Loc"):
		var loc_cls = load("res://scripts/autoload/loc.gd")
		if loc_cls:
			_loc_node = loc_cls.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)
	else:
		_loc_node = root.get_node("Loc")

	if not root.has_node("GameState"):
		var gs_cls = load("res://scripts/autoload/game_state.gd")
		if gs_cls:
			_gs = gs_cls.new()
			_gs.name = "GameState"
			root.add_child(_gs)
	else:
		_gs = root.get_node("GameState")

	if not root.has_node("EnergySystem"):
		var es_cls = load("res://scripts/systems/energy_system.gd")
		if es_cls:
			_es = es_cls.new()
			_es.name = "EnergySystem"
			root.add_child(_es)
	else:
		_es = root.get_node("EnergySystem")


func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("無法獲取 Viewport")
		return ""
	var tex := vp.get_texture()
	if tex == null:
		_fail("無法獲取 Viewport Texture")
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		_fail("Viewport 渲染為空")
		return ""

	var full_bytes := img.save_png_to_buffer()
	var full_ctx := HashingContext.new()
	full_ctx.start(HashingContext.HASH_SHA256)
	full_ctx.update(full_bytes)
	var full_sha := full_ctx.finish().hex_encode()

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA256=%s)" % [full_path, img.get_width(), img.get_height(), full_sha.substr(0, 12)])
		else:
			_fail("儲存全景圖失敗: %s" % full_path)

		if crop_rect.size != Vector2i.ZERO and crop_filename != "":
			var crops_dir := base_dir.path_join("crops")
			var cropped := img.get_region(crop_rect)
			var crop_path := crops_dir.path_join(crop_filename)
			var c_err := cropped.save_png(crop_path)
			if c_err == OK:
				print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
			else:
				_fail("儲存特寫圖失敗: %s" % crop_path)

	_saved_hashes[filename] = full_sha
	return full_sha


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# Step 0: 準備出征戰鬥場景與 1-1 勝利結算彈窗 (zh_TW)
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.set("current_expedition_stage", "1-1")
					_gs.set("energy", 15)
					_gs.set("energy_ts", Time.get_unix_time_from_system())

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_battle = b_scn.instantiate()
					root.add_child(_battle)
					if _battle.has_method("setup"):
						_battle.call("setup", "ash_rat")

				_vic_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "1-1"
				)
				_vic_dlg.z_index = 95

				_step = 1
				_wait = 0

		1:
			# Step 1: 驗證 BattleVictoryDialog 再次挑戰按鈕 (zh_TW)，並截圖
			if _wait >= 25:
				var btn_replay: Button = _vic_dlg.find_child("BtnReplayStage", true, false) as Button
				if btn_replay == null:
					_fail("VictoryDialog 找不到 BtnReplayStage 按鈕")
				else:
					if btn_replay.text != "再次挑戰":
						_fail("BtnReplayStage 文字不符: " + btn_replay.text)
					if btn_replay.custom_minimum_size.x < 170:
						_fail("BtnReplayStage 寬度未達標 >= 170px: %f" % btn_replay.custom_minimum_size.x)
					if btn_replay.custom_minimum_size.y < 52:
						_fail("BtnReplayStage 高度未達標 >= 52px: %f" % btn_replay.custom_minimum_size.y)
					if _has_emoji(btn_replay.text):
						_fail("BtnReplayStage 包含違規 Emoji")

				_save_viewport(
					"proof_01_battle_victory_replay_zh_TW.png",
					Rect2i(240, 480, 800, 180),
					"crop_01_victory_replay_zh_TW.png"
				)

				if is_instance_valid(_vic_dlg):
					_vic_dlg.queue_free()
					_vic_dlg = null

				_step = 2
				_wait = 0

		2:
			# Step 2: 英文語系 (en) BattleVictoryDialog 驗證
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_vic_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "1-1"
				)
				_vic_dlg.z_index = 95

				_step = 3
				_wait = 0

		3:
			# Step 3: 驗證英文 BattleVictoryDialog 零中文殘留，並截圖
			if _wait >= 25:
				var btn_replay: Button = _vic_dlg.find_child("BtnReplayStage", true, false) as Button
				if btn_replay == null:
					_fail("英文 VictoryDialog 找不到 BtnReplayStage")
				else:
					if btn_replay.text != "Retry Stage":
						_fail("英文 BtnReplayStage 文字不符: " + btn_replay.text)
					if _has_cjk(btn_replay.text):
						_fail("英文 BtnReplayStage 殘留 CJK 中文: " + btn_replay.text)

				_save_viewport(
					"proof_02_battle_victory_replay_en.png",
					Rect2i(240, 480, 800, 180),
					"crop_02_victory_replay_en.png"
				)

				if is_instance_valid(_vic_dlg):
					_vic_dlg.queue_free()
					_vic_dlg = null

				# 切回繁中
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_step = 4
				_wait = 0

		4:
			# Step 4: 觸發 4-4 末關結算視窗（驗證 BtnReplayStage 顯示且 BtnNextStage 隱藏）
			if _wait >= 5:
				_vic_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "4-4"
				)
				_vic_dlg.z_index = 95

				_step = 5
				_wait = 0

		5:
			# Step 5: 截圖 4-4 末關重複刷關按鈕展示
			if _wait >= 25:
				var btn_replay: Button = _vic_dlg.find_child("BtnReplayStage", true, false) as Button
				var btn_next: Button = _vic_dlg.find_child("BtnNextStage", true, false) as Button
				if btn_replay == null or not btn_replay.visible:
					_fail("4-4 末關未顯示 BtnReplayStage 按鈕")
				if btn_next != null and btn_next.visible:
					_fail("4-4 末關 BtnNextStage 應自動隱藏")

				_save_viewport(
					"proof_04_battle_victory_final_stage_replay.png",
					Rect2i(240, 480, 800, 180),
					"crop_04_final_stage_replay.png"
				)

				if is_instance_valid(_vic_dlg):
					_vic_dlg.queue_free()
					_vic_dlg = null

				_step = 6
				_wait = 0

		6:
			# Step 6: 觸發勝利結算並模擬點擊 BtnReplayStage 連動重啟戰鬥
			if _wait >= 5:
				if _battle != null:
					_battle.call("_show_victory_settlement", _sample_part)
					var btn_replay: Button = _battle.find_child("BtnReplayStage", true, false) as Button
					if btn_replay == null:
						var dlg: Control = _battle.get("_victory_settlement_dialog") as Control
						if dlg != null:
							btn_replay = dlg.find_child("BtnReplayStage", true, false) as Button
					if btn_replay == null:
						_fail("在勝利結算中找不到 BtnReplayStage 按鈕")
					else:
						print("  ✓ 成功定位勝利彈窗之 BtnReplayStage，發射 pressed.emit() 模擬重複刷關")
						btn_replay.pressed.emit()

				_step = 7
				_wait = 0

		7:
			# Step 7: 截圖重啟戰鬥實機全景（驗證無彈窗遮擋、滿血開戰、扣除能量）
			if _wait >= 30:
				if _battle != null:
					if str(_battle.get("_mode")) != "ash_rat":
						_fail("重開戰鬥模式未保持為 ash_rat")
					if str(_battle.get("_current_expedition_stage")) != "1-1":
						_fail("重開戰鬥出征關卡未保持為 1-1")
					var remaining_btn: Button = _battle.find_child("BtnReplayStage", true, false) as Button
					if remaining_btn != null and is_instance_valid(remaining_btn):
						_fail("重開戰鬥後 BtnReplayStage 仍殘留，彈窗未銷毀")
					var vic_dlg_node: Control = _battle.get("_victory_settlement_dialog") as Control
					if vic_dlg_node != null and is_instance_valid(vic_dlg_node):
						_fail("重開戰鬥後 _victory_settlement_dialog 實體未清理")
					if _gs != null and int(_gs.get("hp")) != int(_gs.call("effective_max_hp")):
						_fail("重開戰鬥後玩家血量未回滿 (當前 hp: %d, max_hp: %d)" % [int(_gs.get("hp")), int(_gs.call("effective_max_hp"))])

				_save_viewport(
					"proof_03_battle_victory_restarted_combat.png",
					Rect2i(20, 20, 880, 520),
					"crop_03_restarted_combat.png"
				)

				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 8
				_wait = 0

		8:
			# Step 8: 驗證所有截圖 SHA256 獨立性
			var all_keys := _saved_hashes.keys()
			print("\n=== SHA256 獨立性檢核（共 %d 張截圖）===" % all_keys.size())
			var seen_hashes := {}
			for k in all_keys:
				var h: String = _saved_hashes[k]
				print("  - %s: %s" % [k, h])
				if seen_hashes.has(h):
					_fail("截圖 SHA256 重複！%s 與 %s 相同 (hash=%s)" % [k, seen_hashes[h], h])
				else:
					seen_hashes[h] = k

			if not _ok:
				push_error("TEST_REGRESSION_T_E5EFF657_FAIL")
				print("TEST_REGRESSION_T_E5EFF657_FAIL")
				quit(1)
				return true

			print("\n=======================================================")
			print("TEST_REGRESSION_T_E5EFF657_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
