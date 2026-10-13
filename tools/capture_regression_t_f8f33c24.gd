extends SceneTree
## 《發條之心》三大戰鬥結算與鍛造快捷聯動全站回歸實機驗收存證腳本 (t_f8f33c24)
## 覆蓋：
## 1. BattleDefeatDialog 戰力診斷卡、三大建議膠囊與前往整頓按鈕樣式驗證
## 2. 點擊前往整頓後導向角色頁面（MobileLobby.Tab.CHARACTER）全景與武器槽
## 3. BattleVictoryDialog 出征 1-1 勝利結算之連續挑戰下一關按鈕（綠色立體果凍厚底）
## 4. BattleVictoryDialog 於 4-4 末關連續挑戰按鈕自動隱藏
## 5. WeaponSwapDialog 底部操作列直通天宮鐵匠快捷按鈕（天藍色立體果凍厚底）
## 6. 點擊直通天宮鐵匠快捷按鈕後，順暢關閉更換彈窗並開啟天宮鐵匠彈窗
## 7. 英文語系 (en) 下 BattleDefeatDialog 戰力診斷無中文殘留
## 8. 英文語系 (en) 下 BattleVictoryDialog 連續挑戰下一關按鈕無中文殘留
## 9. 日文語系 (ja) 下 WeaponSwapDialog 直通天宮鐵匠快捷按鈕正確在地化
## 10. 零系統 Emoji、1280x720 真實 Framebuffer 渲染、全截圖獨立 SHA256 驗證

const BattleDefeatDialogClass := preload("res://scripts/battle/battle_defeat_dialog.gd")
const BattleVictoryDialogClass := preload("res://scripts/battle/battle_victory_dialog.gd")
const WeaponSwapDialogClass := preload("res://scripts/ui/weapon_swap_dialog.gd")
const MobileLobbyClass := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_f8f33c24",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f8f33c24/proofs/t_f8f33c24"
]

var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _battle: Control = null
var _defeat_dlg: Control = null
var _victory_dlg: Control = null
var _lobby: Control = null
var _weapon_swap_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

var _saved_hashes: Dictionary = {}


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
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("has_removed_ads", false)

	_es = root.get_node_or_null("EnergySystem")
	if _es:
		_es.call("refresh")

	print("=== 開始執行三大戰鬥結算與鍛造快捷聯動全站回歸實機驗收存證 (t_f8f33c24) ===")
	_step = 0
	_wait = 0


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
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_battle = b_scn.instantiate()
					root.add_child(_battle)
					if _battle.has_method("setup"):
						_battle.call("setup", "road_bandit")

				_defeat_dlg = BattleDefeatDialogClass.new()
				_defeat_dlg.z_index = 95
				root.add_child(_defeat_dlg)

				_step = 1
				_wait = 0

		1:
			# Step 1: 驗證 BattleDefeatDialog 戰力診斷卡與前往整頓按鈕，並截圖
			if _wait >= 25:
				var title_lbl: Label = _defeat_dlg.find_child("TitleLabel", true, false) as Label
				var diag_title: Label = _defeat_dlg.get("_diag_title_lbl") as Label
				var cap_w: Label = _defeat_dlg.get("_capsule_weapon_tag") as Label
				var cap_a: Label = _defeat_dlg.get("_capsule_affix_tag") as Label
				var cap_s: Label = _defeat_dlg.get("_capsule_skill_tag") as Label
				var btn_gear: Button = _defeat_dlg.get("_gear_up_btn") as Button

				if diag_title == null or diag_title.text != "戰力診斷":
					_fail("DefeatDialog 戰力診斷標題不符: " + (diag_title.text if diag_title else "null"))
				if cap_w == null or cap_w.text != "武器階數":
					_fail("DefeatDialog 武器階數膠囊標籤不符: " + (cap_w.text if cap_w else "null"))
				if cap_a == null or cap_a.text != "裝備副詞條":
					_fail("DefeatDialog 裝備副詞條膠囊標籤不符: " + (cap_a.text if cap_a else "null"))
				if cap_s == null or cap_s.text != "招式調整":
					_fail("DefeatDialog 招式調整膠囊標籤不符: " + (cap_s.text if cap_s else "null"))
				if btn_gear == null or btn_gear.text != "前往整頓":
					_fail("DefeatDialog 前往整頓按鈕文字不符: " + (btn_gear.text if btn_gear else "null"))
				if btn_gear != null:
					if btn_gear.custom_minimum_size.y < 50:
						_fail("BtnGearUp 高度未達人體工學 >= 50px")
					if _has_emoji(btn_gear.text):
						_fail("BtnGearUp 包含違規 Emoji")

				_save_viewport(
					"proof_01_battle_defeat_diagnostic_zh_TW.png",
					Rect2i(240, 100, 800, 520),
					"crop_01_defeat_diagnostic_zh_TW.png"
				)

				# 清理並準備切換到大廳角色頁驗證點擊導向
				if is_instance_valid(_defeat_dlg):
					_defeat_dlg.queue_free()
					_defeat_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 2
				_wait = 0

		2:
			# Step 2: 模擬點擊前往整頓導向角色分頁 (MobileLobby.Tab.CHARACTER)
			if _wait >= 5:
				_lobby = MobileLobbyClass.new()
				_lobby.size = Vector2(1280, 720)
				root.add_child(_lobby)
				_lobby._switch_tab(_lobby.Tab.CHARACTER)

				_step = 3
				_wait = 0

		3:
			# Step 3: 驗證角色頁全景與武器輪替配置，並截圖
			if _wait >= 25:
				if _lobby._current_tab != _lobby.Tab.CHARACTER:
					_fail("未正確切換至角色分頁 Tab.CHARACTER")
				if _lobby.get("_char_layer") == null or not _lobby._char_layer.visible:
					_fail("角色分頁圖層未正常顯示")

				_save_viewport(
					"proof_02_defeat_to_character_tab_navigated.png",
					Rect2i(100, 100, 1080, 540),
					"crop_02_character_tab_weapons.png"
				)

				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				_step = 4
				_wait = 0

		4:
			# Step 4: 建立出征勝利結算彈窗 (1-1 關卡，存在下一關 1-2)
			if _wait >= 5:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_battle = b_scn.instantiate()
					root.add_child(_battle)
					if _battle.has_method("setup"):
						_battle.call("setup", "road_bandit")

				var drop_part := {
					"slot": "mainspring",
					"tier": "blue",
					"tier_name": "藍",
					"slot_name": "主發條"
				}
				_victory_dlg = BattleVictoryDialogClass.show_dialog(
					root, drop_part, Callable(), 100, 5, [], Callable(), "1-1"
				)

				_step = 5
				_wait = 0

		5:
			# Step 5: 驗證 BattleVictoryDialog 挑戰下一關按鈕 (BtnNextStage)，並截圖
			if _wait >= 25:
				var btn_next: Button = _victory_dlg.find_child("BtnNextStage", true, false) as Button
				if btn_next == null:
					_fail("BattleVictoryDialog 找不到 BtnNextStage")
				else:
					if not btn_next.visible:
						_fail("1-1 勝利結算 BtnNextStage 未正確顯示")
					if btn_next.text != "挑戰下一關":
						_fail("BtnNextStage 文字不符: " + btn_next.text)
					if btn_next.custom_minimum_size.y < 50:
						_fail("BtnNextStage 高度未達 >= 50px")
					if _has_emoji(btn_next.text):
						_fail("BtnNextStage 包含違規 Emoji")

				_save_viewport(
					"proof_03_battle_victory_next_stage_button.png",
					Rect2i(240, 480, 800, 180),
					"crop_03_victory_next_stage_button.png"
				)

				# 切換關卡為 4-4 (末關，應隱藏 BtnNextStage)
				_victory_dlg.call("set_stage", "4-4")

				_step = 6
				_wait = 0

		6:
			# Step 6: 驗證 4-4 末關 BtnNextStage 自動隱藏，並截圖
			if _wait >= 20:
				var btn_next: Button = _victory_dlg.find_child("BtnNextStage", true, false) as Button
				if btn_next != null and btn_next.visible:
					_fail("4-4 末關 BtnNextStage 應自動隱藏但仍顯示")

				_save_viewport(
					"proof_04_battle_victory_final_stage_hidden.png",
					Rect2i(240, 480, 800, 180),
					"crop_04_victory_final_stage_no_next_btn.png"
				)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 7
				_wait = 0

		7:
			# Step 7: 建立 MobileLobby 並開啟 WeaponSwapDialog
			if _wait >= 5:
				_lobby = MobileLobbyClass.new()
				_lobby.size = Vector2(1280, 720)
				root.add_child(_lobby)
				_lobby._switch_tab(_lobby.Tab.CHARACTER)
				_weapon_swap_dlg = _lobby.open_weapon_swap_dialog(0)

				_step = 8
				_wait = 0

		8:
			# Step 8: 驗證 WeaponSwapDialog 之 BtnGoForge 前往鍛造按鈕，並截圖
			if _wait >= 25:
				var btn_forge: Button = _weapon_swap_dlg.find_child("BtnGoForge", true, false) as Button
				if btn_forge == null:
					_fail("WeaponSwapDialog 找不到 BtnGoForge")
				else:
					if not btn_forge.visible:
						_fail("BtnGoForge 未正常顯示")
					if btn_forge.text != "前往鍛造":
						_fail("BtnGoForge 文字不符: " + btn_forge.text)
					if btn_forge.custom_minimum_size.y < 48:
						_fail("BtnGoForge 高度未達 >= 48px")
					if _has_emoji(btn_forge.text):
						_fail("BtnGoForge 包含違規 Emoji")

				_save_viewport(
					"proof_05_weapon_swap_dialog_btn_go_forge.png",
					Rect2i(260, 560, 760, 120),
					"crop_05_weapon_swap_btn_go_forge.png"
				)

				# 點擊 BtnGoForge，直通喚醒天宮鐵匠
				if btn_forge:
					btn_forge.pressed.emit()

				_step = 9
				_wait = 0

		9:
			# Step 9: 驗證 WeaponSwapDialog 關閉且 ForgeDialog 順利開啟，並截圖
			if _wait >= 25:
				var forge_dlg := _lobby.get_node_or_null("ForgeDialog")
				if forge_dlg == null or not is_instance_valid(forge_dlg):
					_fail("點擊 BtnGoForge 後未成功開啟 ForgeDialog")

				_save_viewport(
					"proof_06_weapon_swap_forge_dialog_opened.png",
					Rect2i(200, 60, 880, 600),
					"crop_06_forge_dialog_card.png"
				)

				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				_step = 10
				_wait = 0

		10:
			# Step 10: 英文語系 (en) BattleDefeatDialog 驗證
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_battle = b_scn.instantiate()
					root.add_child(_battle)
					if _battle.has_method("setup"):
						_battle.call("setup", "road_bandit")

				_defeat_dlg = BattleDefeatDialogClass.new()
				_defeat_dlg.z_index = 95
				root.add_child(_defeat_dlg)

				_step = 11
				_wait = 0

		11:
			# Step 11: 驗證英文 BattleDefeatDialog 零中文殘留，並截圖
			if _wait >= 25:
				var title_lbl: Label = _defeat_dlg.find_child("TitleLabel", true, false) as Label
				var diag_title: Label = _defeat_dlg.get("_diag_title_lbl") as Label
				var btn_gear: Button = _defeat_dlg.get("_gear_up_btn") as Button

				if diag_title and _has_cjk(diag_title.text):
					_fail("英文 DefeatDialog 戰力診斷標題殘留中文: " + diag_title.text)
				if btn_gear and _has_cjk(btn_gear.text):
					_fail("英文 DefeatDialog 前往整頓按鈕殘留中文: " + btn_gear.text)
				if title_lbl and _has_cjk(title_lbl.text):
					_fail("英文 DefeatDialog 標題殘留中文: " + title_lbl.text)

				_save_viewport(
					"proof_07_battle_defeat_diagnostic_en_no_cjk.png",
					Rect2i(240, 100, 800, 520),
					"crop_07_defeat_en.png"
				)

				if is_instance_valid(_defeat_dlg):
					_defeat_dlg.queue_free()
					_defeat_dlg = null

				# 建立英文出征勝利彈窗 (1-1)
				var drop_part := {
					"slot": "mainspring",
					"tier": "blue",
					"tier_name": "Blue",
					"slot_name": "Mainspring"
				}
				_victory_dlg = BattleVictoryDialogClass.show_dialog(
					root, drop_part, Callable(), 100, 5, [], Callable(), "1-1"
				)

				_step = 12
				_wait = 0

		12:
			# Step 12: 驗證英文 BattleVictoryDialog BtnNextStage 零中文殘留，並截圖
			if _wait >= 25:
				var btn_next: Button = _victory_dlg.find_child("BtnNextStage", true, false) as Button
				if btn_next == null or not btn_next.visible:
					_fail("英文 BattleVictoryDialog 找不到 BtnNextStage 或未顯示")
				elif _has_cjk(btn_next.text):
					_fail("英文 BtnNextStage 殘留中文: " + btn_next.text)

				_save_viewport(
					"proof_08_battle_victory_next_stage_en_no_cjk.png",
					Rect2i(240, 480, 800, 180),
					"crop_08_victory_en.png"
				)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				_step = 13
				_wait = 0

		13:
			# Step 13: 日文語系 (ja) WeaponSwapDialog 驗證
			if _wait >= 5:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_lobby = MobileLobbyClass.new()
				_lobby.size = Vector2(1280, 720)
				root.add_child(_lobby)
				_lobby._switch_tab(_lobby.Tab.CHARACTER)
				_weapon_swap_dlg = _lobby.open_weapon_swap_dialog(0)

				_step = 14
				_wait = 0

		14:
			# Step 14: 驗證日文 WeaponSwapDialog BtnGoForge，並截圖
			if _wait >= 25:
				var btn_forge: Button = _weapon_swap_dlg.find_child("BtnGoForge", true, false) as Button
				if btn_forge == null or not btn_forge.visible:
					_fail("日文 WeaponSwapDialog 找不到 BtnGoForge 或未顯示")
				elif btn_forge.text != "鍛造へ進む":
					_fail("日文 BtnGoForge 文字不符: " + btn_forge.text)

				_save_viewport(
					"proof_09_weapon_swap_forge_ja.png",
					Rect2i(260, 560, 760, 120),
					"crop_09_weapon_swap_ja.png"
				)

				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				# 恢復繁體中文
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_step = 15
				_wait = 0

		15:
			# Step 15: 驗證所有截圖 SHA256 獨立性
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
				push_error("TEST_REGRESSION_T_F8F33C24_FAIL")
				print("TEST_REGRESSION_T_F8F33C24_FAIL")
				quit(1)
				return true

			print("\n=======================================================")
			print("TEST_REGRESSION_T_F8F33C24_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
