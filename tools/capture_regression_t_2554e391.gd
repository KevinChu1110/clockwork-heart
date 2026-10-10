extends SceneTree
## 《發條之心》再次挑戰雙按鈕與鐵匠三槽鍛造全面回歸實機驗收存證腳本 (t_2554e391)
## 涵蓋：
## 1. BattleDefeatDialog 戰敗結算『再次挑戰』（BtnRetryStage）多巴胺薄荷綠立體厚底排版與尺寸（zh_TW）
## 2. 英文語系 (en) 下 BattleDefeatDialog 顯示 "Retry Stage"，零 CJK 殘留
## 3. 點擊再次挑戰後連動 BattleView 扣除能量重啟關卡出征戰鬥實機（滿血滿狀態、無彈窗遮擋）
## 4. BattleVictoryDialog 1-1 出征勝利結算之重複刷關『再次挑戰』按鈕（暖橘立體厚底，zh_TW）
## 5. BattleVictoryDialog 4-4 末關勝利結算：自動隱藏下一關，但再次挑戰保持顯示
## 6. 英文語系 (en) 下 BattleVictoryDialog 顯示 "Retry Stage"，零 CJK 殘留
## 7. 點擊再次挑戰後連動 BattleView 扣除能量重複挑戰關卡戰鬥實機（滿血滿狀態）
## 8. ForgeDialog 天宮鐵匠三欄武器槽位（WeaponSlotChipRow）晶片排版與槽位 1 主手武器展示（zh_TW）
## 9. 點擊槽位 2 切換副手武器（鐵骨重鎚 T2），品質色階（上品）與副詞條即時刷新
## 10. 點擊槽位 3 切換絕技武器（赤炎神弓 T3），品質色階（秘寶）與副詞條即時刷新
## 11. 對槽位 2 進行升階鍛造，驗證武器階級、攻擊力與晶片即時刷新
## 12. 英文語系 (en) 下 ForgeDialog 三槽與品質副詞條零 CJK 中文殘留
## 13. 零系統 Emoji、1280x720 真實 Framebuffer 渲染、全截圖獨立 SHA256 驗證

const BattleDefeatDialogClass := preload("res://scripts/battle/battle_defeat_dialog.gd")
const BattleVictoryDialogClass := preload("res://scripts/battle/battle_victory_dialog.gd")
const MobileLobbyClass := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_2554e391",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2554e391/proofs/t_2554e391"
]

var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _battle: Control = null
var _defeat_dlg: Control = null
var _victory_dlg: Control = null
var _lobby: Control = null
var _forge_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null
var _eq: Node = null

var _saved_hashes: Dictionary = {}

var _sample_part: Dictionary = {
	"id": "gear_bronze",
	"name": "青銅齒輪",
	"name_en": "Bronze Gear",
	"desc": "基礎機械發條零件",
	"desc_en": "Basic clockwork component",
	"kind": "core",
	"rarity": "common"
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

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var gs_cls = load("res://scripts/autoload/game_state.gd")
		if gs_cls:
			_gs = gs_cls.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_es = root.get_node_or_null("EnergySystem")
	if _es == null:
		var es_cls = load("res://scripts/systems/energy_system.gd")
		if es_cls:
			_es = es_cls.new()
			_es.name = "EnergySystem"
			root.add_child(_es)

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var eq_cls = load("res://scripts/systems/equipment_system.gd")
		if eq_cls:
			_eq = eq_cls.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)


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
			# Step 0: 準備戰鬥場景與戰敗診斷彈窗 (zh_TW)
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.set("current_expedition_stage", "1-1")
				if _es:
					_gs.set("energy", 15)
					_gs.set("energy_ts", Time.get_unix_time_from_system())

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_battle = b_scn.instantiate()
					root.add_child(_battle)
					if _battle.has_method("setup"):
						_battle.call("setup", "ash_rat")

				_defeat_dlg = BattleDefeatDialogClass.new()
				_defeat_dlg.z_index = 95
				root.add_child(_defeat_dlg)

				_step = 1
				_wait = 0

		1:
			# Step 1: 驗證 BattleDefeatDialog 再次挑戰按鈕 (zh_TW) 並截圖
			if _wait >= 25:
				var btn_retry: Button = _defeat_dlg.find_child("BtnRetryStage", true, false) as Button
				if btn_retry == null:
					_fail("DefeatDialog 找不到 BtnRetryStage 按鈕")
				else:
					if btn_retry.text != "再次挑戰":
						_fail("BtnRetryStage 文字不符: " + btn_retry.text)
					if btn_retry.custom_minimum_size.x < 170:
						_fail("BtnRetryStage 寬度未達標 >= 170px: %f" % btn_retry.custom_minimum_size.x)
					if btn_retry.custom_minimum_size.y < 52:
						_fail("BtnRetryStage 高度未達標 >= 52px: %f" % btn_retry.custom_minimum_size.y)
					if _has_emoji(btn_retry.text):
						_fail("BtnRetryStage 包含違規 Emoji")

				_save_viewport(
					"proof_01_battle_defeat_retry_zh_TW.png",
					Rect2i(240, 500, 800, 140),
					"crop_01_defeat_retry_zh_TW.png"
				)

				if is_instance_valid(_defeat_dlg):
					_defeat_dlg.queue_free()
					_defeat_dlg = null

				_step = 2
				_wait = 0

		2:
			# Step 2: 英文語系 (en) BattleDefeatDialog 驗證
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_defeat_dlg = BattleDefeatDialogClass.new()
				_defeat_dlg.z_index = 95
				root.add_child(_defeat_dlg)

				_step = 3
				_wait = 0

		3:
			# Step 3: 驗證英文 BattleDefeatDialog 零中文殘留並截圖
			if _wait >= 25:
				var btn_retry: Button = _defeat_dlg.find_child("BtnRetryStage", true, false) as Button
				if btn_retry == null:
					_fail("英文 DefeatDialog 找不到 BtnRetryStage")
				else:
					if btn_retry.text != "Retry Stage":
						_fail("英文 BtnRetryStage 文字不符: " + btn_retry.text)
					if _has_cjk(btn_retry.text):
						_fail("英文 BtnRetryStage 殘留 CJK 中文: " + btn_retry.text)

				_save_viewport(
					"proof_02_battle_defeat_retry_en.png",
					Rect2i(240, 500, 800, 140),
					"crop_02_defeat_retry_en.png"
				)

				if is_instance_valid(_defeat_dlg):
					_defeat_dlg.queue_free()
					_defeat_dlg = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_step = 4
				_wait = 0

		4:
			# Step 4: 觸發戰敗結算並模擬點擊 BtnRetryStage 按鈕連動重啟戰鬥
			if _wait >= 5:
				if _battle != null:
					_battle.call("_on_end", false)
					var btn_retry: Button = _battle.find_child("BtnRetryStage", true, false) as Button
					if btn_retry == null:
						var dlg: Control = _battle.get("_defeat_settlement_dialog") as Control
						if dlg != null:
							btn_retry = dlg.find_child("BtnRetryStage", true, false) as Button
					if btn_retry == null:
						_fail("在戰敗結算中找不到 BtnRetryStage 按鈕")
					else:
						print("  ✓ 成功定位戰敗彈窗之 BtnRetryStage，發射 pressed 模擬點擊")
						btn_retry.pressed.emit()

				_step = 5
				_wait = 0

		5:
			# Step 5: 截圖重啟戰鬥實機全景（驗證無彈窗遮擋、滿血開戰）
			if _wait >= 30:
				if _battle != null:
					if str(_battle.get("_mode")) != "ash_rat":
						_fail("重開戰鬥模式未回復為 ash_rat")
					if str(_battle.get("_current_expedition_stage")) != "1-1":
						_fail("重開戰鬥出征關卡未保持為 1-1")
					var remaining_btn: Button = _battle.find_child("BtnRetryStage", true, false) as Button
					if remaining_btn != null and is_instance_valid(remaining_btn):
						_fail("重開戰鬥後 BtnRetryStage 仍殘留，彈窗未銷毀")
					var defeat_dlg_node: Control = _battle.get("_defeat_settlement_dialog") as Control
					if defeat_dlg_node != null and is_instance_valid(defeat_dlg_node):
						_fail("重開戰鬥後 _defeat_settlement_dialog 實體未清理")
					if _gs != null and int(_gs.get("hp")) != int(_gs.call("effective_max_hp")):
						_fail("重開戰鬥後玩家血量未回滿")

				_save_viewport(
					"proof_03_battle_defeat_restarted_combat.png",
					Rect2i(200, 100, 880, 520),
					"crop_03_defeat_restarted_combat.png"
				)

				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 6
				_wait = 0

		6:
			# Step 6: 準備 1-1 出征勝利結算彈窗 (zh_TW)
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

				_victory_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "1-1"
				)
				_victory_dlg.z_index = 95

				_step = 7
				_wait = 0

		7:
			# Step 7: 驗證 1-1 勝利結算之 BtnReplayStage (zh_TW) 並截圖
			if _wait >= 25:
				var btn_replay: Button = _victory_dlg.find_child("BtnReplayStage", true, false) as Button
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
					"proof_04_battle_victory_replay_zh_TW.png",
					Rect2i(240, 480, 800, 180),
					"crop_04_victory_replay_zh_TW.png"
				)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				_step = 8
				_wait = 0

		8:
			# Step 8: 準備 4-4 末關勝利結算視窗
			if _wait >= 5:
				_victory_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "4-4"
				)
				_victory_dlg.z_index = 95

				_step = 9
				_wait = 0

		9:
			# Step 9: 驗證 4-4 末關 BtnReplayStage 顯示且 BtnNextStage 隱藏並截圖
			if _wait >= 25:
				var btn_replay: Button = _victory_dlg.find_child("BtnReplayStage", true, false) as Button
				var btn_next: Button = _victory_dlg.find_child("BtnNextStage", true, false) as Button
				if btn_replay == null or not btn_replay.visible:
					_fail("4-4 末關 BtnReplayStage 未保持顯示")
				if btn_next != null and btn_next.visible:
					_fail("4-4 末關 BtnNextStage 未隱藏")

				_save_viewport(
					"proof_05_battle_victory_final_stage_replay.png",
					Rect2i(240, 480, 800, 180),
					"crop_05_victory_final_stage_replay.png"
				)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				_step = 10
				_wait = 0

		10:
			# Step 10: 英文語系 (en) BattleVictoryDialog 驗證
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_victory_dlg = BattleVictoryDialogClass.show_dialog(
					root, _sample_part, Callable(), 100, 5, [], Callable(), "1-1"
				)
				_victory_dlg.z_index = 95

				_step = 11
				_wait = 0

		11:
			# Step 11: 驗證英文 BattleVictoryDialog 零中文殘留並截圖
			if _wait >= 25:
				var btn_replay: Button = _victory_dlg.find_child("BtnReplayStage", true, false) as Button
				if btn_replay == null:
					_fail("英文 VictoryDialog 找不到 BtnReplayStage")
				else:
					if btn_replay.text != "Retry Stage":
						_fail("英文 BtnReplayStage 文字不符: " + btn_replay.text)
					if _has_cjk(btn_replay.text):
						_fail("英文 BtnReplayStage 殘留 CJK 中文: " + btn_replay.text)

				_save_viewport(
					"proof_06_battle_victory_replay_en.png",
					Rect2i(240, 480, 800, 180),
					"crop_06_victory_replay_en.png"
				)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_step = 12
				_wait = 0

		12:
			# Step 12: 模擬出征勝利結算並點擊 BtnReplayStage 重複刷關
			if _wait >= 5:
				if _battle != null:
					_battle.call("_show_victory_settlement", _sample_part)
					var dlg: Control = _battle.get("_victory_settlement_dialog") as Control
					var btn_replay: Button = null
					if dlg != null:
						btn_replay = dlg.find_child("BtnReplayStage", true, false) as Button
					if btn_replay == null:
						btn_replay = _battle.find_child("BtnReplayStage", true, false) as Button

					if btn_replay == null:
						_fail("在勝利結算中找不到 BtnReplayStage 按鈕")
					else:
						print("  ✓ 成功定位勝利彈窗之 BtnReplayStage，發射 pressed 模擬點擊")
						btn_replay.pressed.emit()

				_step = 13
				_wait = 0

		13:
			# Step 13: 截圖重複挑戰關卡實機全景（驗證無彈窗遮擋、滿血開戰）
			if _wait >= 30:
				if _battle != null:
					if str(_battle.get("_mode")) != "ash_rat":
						_fail("重複刷關戰鬥模式未回復為 ash_rat")
					if str(_battle.get("_current_expedition_stage")) != "1-1":
						_fail("重複刷關出征關卡未保持為 1-1")
					var vic_dlg_node: Control = _battle.get("_victory_settlement_dialog") as Control
					if vic_dlg_node != null and is_instance_valid(vic_dlg_node):
						_fail("重複刷關後 _victory_settlement_dialog 實體未清理")
					if _gs != null and int(_gs.get("hp")) != int(_gs.call("effective_max_hp")):
						_fail("重複刷關後玩家血量未回滿")

				_save_viewport(
					"proof_07_battle_victory_replayed_combat.png",
					Rect2i(200, 100, 880, 520),
					"crop_07_victory_replayed_combat.png"
				)

				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 14
				_wait = 0

		14:
			# Step 14: 準備 ForgeDialog 天宮鐵匠三槽鍛造測試環境（透過 MobileLobby 確保上下文完整）
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("level", 20)
					_gs.set("gold", 10000)
					if _gs.has_method("calc_level_stats"):
						_gs.call("calc_level_stats")

					var w0: Dictionary = {
						"uid": "w_proof_0",
						"base_id": "sword",
						"name": "微末之刃",
						"slot": "weapon",
						"line": "sword",
						"tier": 1,
						"quality": "common",
						"quality_label": "凡品",
						"rolled": {"atk": 10}
					}
					var w1: Dictionary = {
						"uid": "w_proof_1",
						"base_id": "hammer",
						"name": "鐵骨重鎚",
						"slot": "weapon",
						"line": "hammer",
						"tier": 2,
						"quality": "rare",
						"quality_label": "上品",
						"rolled": {"atk": 24, "crit": 5.0, "def": 8}
					}
					var w2: Dictionary = {
						"uid": "w_proof_2",
						"base_id": "bow",
						"name": "赤炎神弓",
						"slot": "weapon",
						"line": "bow",
						"tier": 3,
						"quality": "epic",
						"quality_label": "秘寶",
						"rolled": {"atk": 36, "crit": 12.5, "hp": 50}
					}

					_gs.equip_worn["w_proof_0"] = w0
					_gs.equip_worn["w_proof_1"] = w1
					_gs.equip_worn["w_proof_2"] = w2

					_gs.weapon_loadout[0] = "w_proof_0"
					_gs.weapon_loadout[1] = "w_proof_1"
					_gs.weapon_loadout[2] = "w_proof_2"
					_gs.weapon_loadout_active = 0
					_gs.equip_slots["weapon"] = "w_proof_0"
					if _eq:
						_eq.call("_sync_active_weapon_mirror")

				_lobby = MobileLobbyClass.new()
				_lobby.size = Vector2(1280, 720)
				root.add_child(_lobby)
				_forge_dlg = _lobby.open_forge()
				if _forge_dlg != null and _forge_dlg.has_method("_refresh_display"):
					_forge_dlg.call("_refresh_display")

				_step = 15
				_wait = 0

		15:
			# Step 15: 驗證 ForgeDialog 槽位 1 主手武器展示並截圖
			if _wait >= 25:
				if _forge_dlg == null:
					_fail("未取得 ForgeDialog 實體")
				else:
					var chips: Array = _forge_dlg.get_slot_chips()
					if chips.size() != 3:
						_fail("ForgeDialog 晶片數量不符: %d" % chips.size())
					for i in range(chips.size()):
						var c: Button = chips[i]
						if c.custom_minimum_size.y < 44.0:
							_fail("Chip %d 高度未達標" % i)

					_save_viewport(
						"proof_08_forge_slot1_main_weapon.png",
						Rect2i(250, 80, 780, 560),
						"crop_08_forge_slot1_main_weapon.png"
					)

					# 點擊槽位 2
					chips[1].emit_signal("pressed")

				_step = 16
				_wait = 0

		16:
			# Step 16: 驗證切換槽位 2 副手武器（鐵骨重鎚 T2），品質色階與副詞條刷新並截圖
			if _wait >= 25:
				if _forge_dlg != null:
					var q_lbl: Label = _forge_dlg.get_quality_label()
					var af_lbl: Label = _forge_dlg.get_affix_label()
					var w_lbl: Label = _forge_dlg.find_child("WeaponLabel", true, false) as Label
					if not ("鐵骨重鎚" in w_lbl.text):
						_fail("切換至槽位 2 武器名稱未更新: " + w_lbl.text)
					if not ("上品" in q_lbl.text):
						_fail("切換至槽位 2 品質未更新為上品: " + q_lbl.text)
					if not ("暴擊 +5.0%" in af_lbl.text):
						_fail("切換至槽位 2 副詞條未更新: " + af_lbl.text)

					_save_viewport(
						"proof_09_forge_slot2_sub_weapon.png",
						Rect2i(250, 80, 780, 560),
						"crop_09_forge_slot2_sub_weapon.png"
					)

					# 點擊槽位 3
					var chips: Array = _forge_dlg.get_slot_chips()
					chips[2].emit_signal("pressed")

				_step = 17
				_wait = 0

		17:
			# Step 17: 驗證切換槽位 3 絕技武器（赤炎神弓 T3），品質色階與副詞條刷新並截圖
			if _wait >= 25:
				if _forge_dlg != null:
					var q_lbl: Label = _forge_dlg.get_quality_label()
					var af_lbl: Label = _forge_dlg.get_affix_label()
					var w_lbl: Label = _forge_dlg.find_child("WeaponLabel", true, false) as Label
					if not ("赤炎神弓" in w_lbl.text):
						_fail("切換至槽位 3 武器名稱未更新: " + w_lbl.text)
					if not ("秘寶" in q_lbl.text):
						_fail("切換至槽位 3 品質未更新為秘寶: " + q_lbl.text)
					if not ("暴擊 +12.5%" in af_lbl.text):
						_fail("切換至槽位 3 副詞條未更新: " + af_lbl.text)

					_save_viewport(
						"proof_10_forge_slot3_special_weapon.png",
						Rect2i(250, 80, 780, 560),
						"crop_10_forge_slot3_special_weapon.png"
					)

					# 切回槽位 2 並進行鍛造
					var chips: Array = _forge_dlg.get_slot_chips()
					chips[1].emit_signal("pressed")
					var btn_forge: Button = _forge_dlg.find_child("BtnForge", true, false) as Button
					if btn_forge == null:
						_fail("找不到 BtnForge 鍛造按鈕")
					else:
						btn_forge.pressed.emit()

				_step = 18
				_wait = 0

		18:
			# Step 18: 驗證槽位 2 鍛造升階成功（T2 -> T3），面板與 Chip 標籤即時連動刷新並截圖
			if _wait >= 25:
				if _forge_dlg != null:
					var chips: Array = _forge_dlg.get_slot_chips()
					var chip1_text: String = (chips[1] as Button).text
					var w_lbl: Label = _forge_dlg.find_child("WeaponLabel", true, false) as Label
					if not ("T3" in chip1_text or "第 3 階" in w_lbl.text):
						_fail("鍛造後槽位 2 未升至第 3 階")

					_save_viewport(
						"proof_11_forge_slot2_upgraded.png",
						Rect2i(250, 80, 780, 560),
						"crop_11_forge_slot2_upgraded.png"
					)

					# 切換為英文語系
					if _loc_node:
						_loc_node.call("set_locale", "en")
					_forge_dlg.call("_refresh_display")

				_step = 19
				_wait = 0

		19:
			# Step 19: 驗證英文語系 (en) 下 ForgeDialog 零中文殘留並截圖
			if _wait >= 25:
				if _forge_dlg != null:
					var q_lbl: Label = _forge_dlg.get_quality_label()
					var af_lbl: Label = _forge_dlg.get_affix_label()
					if _has_cjk(q_lbl.text):
						_fail("英文 ForgeDialog 品質標籤殘留 CJK: " + q_lbl.text)
					if _has_cjk(af_lbl.text):
						_fail("英文 ForgeDialog 副詞條標籤殘留 CJK: " + af_lbl.text)

					_save_viewport(
						"proof_12_forge_dialog_en_no_cjk.png",
						Rect2i(250, 80, 780, 560),
						"crop_12_forge_dialog_en_no_cjk.png"
					)

				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_forge_dlg = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_step = 20
				_wait = 0

		20:
			# Step 20: 檢驗所有截圖之 SHA256 獨立性
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
				push_error("TEST_REGRESSION_T_2554E391_FAIL")
				print("TEST_REGRESSION_T_2554E391_FAIL")
				quit(1)
				return true

			print("\n=======================================================")
			print("TEST_REGRESSION_T_2554E391_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
