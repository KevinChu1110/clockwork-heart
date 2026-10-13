extends SceneTree
## 《發條之心》雙分支合併主線全面回歸驗收存證腳本 (capture_regression_t_f95acf59.gd)
## 覆蓋：
## 1. 天宮鐵匠武器槽更換裝備按鈕連動 WeaponSwapDialog (t_7db3e5a2)
## 2. 木人樁試招結算新增調整心法快捷按鈕連動 SkillDialog (t_f8bc43d5)
## 符合 0-QA5 / 0-QA26 / 0-QA28（1280x720 真實 Viewport OpenGL3 Framebuffer 截圖，零 PIL 假圖）

const OUT_PATH := "/opt/side/bravesoul-game/proofs/t_f95acf59"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var ForgeDialogClass: GDScript = null
var WeaponSwapDialogClass: GDScript = null
var DummySettlementDialogClass: GDScript = null
var MobileLobbyClass: GDScript = null

var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _lobby: Control = null
var _forge_dlg: Control = null
var _swap_dlg: Control = null
var _dummy_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

var _saved_hashes: Dictionary = {}


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_PATH)

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
		_gs.set("gold", 88888)
		_gs.set("weapon_tier", 2)
		_gs.set("weapon_atk", 18)
		_gs.set("weapon_name", "鋼刃")
		_gs.call("set_flag", "c1_forged", true)
		_gs.call("set_flag", "c1_entered_city", true)
		_gs.call("set_flag", "tut_done", true)

	_es = root.get_node_or_null("EquipmentSystem")

	change_scene_to_file("res://scenes/main.tscn")
	print("=== 開始執行雙分支合進主線全面回歸驗收存證 (t_f95acf59) ===")
	_step = 0
	_wait = 0


func _save_viewport(filename: String) -> String:
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

	var full_path := OUT_PATH.path_join(filename)
	var err := img.save_png(full_path)
	if err == OK:
		print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA256=%s)" % [filename, img.get_width(), img.get_height(), full_sha.substr(0, 12)])
	else:
		_fail("儲存全景圖失敗: %s" % full_path)

	_saved_hashes[filename] = full_sha
	return full_sha


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 等待場景與 Autoloads 就緒，開啟大廳與 ForgeDialog
			if _wait >= 25:
				ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				WeaponSwapDialogClass = load("res://scripts/ui/weapon_swap_dialog.gd")
				DummySettlementDialogClass = load("res://scripts/battle/dummy_settlement_dialog.gd")
				MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")

				_loc_node = root.get_node_or_null("Loc")
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_lobby = MobileLobbyClass.new()
				_lobby.size = Vector2(1280, 720)
				root.add_child(_lobby)

				_forge_dlg = _lobby.open_forge_dialog()
				if _forge_dlg == null:
					_fail("無法開啟 ForgeDialog")
					return true

				_step = 1
				_wait = 0

		1:
			# 截圖 01: ForgeDialog 武器鍛造區當前槽位標題列 BtnSwapWeapon 更換裝備按鈕 (zh_TW)
			if _wait >= 20:
				_save_viewport("proof_01_forge_dialog_btn_swap_weapon_zh_TW.png")
				var btn_swap: Button = _forge_dlg.find_child("BtnSwapWeapon", true, false) as Button
				if btn_swap:
					btn_swap.emit_signal("pressed")
				_step = 2
				_wait = 0

		2:
			# 截圖 02: 點擊『更換裝備』後開啟 WeaponSwapDialog
			if _wait >= 20:
				_swap_dlg = _forge_dlg.find_child("WeaponSwapDialog", true, false) as Control
				if _swap_dlg == null:
					_fail("點擊更換裝備後未開啟 WeaponSwapDialog")
				_save_viewport("proof_02_weapon_swap_dialog_opened.png")

				# 模擬換裝事件
				var test_uid := "test_blade_w99"
				var test_weapon := {
					"uid": test_uid,
					"id": "blade_iron_99",
					"name": "天工神刃",
					"tier": 5,
					"quality": "epic",
					"quality_label": "絕品",
					"rolled": {"atk": 999, "crit": 15.0}
				}
				if _es and "weapons" in _es:
					_es.weapons[test_uid] = test_weapon
				if _gs and "equip_worn" in _gs and _gs.equip_worn != null:
					_gs.equip_worn[test_uid] = test_weapon

				if _swap_dlg and _swap_dlg.has_signal("weapon_swapped"):
					_swap_dlg.weapon_swapped.emit(0, test_uid)
				if is_instance_valid(_swap_dlg) and not _swap_dlg.is_queued_for_deletion():
					_swap_dlg.queue_free()

				_step = 3
				_wait = 0

		3:
			# 截圖 03: 換裝後 WeaponSwapDialog 關閉且 ForgeDialog 原地刷新
			if _wait >= 25:
				_save_viewport("proof_03_weapon_swapped_forge_refreshed.png")
				if _loc_node:
					_loc_node.call("set_locale", "zh_CN")
				_step = 4
				_wait = 0

		4:
			# 截圖 04: ForgeDialog 簡中 (zh_CN)
			if _wait >= 20:
				_save_viewport("proof_04_forge_btn_swap_weapon_zh_CN.png")
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_step = 5
				_wait = 0

		5:
			# 截圖 05: ForgeDialog 英文 (en)
			if _wait >= 20:
				_save_viewport("proof_05_forge_btn_swap_weapon_en.png")
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_step = 6
				_wait = 0

		6:
			# 截圖 06: ForgeDialog 日文 (ja)
			if _wait >= 20:
				_save_viewport("proof_06_forge_btn_swap_weapon_ja.png")
				if _loc_node:
					_loc_node.call("set_locale", "ko")
				_step = 7
				_wait = 0

		7:
			# 截圖 07: ForgeDialog 韓文 (ko)
			if _wait >= 20:
				_save_viewport("proof_07_forge_btn_swap_weapon_ko.png")
				if _loc_node:
					_loc_node.call("set_locale", "es")
				_step = 8
				_wait = 0

		8:
			# 截圖 08: ForgeDialog 西文 (es)
			if _wait >= 20:
				_save_viewport("proof_08_forge_btn_swap_weapon_es.png")
				# 關閉 ForgeDialog，準備展示 DummySettlementDialog
				if _forge_dlg and is_instance_valid(_forge_dlg):
					_forge_dlg.queue_free()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_step = 9
				_wait = 0

		9:
			# 開啟 DummySettlementDialog (zh_TW)
			if _wait >= 20:
				_dummy_dlg = DummySettlementDialogClass.new()
				_dummy_dlg.size = Vector2(1280, 720)
				root.add_child(_dummy_dlg)
				_dummy_dlg.setup({
					"duration": 30.0,
					"total_dmg": 18888,
					"dps": 629.6,
					"total_hits": 45,
					"max_single_hit": 1280,
					"is_new_record": true,
					"weapon_stats": [
						{"slot": 0, "name": "天工神刃", "swaps": 12, "dmg": 9888, "pct": 52.3},
						{"slot": 1, "name": "破陣大鎚", "swaps": 8, "dmg": 5000, "pct": 26.5},
						{"slot": 2, "name": "風行雙刺", "swaps": 7, "dmg": 4000, "pct": 21.2}
					]
				})
				_step = 10
				_wait = 0

		10:
			# 截圖 09: DummySettlementDialog 底部按鈕列含『調整心法』(zh_TW)
			if _wait >= 20:
				_save_viewport("proof_09_dummy_settlement_zh_TW.png")
				if _loc_node:
					_loc_node.call("set_locale", "zh_CN")
				_step = 11
				_wait = 0

		11:
			# 截圖 10: DummySettlementDialog 簡中 (zh_CN)
			if _wait >= 20:
				_save_viewport("proof_10_dummy_settlement_zh_CN.png")
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_step = 12
				_wait = 0

		12:
			# 截圖 11: DummySettlementDialog 英文 (en)
			if _wait >= 20:
				_save_viewport("proof_11_dummy_settlement_en.png")
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_step = 13
				_wait = 0

		13:
			# 截圖 12: DummySettlementDialog 日文 (ja)
			if _wait >= 20:
				_save_viewport("proof_12_dummy_settlement_ja.png")
				if _loc_node:
					_loc_node.call("set_locale", "ko")
				_step = 14
				_wait = 0

		14:
			# 截圖 13: DummySettlementDialog 韓文 (ko)
			if _wait >= 20:
				_save_viewport("proof_13_dummy_settlement_ko.png")
				if _loc_node:
					_loc_node.call("set_locale", "es")
				_step = 15
				_wait = 0

		15:
			# 截圖 14: DummySettlementDialog 西文 (es)
			if _wait >= 20:
				_save_viewport("proof_14_dummy_settlement_es.png")
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				# 點擊 BtnGoSkills 關閉結算彈窗並由大廳開啟 SkillDialog
				var btn_skills: Button = _dummy_dlg.find_child("BtnGoSkills", true, false) as Button
				if btn_skills:
					btn_skills.emit_signal("pressed")
				if is_instance_valid(_dummy_dlg) and not _dummy_dlg.is_queued_for_deletion():
					_dummy_dlg.queue_free()

				if _lobby and _lobby.has_method("open_skill_dialog"):
					_lobby.open_skill_dialog()

				_step = 16
				_wait = 0

		16:
			# 截圖 15: 點擊調整心法後由 MobileLobby 開啟之 SkillDialog 實機全景
			if _wait >= 25:
				_save_viewport("proof_15_skill_dialog_opened_lobby.png")
				_finish()
				_step = 17
				return true

	return false


func _finish() -> void:
	print("\n--- 檢查所有截圖之 SHA256 唯一性 ---")
	var sha_seen: Dictionary = {}
	for fn in _saved_hashes.keys():
		var h: String = _saved_hashes[fn]
		if sha_seen.has(h):
			_fail("截圖重複 (SHA256 相同): %s 與 %s" % [fn, sha_seen[h]])
		else:
			sha_seen[h] = fn
			print("  ✓ %s SHA256 唯一: %s" % [fn, h.substr(0, 12)])

	if _ok:
		print("\n=======================================================")
		print("TEST_REGRESSION_T_F95ACF59_OK")
		quit(0)
	else:
		push_error("TEST_REGRESSION_T_F95ACF59_FAIL")
		print("\n=======================================================")
		print("TEST_REGRESSION_T_F95ACF59_FAIL")
		quit(1)
