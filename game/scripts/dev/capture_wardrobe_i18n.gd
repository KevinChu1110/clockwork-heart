extends SceneTree
## 衣櫥星紋斗篷／裸機素體／彈窗標題按鈕六語系落地實機截圖腳本 (wardrobe-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 蛙族進入衣櫥，展示「星紋斗篷」與「無外裝 (裸機素體)」在 zh_TW, en, ja 下即時翻譯。
## 2. 衣櫥彈窗大標題「發條衣櫥 · 英雄換裝」、副標、種族列提示、底部操作按鈕在 zh_TW, en, ja 下即時翻譯。
## 3. 大廳背景與底部 Dock 連動同步切換語系 (0-QA25)。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/wardrobe-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/wardrobe-i18n/crops"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["zh_TW", "en", "ja"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行衣櫥六語系落地實機截圖腳本 (wardrobe-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 步驟 1~3: 大廳開啟衣櫥，蛙選中第二套【星紋斗篷】，展示卡片翻譯、彈窗標題與底部按鈕，背景大廳與 Dock 同步換語系 (0-QA25)
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧簧蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "frog")
						# 選中第二套：星紋斗篷 (costume_astral_cape, index 1)
						wardrobe.set("costume_index", 1)
						wardrobe.set("selected_costume_id", "costume_astral_cape")
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 40:
				var path := "%s/proof_wardrobe_frog_astral_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 大廳連動衣櫥蛙選星紋斗篷 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		4, 5, 6:
			# 步驟 4~6: 大廳開啟衣櫥，蛙選中第三張【無外裝 (裸機素體)】，展示素體選取狀態與全翻譯
			var loc_idx := _step - 4
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧簧蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "frog")
						# 選中第三張：無外裝 (裸機素體) (none, index 2)
						wardrobe.set("costume_index", 2)
						wardrobe.set("selected_costume_id", "none")
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 40:
				var path := "%s/proof_wardrobe_frog_bare_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 大廳連動衣櫥蛙選裸機素體 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		7:
			# 截圖全部完成，產生局部 Crops 供顯微比對
			_generate_crops()
			print("── 衣櫥六語系落地實機截圖全數完成 ──")
			quit(0)
			return true

	return false


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
	for code in TEST_LOCALES:
		var w_path := "%s/proof_wardrobe_frog_astral_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(w_path):
			var img := Image.load_from_file(w_path)
			if img and not img.is_empty():
				# 1. 彈窗大標題與副標題區 (X:270~900, Y:75~145)
				var title_crop := img.get_region(Rect2i(270, 75, 630, 70))
				var title_p := "%s/crop_wardrobe_title_%s.png" % [CROPS_DIR, code]
				title_crop.save_png(title_p)
				print("  [Crop] 彈窗標題特寫 [%s]: %s" % [code, title_p])

				# 2. 右側卡片網格區 (外裝服飾兩張卡：星紋斗篷與無外裝素體) (X:520~1000, Y:200~370)
				var cards_crop := img.get_region(Rect2i(520, 200, 480, 170))
				var cards_p := "%s/crop_wardrobe_cards_%s.png" % [CROPS_DIR, code]
				cards_crop.save_png(cards_p)
				print("  [Crop] 衣櫥卡片特寫 [%s]: %s" % [code, cards_p])

				# 3. 底部操作按鈕區 (還原預設、隨機、確認換裝) (X:520~1000, Y:575~645)
				var actions_crop := img.get_region(Rect2i(520, 575, 480, 70))
				var actions_p := "%s/crop_wardrobe_actions_%s.png" % [CROPS_DIR, code]
				actions_crop.save_png(actions_p)
				print("  [Crop] 底部操作按鈕特寫 [%s]: %s" % [code, actions_p])

				# 4. 底部 Dock 區 (X:0~1280, Y:620~720) 驗證 0-QA25
				var dock_crop := img.get_region(Rect2i(0, 620, 1280, 100))
				var dock_p := "%s/crop_dock_%s.png" % [CROPS_DIR, code]
				dock_crop.save_png(dock_p)
				print("  [Crop] 底部Dock特寫 [%s]: %s" % [code, dock_p])
