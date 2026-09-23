extends SceneTree
## QA Round 25: 玄機龜紙娃娃與大廳頭像備援合併後全流程實機截圖與找破圖驗收腳本
## 涵蓋：
## 1. 玄機龜創角畫面與確認後流轉至大廳展示
## 2. 衣櫥「全部」與「玄機龜」種族篩選及換裝驗收
## 3. 大廳頭像與六語系（zh_TW, zh_CN, en, ja, ko, es）即時刷新與對照
## 4. 戰鬥畫面玄機龜出戰與戰鬥名稱備援對照（含空名 fallback 與戰鬥日誌）
## 5. 近期改動回歸：大廳連動商城即時刷新（0-QA25 檢查）
## 6. 細節 Crops 產生

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round25"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round25/crops"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行 QA Round 25 玄機龜與全流程探索性截圖 ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角介面 (PaperdollSelectDemo) 選中玄機龜
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "tortoise")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "tortoise")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 25:
				var path := "%s/proof_01_creation_tortoise.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/14] 已截取玄機龜創角畫面: %s" % path)
				# 驗證確認創角動作
				if _current_node and _current_node.has_method("confirm_selection"):
					_current_node.call("confirm_selection")
					print("    GameState 創角後種族: %s, 英雄名: %s" % [_gs.get("player_race"), _gs.get("player_name")])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 開啟衣櫥 (WardrobeDialog)，篩選「全部」
			if _wait == 1:
				var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
				if WardrobeClass:
					var dlg = WardrobeClass.new()
					root.add_child(dlg)
					_current_node = dlg
			elif _wait == 10:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "all")
			elif _wait >= 30:
				var path := "%s/proof_02_wardrobe_filter_all.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/14] 已截取衣櫥全部篩選狀態: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 衣櫥切換為「玄機龜」篩選，滾動顯示第十族 chip
			if _wait == 5:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "tortoise")
			elif _wait == 15:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait >= 30:
				var path := "%s/proof_03_wardrobe_filter_tortoise.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/14] 已截取衣櫥玄機龜篩選狀態: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 衣櫥換裝玄機龜道場護甲與青銅古翠綠塗裝
			if _wait == 5:
				if _current_node:
					if _current_node.has_method("select_costume"):
						_current_node.call("select_costume", "costume_zen_dojo_harness")
					if _current_node.has_method("select_chassis"):
						_current_node.call("select_chassis", "paint_tortoise_jade")
			elif _wait >= 30:
				var path := "%s/proof_04_wardrobe_tortoise_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/14] 已截取衣櫥玄機龜換裝後狀態: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 建立手遊大廳 (MobileLobby)，準備六語系循環展示
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "tortoise")
					_gs.set("player_race", "tortoise")
					_gs.set("player_name", "玄機龜")
					_gs.set("energy", 15)
					_gs.set("gold", 12800)
					_gs.set("stardust", 108)
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 30:
				_step = 6
				_wait = 0

		6, 7, 8, 9, 10, 11:
			# 步驟 6~11: 六語系大廳實機截圖 (zh_TW, zh_CN, en, ja, ko, es)
			var loc_idx := _step - 6
			var code: String = LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
			elif _wait >= 25:
				var path := "%s/proof_05_lobby_tortoise_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/14] 已截取大廳 [%s] 語系實機截圖: %s" % [loc_idx + 5, code, path])
				_log_lobby_audit(code)
				_step += 1
				_wait = 0

		12:
			# 步驟 12: 商城與大廳即時刷新驗收 (0-QA25 檢查，以 en 英文大廳開啟商城彈窗)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
			elif _wait == 10:
				if _current_node and _current_node.has_method("open_shop"):
					_current_node.call("open_shop")
			elif _wait >= 35:
				var path := "%s/proof_11_lobby_with_shop_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [11/14] 已截取大廳連動商城即時刷新 (en): %s" % path)
				var shop = _current_node.get_node_or_null("ShopDialog")
				if shop:
					shop.queue_free()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 13
				_wait = 0

		13:
			# 步驟 13: 戰鬥畫面 (BattleView) 玄機龜出戰驗證
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "tortoise")
					_gs.set("player_race", "tortoise")
					_gs.set("player_name", "玄機龜")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait >= 30:
				var path := "%s/proof_12_battle_tortoise.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [12/14] 已截取戰鬥畫面玄機龜出戰: %s" % path)
				_step = 14
				_wait = 0

		14:
			# 步驟 14: 戰鬥名稱備援對照驗證 (player_name 為空時 fallback 各族名與戰鬥日誌)
			if _wait == 5:
				if _current_node:
					_gs.set("player_name", "")
					var saved_sim = _current_node.get("sim")
					_current_node.set("sim", null)
					var fallback_name: String = _current_node.call("_unit_display_name", "player")
					print("    戰鬥備援名稱 (空名 fallback): %s" % fallback_name)
					_current_node.set("sim", saved_sim)

					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 36,
						"crit": true,
						"hp": 64,
						"max_hp": 100
					})
			elif _wait >= 30:
				var path := "%s/proof_13_battle_fallback_empty_name.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [13/14] 已截取戰鬥空名備援與戰鬥日誌: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 15
				_wait = 0

		15:
			# 步驟 15: 特寫裁切 (Crops)
			_generate_crops()
			print("── QA Round 25 截圖全數完成 ──")
			quit(0)
			return true

	return false


func _log_lobby_audit(code: String) -> void:
	if _current_node == null:
		return
	var shop_btn: Button = _current_node.get_shop_button() if _current_node.has_method("get_shop_button") else null
	var set_btn: Button = _current_node.get_settings_button() if _current_node.has_method("get_settings_button") else null
	var sortie_btn: Button = _current_node.get_sortie_button() if _current_node.has_method("get_sortie_button") else null
	var pwr_lbl: Label = _current_node.get("_power_label")
	var nrg_title: Label = _current_node.get("_energy_title_label")
	var gold_title: Label = _current_node.get("_gold_title_label")
	var gem_title: Label = _current_node.get("_gem_title_label")
	var avatar: TextureRect = _current_node.get("_profile_avatar")
	var avatar_path: String = avatar.texture.resource_path if avatar and avatar.texture else "none"

	print("    [%s 稽核] 頭像路徑: %s" % [code, avatar_path])
	print("    [%s 稽核] 頂部狀態: 能量=%s, 金幣=%s, 星屑=%s, %s" % [
		code,
		nrg_title.text if nrg_title else "null",
		gold_title.text if gold_title else "null",
		gem_title.text if gem_title else "null",
		pwr_lbl.text if pwr_lbl else "null"
	])
	print("    [%s 稽核] 按鈕: 商城=%s, 設置=%s, 出征=%s" % [
		code,
		shop_btn.text if shop_btn else "null",
		set_btn.text if set_btn else "null",
		sortie_btn.text if sortie_btn else "null"
	])


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    Successfully wrote: %s" % abs_path)


func _generate_crops() -> void:
	var lobby_zh := "%s/proof_05_lobby_tortoise_zh_TW.png" % OUT_DIR
	if FileAccess.file_exists(lobby_zh):
		var img := Image.load_from_file(lobby_zh)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(30, 10, 260, 90))
			var crop_p := "%s/crop_lobby_avatar_profile.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

			var char_crop := img.get_region(Rect2i(500, 280, 280, 320))
			var char_crop_p := "%s/crop_lobby_tortoise_char.png" % CROPS_DIR
			char_crop.save_png(char_crop_p)
			print("  ✓ 已產出特寫: %s" % char_crop_p)

	var wd_tortoise := "%s/proof_03_wardrobe_filter_tortoise.png" % OUT_DIR
	if FileAccess.file_exists(wd_tortoise):
		var img := Image.load_from_file(wd_tortoise)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(270, 80, 740, 540))
			var crop_p := "%s/crop_wardrobe_tortoise_grid.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	var battle_p := "%s/proof_12_battle_tortoise.png" % OUT_DIR
	if FileAccess.file_exists(battle_p):
		var img := Image.load_from_file(battle_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(100, 30, 1080, 140))
			var crop_p := "%s/crop_battle_nameplates.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)
